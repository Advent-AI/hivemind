"""Tests of the draws' eligibility (D667: six draws launched within one hour, every send within 72 h of the first launch; D675).

Run: python3 -m pytest docs/research/2026-11-17-product-comparison/stage0/test_eligibility.py
"""
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eligibility  # noqa: E402


def make_run(root, launches, last_calls):
    """Six complete draws; each old draw's store holds one model call at its last-call time; new draws opened no question."""
    for draw in ('new-1', 'new-2', 'new-3', 'old-1', 'old-2', 'old-3'):
        folder = root / draw
        folder.mkdir(parents=True)
        component = 'prod' if draw.startswith('old') else 'judge'
        state = 'completed' if draw.startswith('old') else 'skipped'
        (folder / 'run.json').write_text(json.dumps({'identity': eligibility.expected_identity(root, draw), 'state': 'complete', 'components': {
            component: {'state': state, 'folder': component, 'attempts': [{'folder': component, 'state': 'completed',
                                                                            'started at': launches[draw]}]}}}))
        (folder / component).mkdir()
        conn = sqlite3.connect(folder / component / 'archive.sqlite')
        conn.execute('create table model_calls (call_id integer primary key, created_at text)')
        conn.execute('insert into model_calls (created_at) values (?)', (last_calls[draw],))
        conn.commit()
        conn.close()
        (folder / component / 'views.sqlite').write_bytes(b'')
        (root / 'ledgers').mkdir(exist_ok=True)
        (root / 'ledgers' / f'{draw}.json').write_text(json.dumps({'attempts': 1, 'refused': 0, 'spent': 0.01, 'reserved': 0.0}))
        (root / 'ledgers' / f'{draw}.attempts.jsonl').write_text(json.dumps({'kind': 'llm', 'charged': 0.01, 'at': launches[draw]}) + '\n')


LAUNCH = {d: '2026-11-17T22:36:0%d-0800' % n for n, d in enumerate(('new-1', 'new-2', 'new-3', 'old-1', 'old-2', 'old-3'))}
CALLS = {d: '2026-11-18T18:00:00' for d in LAUNCH}


def test_six_complete_draws_inside_both_windows_are_eligible(tmp_path):
    """D667: launched within one hour, every stored call within 72 h of the first launch."""
    make_run(tmp_path, LAUNCH, CALLS)
    result = eligibility.check(tmp_path)
    assert result['eligible'], result['problems']
    assert result['draws']['old-1']['stores']['archive.sqlite']['sha256']


def test_a_launch_over_an_hour_apart_or_a_call_after_72_hours_is_not_eligible(tmp_path):
    """D667: either window broken leaves no release verdict."""
    make_run(tmp_path / 'a', dict(LAUNCH, **{'old-3': '2026-11-17T23:40:00-0800'}), CALLS)
    assert not eligibility.check(tmp_path / 'a')['eligible']
    make_run(tmp_path / 'b', LAUNCH, dict(CALLS, **{'new-2': '2026-11-17T22:36:00', 'old-2': '2026-11-20T23:00:00'}))
    result = eligibility.check(tmp_path / 'b')
    assert not result['eligible'] and 'old-2' in result['problems'][0]


def test_a_draw_registered_with_other_options_or_a_late_failed_attempt_is_not_eligible(tmp_path):
    """D667: only the registered counted draw counts (here a judge ending 09-19); a failed send, which leaves no archive row but a ledger
    attempt, counts towards the 72 hours."""
    make_run(tmp_path / 'a', LAUNCH, CALLS)
    record = json.loads((tmp_path / 'a' / 'new-1' / 'run.json').read_text())
    record['identity']['options']['judge_end_day'] = '2026-09-19'
    (tmp_path / 'a' / 'new-1' / 'run.json').write_text(json.dumps(record))
    assert not eligibility.check(tmp_path / 'a')['eligible']
    make_run(tmp_path / 'b', LAUNCH, CALLS)
    with open(tmp_path / 'b' / 'ledgers' / 'old-3.attempts.jsonl', 'a') as handle:
        handle.write(json.dumps({'refused': 0.2, 'at': '2026-11-21T09:00:00-0800'}) + '\n')
    ledger = tmp_path / 'b' / 'ledgers' / 'old-3.json'
    ledger.write_text(json.dumps(dict(json.loads(ledger.read_text()), refused=1)))
    result = eligibility.check(tmp_path / 'b')
    assert not result['eligible'] and 'old-3' in result['problems'][0]


def test_an_attempt_log_that_does_not_reconcile_with_its_ledger_leaves_the_timing_unestablished(tmp_path):
    """D667: the timing rests on the complete attempt log; a missing log or one short of the ledger is not eligible (D675)."""
    make_run(tmp_path, LAUNCH, CALLS)
    ledger = tmp_path / 'ledgers' / 'new-2.json'
    ledger.write_text(json.dumps(dict(json.loads(ledger.read_text()), attempts=2)))
    result = eligibility.check(tmp_path)
    assert not result['eligible'] and 'cannot be established' in result['problems'][0]
