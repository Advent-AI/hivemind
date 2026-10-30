"""Compare independent readers' classifications of the same cases under the standard.
A reject on the share-price/valuation row and a keep at weight optional are the same outcome in evaluation (no penalty), so the
'outcome' column maps both to 'optional'. Prints per case the readers' outcome, kind, tier and (for questions) open/type, flags
disagreements, and agreement counts.

    python3 compare.py <round> <reader> [<reader> ...]      # files sim-<round>-<reader>.json
"""
import collections, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
rnd, readers = sys.argv[1], sys.argv[2:]
data = {r: json.loads((HERE / f'sim-{rnd}-{r}.json').read_text()) for r in readers}
PRICE = ('股价', '市值', 'share', 'price', 'valuation')


def outcome(s):
    if s is None:
        return 'missing'
    if not s.get('keep'):
        row = str(s.get('reject_row') or '')
        if any(p in row for p in PRICE[:2]) and '别家' not in row:
            return 'optional'
        return 'reject'
    return str(s.get('weight') or 'kept?')


def tier(s):
    return str(s.get('tier')) if s and s.get('keep') else '-'


def kind(s):
    return str(s.get('kind')) if s and s.get('keep') else '-'


rows = collections.Counter()
disagree = []
ids = [s['id'] for s in data[readers[0]]['statements']]
for i in ids:
    by = {r: next((s for s in data[r]['statements'] if s['id'] == i), None) for r in readers}
    o = {r: outcome(s) for r, s in by.items()}
    k = {r: kind(s) for r, s in by.items()}
    t = {r: tier(s) for r, s in by.items()}
    keepish = {r: ('drop' if v == 'reject' else 'keep') for r, v in o.items()}
    rows['statements'] += 1
    rows['keep/drop agree'] += len(set(keepish.values())) == 1
    rows['outcome agree'] += len(set(o.values())) == 1
    kept_all = all(v != 'reject' for v in o.values())
    if kept_all:
        rows['kept by all'] += 1
        rows['kind agree (kept by all)'] += len(set(k.values())) == 1
        rows['tier agree (kept by all)'] += len(set(t.values())) == 1
    if len(set(o.values())) > 1 or (kept_all and (len(set(k.values())) > 1 or len(set(t.values())) > 1)):
        disagree.append((i, o, k, t, {r: (by[r] or {}).get('reason', '')[:110] for r in readers}))
qrows = collections.Counter()
qdis = []
for q in data[readers[0]]['questions']:
    i = q['id']
    by = {r: next((x for x in data[r]['questions'] if x['id'] == i), None) for r in readers}
    op = {r: (('open:' + str(x.get('type')) + '/' + str(x.get('kind'))) if x and x.get('open') else 'no') for r, x in by.items()}
    qrows['questions'] += 1
    qrows['open/no agree'] += len({v.split(':')[0] for v in op.values()}) == 1
    qrows['open+type+kind agree'] += len(set(op.values())) == 1
    if len(set(op.values())) > 1:
        qdis.append((i, op, {r: (by[r] or {}).get('reason', '')[:110] for r in readers}))
print(dict(rows)); print(dict(qrows))
print('\nSTATEMENT DISAGREEMENTS')
for i, o, k, t, why in disagree:
    print(f'{i}: outcome {o} | kind {k} | tier {t}')
    for r, w in why.items():
        print(f'    {r}: {w}')
print('\nQUESTION DISAGREEMENTS')
for i, op, why in qdis:
    print(f'{i}: {op}')
    for r, w in why.items():
        print(f'    {r}: {w}')
