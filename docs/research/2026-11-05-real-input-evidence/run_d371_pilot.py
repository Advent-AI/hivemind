"""Frozen four-source D371 diagnostic; uses production request builder and filing."""
import copy, hashlib, json, sqlite3, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, extraction, model, testdb, universe
from hivemind.views import store

RUN = ROOT / 'poc/data/v117-one-day-smoke-2026-11-05'
VIEWS = ROOT / 'poc/data/pilot-d369-existing-library-v2/views.sqlite'
CONFIG = ROOT / 'poc/config/poc-v117.json'
UNI = ROOT / 'poc/universe.json'
ROLE = HERE / 'role-d371-pilot.txt'
DESIGN = HERE / 'd371-approved-pilot.md'
MANIFEST = HERE / 'd371-pilot-frozen.json'
PREFLIGHT = HERE / 'd371-one-day-preflight.txt'
IDS = [('gnews:d144b91986c520ea36e718cf',116,'117cae5377ed5e903e16682eb82c2d08afd786c50693beafaa5d55490822498e'),('gnews:8f8a2d115ab834c7026aefd1',99,'767ab434772478e66b53541952f49a2abd7473bde67990eaa53ad39ae64d173d'),('gnews:6dcaad557a1b21d7b867fe34',11,'497768d4b5be85f8e6bf926c751af1a3e2316ca808c78830fd9c4cbb32bd541e'),('gnews:71114e6d410b3ece8ed7f321',15,'787bd24d41c40a7ef6ba2e7a6a0da7d607084b3648ee013447ab299ac85dd35d')]
ADDITION = 'Financial information, guidance, forecasts and estimates can be evidence for a related question, regardless of their time period, including a question proposed in the same answer.'
ANCHOR = "- A number, a financial line, a target or a named customer project does not by itself open a thesis; a customer's purchase or rollout plan is evidence to the supplier's demand and product theses unless it changes the supplier's own cash or credit risk."
def sha(b): return hashlib.sha256(b).hexdigest()
def wire(request): return sha(json.dumps(request).encode())
def build():
    cfg=config.load(CONFIG); uni=universe.load(UNI)
    items=sqlite3.connect(str(RUN/'items.sqlite'));items.row_factory=sqlite3.Row
    archive=sqlite3.connect(str(RUN/'archive.sqlite'));archive.row_factory=sqlite3.Row
    views=store.open_db(str(VIEWS)); requests=[]
    for ident,call_id,expected in IDS:
        item=testdb.item_of(items.execute('select * from items where input_id=?',(ident,)).fetchone())
        shown=extraction.shown_views(views,cfg,item,[o['value'] for o in item['object_identifiers'] if uni.has(o['value'])])
        setting,system,user,schema=extraction.request_for(cfg,item,item['text'],shown,uni)
        if system.count(ANCHOR)!=1 or ROLE.read_text()!=system.replace(ANCHOR,ANCHOR+' '+ADDITION,1):raise ValueError('role mismatch')
        archived=archive.execute('select * from model_calls where call_id=?',(call_id,)).fetchone()
        for arm,role in [('control',system),('candidate',ROLE.read_text())]:
            request=model.build_request(setting,role,user,schema,'extraction',cfg.provider)
            identity=model.request_identity(request)[1]
            if arm=='control' and (identity!=expected or archived['request_sha256']!=identity):raise ValueError('stored request mismatch')
            if arm=='candidate':
                reconstructed=copy.deepcopy(request);reconstructed['messages'][0]['content']=system
                if json.dumps(reconstructed)!=json.dumps(control):raise ValueError('unexpected request difference')
            else:control=request
            requests.append(dict(item=item,shown=shown,setting=setting,system=role,user=user,schema=schema,identity=identity,wire=wire(request),arm=arm,call_id=call_id,old=json.loads(archived['answer_json'])))
    items.close(); archive.close(); views.close()
    return cfg,uni,requests

def frozen(reqs):
    files=[Path(__file__),ROLE,DESIGN,CONFIG,UNI,PREFLIGHT,RUN/'items.sqlite',RUN/'archive.sqlite',VIEWS,ROOT/'src/hivemind/prompts/role-v74i.txt']
    files+=sorted((ROOT/'src/hivemind').rglob('*.py'))
    return {'files':{str(p):sha(p.read_bytes()) for p in files},'requests':[{'input_id':r['item']['input_id'],'arm':r['arm'],'identity':r['identity'],'wire_sha256':r['wire'],'body_sha256':sha(r['item']['text'].encode()),'shown':len(r['shown'])} for r in reqs]}

def file_answer(data,r,uni,answer):
    e,c,d,g=extraction.sift_with_groups(copy.deepcopy(data),r['item'],r['item']['text'],{v['view_id'] for v in r['shown']},uni)
    return extraction.file_reading(extraction.Reading(e,c,d,g,answer,'v74i'),r['item'],r['shown'])

