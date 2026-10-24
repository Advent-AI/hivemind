"""Harvest NVIDIA's own press releases from nvidianews.nvidia.com for the window, found through the site's
sitemap (1,100+ URLs with a last-modified date); each release page is fetched, its publication date read from
the page, and the HTML plus a text conversion kept. Releases dated outside the window are recorded but not kept.

Writes raw/nvidianews/<date>-<slug>.html, .txt and raw/nvidianews/manifest.json.
"""
import datetime
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from common import RAW, WINDOW_START, WINDOW_END, fetch, decode, page_text, title_of, published_day_of, write_json, read_json, now_iso, log, main_guard  # noqa: E402

OUT = os.path.join(RAW, 'nvidianews')
SITEMAP = 'https://nvidianews.nvidia.com/sitemap.xml'
MONTHS = {m: i for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                      'September', 'October', 'November', 'December'], start=1)}
DATE = re.compile(r'(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}), (\d{4})')


def sitemap_entries():
    status, _, body = fetch(SITEMAP, timeout=60)
    if status != 200:
        raise SystemExit(f'sitemap failed: {status}')
    xml = decode(body)
    entries = []
    for block in re.findall(r'<url>(.*?)</url>', xml, re.S):
        loc = re.search(r'<loc>(.*?)</loc>', block)
        lastmod = re.search(r'<lastmod>(.*?)</lastmod>', block)
        if loc and '/news/' in loc.group(1):
            entries.append((lastmod.group(1)[:10] if lastmod else '', loc.group(1).strip()))
    return entries


def page_date(markup):
    """The release's own date, read from the page's marks (common.published_day_of); the first pass took the first
    long date anywhere on the page and mis-dated most releases from a sidebar."""
    return published_day_of(markup)


def run():
    os.makedirs(OUT, exist_ok=True)
    manifest = read_json(os.path.join(OUT, 'manifest.json'), {'releases': [], 'outside_window': []})
    have = {r['url'] for r in manifest['releases']} | {r['url'] for r in manifest['outside_window']}
    entries = sitemap_entries()
    # The sitemap's lastmod is not the publish date (a first pass with a 30-day margin found 36 releases where the
    # listing shows several a day), so every /news/ URL is visited once and dated from its own page.
    margin = ''
    candidates = list(entries)
    log('sitemap urls', len(entries), 'candidates with lastmod >=', margin, ':', len(candidates))
    for lastmod, url in sorted(candidates, reverse=True):
        if url in have:
            continue
        status, _, body = fetch(url, timeout=60)
        time.sleep(0.8)
        if status != 200 or not body:
            log('failed', url, status)
            continue
        markup = decode(body)
        day = page_date(markup)
        record = {'url': url, 'lastmod': lastmod, 'date': day, 'title': title_of(markup)[:200], 'retrieved_at': now_iso()}
        if WINDOW_START <= day <= WINDOW_END:
            slug = url.rsplit('/', 1)[-1][:90]
            target = os.path.join(OUT, f'{day}-{slug}.html')
            with open(target, 'wb') as handle:
                handle.write(body)
            with open(target[:-5] + '.full.txt', 'w', encoding='utf-8') as handle:
                handle.write(page_text(markup))
            record['file'] = os.path.basename(target)
            manifest['releases'].append(record)
        else:
            manifest['outside_window'].append(record)
        have.add(url)
        if len(have) % 25 == 0:
            write_json(os.path.join(OUT, 'manifest.json'), manifest)
            log('kept', len(manifest['releases']), 'outside', len(manifest['outside_window']))
    write_json(os.path.join(OUT, 'manifest.json'), manifest)
    log('done:', len(manifest['releases']), 'releases in window;', len(manifest['outside_window']), 'outside')


if __name__ == '__main__':
    main_guard(run)
