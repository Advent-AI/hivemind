"""D400's code-decided parts on every new-system draw (verdict-rule.json `hard_checks`; D665): from the answer-choice step's three passes,
by Stage A's own accounting (`clean-arch/step4-2026-11-10/stage_a/accounting.py`, line 6), with no reader row.

- the favourable end is the same in all three sends of every thesis whose three sends are company figures (measured with at least 3 such);
- the due day is the same in all three sends for at least 90% of the theses whose three sends are ladders (measured with at least 20);
- figure ranges meet end to end: the answer-choice step's own check refuses a ladder whose ranges do not (`ladder_step.check_answer`), so
  every written figure ladder meets it; reported as enforced at the write.

    python3 d400_code_check.py <run root>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, '/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a')
import accounting  # noqa: E402


def check(run_root):
    out = {}
    for draw in ('new-1', 'new-2', 'new-3'):
        record = json.loads((Path(run_root) / draw / 'run.json').read_text())
        folder = Path(run_root) / draw / record['components']['ladder']['folder']
        outcomes = [json.loads(line) for p in (1, 2, 3) for line in (folder / f'send-{p}' / 'outcomes.jsonl').read_text().splitlines()]
        line6 = accounting.account(outcomes, {}, {}, {})['lines'][6]
        out[draw] = {'sends': len(outcomes), 'direction': line6['direction'], 'due day': line6['due day'],
                     'shape differs across sends': line6['shape differs across sends'],
                     'figure ranges meet end to end': 'enforced at the write (ladder_step.check_answer)'}
    passed = all(v['direction'][0] == 'met' and v['due day'][0] == 'met' for v in out.values())
    return out, passed


if __name__ == '__main__':
    result, passed = check(sys.argv[1])
    print(json.dumps(result, indent=1, default=str))
    print('HARD CHECK (D400 code parts):', 'PASS' if passed else 'NOT PASSED (missed or not measured)')
