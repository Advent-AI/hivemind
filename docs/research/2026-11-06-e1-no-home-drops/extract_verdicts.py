"""E1 step 1 ($0): every production miss the benchmark's independent readers put down as written, then dropped by a code check, from the
three same-day production window draws and the three test-article draws (sealed worktree, D378)."""
import json
from pathlib import Path

RESULTS = Path('/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-06-architecture-benchmark/results')


def load(path):
    text = path.read_text()
    return json.loads(text[text.index('['):text.rindex(']') + 1])


rows = [dict(r, set='window') for p in sorted(RESULTS.glob('miss-window-control-*.out')) for r in load(p)]
rows += [dict(r, set='test') for r in load(RESULTS / 'miss-test-control.out')]
dropped = [r for r in rows if r.get('verdict') == 'DROPPED_BY_CHECK']
json.dump(dropped, open(Path(__file__).resolve().parent / 'dropped-verdicts.json', 'w'), ensure_ascii=False, indent=1)
print(len(rows), 'missed draws read;', len(dropped), 'dropped by a check;', len({(r['set'], r['matter']) for r in dropped}), 'matters')
