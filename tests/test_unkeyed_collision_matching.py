"""D248/D258: the existing judge resolves unkeyed proposed merges before writing."""
import json
import sys
from pathlib import Path

import pytest

from test_collision_judge import JEV_ONLY
from test_jev_matching import ITEM, UNIVERSE, ledger_with_view, piece, scripted

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, extraction, model  # noqa: E402
from hivemind.views import jev_matching, matching, store, writing  # noqa: E402

CFG = config.load(str(ROOT / 'poc/config/poc-v118-matching-identity.json'))


def unkeyed():
    return {'id': 'c1', 'kind': 'asset', 'object': 'NVDA', 'looks_at': 'FY2028 total revenue',
            'question': 'What total revenue will NVIDIA report for FY2028?', 'year': '2028', 'due_day': '',
            'rungs': [], 'evidence_ids': ['x1'], 'group_refs': []}


def judge(relations):
    def transport(provider, request):
        assert request['response_format']['json_schema']['name'] == 'collision'
        body = {'relations': [{'thesis_id': vid, 'relation': relation, 'why': 'reviewed'} for vid, relation in relations]}
        return {'choices': [{'message': {'content': json.dumps(body)}}]}
    return transport


@pytest.mark.parametrize('relation,expected', [
    ('different', 'new'), ('distinct_question_same_matter', 'new'),
    ('same_question_other_period', 'new'), ('same_question', 'merge'),
])
@pytest.mark.parametrize('jev_relation', ['part_of', 'same_quantity_or_event'])
def test_the_judge_resolves_unkeyed_proposed_merge_without_requiring_date_or_ladder(tmp_path, relation, expected, jev_relation):
    conn, _ = ledger_with_view(tmp_path)
    c = unkeyed()
    lists = matching.Lists({'c1': ['v1']}, {})
    result = jev_matching.decide(model.Archive(str(tmp_path / 'archive.sqlite')), CFG, conn, ITEM, [c], [], lists, [],
                                 transport=scripted({'rel__v1': (jev_relation, 0.88)}), llm_transport=judge([('v1', relation)]))
    checked = matching.check(conn, UNIVERSE, result.data, [c], [], lists, [])
    assert checked.refusals == [] and checked.outcomes['c1'][0] == expected


def test_review_tries_the_other_proposed_home_before_opening_a_duplicate(tmp_path):
    conn, _ = ledger_with_view(tmp_path)
    store.create_view(conn, view_id='v2', object_id='NVDA', object_kind='asset', kind='asset', looks_at='FY2028 total revenue',
                      question='What is NVIDIA total revenue in FY2028?', due_day='', year='2028', rungs=[],
                      seq=2, input_id='prior', created_at='2026-08-28T00:00:00')
    conn.commit()
    c = unkeyed()
    lists = matching.Lists({'c1': ['v1', 'v2']}, {})
    result = jev_matching.decide(model.Archive(str(tmp_path / 'archive.sqlite')), CFG, conn, ITEM, [c], [], lists, [],
                                 transport=scripted({'rel__v1': ('part_of', 0.9), 'rel__v2': ('part_of', 0.8)}),
                                 llm_transport=judge([('v1', 'different'), ('v2', 'same_question')]))
    assert (result.data['candidates'][0]['outcome'], result.data['candidates'][0]['target_view_id']) == ('merge', 'v2')


@pytest.mark.parametrize('relations', [[], [('v1', 'same_question'), ('v1', 'same_question')], [('v9', 'same_question')]])
def test_incomplete_or_duplicate_judge_answers_do_not_write_a_decision(tmp_path, relations):
    conn, _ = ledger_with_view(tmp_path)
    lists = matching.Lists({'c1': ['v1']}, {})
    with pytest.raises(ValueError, match='exactly once'):
        jev_matching.decide(model.Archive(str(tmp_path / 'archive.sqlite')), CFG, conn, ITEM, [unkeyed()], [], lists, [],
                            transport=scripted({'rel__v1': ('part_of', 0.88)}), llm_transport=judge(relations))
    assert conn.execute('select count(*) from views').fetchone()[0] == 1


def test_distinct_question_and_evidence_are_written_and_visible_to_the_next_item(tmp_path):
    conn, _ = ledger_with_view(tmp_path)
    c = unkeyed()
    e = piece('x1', 'Management expects revenue to rise in the next fiscal year.', ['c1'])
    handover = extraction.Handover([e], [c], [], 0, '', False, 0.0)
    lists = matching.Lists({'c1': ['v1']}, {})
    answer = jev_matching.decide(model.Archive(str(tmp_path / 'archive.sqlite')), CFG, conn, ITEM, [c], [e], lists, [],
                                 transport=scripted({'rel__v1': ('part_of', 0.88)}), llm_transport=judge([('v1', 'different')]))
    checked = matching.check(conn, UNIVERSE, answer.data, [c], [e], lists, [])
    assert not checked.refusals
    written = writing.write(conn, UNIVERSE, 2, dict(ITEM, input_id='later'), handover, checked, {})
    conn.commit()
    assert 'c1' in written.new_views
    new_id = written.new_views['c1']
    assert store.view(conn, new_id)['question'] == c['question']
    assert [x['quote'] for x in store.evidence_in_force(conn, new_id)] == [e['quote']]
    assert new_id in {x['view_id'] for x in store.views_for_prompt(conn, ['NVDA'])}


def test_configuration_without_collision_keeps_existing_behavior(tmp_path):
    conn, _ = ledger_with_view(tmp_path)
    result = jev_matching.decide(model.Archive(str(tmp_path / 'archive.sqlite')), JEV_ONLY, conn, ITEM, [unkeyed()], [],
                                 matching.Lists({'c1': ['v1']}, {}), [], transport=scripted({'rel__v1': ('part_of', 0.88)}))
    assert result.data['candidates'][0]['outcome'] == 'merge'
