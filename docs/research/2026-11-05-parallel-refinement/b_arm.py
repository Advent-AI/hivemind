# -*- coding: utf-8 -*-
"""Freeze and run a single schema-description diagnostic against real historical articles."""
import copy,hashlib,json,sqlite3,sys,threading
from concurrent.futures import ThreadPoolExecutor,wait,FIRST_COMPLETED
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OLD=ROOT/'docs/research/2026-11-05-parallel-thesis-evidence-poc'
sys.path[:0]=[str(OLD),str(ROOT/'src')]
import prepare as prior,run_poc
from hivemind import config,extraction,model,universe
EXTRA=[('gnews:085b1e1a1543437edb9756d6',55),('gnews:3df0bbc8aff2c1d008bc0a32',63),('gnews:4d1b1ca014068fb532f116b3',65),('gnews:795ea94e1100415a67fd1a96',69),('gnews:c75f16a6d64cc27fc28fb571',75),('gnews:d0f3f83296df884fae64921e',90)]
ORIGINAL='IDs of supplied existing questions this evidence can inform; never a candidate ID.'
NEW=("The questions this statement is filed under, decided after you have decided it is evidence: the id of the narrowest open question in [Open questions] whose answer this statement makes more or less likely, as that question's own figure, step or estimate or through the demand, supply, competition or pricing behind its answer; compare the specific questions before a company-wide revenue or margin question and take that one only, never a broader question beside it; a shared company, industry, event or ecosystem is not a connection, and the statement need not repeat the question's words (a variant, sibling or other name of the subject counts); whoever says it, and even when it gives no period, basis or exact amount, because the weight is judged later; an estimate for another period or population of a question's quantity is filed under it when no open question covers that period; when no specific question is connected, a statement that moves the demand, supply, competition or pricing behind the company's results goes to the company-wide revenue question of its period. A relevant quarterly actual or forecast can inform an annual question. A material assumption or condition of a forecast can inform the same question when it changes how the forecast is understood; preserve its uncertainty. Use only the supplied existing question ids; empty when no question is connected, however important the statement sounds.")
def sha(b):return hashlib.sha256(b).hexdigest()
def wire(r):return sha(json.dumps(r).encode())
def base_requests():
 cfg,uni,old=prior.prepare();records=[r for r in old if r['arm']=='existing']
 saved=json.loads((OLD/'frozen-requests.json').read_text())
 for r in records:
  original=next(x for x in saved if x['id']==r['item']['input_id'] and x['arm']=='existing')
  if wire(r['request'])!=original['request_sha256'] or r['shown']!=original['snapshot']:raise ValueError('original four changed')
 items=prior.ro(prior.INPUT/'items.sqlite');views=prior.ro(prior.INPUT/'views.sqlite')
 for ident,seq in EXTRA:
  row=items.execute('select * from items where input_id=?',(ident,)).fetchone()
  if not row:raise ValueError('missing article '+ident)
  item=prior.testdb.item_of(row)
  if not item['text'] or len(item['text'])>extraction.MAX_TEXT_CHARS:raise ValueError('missing or truncated source '+ident)
  rows=views.execute("select distinct sequence_no from processing_steps where input_id=? and step='dispatched'",(ident,)).fetchall()
  if len(rows)!=1 or rows[0][0]!=seq:raise ValueError('sequence mismatch '+ident)
  shown=prior.snapshot(views,seq)
  if not shown:raise ValueError('no existing questions '+ident)
  setting,_,user,schema=extraction.request_for(cfg,item,item['text'],shown,uni)
  oldhead=f'[Open questions at the start of {item["publication_day"]}]';newhead='[Open questions immediately before this item]'
  if user.count(oldhead)!=1 or user.count(extraction.GROUPS_INSTRUCTION)!=1 or user.count(extraction.CLOSING)!=1:raise ValueError('unexpected user block')
  user=user.replace(oldhead,newhead,1).replace(extraction.GROUPS_INSTRUCTION,'[Research groups] Use the supplied question descriptions to understand their scope.',1)
  start=user.find('[Research reference]');end=user.find(newhead)
  if start!=-1:
   if end<start:raise ValueError('unexpected reference position')
   user=user[:start]+user[end:]
  user=user.replace('For a candidate thesis about a company, object is its ticker; about a theme, choose an id from this list, or state what the matter is when none fits:', 'Theme identifiers:',1)
  user=user.replace(extraction.CLOSING,'Return only evidence per the schema. Each evidence link must be an ID of a supplied existing question.',1)
  schema=copy.deepcopy(schema);schema['properties']['evidence']['items']['properties']['links']['description']=ORIGINAL
  schema['properties']={'evidence':schema['properties']['evidence']};schema['required']=['evidence']
  system=(OLD/'existing-evidence.txt').read_text();request=model.build_request(setting,system,user,schema,'extraction',cfg.provider)
  records.append(dict(item=item,shown=shown,setting=setting,system=system,user=user,schema=schema,request=request,arm='existing',seq=seq))
 items.close();views.close()
 # Apply the same standard-alignment correction to both arms before comparison.
 for r in records:
  user=r['user']
  a="- a share-price move, an investor's position or trade, or the market value"
  b="- a share-price move or an investor's position or trade"
  if user.count(a)!=1:raise ValueError('missing shared closing check')
  user=user.replace(a,b,1)
  anchor='it does not cover the news behind the move;'
  if user.count(anchor)!=1:raise ValueError('missing optional-valuation boundary')
  user=user.replace(anchor,anchor+" the covered company's market value, a standalone valuation multiple, and its share-price reaction after earnings are optional;",1)
  anchor='Most of an item is background, but a page with eight statements that pass yields eight evidence items, not a selection.'
  # This sentence belongs to the system text in the prior POC; retain the exact shared system.
  if anchor not in r['system']:raise ValueError('missing shared system boundary')
  review='Before you return the answer, check it once.'
  if user.count(review)!=1:raise ValueError('missing shared review')
  user=user.replace(review,review+' A clearly retold past actual figure may be kept or omitted; still-effective guidance and forecasts retain their usual weight.',1)
  r['user']=user
  r['request']=model.build_request(r['setting'],r['system'],user,r['schema'],'extraction',cfg.provider)
 sources=json.loads((HERE/'source-only-inputs.json').read_text())
 for r in records:
  a=next(x for x in sources if x['input_id']==r['item']['input_id'])
  if a['seq']!=r['seq'] or a['article']!=r['item']['text'] or a['questions']!=r['shown']:raise ValueError('source-only packet mismatch')
 return cfg,uni,records

