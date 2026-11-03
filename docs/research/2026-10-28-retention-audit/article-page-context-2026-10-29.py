"""Compare saved cleaned article text and saved full page in extraction only."""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
import urllib.error
from hivemind import config, extraction, model, universe

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
RUN=HERE/'article-page-context-2026-10-29'
DESIGN=HERE/'article-page-context-design-2026-10-29.md'
ITEMS='/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
PAGES='/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.page.sqlite'
ARCHIVE='/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/archive.sqlite'
IDS={'science':'gnews:8f5a03f1dde395491fc3814b','revenue':'gnews:71df54965281684cc500960f','holdout':'gnews:2934d9634471f3560f8697e0'}
spec=importlib.util.spec_from_file_location('old_probe',HERE/'haiku-extraction-probe-2026-10-29.py')
probe=importlib.util.module_from_spec(spec);spec.loader.exec_module(probe)
wire=probe.previous.wire

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def put(name,obj):
    with (RUN/name).open('x',encoding='utf-8') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
def read(name): return json.loads((RUN/name).read_text())
def source(name,arm):
    with sqlite3.connect(f'file:{ITEMS}?mode=ro',uri=True) as db:
        db.row_factory=sqlite3.Row;item=dict(db.execute('select * from items where input_id=?',(IDS[name],)).fetchone())
    with sqlite3.connect(f'file:{PAGES}?mode=ro',uri=True) as db:
        raw=db.execute('select text from items where input_id=?',(IDS[name],)).fetchone()[0]
    item['object_identifiers']=json.loads(item['object_identifiers']);text=item['text'] if arm=='clean' else raw
    assert text and len(text)<extraction.MAX_TEXT_CHARS
    cfg=config.load(str(ROOT/'poc/config/poc-v38.json'));uni=universe.load(str(ROOT/'poc/universe.json'))
    setting,system,user,schema=extraction.request_for(cfg,item,text,[],uni,[])
    g=model.build_request(setting,system,user,schema,'extraction',cfg.provider)
    h={'model':'claude-haiku-5-5','max_tokens':8000,'system':system,'messages':[g['messages'][1]],'output_config':{'effort':'low','format':{'type':'json_schema','schema':schema}}}
    assert g['model']=='gpt-6-luna' and g['max_completion_tokens']==8000
    return item,text,uni,setting,schema,g,h

