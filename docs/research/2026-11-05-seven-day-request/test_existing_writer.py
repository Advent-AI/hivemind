"""Source-backed A-pass/B handover through real matching checks and writer with fake Jev."""
import copy,json,sqlite3,tempfile,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path[:0]=[str(HERE),str(ROOT/'src')]
import existing_path as path
from hivemind import dispatch,extraction,model,research_context
from hivemind.views import round as rounds,store,writing


def fake_jev(request):
 answers={}
 for key,q in request['questions'].items():
  if q['type']=='choice':
   choices=q['criteria'];label='different' if 'different' in choices else next(iter(choices))
   answers[key]={'type':'choice','choice':label,'probabilities':{k:1.0 if k==label else 0.0 for k in choices},'confidence':1.0}
  elif q['type']=='noul':answers[key]={'type':'noul','noul':0.0}
  else:raise ValueError('unexpected fake question type')
 return {'answers':answers,'usage':{'input_tokens':0,'output_tokens':0}}


def copy_ledger(dest):
 source=sqlite3.connect(path.SNAP.resolve().as_uri()+'?mode=ro',uri=True);target=sqlite3.connect(str(dest));source.backup(target);target.close();source.close()


def fake_handover(cfg,uni,r):
 raw=path.fake_controls(cfg,uni,r);h,_=path.check(raw,r,uni)
 return extraction.Handover(h['evidence'],h['candidates'],h['dropped'],0,'fake-pair',False,0.0,h['new_groups'])


def run_case(mode,cfg,uni,r,h,folder):
 ledger=folder/(mode+'.sqlite');copy_ledger(ledger);conn=store.open_db(str(ledger));archive=model.Archive(str(folder/(mode+'-archive.sqlite')))
 item=copy.deepcopy(r['item']);variant=item['input_id'];shown=extraction.shown_views(conn,cfg,item,[o['value'] for o in item['object_identifiers'] if uni.has(o['value'])])
 if shown!=r['shown'] or store.last_completed_day(conn)!='2026-08-28':raise AssertionError('prior ledger state mismatch')
 route=dispatch.route(conn,item,uni)
 if route.kind!='extract':raise AssertionError(('route',route.kind,route.reason))
 def extractor(*args,**kwargs):return copy.deepcopy(h)
 def bad_match(req):return {'answers':{},'usage':{}}
 transport=bad_match if mode=='matching_failure' else fake_jev
 original=writing._store_piece
 if mode=='writer_failure':
  def fail_after_write(*args,**kwargs):
   original(*args,**kwargs);raise RuntimeError('injected writer failure')
  writing._store_piece=fail_after_write
 try:result=rounds.run(conn,archive,cfg,uni,item,route.sequence_no,transport=transport,extractor=extractor)
 finally:writing._store_piece=original
 count=lambda:conn.execute('select count(*) from evidence where created_from_input=?',(variant,)).fetchone()[0]
 if mode in ('writer_failure','matching_failure'):
  if not result.failed or count()!=0:raise AssertionError((mode,'failure did not roll back',result.failed,count()))
  resumed=dispatch.route(conn,item,uni)
  if resumed.kind!='extract' or resumed.sequence_no!=route.sequence_no or resumed.resume_from not in ('matched','written'):raise AssertionError(('bad resume',resumed))
  result=rounds.run(conn,archive,cfg,uni,item,route.sequence_no,resume_from=resumed.resume_from,transport=fake_jev,extractor=extractor)
 if result.failed or count()!=1:raise AssertionError((mode,'no successful single write',result.failed,count()))
 stored=dict(conn.execute('select * from evidence where created_from_input=?',(variant,)).fetchone())
 if stored['quote']!=h.evidence[0]['quote'] or stored['one_line']!=h.evidence[0]['one_line'] or stored['original_who']!=h.evidence[0]['original_who']:raise AssertionError('stored evidence changed')
 if 'v22' not in store.views_linked_to(conn,stored['evidence_id']):raise AssertionError('wrong question')
 src=conn.execute('select input_id from evidence_sources where evidence_id=?',(stored['evidence_id'],)).fetchall()
 if len(src)!=1 or src[0]['input_id']!=variant:raise AssertionError('source identity wrong')
 if dispatch.route(conn,item,uni).kind!='skipped' or count()!=1:raise AssertionError('committed item duplicated on retry')
 # This marker is a controlled test fixture, not a completed production daily judgement.
 store.complete_day(conn,'2026-08-29',route.sequence_no,'2026-08-29T23:59:59Z');conn.commit();next_item=dict(item,publication_day='2026-08-30')
 next_shown=extraction.shown_views(conn,cfg,next_item,[o['value'] for o in item['object_identifiers'] if uni.has(o['value'])])
 if not any(x['view_id']=='v22' for x in next_shown):raise AssertionError('next-day question not shown')
 with research_context.Reader(str(ledger),route.sequence_no+1,['NVDA'],uni) as reader:
  reader.catalog();expanded=reader.expand(['v22'])
  if not any(x['evidence_id']==stored['evidence_id'] for x in expanded['evidence']):raise AssertionError('next boundary cannot read evidence')
 archive.conn.close();conn.close();print(mode,'passed; one stored evidence, v22 linked; fake Jev; synthetic completion marker',flush=True)


def main():
 cfg,uni,r,_=path.build();h=fake_handover(cfg,uni,r)
 with tempfile.TemporaryDirectory(prefix='existing-writer-proof-') as tmp:
  folder=Path(tmp)
  for mode in ('positive','matching_failure','writer_failure'):run_case(mode,cfg,uni,r,h,folder)
 print('No real Jev, judgement, production ledger, or seven-day run.',flush=True)
if __name__=='__main__':main()
