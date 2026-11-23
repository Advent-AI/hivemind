"""D397 on the product's page (D569, not-judged-display/DESIGN.md): the bundle writer carries each question's parts not judged from
its ladder row: the list, [] when the row lists none, None without a table or a row and before the question's creation; a
malformed row or two rows for one question is refused. Real stores on temporary paths; the rows have the new system's shape."""
import json

import pytest

from hivemind import bundle, dispatch
from hivemind.views import store

RUNGS = [{'label': 'Yes', 'condition': 'MIIT formally approves purchases of the RTX Pro 5500 by 2027-01-31.'},
         {'label': 'Ruled out', 'condition': 'MIIT formally rejects the purchase plans.'},
         {'label': 'Still open', 'condition': 'Neither holds on 2027-01-31.'}]
PARTS = [{'part': 'Whether MIIT caps the quantities approved',
          'why': 'The tracked event is formal approval of purchases; the quantity cap, if any, is not a separate outcome.'},
         {'part': 'Whether Nvidia can ship the product into China and book related revenue',
          'why': 'Those are downstream commercial effects, not the MIIT approval decision being judged.'}]
COLUMNS = 'thesis_id, view_id, status, reason, reference_status, checked_answer, outcome_record, config_checksum, article_seq, article_day, primary key (thesis_id)'


def item_of(input_id):
    return {'title': 'Reuters: China moves to approve RTX Pro 5500 purchases', 'publisher': 'Reuters', 'publisher_type': 'news',
            'category': 'news', 'source_uri': 'https://example.com/a', 'publication_day': '2026-09-27'}


def a_store(tmp_path, *, table=True, rows=(), view_seq=5):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    dispatch.mark(conn, {'input_id': 'gnews:a1', 'publication_day': '2026-09-26'}, 4, 'handed_over')
    dispatch.mark(conn, {'input_id': 'gnews:a2', 'publication_day': '2026-09-27'}, view_seq, 'handed_over')
    store.complete_day(conn, '2026-09-26', 4, '2026-09-26')
    store.complete_day(conn, '2026-09-27', view_seq, '2026-09-27')
    store.create_view(conn, view_id='v7', object_id='chip-export-controls', object_kind='theme', kind='theme', looks_at='MIIT approval of RTX Pro 5500 purchases',
                      question='Will MIIT formally approve purchases of the RTX Pro 5500 by 2027-01-31?', due_day='2027-01-31', year='2027',
                      rungs=RUNGS, seq=view_seq, input_id='gnews:a2', created_at='2026-09-27T00:00:00Z')
    if table:
        conn.execute(f'create table clean_ladders ({COLUMNS})')
        for n, answer in enumerate(rows, 1):
            store.insert(conn, 'clean_ladders', thesis_id=f'clean-{6 + n}', view_id='v7', status='ladder', reason=None, reference_status=None,
                         checked_answer=answer, outcome_record='[]', config_checksum='c', article_seq=view_seq, article_day='2026-09-27')
    conn.commit()
    return conn


def answer(parts, shape=None):
    """A ladder row's checked answer in the new system's shape: v7's event by default, or a figure with a favourable end."""
    body = {'event': {'happened': 'MIIT formally approves the purchases by 2027-01-31.',
                      'ruled_out': {'by_whom': 'MIIT', 'decision': 'MIIT formally rejects the purchase plans.'}}, 'figure': None}
    if shape:
        body = {'event': None, 'figure': {'favourable_end': shape, 'favourable_why': 'test', 'ranges': []}}
    return json.dumps({'ladder': {'question': 'q', 'not_judged': parts, **body}, 'no_ladder': None})


def test_the_bundle_carries_the_rows_parts_and_reasons(tmp_path):
    conn = a_store(tmp_path, rows=[answer(PARTS)])
    assert bundle.view_bundle(conn, item_of, 'v7')['not_judged'] == PARTS


def test_an_empty_list_is_kept_apart_from_no_record(tmp_path):
    assert bundle.view_bundle(a_store(tmp_path, rows=[answer([])]), item_of, 'v7')['not_judged'] == []


