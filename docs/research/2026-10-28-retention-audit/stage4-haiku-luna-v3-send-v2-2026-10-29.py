"""Run a single frozen fourth-step comparison with durable attempts and bounded reservations."""
import concurrent.futures
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import urllib.error

ROOT=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
HERE=ROOT/'docs/research/2026-10-28-retention-audit'
RUN=HERE/'stage4-haiku-luna-v3-2026-10-29'
CONTRACT=HERE/'stage4-send-contract-2026-10-29.md'
COUNTS='counts-v2.json'
CAP=.60


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
prep=module('stage4_prep',HERE/'stage4-haiku-luna-v3-2026-10-29.py')
probe=module('haiku_probe',HERE/'haiku-extraction-probe-2026-10-29.py')


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def digest_wire(value):return hashlib.sha256(probe.previous.wire(value)).hexdigest()

def read(name):return json.loads((RUN/name).read_text())


def put(name,value):
    with (RUN/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())


def claim(path, value):
    with path.open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False);f.write('\n');f.flush();os.fsync(f.fileno())


def check_wire(actual, expected):
    if probe.previous.wire(actual)!=probe.previous.wire(expected):raise ValueError('request serialization changed')


def frozen_requests():
    prep.verify();manifest=read('manifest.json');cases=prep.source_cases();reqs={}
    for name,case in cases.items():
        luna,haiku=prep.requests(case)
        for provider,expected in [('luna',luna),('haiku',haiku)]:
            saved=read(f'{name}-{provider}-request.json');check_wire(saved,expected)
            reqs[(name,provider)]=expected
        if luna['messages']!=[{'role':'system','content':haiku['system']},*haiku['messages']]:raise ValueError('message mismatch')
        check_wire(luna['response_format']['json_schema']['schema'],haiku['output_config']['format']['schema'])
    return manifest,cases,reqs


def reservation(name,provider,req,tokens):
    if type(tokens) is not int or tokens<=0:raise ValueError('token count missing')
    bound=max(3*tokens+16384,len(probe.previous.wire(req)))
    high=provider=='haiku' and bound>100000
    rate_in,rate_out=(.5,2.5) if high else (.1,.5)
    return {'case':name,'provider':provider,'request_sha256':digest_wire(req),'estimated_input_tokens':tokens,
            'input_bound':bound,'output_bound':6064,'high_tariff':high,
            'reserved_usd_per_call':(bound*rate_in+6064*rate_out)/1e6}


def count_one(job,reqs):
    name,provider=job;req=reqs[job]
    if provider=='haiku':
        request={k:v for k,v in req.items() if k!='max_tokens'}
        result=probe.haiku_api('https://api.anthropic.com/v1/messages/count_tokens',request)
    else:
        schema=req['response_format']['json_schema']['schema']
        request={'model':req['model'],'input':req['messages'],'text':{'format':{'type':'json_schema','name':'research_update','strict':True,'schema':schema}}}
        result=probe.previous.api('gpt','https://api.openai.com/v1/responses/input_tokens',request)
    return reservation(name,provider,req,result.get('input_tokens'))


def check_counts(counts, reqs):
    if set(counts)!={'rows','reserved_total_usd','cap_usd','runner_sha256','contract_sha256','note'}:raise ValueError('unexpected count fields')
    if counts['cap_usd']!=CAP or counts['runner_sha256']!=digest(Path(__file__)) or counts['contract_sha256']!=digest(CONTRACT):raise ValueError('frozen runner, contract or cap changed')
    rows=counts['rows'];keys={(r['case'],r['provider']) for r in rows}
    if len(rows)!=10 or keys!=set(reqs):raise ValueError('count population changed')
    for row in rows:
        key=(row['case'],row['provider'])
        if row!=reservation(*key,reqs[key],row['estimated_input_tokens']):raise ValueError('reservation no longer matches its inputs')
    total=sum(r['reserved_usd_per_call']*3 for r in rows)
    if total!=counts['reserved_total_usd'] or total>CAP:raise ValueError('reservation exceeds cap or has changed')


def usage_ok(response,provider,row):
    usage=response.get('usage') if isinstance(response,dict) else None
    if not isinstance(usage,dict):return False
    if provider=='haiku':
        if 'input_tokens' not in usage or 'output_tokens' not in usage:return False
        values=[usage.get(k,0) for k in ('input_tokens','cache_creation_input_tokens','cache_read_input_tokens')]
        out=usage['output_tokens']
    else:
        if 'prompt_tokens' not in usage or 'completion_tokens' not in usage:return False
        values=[usage['prompt_tokens']];out=usage['completion_tokens']
    if any(type(x) is not int or x<0 for x in values+[out]):return False
    inp=sum(values)
    return inp>0 and inp<=row['input_bound'] and out<=row['output_bound'] and not (provider=='haiku' and inp>100000 and not row['high_tariff'])


def parse_response(response,provider,case):
    result={'response':response,'provider_complete':False,'usable':False,'answer':None,'structural_errors':[],'citation_notes':[]}
    try:
        if provider=='haiku':
            result['finish']=response.get('stop_reason')
            content=''.join(x.get('text','') for x in response.get('content',[]) if x.get('type')=='text')
            result['provider_complete']=result['finish']=='end_turn'
        else:
            choice=response['choices'][0];result['finish']=choice.get('finish_reason')
            content=choice['message'].get('content') or ''
            result['provider_complete']=result['finish']=='stop' and not choice['message'].get('refusal')
        result['answer']=json.loads(content)
        result['structural_errors'],result['citation_notes']=prep.answer_checks(result['answer'],case)
        result['usable']=result['provider_complete'] and not result['structural_errors']
    except Exception as error:
        result['parse_error']=type(error).__name__
    return result


