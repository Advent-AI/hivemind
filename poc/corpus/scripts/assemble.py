"""Assemble the test database from the raw harvests: one row per item with the fields of the classification PRD
(docs/prd/02-classification.md), a class (新闻, 公司材料, 官方材料), a 16-category tag kept as an attribute, the
whole original text, and whether the item is an original the pipeline may read (feed). Re-runnable: it rebuilds
items.sqlite from raw/ every time; items.sqlite is derived, raw/ is the record.

Rules that matter (Alex 2026-10-23: the material must be original, not processed):
- text is the whole page or document as text (.full.txt), nothing cut; a page without it is not fed.
- a page's publication day is the earlier of the listing's day and the page's own date (the day the market could
  first have seen it, 02-classification 时间规则 5), in New York time.
- a copy points at its original: the same canonical URL, or the same title on the same day when one side is an
  aggregator or both are the same publisher; distinct outlets with the same headline stay distinct.
- feed = 1 only for coverage 'full': an original page or document, not blocked, not a stub, not truncated.
"""
import collections
import datetime
import email.utils
import json
import os
import re
import sqlite3
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))
from common import (ROOT, RAW, WINDOW_START, WINDOW_END, read_json, sha256_text, now_iso, new_york_day, decode,
                    published_day_of, is_block_page, log, main_guard)  # noqa: E402

DB = os.path.join(ROOT, 'items.sqlite')
HERE = os.path.dirname(__file__)
TABLES = read_json(os.path.join(HERE, 'author-table.json'))
AGGREGATORS = set(TABLES['aggregators'])
AUTHOR_TYPES = TABLES['authors']           # domain -> company | media | analyst | official | individual
TOPICS = {t['id']: t for t in read_json(os.path.join(HERE, 'topics.json'))['topics']}
COMPANIES = {c['ticker']: c for c in read_json(os.path.join(HERE, 'companies.json'))['companies']}
TICKER = [{'kind': 'ticker', 'value': 'NVDA', 'why': 'upstream feed for this object'}]
TRACKING_KEYS = {'ref', 'ref_src', 'guccounter', 'guce_referrer', 'guce_referrer_sig', 'yptr', 'ncid', 'cmpid',
                 'soc_src', 'soc_trk', 'fbclid', 'gclid', 'mc_cid', 'mc_eid'}

SCHEMA = """
-- text        : the original page or document as text, nothing cut (what the pipeline reads)
-- text_article: a heuristic cut of the article body, for the review's estimates only, never fed
-- coverage    : full (the original, whole) | stub | blocked | truncated | title (only the headline) |
--               provider_summary (a third party's summary, not fed) | none
-- feed        : 1 when the item is an original document the pipeline may read; 0 otherwise
-- day_source  : where publication_day came from: page | listing | filing | call | release
create table items (
  input_id text primary key, klass text, category text, content_sha256 text, copy_of text, supersedes text,
  channel text, source_uri text, publisher text, publisher_type text, authors text, published_at text,
  publication_day text, day_source text, listing_day text, page_day text, retrieved_at text, is_structured integer,
  has_readable_text integer, document_format text, channel_category text, media_type text, language text,
  object_identifiers text, title text, text text, text_article text, coverage text, text_chars integer,
  bootstrap integer, feed integer, source text, topic text, tier text, extra text
);
create index items_day on items(publication_day);
create index items_klass on items(klass, publication_day);
create index items_feed on items(feed, publication_day);
"""


# ---------- small helpers ----------

def domain_of(url):
    host = urllib.parse.urlsplit(url or '').netloc.lower()
    return host[4:] if host.startswith('www.') else host


def author_type(domain, channel_default='media'):
    for suffix, kind in AUTHOR_TYPES.items():
        if domain == suffix or domain.endswith('.' + suffix):
            return kind
    return channel_default


def news_category(kind):
    """02-classification: company text outside filings → T6; media → T7; analyst or individual → T8; official → T10."""
    return {'company': 'T6', 'official': 'T10', 'analyst': 'T8', 'individual': 'T8'}.get(kind, 'T7')


BYLINES = TABLES.get('bylines', {})
OUTLET_NAMES = '|'.join(re.escape(name) for name in sorted(BYLINES, key=len, reverse=True))
MONTH = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)'
READ_STAMP = re.compile(MONTH + r' \d{1,2}, \d{4}(?:\s*·)?\s*\d+ min read', re.I)   # Yahoo's byline line ends with it
DATE_STAMP = re.compile(MONTH + r' \d{1,2}, \d{4}', re.I)
DATELINE = re.compile(r'((?:' + OUTLET_NAMES + r')\s*(?:--|—|-)\s|\((?:' + OUTLET_NAMES + r')\)\s*-)', re.I)
REPUBLISHED = re.compile(r'(?:originally published (?:at|on|by)|first appeared (?:on|at)|originally appeared (?:on|at)|'
                         r'this article was (?:originally )?published (?:at|on|by)|read the original article (?:on|at)|©\s*\d{4})\s*(' + OUTLET_NAMES + ')', re.I)


