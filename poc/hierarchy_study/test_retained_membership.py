"""D147: unreferenced proposals do not invalidate valid research memberships."""
import json

import pytest

import retained_membership as retained
import ingestion_threads as legacy
import study
from test_extraction_membership import setup, Answers
from test_ingestion_threads import fixtures, thread
from hivemind import universe


def test_d147_same_raw_answer_writes_only_referenced_group(tmp_path):
    """Decisive case: unchanged q1 -> g1 is retained, unused t1 never becomes an empty group."""
    root = study.ROOT / 'poc/reports/2026-10-25-direct-subjects-01'
    raw = json.loads((root / 'sample-1-flat/item2-extract.json').read_text())['answer']
    items = json.loads((root / 'items.json').read_text())
    first = json.loads((root / 'sample-1-flat/item1-extract.json').read_text())['answer']
    calls = Answers([first, raw])
    conn = legacy.open_db(tmp_path / 'views.sqlite')
    uni = universe.load(str(study.ROOT / 'poc/universe.json'))
    retained.process(conn, calls, uni, items[0], 1)
    result = retained.process(conn, calls, uni, items[1], 2)
    assert len(result['threads']) == 1
    assert {m['view_id'] for m in result['memberships']} == {'v1', 'v2'}
    assert raw['threads'][0]['id'] == 't1' and raw['candidates'][0]['thread_ids'] == ['g1']
    conn.close()


@pytest.mark.parametrize('merge', [False, True])
def test_d147_preserves_original_checks_history_and_resend(tmp_path, merge):
    """State table: new versus existing thesis, evidence-only update, historical read and resend."""
    conn, calls, uni, items = setup(tmp_path / 'views.sqlite', merge=merge)
    calls.raw[0]['threads'].append(thread('t2', 'Unused proposed subject'))
    results = [retained.process(conn, calls, uni, item, i) for i, item in enumerate(items, 1)]
    assert len(results[-1]['threads']) == 1
    assert len(results[-1]['memberships']) == (1 if merge else 2)
    assert results[-1]['affected_threads'] == ['g1']
    assert len(legacy.thread_detail(conn, 'g1', 3)['members'][0]['evidence']) == (3 if merge else 2)
    assert ('item2-match-evidence' in calls.names) == merge
    before = len(calls.names)
    assert retained.process(conn, calls, uni, items[-1], 3)['route'] == 'skipped'
    assert len(calls.names) == before
    conn.close()


@pytest.mark.parametrize('bad_refs', [[], ['t1', 't1'], ['t1', 'g99'], ['t1', 't99']])
def test_d147_reference_rejections_still_apply(bad_refs):
    """Only unused declarations are allowed; empty, duplicate and unknown references remain invalid."""
    _, raw = fixtures()
    raw[0]['candidates'][0]['thread_ids'] = bad_refs
    with pytest.raises(ValueError):
        retained.validate_extraction(raw[0], [])


def test_d147_rollback_still_removes_all_partial_writes(tmp_path, monkeypatch):
    """Transaction row: allowing unused proposals never changes the atomic writer boundary."""
    conn, calls, uni, items = setup(tmp_path / 'views.sqlite')
    retained.process(conn, calls, uni, items[0], 1)
    original = legacy.write_threads
    def fail(*args):
        original(*args)
        raise RuntimeError('Failure after group write')
    monkeypatch.setattr(legacy, 'write_threads', fail)
    with pytest.raises(RuntimeError), conn:
        retained.process(conn, calls, uni, items[1], 2)
    assert conn.execute('select count(*) from views').fetchone()[0] == 1
    assert conn.execute('select count(*) from evidence').fetchone()[0] == 1
    conn.close()
