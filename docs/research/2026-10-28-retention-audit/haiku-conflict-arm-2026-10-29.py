"""One-instruction Haiku extraction arms against frozen source-read cases."""
import concurrent.futures, hashlib, importlib.util, json, os, random, sqlite3, subprocess, sys, time, urllib.error
from pathlib import Path
from hivemind import config, extraction, model, universe
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];RUN=HERE/'haiku-conflict-arm-2026-10-29';DESIGN=HERE/'haiku-conflict-arm-design-2026-10-29.md'
ITEMS='/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite';ARCHIVE='/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/archive.sqlite'
IDS={'stock':'gnews:2934d9634471f3560f8697e0','revenue':'gnews:71df54965281684cc500960f','cpu':'gnews:e4e5f1b5c0c68381e4c486e1','holdout':'gnews:4b34a84a492cb836ad1ba1ed'}
A="The author's forecasts, ratings and price targets with their figures; the facts and figures the author cites, with their original attribution. "
B='Return empty arrays only for a page with no business content.';NEW='Return empty arrays when no statements meet the evidence-keeping rules.'
spec=importlib.util.spec_from_file_location('probe',HERE/'haiku-extraction-probe-2026-10-29.py');probe=importlib.util.module_from_spec(spec);spec.loader.exec_module(probe)
wire=probe.previous.wire
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def put(name,obj):
 with (RUN/name).open('x',encoding='utf-8') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
def read(name):return json.loads((RUN/name).read_text())
def source(name):
 with sqlite3.connect(f'file:{ITEMS}?mode=ro',uri=True) as db:
  db.row_factory=sqlite3.Row;item=dict(db.execute('select * from items where input_id=?',(IDS[name],)).fetchone())
 assert item['category']=='T8';item['object_identifiers']=json.loads(item['object_identifiers']);cfg=config.load(str(ROOT/'poc/config/poc-v38.json'));uni=universe.load(str(ROOT/'poc/universe.json'))
 setting,system,user,schema=extraction.request_for(cfg,item,item['text'],[],uni,[]);g=model.build_request(setting,system,user,schema,'extraction',cfg.provider)
 h={'model':'claude-haiku-5-5','max_tokens':8000,'system':system,'messages':[g['messages'][1]],'output_config':{'effort':'low','format':{'type':'json_schema','schema':schema}}}
 assert user.count(A)==1 and user.count(B)==1 and g['model']=='gpt-6-luna'
 return item,uni,setting,schema,g,h
def request(name,arm):
 item,uni,setting,schema,g,h=source(name);h=json.loads(json.dumps(h));user=h['messages'][0]['content']
 if arm=='a':h['messages'][0]['content']=user.replace(A,'',1)
 if arm=='b':h['messages'][0]['content']=user.replace(B,NEW,1)
 return h
def prepare():
 RUN.mkdir(exist_ok=False);entries={};total=0
 for name in IDS:
  item,uni,setting,schema,g,h=source(name)
  with sqlite3.connect(f'file:{ARCHIVE}?mode=ro',uri=True) as db:n=db.execute('select count(*) from model_calls where request_sha256=?',(model.request_identity(g)[1],)).fetchone()[0]
  assert n==(0 if name=='holdout' else 1),(name,n)
  for arm in ('control','a','b'):
   req=request(name,arm);bound=3*len(wire(req))+16384;high=bound>100000;ir,orr=(.5,2.5) if high else (.1,.5);reserve=3*(bound*ir+8064*orr)/1e6;total+=reserve
   file=f'{name}-{arm}-request.json';put(file,req);entries[f'{name}-{arm}']={'file':file,'sha256':digest(RUN/file),'source_sha256':hashlib.sha256(item['text'].encode()).hexdigest(),'input_bound':bound,'high':high,'reserve':reserve}
 assert total<.6,total
 files=sorted((ROOT/'src/hivemind').rglob('*.py'))+sorted((ROOT/'src/hivemind/prompts').glob('*'))
 put('manifest.json',{'entries':entries,'design_sha256':digest(DESIGN),'script_sha256':digest(Path(__file__)),'code_hashes':{str(p):digest(p) for p in files if p.is_file()},'reserve':total,'cap':.6,'planned':36})
 print('prepared 36 calls, reserve',round(total,6),flush=True)
