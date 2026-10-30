import concurrent.futures, copy, importlib.util, json, os, subprocess, sys, time
from pathlib import Path
root=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
here=root/'docs/research/2026-10-29-prompt-restructure'; old=here.parent/'2026-10-29-evidence-use-6000'
s=importlib.util.spec_from_file_location('p',root/'docs/research/2026-10-28-retention-audit/haiku-extraction-probe-2026-10-29.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
questions={'corning':'You wrote that the NVIDIA-Corning facility details appear only in separate Fox News items and are not part of this record. Which exact instruction led you here, and which two statements in the supplied request did you reject? Distinguish what was supplied from your interpretation.', 'cloud':'You wrote that the NVIDIA quarterly revenue table is internally inconsistent and cannot be used as a source. Which exact instruction and calculation led you here, and which two supplied statements did you reject? Distinguish evidence from your interpretation.'}
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
  req=json.loads((old/(n+'-treatment-request.json')).read_text());resp=json.loads((old/(n+'-treatment-2-answer.json')).read_text())['response']
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
