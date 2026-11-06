# -*- coding: utf-8 -*-
"""Experimental, pair-bound identity join; no investment-relevance decision."""
import copy,hashlib,json
from hivemind import extraction,model,placement
from hivemind.views import matching,writing
import a_id_contract,run_poc
class JoinRefusal(ValueError):pass

def digest(value):
 return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def snapshot_sha(shown):return digest(shown)
def wire_sha(req):return hashlib.sha256(json.dumps(req).encode()).hexdigest()

def register_plan(execution_id,a,b,provider):
 if not execution_id or a['arm']!='new' or b['arm']!='existing':raise JoinRefusal('lane or execution mismatch')
 if a['item']!=b['item'] or a['seq']!=b['seq'] or a['shown']!=b['shown']:raise JoinRefusal('lane inputs differ')
 for r in (a,b):
  req=model.build_request(r['setting'],r['system'],r['user'],r['schema'],'extraction',provider)
  if req!=r['request']:raise JoinRefusal('request differs from prepared inputs')
  body=extraction.item_header(r['item'],r['item']['category'])+r['item']['text']
  header='[Open questions immediately before this item]\n';end='\n\n[Research groups]'
  if r['user'].count(body)!=1 or r['user'].count(header)!=1:raise JoinRefusal('request source or snapshot mismatch')
  tail=r['user'].split(header,1)[1]
  if end not in tail or tail.split(end,1)[0]!='\n'.join(placement.question_lines(r['shown'])):raise JoinRefusal('request question block differs from snapshot')
 return {'execution_id':execution_id,'input_id':a['item']['input_id'],'publication_day':a['item']['publication_day'],'seq':a['seq'],'item_sha256':digest(a['item']),'body_sha256':hashlib.sha256(a['item']['text'].encode()).hexdigest(),'snapshot_sha256':snapshot_sha(a['shown']),'a_wire_sha256':wire_sha(a['request']),'b_wire_sha256':wire_sha(b['request'])}

def lane_check(arm,raw,request,uni,answer):
 schema=request['schema']
 if arm=='new' and schema['properties']['candidates']['items']['properties']['id'].get('pattern')!=r'^c[0-9]+$':raise JoinRefusal('A request lacks experimental identity schema')
 errors=model.check_schema(raw,schema)
 if errors:raise JoinRefusal('raw schema: '+str(errors))
 raw_copy=copy.deepcopy(raw);source=raw_copy['evidence'];raw_sha=digest(raw_copy)
 original_ids=[e['id'] for e in source]
 if arm=='new':
  try:a_id_contract.check_answer(raw_copy,schema)
  except a_id_contract.IdentityRefusal as error:raise JoinRefusal(str(error)) from error
  if len(original_ids)!=len(set(original_ids)):raise JoinRefusal('A duplicate evidence IDs')
  converted=raw_copy
 else:
  converted=copy.deepcopy(raw_copy)
  for i,e in enumerate(converted['evidence'],1):e['id']='e'+str(i)
 original_ref=[]
 if arm=='new':
  present=set(original_ids)
  for candidate in raw_copy['candidates']:
   for evidence_id in candidate['evidence_ids']:
    original_ref.append({'candidate':candidate['id'],'raw_evidence_id':evidence_id,'source_status':'present' if evidence_id in present else 'absent'})
 checked=run_poc.handover(converted,request,uni,answer)
 kept={e['id']:e for e in checked['evidence']}
 drops={}
 for key,reason in checked['dropped']:drops.setdefault(key,[]).append(reason)
 mapping=[]
 for i,e in enumerate(source,1):
  local=e['id'] if arm=='new' else 'e'+str(i)
  reasons=drops.get(local,[]);alias=next((s.split('same quote as ',1)[1].split(';',1)[0] for s in reasons if s.startswith('same quote as ')),None)
  target=alias or local
  state=('merged' if alias else 'kept') if target in kept else ('refused' if reasons else 'not_surviving')
  mapping.append({'lane':arm,'raw_answer_sha256':raw_sha,'ordinal':i,'raw_id':e['id'],'temporary_id':local,'checked_id':target if target in kept else None,'state':state,'reasons':reasons,'raw_record':copy.deepcopy(e)})
 by_raw={m['raw_id']:m for m in mapping} if arm=='new' else {}
 for ref in original_ref:
  if ref['source_status']=='present':
   m=by_raw[ref['raw_evidence_id']];ref.update(checked_id=m['checked_id'],state=m['state'],reasons=m['reasons'])
  candidate_kept=any(c['id']==ref['candidate'] for c in checked['candidates'])
  ref['candidate_status']='kept' if candidate_kept else 'refused'
  ref['candidate_reasons']=drops.get(ref['candidate'],[]) if not candidate_kept else []
 return {'arm':arm,'raw_answer_sha256':raw_sha,'checked':checked,'positions':mapping,'candidate_references':original_ref}

