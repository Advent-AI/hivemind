"""The astra screen end to end at $0 (DESIGN.md): the check, the six interleaved arm-draws on the 12 sampled topics through the real runner
and limit with a fake transport answering each topic's stored answer, the first-request projection, the draw-start check, the blind
reading, made-up reader rows, and the verdict rule fixed before."""
import json
import random
import shutil
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / 'model'), str(HERE.parent / 'effort')]
import astra_probe as probe  # noqa: E402
import accounting  # noqa: E402
import refcontrol  # noqa: E402

USAGE = {'prompt_tokens': 5166, 'completion_tokens': 558}      # sol's measured means on the 26 topics (D629)
KEY = 'failed sends (agreed hard-line faults plus sends refused twice by code)'


def transport(usage=USAGE):
    stored = {case['thesis']['description']: row['requests'][-1]['answer_text'] for _, _, case, row in refcontrol.population()}
    seen = []

    def send(provider, request):
        seen.append(request.get('model'))
        user = request['messages'][1]['content']
        text = next(answer for description, answer in stored.items() if json.dumps(description, ensure_ascii=False)[1:-1] in user)
        return {'choices': [{'message': {'content': text}}], 'usage': usage}
    send.seen = seen
    return send


def topics():
    return sorted(f'{source}:{name}' for source, name, _, _ in probe.sample())


@pytest.fixture(scope='module')
def run(tmp_path_factory):
    folder = tmp_path_factory.mktemp('astra')
    original, probe.RECORD = probe.RECORD, folder / 'check-passed.json'
    try:
        probe.check()
        fake = transport()
        probe.send(folder / 'run', transport=fake)
        probe.reading(folder / 'run', folder / 'keys')
        yield folder, fake
    finally:
        probe.RECORD = original


def test_the_sample_is_twelve_of_the_twenty_six_drawn_by_the_fixed_seed():
    names = sorted(f'{source}:{name}' for source, name, _, _ in refcontrol.population())
    assert len(names) == 26 and topics() == sorted(random.Random(20261123).sample(names, 12))


def test_each_arm_draw_sends_the_twelve_topics_at_its_own_model(run):
    folder, fake = run
    for arm, draw in probe.ORDER:
        rows = [json.loads(line) for line in (folder / 'run' / f'{arm}-d{draw}' / 'outcomes.jsonl').read_text().splitlines()]
        assert sorted(row['case'].split('|', 1)[1] for row in rows) == topics() and all(row['case'].startswith(f'{arm}-d{draw}|') for row in rows)
    assert fake.seen.count('gpt-6.1-sol') >= 36 and fake.seen.count('gpt-6-astra') >= 36 and set(fake.seen) == {'gpt-6.1-sol', 'gpt-6-astra'}


def write_rows(folder, fail, unjustified=lambda case: False):
    key = json.loads((folder / 'keys' / 'key.json').read_text())
    expected = json.loads((folder / 'keys' / 'controls-expected.json').read_text())
    outcomes = {row['case']: row for row in map(json.loads, (folder / 'run' / 'reading' / 'send-1' / 'outcomes.jsonl').read_text().splitlines())}
    answers = folder / 'run' / 'reading' / 'readers-answers'
    answers.mkdir(exist_ok=True)
    for family in ('codex', 'claude'):
        lines = []
        for item, (case, _) in key.items():
            outcome = outcomes[case]
            kind = accounting.kind_of(outcome)
            applicable = accounting.marks_that_apply(kind)
            row = {'item': int(item), 'W': '', 'why': ''}
            for mark in accounting.ALL_MARKS:
                row[mark] = ('not_assessable' if kind in ('company figure', 'theme figure') else 'n/a') if mark == 'G' \
                    else 'holds' if mark in applicable else 'n/a'
            row['B'] = [] if kind == 'refusal' else ['not_a_bet'] * len(outcome['answer']['ladder']['not_judged'])
            for mark, value in expected.get(case, {}).items():
                if mark != 'all':
                    row[mark], row['why'] = value, 'planted'
            if fail(case) and 'L' in applicable:
                row['L'], row['why'] = 'fails', 'a part unlisted'
            if unjustified(case) and kind == 'refusal':
                row['N'], row['why'] = 'fails', 'the stated case does not apply'
            lines.append(json.dumps(row))
        (answers / f'reader-{family}-packet-1.jsonl').write_text('\n'.join(lines) + '\n')


