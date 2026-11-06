"""Replay saved split answers through the current POC adapter without model calls."""
import collections,json,sqlite3,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path[:0]=[str(HERE),str(ROOT/'src')]
import split_seven_day_poc as p
from hivemind import model,testdb

def main():
 cfg,uni,_,_=p.prior.build();views=sqlite3.connect(p.REUSE/'snapshot/views.sqlite');items=testdb.open_db(str(p.INPUT));counts=collections.Counter();bad=[]
 for folder in sorted((p.REUSE/'items').iterdir(),key=lambda x:int(x.name)):
  if not all((folder/(arm+'-answer.json')).exists() for arm in ('a','b')):continue
  row=views.execute('select input_id from handovers where seq=?',(int(folder.name),)).fetchone()
  if not row:counts['skipped_missing_handover']+=1;continue
  raw=items.execute('select * from items where input_id=?',(row[0],)).fetchone()
  if not raw:raise RuntimeError('missing source '+row[0])
  item=testdb.item_of(raw);shown=p.read(folder/'shown.json');a=p.read(folder/'a-answer.json');b=p.read(folder/'b-answer.json')
  mf=folder/'meta-answer.json'
  if not mf.exists() and a['questions']:counts['skipped_missing_metadata']+=1;continue
  meta=p.read(mf) if mf.exists() else {'candidates':[],'evidence':[]}
  for c in meta['candidates']:
   for key,value in [('year',''),('due_day',''),('date_basis','unknown'),('date_provenance',''),('rungs',[])]:c.setdefault(key,value)
  _,requests=p.item_requests(cfg,uni,item,shown)
  for arm,answer,schema in [('a',a,requests['a'][2]),('b',b,requests['b'][2]),('meta',meta,p.meta_schema())]:
   errors=model.check_schema(answer,schema)
   if errors:raise RuntimeError(str(folder)+' '+arm+' schema: '+str(errors))
  try:h=p.build_handover(item,shown,uni,a,b,meta)
  except Exception as error:bad.append({'seq':int(folder.name),'input_id':row[0],'error':str(error)});continue
  counts['answers_replayed']+=1;counts['candidates']+=len(h.candidates);counts['evidence_kept']+=len(h.evidence);counts['evidence_dropped']+=len(h.dropped)
 views.close();items.close();result={'counts':dict(counts),'adapter_refusals':bad,'scope':'stored A/B/metadata answers with original shown lists, optional fields blank when not in old metadata; not a replay of new prompts or live model behavior'}
 (HERE/'preflight-split-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2));return bool(bad) or not counts['answers_replayed']
if __name__=='__main__':sys.exit(main())
