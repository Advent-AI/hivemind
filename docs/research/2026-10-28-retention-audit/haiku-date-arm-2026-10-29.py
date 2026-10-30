"""One-variable Haiku date instruction: fresh controls and preselected source cases."""
import concurrent.futures
import copy
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

ROOT=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
sys.path.insert(0,str(ROOT/'src'))
from hivemind import config, extraction, model, universe

HERE=ROOT/'docs/research/2026-10-28-retention-audit'
RUN=HERE/'haiku-date-arm-2026-10-29'
DESIGN=HERE/'haiku-date-arm-design-v4-2026-10-29.md'
ITEMS='/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
ARCHIVE='/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/archive.sqlite'
IDS={'memory':'gnews:fbce0469dbb5b33e2c34a0f5','amd':'gnews:55b3b854d30ecb73679c2088',
     'growth':'gnews:71df54965281684cc500960f','policy':'gnews:f9e7da6ddbf890fa64baf922',
     'spending_holdout':'gnews:f8191f5bb960d79e47c73d6c', 'valar_holdout':'gnews:ad47330f25c9d5ff84ced7e2',
     'deepseek_holdout':'gnews:2957e5c79a365952140c8cce'}
BEFORE='Identify the speaker and, for a retelling, the original speaker and statement day.'
ADDITION=' If the item does not establish the original statement date, leave original_day empty.'
CAP=.60
spec=importlib.util.spec_from_file_location('haiku_probe',HERE/'haiku-extraction-probe-2026-10-29.py')
probe=importlib.util.module_from_spec(spec);spec.loader.exec_module(probe)


def put(name,obj):
 with (RUN/name).open('x',encoding='utf-8') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')


def read(name):return json.loads((RUN/name).read_text())


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def source(name):
 db=sqlite3.connect(f'file:{ITEMS}?mode=ro',uri=True);db.row_factory=sqlite3.Row
 item=dict(db.execute('select * from items where input_id=?',(IDS[name],)).fetchone());item['object_identifiers']=json.loads(item['object_identifiers'])
 cfg=config.load(str(ROOT/'poc/config/poc-v38.json'));uni=universe.load(str(ROOT/'poc/universe.json'))
 setting,system,user,schema=extraction.request_for(cfg,item,item['text'],[],uni,[])
 gpt=model.build_request(setting,system,user,schema,'extraction',cfg.provider)
 assert gpt['model']=='gpt-6-luna' and gpt['max_completion_tokens']==8000 and system.count(BEFORE)==1
 control={'model':'claude-haiku-5-5','max_tokens':8000,'system':system,'messages':[gpt['messages'][1]],
          'output_config':{'effort':'low','format':{'type':'json_schema','schema':schema}}}
 arm=copy.deepcopy(control);arm['system']=system.replace(BEFORE,BEFORE+ADDITION)
 assert arm['system'].replace(BEFORE+ADDITION,BEFORE)==control['system']
 d1=copy.deepcopy(control);d2=copy.deepcopy(arm);d1.pop('system');d2.pop('system');assert probe.previous.wire(d1)==probe.previous.wire(d2)
 return item,uni,setting,schema,gpt,control,arm


def prepare():
 RUN.mkdir(exist_ok=False);arc=sqlite3.connect(f'file:{ARCHIVE}?mode=ro',uri=True);meta={}
 for name in IDS:
  item,uni,setting,schema,gpt,control,arm=source(name);identity=model.request_identity(gpt)[1]
  matches=arc.execute('select count(*) from model_calls where request_sha256=?',(identity,)).fetchone()[0]
  if name in ('growth','spending_holdout','valar_holdout','deepseek_holdout'):assert matches==1
  files=[]
  for group,request in [('control',control),('arm',arm)]:
   file=f'{name}-{group}-request.json';put(file,request);files.append(file)
  meta[name]={'input_id':IDS[name],'split':'test' if name.endswith('_holdout') else 'development',
      'source_sha256':hashlib.sha256(item['text'].encode()).hexdigest(),'production_request_sha256':identity,'archive_matches':matches,
      'system_chars_control':len(control['system']),'system_chars_arm':len(arm['system']),'files':{n:sha(RUN/n) for n in files}}
  assert meta[name]['system_chars_arm']-meta[name]['system_chars_control']==len(ADDITION)==86
 put('manifest.json',{'articles':meta,'design_sha256':sha(DESIGN),'max_output_tokens':8000,'planned_calls':42,'cap_usd':CAP,
                      'note':'User-decided cases are development; independently pre-read test cases are model-authored, not human gold.'})
 print('prepared seven inputs, paired requests, 42 samples',flush=True)


