"""Tests of the decision rule (DESIGN.md, "Decision rule"), end to end at $0: a fake-transport probe run, the real reading folder and
packet builder, made-up reader rows with known marks, and the scorer's printed decision.

Run: python3 -m pytest docs/research/2026-11-14-use-acceptance/unlisted-parts/test_probe_score.py
"""
import contextlib
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
import probe  # noqa: E402
import probe_score  # noqa: E402
from probe_score import accounting  # noqa: E402
import h_disputes  # noqa: E402
import reading_prep  # noqa: E402
import test_probe  # noqa: E402

MOTIVATING = [f'{source}:{name}' for source, name in probe.TOPICS['motivating']]
HARM_CONTROLS = [f'{source}:{name}' for source, name in probe.TOPICS['harm control']]


@pytest.fixture(scope='module')
def reading(tmp_path_factory):
    """A probe run through the fake transport, its reading folder, the real packets and key."""
    base = tmp_path_factory.mktemp('probe')
    record, original = base / 'check-passed.json', probe.RECORD
    probe.RECORD = record
    try:
        probe.check()
        probe.send(base / 'run', transport=test_probe.transport_with(test_probe.USAGE))
    finally:
        probe.RECORD = original
    reading_prep.main(base / 'run', base / 'keys')
    folder = base / 'run' / 'reading'
    subprocess.run([sys.executable, str(ROOT / 'clean-arch/step4-2026-11-10/stage_a/build_reader_packets.py'), str(base / 'keys' / 'key.json'),
                    '--run', f'{folder}={folder / "cases.json"}', '--readers', str(folder / 'readers')], check=True, capture_output=True)
    return folder, base / 'keys'


def row_for(outcome, item, marks):
    kind = accounting.kind_of(outcome)
    applicable = accounting.marks_that_apply(kind)
    parts = probe_score.parts_listed(outcome)
    row = {'item': item, 'W': '', 'why': '', 'B': ['not_a_bet'] * parts, 'H': ['part'] * parts}
    for mark in accounting.ALL_MARKS:
        row[mark] = 'holds' if mark in applicable else 'n/a'
    row['G'] = 'not_assessable' if kind in ('company figure', 'theme figure') else 'n/a'
    row.update(marks)
    if any(value == 'fails' for value in marks.values()):
        row['why'] = 'made-up fault for the test'
    return row


def write_readers(folder, keys, faults, h_override=None):
    """Both families' rows: every mark holds except `faults` {(case, pass): {mark: 'fails'}}; plants marked as expected unless
    `h_override` {(family, plant): value} says otherwise."""
    key = json.loads((keys / 'key.json').read_text())
    outcomes = {(o['case'], o['pass']): o for o in probe_score.collector.outcomes_of(folder)}
    expected = json.loads((keys / 'plants-expected.json').read_text())
    shutil.rmtree(folder / 'third-reader', ignore_errors=True)
    answers = folder / 'readers-answers'
    if answers.exists():
        for old in answers.iterdir():
            old.unlink()
    answers.mkdir(exist_ok=True)
    for family in ('codex', 'claude'):
        lines = []
        for item, (case, pass_number) in key.items():
            outcome = outcomes[(case, pass_number)]
            row = row_for(outcome, int(item), faults.get((case, pass_number), {}))
            if case in expected:
                row['H'][expected[case]['position']] = (h_override or {}).get((family, case), expected[case]['expected'])
                if row['H'][expected[case]['position']] != 'part':
                    row['why'] = 'a listed item is not a part'
            lines.append(json.dumps(row))
        (answers / f'reader-{family}-packet-1.jsonl').write_text('\n'.join(lines) + '\n')


def decision(folder, keys):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        probe_score.main(folder, keys / 'key.json', keys / 'plants-expected.json')
    return out.getvalue().strip().splitlines()[-1]


def l_failures(arm, topics):
    return {(f'{arm}|{topic}', 1): {'L': 'fails'} for topic in topics}


def test_a_large_drop_with_no_harm_is_a_lead(reading):
    folder, keys = reading
    write_readers(folder, keys, l_failures('control', MOTIVATING[:4]))
    assert decision(folder, keys) == 'DECISION: lead'


def test_a_control_that_fails_l_on_two_topics_is_inconclusive(reading):
    folder, keys = reading
    write_readers(folder, keys, l_failures('control', MOTIVATING[:2]))
    assert decision(folder, keys) == 'DECISION: inconclusive'


