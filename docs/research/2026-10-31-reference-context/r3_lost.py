"""R3's lost and guard lists (review-2026-10-31-method.md §6, loop log row 70): the statements that reach judgement under role-v53 in
the given runs and that role-v65's stored draws (Y5-v65-d1..3) keep in at most one draw, with the gold entry each one matches, so the
model can be asked about each (probe_drop.py) and the articles re-sent under the narrowed check. Two lists: the core and supporting
statements lost (the recall side) and the gold-not-kept statements v65 dropped in every draw (the guard: a narrowed check must not
re-admit them). Same classification as v65_on_reaching.py.
    python3 r3_lost.py <unlisted folder> run1 run2 run3"""
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
articles = {a['input_id']: a for a in sr.articles}
v65 = []
for d in (1, 2, 3):
    db = sqlite3.connect(f'file:{LOOP}/Y5-v65-d{d}/answers.sqlite?mode=ro', uri=True)
    v65.append({iid: (json.loads(content).get('evidence', []) if content else []) for iid, content in db.execute('select input_id, content from answers where completed=1')})


def gold_match(a, e):
    for i in a['items']:
        if i['weight'] in ('core', 'supporting') and sr.sg.same_matter(i, e):
            return 'core/supp', i
    for n in a['not_kept']:
        if n['weight'] == 'not_kept' and sr.sg.same(n['span'], e['quote']):
            return 'gold not kept', n
    return None, None


seen, rows = set(), []
for run in runs:
    v = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); v.row_factory = sqlite3.Row
    replaced = {r[0] for r in v.execute('select old_evidence_id from replacements')}
    for r in v.execute('select evidence_id, quote, one_line, created_from_input from evidence'):
        a = articles.get(r['created_from_input'])
        if not a or r['evidence_id'] in replaced or (a['input_id'], r['quote']) in seen:
            continue
        seen.add((a['input_id'], r['quote']))
        cls, gold = gold_match(a, dict(r))
        if cls is None:
            continue
        as_item = {'span': r['quote']}
        kept_in = sum(1 for draw in v65 if any(sr.sg.same_matter(as_item, x) for x in draw.get(a['input_id'], [])))
        if (cls == 'core/supp' and kept_in <= 1) or (cls == 'gold not kept' and kept_in == 0):
            rows.append((cls, kept_in, a['publication_day'], a['input_id'], gold.get('weight', 'not_kept'), gold['span'], r['quote'], r['one_line']))

json.dump({'lost': [{'input_id': x[3], 'weight': x[4], 'span': x[5], 'v65_kept_in': x[1]} for x in rows if x[0] == 'core/supp'],
           'guard': [{'input_id': x[3], 'span': x[5], 'v65_kept_in': x[1]} for x in rows if x[0] == 'gold not kept']},
          open(HERE / 'r3-lists.json', 'w'), indent=1, ensure_ascii=False)     # read by r3_compare.py
for cls in ('core/supp', 'gold not kept'):
    group = [x for x in rows if x[0] == cls]
    print(f'\n## {cls}: {len(group)} statements, {len({x[3] for x in group})} articles')
    for _, kept_in, day, iid, weight, span, quote, one_line in sorted(group, key=lambda x: (x[2], x[3])):
        print(f'- v65 kept in {kept_in}/3 | {day} | {iid} | gold {weight}: {span[:90]!r}\n    v53 quote: {quote[:140]!r}\n    one_line: {one_line[:140]!r}')
