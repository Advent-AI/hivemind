"""Continue three stored conversations to understand scope choices; self-reports are not proof."""
import base64
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
import urllib.request

ROOT=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
HERE=ROOT/'docs/research/2026-10-28-retention-audit'
OLD=HERE/'stage4-scope-arm-2026-10-29'
RUN=HERE/'stage4-credit-account-2026-10-29'
spec=importlib.util.spec_from_file_location('prior',HERE/'haiku-extraction-probe-2026-10-29.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
CASES=[('haiku1','haiku',1),('haiku2','haiku',2),('haiku3','haiku',3)]
QUESTION=('In your previous answer you wrote that NVIDIA provides or extends credit support. '
          'Which exact sentence in the supplied source establishes who provides that support, and which instruction or other information led to your statement? '
          'What two other interpretations did you consider or reject, and why? Separate the source text from your inference.')


def put(name,value):
    with (RUN/name).open('x',encoding='utf-8') as f:json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):return json.loads(p.read_text())


def originals():
    out={}
    for name,provider,index in CASES:
        request_path=OLD/f'nvidia-scope-{provider}-request.json';answer_path=OLD/f'nvidia-scope-{provider}-{index}.json'
        orig=read(request_path);record=read(answer_path);response=record['response']
        assert record['provider_complete'] and record['answer'] is not None
        if provider=='haiku':
            req={'model':orig['model'],'system':orig['system'],'messages':copy.deepcopy(orig['messages']) + [
                {'role':'assistant','content':copy.deepcopy(response['content'])},{'role':'user','content':QUESTION}],
                'max_tokens':6000,'output_config':{'effort':'medium'}}
        else:
            content=response['choices'][0]['message']['content']
            req={'model':orig['model'],'messages':copy.deepcopy(orig['messages']) + [
                {'role':'assistant','content':content},{'role':'user','content':QUESTION}],
                'max_completion_tokens':6000,'reasoning_effort':'medium'}
        out[name]={'provider':provider,'request':req,'old_request_sha256':digest(request_path),'old_response_sha256':digest(answer_path)}
    return out


def prepare():
    cases=originals();reserved=0
    for x in cases.values():
        bound=3*len(prior.previous.wire(x['request']))+16384;hi=x['provider']=='haiku' and bound>100000
        reserved+=(bound*(.5 if hi else .1)+6064*(2.5 if hi else .5))/1e6
    assert reserved<.60
    RUN.mkdir(exist_ok=False)
    for n,x in cases.items():put(n+'-request.json',x['request'])
    put('manifest.json',{'cases':{n:{k:v for k,v in x.items() if k!='request'} for n,x in cases.items()},
        'request_hashes':{n:digest(RUN/(n+'-request.json')) for n in cases},'reserved_usd':reserved,'cap_usd':.60,
        'note':'Continuation preserves original conversation text; provider-injected formatting may differ. Model explanations are leads, not evidence of internal reasoning.'})
    print('prepared 3 diagnostics; reserved $',round(reserved,6))


def verify():
    manifest=read(RUN/'manifest.json');cases=originals();assert manifest['reserved_usd']<manifest['cap_usd']==.60
    for n,x in cases.items():
        assert {k:v for k,v in x.items() if k!='request'}==manifest['cases'][n]
        p=RUN/(n+'-request.json');assert digest(p)==manifest['request_hashes'][n] and read(p)==x['request']
    return cases


def one(name,case):
    req=case['request'];provider=case['provider'];put(name+'-attempt.json',{'provider':provider,'request_sha256':digest(RUN/(name+'-request.json'))})
    if provider=='haiku':url='https://api.anthropic.com/v1/messages';headers={'x-api-key':prior.haiku_key(),'anthropic-version':'2026-10-21','Content-Type':'application/json'}
    else:url='https://api.openai.com/v1/chat/completions';headers={'Authorization':'Bearer '+prior.previous.key('gpt'),'Content-Type':'application/json'}
    start=time.monotonic();raw=b'';error=None
    try:
        with urllib.request.urlopen(urllib.request.Request(url,prior.previous.wire(req),headers,method='POST'),timeout=180) as response:raw=response.read()
    except urllib.error.HTTPError as e:raw=e.read();error={'type':'HTTPError','status':e.code}
    except Exception as e:error={'type':type(e).__name__}
    put(name+'-raw.json',{'body_base64':base64.b64encode(raw).decode(),'error':error})
    try:answer=json.loads(raw) if raw else None
    except (ValueError,UnicodeDecodeError):answer=None
    put(name+'-response.json',{'response':answer,'error':error,'seconds':round(time.monotonic()-start,2)})
    print(name,'response',bool(answer),'error',error,flush=True)
    return name


def worker():
    cases=verify();put('worker.lock',{'pid':os.getpid()})
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:done=list(pool.map(lambda x:one(x,cases[x]),cases))
    put('summary.json',{'cases':done,'review':'pending'})


def launch():
    verify()
    if (RUN/'run.pid').exists() or (RUN/'worker.lock').exists():raise ValueError('already launched')
    with (RUN/'run.log').open('x') as log:
        proc=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONPATH=str(ROOT/'src')))
    (RUN/'run.pid').write_text(str(proc.pid)+'\n');print('detached pid',proc.pid)


if __name__=='__main__':{'prepare':prepare,'worker':worker,'launch':launch}[sys.argv[1]]()
