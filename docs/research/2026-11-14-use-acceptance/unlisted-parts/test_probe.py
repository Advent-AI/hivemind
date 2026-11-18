"""Tests of the probe's send guard and spending report (DESIGN.md, "Check before the send"): the send refuses a request that differs
from the checked record, completes and files each arm's outcomes when it matches, and stops on an attempt charged above its reserve.
Real stored cases, real Stage A runner and limit; only the transport is faked, so no paid call is made.

Run: python3 -m pytest docs/research/2026-11-14-use-acceptance/unlisted-parts/test_probe.py
"""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import probe  # noqa: E402

USAGE = {'prompt_tokens': 5000, 'completion_tokens': 1500}


@pytest.fixture(scope='module')
def checked(tmp_path_factory):
    """One $0 check, its record written to a temporary path."""
    record = tmp_path_factory.mktemp('record') / 'check-passed.json'
    original, probe.RECORD = probe.RECORD, record
    try:
        probe.check()
    finally:
        probe.RECORD = original
    return record


def stored_answers():
    """Each topic's stored final answer text, keyed by its thesis description (what the request carries)."""
    return {case['thesis']['description']: probe.stored_first(source, name)['requests'][-1]['answer_text']
            for _, source, name, case in probe.load_topics()}


def transport_with(usage):
    answers = stored_answers()

    def transport(provider, request):
        user = request['messages'][1]['content']
        text = next(answer for description, answer in answers.items() if json.dumps(description, ensure_ascii=False)[1:-1] in user)
        return {'choices': [{'message': {'content': text}}], 'usage': usage}
    return transport


def test_the_send_files_both_arms_when_every_request_matches_the_record(checked, tmp_path, monkeypatch):
    monkeypatch.setattr(probe, 'RECORD', checked)
    assert probe.send(tmp_path / 'run', transport=transport_with(USAGE)) == 0
    for arm in probe.ARMS:
        rows = [json.loads(line) for n in probe.PASSES for line in (tmp_path / 'run' / arm / f'send-{n}' / 'outcomes.jsonl').read_text().splitlines()]
        assert len(rows) == 18 * len(probe.PASSES)
        assert all(row['case'].startswith(f'{arm}|') for row in rows)
        assert len(json.loads((tmp_path / 'run' / arm / 'cases.json').read_text())) == 18


def test_a_case_changed_after_the_check_is_refused_before_any_send(checked, tmp_path, monkeypatch):
    monkeypatch.setattr(probe, 'RECORD', checked)
    original = probe.load_topics

    def changed_topics():
        topics = original()
        group, source, name, case = topics[0]
        case = dict(case, thesis=dict(case['thesis'], description=case['thesis']['description'] + ' (edited)'))
        return [(group, source, name, case)] + topics[1:]
    monkeypatch.setattr(probe, 'load_topics', changed_topics)
    sent = []
    with pytest.raises(SystemExit, match='REFUSED: the requests differ'):
        probe.send(tmp_path / 'run', transport=lambda provider, request: sent.append(request))
    assert sent == [] and not (tmp_path / 'run').exists()


def test_an_answer_costing_more_than_its_reserve_stops_every_later_attempt(checked, tmp_path, monkeypatch):
    monkeypatch.setattr(probe, 'RECORD', checked)
    # 25,000 output tokens cost about $0.013: above an attempt's reserve (16,000 tokens of output, about $0.0104 in all) and far
    # below the arm's $0.25 cap, so only the breach guard, not the cap, can stop the sends early (without it about 19 would go)
    answer, calls = transport_with({'prompt_tokens': 5000, 'completion_tokens': 25000}), []

    def counting(provider, request):
        calls.append(1)
        return answer(provider, request)
    with pytest.raises(SystemExit, match='control BREACH'):
        probe.send(tmp_path / 'run', transport=counting)
    assert len(calls) <= 8 and not (tmp_path / 'run' / 'changed').exists()      # at most the attempts already in flight