def byline_outlet(title, text):
    """02-classification 作者规则 3: the author is the party responsible for the content, not the channel. On an
    aggregator's page (Yahoo Finance, AOL, MSN …) the author is named in one of four places, checked in this order:
    the byline between the headline's second occurrence (the article head; the first is the browser title) and the
    date stamp 'July 27, 2026 · 4 min read'; the dateline that opens the body right after the stamp ('Investing.com --',
    '(Reuters) -'); a republication line anywhere ('This article first appeared on GuruFocus'); a copyright line
    ('© 2026 Benzinga'). Returns the outlet's domain from the bylines table, or '' when no outlet is named (a page
    by the aggregator's own staff, or a writer named without an outlet)."""
    flat = re.sub(r'\s+', ' ', text or '')
    head = re.sub(r'\s+', ' ', title or '').strip()[:60]
    if len(head) >= 12 and (first := flat.find(head)) >= 0:
        second = flat.find(head, first + len(head))
        start = (second if second >= 0 else first) + len(head)
        stamp = READ_STAMP.search(flat, start) or DATE_STAMP.search(flat, start)
        if stamp and stamp.start() - start <= 400:
            span = flat[start:stamp.start()].lower()
            for name, domain in BYLINES.items():
                if name in span:
                    return domain
            dateline = DATELINE.search(flat, stamp.end(), stamp.end() + 300)
            if dateline:
                named = dateline.group(1).lower()
                for name, domain in BYLINES.items():
                    if name in named:
                        return domain
    republished = REPUBLISHED.search(flat)
    if republished:
        return BYLINES[republished.group(1).lower()]
    return ''


def page_author(domain, title, text):
    """(publisher, publisher type, identified) for a fetched news page: the page's own domain, except on an aggregator,
    where the byline's outlet is the author and the aggregator only the channel; an aggregator page without a named
    outlet keeps the channel default (media) and is marked unidentified (02-classification 作者规则 4)."""
    if domain in AGGREGATORS:
        outlet = byline_outlet(title, text)
        if outlet:
            return outlet, author_type(outlet), True
        return domain, 'media', False
    return domain, author_type(domain), True


def normalise_title(title):
    title = (title or '').lower()
    title = re.sub(r'\s*[-|–—:]\s*(the motley fool|yahoo finance|reuters|cnbc|bloomberg|benzinga|aol|msn|seeking alpha|nasdaq)\s*$', '', title)
    title = re.sub(r'[^a-z0-9 ]+', ' ', title)
    return re.sub(r'\s+', ' ', title).strip()


def canonical_url(url):
    parts = urllib.parse.urlsplit((url or '').strip())
    query = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
             if not k.lower().startswith('utm_') and k.lower() not in TRACKING_KEYS]
    return urllib.parse.urlunsplit((parts.scheme or 'https', domain_of(url), parts.path.rstrip('/'), urllib.parse.urlencode(query), ''))


def read_text(path):
    with open(path, encoding='utf-8', errors='ignore') as handle:
        return handle.read()


def full_text_of(path_without_suffix):
    """Only the whole-page text counts; the older .txt (a heuristic cut) is never used as the item."""
    path = path_without_suffix + '.full.txt'
    return read_text(path) if os.path.exists(path) else ''


def earlier(*days):
    days = [d for d in days if d]
    return min(days) if days else ''


def rfc_day(stamp):
    try:
        return new_york_day(email.utils.parsedate_to_datetime(stamp))
    except (TypeError, ValueError):
        return ''


def item(**fields):
    base = {'supersedes': None, 'authors': None, 'is_structured': 0, 'has_readable_text': 1, 'media_type': 'text/html',
            'language': 'en', 'object_identifiers': json.dumps(TICKER), 'copy_of': None, 'channel_category': None,
            'extra': None, 'text_article': None, 'topic': 'nvda', 'tier': 'core', 'day_source': 'listing',
            'listing_day': None, 'page_day': None, 'retrieved_at': now_iso()}
    base.update(fields)
    text = base.get('text') or ''
    base['content_sha256'] = sha256_text(text or base.get('title') or base['input_id'])
    base['text_chars'] = len(text)
    base['bootstrap'] = 1 if base['publication_day'] < WINDOW_START else 0
    base['feed'] = 1 if base.get('coverage') == 'full' and len(text) >= 200 and base.get('category') != NOT_MATERIAL else 0
    return base


