"""The astra-with-A2 probe at $0 (council round 29): the check, the four arm-draws through the real runner and limit with a fake
transport, both blind readings built from the run, made-up reader rows, and every condition of the verdict fixed before."""
import json
import shutil
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / 'astra'), str(HERE.parent / 'due-day'), str(HERE.parent / 'model'), str(HERE.parent / 'effort')]
import a2_probe as probe  # noqa: E402
import accounting  # noqa: E402
import refcontrol  # noqa: E402

USAGE = {'prompt_tokens': 2000, 'completion_tokens': 400}


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
    folder = tmp_path_factory.mktemp('a2')
    original, probe.RECORD = probe.RECORD, folder / 'check-passed.json'
    try:
        probe.check()
        fake = transport()
        probe.send(folder / 'run', transport=fake)
        yield folder, fake
    finally:
        probe.RECORD = original


def test_each_arm_sends_its_own_request_and_a2_differs_only_by_its_edits(run):
    _, fake = run
    a2_text = probe.a2_texts()['system']
    frozen_text = probe.FROZEN_TEXTS()['system']
    assert fake.systems.count(frozen_text) >= 20 and fake.systems.count(a2_text) >= 20 and set(fake.systems) == {frozen_text, a2_text}


def copy_with(run, tmp_path, changes):
    """A copy of the run with the given sends rewritten: `decline`, `lost`, or a dict of fields."""
    folder, _ = run
    copy = tmp_path / 'run'
    shutil.copytree(folder / 'run', copy)
    for send, change in changes.items():
        path = copy / send.split('|')[0] / 'outcomes.jsonl'
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        for row in rows:
            if row['case'] == send:
                if change == 'decline':
                    row.update(status='no ladder', answer=None, view=None, passage=None, reason='made up: several parts, none the main one')
                elif change == 'lost':
                    row.update(status='no ladder: refused', answer=None, view=None, passage=None)
        path.write_text(''.join(json.dumps(row) + '\n' for row in rows))
    return copy


def gate_rows(copy, keys, fail=(), harm=(), harm_one_reader=()):
    """Both families' gate rows: every hard line holds except `fail` sends (L for a ladder, N for a decline); every listed part is
    `part` except the sends in `harm` (both families mark their first part already_judged) or `harm_one_reader` (Codex only)."""
    key = json.loads((keys / 'key.json').read_text())
    expected = json.loads((keys / 'controls-expected.json').read_text())
    outcomes = {row['case']: row for row in map(json.loads, (copy / 'gate-reading' / 'send-1' / 'outcomes.jsonl').read_text().splitlines())}
    answers = copy / 'gate-reading' / 'readers-answers'
    answers.mkdir(exist_ok=True)
    for family in ('codex', 'claude'):
        lines = []
        for item, (send, _) in key.items():
            outcome = outcomes[send]
            kind = accounting.kind_of(outcome)
            applicable = accounting.marks_that_apply(kind)
            row = {'item': int(item), 'W': '', 'why': 'made up for the test'}
            for mark in accounting.ALL_MARKS:
                row[mark] = ('not_assessable' if kind in ('company figure', 'theme figure') else 'n/a') if mark == 'G' \
                    else 'holds' if mark in applicable else 'n/a'
            listed = 0 if kind == 'refusal' else len(outcome['answer']['ladder']['not_judged'])
            row['B'] = ['not_a_bet'] * listed
            row['H'] = ['part'] * listed
            if listed and (send in harm or (family == 'codex' and send in harm_one_reader)):
                row['H'][0] = 'already_judged'
            for mark, value in expected.get(send, {}).items():
                if mark != 'all':
                    row[mark] = value
            if send in fail:
                row['N' if kind == 'refusal' else 'L'] = 'fails'
            lines.append(json.dumps(row))
        (answers / f'reader-{family}-packet-1.jsonl').write_text('\n'.join(lines) + '\n')


