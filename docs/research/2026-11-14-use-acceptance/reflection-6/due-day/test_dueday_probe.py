"""The due-day probe at $0 (council round 20): the check, the four arm-draws through the real runner and limit with a fake transport,
the v2 requests carrying the changed clause and nothing else, and the verdict fixed before."""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / 'astra'), str(HERE.parent / 'model'), str(HERE.parent / 'effort')]
import dueday_probe as probe  # noqa: E402
import refcontrol  # noqa: E402

USAGE = {'prompt_tokens': 2000, 'completion_tokens': 400}      # about astra's measured $0.04 a send


def transport():
    stored = {case['thesis']['description']: row['requests'][-1]['answer_text'] for _, _, case, row in refcontrol.population()}
    systems = []

    def send(provider, request):
        systems.append(request['messages'][0]['content'])
        user = request['messages'][1]['content']
        text = next(answer for description, answer in stored.items() if json.dumps(description, ensure_ascii=False)[1:-1] in user)
        return {'choices': [{'message': {'content': text}}], 'usage': USAGE}
    send.systems = systems
    return send


@pytest.fixture(scope='module')
def run(tmp_path_factory):
    folder = tmp_path_factory.mktemp('dueday')
    original, probe.RECORD = probe.RECORD, folder / 'check-passed.json'
    try:
        probe.check()
        fake = transport()
        probe.send(folder / 'run', transport=fake)
        yield folder, fake
    finally:
        probe.RECORD = original


def test_each_arm_sends_its_own_system_text_and_nothing_else_differs(run):
    _, fake = run
    frozen = [text for text in fake.systems if probe.FROZEN_CLAUSE in text]
    changed = [text for text in fake.systems if probe.V2_CLAUSE in text]
    assert len(frozen) >= 18 and len(changed) >= 18 and len(frozen) + len(changed) == len(fake.systems)
    assert {text.replace(probe.V2_CLAUSE, probe.FROZEN_CLAUSE) for text in changed} == set(frozen)


def test_the_check_refuses_a_v2_text_that_changes_more_than_the_clause(tmp_path, monkeypatch):
    edited = tmp_path / 'v2.txt'
    edited.write_text(probe.V2_SYSTEM.read_text().replace('Write in English.', 'Write in plain English.'))
    monkeypatch.setattr(probe, 'V2_SYSTEM', edited)
    monkeypatch.setattr(probe, 'RECORD', tmp_path / 'check-passed.json')
    with pytest.raises(SystemExit, match='CHECK FAILED'):
        probe.check()


def rewrite(folder, changes):
    """Copy the run and set the stored due day (or a decline) of the arm-draw and topic given."""
    import shutil
    copy = folder.parent / (folder.name + '-copy')
    shutil.rmtree(copy, ignore_errors=True)
    shutil.copytree(folder / 'run', copy)
    for (arm_draw, topic), day in changes.items():
        path = copy / arm_draw / 'outcomes.jsonl'
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        for row in rows:
            if row['case'] == f'{arm_draw}|{topic}':
                if day == 'decline':
                    row.update(status='no ladder', answer=None, view=None, passage=None, reason='made up')
                else:
                    row['answer']['ladder']['due_day'] = day
                    row['view']['due_day'] = day
        path.write_text(''.join(json.dumps(row) + '\n' for row in rows))
    return copy


HF, HF_WEEK = 'fortnight:c1/clean-6', 'week-10-06:c1/clean-5'
FIXED = {('frozen-d1', HF): '2027-02-28', ('v2-d1', HF): '2028-03-24', ('v2-d2', HF): '2028-03-24',
         ('v2-d1', HF_WEEK): '2027-06-30', ('v2-d2', HF_WEEK): '2027-06-30'}


def reviews(copy, tmp_path, flags=(), one_reader_flags=(), damage=None):
    """Two made-up reviewers over the copy's packet: every send sound, except those given (both reviewers, or the first only); each
    control as expected. `damage(reader, lines)` may spoil a reviewer's file."""
    keys = tmp_path / 'keys'
    probe.reading(copy, keys)
    key = json.loads((keys / 'key.json').read_text())
    files = []
    for reader in probe.READERS:
        lines = []
        for item, send in key.items():
            bad = send in flags or (reader == 'codex' and send in one_reader_flags) or \
                (send in probe.CONTROLS and probe.CONTROLS[send][2] == 'material')
            lines.append({'item': int(item), 'verdict': 'defect' if bad else 'sound', 'class': 'other' if bad else None,
                          'material': bad, 'evidence': '', 'why': ''})
        if damage:
            lines = damage(reader, lines)
        path = tmp_path / f'review-{reader}.jsonl'
        path.write_text('\n'.join(json.dumps(line) for line in lines) + '\n')
        files.append(path)
    return keys, files


def verdict_of(run, tmp_path, changes, flags=(), one_reader_flags=(), damage=None, files_used=None):
    folder, _ = run
    copy = rewrite(folder, changes)
    keys, files = reviews(copy, tmp_path, flags, one_reader_flags, damage)
    return probe.final(copy, keys, files if files_used is None else files[:files_used])


def test_a_fixed_completion_with_every_control_kept_and_sound_reviews_moves(run, tmp_path):
    assert verdict_of(run, tmp_path, FIXED) == 'moves'


def test_a_completion_still_at_the_annual_filing_closes(run, tmp_path):
    assert verdict_of(run, tmp_path, FIXED | {('v2-d2', HF): '2027-02-28'}) == 'closes'


def test_an_amount_control_whose_stored_day_moves_closes(run, tmp_path):
    assert verdict_of(run, tmp_path, FIXED | {('v2-d1', 'fortnight:c1/clean-2'): '2027-07-31'}) == 'closes'