def prepare():
    RUN.mkdir(exist_ok=False);manifest={};reserve=0
    for name in IDS:
      for arm in ('clean','page'):
        item,text,uni,setting,schema,g,h=source(name,arm)
        if arm=='clean':
            with sqlite3.connect(f'file:{ARCHIVE}?mode=ro',uri=True) as db:
                n=db.execute('select count(*) from model_calls where request_sha256=?',(model.request_identity(g)[1],)).fetchone()[0]
            assert n==1,(name,n)
        else:
            clean=source(name,'clean');assert clean[4]==schema and clean[5]['messages'][0]==g['messages'][0]
            assert clean[5]['messages'][1]['content'].replace(clean[1],'BODY',1)==g['messages'][1]['content'].replace(text,'BODY',1)
        a=3*len(wire(g))+16384;b=3*len(wire(h))+16384;high=b>100000
        ir,orr=(.5,2.5) if high else (.1,.5)
        cost=3*(a*.1+8064*.5)/1e6+3*(b*ir+8064*orr)/1e6;reserve+=cost
        for provider,request in [('gpt',g),('haiku',h)]:put(f'{name}-{arm}-{provider}-request.json',request)
        manifest[f'{name}-{arm}']={'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'input_bounds':{'gpt':a,'haiku':b},'haiku_high':high,'reserve':cost,'files':{f'{name}-{arm}-{p}-request.json':digest(RUN/f'{name}-{arm}-{p}-request.json') for p in ('gpt','haiku')}}
    assert reserve<.60,reserve
    files=sorted((ROOT/'src/hivemind').rglob('*.py'))+sorted((ROOT/'src/hivemind/prompts').glob('*'))
    put('manifest.json',{'cases':manifest,'design_sha256':digest(DESIGN),'script_sha256':digest(Path(__file__)),'code_hashes':{str(p):digest(p) for p in files if p.is_file()},'reserved_usd':reserve,'planned':36})
    print('prepared',len(manifest),'request pairs, 36 calls, reserved',round(reserve,6),flush=True)

def verify():
    m=read('manifest.json');assert m['reserved_usd']<.60 and m['design_sha256']==digest(DESIGN) and m['script_sha256']==digest(Path(__file__))
    for path,h in m['code_hashes'].items():assert digest(Path(path))==h,path
    for key,v in m['cases'].items():
        name,arm=key.split('-');item,text,uni,setting,schema,g,h=source(name,arm)
        assert hashlib.sha256(text.encode()).hexdigest()==v['text_sha256']
        for provider,req in [('gpt',g),('haiku',h)]:
            fn=f'{name}-{arm}-{provider}-request.json';assert digest(RUN/fn)==v['files'][fn] and wire(req)==wire(read(fn))
    item,text,uni,setting,schema,g,_=source('science','clean')
    with sqlite3.connect(f'file:{ARCHIVE}?mode=ro',uri=True) as db:
        saved=db.execute('select answer_json from model_calls where request_sha256=?',(model.request_identity(g)[1],)).fetchone()
    answer=json.loads(saved[0]);assert not model.check_schema(answer,schema) and answer['evidence']
    bad=json.loads(json.dumps(answer));del bad['evidence'][0]['quote'];assert model.check_schema(bad,schema)
    extraction.sift_with_groups(answer,item,text,set(),uni,english=True,shown_group_ids=(),version=setting.prompt_version.rpartition('-')[2],keep_unlinked=True)
    print('requests, sources, frozen code and schema positive/negative controls verified',flush=True)

def one(job):
    name,arm,provider,n=job;start=time.monotonic()
    try:
        req=read(f'{name}-{arm}-{provider}-request.json')
        if provider=='haiku':
            response=probe.haiku_api('https://api.anthropic.com/v1/messages',req);complete=response.get('stop_reason')=='end_turn';content=''.join(x.get('text','') for x in response.get('content',[]) if x.get('type')=='text')
        else:
            response=probe.previous.api('gpt','https://api.openai.com/v1/chat/completions',req);complete=response['choices'][0]['finish_reason']=='stop';content=response['choices'][0]['message'].get('content') or ''
        try:answer=json.loads(content)
        except (ValueError,TypeError):answer=None
        item,text,uni,setting,schema,_,_=source(name,arm);errors=model.check_schema(answer,schema)
        record={'response':response,'answer':answer,'completed':complete,'schema_errors':errors,'seconds':round(time.monotonic()-start,2)}
        if complete and not errors:
            try:
                e,c,d,g=extraction.sift_with_groups(answer,item,text,set(),uni,english=True,shown_group_ids=(),version=setting.prompt_version.rpartition('-')[2],keep_unlinked=True)
                record['sift']={'evidence':e,'candidates':c,'dropped':d,'new_groups':g}
            except Exception as exc:record['sift_error']=type(exc).__name__
    except urllib.error.HTTPError as exc:record={'error':'HTTP error','http_status':exc.code,'seconds':round(time.monotonic()-start,2)}
    except Exception as exc:record={'error':type(exc).__name__,'seconds':round(time.monotonic()-start,2)}
    put(f'{name}-{arm}-{provider}-{n}.json',record)
    print(*job,'complete',record.get('completed',False),'error',record.get('error'),'schema_errors',len(record.get('schema_errors',[])),flush=True)
    return record

def anomaly(job,r):
    name,arm,p,_=job;usage=r.get('response',{}).get('usage')
    if not usage:return False
    v=read('manifest.json')['cases'][f'{name}-{arm}'];bound=v['input_bounds'][p]
    if p=='haiku':
        inp=sum(usage.get(k,0) for k in ('input_tokens','cache_creation_input_tokens','cache_read_input_tokens'));out=usage.get('output_tokens',0)
        return inp>bound or out>8064 or (inp>100000 and not v['haiku_high'])
    return usage.get('prompt_tokens',0)>bound or usage.get('completion_tokens',0)>8064

def worker():
    verify();jobs=[(name,arm,provider,i) for name in IDS for arm in ('clean','page') for i in (1,2,3) for provider in ('haiku','gpt')];pending={};done=[];stopped=False
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
      while jobs or pending:
        while jobs and len(pending)<8 and not stopped:
            job=jobs.pop(0);pending[pool.submit(one,job)]=job
        if not pending:break
        finished,_=concurrent.futures.wait(pending,return_when=concurrent.futures.FIRST_COMPLETED)
        for f in finished:
            job=pending.pop(f);r=f.result();done.append({'job':job,'completed':r.get('completed',False),'error':r.get('error'),'usage':r.get('response',{}).get('usage')})
            if anomaly(job,r) or r.get('error')=='HTTP error':stopped=True
    put('run-summary.json',{'planned':36,'sent':len(done),'not_sent':jobs,'stopped':stopped,'samples':done,'semantic_status':'pending source-by-source human-model review'})
    print('finished',len(done),'unsent',len(jobs),'stopped',stopped,flush=True)

def launch():
    verify();probe.haiku_api('https://api.anthropic.com/v1/models/claude-haiku-5-5')
    assert not (RUN/'run.pid').exists()
    with (RUN/'run.log').open('x') as log:
        p=subprocess.Popen([sys.executable,str(Path(__file__)), 'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONPATH=str(ROOT/'src')))
    (RUN/'run.pid').write_text(str(p.pid)+'\n');print('detached pid',p.pid,flush=True)

if __name__=='__main__':{'prepare':prepare,'verify':verify,'launch':launch,'worker':worker}[sys.argv[1]]()
