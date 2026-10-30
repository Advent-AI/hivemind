import concurrent.futures, copy, importlib.util, json, os, subprocess, sys, time
from pathlib import Path
root=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
here=root/'docs/research/2026-10-29-single-note'; old=here.parent/'2026-10-29-prompt-restructure'
s=importlib.util.spec_from_file_location('p',root/'docs/research/2026-10-28-retention-audit/haiku-extraction-probe-2026-10-29.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
questions={'nvidia':'Your summary says signing status is not stated, but your reason calls it unsigned and the Firmus builder unnamed. Identify the exact source passages supporting those labels, or mark them unsupported. Which task instructions encouraged that answer? Name two supplied statements relevant to checking it. Give a brief evidence-based explanation, not private chain of thought.', 'nn':'Your note makes the supplier signal conditional on NVIDIA being confirmed as a direct customer. Does the text establish that direct customer confirmation is necessary to use a supplier-capacity lead? Which exact instruction and source passages support your choice? Name two supplied statements relevant to checking it. Brief evidence-based explanation only.'}
def one(n):
 req=json.loads((here/(n+'-probe-request.json')).read_text());t=time.monotonic()
 try:r={'response':p.haiku_api('https://api.anthropic.com/v1/messages',req)}
 except Exception as e:r={'error':type(e).__name__}
 r['seconds']=time.monotonic()-t
 (here/(n+'-probe-response.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2));print(n,r.get('response',{}).get('stop_reason'),flush=True)
if len(sys.argv)>1:
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(one,questions))
else:
 reserves=[]
 for n,q in questions.items():
  req=json.loads((old/(n+'-treatment-request.json')).read_text());resp=json.loads((old/(n+'-treatment-'+('2' if n=='nvidia' else '1')+'-answer.json')).read_text())['response']
  req['messages']+= [{'role':'assistant','content':resp['content']},{'role':'user','content':q}]
  req['output_config']={'effort':'medium'}
  bound=3*len(json.dumps(req).encode())+16384
  reserve=(bound*(.5 if bound>100000 else .1)+6064*(2.5 if bound>100000 else .5))/1e6
  reserves.append(reserve);(here/(n+'-probe-request.json')).write_text(json.dumps(req,ensure_ascii=False,indent=2))
 assert sum(reserves)<.60
 (here/'probe-budget.json').write_text(json.dumps({'reserved_usd':sum(reserves),'cap_usd':.60,'calls':2,'note':'Included in this experiment total; diagnostic self-report, not causal proof.'},indent=2))
 with (here/'probe.log').open('x') as log:
  run=subprocess.Popen([sys.executable,__file__,'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(root/'src')))
 (here/'probe.pid').write_text(str(run.pid));print(run.pid,sum(reserves))
