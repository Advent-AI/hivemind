"""Size all individually selectable questions on the saved 2026-08-29 pilot ledger."""
import hashlib,inspect,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'src'))
from hivemind import research_context,universe

LEDGER=ROOT.parent/'hivemind-no-preseed-evidence-review/poc/data/split-fresh-pilot-2026-11-05-v1/snapshot/views.sqlite'

def size(value):return len(json.dumps(value,ensure_ascii=False,separators=(',',':')).encode())
def fingerprint(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 uni=universe.load(str(ROOT/'poc/universe.json'));start=time.perf_counter()
 options={'evidence_limit':100000000} if 'evidence_limit' in inspect.signature(research_context.Reader).parameters else {}
 with research_context.Reader(str(LEDGER),1206,['NVDA'],uni,**options) as reader:
  catalog=reader.catalog();rows=[]
  for q in catalog['questions']:
   result=reader.expand([q['view_id']]);rows.append({'view_id':q['view_id'],'bytes':size(result),'evidence':len(result['evidence']),'content_sha256':fingerprint(result)})
  selected=reader.expand(['v10','v2','v6','v70']);whole=reader.expand([q['view_id'] for q in catalog['questions']])
 result={'ledger_sha256':hashlib.sha256(LEDGER.read_bytes()).hexdigest(),'before_sequence':1206,'scope':['NVDA','all configured themes'],'open_questions':len(rows),'individuals_over_1000000_bytes':[x for x in rows if x['bytes']>1000000],'pilot_selection':{'questions':['v10','v2','v6','v70'],'bytes':size(selected),'evidence':len(selected['evidence']),'content_sha256':fingerprint(selected)},'whole_catalog':{'bytes':size(whole),'unique_evidence':len(whole['evidence']),'content_sha256':fingerprint(whole)},'individuals':rows,'elapsed_seconds':round(time.perf_counter()-start,4),'diagnostic_limit':options.get('evidence_limit'),'note':'Read-only census against a fixed finished pilot snapshot. A non-null diagnostic limit describes the pre-change measurement only.'}
 out=Path(__file__).with_name('census.json');out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='individuals'},indent=2))
if __name__=='__main__':main()
