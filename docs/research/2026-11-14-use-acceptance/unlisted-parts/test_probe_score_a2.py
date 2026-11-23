"""Tests of DESIGN-A2.md v2's added rules ($0): the refusal controls must stay declined where the same-day control declines them; the
recovery topics must gain at least three correct written answers over the control; either condition unexercised is inconclusive; and the
whole A2 pipeline (check, fake-transport send, reading folder, packets, made-up readings, score) runs on its 28 topics.

Run: python3 -m pytest docs/research/2026-11-14-use-acceptance/unlisted-parts/test_probe_score_a2.py
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
import probe  # noqa: E402
import probe_score  # noqa: E402
import reading_prep  # noqa: E402
import test_probe  # noqa: E402
import test_probe_score  # noqa: E402


@pytest.fixture
def a2():
    probe.configure('a2')
    yield
    probe.configure('a')


def topics(group):
    return [f'{source}:{name}' for source, name in probe.TOPICS[group]]


def base_sends(control_l_topics=4):
    """Every send of both arms passes, except: the control fails L on the first motivating topics; both arms decline every refusal
    control; the control declines every recovery topic and the changed request writes each correctly."""
    by_send = {}
    for arm in probe.ARMS:
        for group, entries in probe.TOPICS.items():
            for source, name in entries:
                for n in (1, 2, 3):
                    by_send[(arm, f'{source}:{name}', n)] = set()
    for topic in topics('motivating')[:control_l_topics]:
        by_send[('control', topic, 1)] = {'L'}
    for topic in topics('refusal control'):
        for arm in probe.ARMS:
            for n in (1, 2, 3):
                by_send[(arm, topic, n)] = {'refusal'}
    for topic in topics('recovery'):
        for n in (1, 2, 3):
            by_send[('control', topic, n)] = {'refusal'}
    return by_send


def test_the_added_rules_allow_a_lead_when_refusals_are_kept_and_recoveries_gained(a2):
    assert probe_score.decide(base_sends(), 'holds', [])[0] == 'lead'


def test_losing_one_exercised_refusal_control_makes_it_negative(a2):
    by_send = base_sends()
    topic = topics('refusal control')[0]
    for n in (1, 2):
        by_send[('changed', topic, n)] = set()
    decision, numbers = probe_score.decide(by_send, 'holds', [])
    assert decision == 'negative' and numbers['of them, topics the changed request no longer declines in 2 of 3'] == [topic]


def test_a_recovery_gain_of_two_is_negative(a2):
    by_send = base_sends()
    recovered = [(topic, n) for topic in topics('recovery') for n in (1, 2, 3)]
    for topic, n in recovered[2:]:                       # the changed request recovers only two sends
        by_send[('changed', topic, n)] = {'refusal'}
    assert probe_score.decide(by_send, 'holds', [])[0] == 'negative'


def test_refusal_controls_the_control_declines_on_only_two_topics_are_inconclusive(a2):
    by_send = base_sends()
    for topic in topics('refusal control')[:2]:
        for n in (1, 2, 3):
            by_send[('control', topic, n)] = set()
    assert probe_score.decide(by_send, 'holds', [])[0] == 'inconclusive'


def test_a_control_that_already_writes_ten_recoveries_is_inconclusive(a2):
    by_send = base_sends()
    controls = [(topic, n) for topic in topics('recovery') for n in (1, 2, 3)]
    for topic, n in controls[:10]:
        by_send[('control', topic, n)] = set()
    assert probe_score.decide(by_send, 'holds', [])[0] == 'inconclusive'


def test_expected_refusals_on_refusal_controls_are_not_harm_under_rule_two(a2):
    by_send = base_sends()
    for topic in topics('refusal control'):              # the control declines 2 of 3, the changed request 3 of 3: 12 against 8
        by_send[('control', topic, 3)] = set()
    decision, numbers = probe_score.decide(by_send, 'holds', [])
    assert not [entry for entry in numbers['marks other than L where changed exceeds control + 1 (group, mark, changed, control)']
                if entry[0] in ('recovery', 'refusal control')] and decision == 'lead'


def test_the_a2_pipeline_runs_on_its_28_topics(a2, tmp_path):
    record, original = tmp_path / 'check-passed-a2.json', probe.RECORD
    probe.RECORD = record
    try:
        probe.check()
        probe.send(tmp_path / 'run', transport=test_probe.transport_with(test_probe.USAGE))
    finally:
        probe.RECORD = original
    reading_prep.main(tmp_path / 'run', tmp_path / 'keys')
    folder = tmp_path / 'run' / 'reading'
    subprocess.run([sys.executable, str(ROOT / 'clean-arch/step4-2026-11-10/stage_a/build_reader_packets.py'), str(tmp_path / 'keys' / 'key.json'),
                    '--run', f'{folder}={folder / "cases.json"}', '--readers', str(folder / 'readers')], check=True, capture_output=True)
    test_probe_score.write_readers(folder, tmp_path / 'keys', {})
    last = test_probe_score.decision(folder, tmp_path / 'keys')
    assert len(json.loads((tmp_path / 'run' / 'changed' / 'cases.json').read_text())) == 28
    assert last == 'DECISION: inconclusive'          # identical fake answers: the control fails L on no motivating topic


def test_a_code_refusal_on_a_refusal_control_is_not_a_kept_refusal(a2):
    by_send = base_sends()
    topic = topics('refusal control')[0]
    for n in (1, 2):
        by_send[('changed', topic, n)] = {'refused twice'}
    decision, numbers = probe_score.decide(by_send, 'holds', [])
    assert numbers['of them, topics the changed request no longer declines in 2 of 3'] == [topic] and decision == 'negative'


def test_a_recovery_with_any_failing_mark_is_not_correct(a2):
    by_send = base_sends()
    for index, (topic, n) in enumerate((t, n) for t in topics('recovery') for n in (1, 2, 3)):
        if index >= 2:                                   # ten of the twelve written answers carry an unlisted part
            by_send[('changed', topic, n)] = {'L'}
    assert probe_score.decide(by_send, 'holds', [])[0] == 'negative'


def test_unjustified_refusals_on_recovery_topics_still_count_under_rule_two(a2):
    by_send = base_sends()
    for topic in topics('recovery'):                     # the control's refusals are justified; the changed request declines
        by_send[('changed', topic, 1)] = {'refusal', 'N'}  # once a topic for a reason the readers reject
    decision, numbers = probe_score.decide(by_send, 'holds', [])
    assert ('recovery', 'N', 4, 0) in numbers['marks other than L where changed exceeds control + 1 (group, mark, changed, control)']
    assert decision == 'negative'