def join(execution_id,a_raw,b_raw,a,b,uni,answer,a_binding,b_binding,plan):
 if not execution_id:raise JoinRefusal('missing execution id')
 fields=('input_id','publication_day')
 for key in fields:
  if a['item'][key]!=b['item'][key]:raise JoinRefusal('item mismatch')
 if a['seq']!=b['seq'] or a['item']['text']!=b['item']['text'] or snapshot_sha(a['shown'])!=snapshot_sha(b['shown']):raise JoinRefusal('source, seq or snapshot mismatch')
 expected_plan=register_plan(execution_id,a,b,'openai')
 if plan!=expected_plan:raise JoinRefusal('pair differs from registered plan')
 for raw,r,binding in ((a_raw,a,a_binding),(b_raw,b,b_binding)):
  if r['request']['response_format']['json_schema']['schema']!=r['schema']:raise JoinRefusal('request and checked schema differ')
  expected={'execution_id':execution_id,'input_id':r['item']['input_id'],'publication_day':r['item']['publication_day'],'seq':r['seq'],'snapshot_sha256':snapshot_sha(r['shown']),'wire_sha256':wire_sha(r['request']),'raw_answer_sha256':digest(raw)}
  if any(binding.get(k)!=v for k,v in expected.items()):raise JoinRefusal('lane binding mismatch')
  response=binding.get('response')
  if not isinstance(response,str) or hashlib.sha256(response.encode()).hexdigest()!=binding.get('response_sha256'):raise JoinRefusal('raw response mismatch')
  try:response_answer=json.loads(json.loads(response)['choices'][0]['message']['content'])
  except (KeyError,IndexError,TypeError,ValueError) as error:raise JoinRefusal('invalid provider response') from error
  if response_answer!=raw:raise JoinRefusal('response and answer differ')
 left=lane_check('new',a_raw,a,uni,answer);right=lane_check('existing',b_raw,b,uni,answer)
 pair=dict(expected_plan,a_raw_answer_sha256=left['raw_answer_sha256'],b_raw_answer_sha256=right['raw_answer_sha256'],a_response_sha256=a_binding['response_sha256'],b_response_sha256=b_binding['response_sha256']);pair_id=digest(pair)
 combined=[];local_to_join={};global_map=[]
 for lane in (left,right):
  for e in lane['checked']['evidence']:
   new_id='e'+str(len(combined)+1);local_to_join[(lane['arm'],e['id'])]=new_id
   combined.append(dict(e,id=new_id));global_map.append({'lane':lane['arm'],'checked_id':e['id'],'joined_id':new_id})
 candidates=[]
 for c in left['checked']['candidates']:
  new_refs=[]
  for ref in c['evidence_ids']:
   key=('new',ref)
   if key not in local_to_join:raise JoinRefusal('A candidate has missing surviving evidence')
   new_refs.append(local_to_join[key])
  candidates.append(dict(c,evidence_ids=new_refs))
 for lane in (left,right):
  for pos in lane['positions']:
   pos['joined_id']=local_to_join.get((lane['arm'],pos['checked_id'])) if pos['checked_id'] else None
 for ref in left['candidate_references']:
  ref['joined_id']=local_to_join.get(('new',ref.get('checked_id'))) if ref.get('checked_id') and ref['candidate_status']=='kept' else None
 overlaps=[{'a_id':x['id'],'b_id':y['id'],'quote':x['quote']} for x in combined[:len(left['checked']['evidence'])] for y in combined[len(left['checked']['evidence']):] if x['quote']==y['quote']]
 result={'pair_id':pair_id,'pair':pair,'shown_ids':{v['view_id'] for v in a['shown']},'evidence':combined,'candidates':candidates,'new_groups':left['checked']['new_groups'],'a_trace':left,'b_trace':right,'global_map':global_map,'exact_quote_overlaps':overlaps}
 result['content_sha256']=content_sha(result)
 return result

def content_sha(joined):
 return digest({'pair_id':joined['pair_id'],'shown_ids':sorted(joined['shown_ids']),'evidence':joined['evidence'],'candidates':joined['candidates'],'new_groups':joined['new_groups']})