def variants():
 cfg,uni,base=base_requests();result=[]
 for b in base:
  for arm in ('control','treatment'):
   r=dict(b);r['schema']=copy.deepcopy(b['schema']);desc=r['schema']['properties']['evidence']['items']['properties']['links']
   if desc['description']!=ORIGINAL:raise ValueError('unexpected field')
   if arm=='treatment':desc['description']=NEW
   r['request']=model.build_request(r['setting'],r['system'],r['user'],r['schema'],'extraction',cfg.provider);r['variant']=arm
   if arm=='treatment':
    normalized=copy.deepcopy(r['request']);normalized['response_format']['json_schema']['schema']['properties']['evidence']['items']['properties']['links']['description']=ORIGINAL
    if json.dumps(normalized)!=json.dumps(b['request']):raise ValueError('more than one field changed')
   result.append(r)
 return cfg,uni,result

def frozen(records):
 files=[Path(__file__),OLD/'prepare.py',OLD/'run_poc.py',OLD/'existing-evidence.txt',ROOT/'poc/config/poc-v117.json',ROOT/'poc/universe.json',prior.INPUT/'views.sqlite',prior.INPUT/'items.sqlite',HERE/'source-only-inputs.json',HERE/'source-map-reader-a.md',HERE/'source-map-reader-b.md',HERE/'source-map-corrections.md',HERE/'b-link-schema-design.md',HERE/'b-prompt-audit.md',HERE/'preflight.txt']
 files+=sorted((ROOT/'src/hivemind').rglob('*.py'))
 return {'files':{str(f):sha(f.read_bytes()) for f in files},'requests':[{'id':r['item']['input_id'],'seq':r['seq'],'variant':r['variant'],'question_count':len(r['shown']),'question_sha256':sha(json.dumps(r['shown'],sort_keys=True).encode()),'body_sha256':sha(r['item']['text'].encode()),'wire_sha256':wire(r['request']),'request':r['request']} for r in records]}

