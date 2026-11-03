"""$0: the code half of this morning's ruler (reference v2, quote match of bench_score.structure) over role-v22 (luna-1..3),
role-v23 draw 1 and the loop's v29, all re-sifted with the current code."""
import collections, json, sqlite3, sys
from pathlib import Path
A = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard')
sys.path.insert(0, str(A))
import bench_v23 as bench
import score_week as sw
base = json.loads((bench.RUN / 'sifted.json').read_text())
draws = {d: base[d] for d in ('luna-1', 'luna-2', 'luna-3', 'v23-1')}
db = sqlite3.connect(f"file:{A / 'loop-2026-10-29/v29/answers.sqlite'}?mode=ro", uri=True)
draws['v29'] = {i: bench.sift_answer(json.loads(c) if c else None, d, i, cfg) for i, c, d, cfg in db.execute('select input_id, content, completed, config from answers')}
refs = {}
for name, label in (('reference-week-v2.json', 'week'), ('reference-holdout-v2.json', 'holdout')):
    for art in json.loads((A / name).read_text())['articles']:
        refs[art['input_id']] = dict(art, set=label)
out = {}
for draw, recs in draws.items():
    t = collections.Counter()
    for input_id, art in refs.items():
        rec = recs.get(input_id)
        if rec is None or rec['sift'] is None:
            t['failed'] += 1; continue
        ev = (rec['answer'] or {}).get('evidence', []); kept = {e['id'] for e in rec['sift']['evidence']}
        t['kept'] += len(kept)
        t['questions'] += len(rec['sift']['candidates'])
        used = set()
        for item in art.get('statements', []) + [dict(x, weight='exclude') for x in art.get('exclude', [])]:
            hits = [e for e in ev if sw.matches(e['quote'], item)]
            used.update(e['id'] for e in hits)
            t[f"{item['weight']}:{'kept' if any(e['id'] in kept for e in hits) else 'lost'}"] += 1
        t['unmatched_kept'] += sum(1 for e in ev if e['id'] not in used and e['id'] in kept)
        t['empty_articles_kept'] += 1 if not art.get('statements') and kept else 0
        t['empty_articles'] += 0 if art.get('statements') else 1
    out[draw] = t
keys = ['failed', 'kept', 'core:kept', 'core:lost', 'supporting:kept', 'supporting:lost', 'optional:kept', 'optional:lost', 'unmatched_kept', 'empty_articles', 'empty_articles_kept', 'questions']
print('draw'.ljust(22), ' '.join(d.rjust(8) for d in out))
for k in keys:
    print(k.ljust(22), ' '.join(str(out[d].get(k, 0)).rjust(8) for d in out))

print()
for draw, recs in draws.items():
    if draw == 'v23-1':
        continue
    on_empty = sum(len(recs[i]['sift']['evidence']) for i, art in refs.items() if not art.get('statements') and recs.get(i) and recs[i]['sift'])
    cands = [(i, c) for i, r in recs.items() if r and r['sift'] for c in r['sift']['candidates']]
    kyber = sum(1 for i, c in cands if 'kyber' in c['question'].lower())
    kinds = collections.Counter(c.get('opens_as') for i, c in cands)
    stake_or_debt = [c['question'] for i, c in cands if c.get('opens_as') == 'binding_obligation' and any(w in c['question'].lower() for w in ('stake', 'invest', 'equity', 'notes', 'bond', 'debt', 'borrow', 'lease', 'indemn'))]
    print(draw.ljust(8), 'kept on 37 nothing-to-keep articles', on_empty, '| kyber questions', kyber, '| kinds', dict(kinds), '| obligation on stake/debt/lease words', len(stake_or_debt))
    for q in stake_or_debt[:6]:
        print('     ', q[:150])
