"""Fetch the article pages behind the news listings and keep the HTML plus the whole page as text.

Sources of URLs: the GDELT listing (raw/gdelt/*.jsonl), the TrueNorth stories' source links, and the resolved
Google News links (raw/gnews/resolved.jsonl). Every pass re-reads them, takes the URLs not fetched yet (or fetched
with a retryable failure fewer than three times), and fetches them with worker threads interleaved by domain, at
most one request per domain every two seconds. The outcome of each fetch is one line in raw/pages/index.jsonl:

  status, final_url, bytes, truncated (the body hit the 8 MB cap), blocked (an access wall or bot check, judged on
  the title and first lines only), page_day (the page's own publication day), full_chars (whole-page text),
  paragraphs and body_chars (a heuristic article cut, for the review only), coverage, attempts.

coverage: full (an original page, whole), stub (a page with almost no text), blocked, truncated, none (no body).
Only 'full' is an original document the pipeline may read.

Files: raw/pages/<sha256-of-url>.html, .full.txt (whole page), .txt (the heuristic cut).
Stops when GDELT's progress file says it finished and nothing is pending, or after one pass with --once.
"""
import collections
import json
import os
import queue
import sys
import threading
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))
from common import (RAW, fetch, decode, article_paragraphs, page_text, title_of, published_day_of, is_truncated,
                    is_block_page, sha256_text, read_json, now_iso, log, main_guard)  # noqa: E402

GDELT = os.path.join(RAW, 'gdelt')
TRUENORTH_NEWS = os.path.join(RAW, 'truenorth', 'news')
RESOLVED = os.path.join(RAW, 'gnews', 'resolved.jsonl')
OUT = os.path.join(RAW, 'pages')
INDEX = os.path.join(OUT, 'index.jsonl')
WORKERS = 16
DOMAIN_GAP = 2.0
RETRYABLE = {0, 429, 500, 502, 503, 504}
MAX_ATTEMPTS = 3
SKIP_SUFFIXES = ('.pdf', '.jpg', '.png', '.mp4', '.mp3')
STUB_CHARS = 500


def listed_urls():
    """Every article URL we know of, with the listing's own facts about it."""
    seen = {}

    def add(url, row):
        url = (url or '').strip()
        if url and url not in seen and not url.lower().endswith(SKIP_SUFFIXES):
            seen[url] = row

    if os.path.isdir(GDELT):
        for name in sorted(os.listdir(GDELT)):
            if name.endswith('.jsonl'):
                with open(os.path.join(GDELT, name), encoding='utf-8') as handle:
                    for line in handle:
                        try:
                            row = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        add(row.get('url'), dict(row, source='gdelt'))
    if os.path.isdir(TRUENORTH_NEWS):
        for name in sorted(os.listdir(TRUENORTH_NEWS)):
            story = (read_json(os.path.join(TRUENORTH_NEWS, name), {}) or {}).get('story') or {}
            add(story.get('source_url'), {'url': story.get('source_url'), 'title': story.get('title'), 'source': 'truenorth'})
    if os.path.exists(RESOLVED):
        with open(RESOLVED, encoding='utf-8') as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                add(row.get('url'), {'url': row.get('url'), 'title': row.get('title'), 'source': 'gnews', 'day': row.get('day')})
    return seen


def index_state():
    """url -> (done: bool, attempts) from the index: done unless the last outcome is retryable and attempts remain."""
    state = {}
    if os.path.exists(INDEX):
        with open(INDEX, encoding='utf-8') as handle:
            for line in handle:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                attempts = record.get('attempts', 1)
                retryable = record.get('status') in RETRYABLE
                state[record['url']] = (not retryable or attempts >= MAX_ATTEMPTS, attempts)
    return state


HARD_REFUSALS = {401, 403, 451}
WALL_AFTER = 6            # this many hard refusals in a row and the domain is treated as walled for the pass


class DomainGate:
    """One request per domain per gap. A throttle (429, 5xx, no answer) widens the gap; a hard refusal (401, 403)
    does not slow the pass but, after several in a row, marks the domain walled so its remaining URLs are recorded
    as blocked without a request (an access wall answers every URL the same way)."""

    def __init__(self):
        self.lock = threading.Lock()
        self.next_allowed = collections.defaultdict(float)
        self.throttled = collections.Counter()
        self.refused_in_a_row = collections.Counter()
        self.walled = set()

    def wait(self, domain):
        while True:
            with self.lock:
                now = time.time()
                gap = DOMAIN_GAP * (1 + min(self.throttled[domain], 5))
                if self.next_allowed[domain] <= now:
                    self.next_allowed[domain] = now + gap
                    return
                delay = self.next_allowed[domain] - now
            time.sleep(min(delay, 2.0))

    def is_walled(self, domain):
        with self.lock:
            return domain in self.walled

    def outcome(self, domain, status):
        with self.lock:
            if status in HARD_REFUSALS:
                self.refused_in_a_row[domain] += 1
                if self.refused_in_a_row[domain] >= WALL_AFTER:
                    self.walled.add(domain)
            elif status == 200:
                self.refused_in_a_row[domain] = 0
            else:
                self.throttled[domain] += 1

    @property
    def failures(self):
        return self.throttled + collections.Counter({d: WALL_AFTER for d in self.walled})


