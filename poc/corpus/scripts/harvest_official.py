"""Harvest official material for the window: Federal Reserve press releases and speeches (RSS, then each page),
Federal Register documents of the Bureau of Industry and Security, the US Trade Representative and the Commerce
Department (the public JSON API, then each document's full text), and BLS news releases for CPI and the
Employment Situation (the release archives). Public, no credentials. Whole pages are kept as text.

Writes raw/official/<source>/<date>-<slug>.html, .full.txt and raw/official/manifest.json. Resumable.
"""
import html
import json
import os
import re
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))
from common import RAW, WINDOW_START, WINDOW_END, fetch, decode, page_text, title_of, published_day_of, sha256_text, write_json, read_json, now_iso, log, main_guard  # noqa: E402

OUT = os.path.join(RAW, 'official')
FED_FEEDS = [('fed-press', 'https://www.federalreserve.gov/feeds/press_all.xml', 'T11'),
             ('fed-speeches', 'https://www.federalreserve.gov/feeds/speeches.xml', 'T11'),
             ('fed-testimony', 'https://www.federalreserve.gov/feeds/testimony.xml', 'T11')]
FR_AGENCIES = [('bis', 'industry-and-security-bureau', 'T10'),
               ('ustr', 'trade-representative-office-of-united-states', 'T10'),
               ('commerce', 'commerce-department', 'T10')]
BLS_RELEASES = [('cpi', 'https://www.bls.gov/schedule/news_release/cpi.htm', 'cpi'),
                ('empsit', 'https://www.bls.gov/schedule/news_release/empsit.htm', 'empsit'),
                ('ppi', 'https://www.bls.gov/schedule/news_release/ppi.htm', 'ppi')]


def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', (text or '').lower()).strip('-')[:80] or 'page'


def keep(manifest, have, source, url, day, category, title, body, note=''):
    if url in have:
        return
    markup = decode(body)
    # the URL's hash keeps two same-day notices whose titles share their first 80 characters in two files
    # (2026-10-24: 41 groups, 97 notices, had shared one file and 56 of them held another notice's body)
    key = f'{day}-{slugify(title)[:60] or "page"}-{sha256_text(url)[:8]}'
    folder = os.path.join(OUT, source)
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, key + '.html'), 'wb') as handle:
        handle.write(body)
    text = page_text(markup)
    with open(os.path.join(folder, key + '.full.txt'), 'w', encoding='utf-8') as handle:
        handle.write(text)
    manifest['pages'].append({'source': source, 'url': url, 'date': day, 'category': category, 'title': title[:200],
                              'file': f'{source}/{key}', 'chars': len(text), 'note': note, 'retrieved_at': now_iso()})
    have.add(url)


def rss_entries(feed):
    rows = []
    for item in re.findall(r'<item>(.*?)</item>', feed, re.S):
        link = re.search(r'<link>(.*?)</link>', item, re.S)
        title = re.search(r'<title>(.*?)</title>', item, re.S)
        published = re.search(r'<pubDate>(.*?)</pubDate>', item) or re.search(r'<dc:date>(.*?)</dc:date>', item)
        clean = lambda value: html.unescape(re.sub(r'<!\[CDATA\[|\]\]>', '', value)).strip()  # noqa: E731
        rows.append((clean(link.group(1)) if link else '', clean(title.group(1)) if title else '',
                     clean(published.group(1)) if published else ''))
    return rows


def rss_day(stamp):
    import email.utils
    import datetime
    try:
        moment = email.utils.parsedate_to_datetime(stamp)
    except (TypeError, ValueError):
        try:
            moment = datetime.datetime.fromisoformat(stamp.replace('Z', '+00:00'))
        except ValueError:
            return ''
    return moment.astimezone(datetime.timezone(datetime.timedelta(hours=-4))).date().isoformat()


