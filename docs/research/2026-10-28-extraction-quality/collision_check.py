import sqlite3, json, re, collections
R='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
v=sqlite3.connect(f'file:{R}/views.sqlite?mode=ro', uri=True); v.row_factory=sqlite3.Row
gold={}
for line in open('/Users/lchingen/hivemind-admission-v12-2026-10-26/docs/research/2026-10-28-quality-review/gold-admission.md'):
    m=re.match(r'\| (v\d+) [^|]*\| ([^|]+) \|', line)
    if m: gold[m.group(1)]=m.group(2).strip()
views={r['view_id']:r for r in v.execute("select * from views")}
verdicts=collections.Counter(); opened=[]
for r in v.execute("select input_id, seq, decisions_json from match_records"):
    d=json.loads(r['decisions_json'])
    for c in d.get('candidates',[]):
        m=re.search(r'collision judge: (.*)$', c.get('reason',''))
        if not m: continue
        rel=dict(re.findall(r'(v\d+): (\w+)', m.group(1)))
        for x in rel.values(): verdicts[x]+=1
        if c['outcome']=='new':
            # which view did this candidate become? the view created from this input with seq
            vid=next((k for k,x in views.items() if x['created_from_input']==r['input_id'] and x['created_seq']==r['seq'] and x['question']), None)
            opened.append((vid, rel, c['outcome']))
print('collision verdicts given:', dict(verdicts))
print('\ncandidates opened as new after a collision verdict: view, gold label, verdicts')
agree=collections.Counter()
for vid, rel, out in opened:
    g=gold.get(vid,'?'); dq=[p for p,x in rel.items() if x=='distinct_question_same_matter']
    print(f'  {vid} gold={g} | {rel}')
    if dq: agree[('fold would be', 'right' if g.startswith('重复') else 'wrong' if g=='留' else g)]+=1
print('\nif every distinct_question_same_matter verdict folded the candidate:', dict(agree))
