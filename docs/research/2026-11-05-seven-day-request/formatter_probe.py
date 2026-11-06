"""One isolated record-preparation probe on a saved simple-A result; no writes to the research ledger."""
import copy,hashlib,json,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path[:0]=[str(HERE),str(ROOT/'src'),str(ROOT/'docs/research/2026-11-05-parallel-refinement')]
import formatter_bridge as bridge
from hivemind import config,extraction,model,testdb,universe
ID='gnews:69d682468e018e0065df5180'
OUT=ROOT/'poc/data/split-record-preparation-probe-2026-11-05-v2'

def sha(x):return hashlib.sha256(x).hexdigest()
def schema():
 original=extraction.schema_for('v74i')
 candidate=original['properties']['candidates']['items']; cp={k:copy.deepcopy(v) for k,v in candidate['properties'].items() if k in bridge.CANDIDATE_FIELDS}
 evidence=original['properties']['evidence']['items'];ep={k:copy.deepcopy(v) for k,v in evidence['properties'].items() if k in bridge.META_FIELDS}
 cp={'candidate_id':{'type':'string'},**cp};ep={'evidence_id':{'type':'string'},**ep}
 string={'type':'string'}
 obj=lambda props:{'type':'object','additionalProperties':False,'properties':props,'required':list(props)}
 note=obj({'basis':{'type':'string','enum':['source','analyst_check']},'reason':string,'source_span':string,'rung_reason':string})
 return obj({'status':{'type':'string','enum':['ready','cannot_format']},'reason':string,'candidate_fields':{'type':'array','items':obj(cp)},'evidence_fields':{'type':'array','items':obj(ep)},'date_notes':{'type':'array','items':note},'new_groups':copy.deepcopy(original['properties']['new_groups'])})

def build():
 cfg=config.load(str(ROOT/'poc/config/poc-v117.json'));uni=universe.load(str(ROOT/'poc/universe.json'))
 db=testdb.open_db(str(ROOT/'poc/data/parallel-thesis-evidence-input-2026-11-05/items.sqlite'))
 item=testdb.item_of(db.execute('select * from items where input_id=?',(ID,)).fetchone());db.close()
 source=ROOT/'poc/data/start-state-new-question-diagnostic-2026-11-05-v1/gnews_69d682468e018e0065df5180/result.json'
 raw=json.loads(source.read_text())['answer']
 role=(ROOT/'src/hivemind/prompts/role-v74i.txt').read_text();start=role.index('How to write a candidate thesis');end=role.index('\n',role.index('- Each numeric rung',start));rules=role[start:end]
 system=('Prepare the production record fields for the supplied pre-existing A answer. Do not discover, add, remove, combine, split, or rewrite its questions or its evidence. Return exactly one candidate_fields entry per question, and one evidence_fields entry per evidence item, using the supplied position IDs and order. The calling code preserves question, quotation and summary verbatim. Produce existing production fields using only the article, A answer, supplied context and the standard below. A third-party author opinion is a third_party_view and is not a company statement. An original speaker date not stated is empty. Each date_notes entry must distinguish an explicitly source-stated date from an analyst-selected check date, preserve its basis and explain the rung reference; use an exact source span only for source dates. A guessed source date is forbidden. If the requested due date, scope, ladder, attribution or any other required field cannot be supported without inventing facts or changing the research question, return status cannot_format with a reason and empty arrays. A valid schema is not proof of meaning.\n\n'+rules)
 note=uni.fiscal_note('NVDA',item['publication_day'],english=True).replace('; use that day as the due date.','.')
 positions=[];counter=0
 for i,q in enumerate(raw['questions'],1):
  ids=[]
  for _ in q['evidence']:counter+=1;ids.append(f'e{counter}')
  positions.append({'candidate_id':f'c{i}','evidence_ids':ids})
 user='[Article metadata] '+json.dumps({'id':ID,'publication_day':item['publication_day'],'title':item['title'],'publisher':item['publisher']},ensure_ascii=False)+'\n\n[Fiscal context; approximate publication month is not a day]\n'+note+'\n\n[Position IDs; match A questions and evidence in order]\n'+json.dumps(positions)+'\n\n[Exact A answer]\n'+json.dumps(raw,ensure_ascii=False,indent=2)+'\n\n[Source article]\n'+item['text']
 setting=cfg.extraction_setting(item['category']);request=model.build_request(setting,system,user,schema(),'record_preparation',cfg.provider)
 return cfg,item,raw,uni,setting,system,user,request

