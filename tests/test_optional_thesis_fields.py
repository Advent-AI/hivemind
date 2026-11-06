"""Alex 2026-11-05: missing thesis dates and ladders do not discard research."""
import pytest

from hivemind import pull
from hivemind.views import matching, store, writing


RUNGS = [{'label': 'Yes', 'condition': 'Yes'}, {'label': 'No', 'condition': 'No'}]


@pytest.mark.parametrize('due,rungs,should_close', [
    ('', [], False), ('2026-08-29', [], False),
    ('', RUNGS, False), ('2026-08-29', RUNGS, True),
])
def test_missing_fields_do_not_close_an_open_question(tmp_path, due, rungs, should_close):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='asset', kind='asset',
                      looks_at='Launch', question='Will it launch?', due_day=due, year='', rungs=rungs,
                      seq=1, input_id='news', created_at='2026-08-29T10:00:00')
    conn.commit()
    closed = pull.end_of_day(conn, '2026-08-29', 1)
    assert ('v1' in closed) == should_close
    assert store.is_open(conn, 'v1') != should_close


@pytest.mark.parametrize('previous,current', [([], RUNGS), (RUNGS, []), ([], [])])
def test_successor_with_missing_ladder_has_no_invented_orientation(previous, current):
    candidate = {'id': 'c1', 'rungs': current}
    assert writing.oriented_like(candidate, previous, [])['rungs'] == current
    if not current:
        assert matching.ladder_direction(current) is None


def test_only_questions_with_ladders_enter_judgement_even_when_date_is_unknown(tmp_path):
    from hivemind import model
    from hivemind.views import judging
    from test_theme_block import ASSET_RUNGS, DAY, V7, scripted
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    for view_id, rungs in [('v1', ASSET_RUNGS), ('v2', [])]:
        store.create_view(conn, view_id=view_id, object_id='NVDA', object_kind='company', kind='asset',
                          looks_at='Launch', question='Will it launch?', due_day='', year='', rungs=rungs,
                          seq=1, input_id='news', created_at='2026-07-29T10:00:00')
        eid = 'e' + view_id[1:]
        store.add_evidence(conn, evidence_id=eid, quote='The product is scheduled to launch.', one_line='A launch is scheduled.',
                           speaker='NVIDIA', original_who='NVIDIA', original_day='', tier='party_statement', event_time='', seq=1, input_id='news')
        store.add_source(conn, eid, 'news', 'T7', '2026-07-29', '', 1)
        store.link(conn, eid, view_id, 1)
    conn.commit()
    order = []
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    results = judging.round_of_judgements(archive, V7, conn, ['v1', 'v2'], 5, DAY, transport=scripted(order))
    assert order == ['v1']
    assert [r['view_id'] for r in results] == ['v1']
    assert conn.execute("select count(*) from judgements where view_id='v1'").fetchone()[0] == 1
    assert conn.execute("select count(*) from judgements where view_id='v2'").fetchone()[0] == 0


def test_analyst_check_day_does_not_close_an_unresolved_question(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='company', kind='asset',
                      looks_at='Launch', question='Will it launch?', due_day='2026-08-29', year='', rungs=RUNGS,
                      seq=1, input_id='news', created_at='2026-08-29T10:00:00')
    conn.commit()
    assert pull.end_of_day(conn, '2026-08-29', 1, unresolved_views=['v1']) == []
    assert store.is_open(conn, 'v1')
    assert pull.end_of_day(conn, '2026-08-29', 1) == ['v1']
