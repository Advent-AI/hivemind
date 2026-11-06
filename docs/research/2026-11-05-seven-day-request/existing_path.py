"""Experimental A-pass/B-only pair on a real historical article and prior-day ledger."""
import copy,hashlib,json,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
REF=ROOT/'docs/research/2026-11-05-parallel-refinement'
OLD=ROOT/'docs/research/2026-11-05-parallel-thesis-evidence-poc'
sys.path[:0]=[str(HERE),str(REF),str(OLD),str(ROOT/'src')]
import start_state_existing_control as saved_a
import b_arm,run_poc,run_structure_v2
from hivemind import extraction,model,placement,universe

OUT=ROOT/'poc/data/split-existing-path-2026-11-05-v2'
SNAP=ROOT/'poc/data/pilot-d369-existing-library-v2/views.sqlite'
A_DIR=ROOT/'poc/data/start-state-existing-topic-control-2026-11-05-v1'
A_ID='gnews:6dcaad557a1b21d7b867fe34'

def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def wire(x):return json.dumps(x).encode()

def build():
 cfg,a,full=saved_a.build();uni=universe.load(str(ROOT/'poc/universe.json'))
 am=json.loads((A_DIR/'manifest.json').read_text());ar=json.loads((A_DIR/'result.json').read_text())
 response=json.loads((A_DIR/'provider-response.json').read_text())
 try:provider_answer=json.loads(response['choices'][0]['message']['content'])
 except (KeyError,IndexError,TypeError,ValueError) as e:raise ValueError('saved A response invalid') from e
 if ar['answer']!={'questions':[]} or provider_answer!=ar['answer'] or wire(am['request'])!=wire(a['request']):raise ValueError('saved A is not an exact valid pass')
 body=a['item']['text'];body_sha=sha(body.encode())
 if am['sent_body_sha256']!=body_sha or am['full_stored_sha256']!=sha(full.encode()):raise ValueError('A source mismatch')
 item=copy.deepcopy(a['item']);identity={'source_id':A_ID,'body_sha256':body_sha,'publication_day':item['publication_day'],'source_uri':item['source_uri'],'derivation':'author-body-prefix-v1'}
 variant='derived:'+sha(canonical(identity))[:24];item['input_id']=variant;item['text']=body;item['text_article']=body;item['text_page']=body;item['text_chars']=len(body);item['content_sha256']=body_sha
 conn=b_arm.prior.ro(SNAP);objects=[x['value'] for x in item['object_identifiers'] if uni.has(x['value'])]
 shown=extraction.shown_views(conn,cfg,item,objects);conn.close()
 if shown!=a['shown'] or len(shown)!=68 or not any(q['view_id']=='v22' for q in shown):raise ValueError('shown library mismatch')
 setting,_,user,prod=extraction.request_for(cfg,item,body,shown,uni)
 head=f'[Open questions at the start of {item["publication_day"]}]';temporary='[Open questions immediately before this item]'
 if user.count(head)!=1 or user.count(extraction.GROUPS_INSTRUCTION)!=1 or user.count(extraction.CLOSING)!=1:raise ValueError('unexpected production request')
 user=user.replace(head,temporary,1)
 user=user.replace(extraction.GROUPS_INSTRUCTION,'[Research groups] Use the supplied question descriptions to understand their scope.',1)
 start=user.find('[Research reference]');end=user.find(temporary)
 if start!=-1:
  if end<start:raise ValueError('reference boundary')
  user=user[:start]+user[end:]
 user=user.replace('For a candidate thesis about a company, object is its ticker; about a theme, choose an id from this list, or state what the matter is when none fits:','Theme identifiers:',1)
 user=user.replace(extraction.CLOSING,'Return only evidence per the schema. Each evidence link must be an ID of a supplied existing question.',1)
 a1="- a share-price move, an investor's position or trade, or the market value";a2="- a share-price move or an investor's position or trade"
 if user.count(a1)!=1:raise ValueError('valuation boundary missing')
 user=user.replace(a1,a2,1);anchor='it does not cover the news behind the move;'
 if user.count(anchor)!=1:raise ValueError('valuation anchor missing')
 user=user.replace(anchor,anchor+" the covered company's market value, a standalone valuation multiple, and its share-price reaction after earnings are optional;",1)
 check='Before you return the answer, check it once.'
 if user.count(check)!=1:raise ValueError('review boundary missing')
 user=user.replace(check,check+' A clearly retold past actual figure may be kept or omitted; still-effective guidance and forecasts retain their usual weight.',1)
 user,labels=run_structure_v2.basis_labels(user,shown);user=user.replace(temporary,head,1)
 if user.count(head)!=1 or user.count(body)!=1:raise ValueError('source or label mismatch')
 system=(REF/'structure-v2-existing-evidence.txt').read_text();old='questions supplied from immediately before the item';new="questions supplied at the start of the item's day"
 if system.count(old)!=1:raise ValueError('B2 time wording changed')
 system=system.replace(old,new,1)
 schema={'type':'object','additionalProperties':False,'properties':{'evidence':copy.deepcopy(prod['properties']['evidence'])},'required':['evidence']}
 schema['properties']['evidence']['items']['properties']['links']['description']=b_arm.NEW
 request=model.build_request(setting,system,user,schema,'extraction',cfg.provider)
 r={'arm':'existing','item':item,'shown':shown,'setting':setting,'system':system,'user':user,'schema':schema,'request':request}
 return cfg,uni,r,{'source_identity':identity,'derived_id':variant,'a_request_sha256':sha(wire(am['request'])),'a_result_sha256':sha((A_DIR/'result.json').read_bytes()),'a_provider_response_sha256':sha((A_DIR/'provider-response.json').read_bytes()),'source_snapshot_sha256':sha(SNAP.read_bytes()),'shown_sha256':sha(canonical(shown)),'basis_labels':labels,'original_source_id':A_ID}

