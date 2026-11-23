"""D400's code-decided parts on every new-system draw (verdict-rule.json `hard_checks`; D665; DESIGN-1.6.md §1): from the answer-choice
step's three passes, by Stage A's own accounting (`clean-arch/step4-2026-11-10/stage_a/accounting.py`, line 6), with no reader row.

- the favourable end is the same in all three sends of every thesis whose three sends are company figures (measured with at least 3 such);
- the due day is the same in all three sends for at least 90% of the theses whose three sends are ladders (measured with at least 20);
- figure ranges meet end to end: the answer-choice step's own check refuses a ladder whose ranges do not (`ladder_step.check_answer`), so
  every written figure ladder meets it; reported as enforced at the write.

The ladder folder is the one each draw's run record names; every `outcomes.jsonl` read must carry the fingerprint the eligibility check
recorded. A skipped ladder (no question opened) is not measured. A part not measured cannot clear release (D675).

    python3 d400_code_check.py <run root> <eligibility.json>
"""
import json
import sys
from pathlib import Path

sys.path[:0] = ['/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a', str(Path(__file__).resolve().parent)]
import accounting  # noqa: E402
import eligibility as eligibility_tool  # noqa: E402


def check(run_root, eligibility):
    out = {}
    for draw in ('new-1', 'new-2', 'new-3'):
        record = json.loads((Path(run_root) / draw / 'run.json').read_text())
        ladder = record['components'].get('ladder', {})
        if ladder.get('state') != 'completed':
            out[draw] = {'status': f"not measured: the ladder component is {ladder.get('state')!r}"}
            continue
        outcomes = []
        for p in (1, 2, 3):
            path = eligibility_tool.verified(eligibility, run_root, draw, f"{ladder['folder']}/send-{p}/outcomes.jsonl")
            outcomes += [json.loads(line) for line in path.read_text().splitlines()]
        line6 = accounting.account(outcomes, {}, {}, {})['lines'][6]
        out[draw] = {'sends': len(outcomes), 'direction': line6['direction'], 'due day': line6['due day'],
                     'shape differs across sends': line6['shape differs across sends'],
                     'figure ranges meet end to end': 'enforced at the write (ladder_step.check_answer)'}
    states = [v[k][0] for v in out.values() for k in ('direction', 'due day') if k in v] + \
             [accounting.NOT_MEASURED for v in out.values() if 'status' in v]
    status = ('failed' if 'missed' in states else 'not measured' if accounting.NOT_MEASURED in states else 'passed')
    return out, status


if __name__ == '__main__':
    result, status = check(sys.argv[1], json.loads(Path(sys.argv[2]).read_text()))
    print(json.dumps(result, indent=1, default=str))
    print('D400 code parts:', {'passed': 'hard check clear', 'failed': 'release blocked: D400 code parts failed',
                               'not measured': 'release not cleared: D400 code parts not measured'}[status])
