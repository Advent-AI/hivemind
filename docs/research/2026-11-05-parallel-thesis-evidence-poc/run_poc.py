"""Run frozen split requests in isolated archives; stop at the checked handover."""
import copy, json, sqlite3, sys, threading, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import prepare
from hivemind import extraction, model
HERE=Path(__file__).resolve().parent
FROZEN=HERE/'frozen-requests.json'

def check_frozen(records):
 frozen=json.loads(FROZEN.read_text())
 if len(records)!=len(frozen):raise ValueError('request count')
 for r,f in zip(records,frozen):
  if (r['item']['input_id'],r['seq'],r['arm'])!=(f['id'],f['seq'],f['arm']):raise ValueError('request identity')
  if prepare.sha(json.dumps(r['request']).encode())!=f['request_sha256'] or r['shown']!=f['snapshot'] or prepare.sha(r['item']['text'].encode())!=f['body_sha256']:raise ValueError('frozen request or input changed')

def join_results(pair):
 if len(pair)!=2 or any(r['status']!='ok' for r in pair):return {'status':'incomplete'}
 by_arm={r['arm']:r for r in pair}
 if set(by_arm)!={'new','existing'}:raise ValueError('missing or repeated lane')
 rows=[{'lane':arm,'evidence':e} for arm in ('new','existing') for e in by_arm[arm]['handover']['evidence']]
 overlaps=[{'new_id':a['evidence']['id'],'existing_id':b['evidence']['id'],'quote':a['evidence']['quote']} for a in rows for b in rows if a['lane']=='new' and b['lane']=='existing' and a['evidence']['quote']==b['evidence']['quote']]
 return {'status':'ok','records':rows,'exact_quote_overlaps':overlaps,'candidates':by_arm['new']['handover']['candidates']}

def handover(data,r,uni,ans):
 data=copy.deepcopy(data); arm=r['arm'];shown={v['view_id'] for v in r['shown']};local={c['id'] for c in data.get('candidates',[])};violations=[]
 if arm=='existing': data={'evidence':data['evidence'],'candidates':[],'new_groups':[]}
 if arm in ('new','existing'):
  allowed=local if arm=='new' else shown
  for e in data['evidence']:
   invalid=[x for x in e['links'] if x not in allowed]
   if invalid:violations.append((e['id'],'wrong-lane links: '+str(invalid)))
   e['links']=[x for x in e['links'] if x in allowed]
 e,c,d,g=extraction.sift_with_groups(data,r['item'],r['item']['text'],set() if arm=='new' else shown,uni)
 h=extraction.file_reading(extraction.Reading(e,c,d,g,ans,'v74i'),r['item'],r['shown'])
 return {'evidence':h.evidence,'candidates':h.candidates,'new_groups':h.new_groups,'dropped':violations+h.dropped}

def fixtures(records):
 c=sqlite3.connect(str(prepare.INPUT/'archive.sqlite'));saved=json.loads(c.execute('select answer_json from model_calls where call_id=116').fetchone()[0]);c.close()
 a={'evidence':[copy.deepcopy(next(e for e in saved['evidence'] if e['id']=='e13'))],'candidates':copy.deepcopy(saved['candidates']),'new_groups':[]}
 data={}
 for r in records:
  ident=r['item']['input_id'];e={'id':'e1','quote':r['item']['text'][:120], 'one_line':'A source-backed statement.','speaker':'Source','original_who':'','original_day':'','tier':'fact','event_time':'','links':[r['shown'][0]['view_id']]}
  if r['arm']=='existing':d={'evidence':[e]}
  elif r['arm']=='control':d={'evidence':[e],'candidates':[],'new_groups':[]}
  elif ident==prepare.ARTICLES[0][0]:d=a
  else:d={'evidence':[],'candidates':[],'new_groups':[]}
  errors=model.check_schema(d,r['schema'])
  if errors:raise ValueError('fixture schema '+str(errors))
  data[(ident,r['arm'])]=d
 return data