def simulate(cfg,uni,records,out):
 for i,r in enumerate(records):
  evidence={'id':'e1','quote':r['item']['text'][:100],'one_line':'A source statement.','speaker':'Source','original_who':'','original_day':'','tier':'fact','event_time':'','links':[r['shown'][0]['view_id']]}
  response={'evidence':[evidence]}
  if model.check_schema(response,r['schema']):raise ValueError('positive schema')
  class Dummy:call_id=0;request_sha256='fake';cached=False;cost_usd=0
  h=run_poc.handover(response,r,uni,Dummy())
  if len(h['evidence'])!=1:raise ValueError('positive linkage')
  negative=copy.deepcopy(response);negative['evidence'][0]['links']=['missing-view']
  h=run_poc.handover(negative,r,uni,Dummy())
  if h['evidence'] or not h['dropped']:raise ValueError('invalid link survived')
  negative=copy.deepcopy(response);negative['evidence'][0]['quote']='Fabricated wording that never appeared in the original source.'
  if run_poc.handover(negative,r,uni,Dummy())['evidence']:raise ValueError('invalid quote survived')
  if not model.check_schema({'evidence':[], 'candidates':[]},r['schema']):raise ValueError('schema negative did not fail')
  archive=model.Archive(str(out/f'fake-{i}.sqlite'))
  try:
   def fake(provider,request):
    if wire(request)!=wire(r['request']):raise ValueError('wire mismatch')
    return {'choices':[{'message':{'content':json.dumps(response)}}],'usage':{'prompt_tokens':0,'completion_tokens':0}}
   ans=model.call(archive,cfg,r['setting'],r['system'],r['user'],r['schema'],'extraction','extract',transport=fake)
   if ans.cached or len(run_poc.handover(ans.data,r,uni,ans)['evidence'])!=1:raise ValueError('transport/control failure')
  finally:archive.conn.close()
 # Exercise raw vs retained multi-home reporting, not economic relevance.
 r=records[0];parents={v['view_id']:v.get('parents') or [] for v in r['shown']}
 pair=next((a['view_id'],b['view_id']) for a in r['shown'] for b in r['shown'] if a['view_id']!=b['view_id'] and len(extraction.narrowest_links([a['view_id'],b['view_id']],parents))==2)
 item={'id':'e-multi','quote':r['item']['text'][:100],'one_line':'A source statement.','speaker':'Source','original_who':'','original_day':'','tier':'fact','event_time':'','links':list(pair)}
 raw={'evidence':[item]};h=run_poc.handover(raw,r,uni,Dummy())
 if len(multi_home(raw['evidence']))!=1 or len(multi_home(h['evidence']))!=1:raise ValueError('retained multi-home not reported')
 dropped=copy.deepcopy(raw);dropped['evidence'][0]['quote']='No such source quote appears in this article.'
 h=run_poc.handover(dropped,r,uni,Dummy())
 if len(multi_home(dropped['evidence']))!=1 or multi_home(h['evidence']):raise ValueError('raw multi-home lost from report')
 repeated=copy.deepcopy(raw);repeated['evidence'][0]['links']=[pair[0],pair[0]]
 if multi_home(repeated['evidence']):raise ValueError('duplicate same ID falsely counted')
 # Use a synthetic parent relation to exercise the actual code's narrowing path.
 with_parent=dict(r);with_parent['shown']=copy.deepcopy(r['shown'])
 child=next(v for v in with_parent['shown'] if v['view_id']==pair[0]);child['parents']=[pair[1]]
 narrowed=run_poc.handover(raw,with_parent,uni,Dummy())
 if len(multi_home(raw['evidence']))!=1 or multi_home(narrowed['evidence']) or narrowed['evidence'][0]['links']!=[pair[0]]:raise ValueError('parent narrowing raw/checked report')
 print('fake',len(records),'structural link, source quote and schema checks passed; semantic relevance is not tested',flush=True)

def multi_home(entries):
 return [{'id':e['id'],'links':e['links']} for e in entries if len(set(e['links']))>1]

