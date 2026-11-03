import sqlite3, json, collections, re, sys
sys.path.insert(0,'/Users/lchingen/hivemind-admission-v12-2026-10-26/src')
from hivemind import extraction
R='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
v=sqlite3.connect(f'file:{R}/views.sqlite?mode=ro', uri=True); v.row_factory=sqlite3.Row
a=sqlite3.connect(f'file:{R}/archive.sqlite?mode=ro', uri=True)
t=sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); t.row_factory=sqlite3.Row
text={r['input_id']:r['text'] for r in t.execute("select input_id, text from items where publication_day between '2026-07-01' and '2026-08-19'")}
def loose(s):
    s=extraction.normalise(s)
    s=re.sub(r'\s+([,.;:!?)\]])', r'\1', s); s=re.sub(r'([(\[])\s+', r'\1', s)
    s=s.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('—','-').replace('–','-')
    return re.sub(r'\s+',' ',s)
why=collections.Counter(); linked=0; restored=[]; still=[]
for r in v.execute("select input_id, handover_json from handovers"):
    h=json.loads(r['handover_json']); iid=r['input_id']
    rows=a.execute("select request_json, answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {iid},%',)).fetchall()
    if not rows: continue
    req=json.loads(rows[0][0]); user=[m['content'] for m in req['messages'] if m['role']=='user'][0]
    shown=set(re.findall(r'^  - (v\d+) \(', (re.search(r'\[Existing theses of these objects\](.*?)\n\n', user, re.S) or [None,''])[1], re.M))
    raw={e['id']:e for e in json.loads(rows[0][1]).get('evidence',[])}
    cids={c['id'] for c in h['candidates']}
    for eid, reason in h['dropped']:
        if reason!='quote not in item': continue
        e=raw.get(eid); tx=text.get(iid,'')
        if not e: why['raw piece not found (other call)']+=1; continue
        q=extraction.normalise(e['quote'])
        if len(q)<8: why['quote shorter than 8']+=1; continue
        if loose(e['quote']) in loose(tx):
            links=[l for l in e.get('links',[]) if l in shown or l in cids]
            why['restored, linked' if links else 'restored, unlinked']+=1
            if links and len(restored)<12: restored.append((e['tier'], links, e['one_line'][:120]))
        else:
            # classify: space-collapse only? partial?
            why['still not found']+=1
            if len(still)<6: still.append((e['quote'][:90], iid))
print(dict(why)); print('\nrestored+linked examples:'); [print('  ',x) for x in restored]; print('\nstill not found examples:'); [print('  ',x) for x in still]