def negative_checks(records,uni,fixtures):
 class Dummy:call_id=0;request_sha256='fake';cached=False;cost_usd=0
 r=next(r for r in records if r['arm']=='new' and r['item']['input_id']==prepare.ARTICLES[0][0]);d=copy.deepcopy(fixtures[(r['item']['input_id'],'new')]);h=handover(d,r,uni,Dummy())
 if not h['candidates'] or not any('c1' in e['links'] for e in h['evidence']):raise ValueError('candidate positive')
 # Hypothetical matcher output, not an execution of the product matcher.
 existing_id=r['shown'][0]['view_id']; original=h['evidence'][0]
 remapped=dict(original,links=[existing_id if link=='c1' else link for link in original['links']])
 if remapped['quote']!=original['quote'] or existing_id not in remapped['links']:raise ValueError('hypothetical resolved candidate lost evidence')
 bad=copy.deepcopy(d);bad['evidence'][0]['quote']='A source sentence that was fabricated and does not occur.';h=handover(bad,r,uni,Dummy())
 if h['evidence'] or h['candidates']:raise ValueError('invented source not dropped')
 bad=copy.deepcopy(d);bad['candidates'][0]['settled_by']='';h=handover(bad,r,uni,Dummy())
 if h['evidence'] or h['candidates']:raise ValueError('refused candidate still retained')
 bad=copy.deepcopy(d);bad['evidence'][0]['links']=[r['shown'][0]['view_id']];h=handover(bad,r,uni,Dummy())
 if h['evidence'] or not any('wrong-lane' in x[1] for x in h['dropped']):raise ValueError('existing ID in new lane')
 r=next(r for r in records if r['arm']=='existing');d=copy.deepcopy(fixtures[(r['item']['input_id'],'existing')]);h=handover(d,r,uni,Dummy())
 if len(h['evidence'])!=1:raise ValueError('existing positive')
 d['evidence'][0]['links']=['c1'];h=handover(d,r,uni,Dummy())
 if h['evidence'] or not any('wrong-lane' in x[1] for x in h['dropped']):raise ValueError('candidate ID in existing lane')
 # Different lanes may use the same local id and quote but have distinct attribution and destinations.
 left={'lane':'new','evidence':{'id':'e1','quote':'Same words','speaker':'Company','links':['c1']}}
 right={'lane':'existing','evidence':{'id':'e1','quote':'Same words','speaker':'Analyst','links':[existing_id]}}
 pair=[{'status':'ok','arm':v['lane'],'handover':{'evidence':[v['evidence']],'candidates':[]}} for v in (left,right)]
 joined=join_results(pair)
 if len({(x['lane'],x['evidence']['id']) for x in joined['records']})!=2 or len(joined['exact_quote_overlaps'])!=1:raise ValueError('cross-lane overlap collapsed or lost')
 if left['evidence']['quote']!=right['evidence']['quote'] or left['evidence']['speaker']==right['evidence']['speaker'] or left['evidence']['links']==right['evidence']['links']:raise ValueError('overlap fixture lacks distinct attribution and target')
 different=dict(right,evidence=dict(right['evidence'],quote='Different words, potentially the same matter'))
 pair[1]['handover']['evidence']=[different['evidence']]
 if join_results(pair)['exact_quote_overlaps']:raise ValueError('different quote treated as identical')
 print('Checks passed: valid links, quote and candidate refusals, cross-lane identities and overlapping quotes.',flush=True)

