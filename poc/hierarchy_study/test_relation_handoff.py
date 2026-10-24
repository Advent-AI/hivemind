"""D143 contract tests on real stored articles, real checks and temporary SQLite databases."""
import copy
import json
from pathlib import Path

import pytest

import ingestion_groups as base
import relation_handoff as handoff
import study
from hivemind import universe
from hivemind.views import matching, writing

SOURCE = study.ROOT / 'poc/reports/2026-10-24-ingestion-groups-01'


class StoredAnswers:
    """Adapt old answers for the new contract; this is code replay, never a fresh model sample."""
    def __init__(self, sample, alter=None):
        self.source = SOURCE / f'sample-{sample}-grouped'
        self.cfg = study.config.load(str(study.ROOT / 'poc/config/poc-v7.json'))
        self.count = 0
        self.alter = alter

    def stage(self, name, prompt, payload, schema, setting):
        self.count += 1
        answer = copy.deepcopy(json.loads((self.source / f'{name}.json').read_text())['answer'])
        if name.endswith('-extract'):
            hints = answer.pop('relationship_hints', [])
            answer['associations'] = []
            if name == 'item2-extract':
                for hint in hints:
                    candidate = next(c for c in answer['candidates'] if c['id'] == hint['candidate_id'])
                    answer['associations'].append({'group_id': '', 'question': hint['broader_question'],
                        'member_ids': [hint['candidate_id'], *hint['related_view_ids']],
                        'evidence_ids': candidate['evidence_ids'], 'reason': hint['reason']})
                if self.alter:
                    self.alter(answer)
        else:
            answer.pop('new_groups', None)
            answer.pop('memberships', None)
        return answer


def replay(path, sample, alter=None):
    items = json.loads((SOURCE / 'items.json').read_text())
    calls = StoredAnswers(sample, alter)
    conn = handoff.open_db(path)
    uni = universe.load(str(study.ROOT / 'poc/universe.json'))
    results = [handoff.process(conn, calls, uni, item, index) for index, item in enumerate(items, 1)]
    count = calls.count
    resend = handoff.process(conn, calls, uni, items[-1], 4)
    assert resend['route'] == 'skipped' and calls.count == count
    return conn, calls, results


@pytest.mark.parametrize('sample', [1, 2, 3])
def test_d143_stored_relations_form_real_shared_groups_and_survive_later_items(tmp_path, sample):
    """Acceptance: known 3/3 lost links now persist as shared groups without merging distinct questions."""
    conn, calls, results = replay(tmp_path / 'views.sqlite', sample)
    assert results[0]['groups'] == []
    second, third = results[1:]
    assert len(second['groups']) == 1
    gid = second['groups'][0]['group_id']
    assert second['affected_groups'] == [gid]
    members = {m['view_id'] for m in second['members'] if m['group_id'] == gid}
    assert len(members) == 2
    assert len({v['question'] for v in second['views'] if v['view_id'] in members}) == 2
    assert second['association_decisions'][0]['status'] == 'written'
    assert third['groups'] == second['groups']
    assert members == {m['view_id'] for m in third['members'] if m['group_id'] == gid}
    assert conn.execute('select count(*) from association_evidence').fetchone()[0] > 0
    assert conn.execute('pragma foreign_key_check').fetchall() == []
    conn.close()


def test_d143_merged_quote_id_keeps_accepted_relationship(tmp_path):
    """Review gap: original evidence ID -> surviving identical quote -> persistent evidence ID."""
    def duplicate(answer):
        association = answer['associations'][0]
        source = next(e for e in answer['evidence'] if e['id'] == association['evidence_ids'][0])
        answer['evidence'].append(dict(source, id='alias_evidence'))
        association['evidence_ids'] = ['alias_evidence']
    conn, _, results = replay(tmp_path / 'views.sqlite', 1, duplicate)
    decision = results[1]['association_decisions'][0]
    assert decision['status'] == 'written'
    assert all(conn.execute('select 1 from evidence where evidence_id=?', (e,)).fetchone() for e in decision['evidence_ids'])
    conn.close()


def test_d143_original_rejection_does_not_become_a_group(tmp_path):
    """New path cannot resurrect a quote the original sift rejected."""
    def invalid(answer):
        wanted = set(answer['associations'][0]['evidence_ids'])
        for evidence in answer['evidence']:
            if evidence['id'] in wanted:
                evidence['quote'] = 'This sentence is absent from the actual article.'
    conn, _, results = replay(tmp_path / 'views.sqlite', 1, invalid)
    assert results[1]['groups'] == []
    assert results[1]['association_decisions'][0]['status'] == 'skipped'
    conn.close()


def test_d143_unknown_reference_refuses_and_rolls_back_whole_write(tmp_path, monkeypatch):
    """Atomicity: a failure after group and thesis inserts leaves the previous committed state intact."""
    items = json.loads((SOURCE / 'items.json').read_text())
    calls = StoredAnswers(1)
    conn = handoff.open_db(tmp_path / 'views.sqlite')
    uni = universe.load(str(study.ROOT / 'poc/universe.json'))
    handoff.process(conn, calls, uni, items[0], 1)
    before = conn.execute('select count(*) from views').fetchone()[0]
    original = handoff.write_associations
    def fail(*args, **kwargs):
        original(*args, **kwargs)
        raise RuntimeError('Simulated failure after association writes')
    monkeypatch.setattr(handoff, 'write_associations', fail)
    with pytest.raises(RuntimeError), conn:
        handoff.process(conn, calls, uni, items[1], 2)
    assert conn.execute('select count(*) from views').fetchone()[0] == before
    assert conn.execute('select count(*) from associations').fetchone()[0] == 0
    assert conn.execute('select count(*) from research_groups').fetchone()[0] == 0
    monkeypatch.setattr(handoff, 'write_associations', original)
    calls.alter = lambda answer: answer['associations'][0]['member_ids'].append('v_unseen')
    with pytest.raises(ValueError, match='Invalid association references'), conn:
        handoff.process(conn, calls, uni, items[1], 2)
    assert conn.execute('select count(*) from views').fetchone()[0] == before
    conn.close()


def test_d143_identity_collapse_and_existing_membership(tmp_path):
    """Identity is resolved before cardinality; unchanged membership alone never dirties its group."""
    conn, _, results = replay(tmp_path / 'views.sqlite', 1)
    decision = results[1]['association_decisions'][0]
    members, sources = decision['members'], decision['evidence_ids']
    proposal = {'index': 0, 'skip_reason': '', 'group_id': '', 'question': 'Shared question?',
                'member_ids': ['c1', 'c2'], 'evidence_ids': ['e_alias'], 'reason': 'Supported relation.'}
    checked = matching.Checked({c: (matching.OUTCOMES[0], members[0], []) for c in ['c1', 'c2']}, {}, [], {})
    written = writing.Written(set(), {}, {'e_alias': sources[0]}, [])
    decisions, affected = handoff.write_associations(conn, [proposal], checked, written, 4, {'input_id': 'collapse'})
    assert decisions[0]['reason'] == 'fewer than two distinct resolved theses'
    assert affected == []
    proposal.update(group_id=decision['group_id'], question='', member_ids=members)
    decisions, affected = handoff.write_associations(conn, [proposal], checked, written, 4, {'input_id': 'same-members'})
    assert decisions[0]['status'] == 'written' and affected == []
    assert conn.execute('select count(*) from group_members').fetchone()[0] == 2
    conn.close()