def fetch_one(row, attempts, gate, index_lock):
    url = row['url']
    domain = urllib.parse.urlsplit(url).netloc.lower()
    started = time.time()
    if gate.is_walled(domain):
        status, final_url, body = 403, url, b''
        walled = True
    else:
        gate.wait(domain)
        status, final_url, body = fetch(url, timeout=20, retries=0)
        walled = False
        gate.outcome(domain, status)
    record = {'url': url, 'final_url': final_url, 'status': status, 'domain': domain, 'fetched_at': now_iso(),
              'seconds': round(time.time() - started, 1), 'bytes': len(body), 'attempts': MAX_ATTEMPTS if walled else attempts,
              'truncated': False, 'blocked': walled, 'page_day': '', 'full_chars': 0, 'body_chars': 0, 'paragraphs': 0,
              'coverage': 'blocked' if walled else 'none', 'title': row.get('title'), 'seendate': row.get('seendate'),
              'listing': row.get('source'), 'walled_domain': walled}
    if status == 200 and body:
        truncated = is_truncated(body)
        markup = decode(body)
        full = page_text(markup)
        cut, paragraphs = article_paragraphs(markup)
        blocked = is_block_page(markup)
        key = sha256_text(url)
        with open(os.path.join(OUT, key + '.html'), 'wb') as handle:
            handle.write(body)
        with open(os.path.join(OUT, key + '.full.txt'), 'w', encoding='utf-8') as handle:
            handle.write(full)
        with open(os.path.join(OUT, key + '.txt'), 'w', encoding='utf-8') as handle:
            handle.write(cut)
        if truncated:
            coverage = 'truncated'
        elif blocked:
            coverage = 'blocked'
        elif len(full) < STUB_CHARS:
            coverage = 'stub'
        else:
            coverage = 'full'
        record.update({'file': key, 'truncated': truncated, 'blocked': blocked, 'page_day': published_day_of(markup),
                       'full_chars': len(full), 'body_chars': len(cut), 'paragraphs': paragraphs,
                       'page_title': title_of(markup)[:300], 'coverage': coverage})
    with index_lock:
        with open(INDEX, 'a', encoding='utf-8') as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + '\n')
    return record


def interleave_by_domain(rows):
    """Round-robin over domains so the workers are not all waiting on the same host's gap."""
    buckets = collections.OrderedDict()
    for row in rows:
        buckets.setdefault(urllib.parse.urlsplit(row['url']).netloc.lower(), []).append(row)
    ordered = []
    while buckets:
        for domain in list(buckets):
            ordered.append(buckets[domain].pop(0))
            if not buckets[domain]:
                del buckets[domain]
    return ordered


def one_pass(gate, index_lock):
    state = index_state()
    pending = []
    for url, row in listed_urls().items():
        done, attempts = state.get(url, (False, 0))
        if not done:
            pending.append((row, attempts + 1))
    log('pass: pending', len(pending))
    if not pending:
        return 0
    work = queue.Queue()
    for row in interleave_by_domain([dict(r, _attempts=a) for r, a in pending]):
        attempts = row.pop('_attempts')
        work.put((row, attempts))
    counts = collections.Counter()

    def worker():
        while True:
            try:
                row, attempts = work.get_nowait()
            except queue.Empty:
                return
            try:
                counts[fetch_one(row, attempts, gate, index_lock)['coverage']] += 1
            except Exception as error:  # one bad page never stops the pass; it is counted and retried next pass
                counts['exception'] += 1
                log('exception', row.get('url'), repr(error)[:120])
            finally:
                work.task_done()
                if sum(counts.values()) % 200 == 0:
                    log('progress', dict(counts))

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(WORKERS)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    log('pass done', dict(counts))
    return len(pending)


def run():
    os.makedirs(OUT, exist_ok=True)
    once = '--once' in sys.argv
    gate = DomainGate()
    index_lock = threading.Lock()
    while True:
        handled = one_pass(gate, index_lock)
        gdelt_done = bool(read_json(os.path.join(GDELT, 'progress.json'), {}).get('finished_at'))
        if once or (handled == 0 and gdelt_done):
            break
        if handled == 0:
            time.sleep(60)
    log('finished; domains with failures:', gate.failures.most_common(15))


if __name__ == '__main__':
    main_guard(run)
