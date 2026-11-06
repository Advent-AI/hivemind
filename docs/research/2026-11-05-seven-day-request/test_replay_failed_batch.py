"""Replay every first-batch stored answer after opening research subjects; no model calls."""
import copy,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path[:0]=[str(HERE),str(ROOT/'src')]
import split_seven_day_poc as p
from test_existing_writer import copy_ledger,fake_jev
from hivemind import dispatch,extraction,model,testdb,universe
from hivemind.views import round as rounds,store

def main():
 cfg=p.config.load(str(ROOT/'poc/config/poc-v117.json'));uni=universe.load(str(ROOT/'poc/universe.json'));db=testdb.open_db(str(p.INPUT))
 with tempfile.TemporaryDirectory(prefix='split-replay-subject-') as d:
  ledger=Path(d)/'views.sqlite';copy_ledger(ledger);conn=store.open_db(str(ledger));archive=model.Archive(str(Path(d)/'archive.sqlite'))
  source=store.open_read_only(str(p.REUSE/'views.sqlite'))
  for seq in (1205,1206,1207,1208):
   row=source.execute("select input_id from processing_steps where sequence_no=? and step='dispatched'",(seq,)).fetchone()
   item=testdb.item_of(db.execute('select * from items where input_id=?',(row['input_id'],)).fetchone());folder=p.REUSE/'items'/str(seq)
   shown=extraction.shown_views(conn,cfg,item,[o['value'] for o in item['object_identifiers'] if uni.has(o['value'])])
   if shown!=p.read(folder/'shown.json'):raise ValueError('snapshot changed')
   a=p.read(folder/'a-answer.json');b=p.read(folder/'b-answer.json');meta=p.read(folder/'meta-answer.json') if a['questions'] else {'candidates':[],'evidence':[]}
   h=p.build_handover(item,shown,uni,a,b,meta);p.register_subjects(uni,h.candidates)
   route=dispatch.route(conn,item,uni)
   if route.kind!='extract' or route.sequence_no!=seq:raise ValueError(('sequence',route))
   def extractor(*args,**kwargs):return copy.deepcopy(h)
   result=rounds.run(conn,archive,cfg,uni,item,seq,extractor=extractor,transport=fake_jev)
   if result.failed:raise ValueError(result.failed)
   written=conn.execute('select count(*) from views where created_from_input=?',(item['input_id'],)).fetchone()[0]
   if written!=len(h.candidates):raise AssertionError((seq,written,len(h.candidates)))
   print('stored seq',seq,'candidates',len(h.candidates),'evidence',len(h.evidence),flush=True)
  store.complete_day(conn,'2026-08-29',1208,'2026-08-29T23:59:59Z');conn.commit()
  item['publication_day']='2026-08-30';shown=extraction.shown_views(conn,cfg,item,['NVDA'])
  new=[v for v in shown if v['created_seq']>1204]
  if len(new)!=2:raise AssertionError(('next-day missing',len(new)))
  print('PASS: four real stored A/B answers replayed through actual matching and writer; both new research subjects are shown next day. External matching is fake.')
  archive.conn.close();conn.close();source.close();db.close()
if __name__=='__main__':main()
