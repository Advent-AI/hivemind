"""Tests of FRESH-A2-DESIGN.md v4's harness and decision ($0), on a stand-in: the 10-06 week's 13 stored cases as the "fresh" cases,
answered by their own stored answers through a fake transport, read by made-up readers.

Run: python3 -m pytest docs/research/2026-11-14-use-acceptance/unlisted-parts/fresh-a2/test_fresh.py
"""
import contextlib
import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path[:0] = [str(HERE), str(HERE.parent)]
import fresh_probe  # noqa: E402
import fresh_score  # noqa: E402
import probe  # noqa: E402
import reading_prep  # noqa: E402
import test_probe_score  # noqa: E402

WEEK = ROOT / 'poc/data/clean-second-week-2026-11-15/week-continued'
USAGE = {'prompt_tokens': 5000, 'completion_tokens': 1500}


def stored_answers():
    rows = [json.loads(line) for line in (WEEK / 'stage-a/send-1/outcomes.jsonl').read_text().splitlines() if line]
    return {row['case']: row['requests'][-1]['answer_text'] for row in rows if row['pass'] == 1 and row['requests'] and row['requests'][-1].get('answer_text')}


@pytest.fixture(scope='module')
def run(tmp_path_factory):
    folder = tmp_path_factory.mktemp('fresh')
    answers = stored_answers()
    cases = [case for case in json.loads((WEEK / 'c1/cases/cases.json').read_text()) if case['case'] in answers]
    (folder / 'cases.json').write_text(json.dumps(cases))
    names = [case['case'] for case in cases]
    ladders = [name for name in names if json.loads(answers[name]).get('ladder')]      # only a written answer can leave a part unlisted
    (folder / 'population.json').write_text(json.dumps({'population_a': names, 'population_b': ladders[:6]}))
    by_description = {json.dumps(case['thesis']['description'], ensure_ascii=False)[1:-1]: answers[case['case']] for case in cases}

    def transport(provider, request):
        user = request['messages'][1]['content']
        return {'choices': [{'message': {'content': next(text for key, text in by_description.items() if key in user)}}], 'usage': USAGE}
    original = fresh_probe.RECORD
    fresh_probe.RECORD = folder / 'check.json'
    try:
        fresh_probe.check(folder / 'cases.json', folder / 'population.json')
        fresh_probe.send(folder / 'cases.json', folder / 'population.json', folder / 'run', transport=transport)
    finally:
        fresh_probe.RECORD = original
    reading_prep.main(folder / 'run', folder / 'keys')
    reading = folder / 'run' / 'reading'
    subprocess.run([sys.executable, str(ROOT / 'clean-arch/step4-2026-11-10/stage_a/build_reader_packets.py'), str(folder / 'keys' / 'key.json'),
                    '--run', f'{reading}={reading / "cases.json"}', '--readers', str(reading / 'readers')], check=True, capture_output=True)
    yield folder, ladders
    probe.configure('a')


def decision(folder, faults):
    test_probe_score.write_readers(folder / 'run' / 'reading', folder / 'keys', faults)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        fresh_score.main(folder / 'cases.json', folder / 'population.json', folder / 'run' / 'reading', folder / 'keys' / 'key.json',
                         folder / 'keys' / 'plants-expected.json')
    return out.getvalue().strip().splitlines()[-1]


def l_faults(arm, names):
    return {(f'{arm}|fresh:{name}', 1): {'L': 'fails'} for name in names}


def test_a2_removing_omitted_parts_on_both_populations_is_a_lead(run):
    folder, names = run
    assert decision(folder, l_faults('control', names[:3])) == 'DECISION: lead'


def test_a2_omitting_parts_on_two_topics_is_negative(run):
    folder, names = run
    assert decision(folder, {**l_faults('control', names[:4]), **l_faults('changed', names[:2])}) == 'DECISION: negative'


def test_a_population_b_without_two_control_omissions_gives_no_verdict(run):
    folder, names = run
    assert decision(folder, l_faults('control', [names[0], names[7]])) == 'DECISION: no verdict'


def test_a_new_a2_fault_makes_a_lead_provisional_until_reviewed(run):
    folder, names = run
    faults = {**l_faults('control', names[:3]), ('changed|fresh:' + names[1], 2): {'Y': 'fails'}}
    assert decision(folder, faults) == 'DECISION: lead (PROVISIONAL: the trace review is not done)'
