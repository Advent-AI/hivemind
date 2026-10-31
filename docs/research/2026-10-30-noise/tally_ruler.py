"""Tally a blind ruler folder read by two readers (A: Codex verdicts-A-<p>.jsonl, B: Claude verdicts-B-<p>.jsonl) against its key: agreement,
and per group (kept_rejected, control_kept, control_dropped) the readers' weights against the gold's; plus the unlisted sample (U ids).
    python3 tally_ruler.py blind-v68a-ruler"""
import collections, json, sys
from pathlib import Path
F = Path(__file__).resolve().parent / sys.argv[1]
def read(prefix):
    out = {}
    for p in sorted(F.glob(f'verdicts-{prefix}-*.jsonl')):
        for line in p.read_text().splitlines():
            if line.strip().startswith('{'):
                o = json.loads(line); out[o['id']] = o
    return out
A, B = read('A'), read('B')
key = json.loads((F / 'key.json').read_text())
kk = lambda w: 'keep' if w in ('core', 'supporting') else w
agree = collections.Counter(); byg = collections.defaultdict(collections.Counter)
for sid, k in key.items():
    a, b = A.get(sid, {}).get('weight'), B.get(sid, {}).get('weight')
    if a is None or b is None: continue
    agree[kk(a) == kk(b)] += 1
    verdict = kk(a) if kk(a) == kk(b) else 'split'
    byg[k['group']][verdict] += 1
print('S entries with both readers:', sum(agree.values()), '| agree', agree[True], 'split', agree[False])
for g, c in byg.items(): print(f'  {g}: {dict(c)} (n={sum(c.values())})')
# kept_rejected entries by gold row where both readers keep (candidates for a gold error or an unsettled rule)
rows = collections.Counter(); draws = 0
for sid, k in key.items():
    if k['group'] != 'kept_rejected': continue
    a, b = A.get(sid, {}).get('weight'), B.get(sid, {}).get('weight')
    if a and b and kk(a) == 'keep' and kk(b) == 'keep':
        rows[k['gold_reason'][:40]] += 1
print('kept_rejected both readers keep, by gold row:', rows.most_common(8))
ukey_path = F / 'unlisted.key.json'
if ukey_path.exists():
    uk = json.loads(ukey_path.read_text())
    ua = {o['id']: o for p in F.glob('verdicts-A-unlisted.jsonl') for line in p.read_text().splitlines() if line.strip().startswith('{') for o in [json.loads(line)]}
    ub = {o['id']: o for p in F.glob('verdicts-B-unlisted.jsonl') for line in p.read_text().splitlines() if line.strip().startswith('{') for o in [json.loads(line)]}
    c = collections.Counter()
    for sid in uk:
        a, b = ua.get(sid, {}).get('weight'), ub.get(sid, {}).get('weight')
        if a and b: c[(kk(a), kk(b))] += 1
    print('unlisted sample (readerA, readerB):', dict(c))
