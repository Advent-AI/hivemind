"""Build and inspect exact paired requests for the approved extraction diagnostic."""
import copy, hashlib, importlib.util, json, sqlite3
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('previous_pilot',HERE/'run_d371_pilot.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
from hivemind import extraction,config,universe,testdb,model
from hivemind.views import store
old.RUN=ROOT/'poc/data/restructure-input-snapshot-2026-11-05'
old.VIEWS=old.RUN/'views.sqlite'
ROLE=HERE/'role-restructure-draft.txt';GROUPS=HERE/'groups-restructure-draft.txt';CATEGORIES=HERE/'categories-restructure-draft.json'
EXTRA=('gnews:69d682468e018e0065df5180',18,'1a0627e3738a6110ea4b09abdecb0cbfb6fda2983e870c9771235254776275fd','5034f037d1594df1bf0354b60cc5c181bdc29175288ef950966992d36a4f5062')
def digest(data):return hashlib.sha256(data).hexdigest()
def build():
 cfg=config.load(old.CONFIG);uni=universe.load(old.UNI);records=[]
 items=sqlite3.connect((old.RUN/'items.sqlite').resolve().as_uri()+'?mode=ro',uri=True);items.row_factory=sqlite3.Row
 archive=sqlite3.connect((old.RUN/'archive.sqlite').resolve().as_uri()+'?mode=ro',uri=True);archive.row_factory=sqlite3.Row
 views=sqlite3.connect(old.VIEWS.resolve().as_uri()+'?mode=ro',uri=True);views.row_factory=sqlite3.Row
 for id,call,identity in old.IDS+[(EXTRA[0],EXTRA[1],EXTRA[2])]:
  row=items.execute('select * from items where input_id=?',(id,)).fetchone()
  if not row:raise ValueError('missing item')
  item=testdb.item_of(row)
  if id==EXTRA[0] and digest(item['text'].encode())!=EXTRA[3]:raise ValueError('extra body mismatch')
  shown=extraction.shown_views(views,cfg,item,[o['value'] for o in item['object_identifiers'] if uni.has(o['value'])])
  setting,system,user,schema=extraction.request_for(cfg,item,item['text'],shown,uni);request=model.build_request(setting,system,user,schema,'extraction',cfg.provider)
  archived=archive.execute('select * from model_calls where call_id=?',(call,)).fetchone()
  if model.request_identity(request)[1]!=identity or not archived or archived['request_sha256']!=identity:raise ValueError('identity mismatch')
  records.append(dict(item=item,shown=shown,setting=setting,system=system,user=user,schema=schema,identity=identity,wire=old.wire(request),arm='control',call_id=call,old=json.loads(archived['answer_json'])))
 views.close();items.close();archive.close()
 normal_cats=json.loads(Path(config.prompt_path('categories-v74i.json')).read_text());draft_cats=json.loads(CATEGORIES.read_text())
 if {k:v for k,v in normal_cats.items() if k!='T5'}!={k:v for k,v in draft_cats.items() if k!='T5'}:raise ValueError('unexpected category change')
 if normal_cats['T5']['read']!=draft_cats['T5']['read']:raise ValueError('unexpected T5 read change')
 groups=GROUPS.read_text().strip();result=[]
 for orig in records:
  if orig['user'].count(extraction.GROUPS_INSTRUCTION)!=1:raise ValueError('group block count')
  for arm in ('control','candidate'):
   r=copy.deepcopy(orig);r['arm']=arm
   if arm=='candidate':
    r['system']=ROLE.read_text();r['user']=r['user'].replace(extraction.GROUPS_INSTRUCTION,groups,1)
    if r['item']['category']=='T5':
     source=normal_cats['T5']['what'];target=draft_cats['T5']['what']
     if r['user'].count(source)!=1:raise ValueError('T5 old block count')
     r['user']=r['user'].replace(source,target,1)
   request=model.build_request(r['setting'],r['system'],r['user'],r['schema'],'extraction',cfg.provider)
   r['identity']=model.request_identity(request)[1];r['wire']=old.wire(request)
   if arm=='control':
    if r['identity']!=orig['identity'] or r['wire']!=orig['wire']:raise ValueError('control request changed')
    control=request
   else:
    x=copy.deepcopy(request);x['messages'][0]['content']=orig['system'];x['messages'][1]['content']=x['messages'][1]['content'].replace(groups,extraction.GROUPS_INSTRUCTION,1)
    if r['item']['category']=='T5':x['messages'][1]['content']=x['messages'][1]['content'].replace(draft_cats['T5']['what'],normal_cats['T5']['what'],1)
    if json.dumps(x)!=json.dumps(control):raise ValueError('unplanned treatment difference')
   result.append(r)
 return cfg,uni,result
if __name__=='__main__':
 _,_,reqs=build()
 for r in reqs:
  print(json.dumps({'input_id':r['item']['input_id'],'arm':r['arm'],'original_call_id':r['call_id'],'request_identity':r['identity'],'wire_sha256':r['wire'],'body_sha256':digest(r['item']['text'].encode()),'shown_count':len(r['shown']),'system_chars':len(r['system']),'user_chars':len(r['user'])}))
