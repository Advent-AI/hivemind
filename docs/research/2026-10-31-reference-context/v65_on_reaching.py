"""R3's $0 proof (review-2026-10-31-method.md §5): would role-v65 (D252 paired examples; stored draws Y5-v65-d1..3 on the same articles) have
kept the statements that reach judgement under role-v53 in the given runs? Per class (gold not kept; gold-unlisted judged not kept by both
readers / by either; core and supporting as the recall guard), the number of statements kept by v65 in 0, 1, 2 or 3 of its draws.
    python3 v65_on_reaching.py <unlisted folder> run1 run2 run3"""
import collections
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import score_ref as sr  # noqa: E402

LOOP = ROOT / 'docs/research/2026-10-29-analyst-standard/loop-2026-10-29'
folder, runs = Path(sys.argv[1]), [str(ROOT / p) if not p.startswith('/') else p for p in sys.argv[2:]]
ukey = json.load(open(folder / 'unlisted.key.json'))
readers = [{r['id']: r['weight'] for r in (json.loads(l) for l in open(folder / f'verdicts-{x}.jsonl') if l.strip().startswith('{'))} for x in 'AB']
both = {(ukey[i]['input_id'], ukey[i]['quote']) for i in ukey if all(w.get(i) == 'not_kept' for w in readers)}
either = {(ukey[i]['input_id'], ukey[i]['quote']) for i in ukey if any(w.get(i) == 'not_kept' for w in readers)}
articles = {a['input_id']: a for a in sr.articles}
v65 = []
for d in (1, 2, 3):
    db = sqlite3.connect(f'file:{LOOP}/Y5-v65-d{d}/answers.sqlite?mode=ro', uri=True)
    v65.append({iid: (json.loads(content).get('evidence', []) if content else []) for iid, content in db.execute('select input_id, content from answers where completed=1')})


def cls(a, e):
    if any(sr.sg.same_matter(i, e) for i in a['items'] if i['weight'] in ('core', 'supporting')):
        return 'core/supp (guard)'
    if any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'not_kept'):
        return 'noise: gold not kept'
    k = (a['input_id'], e['quote'])
    if k in both:
        return 'noise: unlisted, both readers not kept'
    if k in either:
        return 'noise: unlisted, one reader not kept'
    return None


seen, kept = set(), collections.defaultdict(collections.Counter)
for run in runs:
    v = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); v.row_factory = sqlite3.Row
    replaced = {r[0] for r in v.execute('select old_evidence_id from replacements')}
    for r in v.execute('select evidence_id, quote, one_line, created_from_input from evidence'):
        a = articles.get(r['created_from_input'])
        if not a or r['evidence_id'] in replaced or (a['input_id'], r['quote']) in seen:
            continue
        seen.add((a['input_id'], r['quote']))
        c = cls(a, dict(r))
        if c is None:
            continue
        as_item = {'span': r['quote']}          # the stored statement read as a gold-shaped item, so the counting aid compares matter, not bytes
        n = sum(1 for draw in v65 if any(sr.sg.same_matter(as_item, x) for x in draw.get(a['input_id'], [])))
        kept[c][n] += 1
print('distinct statements reaching judgement under role-v53 (three runs), by class: kept by role-v65 in k of 3 draws')
for c in sorted(kept):
    row = kept[c]; total = sum(row.values())
    print(f'  {c:<42} n={total:>3}  kept in 0/1/2/3 draws: {row[0]:>3} {row[1]:>3} {row[2]:>3} {row[3]:>3}   (kept in >=2: {(row[2] + row[3]) / total:.0%})')
