"""Tests of DESIGN-A3.md v11's decision ($0): Reading B's four required cases (matching `settlement` fails; a disagreement is
unresolved in both countings; an agreed first-reader `already_judged` is overturned to `part`; a mixed entry whose named-way part holds
and whose other part fails, fails), the removal check over the cannot-tell range, the A3 checks that make it negative, the outcome
mapping, and the whole three-arm pipeline (check, fake-transport send, reading folder, packets, classer and named-way packets, score).

Run: python3 -m pytest docs/research/2026-11-14-use-acceptance/unlisted-parts/test_probe_score_a3.py
"""
import contextlib
import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
import a3_reading  # noqa: E402
import probe  # noqa: E402
import probe_score_a3 as score  # noqa: E402
import reading_prep  # noqa: E402
import test_probe  # noqa: E402
import test_probe_score  # noqa: E402

NAMED = {'kind': 'named way', 'matter': 'a termination or withdrawal', 'text': 'termination'}
OTHER = {'kind': 'other', 'matter': 'a repricing', 'text': 'repricing'}
ROWS = ({'H': ['already_judged']}, {'H': ['already_judged']})
OUTCOME = {'answer': {'no_ladder': None, 'ladder': {'not_judged': [{'part': 'termination or repricing', 'why': 'x'}]}}, 'status': 'ladder'}


@pytest.fixture
def a3():
    probe.configure('a3')
    yield
    probe.configure('a')


def test_matching_settlement_rulings_fail_the_part():
    assert score.entry_value_b([{'codex': 'settlement', 'claude': 'settlement'}], 'holds') == 'fails'


def test_a_disagreement_is_unresolved_in_both_countings():
    ruled = [{'codex': 'part', 'claude': 'already_judged'}]
    assert (score.entry_value_b(ruled, 'holds'), score.entry_value_b(ruled, 'fails')) == ('holds', 'fails')


def test_an_agreed_already_judged_on_a_named_way_is_overturned_by_two_part_rulings(monkeypatch):
    monkeypatch.setattr(score.ps.accounting, 'kind_of', lambda outcome: 'ladder')
    classes, named = {'7-H-0': [NAMED]}, {'7-H-0-0': {'codex': 'part', 'claude': 'part'}}
    assert score.failed_h_a(ROWS, 7, OUTCOME, {}, 'holds') is True
    assert score.failed_h_b(ROWS, 7, OUTCOME, {}, 'holds', classes, named) is False


def test_a_mixed_entry_whose_named_way_holds_still_fails_through_its_other_part(monkeypatch):
    monkeypatch.setattr(score.ps.accounting, 'kind_of', lambda outcome: 'ladder')
    classes = {'7-H-0': [NAMED, OTHER]}
    named = {'7-H-0-0': {'codex': 'part', 'claude': 'part'}, '7-H-0-1': {'codex': 'already_judged', 'claude': 'already_judged'}}
    assert score.failed_h_b(ROWS, 7, OUTCOME, {}, 'holds', classes, named) is True


@pytest.mark.parametrize('counts, expected', [((6, 0, 3, 0), 'passes'), ((6, 2, 2, 2), 'inconclusive'), ((6, 0, 4, 0), 'fails'),
                                              ((2, 0, 0, 0), 'inconclusive'), ((6, 2, 4, 0), 'inconclusive'), ((6, 2, 5, 0), 'fails')])
def test_the_removal_check_over_the_cannot_tell_range(counts, expected):
    assert score.removal(*counts) == expected


def topics(group):
    return [f'{source}:{name}' for source, name in probe.TOPICS[group]]


def base(a3_restating=1, a2_restating=6):
    """Every send passes, except: the control fails L on four motivating topics; every arm declines the refusal controls justifiably;
    the control declines the recovery topics; on the four event topics A2 lists restatements and a named way in every send."""
    by_send = {(arm, f'{source}:{name}', n): set() for arm in probe.ARMS for entries in probe.TOPICS.values() for source, name in entries
               for n in probe.PASSES}
    for topic in topics('motivating')[:4]:
        by_send[('control', topic, 1)] = {'L'}
    for topic in topics('refusal control'):
        for arm in probe.ARMS:
            for n in probe.PASSES:
                by_send[(arm, topic, n)] = {'refusal'}
    for topic in topics('recovery'):
        for n in probe.PASSES:
            by_send[('control', topic, n)] = {'refusal'}
    restating = {'kind': 'restates still awaited', 'matter': 'a delay past the check date', 'text': 'a delay'}
    kinds = {}
    for arm, count in (('control', 0), ('a2', a2_restating), ('changed', a3_restating)):
        for topic in a3_reading.EVENT_TOPICS:
            for n in probe.PASSES:
                kinds[(arm, topic, n)] = [[dict(NAMED)]] + ([[restating]] if (topic, n) in [(t, m) for t in a3_reading.EVENT_TOPICS for m in probe.PASSES][:count] else [])
    return by_send, kinds


