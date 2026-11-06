"""Single-draw new-question diagnostic on two stored articles and the prior day-start ledger."""
import hashlib,json,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path[:0]=[str(HERE),str(ROOT/'src')]
import b_arm
import simple_new_question_poc as simple
from hivemind import config,extraction,model,testdb,universe
IDS=('gnews:69d682468e018e0065df5180','gnews:dbbde813240d4096829a72a9')
OUT=ROOT/'poc/data/start-state-new-question-diagnostic-2026-11-05-v1'

def digest(obj):return hashlib.sha256(json.dumps(obj,ensure_ascii=False).encode()).hexdigest()

def records():
 cfg=config.load(str(ROOT/'poc/config/poc-v117.json'));uni=universe.load(str(ROOT/'poc/universe.json'))
 items=b_arm.prior.ro(b_arm.prior.INPUT/'items.sqlite');views=b_arm.prior.ro(b_arm.prior.INPUT/'views.sqlite')
 day=views.execute("select seq from days_completed where day='2026-08-28' order by id desc limit 1").fetchone()
 if not day or day[0]!=1204:raise ValueError('wrong historical start state')
 system=(HERE/'simple-new-question-prompt.txt').read_text();result=[]
 for ident in IDS:
  row=items.execute('select * from items where input_id=?',(ident,)).fetchone()
  if not row:raise ValueError('missing item')
  item=testdb.item_of(row)
  if item['publication_day']!='2026-08-29' or not item['text']:raise ValueError('wrong source')
  objects=[o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
  shown=extraction.shown_views(views,cfg,item,objects)
  if len(shown)!=68:raise ValueError('unexpected day-start question set')
  setting,_,raw,_=extraction.request_for(cfg,item,item['text'],shown,uni)
  category=raw[:raw.index('[Subjects]')]
  subjects=raw[raw.index('[Subjects]'):raw.index('[What to read out]')]
  if subjects.count('; use that day as the due date.')!=1:raise ValueError('fiscal note changed')
  subjects=subjects.replace('; use that day as the due date.','.',1).replace('Fiscal-year note (a numeric thesis takes its year and due date from it):',"Fiscal-year context for the company's own quantities:",1)
  questions=raw[raw.index('[Open questions at the start of '):raw.index('[Research groups]')]
  article=f"[Article] id {ident}; date {item['publication_day']}; title {item['title']}; publisher {item['publisher']}\n{item['text']}"
  user=category+subjects+questions+article
  request=model.build_request(setting,system,user,simple.schema(),'new_question',cfg.provider)
  result.append({'item':item,'shown':shown,'setting':setting,'system':system,'user':user,'request':request})
 items.close();views.close();return cfg,result

def preview():
 cfg,rs=records();simple.fake_tests(cfg,rs)
 manifest={'description':'Single draw, 8/29; actual 8/28 day-start library; source historical completeness unverified; not acceptance.', 'requests':[{'id':r['item']['input_id'],'title':r['item']['title'],'source_uri':r['item']['source_uri'],'question_ids':[q['view_id'] for q in r['shown']],'question_count':len(r['shown']),'article_sha256':hashlib.sha256(r['item']['text'].encode()).hexdigest(),'request_sha256':digest(r['request']),'request':r['request']} for r in rs]}
 if OUT.exists():raise ValueError('output exists')
 OUT.mkdir(parents=True);(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print('Prepared',len(rs),'requests, questions each:',[len(r['shown']) for r in rs], 'manifest SHA256',hashlib.sha256((OUT/'manifest.json').read_bytes()).hexdigest(),flush=True)

def send(expected):
 cfg,rs=records();manifest=OUT/'manifest.json'
 if hashlib.sha256(manifest.read_bytes()).hexdigest()!=expected:raise ValueError('manifest digest mismatch')
 saved=json.loads(manifest.read_text())
 for r,m in zip(rs,saved['requests']):
  if r['item']['input_id']!=m['id'] or digest(r['request'])!=m['request_sha256'] or r['request']!=m['request']:raise ValueError('input changed')
 for r in rs:
  p=OUT/r['item']['input_id'].replace(':','_');p.mkdir()
  archive=model.Archive(str(p/'archive.sqlite'))
  def transport(provider,request):
   if provider!=cfg.provider or request!=r['request']:raise ValueError('wire drift')
   response=model.openai_transport(provider,request)
   (p/'provider-response.json').write_text(json.dumps(response,ensure_ascii=False,indent=2)+'\n')
   return response
  try:
   answer=model.call(archive,cfg,r['setting'],r['system'],r['user'],simple.schema(),'new_question','extract',transport=transport)
   out={'id':r['item']['input_id'],'answer':answer.data,'source_checks':simple.checked(answer.data,r['item']['text']),'input_tokens':answer.input_tokens,'output_tokens':answer.output_tokens,'request_sha256':answer.request_sha256,'cached':answer.cached}
   (p/'result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
   print(out['id'],'questions',len(out['answer']['questions']),'source checks',out['source_checks'],flush=True)
  finally:archive.conn.close()
if __name__=='__main__':
 if len(sys.argv)==2 and sys.argv[1]=='preview':preview()
 elif len(sys.argv)==3 and sys.argv[1]=='send':send(sys.argv[2])
 else:raise SystemExit('preview | send manifest-sha256')