def selftest():
    sample={'model':'x','properties':{'a':1,'b':2}}
    mutant={'properties':{'a':1,'b':2},'model':'x'}
    check_wire(sample,sample)
    try:check_wire(sample,mutant)
    except ValueError:pass
    else:raise AssertionError('reordered bytes were accepted')
    row=reservation('c','luna',sample,100)
    ok={'usage':{'prompt_tokens':20,'completion_tokens':10}}
    assert usage_ok(ok,'luna',row) and not usage_ok({'usage':{'prompt_tokens':20}},'luna',row)
    assert not usage_ok({'usage':{'completion_tokens':10}},'luna',row)
    case=next(c for c in prep.source_cases().values() if c['question_ids'])
    bad={'choices':[{'finish_reason':'stop','message':{'content':'not json'}}],'usage':{'prompt_tokens':20,'completion_tokens':10}}
    parsed=parse_response(bad,'luna',case);assert parsed['provider_complete'] and not parsed['usable'] and parsed['response']==bad
    malformed={'choices':[],'usage':{'prompt_tokens':20,'completion_tokens':10}}
    parsed=parse_response(malformed,'luna',case);assert not parsed['usable'] and parsed['response']==malformed
    with tempfile.TemporaryDirectory() as temp:
        p=Path(temp)/'lock';claim(p,{'pid':1})
        try:claim(p,{'pid':2})
        except FileExistsError:pass
        else:raise AssertionError('duplicate lock accepted')
    print('wire, usage, malformed-response and exclusive-attempt controls passed',flush=True)


def count():
    manifest,cases,reqs=frozen_requests();selftest()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:rows=list(pool.map(lambda job:count_one(job,reqs),reqs))
    total=sum(r['reserved_usd_per_call']*3 for r in rows)
    data={'rows':rows,'reserved_total_usd':total,'cap_usd':CAP,'runner_sha256':digest(Path(__file__)),
          'contract_sha256':digest(CONTRACT),'note':'Conservative estimate; missing usage retains full reservation; not a provider-enforced cap.'}
    check_counts(data,reqs);put(COUNTS,data)
    print('reserved 30 calls $',round(total,6),flush=True)


def verify_counts():
    manifest,cases,reqs=frozen_requests();selftest();counts=read(COUNTS);check_counts(counts,reqs)
    for field in ('input_bound','output_bound'):
        m=copy.deepcopy(counts);m['rows'][0][field]+=1
        try:check_counts(m,reqs)
        except ValueError:continue
        raise AssertionError('changed '+field+' accepted')
    print('reservation positive and two changed-bound controls passed',flush=True)
    return manifest,cases,reqs,counts


def one(job,reqs,cases):
    name,provider,index=job;stem=f'{name}-{provider}-{index}'
    claim(RUN/(stem+'.attempt.json'),{'case':name,'provider':provider,'sample':index,'request_sha256':digest_wire(reqs[(name,provider)])})
    started=time.monotonic();response=None;error=None
    try:
        req=reqs[(name,provider)]
        response=(probe.haiku_api('https://api.anthropic.com/v1/messages',req) if provider=='haiku' else
                  probe.previous.api('gpt','https://api.openai.com/v1/chat/completions',req))
    except urllib.error.HTTPError as e:error={'type':'HTTPError','status':e.code}
    except Exception as e:error={'type':type(e).__name__}
    put(stem+'.raw.json',{'response':response,'error':error})
    record=parse_response(response,provider,cases[name]) if response is not None else {'response':None,'provider_complete':False,'usable':False}
    record.update({'error':error,'seconds':round(time.monotonic()-started,2)})
    put(stem+'.json',record)
    print(name,provider,index,'finish',record.get('finish'),'usable',record['usable'],'error',error,flush=True)
    return record


def worker():
    manifest,cases,reqs,counts=verify_counts()
    claim(RUN/'worker-v2.lock',{'pid':os.getpid(),'counts_sha256':digest(RUN/COUNTS)})
    jobs=[(n,p,i) for n in manifest['cases'] for i in (1,2,3) for p in ('luna','haiku')]
    planned=len(jobs);pending={};done=[];stopped=False
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        while jobs or pending:
            while jobs and len(pending)<8 and not stopped:
                job=jobs.pop(0);pending[pool.submit(one,job,reqs,cases)]=job
            if not pending:break
            finished,_=concurrent.futures.wait(pending,return_when=concurrent.futures.FIRST_COMPLETED)
            for future in finished:
                job=pending.pop(future)
                try:record=future.result()
                except Exception as error:record={'error':{'type':type(error).__name__},'response':None}
                row=next(r for r in counts['rows'] if (r['case'],r['provider'])==job[:2])
                done.append({'case':job[0],'provider':job[1],'sample':job[2],'finish':record.get('finish'),
                             'usable':record.get('usable',False),'error':record.get('error'),'usage':(record.get('response') or {}).get('usage')})
                if not usage_ok(record.get('response'),job[1],row):stopped=True
    put('run-v2-summary.json',{'planned':planned,'attempted':len(done),'not_sent':jobs,'stopped_on_usage_or_transport_anomaly':stopped,'samples':done})
    print('finished',len(done),'not sent',len(jobs),'stopped',stopped,flush=True)


def launch():
    verify_counts()
    if (RUN/'run-v2.pid').exists() or (RUN/'worker-v2.lock').exists():raise ValueError('already launched')
    with (RUN/'run-v2.log').open('x') as log:
        p=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONPATH=str(ROOT/'src')))
    (RUN/'run-v2.pid').write_text(str(p.pid)+'\n');print('detached pid',p.pid)


if __name__=='__main__':{'selftest':selftest,'count':count,'launch':launch,'worker':worker}[sys.argv[1]]()
