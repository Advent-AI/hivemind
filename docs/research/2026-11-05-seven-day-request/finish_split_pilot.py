"""Continue the reviewed one-article diagnostic with real matching, writer and daily judging."""
import copy,json,sys,traceback
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path[:0]=[str(HERE),str(ROOT/'src')]
import split_seven_day_poc as poc
from hivemind import config,extraction,model,pull,research_context,testdb,universe
from hivemind.views import matching,round as rounds,store

def main(out):
 manifest=poc.read(out/'manifest.json');status=poc.read(out/'run-status.json')
 if not manifest['pilot_id'] or status['status']!='awaiting_source_review':raise ValueError('not awaiting pilot review')
 if poc.select_manifest(manifest['pilot_id'])!=manifest:raise ValueError('frozen pilot runtime changed')
 folder=out/'items'/str(status['pilot_sequence'])
 if not (folder/'source-review.zh.md').exists():raise ValueError('source review absent')
 cfg=config.load(str(ROOT/'poc/config/poc-v118.json'));uni=universe.load(str(ROOT/'poc/universe.json'))
 items=testdb.open_db(str(poc.INPUT));item=testdb.item_of(items.execute('select * from items where input_id=?',(manifest['pilot_id'],)).fetchone());items.close()
 shown=poc.read(folder/'shown.json');a=poc.read(folder/'a-answer.json');b=poc.read(folder/'b-answer.json');meta=poc.read(folder/'meta-answer.json')
 h=poc.build_handover(item,shown,uni,a,b,meta);saved=poc.read(folder/'handover.json')
 if saved!={'candidates':h.candidates,'evidence':h.evidence,'dropped':[list(x) for x in h.dropped]}:raise ValueError('handover changed')
 conn=store.open_db(str(out/'views.sqlite'));archive=model.Archive(str(out/'match-judge-archive.sqlite'))
 try:
  status['status']='matching';poc.write(out/'run-status.json',status)
  poc.register_subjects(uni,h.candidates,conn)
  def extractor(*args,**kwargs):return copy.deepcopy(h)
  seq=status['pilot_sequence'];result=rounds.run(conn,archive,cfg,uni,item,seq,extractor=extractor,shown_views=shown)
  if result.failed:raise RuntimeError(result.failed)
  created=[dict(r) for r in conn.execute('select view_id,question,due_day from views where created_from_input=?',(item['input_id'],))]
  evidence=[dict(r) for r in conn.execute('select evidence_id,quote,one_line,original_who,original_day,tier from evidence where created_from_input=?',(item['input_id'],))]
  for e in evidence:e['linked_views']=store.views_linked_to(conn,e['evidence_id'])
  status['status']='daily_judging';status['created']=created;status['evidence']=evidence;poc.write(out/'run-status.json',status)
  judged=rounds.judge_day(conn,archive,cfg,item['publication_day'],seq,log=print)
  if judged.failed:raise RuntimeError(judged.failed)
  starting_seq=store.day_start_seq(conn,item['publication_day'])
  unresolved=[r[0] for r in conn.execute('select view_id from views where created_seq>?',(starting_seq,))]
  closed=pull.end_of_day(conn,item['publication_day'],seq,unresolved_views=unresolved);store.complete_day(conn,item['publication_day'],seq,item['publication_day']+'T23:59:59Z');conn.commit()
  next_q=poc.latest_library(conn,seq+1)
  next_ids={q['view_id'] for q in next_q};targets=sorted({v for e in evidence for v in e['linked_views']})
  with research_context.Reader(str(out/'views.sqlite'),seq+1,['NVDA'],uni) as reader:
   reader.catalog();visible=reader.expand(targets)['evidence'] if targets else []
  found=[e['evidence_id'] for e in visible if e['evidence_id'] in {x['evidence_id'] for x in evidence}]
  status.update(status='complete_diagnostic',judged=judged.judged,closed=closed,next_day_new_questions=[v for v in created if v['view_id'] in next_ids],next_day_evidence_ids=found,disclosed_issue='Five B original dates not established by source; original model outputs and raw dates preserved.')
  status['days'][item['publication_day']]['processed']=1;status['completed']=1;poc.write(out/'run-status.json',status)
  print('Pilot complete:',len(created),'new questions,',len(evidence),'stored evidence,',judged.judged,'daily judgements,',len(found),'read next day; B date defect disclosed.',flush=True)
 except Exception as error:
  status['status']='failed';status['failures'].append({'error':repr(error),'traceback':traceback.format_exc()});poc.write(out/'run-status.json',status);raise
 finally:archive.conn.close();conn.close()
if __name__=='__main__':main(Path(sys.argv[1]))
