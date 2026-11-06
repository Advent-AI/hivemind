"""One existing-topic diagnostic with a source-verified article body, without its scraped comments."""
import hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path[:0]=[str(HERE),str(ROOT/'src')]
import b_arm
import simple_new_question_poc as simple
from hivemind import config,extraction,model,testdb,universe
ID='gnews:6dcaad557a1b21d7b867fe34'
OUT=ROOT/'poc/data/start-state-existing-topic-control-2026-11-05-v1'
END='Developers that produce great games will continue to produce great games; developers that produce terrible games will just produce terrible photorealistic games instead.'

def sha(x):return hashlib.sha256(x).hexdigest()
def build():
 cfg=config.load(str(ROOT/'poc/config/poc-v117.json'));uni=universe.load(str(ROOT/'poc/universe.json'))
 items=b_arm.prior.ro(b_arm.prior.INPUT/'items.sqlite');views=b_arm.prior.ro(b_arm.prior.INPUT/'views.sqlite')
 item=testdb.item_of(items.execute('select * from items where input_id=?',(ID,)).fetchone());raw=item['text']
 if raw.count(END)!=1 or 'My PC has an Intel 14700K' not in raw[raw.index(END)+len(END):]:raise ValueError('unexpected source boundary')
 article=raw[:raw.index(END)+len(END)];item['text']=article
 objects=[o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])];shown=extraction.shown_views(views,cfg,item,objects)
 if len(shown)!=68 or not any(q['view_id']=='v22' and 'DLSS 5' in q['question'] for q in shown):raise ValueError('existing DLSS subject missing')
 setting,_,user,_=extraction.request_for(cfg,item,article,shown,uni)
 category=user[:user.index('[Subjects]')];subjects=user[user.index('[Subjects]'):user.index('[What to read out]')]
 if subjects.count('; use that day as the due date.')!=1:raise ValueError('fiscal note changed')
 subjects=subjects.replace('; use that day as the due date.','.',1).replace('Fiscal-year note (a numeric thesis takes its year and due date from it):',"Fiscal-year context for the company's own quantities:",1)
 q=user[user.index('[Open questions at the start of '):user.index('[Research groups]')]
 articletext=f"[Article] id {ID}; date {item['publication_day']}; title {item['title']}; publisher {item['publisher']}\n{article}"
 payload=category+subjects+q+articletext;system=(HERE/'simple-new-question-prompt.txt').read_text()
 request=model.build_request(setting,system,payload,simple.schema(),'new_question',cfg.provider)
 items.close();views.close()
 return cfg,{'item':item,'shown':shown,'setting':setting,'system':system,'user':payload,'request':request},raw

def preview():
 cfg,r,raw=build();simple.fake_tests(cfg,[r])
 m={'source_id':ID,'source_uri':r['item']['source_uri'],'corroborating_republication':'https://tech.yahoo.com/gaming/articles/tried-nvidias-dlss-5-official-183013644.html','body_method':'Exact prefix ending at the last paragraph of the author article; removes two scraped reader comments. Current syndication confirms end; not a historically verified page version.','full_stored_sha256':sha(raw.encode()),'sent_body_sha256':sha(r['item']['text'].encode()),'question_ids':[q['view_id'] for q in r['shown']],'request':r['request']}
 if OUT.exists():raise ValueError('output exists')
 OUT.mkdir(parents=True);(OUT/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 print('Existing-topic preview: 68 questions, v22 includes DLSS 5; manifest SHA256',sha((OUT/'manifest.json').read_bytes()),flush=True)

def send(expected):
 cfg,r,raw=build();m=OUT/'manifest.json'
 if sha(m.read_bytes())!=expected or json.loads(m.read_text())['request']!=r['request']:raise ValueError('manifest or request changed')
 archive=model.Archive(str(OUT/'archive.sqlite'))
 def transport(provider,request):
  if provider!=cfg.provider or request!=r['request']:raise ValueError('request changed')
  response=model.openai_transport(provider,request);(OUT/'provider-response.json').write_text(json.dumps(response,ensure_ascii=False,indent=2)+'\n');return response
 try:
  answer=model.call(archive,cfg,r['setting'],r['system'],r['user'],simple.schema(),'new_question','extract',transport=transport)
  result={'id':ID,'answer':answer.data,'source_checks':simple.checked(answer.data,r['item']['text']),'input_tokens':answer.input_tokens,'output_tokens':answer.output_tokens,'cached':answer.cached}
  (OUT/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
  print('Existing-topic result:',json.dumps(result['answer'],ensure_ascii=False),flush=True)
 finally:archive.conn.close()
if __name__=='__main__':
 if len(sys.argv)==2 and sys.argv[1]=='preview':preview()
 elif len(sys.argv)==3 and sys.argv[1]=='send':send(sys.argv[2])
 else:raise SystemExit('preview | send manifest-sha256')
