"""Link recall of the arm against the blind readers' link gold (blind/linkgold-A.json, -B.json; key blind/linkgold.key.json): for every
core or supporting gold entry in an article with >=6 open questions, the question the readers say it moves (agreement, or A alone when B
is missing); per draw, whether the arm's statement matching that entry (score_gold.same_matter) links to that question (hit), to another
shown question (wrong), to nothing shown (unlinked), or is not kept at all.   python3 link_recall.py"""
import json, collections, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_ref as sr  # noqa: E402

def load(name):
    p = HERE / 'blind' / name
    if not p.exists():
        return {}
    raw = p.read_text(); return json.loads(raw[raw.find('{'):raw.rfind('}') + 1])
A, B = load('linkgold-A.json'), load('linkgold-B.json')
key = json.loads((HERE / 'blind/linkgold.key.json').read_text())
first = lambda v: (v or {}).get('question', 'none').split(',')[0].strip()
agree = disagree = 0
gold_q = {}
for gid in key:
    a, b = first(A.get(gid)), first(B.get(gid)) if B else None
    if B:
        if a == b: agree += 1; gold_q[gid] = a
        else: disagree += 1; gold_q[gid] = ('?', a, b)
    else:
        gold_q[gid] = a
if B:
    print(f'readers agree on {agree} of {agree + disagree} entries')
arts = {x['input_id']: x for x in sr.articles}
tot = collections.Counter(); per_q = collections.defaultdict(collections.Counter)
for gid, k in key.items():
    g = gold_q[gid]
    if isinstance(g, tuple) or g == 'none':
        tot['gold none/disputed'] += 1; continue
    item = next(i for i in arts[k['input_id']]['items'] if i['span'] == k['span'])
    for d in (1, 2, 3):
        data = sr.raw(f'REF-v53R-d{d}', k['input_id']) or {}
        e = next((e for e in data.get('evidence', []) if sr.sg.same_matter(item, e)), None)
        shown_ids = {q['view_id'] for q in sr.shown(k['input_id'])}
        if e is None: r = 'not kept'
        elif g in e.get('links', []): r = 'hit'
        elif any(l in shown_ids for l in e.get('links', [])): r = 'wrong question'
        else: r = 'unlinked'
        tot[r] += 1; per_q[g][r] += 1
n = sum(v for k2, v in tot.items() if k2 != 'gold none/disputed')
print('entries the readers link to a question:', n // 3, '| draws:', dict(tot), f'| recall (hit / kept) = {tot["hit"] / max(1, n - tot["not kept"]):.0%}')
for q, c in sorted(per_q.items(), key=lambda kv: -sum(kv[1].values())):
    print(f'  {q}: {dict(c)}')