def check(raw,r,uni):
 errors=model.check_schema(raw,r['schema'])
 if errors:raise ValueError('B schema: '+str(errors))
 allowed={q['view_id'] for q in r['shown']};normalized=copy.deepcopy(raw);mapping=[]
 for i,e in enumerate(normalized['evidence'],1):
  if any(x not in allowed for x in e['links']):raise ValueError('B referenced unknown question')
  if not e['quote'].strip() or e['quote'] not in r['item']['text']:raise ValueError('B quote absent from sent article')
  mapping.append({'position':i,'raw_id':e['id'],'id':'e'+str(i)});e['id']='e'+str(i)
 dummy=type('Dummy',(),{'call_id':0,'request_sha256':'pair','cached':False,'cost_usd':0.0})()
 handover=run_poc.handover(normalized,r,uni,dummy)
 if any('same quote as' in reason for _,reason in handover['dropped']):raise ValueError('same-quote collision needs semantic review')
 return handover,mapping

def fake_controls(cfg,uni,r):
 quote="DLSS 5 isn't due for an official release until sometime later this year, but an unfinished version that slipped out with NBA 2K27 has allowed the RenoDX modding community to get it running with dozens of games."
 if quote not in r['item']['text']:raise ValueError('positive source control missing')
 one={'id':'local','quote':quote,'one_line':'The author reports DLSS 5 is not officially released yet.','speaker':'Nick Lewis','original_who':'Nick Lewis','original_day':'2026-08-29','tier':'third_party_view','event_time':'','links':['v22']}
 raw={'evidence':[one]};h,m=check(raw,r,uni)
 if len(h['evidence'])!=1 or h['evidence'][0]['links']!=['v22']:raise ValueError('valid evidence not kept')
 for name,change in [('bad_quote',{'quote':'A fake source passage not in the article.'}),('bad_link',{'links':['v999999']})]:
  bad=copy.deepcopy(raw);bad['evidence'][0].update(change)
  try:check(bad,r,uni)
  except ValueError:pass
  else:raise ValueError(name+' was not refused')
 empty=copy.deepcopy(raw);empty['evidence'][0]['links']=[];h,_=check(empty,r,uni)
 if h['evidence'] or not any('no home' in reason for _,reason in h['dropped']):raise ValueError('no-home was not reported')
 duplicate={'evidence':[one,dict(one,id='other',one_line='A different matter claimed from the same words.')]} 
 try:check(duplicate,r,uni)
 except ValueError as e:
  if 'same-quote collision' not in str(e):raise
 else:raise ValueError('same-quote ambiguity was not refused')
 with tempfile.TemporaryDirectory(prefix='b2-fake-') as tmp:
  archive=model.Archive(str(Path(tmp)/'archive.sqlite'))
  def fake(provider,request):
   if provider!=cfg.provider or wire(request)!=wire(r['request']):raise ValueError('fake wire mismatch')
   return {'choices':[{'message':{'content':json.dumps(raw)}}],'usage':{}}
  answer=model.call(archive,cfg,r['setting'],r['system'],r['user'],r['schema'],'extraction','extract',transport=fake)
  if answer.data!=raw or answer.cached:raise ValueError('fake response mismatch')
  archive.conn.close()
 print('Fake B: exact wire, valid source/link, no-home, bad source, bad link and same-quote controls passed.',flush=True)
 return raw

