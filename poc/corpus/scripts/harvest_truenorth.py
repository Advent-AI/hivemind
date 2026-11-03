"""Harvest NVDA material from the TrueNorth data service: news stories (90 days), earnings-call transcripts,
and the full text of filings. `--events` harvests the story index by topic instead (Alex, 2026-10-27: NVIDIA,
geopolitics and the chip supply chain): every topic in topics.json with a `truenorth` key names its selectors
(canonical asset ids and text queries) and the window is WINDOW_START..today. Read-only. Needs TRUENORTH_MCP_TOKEN in the environment (run through
../tn-hivemind/scripts/with_credentials.py --only TRUENORTH_MCP_TOKEN). Uses the old repository's read-only client.

Writes raw/truenorth/news/<story_id>.json, raw/truenorth/transcripts/<date>.json, raw/truenorth/filings/<accession>.json
and raw/truenorth/manifest.json. Re-running skips what exists.
"""
import datetime
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'tn-hivemind', 'src')))
from common import RAW, log, write_json, read_json, now_iso, main_guard, BOOTSTRAP_START, WINDOW_START  # noqa: E402
from tn_hivemind.models.truenorth import TrueNorthMCP, tool_payload, MCPError  # noqa: E402

SYMBOL = 'NVDA'
ASSET = 'stock_nvda'
OUT = os.path.join(RAW, 'truenorth')
EVENT_TYPES = ('earnings', 'capital_markets', 'mna', 'market_move', 'product_launch', 'regulatory_policy',
               'legal_regulatory', 'institutional_adoption', 'other',
               # seen in the index on 2026-10-27 (geopolitics and supply-chain probes)
               'geopolitical_event', 'guidance', 'exchange_listing', 'sec_filing')
PAGE = 100     # event_v2's largest page; the index has no offset, so a selector over the cap is sliced by event type and sort


def call(client, name, arguments, pause=1.0):
    for attempt in range(3):
        try:
            payload = tool_payload(client.call_tool(name, arguments))
            time.sleep(pause)
            return payload
        except MCPError as error:
            log('MCP failure', name, arguments, str(error))
            time.sleep(5 * (attempt + 1))
    return {}


def harvest_news(client, manifest):
    stories = {}
    searches = 0
    for sort_by in ('time', 'relevance'):
        for event_type in (None,) + EVENT_TYPES:
            arguments = {'token_address': ASSET, 'sort_by': sort_by, 'time_window': '90d', 'limit': 100,
                         'include_full_summary': True}
            if event_type:
                arguments['event_type'] = event_type
            payload = call(client, 'event_v2', arguments)
            searches += 1
            results = payload.get('results') or []
            log(f'event_v2 {sort_by} {event_type or "all"}: {len(results)} results, total_results={payload.get("total_results")}')
            for story in results:
                story_id = story.get('story_id')
                if story_id and story_id not in stories:
                    stories[story_id] = {'story': story, 'search': arguments, 'retrieved_at': now_iso()}
    for story_id, entry in stories.items():
        path = os.path.join(OUT, 'news', story_id + '.json')
        if not os.path.exists(path):
            write_json(path, entry)
    manifest['news'] = {'stories': len(stories), 'searches': searches, 'retrieved_at': now_iso()}
    log(f'news stories saved: {len(stories)}')


def topic_selectors():
    """(topic id, event_v2 selector) for every topic that names TrueNorth selectors in topics.json."""
    topics = read_json(os.path.join(os.path.dirname(__file__), 'topics.json'))['topics']
    selectors = []
    for topic in topics:
        spec = topic.get('truenorth') or {}
        for address in spec.get('token_addresses', []):
            selectors.append((topic['id'], {'token_address': address}))
        for query in spec.get('queries', []):
            selectors.append((topic['id'], {'query': query}))
    return selectors


def window_days(today):
    """event_v2 takes a recency window, not a date range: the days from WINDOW_START to today, inclusive."""
    start = datetime.date.fromisoformat(WINDOW_START)
    return f'{(today - start).days + 1}d'


def search_events(client, selector, time_window):
    """Every story the index returns for one selector: one call when the total fits a page, otherwise the page of each
    event type under both sort orders (the index returns at most PAGE stories per call and has no offset).
    Returns {story_id: story} and the number of calls."""
    base = dict(selector, time_window=time_window, limit=PAGE, include_full_summary=True)
    stories, calls = {}, 0

    def take(arguments):
        nonlocal calls
        payload = call(client, 'event_v2', arguments)
        calls += 1
        results = payload.get('results') or []
        for story in results:
            if story.get('story_id'):
                stories.setdefault(story['story_id'], story)
        return len(results), payload.get('total_results') or 0

    returned, total = take(dict(base, sort_by='time'))
    if total > returned:
        take(dict(base, sort_by='relevance'))
        for event_type in EVENT_TYPES:
            returned, total = take(dict(base, sort_by='time', event_type=event_type))
            if total > returned:
                take(dict(base, sort_by='relevance', event_type=event_type))
    return stories, calls


