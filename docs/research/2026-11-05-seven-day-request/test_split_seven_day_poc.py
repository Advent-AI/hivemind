"""Offline controls for split POC: actual saved A, article and day-start ledger."""
import copy,json,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path[:0]=[str(HERE),str(ROOT/'src')]
import split_seven_day_poc as poc
import split_v2_fixtures as fixtures
from hivemind import extraction,testdb


def main():
 cfg,uni,_,_=poc.prior.build();db=testdb.open_db(str(poc.INPUT));item=testdb.item_of(db.execute('select * from items where input_id=?',('gnews:69d682468e018e0065df5180',)).fetchone());db.close()
 conn=poc.prior.b_arm.prior.ro(poc.prior.SNAP);shown=extraction.shown_views(conn,cfg,item,['NVDA']);conn.close()
 setting,reqs=poc.item_requests(cfg,uni,item,shown)
 # The stopped real run opened Alphabet and Oracle topics on Aug 29. Its original
 # Aug 30 item did not show them because its upstream tag was only NVDA.
 snapshot=poc.store.open_read_only(str(ROOT/'poc/data/split-seven-day-optional-2026-11-05-v3/snapshot/views.sqlite'))
 saved_item=json.loads((ROOT/'poc/data/split-seven-day-optional-2026-11-05-v3/items/1244/shown.json').read_text())
 later=dict(item,publication_day='2026-08-30')
 all_shown=poc.latest_library(snapshot,1244)
 assert not {'v77','v80'} & {v['view_id'] for v in saved_item}
 assert {'v77','v80'} <= {v['view_id'] for v in all_shown}
 assert any(v['object_kind']=='theme' for v in all_shown)
 before_second=poc.latest_library(snapshot,1211)
 ids={v['view_id'] for v in before_second}
 assert 'v72' in ids and 'v73' not in ids
 assert 'v72' not in {v['view_id'] for v in extraction.shown_views(snapshot,cfg,item,['NVDA'])}
 _,fresh_requests=poc.item_requests(cfg,uni,item,before_second)
 for arm in ('a','b'):
  assert '[Open questions immediately before this item]' in fresh_requests[arm][1]
  assert 'v72' in fresh_requests[arm][1] and 'v73' not in fresh_requests[arm][1]
 snapshot.close()
 a=poc.read(ROOT/'poc/data/start-state-new-question-diagnostic-2026-11-05-v1/gnews_69d682468e018e0065df5180/result.json')['answer']
 q=a['questions'][0];meta={'candidates':[{'id':'c1','object':'NVDA','kind':'asset'}],'evidence':[]}
 for i,e in enumerate(q['evidence'],1):meta['evidence'].append({'id':'e'+str(i),'speaker':'Adam Spatacco','original_who':'NVIDIA' if i in (2,3,4) else 'Adam Spatacco','original_day':'','tier':'party_statement' if i in (2,3,4) else 'third_party_view','event_time':''})
 b={'evidence':[{'id':'original','quote':q['evidence'][2]['quote'],'one_line':q['evidence'][2]['what_it_shows'],'speaker':'Adam Spatacco','original_who':'NVIDIA','original_day':'','tier':'party_statement','event_time':'','links':['v6']}]}
 h=poc.build_handover(item,shown,uni,a,b,meta)
 assert len(h.candidates)==1 and len(h.evidence)==7 and h.candidates[0]['due_day']=='' and h.candidates[0]['rungs']==[]
 assert all(e['links']==['c1'] for e in h.evidence[:6]) and h.evidence[-1]['links']==['v6']
 assert [e['quote'] for e in h.evidence[:6]]==[x['quote'] for x in q['evidence']]
 assert poc.explicit_day('2026-09-04','Friday, September 4, 2026')
 assert poc.explicit_day('2027-01-31','January 31, 2027')
 assert not poc.explicit_day('2027-02-01','around February 2027')
 assert not poc.explicit_day('2027-01-31','Revenue grew 31 percent in January 2027')
 assert not poc.explicit_day('2027-02-01','01/02/2027')
 optional=copy.deepcopy(meta)
 optional['candidates'][0].update(year='FY2027',due_day='2027-03-01',date_basis='analyst_check',date_provenance='March 1, 2027',rungs=[{'label':'Yes','condition':'The reported commitments exceed $250 billion','lo':None,'hi':None},{'label':'No','condition':'The reported commitments are at most $250 billion','lo':None,'hi':None}])
 a_with_check=copy.deepcopy(a);a_with_check['questions'][0]['question']='Will NVIDIA report FY2027 commitments above $250 billion?';a_with_check['questions'][0]['how_and_when_to_check']+=' Analyst check: March 1, 2027.'
 dated=poc.build_handover(item,shown,uni,a_with_check,b,optional)
 assert dated.candidates[0]['due_day']=='2027-03-01' and dated.candidates[0]['year']=='FY2027' and len(dated.candidates[0]['rungs'])==2
 optional['candidates'][0].update(due_day='2027-02-01',date_provenance='around February 2027')
 approximate=poc.build_handover(item,shown,uni,a,b,optional)
 assert approximate.candidates[0]['due_day']=='' and len(approximate.candidates)==1
 original="Nvidia's H100 and B200 processors are included."
 assert poc.source_quote('Nvidia’s H100 and B200 processors are included.',original)==original
 assert poc.source_quote('Nvidia’s H200 and B200 processors are included.',original) is None
 assert poc.source_quote('   ',original) is None
 assert poc.source_quote('20%', 'The company changed by -20%.') is None
 assert poc.source_quote('5 billion', 'The company reported $5 billion.') is None
 assert poc.source_quote('20%', 'The figure grew 120%.') is None
 assert poc.source_quote('H100', 'The company announced H1000.') is None
 assert poc.source_quote('5 billion', 'The company reported $1.5 billion.') is None
 assert poc.source_quote('500', 'The company reported $1,500.') is None
 assert poc.source_quote('H100', 'The H100 succeeds H1000.') == 'H100'
 actual='On Monday, MediaTek became the latest to embrace Nvidia\'s NVLink Fusion high-speed interconnect technology for its fledgling datacenter XPU offering. In later news, the market changed.'
 slightly_changed='And on Monday, MediaTek became the latest to embrace Nvidia\'s NVLink Fusion high-speed interconnect technology for its fledgling datacenter XPU offering.'
 assert poc.source_quote(slightly_changed,actual)==actual.split(' In later',1)[0]
 assert poc.source_quote(slightly_changed.replace('MediaTek','Amazon'),actual) is None
 unknown=copy.deepcopy(meta);unknown['candidates'][0]['object']='New data-center policy topic';unknown['candidates'][0]['kind']='theme'
 new_h=poc.build_handover(item,shown,uni,a,b,unknown)
 poc.register_subjects(uni,new_h.candidates)
 new_id=new_h.candidates[0]['object']
 assert uni.resolve('New data-center policy topic')==new_id and uni.kind(new_id)=='theme'
 no_subject=copy.deepcopy(meta);no_subject['candidates'][0]['object']=''
 without=poc.build_handover(item,shown,uni,a,b,no_subject)
 poc.register_subjects(uni,without.candidates)
 assert uni.has(without.candidates[0]['object'])
 bad_a=copy.deepcopy(a);bad_a['questions'][0]['evidence'][0]['quote']='not an article passage'
 bad_h=poc.build_handover(item,shown,uni,bad_a,b,meta)
 assert any('quote absent' in reason for _,reason in bad_h.dropped) and len(bad_h.candidates)==1
 no_source=copy.deepcopy(a)
 for e in no_source['questions'][0]['evidence']:e['quote']='not an article passage'
 # split version 2 (2026-11-05): as production's sift (D209), an unsourced candidate is dropped with its reason, not opened and not a stopped run
 unsourced=poc.build_handover(item,shown,uni,no_source,b,meta)
 assert not unsourced.candidates and ('c1','candidate without surviving evidence') in unsourced.dropped
 assert not any(e['links']==['c1'] for e in unsourced.evidence)
 for field in ('link','metadata'):
  bad_a=copy.deepcopy(a);bad_b=copy.deepcopy(b);bad_m=copy.deepcopy(meta)
  if field=='link':bad_b['evidence'][0]['links']=['v999999']
  if field=='metadata':bad_m['evidence'][0]['id']='e999'
  try:poc.build_handover(item,shown,uni,bad_a,bad_b,bad_m)
  except ValueError:pass
  else:raise AssertionError(field+' accepted')
 with tempfile.TemporaryDirectory(prefix='split-poc-fake-') as d:
  out=Path(d)
  for arm,response in [('a',fixtures.a_v2(a)),('b',b)]:
   def fake(provider,request):return {'choices':[{'message':{'content':json.dumps(response)}}],'usage':{}}
   assert poc.call(cfg,setting,arm,reqs[arm],out,transport=fake)==response
   assert poc.completed_answer(cfg,setting,arm,reqs[arm],out)==response
  (out/'a-answer.json').unlink()
  try:poc.completed_answer(cfg,setting,'a',reqs['a'],out)
  except RuntimeError as error:assert 'incomplete' in str(error)
  else:raise AssertionError('uncertain provider call reused')
  run_dir=out/'pilot'
  poc.preview(run_dir,item['input_id'])
  original_call=poc.call
  def fake_call(cfg_,setting_,arm,spec,folder,transport=None):
   answer={'a':a,'b':b,'meta':meta}[arm]
   poc.write(folder/(arm+'-answer.json'),answer)
   return copy.deepcopy(answer)
  try:
   poc.call=fake_call
   poc.run(run_dir,poc.digest((run_dir/'manifest.json').read_bytes()))
  finally:poc.call=original_call
  status=poc.read(run_dir/'run-status.json')
  assert status['status']=='awaiting_source_review' and status['completed']==0
  assert len(poc.read(run_dir/'items'/str(status['pilot_sequence'])/'handover.json')['evidence'])==7
  reused_dir=out/'reused'
  first_id=poc.read(poc.REUSE/'manifest.json')['input_rows'][0]['id']
  poc.preview(reused_dir,first_id)
  first_dir=poc.REUSE/'items'/'1205';calls=[]
  old_a=poc.read(first_dir/'a-answer.json');old_b=poc.read(first_dir/'b-answer.json')
  def no_send(cfg_,setting_,arm,spec,folder,transport=None):
   calls.append(arm)
   return copy.deepcopy({'a':old_a,'b':old_b}[arm])
  try:
   poc.call=no_send
   poc.run(reused_dir,poc.digest((reused_dir/'manifest.json').read_bytes()))
  finally:poc.call=original_call
  reused_status=poc.read(reused_dir/'run-status.json')
  assert reused_status['status']=='awaiting_source_review'
  assert sorted(calls)==['a','b']
  assert not (reused_dir/'items'/str(reused_status['pilot_sequence'])/'reuse.json').exists()
 print('PASS: saved A, source-backed B fixture, 68 day-start questions, real request builder, source/link/identity negative controls and fake provider.')
if __name__=='__main__':main()
