import sqlite3, json, sys, re
R='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
v=sqlite3.connect(f'file:{R}/views.sqlite?mode=ro', uri=True); v.row_factory=sqlite3.Row
a=sqlite3.connect(f'file:{R}/archive.sqlite?mode=ro', uri=True)
t=sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); t.row_factory=sqlite3.Row
for iid in sys.argv[1:]:
    it=t.execute("select * from items where input_id=?",(iid,)).fetchone()
    row=a.execute("select request_json, answer_json from model_calls where purpose='extract' and request_json like ? order by call_id limit 1",(f'%[Item] id {iid},%',)).fetchone()
    req=json.loads(row[0]); user=[m['content'] for m in req['messages'] if m['role']=='user'][0]
    shown=re.search(r'\[Existing theses of these objects\].*?\n((?:  - .*\n)+)', user)
    d=json.loads(row[1])
    h=json.loads(v.execute("select handover_json from handovers where input_id=?",(iid,)).fetchone()['handover_json'])
    print(f"\n######## {iid} {it['category']} {it['publisher']} {it['publication_day']} «{it['title']}» text {len(it['text'])} chars")
    print('SHOWN:', re.sub(r'\n\s+', ' | ', re.sub(r', focus "[^"]*"', '', shown.group(1)))[:700] if shown else 'none')
    print('--- TEXT'); print(re.sub(r'\n{2,}', '\n', it['text'])[:4200])
    print('--- RAW EVIDENCE', len(d.get('evidence',[])), 'kept', len(h['evidence']), 'dropped', len(h['dropped']))
    for e in d.get('evidence',[]):
        print(f" {e['id']} [{e['tier']}] who='{e.get('original_who')}' day='{e.get('original_day')}' links={e.get('links')}\n    one_line: {e.get('one_line','')[:230]}\n    quote: {e.get('quote','')[:150]}")
    for c in d.get('candidates',[]):
        print(f" CAND {c['id']} {c.get('object')} {c.get('opens_as')} {c.get('measure')} folds_into='{c.get('folds_into')}' | {c.get('question')}\n    lost_if_folded: {c.get('lost_if_folded','')[:200]}")
    print(' DROPPED:', [(x[0], x[1][:60]) for x in h['dropped']])
