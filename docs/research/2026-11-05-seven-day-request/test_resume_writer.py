"""A crash after a real writer commit must not resend extraction or write twice."""
import copy,json,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path[:0]=[str(HERE),str(ROOT/'src')]
import split_seven_day_poc as p
import split_v2_fixtures as fixtures
from hivemind.views import matching,round as rounds,store

def main():
 original_select=p.select_manifest;original_call=p.call;original_match=rounds._match;original_judge=rounds.judge_day;original_write=p.write
 chosen='gnews:69d682468e018e0065df5180';old=p.REUSE/'items'/'1211';responses={arm:p.read(old/(arm+'-answer.json')) for arm in ('a','b','meta')}
 for c in responses['meta']['candidates']:c.update(year='',due_day='',date_basis='unknown',date_provenance='',rungs=[])
 for group in ('candidates','evidence'):
  responses['meta'][group]={v['id']:{k:x for k,x in v.items() if k!='id'} for v in responses['meta'][group]}
 responses['a']=fixtures.a_v2(responses['a']);responses['meta']=fixtures.meta_v2(responses['meta'],p.universe.load(str(p.ROOT/'poc/universe.json')))
 calls=[]
 def select(pilot=None):
  m=original_select(None);m['input_rows']=[r for r in m['input_rows'] if r['id']==chosen];m['days']=[m['input_rows'][0]['day']];m['pilot_id']=None;return m
 def fake_call(cfg,setting,arm,spec,folder,transport=None):
  calls.append(arm)
  def fake(provider,request):return {'choices':[{'message':{'content':json.dumps(responses[arm])}}],'usage':{}}
  return original_call(cfg,setting,arm,spec,folder,transport=fake)
 def fake_match(conn,archive,cfg,uni,item,seq,result,candidates,evidence,lists,shown,**kwargs):
  outcomes={c['id']:('new',None,[]) for c in candidates}
  linked={(e['id'],v):('new',None,'') for e in evidence for v in e['links'] if v.startswith('v')}
  return matching.Checked(outcomes,linked,[],{})
 def fake_judge(conn,archive,cfg,day,seq,**kwargs):return rounds.RoundResult('day:'+day)
 def interrupted_write(path,value):
  if path.name=='result.json':raise RuntimeError('simulated crash after writer commit')
  return original_write(path,value)
 try:
  p.select_manifest=select;p.call=fake_call;rounds._match=fake_match;rounds.judge_day=fake_judge
  with tempfile.TemporaryDirectory(prefix='resume-real-writer-') as d:
   out=Path(d)/'run';p.preview(out);sha=p.digest((out/'manifest.json').read_bytes());p.write=interrupted_write
   try:p.run(out,sha)
   except RuntimeError as error:assert 'simulated crash' in str(error)
   else:raise AssertionError('crash was not exercised')
   assert sorted(calls)==['a','b','meta']
   conn=store.open_db(str(out/'views.sqlite'));assert store.is_processed(conn,chosen)
   before=conn.execute('select count(*) from views where created_from_input=?',(chosen,)).fetchone()[0]
   evidence_before=conn.execute('select count(*) from evidence where created_from_input=?',(chosen,)).fetchone()[0];conn.close()
   assert before==1 and evidence_before>0
   p.write=original_write;p.run(out,sha,resume=True)
   conn=store.open_db(str(out/'views.sqlite'))
   assert conn.execute('select count(*) from views where created_from_input=?',(chosen,)).fetchone()[0]==before
   assert conn.execute('select count(*) from evidence where created_from_input=?',(chosen,)).fetchone()[0]==evidence_before
   conn.close();assert sorted(calls)==['a','b','meta']
   status=p.read(out/'run-status.json');assert status['status']=='complete' and status['completed']==1
   assert status['completed_items'][chosen]=='written'
   assert status['days'][select()['days'][0]]['routes']['written']==1
  calls.clear()
  with tempfile.TemporaryDirectory(prefix='resume-saved-handover-') as d:
   out=Path(d)/'run';p.preview(out);sha=p.digest((out/'manifest.json').read_bytes())
   def interrupted_match(*args,**kwargs):raise RuntimeError('simulated matching interruption')
   rounds._match=interrupted_match
   try:p.run(out,sha)
   except RuntimeError as error:assert 'simulated matching interruption' in str(error)
   else:raise AssertionError('matching interruption was not exercised')
   assert sorted(calls)==['a','b','meta']
   conn=store.open_db(str(out/'views.sqlite'));assert not store.is_processed(conn,chosen)
   assert conn.execute('select count(*) from handovers where input_id=?',(chosen,)).fetchone()[0]==1;conn.close()
   rounds._match=fake_match;p.run(out,sha,resume=True)
   assert sorted(calls)==['a','b','meta']
   conn=store.open_db(str(out/'views.sqlite'));assert store.is_processed(conn,chosen)
   assert conn.execute('select count(*) from handovers where input_id=?',(chosen,)).fetchone()[0]==1;conn.close()
  calls.clear()
  with tempfile.TemporaryDirectory(prefix='resume-one-arm-') as d:
   out=Path(d)/'run';p.preview(out);sha=p.digest((out/'manifest.json').read_bytes())
   first_failure=[True]
   def unavailable_b(cfg,setting,arm,spec,folder,transport=None):
    if arm=='b' and first_failure[0]:first_failure[0]=False;raise RuntimeError('B unavailable before send')
    return fake_call(cfg,setting,arm,spec,folder,transport)
   p.call=unavailable_b
   try:p.run(out,sha)
   except RuntimeError as error:assert 'B unavailable before send' in str(error)
   else:raise AssertionError('missing B was not exercised')
   assert calls==['a']
   p.run(out,sha,resume=True)
   assert sorted(calls)==['a','b','meta']
   assert p.read(out/'run-status.json')['status']=='complete'
  calls.clear()
  with tempfile.TemporaryDirectory(prefix='resume-review-entry-') as d:
   out=Path(d)/'run';p.preview(out);sha=p.digest((out/'manifest.json').read_bytes())
   original_item_of=p.testdb.item_of
   def missing_source(row):
    item=original_item_of(row);item['source_uri']='';return item
   def crash_before_progress(path,value):
    if path.name=='run-status.json' and value.get('completed_items',{}).get(chosen)=='returned':
     raise RuntimeError('crash after review entry commit')
    return original_write(path,value)
   p.testdb.item_of=missing_source;p.write=crash_before_progress
   try:
    try:p.run(out,sha)
    except RuntimeError as error:assert 'crash after review entry commit' in str(error)
    else:raise AssertionError('review entry crash was not exercised')
    p.write=original_write;p.run(out,sha,resume=True)
    conn=store.open_db(str(out/'views.sqlite'))
    assert conn.execute("select count(*) from review_pool_entries where kind='incomplete_item'").fetchone()[0]==1
    assert p.read(out/'run-status.json')['completed_items'][chosen]=='returned';conn.close()
   finally:p.testdb.item_of=original_item_of;p.write=original_write
 finally:
  p.select_manifest=original_select;p.call=original_call;rounds._match=original_match;rounds.judge_day=original_judge;p.write=original_write
 print('PASS: writer commit survives crash; resume neither repeats A/B/metadata nor duplicates the question or evidence (external model and matching faked).')
if __name__=='__main__':main()
