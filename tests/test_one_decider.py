"""Extraction v72 / poc-v92, the one-decider architecture (D256, chosen by Alex on 2026-11-02; research/2026-11-01-e2e-loop/design-v72.md):
the request shows the questions open at the start of the item's day (D251; the seeds on the first day, D253) each with the takes line
the placer read (placement.takes, one writer: placement.question_lines), the schema defines the evidence field `links` by that rule
(placement.FILING_RULE), the extraction's links file each statement and no placement call is made; a statement linked to nothing is
dropped as 'no home' (D209). The snapshot's takes lines do not change within the day whatever the day's items merge (D251, D257).
Versions 53 and 71 are unchanged. Real ledger and archive on temporary paths; a scripted model; the universe file the pipeline reads."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction, model, placement, seeding  # noqa: E402
from hivemind.views import store  # noqa: E402
from test_placement import ITEM, KRESS, PLATFORM, TEXT, UNI  # noqa: E402
from test_theme_block import ledger  # noqa: E402

V92 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v92.json'))
V91 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v91.json'))
V82 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v82.json'))
SEEDS = os.path.join(ROOT, 'poc', 'seeds', 'nvda-2026-07-01-v2.json')
CANDIDATE = {'id': 'c1', 'object': 'NVDA', 'kind': 'asset', 'looks_at': 'FY2027 stand-alone CPU revenue', 'question': 'How much stand-alone CPU revenue will NVIDIA report for FY2027?',
             'rungs': [{'label': l, 'condition': l, 'lo': None, 'hi': None} for l in ('Strongly bullish', 'Bullish', 'Neutral', 'Bearish', 'Strongly bearish')],
             'due_day': '2027-02-28', 'year': 'FY2027', 'evidence_ids': ['e2'], 'measure': 'product_revenue', 'scope': 'stand-alone CPU', 'period_start': '2026-02-01',
             'period_end': '2027-01-31', 'basis': 'GAAP', 'unit': 'USD', 'event_type': 'n/a', 'opens_as': 'main_driver', 'settled_by': 'the FY2027 annual report', 'group_refs': []}


def snapshot_ledger(tmp_path):
    """The theme-block ledger (v1 asset, v2 theme, both at seq 1) with a key and a research group on v1, and 2026-08-09 completed at seq 1,
    so that 2026-08-10's day-start snapshot holds both questions."""
    conn = ledger(tmp_path)
    store.add_key(conn, 'v1', {'measure': 'segment_revenue', 'scope': 'data center', 'period_start': '2026-02-01', 'period_end': '2027-01-31', 'basis': 'GAAP',
                               'unit': 'USD', 'event_type': 'n/a', 'scope_source': 'model', 'key_version': 2}, 1)
    store.add_group(conn, group_id='g1', name='Hopper-to-Blackwell transition', scope='the data-center platform generation change and its customers', seq=1,
                    input_id='gnews:transition', object_ids=('NVDA',), aliases=('Blackwell ramp',))
    store.add_member(conn, 'g1', 'v1', 1, 'gnews:transition')
    store.complete_day(conn, '2026-08-09', 1, '2026-08-09T23:00:00Z')
    conn.commit()
    return conn


def request(cfg, conn, item):
    shown = extraction.shown_views(conn, cfg, item, ['NVDA'])
    _, _, user, schema = extraction.request_for(cfg, item, TEXT, shown, UNI)
    start = user.find('[Open questions')
    block = user[start:user.find('\n\n', start)] if start >= 0 else None
    return user, block, schema, shown


def test_v72_shows_each_open_question_with_the_takes_line_the_placer_reads_and_defines_links_in_the_schema(tmp_path):
    conn = snapshot_ledger(tmp_path)
    user, block, schema, shown = request(V92, conn, ITEM)
    assert [v['view_id'] for v in shown] == ['v1', 'v2']
    assert block == '[Open questions at the start of 2026-08-10]\n' + '\n'.join(placement.question_lines(shown))      # one writer for both requests
    assert placement.takes(shown[0]) in block and 'segment_revenue figures, guidance, estimates and revisions for data center' in block
    assert "the matter 'Hopper-to-Blackwell transition' (also called Blackwell ramp)" in block
    evidence_fields = schema['properties']['evidence']['items']['properties']
    assert evidence_fields['links']['description'] == placement.FILING_RULE
    assert 'new_in_it' not in evidence_fields and 'moves' not in evidence_fields                 # v71's fields are v71's alone
    assert user.rstrip().endswith('Return only the items you keep.')                                # v66's check ends the request (review-v72.txt)
    # the earlier versions keep their bytes: v71 shows the questions without takes lines and without a links definition, v53 shows none
    _, block_71, schema_71, _ = request(V82, conn, ITEM)
    assert block_71 == ('[Open questions at the start of 2026-08-10]\n'
                        '  - v1 (asset NVDA, due 2027-02-24): Where will NVIDIA FY2027 data center revenue land?\n'
                        '  - v2 (theme chip-export-controls, due 2027-01-31): Will the Chinese authorities allow any H200 imports into China by January 31, 2027?')
    assert 'description' not in schema_71['properties']['evidence']['items']['properties']['links']
    assert request(V91, conn, ITEM)[1] is None


