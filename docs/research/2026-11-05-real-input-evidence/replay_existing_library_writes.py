"""Replay stored experiment extractions through the real matching/writer/reader on isolated prior-library copies."""
import concurrent.futures
import dataclasses
import hashlib
import json
import shutil
import sqlite3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from hivemind import bundle,config,extraction,model,testdb,universe
from hivemind.views import round as rounds,store
BASE=ROOT/'poc/data/pilot-d369-existing-run-20261105'
PRIOR=ROOT/'poc/data/pilot-d369-existing-library-v2/views.sqlite'
ITEMS=ROOT/'poc/data/real-evidence-d369-variants-draft-v1/items.sqlite'
CONTEXT=HERE/'prior-context-68-v1.json'
SNAP=ROOT/'poc/data/pilot-d369-existing-library-v2/snapshot.json'
if len(sys.argv)!=3 or sys.argv[1] not in ('--fake','--send') or not Path(sys.argv[2]).is_absolute():raise SystemExit('usage: --fake|--send /absolute/new-output')
mode,out=sys.argv[1],Path(sys.argv[2])
if out.exists():raise SystemExit('output exists')
if hashlib.sha256(PRIOR.read_bytes()).hexdigest()!=json.loads(SNAP.read_text())['snapshot_db_sha256']:raise SystemExit('prior snapshot hash differs')
contexts={x['variant_id']:x['shown'] for x in json.loads(CONTEXT.read_text())['articles']}
paths=sorted(BASE.glob('draw[123]/*/result.json'))
if len(paths)!=18 or any(json.loads(p.read_text())['status']!='ok' for p in paths):raise SystemExit('all 18 answers required')
out.mkdir(parents=True)
cfg=config.load(ROOT/'poc/config/poc-v117.json');uni=universe.load(ROOT/'poc/universe.json')

def run(path):
 result=json.loads(path.read_text());intent=json.loads((path.parent/'intent.json').read_text());tag=path.parent.parent.name+'-'+path.parent.name
 d=out/tag;d.mkdir();shutil.copyfile(PRIOR,d/'views.sqlite')
 conn=store.open_db(str(d/'views.sqlite'));db=sqlite3.connect(ITEMS.resolve().as_uri()+'?mode=ro',uri=True);db.row_factory=sqlite3.Row
 item=testdb.item_of(db.execute('select * from items where input_id=?',(intent['input_id'],)).fetchone())
 shown=extraction.shown_views(conn,cfg,item,[o['value'] for o in item['object_identifiers'] if uni.has(o['value'])])
 if shown!=contexts[item['input_id']]:raise ValueError('shown context mismatch')
 sift=extraction.sift_with_groups(result['answer'],item,item['text'],{v['view_id'] for v in shown},uni)
 answer=type('StoredAnswer',(),{'call_id':0,'request_sha256':intent['request_identity'],'cached':False,'cost_usd':0.0})()
 h=extraction.file_reading(extraction.Reading(*sift,answer,cfg.extraction_setting(item['category']).prompt_version.rpartition('-')[2]),item,shown)
 actual={'evidence':h.evidence,'candidates':h.candidates,'dropped':[list(x) for x in h.dropped],'new_groups':h.new_groups}
 if actual!=result['handover']:raise ValueError('handover mismatch')
 archive=model.Archive(str(d/'archive.sqlite'))
 def fake(*args):
  if len(args)!=1:raise RuntimeError('fake replay refuses generative external call')
  request=args[0];answers={}
  for key,q in request['questions'].items():
   if q['type']=='noul':answers[key]={'type':'noul','noul':0.9}
   else:
    labels=q['criteria'];choice='different' if 'different' in labels else list(labels)[-1]
    answers[key]={'type':'choice','choice':choice,'confidence':1.0,'probabilities':{label:float(label==choice) for label in labels}}
  return {'model':request['model'],'answers':answers,'usage':{}}
 runresult=rounds.run(conn,archive,cfg,uni,item,1205,extractor=lambda *a,**kw:h,transport=fake if mode=='--fake' else None,log=lambda *a:None)
 new_sources=[dict(r) for r in conn.execute('select evidence_id,input_id,seq from evidence_sources where seq=1205 and input_id=?',(item['input_id'],))]
 new_ids={r['evidence_id'] for r in new_sources}
 links=[dict(r) for r in conn.execute('select evidence_id,view_id,seq from evidence_links where seq=1205')]
 view_ids=sorted({r['view_id'] for r in links if r['evidence_id'] in new_ids})
 read=[]
 for view_id in view_ids:
  v=bundle.view_bundle(conn,bundle.item_lookup(db),view_id)
  read.append({'view_id':view_id,'question':v['question'],'new_evidence':[e for e in v['evidence'] if e['id'] in new_ids]})
 summary={'mode':mode,'intent':intent,'result':dataclasses.asdict(runresult),'new_sources':new_sources,'new_links':links,'reader_views':read}
 (d/'reader.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 conn.close();archive.conn.close();db.close()
 return {'mode':mode,'tag':tag,'failed':runresult.failed,'handover':len(h.evidence),'new_sources':len(new_sources),'reader_evidence':sum(len(v['new_evidence']) for v in read),'new_links':len(links),'reported_match_cost_lower_bound':runresult.cost,'prior_attempt_cost':'unknown'}
def safely_run(path):
 try:
  return run(path)
 except Exception as error:
  return {'mode':mode,'tag':path.parent.parent.name+'-'+path.parent.name,'failed':repr(error)[:500], 'new_sources':0,'reader_evidence':0,'cost':'unknown'}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: summaries=list(pool.map(safely_run,paths))
(out/'summary.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'mode':mode,'cases':len(summaries),'failed':sum(bool(x['failed']) for x in summaries),'new_sources':sum(x['new_sources'] for x in summaries),'reader_links':sum(x['reader_evidence'] for x in summaries)}))
