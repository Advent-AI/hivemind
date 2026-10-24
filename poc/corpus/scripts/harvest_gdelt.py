"""Harvest the list of English news articles about Nvidia from the GDELT DOC 2.0 API for every day of the window.

Adaptive slicing: one request for the whole day; when the page is full (250 rows) the day is split into eight
three-hour slices, and a full slice into single hours, so busy days are not cut at the API's page size while quiet
days cost one call. GDELT throttles bursts; we wait 8 seconds between calls and back off on its throttle message.
Resumable: a day or slice already on disk is skipped.

Writes raw/gdelt/<day>.jsonl (one article per line: url, title, domain, seendate, language, sourcecountry, slice)
and raw/gdelt/progress.json.
"""
import datetime
import json
import os
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))
from common import RAW, WINDOW_START, WINDOW_END, fetch, decode, append_jsonl, read_json, write_json, days_between, log, main_guard  # noqa: E402

OUT = os.path.join(RAW, 'gdelt')
QUERY = 'nvidia sourcelang:english'
INTERVAL = 10.0
PAGE = 250


def gdelt(start, end):
    params = {'query': QUERY, 'mode': 'artlist', 'startdatetime': start, 'enddatetime': end, 'maxrecords': str(PAGE),
              'format': 'json', 'sort': 'datedesc'}
    url = 'https://api.gdeltproject.org/api/v2/doc/doc?' + urllib.parse.urlencode(params)
    for attempt in range(10):
        status, _, body = fetch(url, timeout=90, retries=0)
        text = decode(body) if body else ''
        if status == 200 and text.lstrip().startswith('{'):
            try:
                return json.loads(text).get('articles', []), None
            except json.JSONDecodeError:
                return [], 'bad json'
        if status == 429 or 'limit requests' in text:
            wait = 45 * (attempt + 1)
            log('throttled (status', status, '); waiting', wait)
            time.sleep(wait)
            continue
        if status == 200 and not text.strip():
            return [], None
        time.sleep(15)
    return [], f'failed after retries (status {status})'


def stamp(day, hour):
    if hour == 24:
        day = (datetime.date.fromisoformat(day) + datetime.timedelta(days=1)).isoformat()
        hour = 0
    return day.replace('-', '') + f'{hour:02d}0000'


def rows_of(articles, key):
    return [{'url': a.get('url'), 'title': a.get('title'), 'domain': a.get('domain'), 'seendate': a.get('seendate'),
             'language': a.get('language'), 'sourcecountry': a.get('sourcecountry'), 'slice': key} for a in articles]


def harvest_range(day, start_hour, end_hour, progress, done):
    """Fetch one range; split it when the page is full and the range is longer than one hour."""
    key = f'{day}T{start_hour:02d}-{end_hour:02d}'
    if key in done:
        return
    articles, error = gdelt(stamp(day, start_hour), stamp(day, end_hour))
    time.sleep(INTERVAL)
    if error:
        progress['errors'].append({'slice': key, 'error': error})
        log('error', key, error)
        write_json(os.path.join(OUT, 'progress.json'), progress)
        return
    if len(articles) >= PAGE and end_hour - start_hour > 1:
        step = 3 if end_hour - start_hour > 3 else 1
        log(key, 'page full; splitting into', step, 'hour slices')
        children = []
        for hour in range(start_hour, end_hour, step):
            child_end = min(hour + step, end_hour)
            harvest_range(day, hour, child_end, progress, done)
            children.append(f'{day}T{hour:02d}-{child_end:02d}')
        if all(child in done for child in children):
            progress['done'].append(key)
            done.add(key)
        else:
            log(key, 'left open: a child slice failed; the next run retries it')
        write_json(os.path.join(OUT, 'progress.json'), progress)
        return
    append_jsonl(os.path.join(OUT, day + '.jsonl'), rows_of(articles, key))
    flag = ' (page full at one hour; the rest of this hour is lost)' if len(articles) >= PAGE else ''
    log(key, len(articles), 'articles' + flag)
    progress['done'].append(key)
    done.add(key)
    write_json(os.path.join(OUT, 'progress.json'), progress)


def run():
    os.makedirs(OUT, exist_ok=True)
    progress = read_json(os.path.join(OUT, 'progress.json'), {'done': [], 'errors': []})
    done = set(progress['done'])
    for day in days_between(WINDOW_START, WINDOW_END):
        harvest_range(day, 0, 24, progress, done)
    progress['finished_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    write_json(os.path.join(OUT, 'progress.json'), progress)
    log('done; ranges', len(progress['done']), 'errors', len(progress['errors']))


if __name__ == '__main__':
    main_guard(run)
