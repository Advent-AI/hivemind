"""Reserve and run the reviewed isolated 5-case model comparison; no retries or local answer cache."""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.error

ROOT=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
HERE=ROOT/'docs/research/2026-10-28-retention-audit'
RUN=HERE/'stage4-haiku-luna-v3-2026-10-29'
CAP=.60

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
prep=load_module('stage4_prep',HERE/'stage4-haiku-luna-v3-2026-10-29.py')
probe=load_module('haiku_probe',HERE/'haiku-extraction-probe-2026-10-29.py')


def put(name,value):
    with (RUN/name).open('x',encoding='utf-8') as f:json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')


def read(name):return json.loads((RUN/name).read_text())


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_pairs():
    prep.verify()
    manifest=read('manifest.json')
    for name in manifest['cases']:
        a=read(name+'-luna-request.json');b=read(name+'-haiku-request.json')
        assert a['messages']==[{'role':'system','content':b['system']},*b['messages']]
        assert probe.previous.wire(a['response_format']['json_schema']['schema'])==probe.previous.wire(b['output_config']['format']['schema'])
    return manifest


def count_one(job):
    name,provider=job;req=read(name+'-'+provider+'-request.json')
    if provider=='haiku':
        request={k:v for k,v in req.items() if k!='max_tokens'}
        result=probe.haiku_api('https://api.anthropic.com/v1/messages/count_tokens',request)
        tokens=result.get('input_tokens')
    else:
        schema=req['response_format']['json_schema']['schema']
        request={'model':req['model'],'input':req['messages'],'text':{'format':{'type':'json_schema','name':'research_update','strict':True,'schema':schema}}}
        result=probe.previous.api('gpt','https://api.openai.com/v1/responses/input_tokens',request)
        tokens=result.get('input_tokens')
    if not isinstance(tokens,int) or tokens<=0:raise ValueError('token count unavailable: '+name+' '+provider)
    bound=max(3*tokens+16384,len(probe.previous.wire(req)))
    high=provider=='haiku' and bound>100000
    rate_in,rate_out=(.5,2.5) if high else (.1,.5)
    reserved=(bound*rate_in+6064*rate_out)/1e6
    return {'case':name,'provider':provider,'estimated_input_tokens':tokens,'input_bound':bound,
            'output_bound':6064,'high_tariff':high,'reserved_usd_per_call':reserved}


def count():
    m=verify_pairs();jobs=[(n,p) for n in m['cases'] for p in ('luna','haiku')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:rows=list(pool.map(count_one,jobs))
    reserve=sum(row['reserved_usd_per_call']*3 for row in rows)
    if reserve>CAP:raise ValueError('conservative reservation exceeds cap: '+str(round(reserve,6)))
    put('counts.json',{'rows':rows,'reserved_total_usd':reserve,'cap_usd':CAP,'runner_sha256':digest(Path(__file__)),
        'note':'Counts are estimates; 3x estimated input plus 16384, output 6064, long rate if bound exceeds 100k. Missing usage reserves full amount. This is not a provider-enforced limit.'})
    print('10 requests counted, 30 calls reserved $',round(reserve,6),flush=True)
    for r in rows:print(r['case'],r['provider'],'tokens',r['estimated_input_tokens'],'bound',r['input_bound'],'high',r['high_tariff'],flush=True)


def verify_count():
    m=verify_pairs();counts=read('counts.json');assert counts['runner_sha256']==digest(Path(__file__)) and counts['cap_usd']==CAP
    assert len(counts['rows'])==10 and {(r['case'],r['provider']) for r in counts['rows']}=={(n,p) for n in m['cases'] for p in ('luna','haiku')}
    reserve=sum(r['reserved_usd_per_call']*3 for r in counts['rows'])
    assert reserve==counts['reserved_total_usd'] and reserve<=CAP
    return m,counts


def one(name,provider,index,cases):
    req=read(name+'-'+provider+'-request.json');start=time.monotonic()
    try:
        if provider=='haiku':
            response=probe.haiku_api('https://api.anthropic.com/v1/messages',req)
            finish=response.get('stop_reason');content=''.join(x.get('text','') for x in response.get('content',[]) if x.get('type')=='text')
            complete=finish=='end_turn'
        else:
            response=probe.previous.api('gpt','https://api.openai.com/v1/chat/completions',req)
            choice=response['choices'][0];finish=choice.get('finish_reason');content=choice['message'].get('content') or ''
            complete=finish=='stop' and not choice['message'].get('refusal')
        try:answer=json.loads(content)
        except (TypeError,ValueError):answer=None
        errors,notes=prep.answer_checks(answer,cases[name]) if answer is not None else (['not JSON'],[])
        record={'response':response,'answer':answer,'finish':finish,'completed':complete,'structural_errors':errors,'citation_notes':notes,'seconds':round(time.monotonic()-start,2)}
    except urllib.error.HTTPError as error:record={'error':'HTTPError','status':error.code,'seconds':round(time.monotonic()-start,2)}
    except Exception as error:record={'error':type(error).__name__,'seconds':round(time.monotonic()-start,2)}
    put(f'{name}-{provider}-{index}.json',record)
    print(name,provider,index,'finish',record.get('finish'),'error',record.get('error'),'checks',len(record.get('structural_errors',[])),flush=True)
    return record


def unexpected(record,row):
    usage=record.get('response',{}).get('usage')
    if not isinstance(usage,dict):return True
    if row['provider']=='haiku':
        inp=sum(usage.get(k,0) or 0 for k in ('input_tokens','cache_creation_input_tokens','cache_read_input_tokens'))
        out=usage.get('output_tokens',0) or 0
    else:
        inp=usage.get('prompt_tokens',0) or 0;out=usage.get('completion_tokens',0) or 0
    if not inp:return True
    return inp>row['input_bound'] or out>row['output_bound'] or (row['provider']=='haiku' and inp>100000 and not row['high_tariff'])


def worker():
    manifest,counts=verify_count();cases=prep.source_cases()
    jobs=[(n,p,i) for n in manifest['cases'] for i in (1,2,3) for p in ('luna','haiku')]
    planned=len(jobs);pending={};done=[];stopped=False
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        while jobs or pending:
            while jobs and len(pending)<8 and not stopped:
                job=jobs.pop(0);pending[pool.submit(one,*job,cases)]=job
            if not pending:break
            finished,_=concurrent.futures.wait(pending,return_when=concurrent.futures.FIRST_COMPLETED)
            for future in finished:
                job=pending.pop(future);record=future.result();row=next(r for r in counts['rows'] if (r['case'],r['provider'])==job[:2])
                done.append({'case':job[0],'provider':job[1],'sample':job[2],'finish':record.get('finish'),
                             'error':record.get('error'),'usage':record.get('response',{}).get('usage')})
                if unexpected(record,row):stopped=True
    put('run-summary.json',{'planned':planned,'sent':len(done),'not_sent':jobs,'stopped_on_usage_or_transport_anomaly':stopped,'samples':done})
    print('finished',len(done),'not sent',len(jobs),'stopped',stopped,flush=True)


def launch():
    verify_count()
    if (RUN/'run.pid').exists():raise ValueError('already launched')
    with (RUN/'run.log').open('x') as log:
        p=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONPATH=str(ROOT/'src')))
    (RUN/'run.pid').write_text(str(p.pid)+'\n');print('detached pid',p.pid)


if __name__=='__main__':{'count':count,'launch':launch,'worker':worker}[sys.argv[1]]()