def review_rows(copy, keys, flags=()):
    key = json.loads((keys / 'key.json').read_text())
    files = []
    for reader in ('codex', 'claude'):
        lines = []
        for item, send in key.items():
            bad = send in flags or (send in probe.dueday_probe.CONTROLS and probe.dueday_probe.CONTROLS[send][2] == 'material')
            lines.append(json.dumps({'item': int(item), 'verdict': 'defect' if bad else 'sound', 'class': 'other' if bad else None,
                                     'material': bad, 'evidence': '', 'why': f'made up by the {reader} reviewer'}))
        path = copy / f'review-{reader}.jsonl'
        path.write_text('\n'.join(lines) + '\n')
        files.append(path)
    return files


TARGET_FAILS = tuple(f'frozen-d{d}|{t}' for t in probe.TARGETS for d in (1, 2))      # frozen fails both targets in both draws


def verdict(run, tmp_path, changes=None, fail=TARGET_FAILS, harm=(), harm_one_reader=(), flags=()):
    copy = copy_with(run, tmp_path, changes or {})
    gate_keys, review_keys = tmp_path / 'gate-keys', tmp_path / 'review-keys'
    probe.gate_reading(copy, gate_keys)
    gate_rows(copy, gate_keys, fail, harm, harm_one_reader)
    probe.review_reading(copy, review_keys)
    return probe.final(copy, gate_keys, review_keys, review_rows(copy, review_keys, flags))


def first_ladder(run, arm):
    folder, _ = run
    rows = [json.loads(line) for draw in (1, 2) for line in (folder / 'run' / f'{arm}-d{draw}' / 'outcomes.jsonl').read_text().splitlines()]
    return next(row['case'] for row in rows if row['status'] == 'ladder' and row['answer']['ladder']['not_judged'])


def test_two_fewer_failures_with_every_guard_kept_moves(run, tmp_path):
    assert verdict(run, tmp_path).startswith('moves')


def test_no_fewer_failures_closes(run, tmp_path):
    assert verdict(run, tmp_path, fail=()) == 'closes'


def test_an_answer_code_refuses_twice_counts_as_a_failure(run, tmp_path):
    one = (f'frozen-d1|{probe.TARGETS[0]}',)
    assert verdict(run, tmp_path, changes={f'a2-d1|{probe.TARGETS[1]}': 'lost'}, fail=one) == 'closes'


def test_a_justified_decline_lost_in_a2_closes(run, tmp_path):
    assert verdict(run, tmp_path, changes={f'a2-d2|{probe.JUSTIFIED[0]}': 'lost'}) == 'closes'


def test_harmful_listings_beyond_one_more_than_frozen_close(run, tmp_path):
    send = first_ladder(run, 'a2')
    other = send.replace('-d1|', '-d2|') if '-d1|' in send else send.replace('-d2|', '-d1|')
    assert verdict(run, tmp_path, harm=(send, other)) == 'closes'


def test_a_replacement_question_flagged_by_both_reviewers_closes(run, tmp_path):
    topic = probe.DISPUTED[0]
    changes = {f'frozen-d1|{topic}': 'decline'}
    assert verdict(run, tmp_path, changes=changes, flags=(f'a2-d1|{topic}',)) == 'closes'


def test_countings_that_disagree_are_inconclusive(run, tmp_path):
    send = first_ladder(run, 'a2')
    other = send.replace('-d1|', '-d2|') if '-d1|' in send else send.replace('-d2|', '-d1|')
    assert verdict(run, tmp_path, harm_one_reader=(send, other)).startswith('inconclusive')


def test_a_topic_where_a2_fails_more_than_frozen_blocks_a_move(run, tmp_path):
    clean = f'a2-d1|{probe.RECOVERED[0]}'
    result = verdict(run, tmp_path, fail=TARGET_FAILS + (clean,))
    assert not result.startswith('moves')


