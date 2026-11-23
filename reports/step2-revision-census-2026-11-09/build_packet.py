import sqlite3,json,pathlib,random,collections,hashlib
root=pathlib.Path('/Users/lchingen/hivemind');base=root/'poc/data/clean-e2e-2026-11-09';out=root/'reports/step2-revision-census-2026-11-09';run=base/'stage2-clean-d1-segment-2'
decisions=json.loads((run/'step2/decisions.json').read_text());lib=json.loads((run/'step2/library.json').read_text());records={}
for g in lib['groups'].values():
 for r in [g['original']]+g['members']:
  if r['id'] in records and records[r['id']]!=r:raise ValueError('conflicting record '+r['id'])
  records[r['id']]=r
sources={}
for path in [base/'stage2-clean-d1/trace.sqlite',run/'trace.sqlite']:
 db=sqlite3.connect(f'file:{path}?mode=ro',uri=True)
 for s in json.loads(db.execute('select source_items from run').fetchone()[0]):
  if s['input_id'] in sources and sources[s['input_id']]['text']!=s['text']:raise ValueError('different source text '+s['input_id'])
  sources[s['input_id']]=s
 db.close()
allpairs=[]
for d in decisions:
 for group,a in d.get('answers',{}).items():
  if a['choice'] in ('supersedes','same_statement','different'):
   incoming=records[d['id']];stored=lib['groups'][group]['original']
   if incoming['article']<=stored['article']:raise ValueError('chronology '+str((incoming['id'],stored['id'])))
   for r in (incoming,stored):
    if r['input_id'] not in sources:raise ValueError('source absent '+r['input_id'])
   allpairs.append((d,group,a,incoming,stored))
revision=[x for x in allpairs if x[2]['choice']=='supersedes'];assert len(revision)==56
assert ('203:e1','119:e1') in [(x[0]['id'],x[1]) for x in revision]
rng=random.Random(20261109)
controls=[]
for label in ('same_statement','different'):
 pool=[x for x in allpairs if x[2]['choice']==label and x[0]['id'] not in {z[0]['id'] for z in revision}]
 controls.extend(rng.sample(pool,10))
pairs=revision+controls;rng.shuffle(pairs)
key=[];packets=[[] for _ in range(6)]
for ix,(d,group,a,new,old) in enumerate(pairs,1):
 alias=f'C{ix:03}'
 def piece(r):
  s=sources[r['input_id']]
  return {'record':{k:r.get(k) for k in ('summary','passages','tier','original_party','reporting_speaker','statement_date','statement_date_text','evidence_period')},'source':{'title':s['title'],'publisher':s['publisher'],'publication_day':s['publication_day'],'text':s['text']}}
 packets[(ix-1)%6].append({'case':alias,'stored':piece(old),'incoming':piece(new)})
 key.append({'case':alias,'incoming':d['id'],'stored_group':group,'stored_id':old['id'],'answer':a,'outcome':d['outcome'],'final_group':lib['placement'][d['id']]})
for i,packet in enumerate(packets,1):(out/f'blind-batch-{i}.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
(out/'key-private.json').write_text(json.dumps(key,ensure_ascii=False,indent=2)+'\n')
print('56 revision answers from',len({x[0]['id'] for x in revision}),'incoming records, plus 20 blind controls; six batches:',[len(p) for p in packets])
print('source identity verification: every pair exists, both source inputs found in completed traces, chronology valid; R05 positive control present')
print('batch lengths bytes:',[(out/f'blind-batch-{i}.json').stat().st_size for i in range(1,7)])
print('sha256 frozen blind packets:',*[hashlib.sha256((out/f'blind-batch-{i}.json').read_bytes()).hexdigest() for i in range(1,7)])
