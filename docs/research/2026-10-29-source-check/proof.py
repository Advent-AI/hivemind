import json,importlib.util,concurrent.futures,subprocess,sys,os,time
from pathlib import Path
p=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-source-check');q=p.parent/'2026-10-28-retention-audit/haiku-extraction-probe-2026-10-29.py';s=importlib.util.spec_from_file_location('provider',q);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def one(f):
 d=json.loads(f.read_text());start=time.monotonic();r=m.haiku_api('https://api.anthropic.com/v1/messages',d);out={'response':r,'seconds':time.monotonic()-start};(p/f.name.replace('-request','-answer')).write_text(json.dumps(out,ensure_ascii=False,indent=2));print(f.name,r.get('stop_reason'),flush=True)
if len(sys.argv)>1:
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:list(ex.map(one,sorted(p.glob('proof-*-request.json'))))
else:
 rows=[]
 for f in sorted(p.glob('proof-*-request.json')):
  d=json.loads(f.read_text());d.pop('max_tokens');n=m.haiku_api('https://api.anthropic.com/v1/messages/count_tokens',d)['input_tokens'];b=max(2*n+16384,len(m.previous.wire(json.loads(f.read_text()))));rows.append({'request':f.name,'input_tokens':n,'bound':b,'reserved_usd':(b*.1+6064*.5)/1e6})
 assert sum(r['reserved_usd'] for r in rows)<.02
 (p/'proof-budget.json').write_text(json.dumps(rows,indent=2))
 with (p/'proof.log').open('x') as log:r=subprocess.Popen([sys.executable,__file__,'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 (p/'proof.pid').write_text(str(r.pid));print(r.pid,rows)