def objects_for_topic(topic_ids):
    seen, objects = set(), []
    for topic_id in topic_ids:
        for obj in (TOPICS.get(topic_id) or {}).get('objects', []) or ([] if topic_id in TOPICS else TICKER):
            key = (obj['kind'], obj['value'])
            if key not in seen:
                seen.add(key)
                objects.append(dict(obj, why=f'upstream feed: topic {topic_id}'))
    return objects


THEME_CARRYING_CATEGORIES = ('T1', 'T2', 'T4')     # results, periodic reports and calls speak to the industry themes; contracts, 8-K bodies and other exhibits do not


def objects_for_company(ticker, themes, category='T4', role='filer'):
    """The company itself, plus the themes its results, reports and calls are evidence for (companies.json). A
    contract, an 8-K body or another exhibit carries only the company (counted 2026-10-24: a subsidiaries list and an
    auditor's consent were labelled 'AI capex')."""
    objects = [{'kind': 'ticker', 'value': ticker, 'why': role}]
    if category in THEME_CARRYING_CATEGORIES:
        objects += [{'kind': 'theme', 'value': theme, 'why': 'upstream feed: company in theme'} for theme in themes or []]
    return objects


# ---------- fetched pages ----------

def pages_index():
    """url -> the last index record for it (a retried fetch's newest line wins), with page_day and blocked filled
    from the stored HTML when an older record lacks them."""
    pages = {}
    index = os.path.join(RAW, 'pages', 'index.jsonl')
    if os.path.exists(index):
        with open(index, encoding='utf-8') as handle:
            for line in handle:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                previous = pages.get(record['url'])
                if previous and previous.get('file') and not record.get('file'):
                    continue   # a later failed retry does not erase an earlier good fetch
                pages[record['url']] = record
    for record in pages.values():
        if record.get('file') and ('page_day' not in record or 'blocked' not in record):
            html_path = os.path.join(RAW, 'pages', record['file'] + '.html')
            if os.path.exists(html_path):
                with open(html_path, 'rb') as handle:
                    markup = decode(handle.read())
                record.setdefault('page_day', published_day_of(markup))
                record.setdefault('blocked', is_block_page(markup))
                full = full_text_of(os.path.join(RAW, 'pages', record['file']))
                record['full_chars'] = len(full)
                if record['blocked']:
                    record['coverage'] = 'blocked'
                elif len(full) < 500:
                    record['coverage'] = 'stub'
                elif record.get('coverage') in ('partial', 'full'):
                    record['coverage'] = 'full'
    return pages


VIDEO_PATH = re.compile(r'/video/|/videos/', re.I)


def page_texts(page, url=''):
    """(whole page text, heuristic cut, coverage) for a fetched page record; ('', None, 'title') when none. A video
    page (CNBC's /video/ paths) has no transcript, only the player's description and navigation: its text is kept but
    the coverage is 'video', never 'full' (counted 2026-10-24: 10 CNBC video pages had been fed as full articles)."""
    if not page.get('file'):
        return '', None, 'title'
    base = os.path.join(RAW, 'pages', page['file'])
    text = full_text_of(base)
    cut = read_text(base + '.txt') if os.path.exists(base + '.txt') else None
    coverage = page.get('coverage') or 'none'
    if coverage in ('full', 'partial'):
        coverage = 'full' if text else 'none'
    if coverage == 'full' and VIDEO_PATH.search(urllib.parse.urlsplit(url or '').path):
        coverage = 'video'
    return text, cut, coverage


# ---------- SEC filings ----------

NOT_MATERIAL = '不算材料'            # 02-classification: a document that is not research material; never fed
NOT_MATERIAL_EXHIBITS = ('19', '21', '23', '31', '32', '97')   # insider-trading policy, subsidiaries list, auditor consent,
                                                               # SOX 302 and 906 certifications, clawback policy: forms with no statement about the business


RESULTS_WORDS = re.compile(r'quarter|results|financial statements|half.year|interim|(?:three|six|nine) months ended|earnings release', re.I)
MONTHLY_WORDS = re.compile(r'monthly (?:net )?revenue|monthly sales', re.I)


def item_202_section(primary_text):
    """The body of the 8-K's Item 2.02 section: of every 'Item 2.02' occurrence (the table of contents lists one
    too), the one with the most text before the next item heading or the signature."""
    best = ''
    for found in re.finditer(r'item\s+2\.02(.*?)(?=item\s+\d\.\d{2}|signature|$)', primary_text or '', re.I | re.S):
        if len(found.group(1)) > len(best):
            best = found.group(1)
    return best