def test_harm_on_the_harm_controls_makes_it_negative(reading):
    folder, keys = reading
    faults = l_failures('control', MOTIVATING[:4])
    faults.update({(f'changed|{topic}', 1): {'Q': 'fails'} for topic in HARM_CONTROLS[:2]})
    write_readers(folder, keys, faults)
    assert decision(folder, keys) == 'DECISION: negative'


def test_the_changed_arm_failing_l_on_two_topics_is_negative(reading):
    folder, keys = reading
    faults = l_failures('control', MOTIVATING[:4])
    faults.update(l_failures('changed', MOTIVATING[:2]))
    write_readers(folder, keys, faults)
    assert decision(folder, keys) == 'DECISION: negative'


@pytest.mark.parametrize('control_topics', [4, 2])           # a missed plant stops the reading even when the control is weak
def test_a_missed_planted_control_stops_the_reading(reading, control_topics):
    folder, keys = reading
    write_readers(folder, keys, l_failures('control', MOTIVATING[:control_topics]), h_override={('claude', 'plant|1'): 'part'})
    assert decision(folder, keys).startswith('DECISION: STOPPED: a planted control was missed')


def test_a_row_without_h_is_not_scored(reading):
    folder, keys = reading
    write_readers(folder, keys, l_failures('control', MOTIVATING[:4]))
    answer = folder / 'readers-answers' / 'reader-codex-packet-1.jsonl'
    rows = [json.loads(line) for line in answer.read_text().splitlines()]
    del rows[0]['H']
    answer.write_text('\n'.join(json.dumps(row) for row in rows) + '\n')
    with pytest.raises(SystemExit, match='NOT SCORED'):
        decision(folder, keys)


def test_an_h_disagreement_without_both_rulings_is_not_scored(reading):
    folder, keys = reading
    write_readers(folder, keys, l_failures('control', MOTIVATING[:4]))
    key = json.loads((keys / 'key.json').read_text())
    outcomes = {(o['case'], o['pass']): o for o in probe_score.collector.outcomes_of(folder)}
    item = next(int(n) for n, (case, pass_number) in key.items()
                if case.startswith('changed|') and probe_score.parts_listed(outcomes[(case, pass_number)]) > 0)
    answer = folder / 'readers-answers' / 'reader-claude-packet-1.jsonl'
    rows = [json.loads(line) for line in answer.read_text().splitlines()]
    for row in rows:
        if row['item'] == item:
            row['H'][0], row['why'] = 'settlement', 'the listed item names only a source'
    answer.write_text('\n'.join(json.dumps(row) for row in rows) + '\n')
    with pytest.raises(SystemExit, match='H points need both third-reader families'):
        decision(folder, keys)
    (folder / 'third-reader').mkdir()
    for family in ('codex', 'claude'):                     # both families present, but neither rules this point
        (folder / 'third-reader' / f'h-rulings-{family}-1.jsonl').write_text(json.dumps({'id': '999999-H-0', 'ruling': 'part'}) + '\n')
    with pytest.raises(SystemExit, match=f'H rulings missing for .*{item}-H-0'):
        decision(folder, keys)


def first_changed_item(folder, keys, with_parts=False):
    key = json.loads((keys / 'key.json').read_text())
    outcomes = {(o['case'], o['pass']): o for o in probe_score.collector.outcomes_of(folder)}
    return next(int(n) for n, (case, pass_number) in key.items() if case.startswith('changed|')
                and (not with_parts or probe_score.parts_listed(outcomes[(case, pass_number)]) > 0))


def edit_row(folder, family, item, change):
    answer = folder / 'readers-answers' / f'reader-{family}-packet-1.jsonl'
    rows = [json.loads(line) for line in answer.read_text().splitlines()]
    for row in rows:
        if row['item'] == item:
            change(row)
    answer.write_text('\n'.join(json.dumps(row) for row in rows) + '\n')


def test_a_difference_ruled_by_one_third_reader_family_is_not_scored(reading):
    folder, keys = reading
    write_readers(folder, keys, l_failures('control', MOTIVATING[:4]))
    item = first_changed_item(folder, keys)
    edit_row(folder, 'codex', item, lambda row: row.update(Q='fails', why='made-up fault'))
    (folder / 'third-reader').mkdir()
    (folder / 'third-reader' / 'rulings-codex-1.jsonl').write_text(json.dumps({'id': f'{item}-Q', 'ruling': 'holds', 'why': 'x'}) + '\n')
    with pytest.raises(SystemExit, match='need both third-reader families'):
        decision(folder, keys)