def verify():
 m=read('manifest.json');assert m['design_sha256']==sha(DESIGN) and m['planned_calls']==42
 for name in IDS:
  item,uni,setting,schema,gpt,control,arm=source(name);a=m['articles'][name]
  assert a['source_sha256']==hashlib.sha256(item['text'].encode()).hexdigest() and a['production_request_sha256']==model.request_identity(gpt)[1]
  for file,digest in a['files'].items():assert sha(RUN/file)==digest
  assert probe.previous.wire(read(f'{name}-control-request.json'))==probe.previous.wire(control)
  assert probe.previous.wire(read(f'{name}-arm-request.json'))==probe.previous.wire(arm)
 item,uni,setting,schema,gpt,_,_=source('growth')
 db=sqlite3.connect(f'file:{ARCHIVE}?mode=ro',uri=True)
 answer=json.loads(db.execute('select answer_json from model_calls where request_sha256=?',(model.request_identity(gpt)[1],)).fetchone()[0])
 assert not model.check_schema(answer,schema) and len(answer['evidence'])>0
 def sift(data):return extraction.sift_with_groups(data,item,item['text'],set(),uni,english=True,shown_group_ids=(),version='v22',keep_unlinked=True)
 base=sift(answer);assert len(base[0])>0 and any(e['id']==answer['evidence'][0]['id'] for e in base[0]);first=answer['evidence'][0]['id']
 mutant=copy.deepcopy(answer);del mutant['evidence'][0]['quote'];assert model.check_schema(mutant,schema)
 mutant=copy.deepcopy(answer);mutant['evidence'][0]['quote']='Nonexistent decisive quote nowhere in this article, 42ab.'
 rejected=sift(mutant);assert any(eid==first and reason=='quote not in item' for eid,reason in rejected[2])
 mutant=copy.deepcopy(answer);mutant['evidence'].append(dict(copy.deepcopy(mutant['evidence'][0]),id='e999'))
 merged=sift(mutant);assert any(eid=='e999' and 'same quote as' in reason for eid,reason in merged[2])
 mutant=copy.deepcopy(answer);mutant['evidence'][0]['original_day']='2026-05'
 dated=sift(mutant);assert any(e['id']==first and e['original_day']=='' for e in dated[0])
 print('verified seven request pairs; historical control',len(answer['evidence']),'raw',len(base[0]),'kept; four negative checks exercised',flush=True)


def count_one(pair):
 name,group=pair;req=read(f'{name}-{group}-request.json')
 count_req={k:v for k,v in req.items() if k!='max_tokens'}
 result=probe.haiku_api('https://api.anthropic.com/v1/messages/count_tokens',count_req)
 n=result.get('input_tokens');assert isinstance(n,int) and n>0
 bound=max(3*n,3*len(probe.previous.wire(req)))+16384
 hi=bound>100000;unit=(bound*(.5 if hi else .1)+8064*(2.5 if hi else .5))/1e6
 return {'name':name,'group':group,'input_tokens':n,'wire_bytes':len(probe.previous.wire(req)),'input_bound':bound,'output_bound':8064,'high_tariff':hi,'reserve_per_call_usd':unit}


