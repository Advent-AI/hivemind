"""D190: when a candidate's list holds an open thesis of the same object and measure (a collision), the generative model answers the
analyst's question (collision-v1) and its verdict on those theses replaces Jev's, which reads wording and calls a population variant
'part of'. Without a collision setting the Jev verdict stands. Real ledger on a temporary path; scripted Jev and model transports."""
import json
import os
import sys

from test_jev_matching import ITEM, UNIVERSE, candidate, ledger_with_view, scripted

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, model  # noqa: E402
from hivemind.views import jev_matching, matching  # noqa: E402

CFG = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v26.json'))
JEV_ONLY = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v25.json'))


def llm(relation):
    def transport(provider, request):
        assert request['response_format']['json_schema']['name'] == 'collision'
        return {'choices': [{'message': {'content': json.dumps({'relations': [{'thesis_id': 'v1', 'relation': relation, 'why': 'scripted'}]})}}]}
    return transport


def run(tmp_path, cfg, relation):
    conn, _ = ledger_with_view(tmp_path)
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    c = candidate('c1', looks_at='Compute & Networking annual revenue', question='Compute & Networking revenue in FY2027?', scope='Compute & Networking')
    handover = type('H', (), {'candidates': [c], 'evidence': [], 'dropped': [], 'new_groups': []})()
    lists = matching.build_lists(conn, handover, [], cfg.search_top_n)
    answer = jev_matching.decide(archive, cfg, conn, ITEM, [c], [], lists, [], transport=scripted({'rel__v1': ('part_of', 0.62)}), llm_transport=llm(relation))
    return answer.data['candidates'][0]


def test_config_v26_carries_the_collision_setting():
    assert CFG.collision.prompt_version == 'collision-v1' and CFG.collision.model == 'gpt-6-luna' and JEV_ONLY.collision is None


def test_the_judge_merges_a_population_variant_jev_called_part_of(tmp_path):
    decision = run(tmp_path, CFG, 'same_question')
    assert (decision['outcome'], decision['target_view_id']) == ('merge', 'v1') and 'collision' in decision['reason']


def test_the_judge_keeps_a_distinct_component_apart(tmp_path):
    decision = run(tmp_path, CFG, 'distinct_question_same_matter')
    assert (decision['outcome'], decision['target_view_id']) == ('new', '')


def test_without_a_collision_setting_jev_decides_alone(tmp_path):
    decision = run(tmp_path, JEV_ONLY, 'same_question')
    assert decision['outcome'] == 'new' and 'collision' not in decision['reason']