def run_checks(by_send, kinds, settled=lambda topic, matter, counting: 0):
    numbers, failing, inconclusive = score.a3_checks(by_send, kinds, settled, 'holds')
    return score.verdict(failing, inconclusive, []), numbers, failing


def test_the_base_case_is_a_lead(a3):
    assert run_checks(*base())[0] == 'lead'


def test_a3_dropping_a_named_way_that_a2_keeps_is_negative(a3):
    by_send, kinds = base()
    topic = a3_reading.EVENT_TOPICS[0]
    for n in (1, 2):
        kinds[('changed', topic, n)] = []
    result, numbers, failing = run_checks(by_send, kinds)
    assert result == 'negative' and failing == ['named ways kept']
    assert numbers['named ways (topic, matter) A2 lists in 2 of 3 and A3 in fewer'] == [(topic, 'a termination or withdrawal')]


def test_a3_listing_a_different_named_way_does_not_keep_the_one_a2_listed(a3):   # A3's is outside the list; A2's in it
    by_send, kinds = base()
    topic = a3_reading.EVENT_TOPICS[0]
    for n in probe.PASSES:
        kinds[('changed', topic, n)] = [[dict(NAMED, matter='other', text='a court injunction')]]
    result, numbers, failing = run_checks(by_send, kinds)
    assert failing == ['named ways kept'] and numbers['named ways (topic, matter) A2 lists in 2 of 3 and A3 in fewer'] == [(topic, 'a termination or withdrawal')]


def test_a3_dropping_a_matter_a2_settles_as_a_part_is_negative(a3):
    by_send, kinds = base()
    settled = lambda topic, matter, counting: 3 if (topic, matter) == ('fortnight:c1/clean-6', 'a repricing') else 0
    result, _, failing = run_checks(by_send, kinds, settled)
    assert result == 'negative' and failing == ['parts kept']


def test_motivating_h_above_control_plus_two_is_negative_and_at_two_is_not(a3):
    by_send, kinds = base()
    motivating = topics('motivating')
    for topic in motivating[:2]:
        by_send[('changed', topic, 2)] = {'H'}
    assert run_checks(by_send, kinds)[0] == 'lead'
    by_send[('changed', motivating[2], 2)] = {'H'}
    assert run_checks(by_send, kinds)[2] == ['motivating H']


def test_too_few_restatements_in_a2_is_inconclusive_unless_a_check_fails(a3):
    assert run_checks(*base(a2_restating=2))[0] == 'inconclusive'
    by_send, kinds = base(a2_restating=2)
    by_send[('changed', topics('motivating')[0], 1)] = {'L'}
    by_send[('changed', topics('motivating')[1], 1)] = {'L'}
    assert run_checks(by_send, kinds)[0] == 'negative'


def test_the_outcome_mapping():
    verdicts = lambda a, b: {('A', 'holds'): a, ('A', 'fails'): a, ('B', 'holds'): b, ('B', 'fails'): b}
    only_h, other, none = {'holds': ['motivating H'], 'fails': ['motivating H']}, {'holds': ['parts kept'], 'fails': ['parts kept']}, {'holds': [], 'fails': []}
    same = {(name, counting): 1 for name in 'AB' for counting in ('holds', 'fails')}
    assert score.final(verdicts('negative', 'lead'), only_h, same) == 'diagnostic lead'
    assert score.final(verdicts('negative', 'lead'), other, same) == 'inconclusive'
    assert score.final(verdicts('inconclusive', 'lead'), none, same) == 'inconclusive'
    assert score.final(verdicts('lead', 'lead'), none, same) == 'lead'
    assert score.final(verdicts('lead', 'negative'), none, same) == 'negative'
    assert score.final({('A', 'holds'): 'lead', ('A', 'fails'): 'lead', ('B', 'holds'): 'lead', ('B', 'fails'): 'inconclusive'}, none, same) == 'inconclusive'