def exhibit_category(form, name, primary_document, exhibit_type, description, items_listed, primary_text, exhibit_text=''):
    """02-classification: 10-Q/10-K/20-F → T2; an 8-K exhibit named in the body of Item 2.02 → T1; a 6-K exhibit
    whose description or own cover says it is a period's results → T1; exhibits 2, 3, 4, 10 → T3; presentations → T5;
    certification and policy exhibits → 不算材料; the rest → T6."""
    exhibit_type = (exhibit_type or '').upper()
    description = (description or '').lower()
    if name == primary_document:
        if form.startswith(('10-', '20-')):
            return 'T2', 'report'
        return 'T6', 'filing'
    number = re.match(r'EX-(\d+)(?:\.(\d+))?', exhibit_type)
    major = number.group(1) if number else ''
    if major in NOT_MATERIAL_EXHIBITS:
        return NOT_MATERIAL, 'certification'
    if major == '99' and '2.02' in (items_listed or '') and form.startswith('8-K'):
        section = item_202_section(primary_text)
        label = (number.group(2) or '1') if number else '1'
        if section and re.search(r'99\.' + re.escape(label) + r'\b', section):
            return 'T1', 'release'
        if not section:
            return 'T1', 'release'   # no readable Item 2.02 text: the exhibit of a results 8-K
    if form.startswith('6-K') and major == '99':
        about = description if re.search(r'[a-z]{4,}', description) else (exhibit_text or '')[:1500].lower()   # a bare 'EX-99.1' says nothing: read the cover
        if MONTHLY_WORDS.search(about):
            return 'T6', 'release'
        if RESULTS_WORDS.search(about):
            return 'T1', 'release'
    if major in ('2', '3', '4', '10'):
        return 'T3', 'filing'
    if major == '99' and re.search(r'presentation|slides|investor day', description):
        return 'T5', 'slides'
    return 'T6', 'filing'


def filing_items(manifest_path, base_dir, source, tier, ticker_of, objects_of, id_prefix):
    manifest = read_json(manifest_path, {'filings': []})
    rows = []
    for filing in manifest['filings']:
        form, day, accession = filing['form'], filing['filing_date'], filing['accession']
        ticker = ticker_of(filing)
        folder_dir = os.path.join(base_dir, ticker, accession) if ticker != 'NVDA' or source != 'edgar' else os.path.join(base_dir, accession)
        primary_text = full_text_of(os.path.join(folder_dir, filing['primary_document']))
        for doc in filing['documents']:
            name = doc['name']
            if name.endswith('.txt') and name.startswith(accession):
                continue   # the complete submission bundle duplicates the documents
            role = doc.get('role') or {}
            text = full_text_of(os.path.join(folder_dir, name))
            category, document_format = exhibit_category(form, name, filing['primary_document'], role.get('type'),
                                                         role.get('description'), filing.get('items'), primary_text, text)
            cik_short = (filing.get('cik') or '0001045810').lstrip('0')
            rows.append(item(
                input_id=f'{id_prefix}:{accession}:{name}', klass='公司材料', category=category, channel='EDGAR',
                source_uri=f'https://www.sec.gov/Archives/edgar/data/{cik_short}/{filing["folder"]}/{name}',
                publisher=filing.get('company_name') or 'NVIDIA Corporation', publisher_type='company',
                published_at=filing.get('acceptance_datetime'), publication_day=day, day_source='filing',
                document_format=document_format, title=f'{ticker} {form} {role.get("description") or name}', text=text,
                coverage='full' if text else 'none', source=source, topic=f'company-{ticker}', tier=tier,
                object_identifiers=json.dumps(objects_of(filing, category)),
                extra=json.dumps({'form': form, 'exhibit_type': role.get('type'), 'items': filing.get('items'), 'retrieved_at': filing.get('retrieved_at')})))
    return rows


def edgar_items():
    return filing_items(os.path.join(RAW, 'edgar', 'manifest.json'), os.path.join(RAW, 'edgar'), 'edgar', 'core',
                        lambda f: 'NVDA', lambda f, category: TICKER, 'edgar:NVDA')


def edgar_peer_items():
    return filing_items(os.path.join(RAW, 'edgar-peers', 'manifest.json'), os.path.join(RAW, 'edgar-peers'), 'edgar-peers',
                        'industry', lambda f: f['ticker'], lambda f, category: objects_for_company(f['ticker'], f.get('themes'), category), 'edgar')


# ---------- TrueNorth ----------

