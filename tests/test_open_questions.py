"""Extraction v71 / poc-v82 (D251, D252; design-v71-production.md): the request shows the questions open at the start of the item's
day as a daily snapshot, one line each; the schema carries new_in_it and moves first; a statement the extraction links to a shown
question is filed there and the placement call sees only the rest; versions before 71 are unchanged. Real ledger and archive on
temporary paths; a scripted model; the universe file the pipeline reads."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction, model  # noqa: E402
from hivemind.views import store  # noqa: E402
from test_placement import ITEM, KRESS, PLATFORM, TEXT, UNI  # noqa: E402
from test_theme_block import ASSET_RUNGS, ledger  # noqa: E402

V82 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v82.json'))
V69 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v69.json'))


def margin_view(conn, seq):
    store.create_view(conn, view_id='v3', object_id='NVDA', object_kind='company', kind='asset', looks_at='FY2027 gross margin',
                      question='What gross margin will NVIDIA report for FY2027?', due_day='2027-02-24', year='FY2027', rungs=ASSET_RUNGS, seq=seq,
                      input_id='gnews:margin', created_at='2026-08-09T22:00:00Z')


def block(cfg, conn, item):
    shown = extraction.shown_views(conn, cfg, item, ['NVDA'])
    _, _, user, schema = extraction.request_for(cfg, item, TEXT, shown, UNI)
    start = user.find('[Open questions')
    return (user[start:user.find('\n\n', start)] if start >= 0 else None), schema, shown


def test_v71_shows_the_questions_open_at_the_start_of_the_day_and_v69_shows_none(tmp_path):
    conn = ledger(tmp_path)                                   # v1 (asset) and v2 (theme) created at seq 1; no day completed yet
    assert block(V82, conn, ITEM)[0] == '[Open questions at the start of 2026-08-10]\n  None yet.'       # D251: before the first completed day the list is empty
    store.complete_day(conn, '2026-08-09', 1, '2026-08-09T23:00:00Z')
    margin_view(conn, seq=2)                                  # opened during 2026-08-10: not in that day's snapshot
    conn.commit()
    shown_block, schema, shown = block(V82, conn, ITEM)
    assert shown_block == ('[Open questions at the start of 2026-08-10]\n'
                           '  - v1 (asset NVDA, due 2027-02-24): Where will NVIDIA FY2027 data center revenue land?\n'
                           '  - v2 (theme chip-export-controls, due 2027-01-31): Will the Chinese authorities allow any H200 imports into China by January 31, 2027?')
    store.close_view(conn, 'v2', 'test', 'test', 1)           # closed at seq 1: closed at the start of the day
    conn.commit()
    assert [v['view_id'] for v in extraction.shown_views(conn, V82, ITEM, ['NVDA'])] == ['v1']
    assert block(V69, conn, ITEM)[0] is None                  # D211: the ledger-blind request shows nothing


def test_v71_request_bytes_are_the_same_for_every_item_of_the_day_whatever_opens_within_it(tmp_path):
    conn = ledger(tmp_path)
    store.complete_day(conn, '2026-08-09', 1, '2026-08-09T23:00:00Z')
    conn.commit()
    before = extraction.request_for(V82, ITEM, TEXT, extraction.shown_views(conn, V82, ITEM, ['NVDA']), UNI)[2]
    margin_view(conn, seq=2)                                  # a commit within the day opens a question
    conn.commit()
    after = extraction.request_for(V82, ITEM, TEXT, extraction.shown_views(conn, V82, ITEM, ['NVDA']), UNI)[2]
    assert before == after                                    # the parallel day finds no stale request
    store.complete_day(conn, '2026-08-10', 2, '2026-08-10T23:00:00Z')
    conn.commit()
    next_day = extraction.request_for(V82, dict(ITEM, publication_day='2026-08-11'), TEXT, extraction.shown_views(conn, V82, dict(ITEM, publication_day='2026-08-11'), ['NVDA']), UNI)[2]
    assert 'v3 (asset NVDA' in next_day and 'v3 (asset NVDA' not in after      # it appears from the next day on


def test_v71_schema_requires_new_in_it_and_moves_first_and_v69_does_not(tmp_path):
    conn = ledger(tmp_path)
    schema = block(V82, conn, ITEM)[1]['properties']['evidence']['items']
    assert list(schema['properties'])[:2] == ['new_in_it', 'moves'] and schema['required'][:2] == ['new_in_it', 'moves']
    assert schema['properties']['moves']['description'] == extraction.FIELD_NOTES_V71['moves']
    old = block(V69, conn, ITEM)[1]['properties']['evidence']['items']
    assert 'new_in_it' not in old['properties'] and 'moves' not in old['required']


def test_v71_files_a_statement_linked_to_a_shown_question_without_the_placer_and_places_only_the_rest(tmp_path):
    conn = ledger(tmp_path)
    store.complete_day(conn, '2026-08-09', 1, '2026-08-09T23:00:00Z')
    conn.commit()
    placement_requests = []

    def transport(provider, request):
        name = request['response_format']['json_schema']['name']
        if name == 'extraction':
            fields = {'new_in_it': 'x', 'moves': 'y'}
            data = {'candidates': [], 'evidence': [dict(PLATFORM, **fields, links=['v1']), dict(KRESS, **fields, links=[]),
                                                   dict(KRESS, **fields, id='e3', quote='Nvidia shares climbed 3.7 per cent on July 8.', links=[])], 'new_groups': []}
        else:
            placement_requests.append(request['messages'][-1]['content'])
            data = {'placements': [{'id': 'e2', 'links': ['v2']}, {'id': 'e3', 'links': []}]}
        return {'choices': [{'message': {'content': json.dumps(data)}}]}

    shown = extraction.shown_views(conn, V82, ITEM, ['NVDA'])
    handover = extraction.extract(archive=model.Archive(str(tmp_path / 'archive.sqlite')), cfg=V82, item=ITEM, text=TEXT, shown_views=shown, universe=UNI, transport=transport)
    assert [(e['id'], e['links']) for e in handover.evidence] == [('e1', ['v1']), ('e2', ['v2'])]    # e1 keeps the extraction's link; e2 is placed
    assert handover.dropped == [('e3', 'no home')]
    assert len(placement_requests) == 1 and 'e1' not in placement_requests[0].split('[Statements')[-1] and 'e2' in placement_requests[0]
    assert all(set(e) >= {'new_in_it', 'moves'} for e in handover.evidence)                          # the two fields travel in the handover


def test_the_review_check_closes_versions_59_to_65_only():
    assert [extraction.reviews(f'v{n}') for n in (58, 59, 65, 66, 71)] == [False, True, True, False, False]
