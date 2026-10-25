"""D155: read-only whole-archive census. --source selects current code or the preserved baseline; no model calls."""
from pathlib import Path
import argparse,collections,json,re,sqlite3,sys
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--proposal',action='store_true');a=p.parse_args()
root=Path(__file__).resolve().parents[1];src=Path(a.source);sys.path.insert(0,str(src/'src'))
from hivemind import extraction,universe
u=universe.load(src/'poc/universe.json')
if a.proposal:
 original_fiscal=u.fiscal_period
 u.watch_allows=lambda *args: True
 def fiscal(obj,year):
  if re.fullmatch(r'(?:FY\s*)?\d{4}(?:年|财年)?',year or '',re.I):return original_fiscal(obj,year)
  return None
 def scope(obj,measure,value='',event='n/a'):
  if not value:return '', 'none'
  exact=[e for e in u.watch_list(obj) if e.get('scope') and e.get('measure')==measure and universe.scope_key(e['scope'])==universe.scope_key(value) and (not e.get('event_type') or e['event_type']==event)]
  return (exact[0]['scope'],'watch') if len(exact)==1 else (value,'model')
 u.fiscal_period=fiscal;u.scope_and_source=scope
def scope_matches(entry, scope):
 # Reproduce the retired substring rule only to count the historical failure class.
 key=universe.scope_key(scope)
 return bool(key) and (universe.scope_key(entry['scope'])==key or any(universe.scope_key(alias) and universe.scope_key(alias) in key for alias in entry.get('aliases', [])))
def db(path):
 c=sqlite3.connect(f'file:{path}?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
arc=db(root/'poc/data/keyed-2026-10-25/archive-T2.sqlite');items=db(root/'poc/data/items-window-tags2-2026-10-24.sqlite')
records=[];reasons=collections.Counter();counts=collections.Counter();multi=[]
for row in arc.execute("select * from model_calls where purpose='extract' and request_sha256 not like '%:%' order by call_id"):
 req=json.loads(row['request_json']);user=req['messages'][1]['content'];found=re.search(r'【信息】编号 (\S+?)，类别 ',user)
 if not found:raise ValueError(f'unidentified {row["call_id"]}')
 item=items.execute('select * from items where input_id=?',(found[1],)).fetchone()
 if item is None:raise ValueError(found[1])
 data=json.loads(row['answer_json']);shown=set(re.findall(r'^\s+- (v\d+)（',user,re.M));ev,cs,drops=extraction.sift(data,dict(item),item['text'],shown,u)
 counts.update(answers=1,raw_candidates=len(data['candidates']),kept_candidates=len(cs),raw_evidence=len(data['evidence']),kept_evidence=len(ev))
 for ident,reason in drops: reasons[reason.split(':')[0]]+=1
 for c in data['candidates']:
  hits=[e.get('scope') for e in u.watch_list(u.resolve(c['object']) or c['object']) if e.get('scope') and e['measure']==c.get('measure') and scope_matches(e,c.get('scope',''))]
  if len(set(hits))>1:multi.append({'call':row['call_id'],'candidate':c['id'],'scopes':hits})
 records.append({'call':row['call_id'],'input_id':found[1],'raw':data['candidates'],'kept':cs,'drops':drops})
ledgers=[]
for path in sorted((root/'poc/data').glob('views-2026-10-25-v15-*.sqlite')):
 c=db(path);parallel=list(c.execute("select * from processing_steps where step='extracted' and reason like '%(parallel)'"));stale=[]
 for r in parallel:
  earlier=c.execute('select count(*) from views v join processing_steps p on p.input_id=v.created_from_input and p.step=\'written\' and p.result=\'ok\' where p.publication_day=? and v.created_seq<?',(r['publication_day'],r['sequence_no'])).fetchone()[0]
  if earlier:stale.append({'input_id':r['input_id'],'seq':r['sequence_no'],'earlier_views':earlier})
 ledgers.append({'name':path.name,'views':c.execute('select count(*) from views').fetchone()[0],'parallel_extractions':len(parallel),'parallel_after_same_day_new_views':len(stale),'outside_watch':c.execute("select count(*) from review_pool_entries where kind='candidate_outside_watch'").fetchone()[0]})
assert {261,584}.issubset({r['call'] for r in records})
result={'counts':dict(counts),'drop_reasons':dict(reasons),'multi_scope_aliases':multi,'ledgers':ledgers,'records':records}
assert not Path(a.out).exists(), 'Use a new output path'
Path(a.out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='records'},ensure_ascii=False,indent=2))