def test_no_diagnostic_lead_when_reading_b_passes_by_raising_the_controls_h():
    verdicts = {('A', 'holds'): 'negative', ('A', 'fails'): 'negative', ('B', 'holds'): 'lead', ('B', 'fails'): 'lead'}
    raised = {('A', 'holds'): 1, ('A', 'fails'): 1, ('B', 'holds'): 3, ('B', 'fails'): 1}
    assert score.final(verdicts, {'holds': ['motivating H'], 'fails': ['motivating H']}, raised) == 'inconclusive'


def test_two_different_named_ways_outside_the_matter_list_are_not_matched(a3):
    by_send, kinds = base()
    topic = a3_reading.EVENT_TOPICS[0]
    for n in probe.PASSES:
        kinds[('a2', topic, n)] = [[dict(NAMED)], [dict(NAMED, matter='other', text='a court injunction')]]
        kinds[('changed', topic, n)] = [[dict(NAMED)], [dict(NAMED, matter='other', text='a shareholder vote against it')]]
    result, numbers, failing = run_checks(by_send, kinds)
    assert result == 'inconclusive' and not failing and numbers['event topics where A2 lists a named way outside the matter list in 2 of 3 (unmatched)'] == [topic]


TO_CLASS = {'harm control|W': ['fortnight:c1/clean-4 p2'], 'motivating|Y': ['fortnight:c1/clean-13 p1']}
REVIEW = {'harm control|W|fortnight:c1/clean-4 p2': 'pre-existing', 'motivating|Y|fortnight:c1/clean-13 p1': 'present in A2'}


def test_the_trace_review_decides_after_the_score():
    assert 'PROVISIONAL' in score.after_review('lead', TO_CLASS, None)
    assert score.after_review('lead', TO_CLASS, REVIEW) == 'lead'
    assert score.after_review('diagnostic lead', TO_CLASS, dict(REVIEW, **{'motivating|Y|fortnight:c1/clean-13 p1': 'uncertain'})) == \
        'diagnostic lead, uncertain harms'
    assert score.after_review('lead', TO_CLASS, dict(REVIEW, **{'harm control|W|fortnight:c1/clean-4 p2': 'consistent with the sentence'})) == 'negative'
    assert score.after_review('negative', TO_CLASS, None) == 'negative'
    with pytest.raises(SystemExit, match='does not class exactly'):
        score.after_review('lead', TO_CLASS, {'harm control|W|fortnight:c1/clean-4 p2': 'pre-existing'})


def test_the_a3_pipeline_runs_on_three_arms(a3, tmp_path):
    record, original = tmp_path / 'check-passed-a3.json', probe.RECORD
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
    entries = a3_reading.classer_packet(folder, tmp_path / 'keys' / 'key.json')
    rows = [{'id': entry['id'], 'parts': [{'text': entry['entry'], 'kind': 'named way' if number == 0 else 'other', 'matter': 'other'}]}
            for number, entry in enumerate(entries)]
    (folder / 'a3' / 'class-codex-1.jsonl').write_text('\n'.join(map(json.dumps, rows)) + '\n')
    points = a3_reading.named_packet(folder)
    for family in ('codex', 'claude'):
        (folder / 'a3' / f'named-{family}-1.jsonl').write_text('\n'.join(json.dumps({'id': point['id'], 'ruling': 'part', 'why': 'x'})
                                                                          for point in points) + '\n')
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        score.main(folder, tmp_path / 'keys' / 'key.json', tmp_path / 'keys' / 'plants-expected.json')
    last = out.getvalue().strip().splitlines()[-1]
    assert len(json.loads((tmp_path / 'run' / 'a2' / 'cases.json').read_text())) == 28 and len(points) == 1
    assert last.endswith('RESULT: inconclusive')          # identical fake answers: the control fails L on no motivating topic


def test_an_a2_arm_that_is_not_control_plus_a2s_replacements_fails_the_check(a3, tmp_path, monkeypatch, capsys):
    original = probe.texts_of
    monkeypatch.setattr(probe, 'texts_of', lambda arm: dict(original(arm), closing=original(arm)['closing'] + ' Check once more.')
                        if arm == 'a2' else original(arm))
    monkeypatch.setattr(probe, 'RECORD', tmp_path / 'check-passed-a3.json')
    with pytest.raises(SystemExit, match='CHECK FAILED'):
        probe.check()
    assert not (tmp_path / 'check-passed-a3.json').exists()