def harvest_topic_events(client, manifest, today=None):
    """The story index by topic over the window. A story found by several selectors is one file carrying every topic
    and selector that found it; a file the NVDA harvest wrote earlier gains the topics it is found under now."""
    today = today or datetime.date.today()
    time_window = window_days(today)
    summary = {'window': f'{WINDOW_START}..{today.isoformat()}', 'time_window': time_window, 'selectors': [], 'retrieved_at': now_iso()}
    new_files, touched = 0, set()
    for topic_id, selector in topic_selectors():
        stories, calls = search_events(client, selector, time_window)
        log(f'event_v2 {topic_id} {selector}: {len(stories)} stories in {calls} calls')
        summary['selectors'].append({'topic': topic_id, **selector, 'stories': len(stories), 'calls': calls})
        for story_id, story in stories.items():
            path = os.path.join(OUT, 'news', story_id + '.json')
            record = read_json(path) or {'story': story, 'retrieved_at': now_iso()}
            record.setdefault('topics', ['nvda'] if 'selectors' not in record and os.path.exists(path) else [])
            record.setdefault('selectors', [])
            if topic_id not in record['topics']:
                record['topics'].append(topic_id)
            found_by = {'topic': topic_id, **selector}
            if found_by not in record['selectors']:
                record['selectors'].append(found_by)
            new_files += not os.path.exists(path)
            touched.add(story_id)
            write_json(path, record)
    summary['stories_touched'] = len(touched)
    summary['stories_new'] = new_files
    manifest['events'] = summary
    log(f'topic events: {len(touched)} stories touched, {new_files} new files')


def harvest_transcripts(client, manifest):
    payload = call(client, 'financial_earnings_transcript', {'ticker': SYMBOL, 'limit': 8})
    saved = []
    for transcript in payload.get('transcripts') or []:
        date = str(transcript.get('call_date'))[:10]
        if date < BOOTSTRAP_START:
            continue
        path = os.path.join(OUT, 'transcripts', date + '.json')
        if not os.path.exists(path):
            write_json(path, {'transcript': transcript, 'retrieved_at': now_iso()})
        saved.append({'call_date': date, 'headline': transcript.get('headline'),
                      'chars': len(transcript.get('body_markdown') or '')})
    manifest['transcripts'] = saved
    log('transcripts:', saved)


def harvest_filings(client, manifest):
    payload = call(client, 'financial_sec_filings', {'symbol': SYMBOL, 'filing_type': '10-K,10-Q,8-K', 'limit': 40})
    saved = []
    for filing in payload.get('filings') or []:
        date = str(filing.get('filing_date'))[:10]
        if date < BOOTSTRAP_START:
            continue
        accession = filing['accession_number']
        path = os.path.join(OUT, 'filings', accession + '.json')
        if os.path.exists(path):
            record = read_json(path)
        else:
            document = call(client, 'financial_sec_filing_items',
                            {'symbol': SYMBOL, 'accession_number': accession, 'filing_type': filing['filing_type'],
                             'full_text': True}, pause=2.0)
            record = {'filing': filing, 'document': document, 'retrieved_at': now_iso()}
            write_json(path, record)
        text = ((record.get('document') or {}).get('filing_document') or {}).get('full_text') or ''
        saved.append({'filing_date': date, 'filing_type': filing['filing_type'], 'accession': accession,
                      'items': filing.get('items'), 'chars': len(text)})
    manifest['filings'] = saved
    log('filings:', [(s['filing_date'], s['filing_type'], s['chars']) for s in saved])


def harvest_peer_transcripts(client, manifest):
    """Earnings calls in the window for the peer, supplier and customer companies (companies.json)."""
    companies = read_json(os.path.join(os.path.dirname(__file__), 'companies.json'))['companies']
    saved = manifest.get('peer_transcripts', [])
    have = {(s['ticker'], s['call_date']) for s in saved}
    for company in companies:
        ticker = company['ticker']
        payload = call(client, 'financial_earnings_transcript', {'ticker': ticker, 'limit': 4})
        for transcript in payload.get('transcripts') or []:
            date = str(transcript.get('call_date'))[:10]
            if not ('2026-07-24' <= date <= '2026-10-22') or (ticker, date) in have:
                continue
            path = os.path.join(OUT, 'transcripts-peers', f'{ticker}-{date}.json')
            write_json(path, {'ticker': ticker, 'company_name': company['name'], 'themes': company['themes'],
                              'transcript': transcript, 'retrieved_at': now_iso()})
            saved.append({'ticker': ticker, 'call_date': date, 'headline': transcript.get('headline'),
                          'chars': len(transcript.get('body_markdown') or '')})
            have.add((ticker, date))
    manifest['peer_transcripts'] = saved
    log('peer transcripts:', [(s['ticker'], s['call_date'], s['chars']) for s in saved])


def run():
    token = os.environ.get('TRUENORTH_MCP_TOKEN')
    if not token:
        raise SystemExit('TRUENORTH_MCP_TOKEN is not in the environment; run through with_credentials.py')
    client = TrueNorthMCP(token)
    manifest = read_json(os.path.join(OUT, 'manifest.json'), {})
    if '--peers' in sys.argv:
        harvest_peer_transcripts(client, manifest)
    elif '--events' in sys.argv:
        harvest_topic_events(client, manifest)
    else:
        harvest_news(client, manifest)
        harvest_transcripts(client, manifest)
        harvest_filings(client, manifest)
    write_json(os.path.join(OUT, 'manifest.json'), manifest)
    log('done')


if __name__ == '__main__':
    main_guard(run)
