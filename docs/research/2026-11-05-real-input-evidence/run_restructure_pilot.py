"""Run fixed, independently reviewed, five-article prompt diagnostic."""
import copy, gzip, hashlib, importlib.util, json, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('assemble',HERE/'assemble_restructure_requests.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
old=a.old; model=a.model; extraction=a.extraction
MANIFEST=HERE/'restructure-pilot-frozen.json';FAKE=HERE/'restructure-pilot-fake.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def frozen(reqs):
 base=old.frozen(reqs)
 files=[Path(__file__),HERE/'assemble_restructure_requests.py',HERE/'role-restructure-draft.txt',HERE/'groups-restructure-draft.txt',HERE/'categories-restructure-draft.json',HERE/'full-prompt-redesign-plan.md',HERE/'restructure-combined-audit.md',HERE/'full-prompt-audit-2026-11-05.zh.md',HERE/'full-request-inventory.md',HERE/'restructure-full-requests-draft.json.gz',HERE/'restructure-preflight.txt',HERE/'restructure-independent-audit.zh.md',HERE/'mutation_test_restructure.py',HERE/'restructure-mutation-results.txt']
 base['files'].update({str(p):sha(p.read_bytes()) for p in files})
 return base

def checks(reqs,uni):
 r=reqs[0];dummy=type('Answer',(),dict(call_id=0,request_sha256='fake',cached=False,cost_usd=0))();out={}
 for mode in ('original','positive','invalid_quote','invalid_link','invalid_candidate'):
  data=copy.deepcopy(r['old']);e=next(x for x in data['evidence'] if x['id']=='e11')
  if mode!='original':e['links']=['c1']
  if mode=='invalid_quote':e['quote']='This fabricated quote must not occur anywhere in the source article.'
  if mode=='invalid_link':e['links']=['v999999']
  if mode=='invalid_candidate':data['candidates'][0]['rungs']=[]
  errors=model.check_schema(data,r['schema'])
  if errors:raise ValueError('synthetic answer schema '+str(errors))
  def assert_result(answer):
   h=old.file_answer(answer,r,uni,dummy)
   kept=any(x['id']=='e11' and x['links']==['c1'] for x in h.evidence)
   if mode=='positive':assert kept
   else:
    assert not kept
    expected='quote not in item' if mode=='invalid_quote' else 'no home'
    assert ('e11',expected) in h.dropped
    if mode=='invalid_candidate':assert any(x[0]=='c1' and x[1].startswith('candidate ladder:') for x in h.dropped)
  assert_result(data)
  mutant=copy.deepcopy(data);me=next(x for x in mutant['evidence'] if x['id']=='e11')
  if mode=='positive':me['links']=[]
  elif mode=='invalid_quote':me['quote']=next(x['quote'] for x in r['old']['evidence'] if x['id']=='e11')
  elif mode in ('invalid_link','original'):me['links']=['c1']
  elif mode=='invalid_candidate':mutant['candidates'][0]['rungs']=copy.deepcopy(r['old']['candidates'][0]['rungs'])
  try:assert_result(mutant)
  except AssertionError:pass
  else:raise ValueError('mutant escaped '+mode)
  out[mode]='ok'
 return out

def main():
 if len(sys.argv)<2 or sys.argv[1] not in ('--freeze','--fake','--send'):raise SystemExit('usage --freeze | --fake output | --send output')
 mode=sys.argv[1];cfg,uni,reqs=a.build()
 saved=json.loads(gzip.decompress((HERE/'restructure-full-requests-draft.json.gz').read_bytes()))
 rebuilt=[{'input_id':r['item']['input_id'],'arm':r['arm'],'request':model.build_request(r['setting'],r['system'],r['user'],r['schema'],'extraction',cfg.provider)} for r in reqs]
 if json.dumps(saved)!=json.dumps(rebuilt):raise SystemExit('stored full request bytes mismatch')
 if len(reqs)!=10:raise SystemExit('ten requests required')
 if mode=='--freeze':
  if MANIFEST.exists():raise SystemExit('manifest exists')
  MANIFEST.write_text(json.dumps(frozen(reqs),ensure_ascii=False,indent=2)+'\n');print('manifest',sha(MANIFEST.read_bytes()));return
 if len(sys.argv)!=3:raise SystemExit('output required')
 out=Path(sys.argv[2]);
 if not out.is_absolute() or out.exists():raise SystemExit('new absolute output required')
 if json.loads(MANIFEST.read_text())!=frozen(reqs):raise SystemExit('frozen manifest mismatch')
 if mode=='--send':
  expected={'manifest_sha256':sha(MANIFEST.read_bytes()),'cases':10,'controls':5,'status':'ok'}
  if not FAKE.exists() or json.loads(FAKE.read_text())!=expected:raise SystemExit('fake preflight missing')
 controls=checks(reqs,uni);out.mkdir(parents=True)
 for i,r in enumerate(reqs):
  if json.loads(MANIFEST.read_text())!=frozen(reqs):raise SystemExit('input changed before request; stopped')
  directory=out/f'{i:02d}-{r["arm"]}';directory.mkdir();received=[]
  archive=model.Archive(str(directory/'archive.sqlite'))
  def transport(provider,request):
   if old.wire(request)!=r['wire']:raise ValueError('wire mismatch')
   if mode=='--fake':
    quote=r['old']['evidence'][0]['quote'];fact={'id':'e1','quote':quote,'one_line':'A source-backed statement.','speaker':'Source','original_who':'','original_day':'','tier':'fact','event_time':'','links':[r['shown'][0]['view_id']]}
    return {'choices':[{'message':{'content':json.dumps({'evidence':[fact],'candidates':[],'new_groups':[]})}}], 'usage':{'prompt_tokens':0,'completion_tokens':0}}
   response=model.openai_transport(provider,request);received.append(response)
   (directory/'response.json').write_text(json.dumps(response,ensure_ascii=False)+'\n');return response
  try:
   ans=model.call(archive,cfg,r['setting'],r['system'],r['user'],r['schema'],'extraction','extract',transport=transport)
   if ans.cached or ans.request_sha256!=r['identity']:raise ValueError('cache or request mismatch')
   handover=old.file_answer(ans.data,r,uni,ans)
   if mode=='--fake' and len(handover.evidence)!=1:raise ValueError('positive source-backed existing-question link failed')
   result={'status':'ok','input_id':r['item']['input_id'],'arm':r['arm'],'answer':ans.data,'handover':{'evidence':handover.evidence,'candidates':handover.candidates,'dropped':handover.dropped,'new_groups':handover.new_groups},'input_tokens':ans.input_tokens,'output_tokens':ans.output_tokens,'cost_usd':ans.cost_usd,'earlier_retry_cost':'unknown'}
  except Exception as error:result={'status':'failed_or_unknown','input_id':r['item']['input_id'],'arm':r['arm'],'error':repr(error),'usage':received[0].get('usage') if received else None}
  finally:archive.conn.close()
  (directory/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
  print(json.dumps({'index':i,'arm':r['arm'],'id':r['item']['input_id'],'status':result['status']}),flush=True)
  if result['status']!='ok':raise SystemExit('stopped after failure')
 if mode=='--fake':FAKE.write_text(json.dumps({'manifest_sha256':sha(MANIFEST.read_bytes()),'cases':10,'controls':len(controls),'status':'ok'})+'\n')
 (out/'complete.json').write_text(json.dumps({'status':'ok','cases':len(reqs)})+'\n')
if __name__=='__main__':main()