def execute(r,cfg,uni,out,fake,fixture,barrier=None):
 directory=out/(r['item']['input_id'].replace(':','_')+'-'+r['arm']);directory.mkdir();archive=model.Archive(str(directory/'archive.sqlite'));received=[]
 def transport(provider,request):
  if prepare.sha(json.dumps(request).encode())!=prepare.sha(json.dumps(r['request']).encode()):raise ValueError('wire mismatch')
  if fake:
   if barrier:barrier.wait(timeout=10)
   return {'choices':[{'message':{'content':json.dumps(fixture)}}],'usage':{'prompt_tokens':0,'completion_tokens':0}}
  response=model.openai_transport(provider,request);received.append(response);(directory/'response.json').write_text(json.dumps(response,ensure_ascii=False)+'\n');return response
 try:
  ans=model.call(archive,cfg,r['setting'],r['system'],r['user'],r['schema'],'extraction','extract',transport=transport)
  if ans.cached:raise ValueError('unexpected cache')
  h=handover(ans.data,r,uni,ans)
  result={'status':'ok','id':r['item']['input_id'],'arm':r['arm'],'answer':ans.data,'handover':h,'input_tokens':ans.input_tokens,'output_tokens':ans.output_tokens,'cost_usd':ans.cost_usd}
 except Exception as ex:result={'status':'failed','id':r['item']['input_id'],'arm':r['arm'],'error':repr(ex),'response_received':bool(received)}
 finally:archive.conn.close()
 (directory/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(result['id'],result['arm'],result['status'],flush=True);return result

def main():
 if len(sys.argv)!=3 or sys.argv[1] not in ('--fake','--send'):raise SystemExit('usage --fake|--send ABSOLUTE_NEW_OUTPUT_DIRECTORY')
 fake=sys.argv[1]=='--fake';out=Path(sys.argv[2]);
 if not out.is_absolute() or out.exists():raise ValueError('output must be new absolute path')
 cfg,uni,records=prepare.prepare();check_frozen(records);fixture=fixtures(records);negative_checks(records,uni,fixture)
 if not fake:
  marker=HERE/'fake-proof.json'
  if not marker.exists() or json.loads(marker.read_text())!={'frozen_sha256':prepare.sha(FROZEN.read_bytes()),'status':'ok','requests':12}:raise ValueError('missing fake proof')
 out.mkdir(parents=True);results=[]
 if fake:
  ident=prepare.ARTICLES[0][0];selected={r['arm']:r for r in records if r['item']['input_id']==ident}
  with tempfile.TemporaryDirectory(prefix='parallel-poc-failure-') as tmp:
   barrier=threading.Barrier(2)
   with ThreadPoolExecutor(max_workers=2) as pool:
    good=pool.submit(execute,selected['new'],cfg,uni,Path(tmp),True,fixture[(ident,'new')],barrier)
    bad=pool.submit(execute,selected['existing'],cfg,uni,Path(tmp),True,{'invalid':[]},barrier)
    pair=[good.result(),bad.result()]
   if [x['status'] for x in pair]!=['ok','failed'] or join_results(pair)['status']!='incomplete':raise ValueError('one-lane failure did not remain incomplete')
  print('One-lane schema failure stays an incomplete pair.',flush=True)
 for ident,_ in prepare.ARTICLES:
  selected={r['arm']:r for r in records if r['item']['input_id']==ident}
  control=execute(selected['control'],cfg,uni,out,fake,fixture[(ident,'control')]);results.append(control)
  if control['status']!='ok':break
  barrier=threading.Barrier(2) if fake else None
  with ThreadPoolExecutor(max_workers=2) as pool:
   futures=[pool.submit(execute,selected[arm],cfg,uni,out,fake,fixture[(ident,arm)],barrier) for arm in ('new','existing')]
   pair=[f.result() for f in futures];results.extend(pair)
  (out/(ident.replace(':','_')+'-join.json')).write_text(json.dumps(join_results(pair),ensure_ascii=False,indent=2)+'\n')
  if any(x['status']!='ok' for x in pair):break
 status='ok' if len(results)==12 and all(x['status']=='ok' for x in results) else 'incomplete'
 (out/'complete.json').write_text(json.dumps({'status':status,'requests':len(results)},indent=2)+'\n')
 if fake and status=='ok':(HERE/'fake-proof.json').write_text(json.dumps({'frozen_sha256':prepare.sha(FROZEN.read_bytes()),'status':'ok','requests':12})+'\n')
 if status!='ok':raise SystemExit('incomplete: inspect before proceeding')
if __name__=='__main__':main()
