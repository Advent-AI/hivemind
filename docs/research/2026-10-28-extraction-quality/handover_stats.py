import sqlite3, json, collections
R='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
v=sqlite3.connect(f'file:{R}/views.sqlite?mode=ro', uri=True)
drop=collections.Counter(); keys=collections.Counter(); n=0; ev=0; cand=0
for (h,) in v.execute("select handover_json from handovers"):
    d=json.loads(h); n+=1; ev+=len(d.get('evidence',[])); cand+=len(d.get('candidates',[]))
    for k in d: keys[k]+=1
    for x in d.get('dropped',[]):
        drop[x.get('reason', str(x)[:80]) if isinstance(x,dict) else str(x)[:80]]+=1
print('handovers', n, 'evidence kept', ev, 'candidates kept', cand, 'keys', dict(keys))
for k,c in drop.most_common(20): print(c, k)
h=json.loads(v.execute("select handover_json from handovers where handover_json like '%\"dropped\": [{%' limit 1").fetchone()[0])
print('--- dropped sample:', json.dumps(h['dropped'][:2], ensure_ascii=False)[:800])
print('--- match outcomes')
out=collections.Counter(); reason=collections.Counter(); keys2=collections.Counter()
for (dj,) in v.execute("select decisions_json from match_records"):
    d=json.loads(dj)
    for k in d: keys2[k]+=1
    for c in d.get('candidates',[]): out[c['outcome']]+=1; reason[(c['outcome'], c.get('reason','')[:70])]+=1
print('decision keys', dict(keys2)); print(dict(out))
for k,c in reason.most_common(30): print(c,k)
print('--- late_statements', v.execute("select count(*) from late_statements").fetchone(), 'review_pool', v.execute("select kind, count(*) from review_pool_entries group by kind").fetchall())
d=json.loads(v.execute("select decisions_json from match_records where decisions_json like '%candidates%' limit 1").fetchone()[0]); print(json.dumps(d.get('candidates',[])[:1], ensure_ascii=False)[:1200])
