# -*- coding: utf-8 -*-
"""Fake paired execution through the experimental A identity boundary."""
import copy,json,sys,tempfile,threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OLD=ROOT/'docs/research/2026-11-05-parallel-thesis-evidence-poc'
sys.path[:0]=[str(HERE),str(OLD),str(ROOT/'src')]
import a_id_contract,prepare,run_poc
from hivemind import model

def invoke(cfg,uni,r,out,provider_transport):
 path=out/r['arm'];path.mkdir();archive=model.Archive(str(path/'archive.sqlite'));responses=[]
 schema=a_id_contract.experimental_schema(r['schema']) if r['arm']=='new' else r['schema']
 def capture(provider,request):
  response=provider_transport(provider,request);responses.append(response)
  (path/'response.json').write_text(json.dumps(response,ensure_ascii=False)+'\n');return response
 try:
  answer=model.call(archive,cfg,r['setting'],r['system'],r['user'],schema,'extraction','extract',transport=capture)
  h=a_id_contract.checked_handover(answer.data,schema,r,uni,answer) if r['arm']=='new' else run_poc.handover(answer.data,r,uni,answer)
  result={'status':'ok','arm':r['arm'],'handover':h,'answer':answer.data}
 except Exception as error:result={'status':'failed','arm':r['arm'],'error':repr(error),'response_received':bool(responses)}
 finally:archive.conn.close()
 (path/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');return result

def main():
 cfg,uni,records=prepare.prepare();ident='gnews:d144b91986c520ea36e718cf';pair={r['arm']:r for r in records if r['item']['input_id']==ident and r['arm'] in ('new','existing')}
 source=json.loads((ROOT/'poc/data/parallel-thesis-evidence-poc-2026-11-05/gnews_d144b91986c520ea36e718cf-new/result.json').read_text())['answer']
 e={'id':'e1','quote':pair['existing']['item']['text'][:100],'one_line':'Source statement.','speaker':'Source','original_who':'','original_day':'','tier':'fact','event_time':'','links':[pair['existing']['shown'][0]['view_id']]}
 b={'evidence':[e]};duplicate=copy.deepcopy(source);duplicate['candidates'].append(copy.deepcopy(duplicate['candidates'][0]));invalid=copy.deepcopy(source);invalid['candidates'][0]['id']='n1'
 def wrap(content):return {'choices':[{'message':{'content':content}}],'usage':{'prompt_tokens':0,'completion_tokens':0}}
 scenarios=[('valid',wrap(json.dumps(source)),'ok'),('invalid_id',wrap(json.dumps(invalid)),'failed'),('duplicate_id',wrap(json.dumps(duplicate)),'failed'),('malformed_long',wrap('x'*210001),'failed'),('provider_refusal',{'choices':[{'message':{'content':None,'refusal':'refused'}}]},'failed'),('transport_failure',None,'failed')]
 with tempfile.TemporaryDirectory(prefix='hivemind-a-pair-') as tmp:
  for name,a_response,expected in scenarios:
   directory=Path(tmp)/name;directory.mkdir();barrier=threading.Barrier(2)
   def a_transport(provider,request):
    barrier.wait(timeout=5)
    if a_response is None:raise RuntimeError('simulated transport failure')
    return a_response
   def b_transport(provider,request):barrier.wait(timeout=5);return wrap(json.dumps(b))
   with ThreadPoolExecutor(max_workers=2) as pool:
    future_a=pool.submit(invoke,cfg,uni,pair['new'],directory,a_transport);future_b=pool.submit(invoke,cfg,uni,pair['existing'],directory,b_transport);a=future_a.result();bb=future_b.result()
   assert a['status']==expected and bb['status']=='ok'
   assert (directory/'existing'/'response.json').exists() and (directory/'existing'/'result.json').exists()
   if expected=='failed':
    assert run_poc.join_results([a,bb])['status']=='incomplete'
    assert a['response_received']==(a_response is not None)
    assert (directory/'new'/'response.json').exists()==(a_response is not None)
    if name=='malformed_long':assert len(json.loads((directory/'new'/'response.json').read_text())['choices'][0]['message']['content'])==210001
   else:assert run_poc.join_results([a,bb])['status']=='ok'
  print('A+B real POC request path with fake transports: valid pair succeeds; n1, duplicate, malformed, provider refusal and no-response failures preserve available raw records and make pair incomplete.')
if __name__=='__main__':main()