def test_the_first_day_snapshot_holds_the_seeds_and_nothing_an_item_opens_that_day(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    seeding.seed_views(conn, SEEDS, created_at='2026-07-01T00:00:00Z')                             # 22 questions at seq 0 (D253)
    first_day = dict(ITEM, publication_day='2026-07-01')
    assert [v['view_id'] for v in extraction.shown_views(conn, V92, first_day, ['NVDA'])] == [f'v{n}' for n in range(1, 23)]
    store.create_view(conn, view_id='v23', object_id='NVDA', object_kind='company', kind='asset', looks_at='FY2027 gross margin', question='What gross margin will NVIDIA report for FY2027?',
                      due_day='2027-02-24', year='FY2027', rungs=[{'label': l, 'condition': l} for l in ('Strongly bullish', 'Bullish', 'Neutral', 'Bearish', 'Strongly bearish')],
                      seq=1, input_id='gnews:margin', created_at='2026-07-01T09:00:00Z')             # opened by the first day's first item
    conn.commit()
    assert len(extraction.shown_views(conn, V92, first_day, ['NVDA'])) == 22                          # not in the first day's snapshot
    store.complete_day(conn, '2026-07-01', 1, '2026-07-01T23:00:00Z')
    conn.commit()
    assert len(extraction.shown_views(conn, V92, dict(ITEM, publication_day='2026-07-02'), ['NVDA'])) == 23


def test_the_takes_line_is_the_same_for_every_item_of_the_day_whatever_the_day_merges(tmp_path):
    conn = snapshot_ledger(tmp_path)
    before = request(V92, conn, ITEM)[0]
    store.add_group_aliases(conn, 'g1', ['GB300 ramp'], 2, 'gnews:later')                          # D257: an alias merged by an item within 2026-08-10
    conn.commit()
    after = request(V92, conn, ITEM)[0]
    assert after == before and 'GB300 ramp' not in after                                             # the parallel day finds no stale request
    store.complete_day(conn, '2026-08-10', 2, '2026-08-10T23:00:00Z')
    conn.commit()
    assert 'GB300 ramp' in request(V92, conn, dict(ITEM, publication_day='2026-08-11'))[1]           # it appears from the next day on


def test_v72_files_by_its_own_links_drops_the_unlinked_as_no_home_and_makes_no_placement_call(tmp_path):
    conn = snapshot_ledger(tmp_path)
    schema_names = []

    def transport(provider, request):
        schema_names.append(request['response_format']['json_schema']['name'])
        data = {'candidates': [CANDIDATE], 'new_groups': [],
                'evidence': [dict(PLATFORM, links=['v1']), dict(KRESS, links=['c1']),
                             dict(KRESS, id='e3', quote='Nvidia shares climbed 3.7 per cent on July 8.', links=[])]}
        return {'choices': [{'message': {'content': json.dumps(data)}}]}

    assert V92.placement is None                                                                     # no placement setting: a placement call would refuse
    shown = extraction.shown_views(conn, V92, ITEM, ['NVDA'])
    handover = extraction.extract(archive=model.Archive(str(tmp_path / 'archive.sqlite')), cfg=V92, item=ITEM, text=TEXT, shown_views=shown, universe=UNI, transport=transport)
    assert [(e['id'], e['links']) for e in handover.evidence] == [('e1', ['v1']), ('e2', ['c1'])]  # filed under the open question; waiting for its candidate
    assert handover.dropped == [('e3', 'no home')]
    assert [c['id'] for c in handover.candidates] == ['c1']
    assert schema_names == ['extraction']


def test_a_statement_filed_under_a_driver_and_its_root_keeps_the_driver_only(tmp_path):
    """D207's narrowest rule in code (D265, 2026-11-02): in the v92 draws 31–34% of links were the root beside its driver (190–208
    statements a draw under both total and Data Center revenue). The ledger's dependencies decide, transitively."""
    conn = snapshot_ledger(tmp_path)
    store.create_view(conn, view_id='v3', object_id='NVDA', object_kind='company', kind='asset', looks_at='FY2027 Blackwell and Rubin revenue',
                      question='How much revenue will NVIDIA report from Blackwell and Rubin products in FY2027?', due_day='2027-02-24', year='FY2027',
                      rungs=[{'label': l, 'condition': l} for l in ('Strongly bullish', 'Bullish', 'Neutral', 'Bearish', 'Strongly bearish')], seq=1,
                      input_id='seed:test', created_at='2026-08-09T00:00:00Z')
    store.insert(conn, 'dependencies', view_id='v3', depends_on='v1', wait_chain_view_id='', wait_year='', direction='last_end', seq=1)   # v3 is a part of v1
    store.insert(conn, 'dependencies', view_id='v1', depends_on='v2', wait_chain_view_id='', wait_year='', direction='last_end', seq=1)   # v1 hangs on the theme v2
    conn.commit()

    def transport(provider, request):
        data = {'candidates': [], 'new_groups': [],
                'evidence': [dict(PLATFORM, links=['v1', 'v3', 'v2']), dict(KRESS, links=['v1', 'v2']),
                             dict(KRESS, id='e3', quote='Nvidia shares climbed 3.7 per cent on July 8.', links=['v2'])]}
        return {'choices': [{'message': {'content': json.dumps(data)}}]}

    shown = extraction.shown_views(conn, V92, ITEM, ['NVDA'])
    assert {v['view_id']: v['parents'] for v in shown} == {'v1': ['v2'], 'v2': [], 'v3': ['v1']}
    handover = extraction.extract(archive=model.Archive(str(tmp_path / 'archive.sqlite')), cfg=V92, item=ITEM, text=TEXT, shown_views=shown, universe=UNI, transport=transport)
    assert [(e['id'], e['links']) for e in handover.evidence] == [('e1', ['v3']), ('e2', ['v1']), ('e3', ['v2'])]
    assert extraction.narrowest_links(['v1', 'v2'], {'v1': ['v2'], 'v2': []}) == ['v1'] and extraction.narrowest_links(['v2'], {'v1': ['v2']}) == ['v2']
