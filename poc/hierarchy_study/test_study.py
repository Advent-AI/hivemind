"""Contract checks over the actual read-only NVIDIA snapshot; no model calls."""
import copy
from pathlib import Path
import sqlite3

import pytest
import study
import argument_first
import revisit

SOURCE = study.ROOT / 'poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite'


def records():
    conn = study.read_only(SOURCE)
    ids = {row[0] for row in conn.execute("select view_id from views where object_id='NVDA'")}
    result = study.snapshot(conn, ids, 584)
    conn.close()
    return result


def test_snapshot_uses_only_known_judgements_and_citations():
    conn = study.read_only(SOURCE)
    early = study.snapshot(conn, {'v3', 'v7'}, 6)
    assert len(early['theses']) == 2
    for thesis in early['theses']:
        expected = conn.execute('select max(seq) from judgements where view_id=? and seq<=6', (thesis['id'],)).fetchone()[0]
        assert (thesis['assessment']['seq'] if thesis['assessment'] else None) == expected
        assert all(piece['created_seq'] <= 6 for piece in thesis['evidence'])
    assert conn.execute("select max(seq) from judgements where view_id='v3'").fetchone()[0] > 6
    conn.close()


def test_partition_covers_real_ids_once_and_refuses_duplicates_or_invention():
    ids = [thesis['id'] for thesis in records()['theses']]
    value = {'groups': [{'id': 'g1', 'title': 'Research', 'scope': 'Actual stored questions', 'members': ids}], 'unassigned': []}
    assert study.check_partition(value, ids) is value
    invalid = copy.deepcopy(value)
    invalid['unassigned'].append(ids[0])
    with pytest.raises(ValueError, match='exactly once'):
        study.check_partition(invalid, ids)
    invalid = copy.deepcopy(value)
    invalid['groups'][0]['members'][0] = 'invented'
    with pytest.raises(ValueError, match='exactly once'):
        study.check_partition(invalid, ids)


def test_main_thesis_needs_real_input_references_and_its_own_group():
    snap = records()
    ids = [thesis['id'] for thesis in snap['theses']]
    partition = {'groups': [{'id': 'g1', 'title': 'Research', 'scope': 'Example', 'members': ids[:1]}], 'unassigned': ids[1:]}
    value = {'heads': [{'group_id': 'g1', 'title': 'Research', 'status': 'main_thesis', 'thesis': 'A bounded operating thesis', 'claims': [{'text': snap['theses'][0]['question'], 'relation': 'context', 'view_ids': ids[:1]}], 'limitations': [], 'watch_questions': []}], 'ungrouped_note': ''}
    assert study.check_heads(value, partition, snap) is value
    invalid = copy.deepcopy(value)
    invalid['heads'][0]['claims'][0]['view_ids'] = ['invented']
    with pytest.raises(ValueError, match='real snapshot citations'):
        study.check_heads(invalid, partition, snap)
    invalid = copy.deepcopy(value)
    invalid['heads'][0]['claims'][0]['view_ids'] = ids[1:2]
    with pytest.raises(ValueError, match='own group'):
        study.check_heads(invalid, partition, snap)


def test_invalid_agent_answer_is_recorded_without_resampling_other_steps():
    snap = records()
    heads = [{'group_id': 'main_1'}]
    answers = [{'question_id': q['id'], 'answer': 'Stored answer', 'main_ids': ['main_1'], 'drill_down_ids': [snap['theses'][0]['id']], 'limitations': []} for q in study.QUESTIONS]
    assert study.probe_errors({'answers': answers}, heads, snap) == []
    answers[0]['main_ids'] = ['invented_main']
    errors = study.probe_errors({'answers': answers}, heads, snap)
    assert len(errors) == 1 and 'invented_main' in errors[0]


def test_argument_map_can_share_a_real_leaf_and_derives_unused_ids_in_code():
    snap = records()
    ident = snap['theses'][0]['id']
    head = {'group_id': 'main1', 'title': 'Business judgement', 'status': 'main_thesis', 'thesis': 'A bounded argument', 'claims': [{'text': snap['theses'][0]['question'], 'relation': 'context', 'view_ids': [ident]}], 'limitations': [], 'watch_questions': []}
    second = dict(head, group_id='main2')
    result = argument_first.validate({'heads': [head, second]}, snap)
    assert len(result['unused_ids']) == len(snap['theses']) - 1
    invalid = copy.deepcopy(head)
    invalid['claims'][0]['view_ids'] = ['invented']
    with pytest.raises(ValueError, match='true snapshot references'):
        argument_first.validate({'heads': [invalid]}, snap)


def test_revisit_changes_only_unassigned_membership():
    ids = [thesis['id'] for thesis in records()['theses']]
    old = {'groups': [{'id': 'g1', 'title': 'Business', 'scope': 'Existing scope', 'members': ids[:1]}], 'unassigned': ids[1:]}
    update = {'new_groups': [], 'assignments': [{'view_id': ids[1], 'group_id': 'g1'}], 'unassigned': ids[2:]}
    result = revisit.apply_update(old, update, ids)
    assert result['groups'][0]['members'] == ids[:2]
    assert old['groups'][0]['members'] == ids[:1]
    invalid = copy.deepcopy(update)
    invalid['assignments'][0]['view_id'] = ids[0]
    with pytest.raises(ValueError, match='previously unassigned'):
        revisit.apply_update(old, invalid, ids)
