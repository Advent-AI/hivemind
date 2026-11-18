"""The complementary Astra screen at $0 (council round 15): the 14 topics are the 26 less the first screen's 12, and the same launcher
sends, reads and scores them as it did the first 12 (run in its own process: importing `astra_rest` re-points the launcher)."""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / 'model'), str(HERE.parent / 'effort')]
import astra_rest  # noqa: E402
import test_astra_probe as first  # noqa: E402   (its fake transport and made-up reader rows)
import refcontrol  # noqa: E402

probe = astra_rest.base
KEY = first.KEY


def names(entries):
    return {f'{source}:{name}' for source, name, _, _ in entries}


def test_the_complement_is_the_fourteen_topics_the_first_screen_left_out():
    rest, earlier = names(astra_rest.complement()), names(astra_rest.first_sample())
    assert len(rest) == 14 and not rest & earlier and rest | earlier == names(refcontrol.population())
    assert 'fortnight:c1/clean-13' in rest and 'week-10-06:c1/clean-7' in rest       # where D629's ladder and refusal faults were


@pytest.fixture(scope='module')
def run(tmp_path_factory):
    folder = tmp_path_factory.mktemp('rest')
    original, probe.RECORD = probe.RECORD, folder / 'check-passed-rest.json'
    try:
        probe.check()
        fake = first.transport()
        probe.send(folder / 'run', transport=fake)
        probe.reading(folder / 'run', folder / 'keys')
        yield folder, fake
    finally:
        probe.RECORD = original


def test_each_arm_draw_sends_the_fourteen_and_the_reading_holds_both_arms(run):
    folder, fake = run
    rest = names(astra_rest.complement())
    for arm, draw in probe.ORDER:
        rows = [json.loads(line) for line in (folder / 'run' / f'{arm}-d{draw}' / 'outcomes.jsonl').read_text().splitlines()]
        assert {row['case'].split('|', 1)[1] for row in rows} == rest and len(rows) == 14
    key = json.loads((folder / 'keys' / 'key.json').read_text())
    arms = [case.split('-d')[0] for case, _ in key.values() if not case.startswith('control|')]
    assert arms.count('sol') == 42 and arms.count('astra') == 42 and len(key) == 90


def test_one_astra_failure_against_three_is_promising_on_the_fourteen(run):
    folder, _ = run
    first.write_rows(folder, first.faulted({'sol-d1': first.ladders(folder, 'sol-d1')[:3], 'astra-d2': first.ladders(folder, 'astra-d2')[:1]}))
    verdict, report = probe.score(folder / 'run', folder / 'keys')
    assert report['holds'][KEY] == {'sol': 3, 'astra': 1} and verdict.startswith('promising')


def test_three_astra_failures_close_it_on_the_fourteen(run):
    folder, _ = run
    first.write_rows(folder, first.faulted({'sol-d1': first.ladders(folder, 'sol-d1')[:4], 'astra-d3': first.ladders(folder, 'astra-d3')[:3]}))
    verdict, report = probe.score(folder / 'run', folder / 'keys')
    assert report['holds'][KEY] == {'sol': 4, 'astra': 3} and verdict == 'closes this candidate under this test'