def preview():
 cfg,uni,r,meta=build();fake_controls(cfg,uni,r)
 if OUT.exists():raise ValueError('output exists')
 OUT.mkdir(parents=True)
 manifest={'meta':meta,'item':r['item'],'shown':r['shown'],'b_request':r['request'],'b_wire_sha256':sha(wire(r['request'])),'a_saved_answer':{'questions':[]},'scope':'A pass plus one newly built B2 request. Source body is derived; no A-new or production acceptance.'}
 (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print('Pair preview, 68 questions; manifest SHA256',sha((OUT/'manifest.json').read_bytes()),flush=True)

def send(expected, provider_transport=None):
 cfg,uni,r,meta=build();m=OUT/'manifest.json';saved=json.loads(m.read_text())
 if sha(m.read_bytes())!=expected or canonical(saved['meta'])!=canonical(meta) or saved['item']!=r['item'] or saved['shown']!=r['shown'] or wire(saved['b_request'])!=wire(r['request']) or saved['b_wire_sha256']!=sha(wire(r['request'])):raise ValueError('pair or wire changed')
 archive=model.Archive(str(OUT/'b-archive.sqlite'))
 def transport(provider,actual):
  if provider!=cfg.provider or wire(actual)!=wire(r['request']):raise ValueError('actual wire mismatch')
  response=(provider_transport or model.openai_transport)(provider,actual);(OUT/'b-provider-response.json').write_text(json.dumps(response,ensure_ascii=False,indent=2)+'\n');return response
 try:
  answer=model.call(archive,cfg,r['setting'],r['system'],r['user'],r['schema'],'extraction','extract',transport=transport)
  result={'answer':answer.data,'input_tokens':answer.input_tokens,'output_tokens':answer.output_tokens,'cached':answer.cached}
  try:result['handover'],result['id_mapping']=check(answer.data,r,uni)
  except ValueError as e:result['refusal']=str(e)
  (OUT/'b-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
  print('B returned',len(answer.data.get('evidence',[])),'raw; retained',len(result.get('handover',{}).get('evidence',[])),'refusal',result.get('refusal','none'),flush=True)
 finally:archive.conn.close()
if __name__=='__main__':
 if len(sys.argv)==2 and sys.argv[1]=='preview':preview()
 elif len(sys.argv)==3 and sys.argv[1]=='send':send(sys.argv[2])
 else:raise SystemExit('preview | send manifest-sha256')
