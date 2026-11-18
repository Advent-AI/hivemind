"""Independent validation of stored scores and candidate ordering, with mutants."""
import copy,importlib.util,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=Path('/Users/lchingen/hivemind');sys.path.insert(0,str(ROOT/'src'))
s=importlib.util.spec_from_file_location('preparer',HERE/'probe_prepare.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
def check(manifest,vectors):
 if not manifest or not vectors:raise ValueError('empty data')
 articles,questions,_=p.run.step1_records(str(p.SOURCE/'step1/trace.sqlite'));records={r['id']:r for a in articles for r in a};saved=json.loads((p.STEP/'library.json').read_text()); groups=saved['groups']; checked=0
 for item in manifest:
  rec=records[item['id']];keys=[p.cmp.query_text(rec,questions[t]) for t in rec['thesis_ids']]
  if not rec['thesis_ids'] or rec.get('figures'):keys.append(p.cmp.doc_text(rec))
  if len(keys)!=len(item['queries']):raise ValueError('query count mismatch')
  union=[]; origin={g:[] for g in item['candidates']}
  for index,(key,row) in enumerate(zip(keys,item['queries']),1):
   q=vectors[key];expect='thesis search' if index<=len(rec['thesis_ids']) else 'own-text search'
   if row['type']!=expect or row['vector_sha256']!=p.digest(q):raise ValueError('query identity or type mismatch')
   def cosine(a,b):return math.fsum(x*y for x,y in zip(a,b))/(math.sqrt(math.fsum(x*x for x in a))*math.sqrt(math.fsum(x*x for x in b)))
   scores={g:cosine(q,vectors[p.cmp.doc_text(groups[g]['original'])]) for g in item['group_order']}
   rank=sorted(item['group_order'],key=lambda g:-scores[g])[:p.cmp.TOP]
   if rank!=row['ranked_top10']:raise ValueError('ranking mismatch')
   for g in item['candidates']:
    if abs(row['scores'][g]-scores[g])>1e-12:raise ValueError('score mismatch')
    if g in rank:origin[g].append(index)
   union += [g for g in rank if g not in union];checked+=1
  if union!=item['candidates'] or origin!=item['origins']:raise ValueError('union or origins mismatch')
  for i,g in enumerate(item['candidates']):
   added='\nRetrieval metadata (not part of the stored piece; cosine, not a probability): '+'; '.join(f"query {j} [{row['type']}]: {row['scores'][g]:.4f}" for j,row in enumerate(item['queries'],1))
   if item['treatment']['questions'][f'q{i}']['instructions']!=item['control']['questions'][f'q{i}']['instructions']+added:raise ValueError('treatment metadata mismatch')
 return checked
m=json.loads((HERE/'probe-manifest.json').read_text());v=json.loads((p.STEP/'embeddings.json').read_text());print('independent query scores and rank lists checked',check(m,v))
for kind in ('vector','score','origin','candidate','missing'):
 mm=copy.deepcopy(m);vv=dict(v)
 if kind=='vector':
  articles,q,_=p.run.step1_records(str(p.SOURCE/'step1/trace.sqlite'));r=next(r for a in articles for r in a if r['id']==mm[0]['id']);key=p.cmp.query_text(r,q[r['thesis_ids'][0]]) if r['thesis_ids'] else p.cmp.doc_text(r);vv[key]=[x+0.5 for x in vv[key]]
 if kind=='score':mm[0]['queries'][0]['scores'][mm[0]['candidates'][0]]+=0.1
 if kind=='origin':mm[0]['origins'][mm[0]['candidates'][0]]=[]
 if kind=='candidate':mm[0]['candidates'][0]='missing'
 if kind=='missing':vv={}
 try:check(mm,vv)
 except (ValueError,KeyError):print('independent negative control caught:',kind)
 else:raise RuntimeError('mutant survived '+kind)
