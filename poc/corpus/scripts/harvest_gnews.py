"""Harvest Google News RSS headlines about Nvidia for every day of the window (up to 100 per day) as a coverage
cross-check: title, source name, publication time. The links are Google redirect pages and are kept only as ids.

Writes raw/gnews/<day>.json and raw/gnews/manifest.json.
"""
import html
import os
import re
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))
from common import RAW, WINDOW_START, WINDOW_END, fetch, decode, write_json, read_json, days_between, now_iso, log, main_guard  # noqa: E402

OUT = os.path.join(RAW, 'gnews')


def day_after(day):
    import datetime
    return (datetime.date.fromisoformat(day) + datetime.timedelta(days=1)).isoformat()


def run():
    manifest = read_json(os.path.join(OUT, 'manifest.json'), {'days': {}})
    for day in days_between(WINDOW_START, WINDOW_END):
        target = os.path.join(OUT, day + '.json')
        if os.path.exists(target):
            continue
        query = f'nvidia after:{day} before:{day_after(day)}'
        url = 'https://news.google.com/rss/search?' + urllib.parse.urlencode({'q': query, 'hl': 'en-US', 'gl': 'US', 'ceid': 'US:en'})
        status, _, body = fetch(url, timeout=60)
        if status != 200:
            log('failed', day, status)
            time.sleep(5)
            continue
        feed = decode(body)
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
        write_json(target, {'day': day, 'count': len(rows), 'items': rows, 'retrieved_at': now_iso()})
        manifest['days'][day] = len(rows)
        write_json(os.path.join(OUT, 'manifest.json'), manifest)
        log(day, len(rows))
        time.sleep(2.0)
    log('done')


if __name__ == '__main__':
    main_guard(run)