def harvest_fed(manifest, have):
    for source, feed_url, category in FED_FEEDS:
        status, _, body = fetch(feed_url, timeout=60)
        if status != 200:
            log('feed failed', source, status)
            continue
        entries = rss_entries(decode(body))
        kept = 0
        for url, title, stamp in entries:
            day = rss_day(stamp)
            if not url or not (WINDOW_START <= day <= WINDOW_END) or url in have:
                continue
            status, _, page = fetch(url, timeout=60)
            time.sleep(0.7)
            if status != 200 or not page:
                log('failed', url, status)
                continue
            keep(manifest, have, source, url, day, category, title, page)
            kept += 1
        log(source, 'entries', len(entries), 'kept in window', kept)


def harvest_federal_register(manifest, have):
    for source, agency, category in FR_AGENCIES:
        page_no = 1
        while True:
            params = {'conditions[agencies][]': agency, 'conditions[publication_date][gte]': WINDOW_START,
                      'conditions[publication_date][lte]': WINDOW_END, 'per_page': 100, 'page': page_no,
                      'fields[]': ['title', 'publication_date', 'html_url', 'body_html_url', 'type', 'document_number']}
            url = 'https://www.federalregister.gov/api/v1/documents.json?' + urllib.parse.urlencode(params, doseq=True)
            status, _, body = fetch(url, timeout=60, accept='application/json')
            if status != 200:
                log('federal register failed', source, status)
                break
            data = json.loads(decode(body))
            for document in data.get('results', []):
                body_url = document.get('body_html_url') or document.get('html_url')
                if not body_url or body_url in have:
                    continue
                status, _, page = fetch(body_url, timeout=60)
                time.sleep(0.7)
                if status != 200 or not page:
                    log('failed', body_url, status)
                    continue
                keep(manifest, have, 'fr-' + source, body_url, document['publication_date'], category, document.get('title', ''), page,
                     note=f'{document.get("type")} {document.get("document_number")}')
            log('fr', source, 'page', page_no, 'results', len(data.get('results', [])), 'total', data.get('count'))
            if not data.get('next_page_url'):
                break
            page_no += 1


BLS_USER_AGENT = 'Hivemind research (alex@adventai.io)'   # BLS refuses browser and curl agents, accepts a contact


def harvest_bls(manifest, have):
    """The schedule page lists only coming releases; the archive listing (bls.gov/bls/news-release/<stem>.htm)
    links every past release as archives/<stem>_MMDDYYYY.htm."""
    for source, _schedule_url, stem in BLS_RELEASES:
        status, _, body = fetch(f'https://www.bls.gov/bls/news-release/{stem}.htm', timeout=60, user_agent=BLS_USER_AGENT)
        if status != 200:
            log('bls archive listing failed', source, status)
            continue
        dates = set(re.findall(r'archives/' + re.escape(stem) + r'_(\d{2})(\d{2})(\d{4})\.htm', decode(body)))
        kept = 0
        for month, day, year in sorted(dates, key=lambda d: (d[2], d[0], d[1])):
            iso = f'{year}-{month}-{day}'
            if not (WINDOW_START <= iso <= WINDOW_END):
                continue
            url = f'https://www.bls.gov/news.release/archives/{stem}_{month}{day}{year}.htm'
            if url in have:
                continue
            status, _, page = fetch(url, timeout=60, user_agent=BLS_USER_AGENT)
            time.sleep(1.0)
            if status != 200 or not page:
                log('bls release missing', url, status)
                continue
            keep(manifest, have, 'bls-' + source, url, iso, 'T11', title_of(decode(page)) or f'{stem} {iso}', page)
            kept += 1
        log('bls', source, 'kept', kept)


def run():
    os.makedirs(OUT, exist_ok=True)
    manifest = read_json(os.path.join(OUT, 'manifest.json'), {'pages': []})
    have = {p['url'] for p in manifest['pages']}
    for step in (harvest_fed, harvest_federal_register, harvest_bls):
        try:
            step(manifest, have)
        except Exception as error:  # one source failing never stops the others
            log('step failed', step.__name__, repr(error)[:200])
        write_json(os.path.join(OUT, 'manifest.json'), manifest)
    log('done:', len(manifest['pages']), 'official pages')


if __name__ == '__main__':
    main_guard(run)
