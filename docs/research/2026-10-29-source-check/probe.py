import concurrent.futures, copy, importlib.util, json, os, subprocess, sys, time
from pathlib import Path
root=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
here=root/'docs/research/2026-10-29-source-check'; old=here.parent/'2026-10-29-inference-check'
s=importlib.util.spec_from_file_location('p',root/'docs/research/2026-10-28-retention-audit/haiku-extraction-probe-2026-10-29.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
questions={'nvidia': 'Your answer says NVIDIA is taking on a credit-support role. Does the supplied source identify NVIDIA as the provider? Which instruction did you apply, and which two source statements did you discount? Why did the counterexample check address size rather than who provides support? Give a brief evidence-based diagnosis, not private chain of thought.', 'nn': 'Your answer says NVIDIA-linked demand is unconfirmed because other rack makers may be the buyers. Does a different buyer negate the stated NVIDIA rack end application? Which instruction did you apply, and which two source statements did you discount? Give a brief evidence-based diagnosis, not private chain of thought.'}
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
  req=json.loads((old/(n+'-treatment-request.json')).read_text());resp=json.loads((old/(n+'-treatment-'+'2'+'-answer.json')).read_text())['response']
  req['messages']+= [{'role':'assistant','content':resp['content']},{'role':'user','content':q}]
  req['output_config']={'effort':'medium'}
  bound=3*len(json.dumps(req).encode())+16384
  reserve=(bound*(.5 if bound>100000 else .1)+6064*(2.5 if bound>100000 else .5))/1e6
  reserves.append(reserve);(here/(n+'-probe-request.json')).write_text(json.dumps(req,ensure_ascii=False,indent=2))
 assert sum(reserves)<.05
 (here/'probe-budget.json').write_text(json.dumps({'reserved_usd':sum(reserves),'cap_usd':.60,'calls':2,'note':'Included in this experiment total; diagnostic self-report, not causal proof.'},indent=2))
 with (here/'probe.log').open('x') as log:
  run=subprocess.Popen([sys.executable,__file__,'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(root/'src')))
 (here/'probe.pid').write_text(str(run.pid));print(run.pid,sum(reserves))