@pytest.mark.parametrize('lines, message', [
    (['{"id": "ITEM-H-0", "ruling": "fine"}'], 'not one of'),
    (['{"id": "ITEM-H-0", "ruling": "part"}', '{"id": "ITEM-H-0", "ruling": "settlement"}'], 'ruled twice'),
])
def test_an_h_ruling_outside_the_four_values_or_given_twice_is_not_scored(reading, lines, message):
    folder, keys = reading
    write_readers(folder, keys, l_failures('control', MOTIVATING[:4]))
    item = first_changed_item(folder, keys, with_parts=True)
    edit_row(folder, 'claude', item, lambda row: row['H'].__setitem__(0, 'settlement') or row.update(why='a source only'))
    (folder / 'third-reader').mkdir()
    for family in ('codex', 'claude'):
        (folder / 'third-reader' / f'h-rulings-{family}-1.jsonl').write_text('\n'.join(line.replace('ITEM', str(item)) for line in lines) + '\n')
    with pytest.raises(SystemExit, match=message):
        decision(folder, keys)


def test_a_reading_that_misses_a_send_is_not_scored(reading, tmp_path):
    folder, keys = reading
    write_readers(folder, keys, l_failures('control', MOTIVATING[:4]))
    copy = tmp_path / 'reading'
    shutil.copytree(folder, copy)
    outcomes = copy / 'send-2' / 'outcomes.jsonl'
    outcomes.write_text('\n'.join(line for line in outcomes.read_text().splitlines() if not line.startswith('{"case": "control|')
                                   or MOTIVATING[0] not in line) + '\n')
    with pytest.raises(SystemExit, match='exactly once'):
        decision(copy, keys)


def test_an_altered_plants_file_is_not_scored(reading, tmp_path):
    folder, keys = reading
    write_readers(folder, keys, l_failures('control', MOTIVATING[:4]))
    altered = tmp_path / 'keys'
    shutil.copytree(keys, altered)
    expected = json.loads((altered / 'plants-expected.json').read_text())
    expected['plant|1']['expected'] = 'part'
    (altered / 'plants-expected.json').write_text(json.dumps(expected))
    with pytest.raises(SystemExit, match='plants file'):
        decision(folder, altered)


def test_h_disagreements_go_to_the_third_readers_and_their_rulings_decide(reading):
    """Two changed harm-control sends whose first part the readers split on: the H packet holds exactly those points with both marks
    unnamed; both families rule them `settlement`; the changed arm then fails H on two sends against none, and rule 2 makes it negative."""
    folder, keys = reading
    write_readers(folder, keys, l_failures('control', MOTIVATING[:4]))
    key = json.loads((keys / 'key.json').read_text())
    outcomes = {(o['case'], o['pass']): o for o in probe_score.collector.outcomes_of(folder)}
    items = [int(n) for n, (case, pass_number) in sorted(key.items(), key=lambda pair: int(pair[0]))
             if case.split('|')[0] == 'changed' and case.split('|')[1] in HARM_CONTROLS and pass_number == 1
             and probe_score.parts_listed(outcomes[(case, pass_number)]) > 0][:2]
    assert len(items) == 2
    for item in items:
        edit_row(folder, 'claude', item, lambda row: row['H'].__setitem__(0, 'settlement') or row.update(why='a source only'))
    assert h_disputes.main(folder, keys / 'key.json') == 2
    packet = json.loads((folder / 'third-reader' / 'h-packet-1.json').read_text())
    assert sorted(point['id'] for point in packet) == sorted(f'{item}-H-0' for item in items)
    assert all(sorted(point['marks'].values()) == ['part', 'settlement'] and set(point['marks']) == {'a', 'b'} for point in packet)
    for family in ('codex', 'claude'):
        (folder / 'third-reader' / f'h-rulings-{family}-1.jsonl').write_text(
            '\n'.join(json.dumps({'id': point['id'], 'ruling': 'settlement', 'why': 'names a source'}) for point in packet) + '\n')
    assert decision(folder, keys) == 'DECISION: negative'
