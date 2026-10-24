"""Shared helpers for the corpus harvesters: polite HTTP, HTML to text, JSON files, logging.

Standard library only. Every harvester is resumable: it skips what is already on disk.
"""
import datetime
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW = os.path.join(ROOT, 'raw')
USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
SEC_USER_AGENT = 'Hivemind research alex@adventai.io'
WINDOW_START = '2026-07-24'
WINDOW_END = '2026-10-22'
BOOTSTRAP_START = '2026-02-25'
MAX_BYTES = 8_000_000


def log(*parts):
    stamp = datetime.datetime.now().strftime('%H:%M:%S')
    print(stamp, *parts, flush=True)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def sha256_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def is_truncated(body, max_bytes=MAX_BYTES):
    """fetch() reads one byte past its cap, so a body longer than the cap was cut and must not pass as whole."""
    return len(body) > max_bytes


def is_block_page(markup):
    """A page that is not the article: an access wall, a bot check, a not-found page. Judged on the title and the
    first lines only; the text itself is never read for meaning."""
    head = (title_of(markup) + ' ' + page_text(markup[:6000])[:600])
    return bool(_BLOCK_PAGE.search(head))


def new_york_day(moment):
    """The New York calendar day of an aware datetime (a naive one is taken as UTC)."""
    from zoneinfo import ZoneInfo
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=datetime.timezone.utc)
    return moment.astimezone(ZoneInfo('America/New_York')).date().isoformat()


def fetch(url, *, timeout=30, user_agent=USER_AGENT, retries=2, pause=3.0, accept=None, max_bytes=MAX_BYTES):
    """GET a URL and return (status, final_url, bytes). A failure returns (status or 0, url, b''). A body longer
    than max_bytes is returned one byte over the cap so the caller can see it was cut (is_truncated)."""
    headers = {'User-Agent': user_agent, 'Accept-Language': 'en-US,en;q=0.9'}
    if accept:
        headers['Accept'] = accept
    last_status = 0
    for attempt in range(retries + 1):
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read(max_bytes + 1)
                return response.status, response.geturl(), body
        except urllib.error.HTTPError as error:
            last_status = error.code
            if error.code in (401, 403, 404, 410, 451):
                return error.code, url, b''
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            last_status = 0
        time.sleep(pause * (attempt + 1))
    return last_status, url, b''


def decode(body):
    for encoding in ('utf-8', 'latin-1'):
        try:
            return body.decode(encoding)
        except UnicodeDecodeError:
            continue
    return body.decode('utf-8', errors='ignore')


_BLOCK_TAGS = re.compile(r'</?(p|div|br|li|h[1-6]|tr|td|th|section|article|blockquote|table)[^>]*>', re.I)
_DROP = re.compile(r'<(script|style|noscript|svg|nav|footer|header|aside|form)[^>]*>.*?</\1>', re.I | re.S)
_TAGS = re.compile(r'<[^>]+>')


def html_to_text(markup):
    """A crude but dependency-free conversion: drop scripts, styles and chrome, keep block boundaries."""
    text = _DROP.sub(' ', markup)
    text = _BLOCK_TAGS.sub('\n', text)
    text = _TAGS.sub(' ', text)
    text = html.unescape(text)
    lines = [re.sub(r'[ \t\xa0]+', ' ', line).strip() for line in text.split('\n')]
    return '\n'.join(line for line in lines if line)


_NON_TEXT = re.compile(r'<(script|style)[^>]*>.*?</\1>', re.I | re.S)
_BLOCK_PAGE = re.compile(r'access denied|just a moment|attention required|are you a robot|verify you are human|'
                         r'enable javascript and cookies|403 forbidden|page not found|subscribe to continue|'
                         r'this site can.t be reached|captcha', re.I)


def page_text(markup):
    """The whole page as text, nothing judged: only script and style elements are removed (they hold code, not
    prose); navigation, headers, footers, asides, noscript and svg text all stay. This is what the pipeline reads."""
    text = _NON_TEXT.sub(' ', markup)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.S)
    text = _BLOCK_TAGS.sub('\n', text)
    text = _TAGS.sub(' ', text)
    text = html.unescape(text)
    lines = [re.sub(r'[ \t\xa0]+', ' ', line).strip() for line in text.split('\n')]
    return '\n'.join(line for line in lines if line)


