"""Placement, extraction v20 / poc-v36 (docs/research/2026-10-28-extraction-quality/routing-analysis.md §6): the sift keeps a
statement without a link for the placer; a separate call files the statements under the open theses, each shown with its
code-written 'takes' line; a statement filed nowhere is dropped with the reason 'no home' (D209); a link the extraction gave to
its own candidate is kept. Measured on the frozen gold over three draws: core statements filed right 55% → 80%, wrong links 9 → 4.
Real ledger and archive on temporary paths; a scripted model; the universe file the pipeline reads."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction, model, placement, universe  # noqa: E402
from test_theme_block import ledger  # noqa: E402

UNI = universe.load(os.path.join(ROOT, 'poc', 'universe.json'))
V36 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v36.json'))
V35 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v35.json'))
TEXT = ('Nvidia said on Aug 10 it has partnered six major financial institutions to launch compute financing platforms aimed at raising more than '
        'US$500 billion in third-party capital for AI infrastructure. In May, Nvidia chief financial officer Colette Kress said the H200 chips had yet to '
        'generate any revenue for the company in China. Nvidia shares climbed 3.7 per cent on July 8.')
ITEM = {'input_id': 'gnews:deb37e6ad15fb74d545ca368', 'category': 'T7', 'publication_day': '2026-08-10', 'publisher': 'straitstimes.com', 'publisher_type': 'media',
        'title': 'Nvidia partners Wall Street giants to raise $640 billion for AI infrastructure', 'object_identifiers': [{'kind': 'ticker', 'value': 'NVDA'}], 'text': TEXT}
PLATFORM = {'id': 'e1', 'quote': 'Nvidia said on Aug 10 it has partnered six major financial institutions to launch compute financing platforms aimed at raising more than US$500 billion in third-party capital for AI infrastructure.',
            'one_line': 'NVIDIA partnered six institutions to raise over $500bn for AI infrastructure.', 'speaker': 'NVIDIA', 'original_who': 'NVIDIA', 'original_day': '2026-08-10', 'tier': 'party_statement', 'event_time': '', 'links': []}
KRESS = {'id': 'e2', 'quote': 'Nvidia chief financial officer Colette Kress said the H200 chips had yet to generate any revenue for the company in China.',
         'one_line': 'CFO Kress said H200 had generated no China revenue as of May.', 'speaker': 'Colette Kress', 'original_who': 'NVIDIA CFO Colette Kress', 'original_day': '', 'tier': 'party_statement', 'event_time': '', 'links': ['v9']}


def test_v20_sift_keeps_a_statement_without_a_link_and_v19_drops_it():
    answer = {'candidates': [], 'evidence': [PLATFORM]}
    kept, _, dropped = extraction.sift(answer, ITEM, TEXT, {'v1'}, english=True, keep_unlinked=True)
    assert [e['id'] for e in kept] == ['e1'] and kept[0]['links'] == [] and dropped == []
    kept, _, dropped = extraction.sift(answer, ITEM, TEXT, {'v1'}, english=True)
    assert kept == [] and dropped == [('e1', 'links to nothing shown: []')]


def test_the_placer_files_statements_keeps_candidate_links_and_returns_the_rest_unfiled(tmp_path):
    conn = ledger(tmp_path)
    shown = extraction.shown_views(conn, V36, ITEM, ['NVDA'])
    assert [v['view_id'] for v in shown] == ['v1', 'v2'] and all('key' in v for v in shown)
    seen = {}

    def transport(provider, request):
        seen['request'] = request
        data = {'placements': [{'id': 'e1', 'links': []}, {'id': 'e2', 'links': ['v2', 'v99']}, {'id': 'e3', 'links': ['v1']}]}
        return {'choices': [{'message': {'content': json.dumps(data)}}]}

    statements = [PLATFORM, dict(KRESS, links=['c1']), dict(PLATFORM, id='e3', links=['v1'])]
    placed, unfiled, answer = placement.place(model.Archive(str(tmp_path / 'archive.sqlite')), V36, statements, shown, transport=transport)
    user = seen['request']['messages'][1]['content']
    assert '[Open questions]' in user and 'takes: ' in user and '- e2 [party_statement] who: NVIDIA CFO Colette Kress' in user
    assert [e['id'] for e in unfiled] == ['e1']                                    # filed nowhere: returned for the caller to drop
    assert [(e['id'], e['links']) for e in placed] == [('e2', ['c1', 'v2']), ('e3', ['v1'])]   # the candidate link survives; v99 is not a shown thesis
    assert answer.request_sha256 and seen['request']['response_format']['json_schema']['name'] == 'placement'


def test_v20_extraction_places_and_drops_the_unfiled_with_its_reason_and_v19_does_not_call_the_placer(tmp_path):
    conn = ledger(tmp_path)
    calls = []

    def transport(provider, request):
        name = request['response_format']['json_schema']['name']
        calls.append(name)
        if name == 'extraction':
            data = {'candidates': [], 'evidence': [PLATFORM, dict(KRESS, links=[])], 'new_groups': []}
        else:
            data = {'placements': [{'id': 'e1', 'links': []}, {'id': 'e2', 'links': ['v2']}]}
        return {'choices': [{'message': {'content': json.dumps(data)}}]}

    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    handover = extraction.extract(archive, V36, ITEM, TEXT, extraction.shown_views(conn, V36, ITEM, ['NVDA']), UNI, transport=transport)
    assert calls == ['extraction', 'placement']
    assert [(e['id'], e['links']) for e in handover.evidence] == [('e2', ['v2'])] and handover.dropped == [('e1', 'no home')]
    calls.clear()
    archive = model.Archive(str(tmp_path / 'archive-v35.sqlite'))        # v19 and v20 extraction requests are the same bytes; a shared archive would serve the stored answer
    handover = extraction.extract(archive, V35, ITEM, TEXT, extraction.shown_views(conn, V35, ITEM, ['NVDA']), UNI, transport=transport)
    assert calls == ['extraction'] and handover.evidence == [] and [d[0] for d in handover.dropped] == ['e1', 'e2']   # v19: no placer, the unlinked pieces drop as before
