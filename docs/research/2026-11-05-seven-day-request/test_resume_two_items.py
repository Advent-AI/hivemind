"""D375: a resumed writer's new question reaches both calls for the next item."""
import copy,json,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path[:0]=[str(HERE),str(ROOT/'src')]
import split_seven_day_poc as p
import split_v2_fixtures as fixtures
from hivemind.views import matching,round as rounds,store

def main():
 chosen=['gnews:dbbde813240d4096829a72a9','gnews:69d682468e018e0065df5180']
 old=p.REUSE/'items';saved={i:{a:p.read(old/s/(a+'-answer.json')) for a in ('a','b','meta')} for i,s in enumerate(('1210','1211'))}
 for row in saved.values():
  for c in row['meta']['candidates']:c.update(year='',due_day='',date_basis='unknown',date_provenance='',rungs=[])
  for group in ('candidates','evidence'):
   row['meta'][group]={v['id']:{k:x for k,x in v.items() if k!='id'} for v in row['meta'][group]}
 question=saved[0]['a']['questions'][0]['question'];calls=[];second_seen=[]
 original_select=p.select_manifest;original_call=p.call;original_match=rounds._match;original_judge=rounds.judge_day;original_write=p.write
 def select(pilot=None):
  m=original_select(None);byid={r['id']:r for r in m['input_rows']};m['input_rows']=[byid[i] for i in chosen];m['days']=[m['input_rows'][0]['day']];m['pilot_id']=None;return m
 def fake_call(cfg,setting,arm,spec,folder,transport=None):
  shown=p.read(folder/'shown.json');article=spec[1];index=0 if chosen[0] in article else 1
  if arm=='meta':index=0
  calls.append((index,arm))
  if index==1:
   q=[v['view_id'] for v in shown if v['question']==question];assert len(q)==1;second_seen.append((arm,q[0]))
   if arm=='a':answer={'questions':[]}
   else:
    answer=copy.deepcopy(saved[1]['b']);answer['evidence']=answer['evidence'][:1];answer['evidence'][0]['links']=q
  else:answer=copy.deepcopy(saved[0][arm])
  answer=fixtures.a_v2(answer) if arm=='a' else fixtures.meta_v2(answer,p.universe.load(str(p.ROOT/'poc/universe.json'))) if arm=='meta' else answer
  def fake(provider,request):return {'choices':[{'message':{'content':json.dumps(answer)}}],'usage':{}}
  return original_call(cfg,setting,arm,spec,folder,transport=fake)
 def fake_match(conn,archive,cfg,uni,item,seq,result,candidates,evidence,lists,shown,**kwargs):
  return matching.Checked({c['id']:('new',None,[]) for c in candidates},{(e['id'],v):('new',None,'') for e in evidence for v in e['links'] if v.startswith('v')},[],{})
 def fake_judge(conn,archive,cfg,day,seq,**kwargs):return rounds.RoundResult('day:'+day)
 def interrupted_write(path,value):
  if path.name=='result.json':raise RuntimeError('crash after first writer')
  return original_write(path,value)
 try:
  p.select_manifest=select;p.call=fake_call;rounds._match=fake_match;rounds.judge_day=fake_judge
  with tempfile.TemporaryDirectory(prefix='resume-two-items-') as d:
   out=Path(d)/'run';p.preview(out);sha=p.digest((out/'manifest.json').read_bytes());p.write=interrupted_write
   try:p.run(out,sha)
   except RuntimeError as error:assert 'crash after first writer' in str(error)
   else:raise AssertionError('first writer crash not exercised')
   p.write=original_write;p.run(out,sha,resume=True)
   assert sorted(arm for i,arm in calls if i==0)==['a','b','meta']
   assert sorted(arm for i,arm in calls if i==1)==['a','b']
   assert len(second_seen)==2 and len({i for _,i in second_seen})==1
   target=second_seen[0][1];conn=store.open_db(str(out/'views.sqlite'))
   rows=list(conn.execute('select evidence_id from evidence where created_from_input=?',(chosen[1],)))
   assert rows and any(target in store.views_linked_to(conn,row[0]) for row in rows)
   assert p.read(out/'run-status.json')['completed']==2;conn.close()
 finally:
  p.select_manifest=original_select;p.call=original_call;rounds._match=original_match;rounds.judge_day=original_judge;p.write=original_write
 print('PASS: after crash and resume, next same-day A and B see the first question and B evidence writes to it (models and matching faked).')
if __name__=='__main__':main()
