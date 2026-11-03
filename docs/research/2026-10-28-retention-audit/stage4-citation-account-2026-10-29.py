"""Continue three saved Haiku analyses about how their new-material citations were chosen."""
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
HERE=ROOT/'docs/research/2026-10-28-retention-audit';OLD=HERE/'stage4-haiku-luna-v3-2026-10-29';RUN=HERE/'stage4-citation-account-2026-10-29'
spec=importlib.util.spec_from_file_location('prior',HERE/'haiku-extraction-probe-2026-10-29.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
QUESTION=('In your previous answer you described the cancellation of the four-die Rubin Ultra version in the v11 and v13 arguments. '
          'Which exact source record supports that claim, and which original instruction governed the IDs you placed in support_ids? '
          'Why did you choose those support IDs? Identify two other citation choices you considered and rejected, and distinguish what the text states from your inference.')


def put(name,value):
    with (RUN/name).open('x',encoding='utf-8') as f:json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):return json.loads(p.read_text())


def originals():
    request_path=OLD/'product_progress-haiku-request.json';orig=read(request_path);out={}
    for i in (1,2,3):
        answer_path=OLD/f'product_progress-haiku-{i}.json';record=read(answer_path);response=record['response']
        assert record['provider_complete'] and record['answer'] is not None
        req={'model':orig['model'],'system':orig['system'],'messages':copy.deepcopy(orig['messages']) + [
            {'role':'assistant','content':copy.deepcopy(response['content'])},{'role':'user','content':QUESTION}],
            'max_tokens':6000,'output_config':{'effort':'medium'}}
        out[str(i)]={'request':req,'old_request_sha256':digest(request_path),'old_response_sha256':digest(answer_path)}
    return out


def prepare():
    cases=originals();RUN.mkdir(exist_ok=False)
    for n,x in cases.items():put(n+'-request.json',x['request'])
    put('manifest.json',{'cases':{n:{k:v for k,v in x.items() if k!='request'} for n,x in cases.items()},
        'request_hashes':{n:digest(RUN/(n+'-request.json')) for n in cases},'script_sha256':digest(Path(__file__)),'cap_usd':.60,
        'note':'Reconstructed conversation text and saved assistant content; provider-injected formatting may differ. Model explanations are leads, not proof.'})
    print('prepared three diagnostic continuations')


def verify():
    manifest=read(RUN/'manifest.json');cases=originals();assert manifest['script_sha256']==digest(Path(__file__)) and manifest['cap_usd']==.60
    for n,x in cases.items():
        assert {k:v for k,v in x.items() if k!='request'}==manifest['cases'][n]
        p=RUN/(n+'-request.json');assert digest(p)==manifest['request_hashes'][n] and read(p)==x['request']
    return cases


def count():
    cases=verify();rows=[]
    for n,x in cases.items():
        req=x['request'];result=prior.haiku_api('https://api.anthropic.com/v1/messages/count_tokens',{k:v for k,v in req.items() if k!='max_tokens'})
        tokens=result.get('input_tokens');assert isinstance(tokens,int) and tokens>0
        bound=max(3*tokens+16384,len(prior.previous.wire(req)));hi=bound>100000
        reserve=(bound*(.5 if hi else .1)+6064*(2.5 if hi else .5))/1e6
        rows.append({'case':n,'tokens':tokens,'input_bound':bound,'high_tariff':hi,'reserved_usd':reserve})
    total=sum(r['reserved_usd'] for r in rows);assert total<.60
    put('counts.json',{'rows':rows,'reserved_usd':total,'cap_usd':.60,'script_sha256':digest(Path(__file__)),'note':'Conservative estimate, not a provider-enforced cap.'})
    print('reserved $',round(total,6))


def one(name,case):
    req=case['request'];put(name+'-attempt.json',{'request_sha256':digest(RUN/(name+'-request.json'))})
    headers={'x-api-key':prior.haiku_key(),'anthropic-version':'2026-10-21','Content-Type':'application/json'}
    started=time.monotonic();raw=b'';error=None
    try:
        with urllib.request.urlopen(urllib.request.Request('https://api.anthropic.com/v1/messages',prior.previous.wire(req),headers,method='POST'),timeout=180) as response:raw=response.read()
    except urllib.error.HTTPError as e:raw=e.read();error={'type':'HTTPError','status':e.code}
    except Exception as e:error={'type':type(e).__name__}
    put(name+'-raw.json',{'body_base64':base64.b64encode(raw).decode(),'error':error})
    try:answer=json.loads(raw) if raw else None
    except (ValueError,UnicodeDecodeError):answer=None
    put(name+'-response.json',{'response':answer,'error':error,'seconds':round(time.monotonic()-started,2)})
    print(name,'response',bool(answer),'error',error,flush=True);return name


def worker():
    cases=verify();counts=read(RUN/'counts.json');assert counts['script_sha256']==digest(Path(__file__)) and counts['reserved_usd']<.60
    put('worker.lock',{'pid':os.getpid()})
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:done=list(pool.map(lambda n:one(n,cases[n]),cases))
    put('summary.json',{'cases':done,'review':'pending'})


def launch():
    verify();counts=read(RUN/'counts.json');assert counts['script_sha256']==digest(Path(__file__)) and counts['reserved_usd']<.60
    if (RUN/'run.pid').exists() or (RUN/'worker.lock').exists():raise ValueError('already launched')
    with (RUN/'run.log').open('x') as log:
        p=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONPATH=str(ROOT/'src')))
    (RUN/'run.pid').write_text(str(p.pid)+'\n');print('detached pid',p.pid)


if __name__=='__main__':{'prepare':prepare,'count':count,'launch':launch,'worker':worker}[sys.argv[1]]()