def transcript_items():
    rows = []
    base = os.path.join(RAW, 'truenorth')
    folder = os.path.join(base, 'transcripts')
    for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        record = read_json(os.path.join(folder, name))
        transcript = record['transcript']
        day = str(transcript['call_date'])[:10]
        rows.append(item(
            input_id=f'truenorth:transcript:NVDA:{day}', klass='公司材料', category='T4', channel='TrueNorth',
            source_uri=f'truenorth-mcp://financial_earnings_transcript/NVDA/{day}', publisher='NVIDIA Corporation',
            publisher_type='company', published_at=day + 'T21:00:00Z', publication_day=day, day_source='call',
            document_format='transcript', title=transcript.get('headline'), text=transcript.get('body_markdown') or '',
            coverage='full', source='truenorth', retrieved_at=record.get('retrieved_at'),
            extra=json.dumps({'event_organizer': 'company', 'quarter_label': transcript.get('quarter_label')})))
    folder = os.path.join(base, 'transcripts-peers')
    for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        record = read_json(os.path.join(folder, name))
        transcript = record['transcript']
        ticker = record['ticker']
        day = str(transcript['call_date'])[:10]
        rows.append(item(
            input_id=f'truenorth:transcript:{ticker}:{day}', klass='公司材料', category='T4', channel='TrueNorth',
            source_uri=f'truenorth-mcp://financial_earnings_transcript/{ticker}/{day}', publisher=record.get('company_name') or ticker,
            publisher_type='company', published_at=day + 'T21:00:00Z', publication_day=day, day_source='call',
            document_format='transcript', title=transcript.get('headline'), text=transcript.get('body_markdown') or '',
            coverage='full', source='truenorth', topic=f'company-{ticker}', tier='industry',
            object_identifiers=json.dumps(objects_for_company(ticker, record.get('themes'), 'T4', 'the company speaking on its own call')), retrieved_at=record.get('retrieved_at'),
            extra=json.dumps({'event_organizer': 'company', 'quarter_label': transcript.get('quarter_label')})))
    return rows


def truenorth_story_items(pages):
    """TrueNorth's clustered stories: the item is the original article when its page was fetched; otherwise only the
    provider's own summary exists, which is kept for the review and never fed."""
    rows = []
    folder = os.path.join(RAW, 'truenorth', 'news')
    for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        record = read_json(os.path.join(folder, name))
        story = record['story']
        moment = datetime.datetime.fromtimestamp(int(story.get('published_at') or 0) / 1000, tz=datetime.timezone.utc)
        listing_day = new_york_day(moment)
        url = (story.get('source_url') or '').strip()
        domain = domain_of(url) or (story.get('publisher') or '').lower()
        page = pages.get(url, {})
        title = story.get('title') or ''
        text, cut, coverage = page_texts(page, url)
        publisher, kind, identified = page_author(domain, title, text)
        page_day = page.get('page_day') or ''
        if not page.get('file'):
            text = title + '\n\n[provider summary, not the article]\n' + (story.get('summary') or story.get('preview') or '')
            coverage = 'provider_summary'
        day = earlier(listing_day, page_day) or listing_day
        rows.append(item(
            input_id=f'truenorth:story:{story["story_id"]}', klass='新闻', category=news_category(kind), channel='TrueNorth event index',
            source_uri=url, publisher=publisher or story.get('publisher'), publisher_type=kind, published_at=moment.isoformat(timespec='seconds'),
            publication_day=day, day_source='page' if page_day and page_day < listing_day else 'listing', listing_day=listing_day, page_day=page_day,
            document_format='article', title=title, text=text, text_article=cut, coverage=coverage, source='truenorth',
            retrieved_at=page.get('fetched_at') or record.get('retrieved_at'),
            extra=json.dumps({'event_type': story.get('event_type'), 'event_count': story.get('event_count'), 'rank': story.get('final_rank_score'),
                              'provider_summary': story.get('summary') or story.get('preview'), 'author_unidentified': not identified})))
    return rows


# ---------- company sites ----------

def newsroom_category(title):
    """A release that reports a period's results is T1; one that schedules the results call is an ordinary release (T6)."""
    return 'T1' if re.search(r'(?:reports|announces) .*financial results', title, re.I) and not re.search(r'conference call', title, re.I) else 'T6'


def nvidianews_items():
    manifest = read_json(os.path.join(RAW, 'nvidianews', 'manifest.json'), {'releases': []})
    rows = []
    for release in manifest['releases']:
        text = full_text_of(os.path.join(RAW, 'nvidianews', release['file'][:-5]))
        title = release.get('title') or ''
        category = newsroom_category(title)
        rows.append(item(
            input_id=f'nvidianews:{release["url"].rsplit("/", 1)[-1][:120]}', klass='公司材料', category=category, channel='company newsroom',
            source_uri=release['url'], publisher='NVIDIA Corporation', publisher_type='company', published_at=release['date'] + 'T12:00:00Z',
            publication_day=release['date'], day_source='page', page_day=release['date'], document_format='release', title=title, text=text,
            coverage='full' if len(text) > 200 else 'none', source='nvidianews', retrieved_at=release.get('retrieved_at')))
    return rows


