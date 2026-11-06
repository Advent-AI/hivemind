# -*- coding: utf-8 -*-
"""Stored-answer and scratch-writer identity proofs; no semantic scoring or paid calls."""
import copy,hashlib,json,sqlite3,sys,tempfile
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OLD=ROOT/'docs/research/2026-11-05-parallel-thesis-evidence-poc'
sys.path[:0]=[str(HERE),str(OLD),str(ROOT/'src')]
import prepare,run_poc,b_arm,join_identity as ji,a_id_contract
from hivemind import extraction,model
from hivemind.views import matching,store,writing
class Answer:call_id=0;request_sha256='fake';cached=False;cost_usd=0

def binding(execution,r,raw):
 response=json.dumps({'choices':[{'message':{'content':json.dumps(raw)}}]},ensure_ascii=False)
 return {'execution_id':execution,'input_id':r['item']['input_id'],'publication_day':r['item']['publication_day'],'seq':r['seq'],'snapshot_sha256':ji.snapshot_sha(r['shown']),'wire_sha256':ji.wire_sha(r['request']),'raw_answer_sha256':ji.digest(raw),'response':response,'response_sha256':hashlib.sha256(response.encode()).hexdigest()}
def create_pair(a_raw,b_raw,a,b,uni,execution='run-one'):
 plan=ji.register_plan(execution,a,b,'openai')
 return ji.join(execution,a_raw,b_raw,a,b,uni,Answer(),binding(execution,a,a_raw),binding(execution,b,b_raw),plan)
def semantic(h):
 return [{k:e[k] for k in ('quote','one_line','speaker','original_who','original_day','tier','event_time','links')} for e in h['evidence']]
def must_fail(func):
 try:func()
 except ji.JoinRefusal:return
 raise AssertionError('invalid identity accepted')

def actual_b_replay():
 cfg,uni,requests=b_arm.variants();lookup={(r['item']['input_id'],r['variant']):r for r in requests};rows=[json.loads(f.read_text()) for f in (ROOT/'poc/data/parallel-b-link-2026-11-05-v2').glob('*/result.json')]
 assert len(rows)==60;changed=0
 for row in rows:
  r=lookup[(row['id'],row['variant'])];old=run_poc.handover(copy.deepcopy(row['answer']),r,uni,Answer());new=ji.lane_check('existing',row['answer'],r,uni,Answer())['checked']
  if semantic(old)!=semantic(new):raise AssertionError((row['id'],row['variant'],row['draw'],'semantic drift'))
  if [reason.split('same quote as ',1)[0] if reason.startswith('same quote as ') else reason for _,reason in old['dropped']]!=[reason.split('same quote as ',1)[0] if reason.startswith('same quote as ') else reason for _,reason in new['dropped']]:raise AssertionError('drop-class drift')
  if len({e['id'] for e in row['answer']['evidence']})<len(row['answer']['evidence']):changed+=1
 assert changed==1
 row=next(x for x in rows if x['id']=='gnews:8f8a2d115ab834c7026aefd1' and x['variant']=='treatment' and x['draw']==3);r=lookup[(row['id'],row['variant'])]
 old=run_poc.handover(copy.deepcopy(row['answer']),r,uni,Answer());new=ji.lane_check('existing',row['answer'],r,uni,Answer())['checked'];conn=prepare.ro(prepare.INPUT/'views.sqlite')
 keys_old=matching.build_lists(conn,SimpleNamespace(evidence=old['evidence'],candidates=[]),r['shown'],5).evidence_lists
 keys_new=matching.build_lists(conn,SimpleNamespace(evidence=new['evidence'],candidates=[]),r['shown'],5).evidence_lists;conn.close()
 assert len(keys_old)==3 and len(keys_new)==14
 print('60 stored B answers replayed: semantic handover unchanged; one answer had repeated raw IDs.')