def count():
 verify();pairs=[(n,g) for n in IDS for g in ('control','arm')]
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: counts=list(pool.map(count_one,pairs))
 reserved=sum(x['reserve_per_call_usd']*3 for x in counts);assert reserved<CAP
 put('counts.json',{'requests':counts,'reserved_usd':reserved,'cap_usd':CAP,'count_method':'Anthropic count_tokens; free estimate; budget uses larger of 3x tokens or 3x wire bytes plus 16384',
                    'note':'Estimate, not provider-enforced ceiling; unknown usage retains full reservation.'})
 print('counted 14 paired requests; reserved USD',round(reserved,6),flush=True)
 for c in counts:print(c['name'],c['group'],'tokens',c['input_tokens'],'chars',read(f"{c['name']}-{c['group']}-request.json")['system'].__len__(),flush=True)


def one(name,group,number):
 start=time.monotonic()
 try:
  response=probe.haiku_api('https://api.anthropic.com/v1/messages',read(f'{name}-{group}-request.json'))
  complete=response.get('stop_reason')=='end_turn'
  content=''.join(c.get('text','') for c in response.get('content',[]) if c.get('type')=='text')
  try:answer=json.loads(content)
  except (ValueError,TypeError):answer=None
  item,uni,setting,schema,_,_,_=source(name);errors=model.check_schema(answer,schema)
  record={'response':response,'answer':answer,'completed':complete,'schema_errors':errors,'seconds':round(time.monotonic()-start,2)}
  if complete and not errors:
   try:
    e,c,d,g=extraction.sift_with_groups(answer,item,item['text'],set(),uni,english=True,shown_group_ids=(),version='v22',keep_unlinked=True)
    record['sift']={'evidence':e,'candidates':c,'dropped':d,'new_groups':g}
   except Exception as error:record['sift_error']=type(error).__name__
 except urllib.error.HTTPError as error:record={'error':'HTTPError','http_status':error.code,'seconds':round(time.monotonic()-start,2)}
 except Exception as error:record={'error':type(error).__name__,'seconds':round(time.monotonic()-start,2)}
 put(f'{name}-{group}-{number}.json',record)
 print(name,group,number,'completed',record.get('completed',False),'error',record.get('error'),flush=True)
 return record


def anomaly(name,group,record):
 usage=record.get('response',{}).get('usage')
 if usage is None:return False
 row=next(x for x in read('counts.json')['requests'] if x['name']==name and x['group']==group)
 inp=sum(usage.get(k,0) for k in ('input_tokens','cache_creation_input_tokens','cache_read_input_tokens'))
 out=usage.get('output_tokens',0);high=inp>100000
 cost=(inp*(.5 if high else .1)+out*(2.5 if high else .5))/1e6
 return inp>row['input_bound'] or out>row['output_bound'] or (high and not row['high_tariff']) or cost>row['reserve_per_call_usd']


def worker():
 verify();assert read('counts.json')['reserved_usd']<CAP
 jobs=[(n,g,i) for n in IDS for i in (1,2,3) for g in ('control','arm')];pending={};done=[];stopped=False
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  while jobs or pending:
   while jobs and len(pending)<8 and not stopped:
    job=jobs.pop(0);pending[pool.submit(one,*job)]=job
   if not pending:break
   finished,_=concurrent.futures.wait(pending,return_when=concurrent.futures.FIRST_COMPLETED)
   for future in finished:
    job=pending.pop(future);result=future.result();done.append({'job':job,'completed':result.get('completed',False),'error':result.get('error'),'usage':result.get('response',{}).get('usage')})
    if anomaly(job[0],job[1],result):stopped=True
 put('run-summary.json',{'planned':42,'sent':len(done),'not_sent':jobs,'stopped_on_anomaly':stopped,'samples':done,'semantic_status':'pending manual review'})
 print('finished',len(done),'remaining',len(jobs),'anomaly',stopped,flush=True)


def launch():
 verify();assert read('counts.json')['reserved_usd']<CAP and not (RUN/'run.pid').exists()
 with (RUN/'run.log').open('x') as log:
  p=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONPATH=str(ROOT/'src')))
 (RUN/'run.pid').write_text(str(p.pid)+'\n');print('detached pid',p.pid)


if __name__=='__main__':{'prepare':prepare,'verify':verify,'count':count,'worker':worker,'launch':launch}[sys.argv[1]]()
