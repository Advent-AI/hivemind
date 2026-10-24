"""D146's direct identity contract, real article fixtures, and real storage."""
import copy
import json

import pytest

import direct_subjects as direct
import ingestion_threads as legacy
import study
from test_ingestion_threads import fixtures, thread
from hivemind import universe


class Answers:
    """Only the external model is replaced; all filtering, search and writes are real."""
    def __init__(self, raw, merge=False):
        self.raw, self.merge, self.names = raw, merge, []
        self.cfg = study.config.load(str(study.ROOT / 'poc/config/poc-v7.json'))

    def stage(self, name, prompt, payload, schema, setting):
        self.names.append(name)
        index = int(name[4]) - 1
        if name.endswith('extract'):
            return copy.deepcopy(self.raw[index])
        result = {'candidates': [], 'evidence': [
            {'id': pair['evidence_id'], 'view_id': pair['view_id'], 'outcome': 'new',
             'target_evidence_id': '', 'said_day': '', 'reason': 'A distinct statement.'}
            for pair in payload['evidence_pairs']]}
        if name.endswith('match-evidence'):
            return result
        for candidate in payload['candidates']:
            assert 'thread_ids' not in candidate
            merge = self.merge and index == 1
            result['candidates'].append({'id': candidate['id'], 'outcome': 'existing' if merge else 'new',
                'target_view_id': 'v1' if merge else '', 'reason': 'A measured test decision.', 'dependencies': []})
        identity = payload['subject_identity']
        if index == 1 and identity['local_descriptions']:
            assert 'g1' in identity['eligible_stored_ids']['t1']
        result['subject_groups'] = [{'local_ids': [subject['id']], 'destination': 'new' if index == 0 else 'g1',
                                     'reason': 'The same continuing product rollout.'}
                                    for subject in identity['local_descriptions']]
        assert study.model.check_schema(result, schema) == []
        return result


def setup(path, merge=False):
    items, raw = fixtures()
    return legacy.open_db(path), Answers(raw, merge), universe.load(str(study.ROOT / 'poc/universe.json')), items


def test_d146_three_articles_preserve_separate_theses_one_subject_and_risk(tmp_path):
    """State rows: initial identity, later milestone, evidence-only update and idempotent resend."""
    conn, calls, uni, items = setup(tmp_path / 'views.sqlite')
    events = [direct.process(conn, calls, uni, item, index) for index, item in enumerate(items, 1)]
    assert len(events[-1]['threads']) == 1
    assert {m['view_id'] for m in events[-1]['memberships']} == {'v1', 'v2'}
    assert events[-1]['affected_threads'] == ['g1']
    assert [len(m['evidence']) for m in legacy.thread_detail(conn, 'g1', 3)['members']] == [2, 1]
    before = list(calls.names)
    assert direct.process(conn, calls, uni, items[-1], 3)['route'] == 'skipped'
    assert calls.names == before and len(before) == 6
    conn.close()


def test_d146_merged_candidate_runs_original_second_evidence_pass(tmp_path):
    """Old-check table: resolving a candidate to an old thesis must still compare its evidence."""
    conn, calls, uni, items = setup(tmp_path / 'views.sqlite', merge=True)
    direct.process(conn, calls, uni, items[0], 1)
    result = direct.process(conn, calls, uni, items[1], 2)
    assert calls.names[-1] == 'item2-match-evidence'
    assert result['new_views'] == {} and len(result['memberships']) == 1
    assert [e['evidence_id'] for e in result['details'][0]['members'][0]['evidence']] == ['e1', 'e2']
    conn.close()


