"""One fixed, paired model-by-prompt experiment; no production writes."""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE_FILE = HERE.parent/'2026-10-29-model-capability/run.py'
spec = importlib.util.spec_from_file_location('baseline', BASE_FILE)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
provider = base.provider

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n): return json.loads((HERE/n).read_text())
def put(n, v):
    with (HERE/n).open('x') as f:
        json.dump(v, f, ensure_ascii=False, indent=2)
        f.flush(); os.fsync(f.fileno())

def validate():
    plan=read('plan.json')
    assert plan['cases']==['nvidia','nn','cloud','signed','singapore']
    assert plan['models']==['haiku','luna'] and plan['prompts']==['base','check']
    assert plan['planned_calls']==60 and plan['samples']==3 and plan['cap_usd']==.60
    for case in plan['cases']:
        old=None
        for prompt in plan['prompts']:
            h=read(f'{case}-haiku-{prompt}-request.json');l=read(f'{case}-luna-{prompt}-request.json')
            assert h['model']=='claude-haiku-5-5' and l['model']=='gpt-6-luna'
            assert h['max_tokens']==l['max_completion_tokens']==6000
            assert h['output_config']['effort']==l['reasoning_effort']=='medium'
            assert l['messages']==[{'role':'system','content':h['system']},*h['messages']]
            assert provider.previous.wire(base.schema(h))==provider.previous.wire(base.schema(l))
            assert h['system']==(HERE/(prompt+'-system.txt')).read_text()
            expected=json.loads((HERE.parent/'2026-10-29-inference-check'/f"{case}-{'control' if prompt=='base' else 'treatment'}-request.json").read_text())
            assert h==expected
            if old:
                assert h['messages']==old['messages'] and h['output_config']==old['output_config']
            old=h
            history,siblings,questions=base.domains(h)
            assert not history and not questions
            props=base.schema(h)['properties']
            assert 'comparisons' not in props and 'updates' not in props
            assert props['proposal']['anyOf'][1]['properties']['support_ids']['items']['enum']==['incoming']+siblings

def freeze():
    validate();budget=read('counts.json')
    assert budget['cap_usd']==.60 and budget['combined_reserved_usd']<.60
    assert len(budget['rows'])==20
    assert budget['reserved_usd']==sum(r['reserved_per_call']*3 for r in budget['rows'])
    for r in budget['rows']: assert digest(HERE/r['request'])==r['sha256']
    files=list(HERE.glob('*'))+list((ROOT/'src/hivemind').rglob('*.py'))+list((ROOT/'src/hivemind/prompts').glob('*'))
    files += [BASE_FILE,ROOT/'docs/research/2026-10-28-retention-audit/haiku-extraction-probe-2026-10-29.py',ROOT/'docs/research/2026-10-28-retention-audit/deepseek-extraction-probe-2026-10-29.py']
    put('manifest.json',{'files':{str(p):digest(p) for p in files if p.is_file()}})

def verify():
    for p,h in read('manifest.json')['files'].items(): assert digest(Path(p))==h,p

def jobs():
    p=read('plan.json');j=[(c,m,a,n) for n in (1,2,3) for c in p['cases'] for m in p['models'] for a in p['prompts']]
    random.Random(20261029).shuffle(j)
    return j

def worker():
    verify();rows={r['request']:r for r in read('counts.json')['rows']};stop=threading.Event();start=time.monotonic()
    def one(job):
        c,m,a,n=job;ident=f'{c}-{m}-{a}-{n}'
        if stop.is_set(): return {'id':ident,'not_sent':True}
        file=f'{c}-{m}-{a}-request.json';request=read(file)
        put(ident+'-attempt.json',{'request':file,'sha256':rows[file]['sha256']})
        before=time.monotonic();result={'id':ident}
        try:
            if m=='haiku':
                response=provider.haiku_api('https://api.anthropic.com/v1/messages',request)
                done=response.get('stop_reason')=='end_turn';text=''.join(x.get('text','') for x in response.get('content',[]) if x['type']=='text')
                u=response['usage'];i,o=u['input_tokens'],u['output_tokens']
            else:
                response=provider.previous.api('gpt','https://api.openai.com/v1/chat/completions',request)
                done=response['choices'][0]['finish_reason']=='stop';text=response['choices'][0]['message'].get('content') or ''
                u=response['usage'];i,o=u['prompt_tokens'],u['completion_tokens']
            result.update(response=response,completed=done)
            assert 0<i<=rows[file]['input_bound'] and 0<o<=6064
            result['answer']=json.loads(text)
            result['errors']=base.check(result['answer'],request,m)
            if not done: stop.set()
        except Exception as e:
            result['error']=type(e).__name__;stop.set()
        result['seconds']=round(time.monotonic()-before,2);put(ident+'-answer.json',result)
        print(ident,result.get('completed'),result.get('errors'),result.get('error'),flush=True)
        return {k:result[k] for k in ('id','completed','errors','error') if k in result}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(one,jobs()))
    verify();put('run-summary.json',{'status':'stopped' if stop.is_set() else 'completed','results':results,'elapsed_seconds':time.monotonic()-start})

def launch():
    verify();put('launch.json',{'parent_pid':os.getpid()})
    with (HERE/'run.log').open('x') as log:
        p=subprocess.Popen([sys.executable,__file__,'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(ROOT/'src')))
    (HERE/'run.pid').write_text(str(p.pid));print('Detached',p.pid)

def blind():
    summary=read('run-summary.json');(HERE/'blind').mkdir();j=jobs();random.Random(2946102).shuffle(j);mapping={}
    for number,(c,m,a,n) in enumerate(j,1):
        key=f'R{number:03d}';name=f'{c}-{m}-{a}-{n}';f=HERE/(name+'-answer.json')
        d=json.loads(f.read_text()) if f.exists() else {'not_sent':True}
        mapping[key]=name
        put('blind/'+key+'.json',{'case':c,'complete':d.get('completed',False),'answer':d.get('answer'),'errors':d.get('errors'),'not_sent':d.get('not_sent',False)})
    put('blind-map.json',mapping)

if __name__=='__main__': globals()[sys.argv[1]]()
