"""The paired rule's verdict paths at $0 (council round 5: "verify those paths before sending"): synthetic outcomes, reader rows and review
rows through `paired_probe.score`, with the reader collection replaced by the synthetic rows; and the shared-cap refusal in `check`."""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paired_probe as probe  # noqa: E402

FIGURE = {'status': 'ladder', 'answer': {'ladder': {'figure': {'unit': 'USD'}, 'event': None, 'not_judged': [{'part': 'the second side', 'why': 'context'}]}},
          'view': {'kind': 'theme'}}
DECLINE = {'status': 'no ladder', 'answer': {'no_ladder': 'several with none the main one', 'ladder': None}, 'view': None}


def holds_row(outcome):
    kind = probe.accounting.kind_of(outcome)
    applicable = probe.accounting.marks_that_apply(kind)
    row = {mark: ('holds' if mark in applicable else 'n/a') for mark in probe.accounting.ALL_MARKS}
    row['G'] = 'not_assessable' if kind in ('company figure', 'theme figure') else 'n/a'
    row.update(B=['not_a_bet'] * (0 if kind == 'refusal' else len(outcome['answer']['ladder']['not_judged'])), W='', why='')
    return row


def build(tmp_path, monkeypatch, statuses, fail=None, review=None):
    """statuses: {(arm, draw, topic): 'ladder' | 'no ladder'}; fail: {(arm, draw, topic): mark failed by the claude family};
    review: {(arm, draw, topic): {'codex': [...], 'claude': [...]}}."""
    run = tmp_path / 'run'
    outcomes, readers = {}, {family: {} for family in probe.collector.FAMILIES}
    for arm, draw in probe.ORDER:
        rows = []
        for topic in probe.topics_of(draw):
            status = statuses.get((arm, draw, topic), 'no ladder')
            outcome = dict(FIGURE if status == 'ladder' else DECLINE, case=f'{arm}-d{draw}|{topic}')
            if status == 'no ladder: refused':
                outcome = dict(outcome, status=status, answer=None)
            rows.append(outcome)
            send = (outcome['case'], 1)
            outcomes[send] = outcome
            if status == 'no ladder: refused':
                continue                                          # a lost answer goes to no reader
            for family in readers:
                row = holds_row(outcome)
                if fail and family == list(probe.collector.FAMILIES)[1] and (arm, draw, topic) in fail:
                    row[fail[(arm, draw, topic)]] = 'fails'
                    row['why'] = 'a planted fault for the test'
                readers[family][send] = row
        (run / f'{arm}-d{draw}').mkdir(parents=True)
        (run / f'{arm}-d{draw}' / 'outcomes.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in rows))
    keys = tmp_path / 'keys'
    keys.mkdir()
    (keys / 'controls-expected.json').write_text('{}')
    reviewed = [name for name, outcome in ((o['case'], o) for o in outcomes.values())
                if outcome['status'] == 'ladder' and name.split('|', 1)[1] in probe.TARGETS + probe.SHARE + ('u3/clean-10',)]
    (keys / 'review-key.json').write_text(json.dumps({str(n): name for n, name in enumerate(reviewed, start=1)}))
    for family in ('codex', 'claude'):
        lines = []
        for n, name in enumerate(reviewed, start=1):
            arm_draw, topic = name.split('|', 1)
            arm, draw = arm_draw.split('-d')
            defects = ((review or {}).get((arm, int(draw), topic)) or {}).get(family, [])
            lines.append(json.dumps({'item': n, 'defects': defects, 'why': ''}))
        (tmp_path / f'review-{family}.jsonl').write_text('\n'.join(lines) + '\n')
    monkeypatch.setattr(probe.collector, 'read_rows', lambda folder, key_path: ({}, {}, outcomes, readers, {family: {'rows': [], 'unreadable lines': []} for family in probe.collector.FAMILIES}))
    return run, keys, tmp_path / 'review-codex.jsonl', tmp_path / 'review-claude.jsonl'


def passing_statuses():
    out = {}
    for draw in (1, 2, 3):
        for topic in probe.TARGETS:
            out[('frozen', draw, topic)] = 'no ladder'
            out[('edited', draw, topic)] = 'ladder'
    for draw in (1, 2):
        out[('edited', draw, 'u3/clean-11')] = 'ladder'
        out[('frozen', draw, 'u3/clean-11')] = 'ladder'
    return out


def test_a_clean_run_passes(tmp_path, monkeypatch):
    assert probe.score(*build(tmp_path, monkeypatch, passing_statuses())) == 'PASS'


def test_one_reviewer_marking_a_wrong_side_on_one_edited_target_fails_it(tmp_path, monkeypatch):
    review = {('edited', 2, 'acc/clean-9'): {'claude': ['i']}}
    assert probe.score(*build(tmp_path, monkeypatch, passing_statuses(), review=review)) == 'FAIL'


def test_a_due_day_defect_alone_is_reported_not_deciding(tmp_path, monkeypatch):
    review = {('edited', 1, 'acc/clean-8'): {'codex': ['iv'], 'claude': ['iv']}}
    assert probe.score(*build(tmp_path, monkeypatch, passing_statuses(), review=review)) == 'PASS'


def test_one_family_failing_a_hard_line_on_an_edited_target_fails_it(tmp_path, monkeypatch):
    assert probe.score(*build(tmp_path, monkeypatch, passing_statuses(), fail={('edited', 3, 'pool-17'): 'L'})) == 'FAIL'


def test_a_control_written_in_the_edited_arm_fails(tmp_path, monkeypatch):
    statuses = {**passing_statuses(), ('edited', 1, 'week-10-06:c1/clean-4'): 'ladder'}
    assert probe.score(*build(tmp_path, monkeypatch, statuses)) == 'FAIL'


def test_the_reported_topic_does_not_decide(tmp_path, monkeypatch):
    statuses = {**passing_statuses(), ('edited', 1, 'u2/clean-10'): 'ladder'}
    assert probe.score(*build(tmp_path, monkeypatch, statuses)) == 'PASS'


def test_the_share_control_asking_the_total_fails(tmp_path, monkeypatch):
    review = {('edited', 1, 'u3/clean-11'): {'codex': ['i']}}
    assert probe.score(*build(tmp_path, monkeypatch, passing_statuses(), review=review)) == 'FAIL'


def test_too_few_frozen_declines_is_inconclusive(tmp_path, monkeypatch):
    statuses = passing_statuses()
    for draw in (1, 2, 3):
        for topic in probe.TARGETS[1:]:
            statuses[('frozen', draw, topic)] = 'ladder'          # only acc/clean-8 declined: 3 sends on 1 target
    assert probe.score(*build(tmp_path, monkeypatch, statuses)).startswith('INCONCLUSIVE')


def test_the_capacity_topic_is_reported_not_deciding(tmp_path, monkeypatch):
    statuses = {**passing_statuses(), **{('edited', draw, 'u3/clean-10'): 'no ladder' for draw in (1, 2, 3)}}
    assert probe.score(*build(tmp_path, monkeypatch, statuses)) == 'PASS'


def test_a_review_row_without_a_defects_list_is_not_measured(tmp_path, monkeypatch):
    run, keys, codex, claude = build(tmp_path, monkeypatch, passing_statuses())
    lines = codex.read_text().splitlines()
    lines[0] = json.dumps({'item': 1, 'why': ''})
    codex.write_text('\n'.join(lines) + '\n')
    with pytest.raises(SystemExit, match='NOT MEASURED'):
        probe.score(run, keys, codex, claude)


def test_check_refuses_a_shared_cap_below_the_room_and_expected_spend(monkeypatch, tmp_path):
    monkeypatch.setattr(probe, 'TOTAL_CAP', 2.0)
    monkeypatch.setattr(probe, 'RECORD', tmp_path / 'check-passed.json')
    with pytest.raises(SystemExit, match='CHECK FAILED'):
        probe.check()


def test_a_share_control_decline_neither_family_faults_passes(tmp_path, monkeypatch):
    statuses = {**passing_statuses(), ('edited', 1, 'u3/clean-11'): 'no ladder'}
    assert probe.score(*build(tmp_path, monkeypatch, statuses)) == 'PASS'


def test_a_share_control_decline_one_family_marks_unjustified_fails(tmp_path, monkeypatch):
    statuses = {**passing_statuses(), ('edited', 1, 'u3/clean-11'): 'no ladder'}
    assert probe.score(*build(tmp_path, monkeypatch, statuses, fail={('edited', 1, 'u3/clean-11'): 'N'})) == 'FAIL'


def test_a_lost_answer_on_a_reported_topic_fails(tmp_path, monkeypatch):
    statuses = {**passing_statuses(), ('edited', 2, 'u2/clean-10'): 'no ladder: refused'}
    assert probe.score(*build(tmp_path, monkeypatch, statuses)).startswith('FAIL')


def test_a_lost_answer_fails_even_when_the_frozen_arm_is_not_exercised(tmp_path, monkeypatch):
    statuses = {**passing_statuses(), ('edited', 1, 'u3/clean-10'): 'no ladder: refused'}
    for draw in (1, 2, 3):
        for topic in probe.TARGETS:
            statuses[('frozen', draw, topic)] = 'ladder'          # no frozen decline at all: alone, INCONCLUSIVE
    assert probe.score(*build(tmp_path, monkeypatch, statuses)).startswith('FAIL')
