"""Resolve Google News RSS links to the publishers' article URLs.

A Google News link (news.google.com/rss/articles/<id>) opens a page that embeds a signature and timestamp; a POST
to Google's batchexecute endpoint with those returns the real URL. Two requests per headline, a few workers, a
pause between requests, long waits on a refusal. Resumable: headlines already resolved (or already failed twice)
are skipped.

Reads raw/gnews/<day>.json; writes raw/gnews/resolved.jsonl (day, title, source, published, google_link, url, status).
"""
import json
import os
import queue
import re
import sys
import threading
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from common import RAW, USER_AGENT, WINDOW_START, WINDOW_END, read_json, days_between, now_iso, log, main_guard  # noqa: E402

GNEWS = os.path.join(RAW, 'gnews')
RESOLVED = os.path.join(GNEWS, 'resolved.jsonl')
WORKERS = 2
PAUSE = 2.5
ENDPOINT = 'https://news.google.com/_/DotsSplashUi/data/batchexecute'


def already():
    """The last outcome per Google link. A later line for the same link replaces the earlier one, so a re-resolved
    link's newest URL wins when the assembler reads the file the same way."""
    done = {}
    if os.path.exists(RESOLVED):
        with open(RESOLVED, encoding='utf-8') as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                    done[row['google_link']] = row
                except (json.JSONDecodeError, KeyError):
                    continue
    return done


def http(url, data=None, headers=None, timeout=30, max_bytes=4_000_000):
    request = urllib.request.Request(url, data=data, headers={'User-Agent': USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status, response.read(max_bytes).decode('utf-8', 'ignore')


def resolve(link):
    status, page = http(link + ('&' if '?' in link else '?') + 'hl=en-US&gl=US&ceid=US:en')
    signature = re.search(r'data-n-a-sg="([^"]+)"', page)
    stamp = re.search(r'data-n-a-ts="([^"]+)"', page)
    article = re.search(r'data-n-a-id="([^"]+)"', page)
    if not (signature and stamp and article):
        return None, 'no signature on page'
    inner = json.dumps(["garturlreq", [["X", "X", ["X", "X"], None, None, 1, 1, "US:en", None, 1, None, None, None,
                                        None, None, 0, 1], "X", "X", 1, [1, 1, 1], 1, 1, None, 0, 0, None, 0],
                        article.group(1), stamp.group(1), signature.group(1)])
    payload = [[["Fbv4je", inner, None, "generic"]]]
    body = urllib.parse.urlencode({'f.req': json.dumps(payload)}).encode()
    time.sleep(PAUSE)
    status, answer = http(ENDPOINT, data=body, headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'})
    start = answer.find('garturlres')
    region = answer[start:] if start >= 0 else answer
    # The URL sits inside a JSON string: take it up to the closing quote, keeping escapes, then JSON-decode them
    # (an escaped "=" is =; cutting at the backslash lost the query string, as in "…?seq").
    match = re.search(r'https?://(?:[^"\\]|\\.)+', region)
    if not match:
        return None, 'no url in answer'
    try:
        url = json.loads('"' + match.group(0) + '"')
    except json.JSONDecodeError:
        url = match.group(0)
    return url, 'ok'


def suspicious(url):
    """A resolved URL that was probably cut at an escape: it ends in a separator or has a parameter with no value."""
    return bool(url) and (url.endswith(('?', '&', '=')) or re.search(r'[?&][A-Za-z_]+$', url) is not None)


TOPICS_DIR = os.path.join(RAW, 'gnews-topics')


def headline_files():
    """(topic, day, record) for the core topic and every other topic harvested so far."""
    for day in days_between(WINDOW_START, WINDOW_END):
        record = read_json(os.path.join(GNEWS, day + '.json'))
        if record:
            yield 'nvda', day, record
    if os.path.isdir(TOPICS_DIR):
        for topic in sorted(os.listdir(TOPICS_DIR)):
            folder = os.path.join(TOPICS_DIR, topic)
            if not os.path.isdir(folder):
                continue
            for name in sorted(os.listdir(folder)):
                if name.endswith('.json'):
                    record = read_json(os.path.join(folder, name))
                    if record:
                        yield topic, name[:-5], record


def run():
    done = already()
    work = queue.Queue()
    queued = set()
    for topic, day, record in headline_files():
        for entry in record['items']:
            link = entry.get('google_link')
            if not link or '/articles/' not in link or link in queued:
                continue
            previous = done.get(link)
            if previous and previous.get('status') == 'ok' and not suspicious(previous.get('url')):
                continue
            if previous and previous.get('status') != 'ok' and previous.get('attempts', 1) >= 3:
                continue
            queued.add(link)
            work.put((day, dict(entry, topic=topic), (previous or {}).get('attempts', 0) + 1))
    log('to resolve:', work.qsize())
    lock = threading.Lock()
    counts = {'ok': 0, 'failed': 0}
    refusals = {'n': 0}

    def worker():
        while True:
            try:
                day, entry, attempts = work.get_nowait()
            except queue.Empty:
                return
            url, status = None, 'error'
            try:
                url, status = resolve(entry['google_link'])
                refusals['n'] = 0
            except urllib.error.HTTPError as error:
                status = f'http {error.code}'
                if error.code in (429, 403, 503):
                    with lock:
                        refusals['n'] += 1
                        wait = min(600, 60 * refusals['n'])
                    log('refused', error.code, 'waiting', wait)
                    time.sleep(wait)
            except Exception as error:  # a single bad link never stops the pass
                status = 'error ' + repr(error)[:80]
            row = {'day': day, 'topic': entry.get('topic', 'nvda'), 'query': entry.get('query'), 'title': entry.get('title'),
                   'source': entry.get('source'), 'published': entry.get('published'), 'google_link': entry['google_link'],
                   'url': url, 'status': status, 'attempts': attempts, 'resolved_at': now_iso()}
            with lock:
                with open(RESOLVED, 'a', encoding='utf-8') as handle:
                    handle.write(json.dumps(row, ensure_ascii=False) + '\n')
                counts['ok' if url else 'failed'] += 1
                total = counts['ok'] + counts['failed']
                if total % 100 == 0:
                    log('progress', dict(counts))
            work.task_done()
            time.sleep(PAUSE)

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(WORKERS)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    log('done', dict(counts))


if __name__ == '__main__':
    import urllib.error  # noqa: E402  (used in worker)
    main_guard(run)