def ladders(folder, arm_draw):
    rows = map(json.loads, (folder / 'run' / arm_draw / 'outcomes.jsonl').read_text().splitlines())
    return [row['case'].split('|', 1)[1] for row in rows if row['status'] == 'ladder']


def faulted(arm_draws):
    """A fail predicate: the ladders of each arm-draw on the topics given."""
    return lambda case: case.split('|', 1)[1] in arm_draws.get(case.split('|')[0], ())


def test_zero_against_zero_is_inconclusive_not_a_close(run):
    folder, _ = run
    write_rows(folder, lambda case: False)
    verdict, report = probe.score(folder / 'run', folder / 'keys')
    assert verdict.startswith('inconclusive') and report['holds'][KEY] == {'sol': 0, 'astra': 0}


def test_three_astra_failures_close_the_candidate_even_against_more(run):
    folder, _ = run
    write_rows(folder, faulted({'sol-d1': ladders(folder, 'sol-d1')[:5], 'astra-d2': ladders(folder, 'astra-d2')[:3]}))
    verdict, report = probe.score(folder / 'run', folder / 'keys')
    assert report['holds'][KEY] == {'sol': 5, 'astra': 3} and verdict == 'closes this candidate under this test'


def test_equal_failures_close_the_candidate(run):
    folder, _ = run
    write_rows(folder, faulted({'sol-d1': ladders(folder, 'sol-d1')[:2], 'astra-d1': ladders(folder, 'astra-d1')[:2]}))
    verdict, report = probe.score(folder / 'run', folder / 'keys')
    assert report['holds'][KEY] == {'sol': 2, 'astra': 2} and verdict == 'closes this candidate under this test'


def test_one_astra_failure_against_three_is_promising(run):
    folder, _ = run
    write_rows(folder, faulted({'sol-d1': ladders(folder, 'sol-d1')[:3], 'astra-d3': ladders(folder, 'astra-d3')[:1]}))
    verdict, report = probe.score(folder / 'run', folder / 'keys')
    assert report['holds'][KEY] == {'sol': 3, 'astra': 1} and verdict.startswith('promising')


def test_two_astra_failures_against_four_are_inconclusive_not_promising(run):
    folder, _ = run
    write_rows(folder, faulted({'sol-d2': ladders(folder, 'sol-d2')[:4], 'astra-d1': ladders(folder, 'astra-d1')[:2]}))
    verdict, report = probe.score(folder / 'run', folder / 'keys')
    assert report['holds'][KEY] == {'sol': 4, 'astra': 2} and verdict == 'inconclusive'


def test_an_advantage_resting_on_disputed_marks_is_inconclusive(run):
    folder, _ = run
    write_rows(folder, faulted({'sol-d1': ladders(folder, 'sol-d1')[:3]}))
    answers = folder / 'run' / 'reading' / 'readers-answers' / 'reader-claude-packet-1.jsonl'
    key = json.loads((folder / 'keys' / 'key.json').read_text())
    disputed = {int(item) for item, (case, _) in key.items()
                if case.startswith('astra-d1|') and case.split('|', 1)[1] in ladders(folder, 'astra-d1')[:4]}
    rows = [json.loads(line) for line in answers.read_text().splitlines()]
    for row in rows:
        if row['item'] in disputed:
            row['L'], row['why'] = 'fails', 'one family only'
    answers.write_text('\n'.join(json.dumps(row) for row in rows) + '\n')
    verdict, report = probe.score(folder / 'run', folder / 'keys')
    assert report['holds'][KEY] == {'sol': 3, 'astra': 0} and report['fails'][KEY] == {'sol': 3, 'astra': 4} and verdict == 'inconclusive'


def test_an_unjustified_astra_refusal_where_sol_has_none_blocks_promising(run):
    folder, _ = run
    refusal = next(row['case'] for row in map(json.loads, (folder / 'run' / 'astra-d1' / 'outcomes.jsonl').read_text().splitlines())
                   if row['status'] == 'no ladder')
    write_rows(folder, faulted({'sol-d1': ladders(folder, 'sol-d1')[:3]}), unjustified=lambda case: case == refusal)
    verdict, report = probe.score(folder / 'run', folder / 'keys')
    assert report['holds'][KEY] == {'sol': 3, 'astra': 1} and report['holds']['unjustified refusals'] == {'sol': 0, 'astra': 1}
    assert verdict == 'inconclusive'