def test_a_new_decline_both_reviewers_call_unjustified_closes(run, tmp_path):
    changes = FIXED | {('v2-d1', 'week-10-06:c1/clean-11'): 'decline'}
    assert verdict_of(run, tmp_path, changes, flags=('v2-d1|week-10-06:c1/clean-11',)) == 'closes'


def test_a_material_fault_in_a_fixed_completion_question_that_one_reviewer_sees_is_inconclusive(run, tmp_path):
    assert verdict_of(run, tmp_path, FIXED, one_reader_flags=('v2-d1|' + HF,)).startswith('inconclusive')


def test_no_annual_filing_date_in_the_frozen_arm_is_inconclusive(run, tmp_path):
    changes = {key: day for key, day in FIXED.items() if key[0] != 'frozen-d1'}
    assert verdict_of(run, tmp_path, changes).startswith('inconclusive')


def test_a_flagged_fixed_completion_question_closes_even_when_the_frozen_ones_are_flagged_too(run, tmp_path):
    flags = ('frozen-d1|' + HF, 'frozen-d2|' + HF, 'v2-d1|' + HF)          # the topic count alone would pass: 1 against 2
    assert verdict_of(run, tmp_path, FIXED | {('frozen-d2', HF): '2027-02-28'}, flags=flags) == 'closes'


def test_an_unjustified_new_decline_closes_even_where_the_frozen_ladder_was_flagged(run, tmp_path):
    topic = 'week-10-06:c1/clean-11'
    flags = ('frozen-d1|' + topic, 'v2-d1|' + topic)                       # the topic count alone would pass: 1 against 1
    assert verdict_of(run, tmp_path, FIXED | {('v2-d1', topic): 'decline'}, flags=flags) == 'closes'


def test_a_new_material_fault_on_another_topic_closes(run, tmp_path):
    assert verdict_of(run, tmp_path, FIXED, flags=('v2-d1|fortnight:c1/clean-2',)) == 'closes'


def test_a_reviewer_missing_a_row_is_not_scored(run, tmp_path):
    with pytest.raises(SystemExit, match='NOT SCORED: .* does not hold each of the 40 items once'):
        verdict_of(run, tmp_path, FIXED, damage=lambda reader, lines: lines[1:] if reader == 'claude' else lines)


def test_one_reviewer_alone_is_not_scored(run, tmp_path):
    with pytest.raises(SystemExit, match='NOT SCORED: 2 review files are needed, got 1'):
        verdict_of(run, tmp_path, FIXED, files_used=1)


def test_a_malformed_verdict_is_not_scored(run, tmp_path):
    def spoil(reader, lines):
        return [dict(line, verdict='maybe') if line['item'] == 3 else line for line in lines] if reader == 'codex' else lines
    with pytest.raises(SystemExit, match='NOT SCORED: .* item 3 is not a valid row'):
        verdict_of(run, tmp_path, FIXED, damage=spoil)


def test_a_reviewer_who_misses_a_planted_defect_voids_the_reading(run, tmp_path):
    def miss(reader, lines):
        key = json.loads((tmp_path / 'keys' / 'key.json').read_text())
        target = next(int(item) for item, send in key.items() if send == 'control|completion-at-filing')
        return [dict(line, verdict='sound', material=False, **{'class': None}) if line['item'] == target else line for line in lines] \
            if reader == 'claude' else lines
    with pytest.raises(SystemExit, match='VOID: .* misses the control\\|completion-at-filing'):
        verdict_of(run, tmp_path, FIXED, damage=miss)


def test_the_packet_shows_the_rendered_question_and_the_four_controls(run, tmp_path):
    folder, _ = run
    copy = rewrite(folder, FIXED)
    probe.reading(copy, tmp_path / 'keys')
    items = json.loads((copy / 'review' / 'packet.json').read_text())
    assert len(items) == 40 and all('opens_as' in item['thesis'] and 'fiscal_year_note' in item for item in items)
    shown = [item['ladder_as_the_judge_is_shown_it'] for item in items]
    assert sum('rungs' in ladder for ladder in shown) >= 30 and sum('no_ladder' in ladder for ladder in shown) >= 2


def test_an_answer_code_refuses_twice_is_lost_kept_out_of_the_review_and_closes(tmp_path, monkeypatch):
    """The real runner on a v2 answer whose due day is not a date, twice: `no ladder: refused`, counted as lost, not read."""
    monkeypatch.setattr(probe, 'RECORD', tmp_path / 'check-passed.json')
    probe.check()
    good = transport()

    def breaking(provider, request):
        answer = good(provider, request)
        if probe.V2_CLAUSE in request['messages'][0]['content'] and 'Ministry of Industry and Information Technology' in request['messages'][1]['content']:
            text = json.loads(answer['choices'][0]['message']['content'])
            text['ladder']['due_day'] = '2027-02-30'
            answer = dict(answer, choices=[{'message': {'content': json.dumps(text)}}])
        return answer
    probe.send(tmp_path / 'run', transport=breaking)
    row = next(json.loads(line) for line in (tmp_path / 'run' / 'v2-d1' / 'outcomes.jsonl').read_text().splitlines()
               if json.loads(line)['case'] == 'v2-d1|fortnight:c1/clean-7')
    assert row['status'] == 'no ladder: refused' and len(row['requests']) == 2
    copy = rewrite(tmp_path, FIXED)
    keys, files = reviews(copy, tmp_path)
    key = json.loads((keys / 'key.json').read_text())
    assert len(key) == 38 and not any(send.endswith('fortnight:c1/clean-7') and send.startswith('v2-') for send in key.values())
    assert probe.final(copy, keys, files) == 'closes'