def test_d146_local_descriptions_consolidate_without_a_pointer_graph():
    """Same-batch row: order of returned local IDs cannot change the canonical new description."""
    subjects = [thread('t1'), thread('t2')]
    candidates = {'t1': [{'thread_id': 'g8'}], 't2': [{'thread_id': 'g8'}]}
    answer = {'candidates': [], 'evidence': [], 'subject_groups': [
        {'local_ids': ['t2', 't1'], 'destination': 'new', 'reason': 'The same product rollout.'}]}
    assert direct.resolve_groups(answer, subjects, candidates) == {'t1': 't1', 't2': 't1'}
    answer['subject_groups'][0]['destination'] = 'g8'
    assert direct.resolve_groups(answer, subjects, candidates) == {'t1': 'g8', 't2': 'g8'}
    candidates['t2'] = []
    with pytest.raises(ValueError, match='every local member'):
        direct.resolve_groups(answer, subjects, candidates)


@pytest.mark.parametrize('breach', ['self', 'unseen', 'duplicate', 'missing', 'empty'])
def test_d146_closed_destination_and_partition(breach):
    """Closed-set row: a model cannot send a temporary ID as destination or silently omit a subject."""
    answer = {'candidates': [], 'evidence': [], 'subject_groups': [
        {'local_ids': ['t1'], 'destination': 'new', 'reason': 'Product rollout.'}]}
    group = answer['subject_groups'][0]
    if breach == 'self': group['destination'] = 't1'
    if breach == 'unseen': group['destination'] = 'g9'
    if breach == 'duplicate': group['local_ids'] = ['t1', 't1']
    if breach == 'missing': answer['subject_groups'] = []
    if breach == 'empty': group['local_ids'] = []
    with pytest.raises(ValueError):
        direct.resolve_groups(answer, [thread()], {'t1': []})


@pytest.mark.parametrize('sample', [1, 3])
def test_d146_real_self_target_failures_are_expressible_without_changing_business_content(tmp_path, sample):
    """Decisive $0 proof: the two stored D144 failures can write with only the identity representation changed."""
    source = study.ROOT / 'poc/reports/2026-10-25-ingestion-threads-01'
    item = json.loads((source / 'items.json').read_text())[0]
    class Stored:
        cfg = study.config.load(str(study.ROOT / 'poc/config/poc-v7.json'))
        def stage(self, name, prompt, payload, schema, setting):
            answer = json.loads((source / f'sample-{sample}-threads' / (name + '.json')).read_text())['answer']
            if 'thread_matches' in answer:
                old = answer.pop('thread_matches')
                assert all(row['id'] == row['target_thread_id'] for row in old)
                answer['subject_groups'] = [{'local_ids': [row['id']], 'destination': 'new', 'reason': row['reason']} for row in old]
            return answer
    conn = legacy.open_db(tmp_path / 'views.sqlite')
    result = direct.process(conn, Stored(), universe.load(str(study.ROOT / 'poc/universe.json')), item, 1)
    assert len(result['views']) == len(result['threads']) == len(result['memberships']) == 3
    conn.close()


def test_d146_rejected_sources_do_not_create_subjects(tmp_path):
    """Original checks: subject identity cannot revive a candidate whose evidence was rejected."""
    conn, calls, uni, items = setup(tmp_path / 'views.sqlite')
    calls.raw[0]['evidence'][0]['quote'] = 'This sentence is absent from the source article.'
    result = direct.process(conn, calls, uni, items[0], 1)
    assert result['views'] == [] and result['threads'] == []
    conn.close()


def test_d146_subject_failure_rolls_back_theses_and_evidence(tmp_path, monkeypatch):
    """Transaction row: a failure after original thesis/evidence writes leaves no partial new article."""
    conn, calls, uni, items = setup(tmp_path / 'views.sqlite')
    direct.process(conn, calls, uni, items[0], 1)
    original = legacy.write_threads
    def fail(*args, **kwargs):
        original(*args, **kwargs)
        raise RuntimeError('Failure after subject write')
    monkeypatch.setattr(legacy, 'write_threads', fail)
    with pytest.raises(RuntimeError), conn:
        direct.process(conn, calls, uni, items[1], 2)
    assert conn.execute('select count(*) from views').fetchone()[0] == 1
    assert conn.execute('select count(*) from evidence').fetchone()[0] == 1
    assert conn.execute('select count(*) from thread_members').fetchone()[0] == 1
    conn.close()
