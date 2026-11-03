import sqlite3, json, collections, re
R='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
v=sqlite3.connect(f'file:{R}/views.sqlite?mode=ro', uri=True); v.row_factory=sqlite3.Row
a=sqlite3.connect(f'file:{R}/archive.sqlite?mode=ro', uri=True)
t=sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); t.row_factory=sqlite3.Row
items={r['input_id']:dict(r) for r in t.execute("select input_id, publisher, publication_day, category, title from items")}
MEDIA=re.compile(r'article|author|reporter|report|the (post|times|register|verge|information|journal)|\.com|news|cnbc|bloomberg|reuters|tom\'s hardware|wccftech|techcrunch|techradar|bgr|fool|247wallst|investing|marketwatch|benzinga|yahoo|seeking alpha|motley|zacks|barron|wsj|ft\b|nikkei|scmp|straits|datacenterdynamics|the register|tradingview|futurum|marketscale|techrepublic|engadget|ars technica|9to5|gizmodo|venturebeat|axios|semafor|fortune|forbes|business insider|insider|morningstar|tipranks|simply wall|gurufocus|nasdaq\.com|thestreet|barchart', re.I)
def who_class(e, pub):
    w=(e.get('original_who') or '').strip(); s=(e.get('speaker') or '').strip()
    if not w and not s: return 'none'
    x=w or s
    if MEDIA.search(x) or (pub and pub.split('.')[0].lower() in x.lower()): return 'outlet'
    return 'named'
# stored evidence with judge citations
cited=set()
for (cj,) in v.execute("select cited_evidence_json from judgements"):
    cited.update(json.loads(cj or '[]'))
src={r['evidence_id']:r['input_id'] for r in v.execute("select evidence_id, input_id from evidence_sources")}
nlinks=collections.Counter(r['evidence_id'] for r in v.execute("select evidence_id from evidence_links"))
by=collections.defaultdict(lambda:[0,0])
bylinks=collections.defaultdict(lambda:[0,0])
for r in v.execute("select * from evidence"):
    e=dict(r); pub=items.get(src.get(e['evidence_id']),{}).get('publisher','')
    k=(e['tier'], who_class(e,pub)); by[k][0]+=1; by[k][1]+=int(e['evidence_id'] in cited)
    kk=min(nlinks[e['evidence_id']],3); bylinks[kk][0]+=1; bylinks[kk][1]+=int(e['evidence_id'] in cited)
print('stored evidence by (tier, who-class): n, cited, share')
for k in sorted(by): print(f'  {k}: {by[k][0]:5d} {by[k][1]:4d} {by[k][1]/by[k][0]:.0%}')
print('by link count:', {k:(n,c,f'{c/n:.0%}') for k,(n,c) in sorted(bylinks.items())})
tot=sum(n for n,_ in by.values()); totc=sum(c for _,c in by.values()); print('total', tot, 'cited', totc, f'{totc/tot:.0%}')
# raw pieces: who-class, split proxy, reference-vs-shown mismatch
raw=collections.Counter(); split=collections.Counter(); mism=0; reqs=0; keyshown=collections.Counter()
for (req, ans) in a.execute("select request_json, answer_json from model_calls where purpose='extract'"):
    try: d=json.loads(ans); r=json.loads(req)
    except Exception: continue
    user=[m['content'] for m in r['messages'] if m['role']=='user'][0]
    m=re.search(r'\[Item\] id (\S+),', user); iid=m.group(1) if m else ''
    pub=items.get(iid,{}).get('publisher','')
    reqs+=1
    ref=re.search(r'\[Research reference\].*?\n((?:  - .*\n)+)', user)
    shown=re.search(r'\[Existing theses of these objects\].*?\n((?:  - .*\n)+)', user)
    shown_txt=shown.group(1) if shown else ''
    if ref and 'event[H20/H200 China](licence)' in ref.group(1):
        keyshown['H200 key in reference']+=1
        if 'H200' not in shown_txt and 'H20' not in shown_txt: keyshown['...but no H200 thesis shown']+=1
    g=collections.Counter()
    for e in d.get('evidence',[]):
        raw[(e.get('tier'), who_class(e,pub), bool(e.get('links')))]+=1
        g[((e.get('original_who') or '').strip().lower(), (e.get('original_day') or '').strip())]+=1
    for (w,dy),n in g.items():
        if n>=3 and w: split['>=3 pieces same who+day']+=1; split['pieces in such runs']+=n
print('\nraw pieces by (tier, who-class, linked):')
for k in sorted(raw): print(f'  {k}: {raw[k]}')
print('\nrequests', reqs, dict(keyshown)); print('split proxy', dict(split))
