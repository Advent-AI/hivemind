import sqlite3, json, collections, random, re
random.seed(11)
R='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
v=sqlite3.connect(f'file:{R}/views.sqlite?mode=ro', uri=True); v.row_factory=sqlite3.Row
a=sqlite3.connect(f'file:{R}/archive.sqlite?mode=ro', uri=True)
t=sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); t.row_factory=sqlite3.Row
items={r['input_id']:r for r in t.execute("select input_id, publisher, publication_day, category, title, length(text) n, text from items")}
# 1 fed items length
fed=[r['input_id'] for r in v.execute("select distinct input_id from handovers")]
b=collections.Counter()
for i in fed:
    n=items[i]['n'] if i in items else -1
    b['<200' if n<200 else '<1000' if n<1000 else '<5000' if n<5000 else '<20000' if n<20000 else '>=20000']+=1
print('fed items', len(fed), dict(b))
print('fed by category', collections.Counter(items[i]['category'] for i in fed if i in items).most_common())
# 3 candidate drop reasons + 4 flow
cdrop=collections.Counter(); raw_c=0; kept_c=0
for (h,) in v.execute("select handover_json from handovers"):
    d=json.loads(h); kept_c+=len(d['candidates'])
    for x in d['dropped']:
        if x[0].startswith('c'): cdrop[re.sub(r"'[^']*'","'…'",x[1])[:90]]+=1
print('\ncandidate drops:'); [print(' ',c,k) for k,c in cdrop.most_common()]
out=collections.Counter()
for (dj,) in v.execute("select decisions_json from match_records"):
    for c in json.loads(dj).get('candidates',[]): out[c['outcome']]+=1
print('kept candidates', kept_c, 'match outcomes', dict(out), 'views', v.execute("select count(*) from views").fetchone()[0])
# 5 third_party_view
who=collections.Counter(); spk=collections.Counter(); n3=0
rows=list(a.execute("select answer_json from model_calls where purpose='extract'"))
pieces=[]
for (ans,) in rows:
    try: d=json.loads(ans)
    except Exception: continue
    for e in d.get('evidence',[]): pieces.append(e)
tp=[e for e in pieces if e.get('tier')=='third_party_view']
for e in tp: who[(e.get('original_who') or '')[:40]]+=1; spk[(e.get('speaker') or '')[:40]]+=1
print('\nthird_party_view', len(tp), 'of', len(pieces)); print(' original_who top:', who.most_common(15)); print(' speaker top:', spk.most_common(15))
print('\n15 random third_party_view pieces:')
for e in random.sample(tp,15): print(f"  - who='{e.get('original_who')}' spk='{e.get('speaker')}' links={e.get('links')} | {e.get('one_line','')[:160]}")
# 6 unlinked pieces
unl=[e for e in pieces if not e.get('links')]
kw=re.compile(r'H20|H200|export|China|Chinese|licen|capex|capital (spend|expend)|hyperscaler|Big Tech|data.cent(er|re) spend|Commerce', re.I)
hit=sum(1 for e in unl if kw.search(e.get('one_line','')+' '+e.get('quote','')))
print(f'\nunlinked {len(unl)}; mention theme keywords: {hit} ({hit/len(unl):.0%})')
tiers=collections.Counter(e.get('tier') for e in unl); print(' unlinked by tier', dict(tiers))
print('20 random unlinked pieces:')
for e in random.sample(unl,20): print(f"  - [{e.get('tier')}] who='{e.get('original_who')}' | {e.get('one_line','')[:170]}")
# 7 same-story duplicates: evidence_sources vs same_claims
print('\nstored evidence', v.execute("select count(*) from evidence").fetchone()[0], 'same_claims rows', v.execute("select count(*) from same_claims").fetchone()[0], 'revisions', v.execute("select count(*) from revisions").fetchone()[0])
# duplicate titles among fed items per day (normalised)
def norm(s): return ' '.join(re.findall(r'[a-z0-9]+', (s or '').lower()))
byday=collections.defaultdict(list)
for i in fed:
    if i in items: byday[items[i]['publication_day']].append(norm(items[i]['title']))
dup=0
for d,ts in byday.items():
    seen=[]
    for x in ts:
        w=set(x.split())
        if any(len(w&set(y.split()))/max(1,len(w|set(y.split())))>=0.5 for y in seen): dup+=1
        seen.append(x)
print('fed items whose title overlaps >=50% with an earlier same-day fed item:', dup, 'of', len(fed))
