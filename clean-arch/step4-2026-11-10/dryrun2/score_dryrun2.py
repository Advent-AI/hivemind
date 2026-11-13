"""Score a reader of the second dry run. Usage: python3 score_dryrun2.py a|b <reader jsonl> [<seconds>]"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
key = json.loads((HERE / 'dryrun2_key.json').read_text())[sys.argv[1]]
rows = [json.loads(l) for l in Path(sys.argv[2]).read_text().splitlines() if l.strip().startswith('{')]
MARKS = ['Q', 'O', 'R', 'D', 'X', 'F', 'Y', 'G', 'N']
if sys.argv[1] == 'a':
    got = {f"{r['thesis_id'].split()[0]} {r['ladder']}": r for r in rows}
    if set(got) != set(key): raise SystemExit(f'answered {len(got)} ladders, key has {len(key)}; differing: {sorted(set(got) ^ set(key))[:6]}')
    caught = other = missed = 0; flagged = []
    for name, k in key.items():
        r = got[name]; fails = [m for m in MARKS if r.get(m) == 'fails']
        if k['planted_mark']:
            if r.get(k['planted_mark']) == 'fails': caught += 1
            elif fails or r.get('W'): other += 1; print('  other mark:', name, k, fails)
            else: missed += 1; print('  MISSED:', name, k)
        elif fails or r.get('W'):
            flagged.append((name, k['arm'], fails, (r.get('why') or '')[:170]))
    planted = sum(1 for k in key.values() if k['planted_mark'])
    print(f'A: planted {planted}: caught under their mark {caught}, under another {other}, missed {missed}; unplanted {len(key) - planted}: flagged {len(flagged)}')
    for f in flagged: print('   flagged', f)
else:
    got = {str(r['judgement']): r for r in rows}
    if set(got) != set(key): raise SystemExit(f'answered {len(got)} judgements, key has {len(key)}')
    caught = sum(1 for n, k in key.items() if k['planted'] and got[n]['verdict'] == 'UNSUPPORTED')
    planted = sum(1 for k in key.values() if k['planted'])
    rest = [got[n]['verdict'] for n, k in key.items() if not k['planted']]
    print(f'B: planted wrong rungs {planted}: marked UNSUPPORTED {caught}; stored judgements {len(rest)}: ' + ', '.join(f'{v} {rest.count(v)}' for v in sorted(set(rest))))
    for n, k in key.items():
        r = got[n]
        if (k['planted'] and r['verdict'] != 'UNSUPPORTED') or (not k['planted'] and r['verdict'] != 'SUPPORTED') or r.get('arithmetic') == 'wrong':
            print(f"   judgement {n} {k['view']} {k['day']} planted={k['planted']} verdict={r['verdict']} arithmetic={r.get('arithmetic')} | {(r.get('why') or '')[:200]}")
if len(sys.argv) > 3: print(f'reading time {int(sys.argv[3])} s for {len(key)}: {int(sys.argv[3]) / len(key):.0f} s each')
