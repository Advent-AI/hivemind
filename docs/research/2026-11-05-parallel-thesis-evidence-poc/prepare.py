"""Prepare the three frozen requests for an isolated parallel extraction diagnostic."""
import copy, hashlib, json, sqlite3, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'src'))
from hivemind import config, extraction, model, testdb, universe
from hivemind.views import store
INPUT=ROOT/'poc/data/parallel-thesis-evidence-input-2026-11-05'
ARTICLES=[('gnews:d144b91986c520ea36e718cf',1229),('gnews:8f8a2d115ab834c7026aefd1',1224),('gnews:69d682468e018e0065df5180',1211),('gnews:6dcaad557a1b21d7b867fe34',1215)]
def sha(b):return hashlib.sha256(b).hexdigest()
def ro(path):
 c=sqlite3.connect(path.resolve().as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
def snapshot(conn,seq):
 out=[]
 rows=conn.execute('select view_id,object_id,object_kind,kind,looks_at,question,due_day,year,created_seq from views where created_seq < ? order by created_seq, rowid',(seq,)).fetchall()
 for v in rows:
  switch=conn.execute('select open from view_switches where view_id=? and after_seq < ? order by id desc limit 1',(v['view_id'],seq)).fetchone()
  if not switch or not switch['open']:continue
  key=store.view_key(conn,v['view_id'])
  if not key or key['seq']>=seq:raise ValueError('missing or future key '+v['view_id'])
  groups=[{'name':g['name'],'scope':g['scope'],'aliases':g.get('aliases') or []} for g in store.groups_of_view_at(conn,v['view_id'],seq-1)]
  out.append(dict(v,snapshot_seq=seq-1,key=key,groups=groups,parents=store.direct_parents(conn,v['view_id'],seq-1)))
 return out
def prepare():
 cfg=config.load(ROOT/'poc/config/poc-v117.json');uni=universe.load(ROOT/'poc/universe.json');items=ro(INPUT/'items.sqlite');views=ro(INPUT/'views.sqlite');out=[]
 for ident,seq in ARTICLES:
  row=items.execute('select * from items where input_id=?',(ident,)).fetchone()
  if not row:raise ValueError('missing '+ident)
  item=testdb.item_of(row)
  if ident==ARTICLES[0][0]:
   item['object_identifiers']=item['object_identifiers']+[{'kind':'ticker','value':'MSFT','why':'POC correction: article directly concerns Microsoft'}]
  assert item['text'] and len(item['text'])<=extraction.MAX_TEXT_CHARS
  shown=snapshot(views,seq)
  setting,original,user,base=extraction.request_for(cfg,item,item['text'],shown,uni)
  original=original.replace("at the start of the item's day","immediately before the item",1)
  old=f'[Open questions at the start of {item["publication_day"]}]';new='[Open questions immediately before this item]'
  assert user.count(old)==1 and user.count(extraction.CLOSING)==1 and user.count(extraction.GROUPS_INSTRUCTION)==1
  user=user.replace(old,new,1)
  group_text="[Research groups] No separate group list is supplied. For a candidate that tracks an ongoing matter (a product rollout, a deal, a policy process, an investment or demand cycle), declare the group in new_groups (local ids n1, n2 …) and cite it in group_refs; leave group_refs empty for a company's own financial lines."
  user=user.replace(extraction.GROUPS_INSTRUCTION,group_text,1)
  for arm in ('control','new','existing'):
   schema=copy.deepcopy(base);u=user;s=original
   if arm=='new':
    s=(HERE/'new-thesis.txt').read_text()
    schema['properties']['evidence']['items']['properties']['links']['description']='IDs of this answer’s candidate questions that this evidence can inform, whether supporting or opposing; never an existing question ID.'
    u=u.replace(extraction.CLOSING,'Return candidates, their article evidence, and any new groups per the schema. Evidence links contain only candidate IDs from this answer; each candidate evidence_ids names its own evidence.',1)
   if arm=='existing':
    s=(HERE/'existing-evidence.txt').read_text()
    schema['properties']['evidence']['items']['properties']['links']['description']='IDs of supplied existing questions this evidence can inform; never a candidate ID.'
    schema['properties']={'evidence':schema['properties']['evidence']};schema['required']=['evidence']
    u=u.replace(group_text,'[Research groups] Use the supplied question descriptions to understand their scope.',1)
    start=u.find('[Research reference]');end=u.find('[Open questions immediately before this item]')
    if start!=-1:
     assert end>start
     u=u[:start]+u[end:]
    u=u.replace('For a candidate thesis about a company, object is its ticker; about a theme, choose an id from this list, or state what the matter is when none fits:', 'Theme identifiers:',1)
    u=u.replace(extraction.CLOSING,'Return only evidence per the schema. Each evidence link must be an ID of a supplied existing question.',1)
   request=model.build_request(setting,s,u,schema,'extraction',cfg.provider)
   out.append(dict(item=item,shown=shown,setting=setting,system=s,user=u,schema=schema,request=request,arm=arm,seq=seq))
 items.close();views.close();return cfg,uni,out
if __name__=='__main__':
 cfg,uni,records=prepare();out=HERE/'frozen-requests.json'
 if out.exists():raise SystemExit('refusing overwrite')
 data=[]
 for r in records:
  wire=json.dumps(r['request']).encode()
  data.append({'id':r['item']['input_id'],'seq':r['seq'],'arm':r['arm'],'snapshot':r['shown'],'snapshot_sha256':sha(json.dumps(r['shown'],sort_keys=True).encode()),'body_sha256':sha(r['item']['text'].encode()),'request_sha256':sha(wire),'request':r['request']})
 out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');print('Prepared',len(data),'requests; sha256',sha(out.read_bytes()))
 for r in data:print(r['arm'],r['id'],r['seq'],len(r['snapshot']),r['request_sha256'])