def preview():
 cfg,item,raw,uni,setting,system,user,request=build();fixed=schema()
 if len(raw['questions'])!=1 or len(raw['questions'][0]['evidence'])!=6:raise ValueError('stored case changed')
 for q in raw['questions']:
  for e in q['evidence']:
   if e['quote'] not in item['text']:raise ValueError('saved A quote changed')
 # An explicit refusal is allowed; invalid values must not satisfy the schema.
 refusal={'status':'cannot_format','reason':'insufficient information','candidate_fields':[],'evidence_fields':[],'date_notes':[],'new_groups':[]}
 if model.check_schema(refusal,fixed):raise ValueError('valid refusal rejected')
 bad=dict(refusal,status='invented')
 if not model.check_schema(bad,fixed):raise ValueError('invalid status accepted')
 with tempfile.TemporaryDirectory(prefix='format-fake-') as tmp:
  archive=model.Archive(str(Path(tmp)/'fake.sqlite'))
  def fake(provider,actual):
   if provider!=cfg.provider or json.dumps(actual)!=json.dumps(request):raise ValueError('wire mismatch')
   return {'choices':[{'message':{'content':json.dumps(refusal)}}],'usage':{}}
  answer=model.call(archive,cfg,setting,system,user,fixed,'record_preparation','record_preparation',transport=fake)
  if answer.data!=refusal or answer.cached:raise ValueError('fake response wrong')
  archive.conn.close()
 if OUT.exists():raise ValueError('probe directory exists')
 OUT.mkdir(parents=True)
 manifest={'source_id':ID,'a_answer_sha256':sha(json.dumps(raw,ensure_ascii=False,sort_keys=True).encode()),'body_sha256':sha(item['text'].encode()),'system_sha256':sha(system.encode()),'request_wire_sha256':sha(json.dumps(request).encode()),'request':request,'warning':'Formatter makes new record-shaping judgments. One stored result, no match/write, no acceptance.'}
 (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print('Offline refusal/schema/source/wire controls passed; manifest SHA256',sha((OUT/'manifest.json').read_bytes()),flush=True)

def send(expected):
 cfg,item,raw,uni,setting,system,user,request=build();m=OUT/'manifest.json'
 saved=json.loads(m.read_text())
 if sha(m.read_bytes())!=expected or json.dumps(saved['request']).encode()!=json.dumps(request).encode() or saved['request_wire_sha256']!=sha(json.dumps(request).encode()):raise ValueError('manifest or exact request order changed')
 archive=model.Archive(str(OUT/'archive.sqlite'))
 def transport(provider,actual):
  if provider!=cfg.provider or json.dumps(actual)!=json.dumps(request):raise ValueError('wire mismatch')
  response=model.openai_transport(provider,actual);(OUT/'provider-response.json').write_text(json.dumps(response,ensure_ascii=False,indent=2)+'\n');return response
 try:
  result=model.call(archive,cfg,setting,system,user,schema(),'record_preparation','record_preparation',transport=transport)
  formatted=result.data;report={'model_status':formatted['status'],'reason':formatted['reason'],'input_tokens':result.input_tokens,'output_tokens':result.output_tokens,'cached':result.cached,'prepared':formatted}
  if formatted['status']=='ready':
   try:
    value={k:formatted[k] for k in ('candidate_fields','evidence_fields','date_notes','new_groups')}
    report['bridge']=bridge.build(raw,item['text'],item,set(),uni,value)
   except bridge.BridgeRefusal as e:report['bridge_refusal']=str(e)
  (OUT/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
  print('Formatter:',report['model_status'],'bridge:',report.get('bridge',{}).get('status',report.get('bridge_refusal','not attempted')),flush=True)
 finally:archive.conn.close()
if __name__=='__main__':
 if len(sys.argv)==2 and sys.argv[1]=='preview':preview()
 elif len(sys.argv)==3 and sys.argv[1]=='send':send(sys.argv[2])
 else:raise SystemExit('preview | send manifest-sha256')
