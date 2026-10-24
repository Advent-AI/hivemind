"""Harvest NVIDIA's corporate blog (blogs.nvidia.com) for the window through its WordPress post sitemap, which
lists the newest 1,000 posts with last-modified dates. Each candidate page is fetched and dated from its own
article:published_time meta tag; posts outside the window are recorded but not kept.

Writes raw/nvblog/<date>-<slug>.html, .txt and raw/nvblog/manifest.json.
"""
import datetime
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from common import RAW, WINDOW_START, WINDOW_END, fetch, decode, page_text, title_of, write_json, read_json, now_iso, log, main_guard  # noqa: E402

OUT = os.path.join(RAW, 'nvblog')
SITEMAP_INDEX = 'https://blogs.nvidia.com/sitemap_index.xml'


def entries():
    """Every post in every post sitemap the index lists (WordPress splits them 1,000 posts a file, oldest first)."""
    status, _, body = fetch(SITEMAP_INDEX, timeout=60)
    if status != 200:
        raise SystemExit(f'sitemap index failed: {status}')
    sitemaps = [loc for loc in re.findall(r'<loc>(.*?)</loc>', decode(body)) if 'post-sitemap' in loc]
    rows = []
    for sitemap in sitemaps:
        status, _, body = fetch(sitemap, timeout=60)
        if status != 200:
            log('sitemap failed', sitemap, status)
            continue
        for block in re.findall(r'<url>(.*?)</url>', decode(body), re.S):
            loc = re.search(r'<loc>(.*?)</loc>', block)
            lastmod = re.search(r'<lastmod>(.*?)</lastmod>', block)
            if loc and '/blog/' in loc.group(1):
                rows.append((lastmod.group(1)[:10] if lastmod else '', loc.group(1).strip()))
        time.sleep(0.5)
    log('post sitemaps', len(sitemaps), 'posts', len(rows))
    return rows


def published_day(markup):
    match = re.search(r'property="article:published_time"\s+content="([^"]+)"', markup)
    if not match:
        match = re.search(r'"datePublished"\s*:\s*"([^"]+)"', markup)
    if not match:
        return ''
    stamp = match.group(1)
    try:
        moment = datetime.datetime.fromisoformat(stamp.replace('Z', '+00:00'))
        return moment.astimezone(datetime.timezone(datetime.timedelta(hours=-4))).date().isoformat()
    except ValueError:
        return stamp[:10]


def run():
    os.makedirs(OUT, exist_ok=True)
    manifest = read_json(os.path.join(OUT, 'manifest.json'), {'posts': [], 'outside_window': []})
    have = {p['url'] for p in manifest['posts']} | {p['url'] for p in manifest['outside_window']}
    margin = (datetime.date.fromisoformat(WINDOW_START) - datetime.timedelta(days=10)).isoformat()
    candidates = [(mod, url) for mod, url in entries() if not mod or mod >= margin]
    log('sitemap posts', len(candidates), 'with lastmod >=', margin)
    for lastmod, url in sorted(candidates, reverse=True):
        if url in have:
            continue
        status, _, body = fetch(url, timeout=60)
        time.sleep(0.8)
        if status != 200 or not body:
            log('failed', url, status)
            continue
        markup = decode(body)
        day = published_day(markup)
        record = {'url': url, 'lastmod': lastmod, 'date': day, 'title': title_of(markup)[:200], 'retrieved_at': now_iso()}
        if WINDOW_START <= day <= WINDOW_END:
            slug = url.rstrip('/').rsplit('/', 1)[-1][:90]
            target = os.path.join(OUT, f'{day}-{slug}.html')
            text = page_text(markup)
            with open(target, 'wb') as handle:
                handle.write(body)
            with open(target[:-5] + '.full.txt', 'w', encoding='utf-8') as handle:
                handle.write(text)
            record['file'] = os.path.basename(target)
            record['chars'] = len(text)
            manifest['posts'].append(record)
        else:
            manifest['outside_window'].append(record)
        have.add(url)
        if len(have) % 25 == 0:
            write_json(os.path.join(OUT, 'manifest.json'), manifest)
            log('kept', len(manifest['posts']), 'outside', len(manifest['outside_window']))
    write_json(os.path.join(OUT, 'manifest.json'), manifest)
    log('done:', len(manifest['posts']), 'posts in window;', len(manifest['outside_window']), 'outside')


if __name__ == '__main__':
    main_guard(run)