def run():
 actual_b_replay();cfg,uni,requests=prepare.prepare();ident='gnews:d144b91986c520ea36e718cf';a=copy.deepcopy(next(x for x in requests if x['arm']=='new' and x['item']['input_id']==ident));b=copy.deepcopy(next(x for x in requests if x['arm']=='existing' and x['item']['input_id']==ident))
 a['schema']=a_id_contract.experimental_schema(a['schema']);a['request']=model.build_request(a['setting'],a['system'],a['user'],a['schema'],'extraction',cfg.provider)
 a_raw=json.loads((ROOT/'poc/data/parallel-thesis-evidence-poc-2026-11-05/gnews_d144b91986c520ea36e718cf-new/result.json').read_text())['answer']
 b_raw={'evidence':[dict(copy.deepcopy(a_raw['evidence'][0]),id='e1',links=[b['shown'][0]['view_id']])]}
 # Same quotation, lane-local e1 in both, distinct targets and preserved provenance.
 joined=create_pair(a_raw,b_raw,a,b,uni);assert len(set(e['id'] for e in joined['evidence']))==len(joined['evidence']);assert joined['exact_quote_overlaps']
 a_ids={x['joined_id'] for x in joined['global_map'] if x['lane']=='new'};b_ids={x['joined_id'] for x in joined['global_map'] if x['lane']=='existing'};assert not a_ids&b_ids
 assert set(joined['candidates'][0]['evidence_ids'])<=a_ids
 duplicate=copy.deepcopy(a_raw);duplicate['evidence'].append(copy.deepcopy(duplicate['evidence'][0]));must_fail(lambda:create_pair(duplicate,b_raw,a,b,uni))
 numeric=copy.deepcopy(b_raw);numeric['evidence'][0]['id']=7;must_fail(lambda:create_pair(a_raw,numeric,a,b,uni))
 other=copy.deepcopy(b);other['seq']+=1;must_fail(lambda:create_pair(a_raw,b_raw,a,other,uni))
 wrong_binding=binding('another-execution',b,b_raw);plan={k:joined['pair'][k] for k in ('execution_id','input_id','publication_day','seq','item_sha256','body_sha256','snapshot_sha256','a_wire_sha256','b_wire_sha256')};must_fail(lambda:ji.join('run-one',a_raw,b_raw,a,b,uni,Answer(),binding('run-one',a,a_raw),wrong_binding,plan))
 wrong_plan=dict(plan,a_wire_sha256='different-request');must_fail(lambda:ji.join('run-one',a_raw,b_raw,a,b,uni,Answer(),binding('run-one',a,a_raw),binding('run-one',b,b_raw),wrong_plan))
 wrong_lane=copy.deepcopy(b);wrong_lane['arm']='new';must_fail(lambda:ji.register_plan('run-one',a,wrong_lane,'openai'))
 wrong_publisher=copy.deepcopy(b);wrong_publisher['item']['publisher_type']='self';must_fail(lambda:ji.register_plan('run-one',a,wrong_publisher,'openai'))
 other_request=copy.deepcopy(b);foreign=next(x for x in requests if x['arm']=='existing' and x['item']['input_id']!=ident);other_request['request']=foreign['request'];must_fail(lambda:ji.register_plan('run-one',a,other_request,'openai'))
 extra_question=copy.deepcopy(b);extra_question['user']=extra_question['user'].replace('\n\n[Research groups]','\n  - v999999: extra unregistered question\n\n[Research groups]',1);extra_question['request']=model.build_request(extra_question['setting'],extra_question['system'],extra_question['user'],extra_question['schema'],'extraction',cfg.provider);must_fail(lambda:ji.register_plan('run-one',a,extra_question,'openai'))
 # Same-quote alias and missing versus present-but-refused raw candidate references.
 source=copy.deepcopy(a_raw);alias=copy.deepcopy(source['evidence'][0]);alias['id']='e99';source['evidence'].append(alias)
 bad=copy.deepcopy(source['evidence'][0]);bad.update(id='e98',quote='Fabricated sentence absent from this source.');source['evidence'].append(bad)
 source['candidates'][0]['evidence_ids']+=['e99','e98','e999']
 mapped=create_pair(source,b_raw,a,b,uni);refs=mapped['a_trace']['candidate_references'];assert next(x for x in refs if x['raw_evidence_id']=='e99')['state']=='merged';assert next(x for x in refs if x['raw_evidence_id']=='e98')['state']=='refused';assert next(x for x in refs if x['raw_evidence_id']=='e999')['source_status']=='absent'
 rejected=copy.deepcopy(a_raw);another=copy.deepcopy(rejected['candidates'][0]);another['id']='c2';rejected['candidates'].append(another);rejected['candidates'][0]['due_day']='2020-01-01'
 for evidence in rejected['evidence']:evidence['links'].append('c2')
 rejected_pair=create_pair(rejected,b_raw,a,b,uni);refs=rejected_pair['a_trace']['candidate_references'];first_ref=next(x for x in refs if x['candidate']=='c1');assert first_ref['candidate_status']=='refused' and first_ref['joined_id'] is None
 view=b['shown'][0]['view_id'];candidate=joined['candidates'][0]['id']
 # Each writer case begins with its own backup of the same later end-state ledger.
 for mode in ('new','merge','skip'):
  first={(e['id'],link):('new',None,'') for e in joined['evidence'] for link in e['links'] if link in joined['shown_ids']}
  second={(e['id'],view):('new',None,'') for e in joined['evidence'] if candidate in e['links']} if mode=='merge' else {}
  envelope={'pair_id':joined['pair_id'],'outcomes':{candidate:(mode,view if mode=='merge' else None,[])},'evidence':first,'second_pass':second};assert ji.validate_decisions(joined,envelope)
  wrong=dict(envelope,pair_id='different-pair');must_fail(lambda:ji.validate_decisions(joined,wrong))
  if mode=='merge':
   missing=dict(envelope,second_pass={});must_fail(lambda:ji.validate_decisions(joined,missing))
  with tempfile.TemporaryDirectory(prefix='hivemind-join-') as tmp:
   path=Path(tmp)/'views.sqlite';src=prepare.ro(prepare.INPUT/'views.sqlite');dest=sqlite3.connect(str(path));src.backup(dest);src.close();dest.close();conn=store.open_db(str(path))
   handover=extraction.Handover(joined['evidence'],joined['candidates'],[],0,joined['pair_id'],False,0,joined['new_groups'])
   target=view
   if mode=='merge':
    target='v9999';c=joined['candidates'][0]
    store.create_view(conn,view_id=target,object_id=c['object'],object_kind=uni.kind(c['object']),kind=c['kind'],looks_at=c['looks_at'],question=c['question'],due_day=c['due_day'],year=c['year'],rungs=c['rungs'],seq=1299,input_id='scratch-existing',created_at='2026-08-29T12:00:00')
    store.add_key(conn,target,c,1299)
   lists=matching.build_lists(conn,handover,a['shown'],5);assert len(lists.evidence_lists)==len(first)
   first_raw={'candidates':[{'id':candidate,'outcome':mode,'target_view_id':target if mode=='merge' else '', 'reason':'synthetic','dependencies':[]}], 'evidence':[{'id':eid,'view_id':vid,'outcome':'new','target_evidence_id':'','said_day':'','reason':'synthetic'} for eid,vid in first]}
   second_raw={'candidates':[], 'evidence':[{'id':e['id'],'view_id':target,'outcome':'new','target_evidence_id':'','said_day':'','reason':'synthetic'} for e in joined['evidence'] if mode=='merge' and candidate in e['links']]}
   package={'pair_id':joined['pair_id'],'write_seq':1300,'first':first_raw,'second':second_raw}
   stale=dict(package,pair_id='different-pair');must_fail(lambda:ji.checked_write(conn,uni,1300,a['item'],joined,a['shown'],stale))
   altered=copy.deepcopy(joined);altered['evidence'][0]['quote']='This sentence was never in the article.';must_fail(lambda:ji.checked_write(conn,uni,1300,a['item'],altered,a['shown'],package))
   unknown_target=copy.deepcopy(package);unknown_target['first']['evidence'][0].update(outcome='repeat',target_evidence_id='e-not-shown');must_fail(lambda:ji.checked_write(conn,uni,1300,a['item'],joined,a['shown'],unknown_target))
   no_target=copy.deepcopy(package);no_target['first']['evidence'][0].update(outcome='replace',target_evidence_id='');must_fail(lambda:ji.checked_write(conn,uni,1300,a['item'],joined,a['shown'],no_target))
   bad_action=copy.deepcopy(package);bad_action['first']['candidates'][0]['outcome']='invented';must_fail(lambda:ji.checked_write(conn,uni,1300,a['item'],joined,a['shown'],bad_action))
   if mode=='merge':
    missing_package=dict(package,second={'candidates':[],'evidence':[]});must_fail(lambda:ji.checked_write(conn,uni,1300,a['item'],joined,a['shown'],missing_package))
   written=ji.checked_write(conn,uni,1300,a['item'],joined,a['shown'],package)
   expected=1 if mode=='skip' else len(joined['evidence']);assert len(written.evidence_ids)==expected,(mode,written)
   for local,stored in written.evidence_ids.items():
    row=store.evidence(conn,stored);original=next(x for x in joined['evidence'] if x['id']==local);assert row['quote']==original['quote']
    assert row['created_from_input']==a['item']['input_id']
    linked=set(store.views_linked_to(conn,stored));assert linked
    if local in b_ids:assert view in linked
    if local in a_ids:
     expected_target=written.new_views[candidate] if mode=='new' else target
     assert expected_target in linked,(mode,local,expected_target,linked)
   if mode=='new':assert candidate in written.new_views
   conn.rollback();conn.close()
  print('scratch writer',mode,'stored',expected,'records; cross-lane source counting remains untested')
 print('Join: lane collisions separated; aliases/rejections traced; wrong-pair, missing merge decisions and invalid raw schema refused.')
if __name__=='__main__':run()
