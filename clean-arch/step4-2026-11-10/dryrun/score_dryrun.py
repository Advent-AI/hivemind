"""Score a dry-run reader against the key: planted faults caught (the planted mark reads 'fails'), faults caught under another mark,
and marks failed on the sound items. Usage: python3 score_dryrun.py <reader jsonl> [<seconds>]"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
key = json.loads((HERE / 'dryrun_key.json').read_text())
MARKS = ['Q', 'O', 'R', 'D', 'X', 'F', 'Y', 'G', 'L', 'XR', 'N']
rows = {}
for line in Path(sys.argv[1]).read_text().splitlines():
    line = line.strip()
    if line.startswith('{'):
        r = json.loads(line); rows[str(r['item'])] = r
if sorted(rows, key=int) != sorted(key, key=int):
    raise SystemExit(f'the reader answered items {sorted(rows, key=int)}, not all {len(key)}')
caught = other = missed = 0; false_fail = []
for n, k in sorted(key.items(), key=lambda kv: int(kv[0])):
    r = rows[n]; fails = [m for m in MARKS if r.get(m) == 'fails']
    if k['planted_mark']:
        if r.get(k['planted_mark']) == 'fails': caught += 1; verdict = 'CAUGHT'
        elif fails or r.get('W'): other += 1; verdict = 'caught under another mark'
        else: missed += 1; verdict = 'MISSED'
        print(f"item {n:>2} {k['source']:4} planted {k['planted_mark']:2}: {verdict}; fails {fails}; W={r.get('W')!r:.60}")
    else:
        if fails or r.get('W'): false_fail.append((n, k['source'], fails, r.get('W'), r.get('why')))
planted = sum(1 for k in key.values() if k['planted_mark'])
print(f'planted faults {planted}: caught under their mark {caught}, under another mark {other}, missed {missed}')
print(f'sound items {len(key) - planted}: with a failed mark or a W {len(false_fail)}')
for f in false_fail: print('   sound item', f[0], f[1], 'fails', f[2], '| W:', (f[3] or '')[:80], '| why:', (f[4] or '')[:200])
if len(sys.argv) > 2: print(f'reading time {int(sys.argv[2])} s for {len(key)} ladders: {int(sys.argv[2]) / len(key):.0f} s a ladder')
