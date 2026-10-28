import sqlite3, json, collections, re, sys
sys.path.insert(0,'/Users/lchingen/hivemind-admission-v12-2026-10-26/src')
from hivemind import extraction
R='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
v=sqlite3.connect(f'file:{R}/views.sqlite?mode=ro', uri=True); v.row_factory=sqlite3.Row
a=sqlite3.connect(f'file:{R}/archive.sqlite?mode=ro', uri=True)
t=sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); t.row_factory=sqlite3.Row
text={r['input_id']:r['text'] for r in t.execute("select input_id, text from items where publication_day between '2026-07-01' and '2026-08-19'")}
print('normalise source:'); import inspect; print(inspect.getsource(extraction.normalise))
# a. quote-not-in-item drops: which would pass with punctuation-spacing normalisation
def loose(s):
    s=extraction.normalise(s)
    s=re.sub(r'\s+([,.;:!?)\]])', r'\1', s); s=re.sub(r'([(\[])\s+', r'\1', s)
    s=s.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('—','-').replace('–','-')
    return re.sub(r'\s+',' ',s)
qdrop=0; fixed=0; unshown=collections.Counter(); unshown_ids=collections.Counter(); items_with_qdrop=set(); examples=[]
calls_per_item=collections.Counter()
for r in v.execute("select input_id, handover_json from handovers"):
    h=json.loads(r['handover_json']); iid=r['input_id']
    # find the raw answer that produced this handover: the call whose evidence ids match... use the latest call for the item
    rows=a.execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id", (f'%[Item] id {iid},%',)).fetchall()
    calls_per_item[len(rows)]+=1
    raw={}
    for (ans,) in rows:
        try:
            for e in json.loads(ans).get('evidence',[]): raw[e['id']]=e      # later calls overwrite
        except Exception: pass
    for eid, reason in h['dropped']:
        if reason=='quote not in item':
            qdrop+=1; items_with_qdrop.add(iid)
            e=raw.get(eid); tx=text.get(iid,'')
            if e and loose(e['quote']) in loose(tx):
                fixed+=1
                if len(examples)<4: examples.append((iid, e['quote'][:110]))
        m=re.match(r"links to nothing shown: \[(.*)\]", reason)
        if m and m.group(1):
            ids=re.findall(r"'(v\d+)'", m.group(1))
            if ids: unshown['pieces linking only to unshown thesis ids']+=1; [unshown_ids.__setitem__(i, unshown_ids[i]+1) for i in ids]
print(f'\nquote-not-in-item drops: {qdrop} in {len(items_with_qdrop)} items; pass with punctuation/quote normalisation: {fixed}')
for x in examples: print('  e.g.', x)
print('\n', dict(unshown), '| ids:', unshown_ids.most_common(10))
print('\nextract calls per item (retries):', dict(calls_per_item))
