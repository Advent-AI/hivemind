"""D148 input visibility and isolated experiment bounds on real stored records."""
import copy
import json

import pytest

import grouping_consistency as diagnostic
import ingestion_threads as threads
import retained_membership as retained
import study
from hivemind import universe

SOURCE = study.ROOT / 'poc/reports/2026-10-25-direct-subjects-01'


def test_d148_visible_memberships_follow_the_stored_prefix(tmp_path):
    """Value/reader row: add real displayed memberships without changing the old payload."""
    out = tmp_path / 'experiment'
    diagnostic.prepare(out, SOURCE)
    conn = threads.open_db(out / 'prefix.sqlite')
    calls = diagnostic.Calls(out, '1-control', conn, SOURCE / 'sample-2-retained')
    uni = universe.load(str(study.ROOT / 'poc/universe.json'))
    for i, item in enumerate(json.loads((out / 'items.json').read_text())[:2], 1):
        retained.process(conn, calls, uni, item, i)
    record = json.loads((SOURCE / 'sample-2-retained/item3-extract.json').read_text())
    payload = json.loads(record['request']['messages'][1]['content'])
    original = copy.deepcopy(payload)
    enriched = diagnostic.membership_context(conn, payload)
    assert [t.get('thread_ids') for t in enriched['existing_theses']] == [['g1'], ['g1', 'g2']]
    assert payload == original
    payload['existing_subjects'] = [g for g in payload['existing_subjects'] if g['thread_id'] == 'g1']
    assert [t['thread_ids'] for t in diagnostic.membership_context(conn, payload)['existing_theses']] == [['g1'], ['g1']]
    assert json.loads((out / 'budget.json').read_text())['attempts'] == []
    calls.archive.conn.close()
    conn.close()


@pytest.mark.parametrize('budget', [
    {'attempts': [{}] * 18, 'estimated_spent': 0},
    {'attempts': [], 'estimated_spent': 2},
])
def test_d148_own_cap_stops_before_external_service(tmp_path, monkeypatch, budget):
    """Budget row: both the request and money bounds refuse before the model is invoked."""
    out = tmp_path / 'experiment'
    diagnostic.prepare(out, SOURCE)
    study.write_json(out / 'budget.json', budget)
    conn = threads.open_db(out / 'prefix.sqlite')
    calls = diagnostic.Calls(out, '1-control', conn, SOURCE / 'sample-2-retained')
    def external_service(*args, **kwargs):
        raise AssertionError('External service was reached')
    monkeypatch.setattr(study.model, 'call', external_service)
    with pytest.raises(diagnostic.BudgetReached):
        calls.stage('item3-extract', 'Unchanged test prompt', {}, study.obj({}), calls.cfg.matching)
    assert json.loads((out / 'budget.json').read_text()) == budget
    calls.archive.conn.close()
    conn.close()
