"""Read the fixed pilot catalog before or after the catalog byte guard is removed."""
import hashlib,inspect,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'src'))
from hivemind import research_context,universe
LEDGER=ROOT.parent/'hivemind-no-preseed-evidence-review/poc/data/split-fresh-pilot-2026-11-05-v1/snapshot/views.sqlite'

def main():
 uni=universe.load(str(ROOT/'poc/universe.json'));options={'catalog_limit':100000000} if 'catalog_limit' in inspect.signature(research_context.Reader).parameters else {}
 start=time.perf_counter()
 with research_context.Reader(str(LEDGER),1206,['NVDA'],uni,**options) as reader:catalog=reader.catalog()
 elapsed=time.perf_counter()-start;encoded=json.dumps(catalog,ensure_ascii=False,separators=(',',':')).encode();canonical=json.dumps(catalog,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
 result={'ledger_sha256':hashlib.sha256(LEDGER.read_bytes()).hexdigest(),'before_sequence':1206,'questions':len(catalog['questions']),'bytes':len(encoded),'canonical_sha256':hashlib.sha256(canonical).hexdigest(),'elapsed_seconds':round(elapsed,5),'diagnostic_limit':options.get('catalog_limit')}
 print(json.dumps(result,indent=2));return result
if __name__=='__main__':
 result=main()
 if len(sys.argv)==2:Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