def counterfactual(reqs,uni):
    r=reqs[0];data=copy.deepcopy(r['old']); target=next(e for e in data['evidence'] if e['id']=='e11');target['links']=['c1']
    errors=model.check_schema(data,r['schema']);
    if errors: raise ValueError('archived positive schema: '+str(errors))
    dummy=type('Answer',(),dict(call_id=0,request_sha256='fake',cached=False,cost_usd=0))()
    h=file_answer(data,r,uni,dummy)
    if not any(e['id']=='e11' and 'c1' in e['links'] for e in h.evidence):raise ValueError('positive e11 failed')
    target['quote']='This fabricated quote must not occur anywhere in the source article.'
    h=file_answer(data,r,uni,dummy)
    if any(e['id']=='e11' for e in h.evidence) or not any(x[0]=='e11' and x[1]=='quote not in item' for x in h.dropped):raise ValueError('invalid quote negative not refused')

def main():
    if len(sys.argv)<2 or sys.argv[1] not in ('--freeze','--fake','--send'):raise SystemExit('usage --freeze | --fake output | --send output')
    mode=sys.argv[1];cfg,uni,reqs=build()
    if mode=='--freeze':
        if MANIFEST.exists():raise SystemExit('manifest exists')
        MANIFEST.write_text(json.dumps(frozen(reqs),ensure_ascii=False,indent=2)+'\n');print('manifest',sha(MANIFEST.read_bytes()));return
    if len(sys.argv)!=3:raise SystemExit('output directory required')
    out=Path(sys.argv[2]);
    if not out.is_absolute() or out.exists():raise SystemExit('new absolute output required')
    if json.loads(MANIFEST.read_text())!=frozen(reqs):raise SystemExit('frozen manifest mismatch')
    if mode=='--send':
        fake=HERE/'d371-fake-result.json'
        if not fake.exists() or json.loads(fake.read_text())!={'manifest_sha256':sha(MANIFEST.read_bytes()),'cases':8,'positive':1,'negative':1,'status':'ok'}:raise SystemExit('fake preflight missing')
    counterfactual(reqs,uni)
    out.mkdir(parents=True)
    for i,r in enumerate(reqs):
        directory=out/f'{i:02d}-{r["arm"]}';directory.mkdir();received=[]
        archive=model.Archive(str(directory/'archive.sqlite'))
        def transport(provider,request):
            if wire(request)!=r['wire']:raise ValueError('actual request wire mismatch')
            if mode=='--fake':
                quote=r['old']['evidence'][0]['quote'];fact={'id':'e1','quote':quote,'one_line':'A source-backed statement.','speaker':'Source','original_who':'','original_day':'','tier':'fact','event_time':'','links':[r['shown'][0]['view_id']]}
                return {'choices':[{'message':{'content':json.dumps({'evidence':[fact],'candidates':[],'new_groups':[]})}}], 'usage':{'prompt_tokens':0,'completion_tokens':0}}
            response=model.openai_transport(provider,request);received.append(response)
            (directory/'response.json').write_text(json.dumps(response,ensure_ascii=False)+'\n');return response
        try:
            ans=model.call(archive,cfg,r['setting'],r['system'],r['user'],r['schema'],'extraction','extract',transport=transport)
            if ans.cached or ans.request_sha256!=r['identity']:raise ValueError('cache or identity mismatch')
            h=file_answer(ans.data,r,uni,ans)
            if mode=='--fake' and len(h.evidence)!=1:raise ValueError('fake source link failed')
            result={'status':'ok','input_id':r['item']['input_id'],'arm':r['arm'],'answer':ans.data,'handover':{'evidence':h.evidence,'candidates':h.candidates,'dropped':h.dropped,'new_groups':h.new_groups},'input_tokens':ans.input_tokens,'output_tokens':ans.output_tokens,'cost_usd':ans.cost_usd,'earlier_retry_cost':'unknown'}
        except Exception as error:
            result={'status':'failed_or_unknown','input_id':r['item']['input_id'],'arm':r['arm'],'error':repr(error),'usage':received[0].get('usage') if received else None}
        finally:archive.conn.close()
        (directory/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'index':i,'arm':r['arm'],'id':r['item']['input_id'],'status':result['status']}),flush=True)
        if result['status']!='ok':raise SystemExit('stopped after failure')
    if mode=='--fake':(HERE/'d371-fake-result.json').write_text(json.dumps({'manifest_sha256':sha(MANIFEST.read_bytes()),'cases':8,'positive':1,'negative':1,'status':'ok'})+'\n')
    (out/'complete.json').write_text(json.dumps({'status':'ok','cases':len(reqs)})+'\n')
if __name__=='__main__':main()
