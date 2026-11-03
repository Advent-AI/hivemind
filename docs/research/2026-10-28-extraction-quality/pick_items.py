import sqlite3, json, random
random.seed(5)
R='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
v=sqlite3.connect(f'file:{R}/views.sqlite?mode=ro', uri=True); v.row_factory=sqlite3.Row
t=sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); t.row_factory=sqlite3.Row
rows=[]
for r in v.execute("select input_id, handover_json from handovers"):
    it=t.execute("select publisher, publication_day, category, title, length(text) n from items where input_id=?",(r['input_id'],)).fetchone()
    if not it or not (1500<=it['n']<=7000): continue
    h=json.loads(r['handover_json'])
    rows.append((it['category'], r['input_id'], it['publisher'], it['publication_day'], it['n'], len(h['evidence']), len(h['dropped']), len(h['candidates']), it['title'][:70]))
want={'T7':5,'T8':3,'T6':2}
for cat,k in want.items():
    pool=[x for x in rows if x[0]==cat]
    for x in random.sample(pool, k): print(x)
