import sqlite3, json, collections, re, random
random.seed(23)
R='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
v=sqlite3.connect(f'file:{R}/views.sqlite?mode=ro', uri=True); v.row_factory=sqlite3.Row
a=sqlite3.connect(f'file:{R}/archive.sqlite?mode=ro', uri=True)
t=sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); t.row_factory=sqlite3.Row
titles={r['input_id']:(r['publisher'],r['publication_day'],r['title']) for r in t.execute("select input_id, publisher, publication_day, title from items")}
# 1 retry cause
by=collections.defaultdict(list)
for cid, req, cost, itok, otok, ans in a.execute("select call_id, request_json, cost_usd, input_tokens, output_tokens, answer_json from model_calls where purpose='extract' order by call_id"):
    m=re.search(r'\[Item\] id (\S+),', req); iid=m.group(1) if m else '?'
    user=[x['content'] for x in json.loads(req)['messages'] if x['role']=='user'][0]
    shown=re.search(r'\[Existing theses of these objects\](.*?)\n\n', user, re.S); groups=re.search(r'\[Research groups\](.*?)\n\n', user, re.S)
    by[iid].append((cid, cost, itok, otok, shown.group(1) if shown else '', groups.group(1) if groups else '', len(ans)))
cause=collections.Counter(); extra_cost=0; extra_calls=0
for iid, calls in by.items():
    if len(calls)<2: continue
    for prev, cur in zip(calls, calls[1:]):
        extra_calls+=1; extra_cost+=prev[1]
        if prev[4]!=cur[4]: cause['shown theses changed']+=1
        elif prev[5]!=cur[5]: cause['groups block changed']+=1
        elif prev[6]==0: cause['previous answer empty']+=1
        else: cause['same request text, re-sent anyway']+=1
tot=a.execute("select sum(cost_usd), count(*) from model_calls where purpose='extract'").fetchone()
print('extra extract calls', extra_calls, 'cost of superseded calls $%.3f of $%.3f total (%d calls)'%(extra_cost, tot[0], tot[1])); print(dict(cause))
# 2 unlinked pieces sample from items with >=1 kept piece
kept_items={r['input_id'] for r in v.execute("select input_id from handovers where handover_json not like '%\"evidence\": []%'")}
pool=[]
for iid, calls in by.items():
    if iid not in kept_items: continue
    ans=a.execute("select answer_json from model_calls where call_id=?",(calls[-1][0],)).fetchone()[0]
    for e in json.loads(ans).get('evidence',[]):
        if not e.get('links'): pool.append((iid, e))
print('\nunlinked pieces in items that kept >=1 piece:', len(pool))
for iid,e in random.sample(pool,40):
    p=titles.get(iid,('?','?','?')); print(f"- [{e['tier']}] who='{(e.get('original_who') or '')[:30]}' ({p[0]} {p[1]} «{p[2][:50]}»)\n    {e['one_line'][:190]}")
# 3 reject-list regex over kept (stored) pieces
spec=re.compile(r'\b\d+(\.\d+)?\s?(W|watts|kW|TB|GB|MHz|GHz|nm)\b|\b\d+(\.\d+)?[x×] (faster|more performance|the performance|speedup)|frame rate|benchmark', re.I)
n=0; hit=0; ex=[]
for r in v.execute("select one_line, quote from evidence"):
    n+=1
    if spec.search(r['one_line']) or spec.search(r['quote']): hit+=1; len(ex)<6 and ex.append(r['one_line'][:120])
print(f'\nstored pieces matching spec/benchmark pattern: {hit} of {n}'); [print('   ', x) for x in ex]
