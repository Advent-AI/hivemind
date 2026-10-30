"""Continue three stored Haiku conversations once to inspect why specific decisions were made."""
import concurrent.futures
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.error

HERE=Path(__file__).resolve().parent
RUN=HERE/'haiku-model-account-probe-2026-10-29'
spec=importlib.util.spec_from_file_location('haiku_probe',HERE/'haiku-extraction-probe-2026-10-29.py')
probe=importlib.util.module_from_spec(spec);spec.loader.exec_module(probe)
CASES={
 'memory': ('haiku-luna-multi-2026-10-29/memory-haiku-request.json','haiku-luna-multi-2026-10-29/memory-haiku-2.json',
   'In your previous answer, you gave the SK hynix forecast the original_day 2026-07-18. Which exact original instruction and source passage led you to that date? Which two other interpretations or instructions did you reject, and why? Distinguish what is stated from what you assumed.'),
 'singapore': ('haiku-luna-multi-2026-10-29/singapore-haiku-request.json','haiku-luna-multi-2026-10-29/singapore-haiku-2.json',
   'In your previous answer, you extracted the Singapore server investigation and the company charges. Which exact original instructions and article statements led you to retain them? Which two competing instructions or interpretations did you reject, and why? Distinguish instructions from your inference.'),
 'growth': ('haiku-extraction-probe-2026-10-29/haiku-request.json','haiku-extraction-probe-2026-10-29/haiku-1.json',
   'In your previous answer, you wrote revenue growth in the summary, but your quote contained only the percentage sentences. Which exact original instructions and source passages led you to choose that quote? Which two competing interpretations or instructions did you reject, and why? Distinguish what is stated from what you assumed.')}


def put(name,obj):
 with (RUN/name).open('x',encoding='utf-8') as f: json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')


def prepare():
 RUN.mkdir(exist_ok=False); res=0; files={}
 for name,(request_path,answer_path,question) in CASES.items():
  old=json.loads((HERE/request_path).read_text()); response=json.loads((HERE/answer_path).read_text())['response']
  assert response['stop_reason']=='end_turn' and old['model']=='claude-haiku-5-5'
  request={'model':old['model'],'system':old['system'],'messages':copy.deepcopy(old['messages']) + [{'role':'assistant','content':copy.deepcopy(response['content'])},{'role':'user','content':question}], 'max_tokens':1800,'output_config':{'effort':'low'}}
  bound=3*len(probe.previous.wire(request))+16384
  inp_rate,out_rate=(.5,2.5) if bound>100000 else (.1,.5)
  res+=(bound*inp_rate+1864*out_rate)/1e6
  put(name+'-request.json',request)
  files[name]={'request_sha256':probe.previous.digest(RUN/(name+'-request.json')),'source_request_sha256':probe.previous.digest(HERE/request_path),'source_response_sha256':probe.previous.digest(HERE/answer_path),'input_bound':bound}
 assert res<.60
 put('manifest.json',{'cases':files,'reserved_usd':res,'cap_usd':.60,'note':'Diagnostic self-reports are model statements, not proof of internal cause. No change to production prompts or settings.'})
 print('prepared three recorded-conversation continuations; reserve',round(res,6))


def one(name):
 try:
  request=json.loads((RUN/(name+'-request.json')).read_text());t=time.monotonic()
  response=probe.haiku_api('https://api.anthropic.com/v1/messages',request)
  record={'response':response,'seconds':round(time.monotonic()-t,2)}
 except urllib.error.HTTPError as error:
  record={'error':'HTTPError','status':error.code}
 except Exception as error:
  record={'error':type(error).__name__}
 put(name+'-response.json',record)
 print(name,record.get('response',{}).get('stop_reason'),record.get('error'),flush=True)
 return name


def worker():
 manifest=json.loads((RUN/'manifest.json').read_text());assert manifest['reserved_usd']<.60
 for name,entry in manifest['cases'].items():
  assert probe.previous.digest(RUN/(name+'-request.json'))==entry['request_sha256']
  req=json.loads((RUN/(name+'-request.json')).read_text());old_path,ans_path,_=CASES[name]
  assert probe.previous.digest(HERE/old_path)==entry['source_request_sha256'] and probe.previous.digest(HERE/ans_path)==entry['source_response_sha256']
  original=json.loads((HERE/old_path).read_text());answer=json.loads((HERE/ans_path).read_text())['response']
  assert req['system']==original['system'] and req['messages'][:-2]==original['messages'] and req['messages'][-2]['content']==answer['content']
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  result=list(pool.map(one,CASES))
 put('run-summary.json',{'cases':result,'review':'pending human read'})


def launch():
 assert not (RUN/'run.pid').exists()
 with (RUN/'run.log').open('x') as log:
  p=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONPATH=str(probe.previous.ROOT/'src')))
 (RUN/'run.pid').write_text(str(p.pid)+'\n');print('detached pid',p.pid)


if __name__=='__main__': {'prepare':prepare,'worker':worker,'launch':launch}[sys.argv[1]]()