def test_answers_astra_loses_to_code_refusals_count_as_failures(run, tmp_path):
    folder, _ = run
    copy = tmp_path / 'copy'
    shutil.copytree(folder, copy)
    lost = ladders(copy, 'astra-d1')[:3]
    path = copy / 'run' / 'astra-d1' / 'outcomes.jsonl'
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    for row in rows:
        if row['case'].split('|', 1)[1] in lost:
            row.update(status='no ladder: refused', answer=None, view=None, passage=None)
    path.write_text(''.join(json.dumps(row) + '\n' for row in rows))
    write_rows(copy, faulted({'sol-d1': ladders(copy, 'sol-d1')[:4]}))
    verdict, report = probe.score(copy / 'run', copy / 'keys')
    assert report['holds'][KEY] == {'sol': 4, 'astra': 3} and verdict == 'closes this candidate under this test'


def test_a_missed_planted_control_voids_the_reading(run):
    folder, _ = run
    write_rows(folder, lambda case: False)
    path = folder / 'run' / 'reading' / 'readers-answers' / 'reader-claude-packet-1.jsonl'
    key = json.loads((folder / 'keys' / 'key.json').read_text())
    item = next(int(item) for item, (case, _) in key.items() if case == 'control|unlisted-part')
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    for row in rows:
        if row['item'] == item:
            row['L'], row['why'] = 'holds', ''
    path.write_text('\n'.join(json.dumps(row) for row in rows) + '\n')
    with pytest.raises(SystemExit, match='VOID: a family missed the planted control\\|unlisted-part'):
        probe.score(folder / 'run', folder / 'keys')


def test_both_families_failing_a_sound_control_voids_the_reading_as_too_harsh(run):
    folder, _ = run
    write_rows(folder, lambda case: case == 'control|sound-clean-5')
    with pytest.raises(SystemExit, match='VOID: both families fail a hard line on the sound control\\|sound-clean-5'):
        probe.score(folder / 'run', folder / 'keys')


def test_the_check_refuses_an_astra_request_that_differs_in_more_than_its_model(tmp_path, monkeypatch):
    real = probe.built

    def built(case, setting, rl):
        request = real(case, setting, rl)
        if setting.model == 'gpt-6-astra':
            request['max_completion_tokens'] = request['max_completion_tokens'] + 1
        return request
    monkeypatch.setattr(probe, 'built', built)
    monkeypatch.setattr(probe, 'RECORD', tmp_path / 'check-passed.json')
    with pytest.raises(SystemExit, match='CHECK FAILED'):
        probe.check()
    assert not (tmp_path / 'check-passed.json').exists()


def test_a_first_astra_request_projecting_past_the_cap_stops_before_the_rest(tmp_path, monkeypatch):
    monkeypatch.setattr(probe, 'RECORD', tmp_path / 'check-passed.json')
    probe.check()
    costly = transport({'prompt_tokens': 5166, 'completion_tokens': 2000})        # astra $0.15 a send: $5.5 for 36
    with pytest.raises(SystemExit, match='astra d1 STOPPED: projected'):
        probe.send(tmp_path / 'run', transport=costly)
    assert costly.seen.count('gpt-6-astra') == 1


def test_a_draw_that_cannot_finish_under_its_cap_is_not_started(tmp_path, monkeypatch):
    monkeypatch.setattr(probe, 'RECORD', tmp_path / 'check-passed.json')
    probe.check()
    monkeypatch.setitem(probe.CAPS, 'sol', 0.90)      # a fake sol draw costs about $0.19, two attempts in flight reserve about $0.42:
    #                                                   d2 starts with $0.71 left, d3 is refused with $0.52 left
    with pytest.raises(SystemExit, match='sol d3 STOPPED before sending'):
        probe.send(tmp_path / 'run', transport=transport())
    assert (tmp_path / 'run' / 'sol-d2').exists() and not (tmp_path / 'run' / 'sol-d3').exists()


def test_the_first_astra_request_runs_alone_and_a_refusal_there_stops_the_run(tmp_path, monkeypatch):
    monkeypatch.setattr(probe, 'RECORD', tmp_path / 'check-passed.json')
    probe.check()
    calls = []
    good = transport()

    def refusing(provider, request):
        calls.append(request['model'])
        if request['model'] == 'gpt-6-astra':
            error = probe.model.TransportError('400 Bad Request: unsupported parameter')
            error.http_status = 400                 # the transport's not-retried status (budget.NOT_RETRIED)
            raise error
        return good(provider, request)
    with pytest.raises(SystemExit, match='astra d1 STOPPED'):
        probe.send(tmp_path / 'run', transport=refusing)
    assert calls.count('gpt-6-astra') == 1 and calls.count('gpt-6.1-sol') >= 12