def nvblog_items():
    manifest = read_json(os.path.join(RAW, 'nvblog', 'manifest.json'), {'posts': []})
    rows = []
    for post in manifest['posts']:
        text = full_text_of(os.path.join(RAW, 'nvblog', post['file'][:-5]))
        rows.append(item(
            input_id=f'nvblog:{post["url"].rstrip("/").rsplit("/", 1)[-1][:120]}', klass='公司材料', category='T6', channel='company blog',
            source_uri=post['url'], publisher='NVIDIA Corporation', publisher_type='company', published_at=post['date'] + 'T12:00:00Z',
            publication_day=post['date'], day_source='page', page_day=post['date'], document_format='article', title=post.get('title'), text=text,
            coverage='full' if len(text) > 200 else 'none', source='nvblog', retrieved_at=post.get('retrieved_at')))
    return rows


def extra_items():
    """Hand-listed pages from research (transcripts, blog posts), with the classification the list gives."""
    manifest = read_json(os.path.join(RAW, 'extra', 'manifest.json'), {'pages': []})
    rows = []
    for page in manifest['pages']:
        if not page.get('file'):
            continue
        text = full_text_of(os.path.join(RAW, 'extra', page['file']))
        if len(text) < 200:
            continue   # a blocked or script-rendered page; nothing to read
        klass = '公司材料' if page['publisher_type'] == 'company' else '新闻'
        rows.append(item(
            input_id=f'extra:{page["file"][:24]}', klass=klass, category=page['category'], channel='research list',
            source_uri=page['url'], publisher=page['publisher'], publisher_type=page['publisher_type'], published_at=page['date'] + 'T12:00:00Z',
            publication_day=page['date'], day_source='page', page_day=page['date'], document_format=page.get('document_format', 'article'),
            title=page.get('title'), text=text, coverage='full', source='extra', retrieved_at=page.get('retrieved_at'),
            extra=json.dumps({'note': page.get('note')})))
    return rows


# ---------- official ----------

OFFICIAL_OBJECTS = {
    'fed-press': [{'kind': 'theme', 'value': 'fed-policy-rate', 'why': 'upstream feed: Federal Reserve releases'}],
    'fed-speeches': [{'kind': 'theme', 'value': 'fed-policy-rate', 'why': 'upstream feed: Federal Reserve speeches'}],
    'fed-testimony': [{'kind': 'theme', 'value': 'fed-policy-rate', 'why': 'upstream feed: Federal Reserve testimony'}],
    'fr-bis': [{'kind': 'theme', 'value': 'chip-export-controls', 'why': 'upstream feed: BIS in the Federal Register'}],
    'fr-ustr': [{'kind': 'theme', 'value': 'us-china-tariffs', 'why': 'upstream feed: USTR in the Federal Register'}],
    'fr-commerce': [{'kind': 'theme', 'value': 'us-china-tariffs', 'why': 'upstream feed: Commerce in the Federal Register'}],
    'bls-cpi': [{'kind': 'theme', 'value': 'us-inflation', 'why': 'upstream feed: BLS CPI'}],
    'bls-ppi': [{'kind': 'theme', 'value': 'us-inflation', 'why': 'upstream feed: BLS PPI'}],
    'bls-empsit': [{'kind': 'theme', 'value': 'us-recession-risk', 'why': 'upstream feed: BLS employment'}],
}


def official_objects(source, title):
    """The theme an official document is filed under, by source. The Commerce Department's Federal Register feed
    (fr-commerce) carries no object: it is the deliberate noise tier (fisheries, census, antidumping and countervailing
    proceedings on single goods, foreign-trade-zone notices); export-control actions come from BIS's own feed (fr-bis)
    and tariff actions from USTR's (fr-ustr). Counted 2026-10-24: all 105 Commerce notices a title-keyword rule had
    labelled were antidumping, countervailing, quota or foreign-trade-zone proceedings, none a tariff action."""
    if source == 'fr-commerce':
        return []
    return OFFICIAL_OBJECTS.get(source, [])


OFFICIAL_PUBLISHERS = {
    'fr-bis': 'Bureau of Industry and Security', 'fr-ustr': 'Office of the United States Trade Representative',
    'fr-commerce': 'Department of Commerce', 'bls-cpi': 'Bureau of Labor Statistics', 'bls-ppi': 'Bureau of Labor Statistics',
    'bls-empsit': 'Bureau of Labor Statistics',
}


def official_publisher(source):
    """02-classification 作者规则 3: the author is the agency that issued the document; the Federal Register is the channel."""
    if source in OFFICIAL_PUBLISHERS:
        return OFFICIAL_PUBLISHERS[source]
    return 'Federal Reserve Board' if source.startswith('fed') else source


def official_category(source, url, listed):
    """Federal Reserve: monetary policy material → T11, enforcement and other actions → T10; speeches and testimony
    → T11; Federal Register documents → T10; BLS statistics → T11."""
    if source == 'fed-press':
        return 'T11' if '/monetary' in url else 'T10'
    return listed


