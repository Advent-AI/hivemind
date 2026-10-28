import sqlite3, json, collections
R='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
a=sqlite3.connect(f'file:{R}/archive.sqlite?mode=ro', uri=True)
n=0; pieces=0; unl=0; empty=0; cands=0
oa=collections.Counter(); linkdist=collections.Counter(); percall=[]
tiers=collections.Counter(); who_empty=0; day_empty=0; first=None
for sha, ans in a.execute("select request_sha256, answer_json from model_calls where purpose='extract'"):
    try: d=json.loads(ans)
    except Exception: continue
    n+=1; ev=d.get('evidence',[]); cs=d.get('candidates',[])
    if not ev and not cs: empty+=1
    pieces+=len(ev); cands+=len(cs); percall.append(len(ev))
    for e in ev:
        L=e.get('links') or []
        if not L: unl+=1
        linkdist[min(len(L),4)]+=1
        tiers[e.get('tier')]+=1
        if not e.get('original_who'): who_empty+=1
        if not e.get('original_day'): day_empty+=1
    for c in cs:
        k=c.get('key') or {}
        oa[(c.get('opens_as'), k.get('measure') or c.get('measure'), c.get('object'), bool(c.get('folds_into')))]+=1
        if first is None: first=c
percall.sort()
print('extract answers', n, 'empty', empty, 'pieces', pieces, 'unlinked', unl, f'{unl/pieces:.0%}', 'candidates', cands)
print('links per piece', dict(linkdist))
print('pieces per call: median', percall[len(percall)//2], 'p90', percall[int(len(percall)*.9)], 'max', percall[-1])
print('tiers', dict(tiers), 'who empty', who_empty, 'day empty', day_empty)
print('candidates by (opens_as, measure, object, folds_into set):')
for k,v in oa.most_common(40): print('  ',v,k)
print(json.dumps(first, ensure_ascii=False)[:1500])