def verify():
 m=read('manifest.json');assert m['reserve']<m['cap'] and m['design_sha256']==digest(DESIGN) and m['script_sha256']==digest(Path(__file__))
 for p,h in m['code_hashes'].items():assert digest(Path(p))==h
 for key,v in m['entries'].items():
  name,arm=key.split('-');item,*_=source(name);assert v['source_sha256']==hashlib.sha256(item['text'].encode()).hexdigest();assert digest(RUN/v['file'])==v['sha256'] and wire(read(v['file']))==wire(request(name,arm))
 item,uni,setting,schema,g,_=source('stock')
 with sqlite3.connect(f'file:{ARCHIVE}?mode=ro',uri=True) as db:row=db.execute('select answer_json from model_calls where request_sha256=?',(model.request_identity(g)[1],)).fetchone()
 ans=json.loads(row[0]);assert not model.check_schema(ans,schema)
 other=json.loads(json.dumps(ans));other['evidence']='not an array';assert model.check_schema(other,schema)
 print('requests and source hashes, schema positive/negative controls verified',flush=True)
def one(job):
 name,arm,i=job;start=time.monotonic()
 try:
  response=probe.haiku_api('https://api.anthropic.com/v1/messages',read(f'{name}-{arm}-request.json'));complete=response.get('stop_reason')=='end_turn';content=''.join(x.get('text','') for x in response.get('content',[]) if x.get('type')=='text')
  try:answer=json.loads(content)
  except (ValueError,TypeError):answer=None
  item,uni,setting,schema,_,_=source(name);errors=model.check_schema(answer,schema);r={'response':response,'answer':answer,'completed':complete,'schema_errors':errors,'seconds':round(time.monotonic()-start,2)}
  if complete and not errors:
   try:
    e,c,d,g=extraction.sift_with_groups(answer,item,item['text'],set(),uni,english=True,shown_group_ids=(),version=setting.prompt_version.rpartition('-')[2],keep_unlinked=True);r['sift']={'evidence':e,'candidates':c,'dropped':d,'new_groups':g}
   except Exception as exc:r['sift_error']=type(exc).__name__
 except urllib.error.HTTPError as exc:r={'error':'HTTP error','http_status':exc.code,'seconds':round(time.monotonic()-start,2)}
 except Exception as exc:r={'error':type(exc).__name__,'seconds':round(time.monotonic()-start,2)}
 put(f'{name}-{arm}-{i}.json',r);print(*job,'complete',r.get('completed',False),'error',r.get('error'),flush=True);return r
def abnormal(job,r):
 v=read('manifest.json')['entries'][f'{job[0]}-{job[1]}'];u=r.get('response',{}).get('usage')
 if not u:return False
 inp=sum(u.get(k,0) for k in ('input_tokens','cache_creation_input_tokens','cache_read_input_tokens'));return inp>v['input_bound'] or u.get('output_tokens',0)>8064 or (inp>100000 and not v['high'])
def worker():
 verify();jobs=[(n,a,i) for n in IDS for a in ('control','a','b') for i in (1,2,3)];random.Random(20261029).shuffle(jobs);pending={};done=[];stopped=False
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  while jobs or pending:
   while jobs and len(pending)<8 and not stopped:
    j=jobs.pop(0);pending[pool.submit(one,j)]=j
   if not pending:break
   fs,_=concurrent.futures.wait(pending,return_when=concurrent.futures.FIRST_COMPLETED)
   for f in fs:
    j=pending.pop(f);r=f.result();done.append({'job':j,'completed':r.get('completed',False),'error':r.get('error'),'usage':r.get('response',{}).get('usage')})
    if abnormal(j,r) or r.get('error')=='HTTP error':stopped=True
 put('summary.json',{'planned':36,'sent':len(done),'not_sent':jobs,'stopped':stopped,'samples':done});print('finished',len(done),'unsent',len(jobs),flush=True)
def launch():
 verify();probe.haiku_api('https://api.anthropic.com/v1/models/claude-haiku-5-5');assert not (RUN/'run.pid').exists()
 with (RUN/'run.log').open('x') as log:p=subprocess.Popen([sys.executable,str(Path(__file__)),'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONPATH=str(ROOT/'src')))
 (RUN/'run.pid').write_text(str(p.pid)+'\n');print('detached pid',p.pid,flush=True)
if __name__=='__main__':{'prepare':prepare,'verify':verify,'worker':worker,'launch':launch}[sys.argv[1]]()