def send_one(cfg,uni,r,draw,out,injected=None):
 directory=out/(r['item']['input_id'].replace(':','_')+'-'+r['variant']+'-'+str(draw));directory.mkdir();archive=model.Archive(str(directory/'archive.sqlite'));responses=[]
 def transport(provider,request):
  if wire(request)!=wire(r['request']):raise ValueError('wire mismatch')
  response=(injected or model.openai_transport)(provider,request);responses.append(response);(directory/'response.json').write_text(json.dumps(response,ensure_ascii=False)+'\n');return response
 try:
  ans=model.call(archive,cfg,r['setting'],r['system'],r['user'],r['schema'],'extraction','extract',transport=transport)
  if ans.cached:raise ValueError('unexpected cached answer')
  h=run_poc.handover(ans.data,r,uni,ans)
  result={'status':'ok','id':r['item']['input_id'],'variant':r['variant'],'draw':draw,'answer':ans.data,'handover':h,'raw_multi_home':multi_home(ans.data['evidence']),'checked_multi_home':multi_home(h['evidence'])}
 except Exception as error:result={'status':'failed','id':r['item']['input_id'],'variant':r['variant'],'draw':draw,'error':repr(error),'response_received':bool(responses)}
 finally:archive.conn.close()
 (directory/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(result['status'],result['id'],r['variant'],draw,flush=True);return result

def schedule(tasks,invoke,workers):
 failed=False;finished=[];submitted=[]
 with ThreadPoolExecutor(max_workers=workers) as pool:
  pending={};iterator=iter(tasks)
  def fill():
   while not failed and len(pending)<workers:
    try:task=next(iterator)
    except StopIteration:return
    submitted.append(task);pending[pool.submit(invoke,task)]=task
  fill()
  while pending:
   done,_=wait(pending,return_when=FIRST_COMPLETED)
   for f in done:
    task=pending.pop(f)
    try:result=f.result()
    except Exception as error:result={'status':'failed','error':repr(error),'stage':'worker'}
    finished.append(result)
    if result['status']!='ok':failed=True
   fill()
 return finished,submitted,failed

def fake_failure(cfg,uni,records,out):
 r=records[0]
 def invalid(provider,request):return {'choices':[{'message':{'content':json.dumps({'evidence':[],'candidates':[]})}}]}
 result=send_one(cfg,uni,r,0,out,injected=invalid)
 if result['status']!='failed' or not result['response_received']:raise ValueError('schema failure not recorded')
 barrier=threading.Barrier(2)
 def invoke(task):
  if task=='never':raise ValueError('started after failure')
  barrier.wait(timeout=5)
  if task=='good':threading.Event().wait(0.2)
  if task=='bad':raise RuntimeError('synthetic worker exception')
  return {'status':'ok'}
 finished,submitted,failed=schedule(['bad','good','never'],invoke,2)
 if not failed or submitted!=['bad','good'] or len(finished)!=2:raise ValueError('failure did not halt scheduling')
 print('fake provider schema failure preserved; scheduler stopped with incomplete measurement',flush=True)

def main():
 if len(sys.argv)!=3 or sys.argv[1] not in ('freeze','fake','send'):raise SystemExit('freeze|fake|send NEW_ABSOLUTE_DIRECTORY')
 mode=sys.argv[1];out=Path(sys.argv[2]);
 if not out.is_absolute() or out.exists():raise ValueError('new absolute output required')
 cfg,uni,records=variants();manifest=HERE/'b-arm-frozen-v2.json'
 if mode=='freeze':
  if manifest.exists():raise ValueError('manifest exists')
  out.mkdir(parents=True);f=frozen(records);manifest.write_text(json.dumps(f,ensure_ascii=False,indent=2)+'\n');print('frozen requests',len(records),'manifest',sha(manifest.read_bytes()),'field chars',len(ORIGINAL),'->',len(NEW));return
 if not manifest.exists() or frozen(records)!=json.loads(manifest.read_text()):raise ValueError('manifest mismatch')
 out.mkdir(parents=True)
 if mode=='fake':
  simulate(cfg,uni,records,out);fake_failure(cfg,uni,records,out);(HERE/'b-arm-fake-proof-v2.json').write_text(json.dumps({'manifest_sha256':sha(manifest.read_bytes()),'requests':20,'status':'ok'})+'\n');return
 proof=json.loads((HERE/'b-arm-fake-proof-v2.json').read_text());assert proof=={'manifest_sha256':sha(manifest.read_bytes()),'requests':20,'status':'ok'}
 tasks=[(r,draw) for draw in (1,2,3) for r in records]
 (out/'complete.json').write_text(json.dumps({'status':'incomplete','requested':len(tasks),'completed':0})+'\n')
 finished=[];status='incomplete'
 try:
  finished,submitted,failed=schedule(tasks,lambda task:send_one(cfg,uni,task[0],task[1],out),8)
  status='ok' if len(finished)==len(tasks) and not failed else 'incomplete'
 finally:
  (out/'complete.json').write_text(json.dumps({'status':status,'requested':len(tasks),'completed':len(finished)})+'\n')
 if status!='ok':raise SystemExit('incomplete; do not resume automatically')
if __name__=='__main__':main()