def test_a_missed_gate_control_voids_the_reading(run, tmp_path):
    copy = copy_with(run, tmp_path, {})
    gate_keys, review_keys = tmp_path / 'gate-keys', tmp_path / 'review-keys'
    probe.gate_reading(copy, gate_keys)
    gate_rows(copy, gate_keys, TARGET_FAILS)
    path = copy / 'gate-reading' / 'readers-answers' / 'reader-claude-packet-1.jsonl'
    key = json.loads((gate_keys / 'key.json').read_text())
    item = next(int(item) for item, (send, _) in key.items() if send == 'control|unlisted-part')
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    path.write_text('\n'.join(json.dumps(dict(row, L='holds') if row['item'] == item else row) for row in rows) + '\n')
    probe.review_reading(copy, review_keys)
    with pytest.raises(SystemExit, match='VOID: a family missed the planted control\\|unlisted-part'):
        probe.final(copy, gate_keys, review_keys, review_rows(copy, review_keys))


def test_a_draw_whose_estimate_does_not_fit_is_not_started(tmp_path, monkeypatch):
    monkeypatch.setattr(probe, 'RECORD', tmp_path / 'check-passed.json')
    monkeypatch.setattr(probe, 'CAP_USD', 2.6)        # four draws of about $0.40 and a $1.14 reserve: the fourth does not fit
    probe.check()
    with pytest.raises(SystemExit, match='a2 d2 STOPPED before sending'):
        probe.send(tmp_path / 'run', transport=transport())
    assert (tmp_path / 'run' / 'frozen-d2').exists() and not (tmp_path / 'run' / 'a2-d2').exists()


def test_one_fewer_failure_is_inconclusive_not_a_move(run, tmp_path):
    target = probe.TARGETS[0]
    fail = (f'frozen-d1|{target}', f'frozen-d2|{target}', f'a2-d1|{target}')
    assert verdict(run, tmp_path, fail=fail) == 'inconclusive'


def test_a_family_that_misses_the_planted_already_judged_listing_voids_the_reading(run, tmp_path):
    copy = copy_with(run, tmp_path, {})
    gate_keys, review_keys = tmp_path / 'gate-keys', tmp_path / 'review-keys'
    probe.gate_reading(copy, gate_keys)
    gate_rows(copy, gate_keys, TARGET_FAILS)
    path = copy / 'gate-reading' / 'readers-answers' / 'reader-codex-packet-1.jsonl'
    key = json.loads((gate_keys / 'key.json').read_text())
    items = [int(item) for item, (send, _) in key.items() if send == 'control|listings']
    assert len(items) == 1, 'the planted listing control is in the packet once'
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    path.write_text('\n'.join(json.dumps(dict(row, H=['part'] * 4) if row['item'] == items[0] else row) for row in rows) + '\n')
    probe.review_reading(copy, review_keys)
    with pytest.raises(SystemExit, match='VOID: a family missed the planted control\\|listings'):
        probe.final(copy, gate_keys, review_keys, review_rows(copy, review_keys))


def test_the_check_refuses_an_a2_request_with_an_unrecorded_change(tmp_path, monkeypatch):
    real = probe.built

    def built(case, arm, rl):
        request = real(case, arm, rl)
        if arm == 'a2':
            request['max_completion_tokens'] = request['max_completion_tokens'] + 1
        return request
    monkeypatch.setattr(probe, 'built', built)
    monkeypatch.setattr(probe, 'RECORD', tmp_path / 'check-passed.json')
    with pytest.raises(SystemExit, match='CHECK FAILED.*more than the recorded edits'):
        probe.check()
    assert not (tmp_path / 'check-passed.json').exists()


def test_one_review_file_given_twice_is_not_scored(run, tmp_path):
    copy = copy_with(run, tmp_path, {})
    gate_keys, review_keys = tmp_path / 'gate-keys', tmp_path / 'review-keys'
    probe.gate_reading(copy, gate_keys)
    gate_rows(copy, gate_keys, TARGET_FAILS)
    probe.review_reading(copy, review_keys)
    files = review_rows(copy, review_keys)
    with pytest.raises(SystemExit, match='NOT SCORED: the review files are not two distinct readings'):
        probe.final(copy, gate_keys, review_keys, [files[0], files[0]])
