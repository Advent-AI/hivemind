"""Harvest Google News RSS headlines for every topic in topics.json, every day of the window: up to per_day headlines
per query per day (Google ranks by relevance, the first rows are kept), with the topic id and its object labels
attached. The core 'nvda' topic was harvested by harvest_gnews.py into raw/gnews/<day>.json; this script writes the
other topics to raw/gnews-topics/<topic>/<day>.json and a manifest. Resumable: a (topic, day) file is skipped.

The headlines' Google links are resolved to publisher URLs by resolve_gnews.py, which reads both folders.
"""
import html
import os
import re
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))
from common import RAW, WINDOW_START, WINDOW_END, fetch, decode, write_json, read_json, days_between, now_iso, log, main_guard  # noqa: E402

OUT = os.path.join(RAW, 'gnews-topics')
TOPICS = read_json(os.path.join(os.path.dirname(__file__), 'topics.json'))['topics']
PAUSE = 1.5


def day_after(day):
    import datetime
    return (datetime.date.fromisoformat(day) + datetime.timedelta(days=1)).isoformat()


def rss_items(feed):
    rows = []
    for item in re.findall(r'<item>(.*?)</item>', feed, re.S):
        title = re.search(r'<title>(.*?)</title>', item, re.S)
        source = re.search(r'<source[^>]*>(.*?)</source>', item, re.S)
        published = re.search(r'<pubDate>(.*?)</pubDate>', item)
        link = re.search(r'<link>(.*?)</link>', item, re.S)
        rows.append({'title': html.unescape(title.group(1)).strip() if title else '',
                     'source': html.unescape(source.group(1)).strip() if source else '',
                     'published': published.group(1) if published else '',
                     'google_link': link.group(1).strip() if link else ''})
    return rows


def run():
    only = sys.argv[1:]   # optional topic ids to restrict a run
    manifest = read_json(os.path.join(OUT, 'manifest.json'), {'counts': {}})
    refusals = 0
    for topic in TOPICS:
        if topic['id'] == 'nvda' or (only and topic['id'] not in only):
            continue
        folder = os.path.join(OUT, topic['id'])
        os.makedirs(folder, exist_ok=True)
        for day in days_between(WINDOW_START, WINDOW_END):
            target = os.path.join(folder, day + '.json')
            if os.path.exists(target):
                continue
            kept = []
            incomplete = False
            for query in topic['queries']:
                q = f'{query} after:{day} before:{day_after(day)}'
                url = 'https://news.google.com/rss/search?' + urllib.parse.urlencode({'q': q, 'hl': 'en-US', 'gl': 'US', 'ceid': 'US:en'})
                status, _, body = fetch(url, timeout=60, retries=1)
                if status != 200:
                    refusals += 1
                    wait = min(600, 30 * refusals)
                    log('refused', status, topic['id'], day, 'waiting', wait)
                    time.sleep(wait)
                    incomplete = True
                    continue
                refusals = 0
                rows = rss_items(decode(body))[:topic['per_day']]
                for row in rows:
                    row['query'] = query
                kept.extend(rows)
                time.sleep(PAUSE)
            if incomplete:
                log('day left for a later run (a query was refused):', topic['id'], day)
                continue   # no file written, so the next run fetches the day again
            write_json(target, {'topic': topic['id'], 'tier': topic['tier'], 'objects': topic['objects'], 'day': day,
                                'count': len(kept), 'items': kept, 'retrieved_at': now_iso()})
            manifest['counts'][f'{topic["id"]}/{day}'] = len(kept)
        write_json(os.path.join(OUT, 'manifest.json'), manifest)
        total = sum(v for k, v in manifest['counts'].items() if k.startswith(topic['id'] + '/'))
        log('topic done', topic['id'], 'headlines', total)
    log('done; headlines in all topics:', sum(manifest['counts'].values()))


if __name__ == '__main__':
    main_guard(run)
