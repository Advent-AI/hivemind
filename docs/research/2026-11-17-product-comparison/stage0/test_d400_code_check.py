"""Tests of D400's code-decided check (DESIGN-1.6.md §0, §1; D675): which release line it prints.

Run: python3 -m pytest docs/research/2026-11-17-product-comparison/stage0/test_d400_code_check.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d400_code_check  # noqa: E402
import eligibility  # noqa: E402


def outcome(case, pass_number, favourable, due):
    return {'case': case, 'pass': pass_number, 'status': 'ladder', 'view': {'kind': 'asset', 'due_day': due},
            'answer': {'ladder': {'figure': {'favourable_end': favourable}, 'not_judged': []}}}


def make_draws(root, new1_favourable):
    """new-1: three company-figure theses over three passes, the first changing its favourable end when `new1_favourable` differs;
    new-2 and new-3: a skipped ladder (no question opened)."""
    fingerprints = {}
    for draw in ('new-1', 'new-2', 'new-3'):
        folder = root / draw
        folder.mkdir(parents=True)
        if draw == 'new-1':
            (folder / 'run.json').write_text(json.dumps({'components': {'ladder': {'state': 'completed', 'folder': 'ladder'}}}))
            for p in (1, 2, 3):
                (folder / 'ladder' / f'send-{p}').mkdir(parents=True)
                rows = [outcome(f'c{k}', p, new1_favourable[p - 1] if k == 0 else 'high', '2027-01-31') for k in range(3)]
                (folder / 'ladder' / f'send-{p}' / 'outcomes.jsonl').write_text('\n'.join(json.dumps(r) for r in rows))
            fingerprints[draw] = {'inputs': {f'ladder/send-{p}/outcomes.jsonl': eligibility.sha256(folder / 'ladder' / f'send-{p}' / 'outcomes.jsonl')
                                             for p in (1, 2, 3)}}
        else:
            (folder / 'run.json').write_text(json.dumps({'components': {'ladder': {'state': 'skipped'}}}))
            fingerprints[draw] = {'inputs': {}}
    return {'draws': fingerprints}


def test_a_missed_part_blocks_release_ahead_of_a_part_not_measured(tmp_path):
    """D675: a failed hard check prints "release blocked"; one only not measured prints "release not cleared"."""
    _, status = d400_code_check.check(tmp_path / 'a', make_draws(tmp_path / 'a', ['high', 'low', 'high']))
    assert status == 'failed'                         # new-1's favourable end moved: missed, though new-2 and new-3 are not measured
    _, status = d400_code_check.check(tmp_path / 'b', make_draws(tmp_path / 'b', ['high', 'high', 'high']))
    assert status == 'not measured'                   # new-1's due-day line has 3 theses of 20 needed, and two ladders were skipped