def validate_decisions(joined,envelope,lists=None):
 if envelope.get('pair_id')!=joined['pair_id']:raise JoinRefusal('decision belongs to another pair')
 outcomes=envelope['outcomes'];first=envelope['evidence'];second=envelope['second_pass'];candidate_ids={c['id'] for c in joined['candidates']};evidence_ids={e['id'] for e in joined['evidence']}
 if set(outcomes)!=candidate_ids:raise JoinRefusal('missing/extra candidate outcome')
 for cid,(action,target,_) in outcomes.items():
  if action not in ('new','merge','skip','succession'):raise JoinRefusal('unknown candidate outcome')
  available=set(joined['shown_ids']) | set((lists.candidate_lists if lists else {}).get(cid,[]))
  if action in ('merge','succession') and target not in available:raise JoinRefusal('candidate target not shown or listed')
 required_first=set();required_second=set()
 for e in joined['evidence']:
  for link in e['links']:
   if link in candidate_ids:
    action,target,_=outcomes[link]
    if action=='merge':
     required_second.add((e['id'],target))
   elif link in joined['shown_ids']:required_first.add((e['id'],link))
   else:raise JoinRefusal('unknown destination')
 if set(first)!=required_first or set(second)!=required_second:raise JoinRefusal('missing/extra per-target evidence decision')
 for evidence_id,_ in set(first)|set(second):
  if evidence_id not in evidence_ids:raise JoinRefusal('decision references another evidence')
 for decision in list(first.values())+list(second.values()):
  if not isinstance(decision,(tuple,list)) or len(decision)!=3 or decision[0] not in ('new','repeat','replace'):raise JoinRefusal('invalid evidence decision')
 return True

def checked_write(conn,uni,seq,item,joined,shown,package):
 """Scratch-only: validate pair-bound synthetic decisions through the real matching checks before writing."""
 if package.get('pair_id')!=joined['pair_id'] or package.get('write_seq')!=seq:raise JoinRefusal('stale decision package')
 if joined.get('content_sha256')!=content_sha(joined):raise JoinRefusal('joined handover changed')
 if digest(item)!=joined['pair']['item_sha256'] or snapshot_sha(shown)!=joined['pair']['snapshot_sha256']:raise JoinRefusal('writer input differs from pair')
 h=extraction.Handover(joined['evidence'],joined['candidates'],[],0,joined['pair_id'],False,0,joined['new_groups'])
 lists=matching.build_lists(conn,h,shown,5);schema=matching.schema_for('matching-v4')
 first=package.get('first');second=package.get('second')
 if model.check_schema(first,schema) or model.check_schema(second,schema):raise JoinRefusal('decision schema')
 candidate_keys=[x['id'] for x in first['candidates']];first_keys=[(x['id'],x['view_id']) for x in first['evidence']]
 if len(candidate_keys)!=len(set(candidate_keys)) or len(first_keys)!=len(set(first_keys)):raise JoinRefusal('duplicate first decision')
 if set(candidate_keys)!={c['id'] for c in h.candidates} or set(first_keys)!=set(lists.evidence_lists):raise JoinRefusal('missing or extra first decision')
 checked=matching.check(conn,uni,first,h.candidates,h.evidence,lists,shown)
 if checked.refusals:raise JoinRefusal('first-pass refusal: '+str(checked.refusals))
 merge_pairs={(e['id'],checked.outcomes[link][1]) for e in h.evidence for link in e['links'] if link in checked.outcomes and checked.outcomes[link][0]=='merge'}
 second_keys=[(x['id'],x['view_id']) for x in second['evidence']]
 if second['candidates'] or len(second_keys)!=len(set(second_keys)) or set(second_keys)!=merge_pairs:raise JoinRefusal('missing or extra second decision')
 pieces={e['id']:e for e in h.evidence};second_lists=matching.Lists({}, {(eid,vid):matching.rank_evidence(conn,vid,pieces[eid]['one_line'],5) for eid,vid in merge_pairs})
 checked_second=matching.check(conn,uni,second,[],h.evidence,second_lists,shown)
 if checked_second.refusals:raise JoinRefusal('second-pass refusal: '+str(checked_second.refusals))
 envelope={'pair_id':joined['pair_id'],'outcomes':checked.outcomes,'evidence':checked.evidence,'second_pass':checked_second.evidence}
 validate_decisions(joined,envelope,lists)
 return writing.write(conn,uni,seq,item,h,checked,checked_second.evidence)
