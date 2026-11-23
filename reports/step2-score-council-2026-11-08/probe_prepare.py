"""Reconstruct selected c8 comparisons without service calls; refuse mismatches."""
import copy,hashlib,importlib.util,json,math,sqlite3,sys
from pathlib import Path
ROOT=Path('/Users/lchingen/hivemind');HERE=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/'src'))
def load(path):
 spec=importlib.util.spec_from_file_location('step_runner',path); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
run=load(ROOT/'clean-arch/step2/run_forward.py'); cmp=run.compare
from hivemind import jev
SOURCE=ROOT/'poc/data/clean-acceptance-2026-11-09'; STEP=SOURCE/'step2';IDS=['22:ev-11','13:e11','38:ev-2','18:e2','43:e3','3:e1','9:e6','14:e3','5:e1','9:e1','19:ev-guidance-70']
def serial(obj):return json.dumps(obj,sort_keys=True,ensure_ascii=False)
def digest(obj):return hashlib.sha256(serial(obj).encode()).hexdigest()
def build():
 arts,questions,_=run.step1_records(str(SOURCE/'step1/trace.sqlite')); decisions=json.loads((STEP/'decisions.json').read_text()); byid={x['id']:x for x in decisions}; vectors=json.loads((STEP/'embeddings.json').read_text());db=sqlite3.connect('file:'+str(STEP/'jev.sqlite')+'?mode=ro',uri=True); rows=db.execute("select request_json,answer_json from model_calls where purpose='clean_step2'").fetchall(); original={r:json.loads(a) for r,a in rows}; lib=run.library.Library(); output=[]
 if not arts or not decisions or not vectors or len(IDS)!=len(set(IDS)):raise ValueError('missing or empty input')
 for article in arts:
  for record in article:
   if record['id'] not in IDS:continue
   d=byid[record['id']]; ids=d['candidates']; qvec=cmp.query_vectors(vectors,record,questions); labels=['thesis search']*len(record['thesis_ids'])+(['own-text search'] if not record['thesis_ids'] or record.get('figures') else [])
   if not ids or len(qvec)!=len(labels):raise ValueError('missing candidates or queries')
   qrows=[]; union=[]
   for q,label in zip(qvec,labels):
    values={g:cmp.cosine(q,vectors[cmp.doc_text(lib.groups[g]['original'])]) for g in lib.order};ranked=sorted(lib.order,key=lambda g:-values[g])[:cmp.TOP];qrows.append({'type':label,'vector_sha256':digest(q),'ranked_top10':ranked,'scores':{g:values[g] for g in ids}})
    union.extend(g for g in ranked if g not in union)
   if union!=ids:raise ValueError('historical union mismatch '+record['id'])
   qs={f'q{i}':cmp.piece_question(cmp.piece_text(lib.groups[g]['original'],'STORED PIECE')) for i,g in enumerate(ids)}; req=jev.request_for(run.SETTING,cmp.piece_text(record,'INCOMING PIECE'),qs); encoded=serial(req)
   if encoded not in original:raise ValueError('request not in archive '+record['id'])
   answer=original[encoded]; problems=jev.validate(answer,qs)
   if problems:raise ValueError('saved answer invalid '+str(problems))
   mapped={g:{'choice':answer[f'q{i}']['choice'],'probabilities':answer[f'q{i}']['probabilities']} for i,g in enumerate(ids)}
   if mapped!=d['answers'] or cmp.outcome(mapped,lib.order)!=d['outcome']:raise ValueError('saved outcome mismatch '+record['id'])
   treatment=copy.deepcopy(req); origins={g:[i+1 for i,row in enumerate(qrows) if g in row['ranked_top10']] for g in ids}
   for i,g in enumerate(ids):
    bits=[f"query {j+1} [{row['type']}]: {row['scores'][g]:.4f}" for j,row in enumerate(qrows)]
    treatment['questions'][f'q{i}']['instructions']+='\nRetrieval metadata (not part of the stored piece; cosine, not a probability): '+'; '.join(bits)
   output.append({'id':record['id'],'group_order':list(lib.order),'candidates':ids,'queries':qrows,'origins':origins,'control':req,'treatment':treatment,'archive_sha256':digest(req),'old_answer_sha256':digest(answer),'old_answers':answer})
  for r in article:
   d=byid[r['id']];lib.apply(r,d['outcome'])
 if {x['id'] for x in output}!=set(IDS):raise ValueError('selected population incomplete')
 return output

def check(manifest,expected):
 if not manifest or len(manifest)!=len(expected):raise ValueError('empty or wrong population')
 for got,want in zip(manifest,expected):
  if got!=want:raise ValueError('manifest differs for '+str(got.get('id')))
def main():
 a=build();b=build();check(a,b)
 for kind in ('score','candidate','origin','query'):
  mutated=copy.deepcopy(a);x=mutated[0]
  if kind=='score':x['queries'][0]['scores'][x['candidates'][0]]+=0.1
  if kind=='candidate':x['candidates'][0]='not-a-candidate'
  if kind=='origin':x['origins'][x['candidates'][0]]=[]
  if kind=='query':x['queries'][0]['ranked_top10'].reverse()
  try:check(mutated,b)
  except ValueError:print('negative control caught:',kind)
  else:raise RuntimeError('negative control failed '+kind)
 try:check([],b)
 except ValueError:print('negative control caught: empty input')
 else:raise RuntimeError('empty control failed')
 output=HERE/'probe-manifest.json';output.write_text(json.dumps(a,ensure_ascii=False,indent=1)+'\n');print('selected cases',len(a),'candidate pairs',sum(len(x['candidates']) for x in a),'multiquery',sum(len(x['queries'])>1 for x in a),'manifest sha256',hashlib.sha256(output.read_bytes()).hexdigest())
if __name__=='__main__':main()
