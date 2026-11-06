"""Saved real A answer through real matching/check/writer and next-day read; fake external Jev."""
import contextlib,copy,json,sqlite3,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path[:0]=[str(HERE),str(ROOT/'src')]
import existing_path as path
from test_existing_writer import fake_jev,copy_ledger
from hivemind import dispatch,extraction,model,pull,research_context,testdb
from hivemind.views import round as rounds,store

ID='gnews:69d682468e018e0065df5180'

def main():
 real=len(sys.argv)==3 and sys.argv[1]=='--real'
 out=Path(sys.argv[2]) if real else None
 if real and out.exists():raise ValueError('output exists')
 if real:out.mkdir(parents=True)
 cfg,uni,_,_=path.build()
 src=testdb.open_db(str(ROOT/'poc/data/parallel-thesis-evidence-input-2026-11-05/items.sqlite'))
 item=testdb.item_of(src.execute('select * from items where input_id=?',(ID,)).fetchone());src.close()
 raw=json.loads((ROOT/'poc/data/start-state-new-question-diagnostic-2026-11-05-v1/gnews_69d682468e018e0065df5180/result.json').read_text())['answer']
 q=raw['questions'][0];e=q['evidence'][1]
 if e['quote'] not in item['text'] or 'Colette Kress' not in e['original_speaker']:raise ValueError('saved source control changed')
 ids=['e'+str(i) for i in range(1,len(q['evidence'])+1)]
 candidate={'id':'c1','kind':'asset','object':'NVDA','looks_at':q['question'],'question':q['question'],'year':'','due_day':'','rungs':[], 'evidence_ids':ids,'group_refs':[]}
 evidence=[]
 for i,x in enumerate(q['evidence']):
  if x['quote'] not in item['text']:raise ValueError('saved A quote absent')
  origin='NVIDIA CFO Colette Kress' if i in (1,2,3) else 'Adam Spatacco'
  evidence.append({'id':ids[i],'quote':x['quote'],'one_line':x['what_it_shows'],'speaker':'Adam Spatacco','original_who':origin,'original_day':'','tier':'party_statement' if i in (1,2,3) else 'third_party_view','event_time':'','links':['c1']})
 # A source-backed B fixture deliberately shares the margin-guidance quote with A;
 # it represents the same article, not a second independent source.
 b=dict(evidence[2],id='e7',links=['v6'])
 handover=extraction.Handover(evidence if real else evidence+[b],[candidate],[],0,'saved-a-only' if real else 'offline-saved-a-and-b-fixture',False,0.0,[])
 with (contextlib.nullcontext(str(out)) if real else tempfile.TemporaryDirectory(prefix='optional-saved-a-')) as tmp:
  ledger=Path(tmp)/'views.sqlite';copy_ledger(ledger);conn=store.open_db(str(ledger));archive=model.Archive(str(Path(tmp)/'archive.sqlite'))
  route=dispatch.route(conn,item,uni)
  if route.kind!='extract':raise ValueError(('unexpected route',route))
  def extractor(*args,**kwargs):return copy.deepcopy(handover)
  result=rounds.run(conn,archive,cfg,uni,item,route.sequence_no,extractor=extractor,transport=None if real else fake_jev)
  if result.failed or result.new_views!=1:raise AssertionError((result.failed,result.new_views))
  view=conn.execute('select view_id,due_day,question from views where created_from_input=?',(ID,)).fetchone()
  if not view or view['due_day']!='' or view['question']!=q['question']:raise AssertionError('new view not preserved')
  pieces=conn.execute('select evidence_id,quote,one_line from evidence where created_from_input=?',(ID,)).fetchall()
  if len(pieces)!=(6 if real else 7):raise AssertionError(('some evidence lost',len(pieces)))
  for source in evidence:
   found=[p for p in pieces if p['quote']==source['quote'] and p['one_line']==source['one_line']]
   if not found or not any(view['view_id'] in store.views_linked_to(conn,p['evidence_id']) for p in found):raise AssertionError(('source or candidate link changed',source['id']))
  if not real and not any('v6' in store.views_linked_to(conn,p['evidence_id']) for p in pieces):raise AssertionError('B fixture not linked')
  pull.end_of_day(conn,'2026-08-29',route.sequence_no)
  if not store.is_open(conn,view['view_id']):raise AssertionError('unknown date closed')
  store.complete_day(conn,'2026-08-29',route.sequence_no,'2026-08-29T23:59:59Z');conn.commit()
  next_item=dict(item,publication_day='2026-08-30')
  shown=extraction.shown_views(conn,cfg,next_item,['NVDA'])
  if not any(v['view_id']==view['view_id'] and v['question']==q['question'] for v in shown):raise AssertionError('next day misses question')
  with research_context.Reader(str(ledger),route.sequence_no+1,['NVDA'],uni) as reader:
   reader.catalog();got=reader.expand([view['view_id']])['evidence']
   if len([x for x in got if x['evidence_id'] in {p['evidence_id'] for p in pieces}])!=6:raise AssertionError('reader misses A evidence')
  if real:
   (out/'result.json').write_text(json.dumps({'view_id':view['view_id'],'question':q['question'],'evidence_ids':[p['evidence_id'] for p in pieces],'source_id':ID,'starting_questions':68,'real_matching':True,'actual_b_call':False,'day_end':'simulated completion with no daily judgement','notes':'Saved A result; manual source metadata; all A evidence preserved. Not a seven-day run.'},indent=2)+'\n')
   print('REAL MATCH:',view['view_id'],'with',len(pieces),'evidence, next-day reader sees both. Saved A only; B and daily judgement not run.',flush=True)
  else:print('PASS: saved real A question, all six article passages and one source-backed B fixture -> real matching/check/writer -> next-day question and evidence reader; external Jev is simulated; same source is not an independent second outlet.')
  archive.conn.close();conn.close()
if __name__=='__main__':main()