def test_a_store_without_the_table_and_a_question_without_a_row_give_none(tmp_path):
    (tmp_path / 'a').mkdir()
    (tmp_path / 'b').mkdir()
    assert bundle.view_bundle(a_store(tmp_path / 'a', table=False), item_of, 'v7')['not_judged'] is None
    assert bundle.view_bundle(a_store(tmp_path / 'b', rows=()), item_of, 'v7')['not_judged'] is None


@pytest.mark.parametrize('bad', ['not json', json.dumps({'ladder': {'not_judged': 'a part'}}), json.dumps({'ladder': {'not_judged': [{'part': 'x'}]}}),
                                 json.dumps({'no_ladder': 'reason'})])
def test_a_malformed_row_is_refused(tmp_path, bad):
    with pytest.raises(ValueError):
        bundle.view_bundle(a_store(tmp_path, rows=[bad]), item_of, 'v7')


def test_two_rows_for_one_question_are_refused(tmp_path):
    with pytest.raises(ValueError, match='2 ladder rows'):
        bundle.view_bundle(a_store(tmp_path, rows=[answer(PARTS), answer([])]), item_of, 'v7')


def test_before_its_creation_the_direct_path_refuses_the_question_and_the_library_leaves_it_out(tmp_path):
    """Changed by the live-store contract (OPERATING-CONTRACT.md, row 3's product-facing contract, council rounds 122 and 123): a direct
    call for a view not visible at its bound refuses the view, so its question and choices are never returned before its creation;
    it was a bundle with the parts suppressed."""
    conn = a_store(tmp_path, rows=[answer(PARTS)])
    with pytest.raises(KeyError, match='not available as of 2026-09-26'):
        bundle.view_bundle(conn, item_of, 'v7', as_of='2026-09-26')
    with pytest.raises(KeyError, match='not available as of 2026-09-26'):
        bundle.not_judged(conn, 'v7', 5, as_of='2026-09-26')
    assert bundle.view_bundle(conn, item_of, 'v7', as_of='2026-09-27')['not_judged'] == PARTS
    store.close_view(conn, 'v7', 'due 2027-01-31, frozen', 'pull', 5)
    conn.commit()
    assert bundle.view_bundle(conn, item_of, 'v7', as_of='2026-09-27')['not_judged'] == PARTS       # a closed question keeps its parts


def test_through_the_library_the_question_and_its_parts_appear_from_its_creation_day_and_stay_after_closing(tmp_path):
    conn = a_store(tmp_path, rows=[answer(PARTS)])
    listed = lambda day: {v['view_id']: v['not_judged'] for v in bundle.library(conn, None, as_of=day)['views']}
    assert listed('2026-09-26') == {}
    assert listed('2026-09-27') == {'v7': PARTS}
    store.close_view(conn, 'v7', 'due 2027-01-31, frozen', 'pull', 5)
    conn.commit()
    assert listed('2026-09-27') == {'v7': PARTS}


def test_the_answer_shape_reads_the_row_and_the_store_not_only_the_row(tmp_path):
    """page-contract/DESIGN.md: the store is the discriminator: no table is a legacy ledger (None); a store with rows gives the
    row's shape, and 'unrecorded' for a question without a row; a row that is neither shape is refused."""
    for name, kwargs, expected in (('event', {'rows': [answer(PARTS)]}, ('event', None)),
                                   ('higher', {'rows': [answer([], 'higher')]}, ('figure', 'higher')),
                                   ('theme', {'rows': [answer([], 'n/a')]}, ('figure', 'n/a')),
                                   ('legacy', {'table': False}, (None, None)),
                                   ('unrecorded', {'rows': ()}, ('unrecorded', None))):
        (tmp_path / name).mkdir()
        got = bundle.view_bundle(a_store(tmp_path / name, **kwargs), item_of, 'v7')
        assert (got['answer_shape'], got['favourable_end']) == expected, name
    (tmp_path / 'neither').mkdir()
    with pytest.raises(ValueError, match='neither an event nor a figure'):
        bundle.view_bundle(a_store(tmp_path / 'neither', rows=[json.dumps({'ladder': {'not_judged': [], 'event': None, 'figure': None}})]), item_of, 'v7')