def article_paragraphs(markup):
    """The article body of a news page: the <p> elements, kept when the page yields enough prose.

    Returns (text, paragraph_count). The caller decides whether the yield is complete or partial."""
    clean = _DROP.sub(' ', markup)
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', clean, re.S | re.I)
    kept = []
    for paragraph in paragraphs:
        line = html.unescape(_TAGS.sub(' ', paragraph))
        line = re.sub(r'\s+', ' ', line).strip()
        if len(line) >= 40 and not re.search(r'(sign up|subscribe|cookies|all rights reserved|newsletter)', line, re.I):
            kept.append(line)
    return '\n\n'.join(kept), len(kept)


def title_of(markup):
    match = re.search(r'<title[^>]*>(.*?)</title>', markup, re.S | re.I)
    if not match:
        match = re.search(r'property="og:title"\s+content="([^"]*)"', markup, re.I)
    return html.unescape(re.sub(r'\s+', ' ', match.group(1))).strip() if match else ''


_MONTHS = {m: i for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                       'September', 'October', 'November', 'December'], start=1)}
_LONG_DATE = re.compile(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})')


def _iso_day(stamp):
    stamp = stamp.strip()
    try:
        moment = datetime.datetime.fromisoformat(stamp.replace('Z', '+00:00'))
        return moment.date().isoformat() if moment.tzinfo is None else new_york_day(moment)
    except ValueError:
        return stamp[:10] if re.match(r'\d{4}-\d{2}-\d{2}', stamp) else ''


def published_day_of(markup):
    """The page's own publication day (New York), from the most reliable mark present, in this order: the
    article:published_time meta tag; JSON-LD datePublished; a <time datetime> or a dated header element inside the
    article (after the <h1>, within 6,000 characters); else the first long date after the <h1>. Marks before the
    <h1> (navigation, sidebars) are not used. Returns '' when none is found. Nothing here reads the body for meaning."""
    for pattern in (r'property="article:published_time"\s+content="([^"]+)"',
                    r'content="([^"]+)"\s+property="article:published_time"',
                    r'"datePublished"\s*:\s*"([^"]+)"',
                    r'name="(?:date|publish-date|pubdate|dc\.date|dcterms\.created|parsely-pub-date)"\s+content="([^"]+)"'):
        match = re.search(pattern, markup, re.I)
        if match:
            day = _iso_day(match.group(1))
            if day:
                return day
    start = markup.find('<h1')
    region = markup[start:start + 6000] if start >= 0 else ''
    for pattern in (r'<time[^>]+datetime="([^"]+)"',):
        match = re.search(pattern, region, re.I)
        if match:
            day = _iso_day(match.group(1))
            if day:
                return day
    header = re.search(r'class="[^"]*(?:date|time)[^"]*"[^>]*>\s*([^<]{6,40})<', region, re.I)
    if header:
        match = _LONG_DATE.search(header.group(1))
        if match:
            return datetime.date(int(match.group(3)), _MONTHS[match.group(1)], int(match.group(2))).isoformat()
    match = _LONG_DATE.search(region)
    if match:
        return datetime.date(int(match.group(3)), _MONTHS[match.group(1)], int(match.group(2))).isoformat()
    return ''


def write_json(path, data):
    """Write to a temporary file and rename, so a crash never leaves a half-written manifest."""
    ensure_dir(os.path.dirname(path))
    temporary = path + '.tmp'
    with open(temporary, 'w', encoding='utf-8') as handle:
        json.dump(data, handle, ensure_ascii=False, indent=1)
    os.replace(temporary, path)


def read_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding='utf-8') as handle:
        return json.load(handle)


def append_jsonl(path, rows):
    ensure_dir(os.path.dirname(path))
    with open(path, 'a', encoding='utf-8') as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + '\n')


def days_between(start, end):
    day = datetime.date.fromisoformat(start)
    last = datetime.date.fromisoformat(end)
    while day <= last:
        yield day.isoformat()
        day += datetime.timedelta(days=1)


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')


def main_guard(function):
    try:
        function()
    except KeyboardInterrupt:
        log('interrupted')
        sys.exit(130)
