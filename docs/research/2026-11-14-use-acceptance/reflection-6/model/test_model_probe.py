"""The effort comparison end to end at $0 (DESIGN.md): the check, the six interleaved arm-draws through the real runner and limit with a
fake transport answering each topic's stored answer, the blind reading, made-up reader rows, and the verdict rule fixed before."""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / 'effort')]
import model_probe as effort_probe  # noqa: E402
import accounting  # noqa: E402
import refcontrol  # noqa: E402

USAGE = {'prompt_tokens': 5000, 'completion_tokens': 1500}


def transport():
    stored = {case['thesis']['description']: row['requests'][-1]['answer_text'] for _, _, case, row in refcontrol.population()}
    seen = []

    def send(provider, request):
        seen.append(request.get('model'))
        user = request['messages'][1]['content']
        text = next(answer for description, answer in stored.items() if json.dumps(description, ensure_ascii=False)[1:-1] in user)
        return {'choices': [{'message': {'content': text}}], 'usage': USAGE}
    send.seen = seen
    return send


@pytest.fixture(scope='module')
def run(tmp_path_factory):
    folder = tmp_path_factory.mktemp('effort')
    original, effort_probe.RECORD = effort_probe.RECORD, folder / 'check-passed.json'
    try:
        effort_probe.check()
        fake = transport()
        effort_probe.send(folder / 'run', transport=fake)
        effort_probe.reading(folder / 'run', folder / 'keys')
    finally:
        effort_probe.RECORD = original
    return folder, fake


def test_each_arm_draw_sends_every_topic_at_its_own_effort(run):
    folder, fake = run
    for arm, draw in effort_probe.ORDER:
        rows = (folder / 'run' / f'{arm}-d{draw}' / 'outcomes.jsonl').read_text().splitlines()
        assert len(rows) == 26 and all(json.loads(row)['case'].startswith(f'{arm}-d{draw}|') for row in rows)
    assert fake.seen.count('gpt-6-luna') >= 78 and fake.seen.count('gpt-6.1-sol') >= 78 and set(fake.seen) == {'gpt-6-luna', 'gpt-6.1-sol'}


def write_rows(folder, fail):
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
            lines.append(json.dumps(row))
        (answers / f'reader-{family}-packet-1.jsonl').write_text('\n'.join(lines) + '\n')


KEY = 'failed sends (agreed hard-line faults plus sends refused twice by code)'


def test_zero_against_zero_is_inconclusive_not_a_close(run):
    folder, _ = run
    write_rows(folder, lambda case: False)
    verdict, report = effort_probe.score(folder / 'run', folder / 'keys')
    assert verdict.startswith('inconclusive') and report['holds'][KEY] == {'luna': 0, 'sol': 0}


def test_equal_failures_close_the_candidate(run):
    folder, _ = run
    topics = ['fortnight:c1/clean-1', 'fortnight:c1/clean-2', 'week-10-06:c1/clean-1']
    write_rows(folder, lambda case: case.split('|', 1)[1] in topics and case.split('|')[0] in ('luna-d1', 'sol-d1'))
    verdict, report = effort_probe.score(folder / 'run', folder / 'keys')
    assert report['holds'][KEY] == {'luna': 3, 'sol': 3} and verdict == 'closes it'


def test_answers_the_high_arm_loses_to_code_refusals_count_as_failures_not_as_an_improvement(run, tmp_path):
    import shutil
    folder, _ = run
    copy = tmp_path / 'copy'
    shutil.copytree(folder, copy)
    topics = ['fortnight:c1/clean-1', 'fortnight:c1/clean-2', 'week-10-06:c1/clean-1', 'week-10-06:c1/clean-2']
    path = copy / 'run' / 'sol-d1' / 'outcomes.jsonl'
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    for row in rows:
        if row['case'].split('|', 1)[1] in topics:
            row.update(status='no ladder: refused', answer=None, view=None, passage=None)
    path.write_text(''.join(json.dumps(row) + '\n' for row in rows))
    write_rows(copy, lambda case: case.startswith('luna-d1|') and case.split('|', 1)[1] in topics)
    verdict, report = effort_probe.score(copy / 'run', copy / 'keys')
    assert report['holds'][KEY] == {'luna': 4, 'sol': 4} and verdict == 'closes it'
    assert all(report['holds']['failed per topic']['sol'][topic] == 1 for topic in topics)


def test_a_medium_arm_faulted_on_four_topics_where_high_is_clean_moves_the_candidate(run):
    folder, _ = run
    topics = ['fortnight:c1/clean-1', 'fortnight:c1/clean-2', 'week-10-06:c1/clean-1', 'week-10-06:c1/clean-2']
    write_rows(folder, lambda case: case.startswith('luna-d1|') and case.split('|', 1)[1] in topics)
    verdict, report = effort_probe.score(folder / 'run', folder / 'keys')
    assert report['holds'][KEY] == {'luna': 4, 'sol': 0} and verdict == 'moves the candidate'


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
        effort_probe.score(folder / 'run', folder / 'keys')


def test_both_families_failing_a_sound_control_voids_the_reading_as_too_harsh(run):
    folder, _ = run
    write_rows(folder, lambda case: case == 'control|sound-clean-5')
    with pytest.raises(SystemExit, match='VOID: both families fail a hard line on the sound control\\|sound-clean-5'):
        effort_probe.score(folder / 'run', folder / 'keys')


def test_the_check_refuses_a_high_request_that_differs_in_more_than_its_effort(tmp_path, monkeypatch):
    real = effort_probe.built

    def built(case, setting, rl):
        request = real(case, setting, rl)
        if setting.model == 'gpt-6.1-sol':
            request['max_completion_tokens'] = request['max_completion_tokens'] + 1
        return request
    monkeypatch.setattr(effort_probe, 'built', built)
    monkeypatch.setattr(effort_probe, 'RECORD', tmp_path / 'check-passed.json')
    with pytest.raises(SystemExit, match='CHECK FAILED'):
        effort_probe.check()
    assert not (tmp_path / 'check-passed.json').exists()


def test_the_first_sol_request_runs_alone_and_a_refusal_there_stops_the_run(tmp_path, monkeypatch):
    monkeypatch.setattr(effort_probe, 'RECORD', tmp_path / 'check-passed.json')
    effort_probe.check()
    calls = []
    good = transport()

    def refusing(provider, request):
        calls.append(request['model'])
        if request['model'] == 'gpt-6.1-sol':
            error = effort_probe.model.TransportError('400 Bad Request: unsupported parameter')
            error.http_status = 400                 # the transport's not-retried status (budget.NOT_RETRIED)
            raise error
        return good(provider, request)
    with pytest.raises(SystemExit, match='sol d1 STOPPED'):
        effort_probe.send(tmp_path / 'run', transport=refusing)
    assert calls.count('gpt-6.1-sol') == 1 and calls.count('gpt-6-luna') >= 26