def official_items():
    manifest = read_json(os.path.join(RAW, 'official', 'manifest.json'), {'pages': []})
    rows = []
    for page in manifest['pages']:
        text = full_text_of(os.path.join(RAW, 'official', page['file']))
        source = page['source']
        publisher = official_publisher(source)
        objects = official_objects(source, page.get('title'))
        tier = 'macro' if source.startswith(('fed', 'bls')) else ('geopolitics' if objects else 'noise')
        rows.append(item(
            input_id=f'official:{source}:{sha256_text(page["url"])[:20]}', klass='官方材料', category=official_category(source, page['url'], page['category']),
            channel=source, source_uri=page['url'], publisher=publisher, publisher_type='official', published_at=page['date'] + 'T12:00:00Z',
            publication_day=page['date'], day_source='release', document_format='release', title=page.get('title'), text=text,
            coverage='full' if len(text) > 200 else 'none', source='official', topic=source, tier=tier,
            object_identifiers=json.dumps(objects), retrieved_at=page.get('retrieved_at'),
            extra=json.dumps({'note': page.get('note')})))
    return rows


# ---------- news listings ----------

def gdelt_items(pages):
    listing = {}
    gdelt_dir = os.path.join(RAW, 'gdelt')
    for name in sorted(os.listdir(gdelt_dir)) if os.path.isdir(gdelt_dir) else []:
        if not name.endswith('.jsonl'):
            continue
        with open(os.path.join(gdelt_dir, name), encoding='utf-8') as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get('url') and row['url'] not in listing:
                    listing[row['url']] = row
    rows = []
    for url, row in listing.items():
        seen = row.get('seendate') or ''
        moment = datetime.datetime.strptime(seen, '%Y%m%dT%H%M%SZ').replace(tzinfo=datetime.timezone.utc) if seen else None
        listing_day = new_york_day(moment) if moment else ''
        page = pages.get(url, {})
        page_day = page.get('page_day') or ''
        day = earlier(listing_day, page_day)
        if not (WINDOW_START <= day <= WINDOW_END):
            continue
        domain = domain_of(url)
        text, cut, coverage = page_texts(page, url)
        title = row.get('title') or page.get('page_title') or ''
        publisher, kind, identified = page_author(domain, title, text)
        rows.append(item(
            input_id=f'gdelt:{sha256_text(url)[:24]}', klass='新闻', category=news_category(kind), channel='GDELT listing',
            source_uri=url, publisher=publisher, publisher_type=kind, published_at=moment.isoformat(timespec='seconds') if moment else None,
            publication_day=day, day_source='page' if page_day and page_day < listing_day else 'listing', listing_day=listing_day, page_day=page_day,
            document_format='article', title=title, text=text or title, text_article=cut, coverage=coverage, source='gdelt',
            retrieved_at=page.get('fetched_at') or now_iso(),
            extra=json.dumps({'status': page.get('status'), 'paragraphs': page.get('paragraphs'), 'sourcecountry': row.get('sourcecountry'),
                              'author_unidentified': not identified})))
    return rows


def gnews_items(pages):
    """Google News headlines whose publisher URL was resolved: one item per URL; a URL found under several topics
    carries every topic and the union of their objects."""
    resolved = os.path.join(RAW, 'gnews', 'resolved.jsonl')
    if not os.path.exists(resolved):
        return []
    by_link = {}
    with open(resolved, encoding='utf-8') as handle:
        for line in handle:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get('url'):
                by_link[row['google_link']] = row   # the newest line per Google link wins (re-resolved URLs)
    by_url = collections.OrderedDict()
    for row in by_link.values():
        entry = by_url.setdefault(row['url'].strip(), {'rows': [], 'topics': [], 'queries': []})
        entry['rows'].append(row)
        topic = row.get('topic') or 'nvda'
        if topic not in entry['topics']:
            entry['topics'].append(topic)
        if row.get('query') and row['query'] not in entry['queries']:
            entry['queries'].append(row['query'])
    rows = []
    for url, entry in by_url.items():
        first = entry['rows'][0]
        listing_day = earlier(*[rfc_day(r.get('published') or '') or r.get('day') or '' for r in entry['rows']])
        page = pages.get(url, {})
        page_day = page.get('page_day') or ''
        day = earlier(listing_day, page_day)
        if not (WINDOW_START <= day <= WINDOW_END):
            continue
        domain = domain_of(url)
        text, cut, coverage = page_texts(page, url)
        title = re.sub(r'\s+-\s+[^-]+$', '', first.get('title') or '')
        publisher, kind, identified = page_author(domain, title, text)
        topics = entry['topics']
        tiers = [TOPICS.get(t, {}).get('tier', 'core') for t in topics]
        tier = 'core' if 'core' in tiers else tiers[0]
        rows.append(item(
            input_id=f'gnews:{sha256_text(url)[:24]}', klass='新闻', category=news_category(kind), channel='Google News listing',
            source_uri=url, publisher=publisher, publisher_type=kind, published_at=first.get('published'),
            publication_day=day, day_source='page' if page_day and page_day < listing_day else 'listing', listing_day=listing_day, page_day=page_day,
            document_format='article', title=title, text=text or title, text_article=cut, coverage=coverage, source='gnews',
            topic=','.join(topics), tier=tier, object_identifiers=json.dumps(objects_for_topic(topics)),
            retrieved_at=page.get('fetched_at') or first.get('resolved_at'),
            extra=json.dumps({'status': page.get('status'), 'paragraphs': page.get('paragraphs'), 'google_source': first.get('source'),
                              'queries': entry['queries'], 'blocked': page.get('blocked'), 'truncated': page.get('truncated'),
                              'author_unidentified': not identified})))
    return rows


