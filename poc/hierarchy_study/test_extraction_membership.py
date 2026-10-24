"""D147: extraction owns memberships; the ordinary matcher never decides them."""
import copy
import json

import pytest

import extraction_membership as membership
import ingestion_threads as legacy
import study
from test_ingestion_threads import fixtures, thread
from hivemind import universe


class Answers:
    """Only the external model is replaced; the sources, search and database are real."""
    def __init__(self, raw, merge=False):
        self.raw, self.merge, self.names = raw, merge, []
        self.cfg = study.config.load(str(study.ROOT / 'poc/config/poc-v7.json'))

    def stage(self, name, prompt, payload, schema, setting):
        self.names.append(name)
        index = int(name[4]) - 1
        if name.endswith('extract'):
            if index == 1:
                assert 'g1' in {g['thread_id'] for g in payload['existing_subjects']}
            return copy.deepcopy(self.raw[index])
        assert not any('thread_ids' in c for c in payload['candidates'])
        assert set(schema['properties']) == {'candidates', 'evidence'}
        return {'candidates': [
            {'id': c['id'], 'outcome': 'existing' if self.merge and index == 1 else 'new',
             'target_view_id': 'v1' if self.merge and index == 1 else '',
             'reason': 'A distinct measured question.', 'dependencies': []}
            for c in payload['candidates']],
            'evidence': [{'id': pair['evidence_id'], 'view_id': pair['view_id'], 'outcome': 'new',
                          'target_evidence_id': '', 'said_day': '', 'reason': 'New source statement.'}
                         for pair in payload['evidence_pairs']]}


def setup(path, merge=False):
    items, raw = fixtures()
    raw[1]['threads'] = []
    raw[1]['candidates'][0]['thread_ids'] = ['g1']
    return legacy.open_db(path), Answers(raw, merge), universe.load(str(study.ROOT / 'poc/universe.json')), items


def test_d147_membership_survives_thesis_matching_and_later_risk(tmp_path):
    """State rows: empty library, later milestone, evidence-only update, historical read and resend."""
    conn, calls, uni, items = setup(tmp_path / 'views.sqlite')
    results = [membership.process(conn, calls, uni, item, i) for i, item in enumerate(items, 1)]
    assert len(results[-1]['threads']) == 1
    assert {m['view_id'] for m in results[-1]['memberships']} == {'v1', 'v2'}
    assert results[-1]['affected_threads'] == ['g1']
    assert [len(m['evidence']) for m in legacy.thread_detail(conn, 'g1', 2)['members']] == [1, 1]
    assert [len(m['evidence']) for m in legacy.thread_detail(conn, 'g1', 3)['members']] == [2, 1]
    assert membership.process(conn, calls, uni, items[-1], 3)['route'] == 'skipped'
    assert len(calls.names) == 6
    conn.close()


@pytest.mark.parametrize('breach', ['missing', 'empty', 'unknown_local', 'unknown_stored', 'duplicate', 'unused'])
def test_d147_references_are_closed(breach):
    """Closed-set row: each candidate references only declared locals or displayed stored subjects."""
    _, raw = fixtures()
    answer = raw[0]
    refs = answer['candidates'][0]
    if breach == 'missing': del refs['thread_ids']
    if breach == 'empty': refs['thread_ids'] = []
    if breach == 'unknown_local': refs['thread_ids'] += ['t9']
    if breach == 'unknown_stored': refs['thread_ids'] += ['g9']
    if breach == 'duplicate': refs['thread_ids'] += ['t1']
    if breach == 'unused': answer['threads'] += [thread('t2')]
    with pytest.raises(ValueError):
        membership.validate_extraction(answer, [{'thread_id': 'g1'}])


def test_d147_thesis_can_belong_to_old_and_new_subjects(tmp_path):
    """Multiple scopes row: preserve both explicit memberships without collapsing their subjects."""
    conn, calls, uni, items = setup(tmp_path / 'views.sqlite')
    membership.process(conn, calls, uni, items[0], 1)
    calls.raw[1]['threads'] = [thread('t1', 'SK Telecom AI factory deployment')]
    calls.raw[1]['candidates'][0]['thread_ids'].append('t1')
    result = membership.process(conn, calls, uni, items[1], 2)
    assert {(m['thread_id'], m['view_id']) for m in result['memberships']} == {('g1', 'v1'), ('g1', 'v2'), ('g2', 'v2')}
    conn.close()


def test_d147_merged_candidate_keeps_original_evidence_pass(tmp_path):
    """Old-check row: the original second evidence pass still runs after a thesis merge."""
    conn, calls, uni, items = setup(tmp_path / 'views.sqlite', merge=True)
    membership.process(conn, calls, uni, items[0], 1)
    result = membership.process(conn, calls, uni, items[1], 2)
    assert calls.names[-1] == 'item2-match-evidence'
    assert result['new_views'] == {} and len(result['memberships']) == 1
    assert len(result['details'][0]['members'][0]['evidence']) == 2
    conn.close()


def test_d147_source_refusal_does_not_create_empty_subject(tmp_path):
    """Pruning row: membership never revives a candidate whose source failed."""
    conn, calls, uni, items = setup(tmp_path / 'views.sqlite')
    calls.raw[0]['evidence'][0]['quote'] = 'This is absent from the article.'
    result = membership.process(conn, calls, uni, items[0], 1)
    assert result['views'] == [] and result['threads'] == []
    conn.close()


def test_d147_rollback_includes_original_thesis_writes(tmp_path, monkeypatch):
    """Failure row: no partial thesis, evidence or membership survives a failed group write."""
    conn, calls, uni, items = setup(tmp_path / 'views.sqlite')
    membership.process(conn, calls, uni, items[0], 1)
    original = legacy.write_threads
    def fail(*args):
        original(*args)
        raise RuntimeError('Failure after membership write')
    monkeypatch.setattr(legacy, 'write_threads', fail)
    with pytest.raises(RuntimeError), conn:
        membership.process(conn, calls, uni, items[1], 2)
    assert conn.execute('select count(*) from views').fetchone()[0] == 1
    assert conn.execute('select count(*) from evidence').fetchone()[0] == 1
    assert conn.execute('select count(*) from thread_members').fetchone()[0] == 1
    conn.close()


@pytest.mark.parametrize('sample, target', [(2, 'g3'), (3, 'g1')])
def test_d147_real_split_can_be_written_as_direct_extraction_membership(tmp_path, sample, target):
    """Cheapest proof: only the stored membership is changed; all real thesis/evidence answers remain."""
    root = study.ROOT / 'poc/reports/2026-10-25-direct-subjects-01'
    folder = root / f'sample-{sample}-threads'
    class Saved:
        cfg = study.config.load(str(study.ROOT / 'poc/config/poc-v7.json'))
        def stage(self, name, prompt, payload, schema, setting):
            answer = json.loads((folder / (name + '.json')).read_text())['answer']
            if name == 'item2-extract':
                assert target in {g['thread_id'] for g in payload['existing_subjects']}
                answer['threads'] = []
                answer['candidates'][0]['thread_ids'] = [target]
            answer.pop('subject_groups', None)
            return answer
    items = json.loads((root / 'items.json').read_text())
    conn = legacy.open_db(tmp_path / 'views.sqlite')
    uni = universe.load(str(study.ROOT / 'poc/universe.json'))
    for i, item in enumerate(items[:2], 1):
        membership.process(conn, Saved(), uni, item, i)
    assert len(legacy.thread_detail(conn, target, 2)['members']) == 2
    conn.close()
