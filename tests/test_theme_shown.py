"""Proposal A (docs/research/2026-10-28-extraction-quality/results.md): from extraction v19 (`poc-v35`) a company item's extraction
request shows every open theme thesis beside the objects' own, so a statement about a theme matter can link to it instead of
being dropped (the three-month run: 48 pieces linked only to theme ids the groups block printed and the link check refused;
the H200 key named in every request's reference while v3 was never shown). v18 requests are byte-for-byte as before.
Real ledger on a temporary path; the universe file the pipeline reads; no model."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction, universe  # noqa: E402
from hivemind.views import store  # noqa: E402
from test_theme_block import ASSET_RUNGS, ledger  # noqa: E402

UNI = universe.load(os.path.join(ROOT, 'poc', 'universe.json'))
V35 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v35.json'))
V34 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v34.json'))
ITEM = {'input_id': 'gnews:c8c39f971721fd820aab5c1c', 'category': 'T7', 'publication_day': '2026-07-08', 'publisher': 'straitstimes.com', 'publisher_type': 'media',
        'title': 'China to let AI firms buy Nvidia H200s, says report', 'object_identifiers': [{'kind': 'ticker', 'value': 'NVDA'}],
        'text': 'China plans to allow top artificial intelligence companies to buy a limited amount of H200 chips from Nvidia.'}


def test_the_prompt_list_carries_every_open_theme_thesis_only_when_asked(tmp_path):
    conn = ledger(tmp_path)
    assert [v['view_id'] for v in store.views_for_prompt(conn, ['NVDA'])] == ['v1']
    assert [v['view_id'] for v in store.views_for_prompt(conn, ['NVDA'], themes=True)] == ['v1', 'v2']
    store.create_view(conn, view_id='v3', object_id='ai-capex', object_kind='theme', kind='theme', looks_at='Hyperscaler capex 2026',
                      question='How much will the four largest hyperscalers spend in 2026?', due_day='2027-03-31', year='2026', rungs=ASSET_RUNGS, seq=2,
                      input_id='gnews:capex', created_at='2026-03-01T00:00:00Z')
    store.create_view(conn, view_id='v4', object_id='NVDA', object_kind='company', kind='asset', looks_at='FY2027 gross margin',
                      question='What gross margin will NVIDIA report for FY2027?', due_day='2027-02-24', year='FY2027', rungs=ASSET_RUNGS, seq=3,
                      input_id='gnews:margin', created_at='2026-03-02T00:00:00Z')
    conn.commit()
    assert [v['view_id'] for v in store.views_for_prompt(conn, ['NVDA'], themes=True)] == ['v1', 'v2', 'v3', 'v4']   # one list in creation order
    store.close_view(conn, 'v2', 'test', 'test', 5)
    assert [v['view_id'] for v in store.views_for_prompt(conn, ['NVDA'], themes=True)] == ['v1', 'v3', 'v4']     # a closed theme leaves the list


def test_v19_request_shows_the_theme_thesis_and_lets_links_name_it_and_v18_does_not(tmp_path):
    conn = ledger(tmp_path)
    for cfg, shown_expected in ((V35, ['v1', 'v2']), (V34, ['v1'])):
        shown = extraction.shown_views(conn, cfg, ITEM, ['NVDA'])
        assert [v['view_id'] for v in shown] == shown_expected
        _, _, user, schema = extraction.request_for(cfg, ITEM, ITEM['text'], shown, UNI, ())
        assert ('  - v2 (chip-export-controls' in user) == (cfg is V35)
        assert ('v2' in schema['properties']['candidates']['items']['properties']['folds_into']['pattern']) == (cfg is V35)
    answer = {'candidates': [], 'evidence': [{'id': 'e1', 'quote': ITEM['text'], 'one_line': 'China to allow limited H200 purchases.', 'speaker': 'The Information',
                                              'original_who': 'The Information', 'original_day': '2026-07-08', 'tier': 'rumour', 'event_time': '', 'links': ['v2']}]}
    kept, _, dropped = extraction.sift(answer, ITEM, ITEM['text'], {v['view_id'] for v in extraction.shown_views(conn, V35, ITEM, ['NVDA'])}, english=True)
    assert [e['id'] for e in kept] == ['e1'] and dropped == []
    _, _, dropped = extraction.sift(answer, ITEM, ITEM['text'], {v['view_id'] for v in extraction.shown_views(conn, V34, ITEM, ['NVDA'])}, english=True)
    assert dropped == [('e1', "links to nothing shown: ['v2']")]


def test_v19_groups_block_prints_only_member_ids_the_answer_may_link_to(tmp_path):
    conn = ledger(tmp_path)
    store.create_view(conn, view_id='v3', object_id='AMD', object_kind='company', kind='asset', looks_at='AMD FY2026 data center revenue',
                      question='What data center revenue will AMD report for FY2026?', due_day='2027-02-01', year='FY2026', rungs=ASSET_RUNGS, seq=2,
                      input_id='gnews:amd', created_at='2026-03-01T00:00:00Z')
    store.add_group(conn, group_id='g1', name='AI accelerator demand cycle', scope='Data center accelerator demand at NVIDIA and AMD.', seq=2, input_id='gnews:amd', aliases=['accelerator demand'])
    for view_id in ('v1', 'v2', 'v3'):
        store.add_member(conn, 'g1', view_id, 2, 'gnews:amd')
    conn.commit()
    groups = store.groups_for_prompt(conn, ['NVDA'], ITEM['title'])
    assert {m['view_id'] for m in groups[0]['members']} == {'v1', 'v2', 'v3'}
    _, _, user35, _ = extraction.request_for(V35, ITEM, ITEM['text'], extraction.shown_views(conn, V35, ITEM, ['NVDA']), UNI, groups)
    _, _, user34, _ = extraction.request_for(V34, ITEM, ITEM['text'], extraction.shown_views(conn, V34, ITEM, ['NVDA']), UNI, groups)
    members35 = user35.split('members: ')[1].split('\n')[0]
    members34 = user34.split('members: ')[1].split('\n')[0]
    assert 'v1' in members35 and 'v2' in members35 and 'v3' not in members35       # the AMD thesis is not shown to an NVDA item, so it is not printed
    assert 'v2' in members34 and 'v3' in members34                                   # v18 bytes unchanged