# ---------- copies ----------

def rows_same_document(row, original):
    """Two company or official rows at one URL are the same document only when their text is the same."""
    return row['content_sha256'] == original['content_sha256']


def mark_copies(rows):
    """Same canonical URL → copy, whatever the two rows' kinds (a Google News listing of an NVIDIA newsroom release
    is a copy of the newsroom original; counted 2026-10-24: 28 such pairs were two items). Same normalised title on
    the same day → copy only when one side is an aggregator or both have the same author (02-classification: a copy
    is the same content republished; an aggregator page's author is the byline's outlet, so a Motley Fool piece on
    Yahoo is a copy of the one on fool.com); two outlets with the same headline stay two items."""
    by_url = {}
    by_title = collections.defaultdict(list)
    # the original of a URL is the company's or official copy when there is one, else the earliest listing
    order = {'公司材料': 0, '官方材料': 1, '新闻': 2}
    for row in sorted(rows, key=lambda r: (order.get(r['klass'], 3), r['publication_day'], r['published_at'] or '')):
        key = canonical_url(row['source_uri'])
        if not key or key == 'https://':
            continue
        if key in by_url:
            if row['klass'] == '新闻' or rows_same_document(row, by_url[key]):
                row['copy_of'] = by_url[key]['input_id']
            continue
        by_url[key] = row
    for row in sorted(rows, key=lambda r: (r['publication_day'], r['published_at'] or '')):
        if row['klass'] != '新闻' or row['copy_of']:
            continue
        by_title[(row['publication_day'], normalise_title(row['title']))].append(row)
    for (_, title), group in by_title.items():
        if len(group) < 2 or len(title) < 20:
            continue
        originals = [r for r in group if domain_of(r['source_uri']) not in AGGREGATORS] or group
        original = originals[0]
        for row in group:
            if row is original or row['copy_of']:
                continue
            same_publisher = row['publisher'] == original['publisher']
            aggregator = domain_of(row['source_uri']) in AGGREGATORS or domain_of(original['source_uri']) in AGGREGATORS
            if same_publisher or aggregator:
                row['copy_of'] = original['input_id']
    return rows


# ---------- build ----------

def run():
    pages = pages_index()
    rows = (edgar_items() + edgar_peer_items() + transcript_items() + truenorth_story_items(pages) + official_items()
            + nvidianews_items() + nvblog_items() + extra_items() + gdelt_items(pages) + gnews_items(pages))
    rows = mark_copies(rows)
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.executescript(SCHEMA)
    columns = ['input_id', 'klass', 'category', 'content_sha256', 'copy_of', 'supersedes', 'channel', 'source_uri', 'publisher',
               'publisher_type', 'authors', 'published_at', 'publication_day', 'day_source', 'listing_day', 'page_day', 'retrieved_at',
               'is_structured', 'has_readable_text', 'document_format', 'channel_category', 'media_type', 'language',
               'object_identifiers', 'title', 'text', 'text_article', 'coverage', 'text_chars', 'bootstrap', 'feed', 'source',
               'topic', 'tier', 'extra']
    conn.executemany(f'insert or replace into items ({",".join(columns)}) values ({",".join("?" * len(columns))})',
                     [[row.get(c) for c in columns] for row in rows])
    conn.commit()
    log('items.sqlite built (klass, rows, originals, fed):', conn.execute('select klass, count(*), sum(copy_of is null), sum(feed) from items group by klass').fetchall())
    log('by tier (tier, rows, fed):', conn.execute('select tier, count(*), sum(feed) from items group by tier').fetchall())
    log('day source (source, rows):', conn.execute('select day_source, count(*) from items group by day_source').fetchall())
    conn.close()


if __name__ == '__main__':
    main_guard(run)
