"""Regression between two loop runs, $0 (Alex 2026-10-29: 一类一类改，快速迭代然后测regression). An alarm, not a score: reference
v2 matched by quote (score_week.matches) over answers re-sifted with the current code; every flagged article is then read by hand.

    python3 regress.py <old-tag> <new-tag>
"""
import collections, json, sqlite3, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import bench_v23 as bench, score_week as sw

refs = {}
for name in ('reference-week-v2.json', 'reference-holdout-v2.json'):
    for art in json.loads((HERE.parent / name).read_text())['articles']:
        refs[art['input_id']] = art


def load(tag):
    db = sqlite3.connect(f"file:{HERE / tag / 'answers.sqlite'}?mode=ro", uri=True)
    return {i: bench.sift_answer(json.loads(c) if c else None, d, i, cfg) for i, c, d, cfg in db.execute('select input_id, content, completed, config from answers')}


def states(rec, art):
    if rec is None or rec['sift'] is None:
        return None
    ev = (rec['answer'] or {}).get('evidence', []); kept = {e['id'] for e in rec['sift']['evidence']}
    return {item['id']: (item['weight'], any(e['id'] in kept for e in ev if sw.matches(e['quote'], item)), item['note'])
            for item in art.get('statements', [])}


def totals(recs):
    t = collections.Counter()
    for i, art in refs.items():
        rec = recs.get(i)
        st = states(rec, art)
        if st is None:
            t['failed'] += 1; continue
        t['records kept'] += len(rec['sift']['evidence'])
        t['empty answers'] += 0 if rec['sift']['evidence'] or rec['sift']['candidates'] else 1
        for w, k, _ in st.values():
            t[f'{w} kept'] += k
        if not art.get('statements'):
            t['records on nothing-to-keep articles'] += len(rec['sift']['evidence'])
        for c in rec['sift']['candidates']:
            t[f"questions {c.get('opens_as')}"] += 1
    return t


old_tag, new_tag = sys.argv[1:3]
old, new = load(old_tag), load(new_tag)
to, tn = totals(old), totals(new)
print('measure'.ljust(40), old_tag.rjust(8), new_tag.rjust(8))
for k in sorted(set(to) | set(tn)):
    print(k.ljust(40), str(to.get(k, 0)).rjust(8), str(tn.get(k, 0)).rjust(8))
print('\nreference statements kept before and lost now (regressions first):')
for i, art in refs.items():
    so, sn = states(old.get(i), art), states(new.get(i), art)
    if so is None or sn is None:
        print('  answer failed', i); continue
    for sid, (w, k_old, note) in so.items():
        if k_old and not sn[sid][1] and w in ('core', 'supporting'):
            print(f'  LOST {w:10} {i} | {note[:120]}')
for i, art in refs.items():
    so, sn = states(old.get(i), art), states(new.get(i), art)
    for sid, (w, k_old, note) in (so or {}).items():
        if not k_old and sn and sn[sid][1] and w in ('core', 'supporting'):
            print(f'  GAINED {w:10} {i} | {note[:120]}')
print('\nper-article record counts that moved by 3 or more:')
for i in refs:
    a = len(old[i]['sift']['evidence']) if old.get(i) and old[i]['sift'] else 0
    b = len(new[i]['sift']['evidence']) if new.get(i) and new[i]['sift'] else 0
    if abs(a - b) >= 3:
        print(f"  {a:3} -> {b:3}  {'(reference keeps nothing) ' if not refs[i].get('statements') else ''}{i}")
