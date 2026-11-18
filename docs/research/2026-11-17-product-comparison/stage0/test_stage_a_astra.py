"""Tests of the astra entry for the answer-choice step (plan §1.5 D; D667 item 1). Each names the requirement it proves.
Real stage_a, real archive, real ladder step and limit; only the transport is faked. No credential is read (tests/conftest.py refuses one).

Run: python3 -m pytest docs/research/2026-11-17-product-comparison/stage0/test_stage_a_astra.py
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/lchingen/hivemind')
STEP = ROOT / 'clean-arch/step4-2026-11-10'
sys.path[:0] = [str(STEP / 'stage_a'), str(STEP / 'ladder'), str(ROOT / 'src'), str(ROOT / 'clean-arch/e2e-2026-11-09')]
WRAPPER = Path(os.environ.get('STAGE_A_ASTRA_UNDER_TEST', HERE / 'stage_a_astra.py'))    # a mutant copy is pointed at here


def load_wrapper():
    spec = importlib.util.spec_from_file_location('stage_a_astra_under_test', WRAPPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def astra(monkeypatch):
    """A fresh stage_a switched to astra; the shared modules it patches are restored after the test."""
    wrapper = load_wrapper()
    stage_a = wrapper.load_stage_a()
    monkeypatch.setattr(stage_a.model_calls, 'model_caller', stage_a.model_calls.model_caller)   # restored at teardown
    luna, setting = wrapper.install(stage_a)
    from hivemind import universe
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    cases = {case['case']: case for case in json.loads((STEP / 'stage_a' / 'cases.json').read_text())}
    return wrapper, stage_a, luna, setting, research_list, cases


def unreadable_transport(calls):
    """Answers every request with text that is not JSON, so the ladder step refuses the first answer and sends again with its note."""
    def transport(provider, request):
        calls.append(request)
        return {'choices': [{'message': {'content': 'not json'}}], 'usage': {'prompt_tokens': 1000, 'completion_tokens': 10}}
    return transport


def test_every_request_first_send_and_resend_reaches_the_transport_as_astra_and_checked(astra, tmp_path):
    """§1.5 D: every request, the resend with the refusal note included, is the checked astra request."""
    wrapper, stage_a, luna, setting, research_list, cases = astra
    calls = []
    written, limit, jobs = stage_a.run([cases['u1/clean-3']], [1], tmp_path / 'run', 20.00, research_list=research_list,
                                       texts=stage_a.request_texts(), transport=unreadable_transport(calls))
    assert not limit.stopped and len(written) == jobs == 1
    assert len(calls) == 2 and all(request['model'] == 'gpt-6-astra' for request in calls)
    assert calls[1]['messages'][1]['content'].startswith(calls[0]['messages'][1]['content'])
    assert len(calls[1]['messages'][1]['content']) > len(calls[0]['messages'][1]['content'])       # the refusal note
    for request in calls:                                    # each is the frozen luna request with only the model string changed
        luna_request = dict(request, model='gpt-6-luna')
        assert json.dumps(request) == json.dumps(luna_request).replace('"model": "gpt-6-luna"', '"model": "gpt-6-astra"')


def test_a_request_differing_beyond_the_model_is_refused_before_any_send(astra, tmp_path, monkeypatch):
    """§1.5 D: an astra request that is not the frozen request with only its model changed is never sent."""
    wrapper, stage_a, luna, setting, research_list, cases = astra
    original = stage_a.model.build_request

    def drifting(setting_given, *args):
        request = original(setting_given, *args)
        if setting_given.model == 'gpt-6-astra':
            request['temperature'] = 0
        return request
    monkeypatch.setattr(stage_a.model, 'build_request', drifting)
    calls = []
    written, limit, jobs = stage_a.run([cases['u1/clean-3']], [1], tmp_path / 'run', 20.00, research_list=research_list,
                                       texts=stage_a.request_texts(), transport=unreadable_transport(calls))
    assert calls == [] and limit.stopped and 'NotTheFrozenRequest' in limit.stop_reason


def test_a_request_altered_after_the_check_is_refused_at_the_transport(astra, tmp_path):
    """§1.5 D: the request reaching the transport must be the one checked; another is refused before its reservation."""
    wrapper, stage_a, luna, setting, research_list, cases = astra
    limit = stage_a.StageALimit(1.00, tmp_path / 'spend.jsonl', attempt=lambda provider, request: pytest.fail('sent'))
    request = stage_a.model.build_request(setting, 'system', 'user', stage_a.request_texts()['schema'], 'clean_ladder', 'openai')
    with pytest.raises(wrapper.NotTheFrozenRequest):
        limit.send_labelled('case|1|1', 'openai', request)
    assert not (tmp_path / 'spend.jsonl').exists()            # no reservation was written


def test_the_archive_carries_the_astra_configuration_checksum_not_the_frozen_luna_one(astra, tmp_path):
    """§1.5 D: run_fresh checks every pass's archive against the astra checksum; it differs from the frozen luna configuration."""
    wrapper, stage_a, luna, setting, research_list, cases = astra
    calls = []
    stage_a.run([cases['u1/clean-3']], [1, 2], tmp_path / 'run', 20.00, research_list=research_list, texts=stage_a.request_texts(),
                transport=unreadable_transport(calls))
    import sqlite3
    found = set()
    for pass_number in (1, 2):
        conn = sqlite3.connect(tmp_path / 'run' / f'send-{pass_number}' / 'archive.sqlite')
        found |= set(conn.execute('select distinct config_version, config_checksum from model_calls').fetchall())
    assert found == {('clean-ladder-stage-a', wrapper.configuration_checksum(stage_a))}
    assert wrapper.configuration_checksum(stage_a) != 'd3b4a5f696c7cc82'
