"""Isolated Jev probe; offline checks by default, live only with --send."""
import hashlib,importlib.util,json,random,sys,tempfile,os,urllib.request,subprocess
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent; ROOT=Path('/Users/lchingen/hivemind');sys.path.insert(0,str(ROOT/'src'))
spec=importlib.util.spec_from_file_location('prepare',HERE/'probe_prepare.py');prep=importlib.util.module_from_spec(spec);spec.loader.exec_module(prep)
from hivemind import jev,model
REQUIRED=['EXPERIMENT-DESIGN.md','probe_prepare.py','probe_send.py','independent_check.py','integration_check.py','inspect_saved.py','probe-manifest.json','../../clean-arch/step2/compare.py','../../clean-arch/step2/run_forward.py','../../clean-arch/step3/library.py','../../src/hivemind/jev.py','../../src/hivemind/model.py','../../poc/data/clean-acceptance-2026-11-09/step1/trace.sqlite','../../poc/data/clean-acceptance-2026-11-09/step2/decisions.json','../../poc/data/clean-acceptance-2026-11-09/step2/embeddings.json','../../poc/data/clean-acceptance-2026-11-09/step2/jev.sqlite']
CONFIG=SimpleNamespace(version='clean-step2-score-probe',checksum='experimental');SETTING=prep.run.SETTING

def ask(archive,req,transport=None):
 return jev.ask(archive,CONFIG,SETTING,req['state'],req['questions'],'clean_step2_score_probe',transport=transport)

def single_attempt(req):
 body=json.dumps(req,sort_keys=True,ensure_ascii=False).encode('utf-8')
 key=jev._key()
 request=urllib.request.Request(jev.ENDPOINT,body,{'Authorization':'Bearer '+key,'Content-Type':'application/json','Accept':'application/json'})
 with urllib.request.urlopen(request,timeout=60) as response: raw=response.read()
 if key.encode('utf-8') in raw:raise RuntimeError('credential echoed')
 return json.loads(raw.decode('utf-8'))

def fake_checks(manifest):
 example=manifest[0];calls=[]
 def fake(req):calls.append(req);return {'answers':example['old_answers'],'usage':{'input_tokens':10,'output_tokens':0}}
 with tempfile.TemporaryDirectory() as directory:
  for n in range(3):
   ar=model.Archive(str(Path(directory)/f'{n}.sqlite')); answer=ask(ar,example['control'],fake)
   if answer.cached:raise AssertionError('unexpected cache hit')
   ar.conn.close()
  if len(calls)!=3:raise AssertionError('not three independent fake calls')
  interrupted=Path(directory)/'interrupted'; interrupted.mkdir()
  try:interrupted.mkdir(exist_ok=False)
  except FileExistsError:pass
  else:raise AssertionError('unsafe restart after interrupted dispatch')
  ar=model.Archive(str(Path(directory)/'lost.sqlite'));lost=[]
  def lost_reply(req):lost.append(req);raise OSError('simulated lost reply')
  try:ask(ar,example['control'],lost_reply)
  except OSError:pass
  else:raise AssertionError('lost reply accepted')
  if len(lost)!=1:raise AssertionError('lost reply retried')
  ar.conn.close()
  ar=model.Archive(str(Path(directory)/'bad.sqlite'))
  try:ask(ar,example['control'],lambda req:{'answers':{},'usage':{}})
  except model.SchemaError:pass
  else:raise AssertionError('malformed answer accepted')
  ar.conn.close()
 print('fake transport: 3 separate cache misses, malformed answer refused, lost reply attempted once, interrupted run refuses restart')

def verify_registration(registration):
 if set(registration)!=set(REQUIRED):raise ValueError('registration population mismatch')
 for name,expected in registration.items():
  if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=expected:raise ValueError('registration hash changed: '+name)

def execute(manifest,dest,registration,transport):
 dest.mkdir(exist_ok=False); (dest/'registration.json').write_text(json.dumps(registration,indent=2)+'\n'); order=[]
 for item in manifest:
  plan=[(arm,draw) for arm in ('control','treatment') for draw in range(3)];random.Random(42031+len(order)).shuffle(plan);order += [(item['id'],arm,draw) for arm,draw in plan]
 (dest/'plan.json').write_text(json.dumps(order,indent=2)+'\n'); data={x['id']:x for x in manifest}; archives={(arm,n):model.Archive(str(dest/f'{arm}-{n}.sqlite')) for arm in ('control','treatment') for n in range(3)}
 with (dest/'events.jsonl').open('x',buffering=1) as out:
  for i,(key,arm,draw) in enumerate(order):
   req=data[key][arm];event={'id':key,'arm':arm,'draw':draw,'sequence':i,'request_sha256':prep.digest(req)}
   out.write(json.dumps({**event,'status':'dispatching'})+'\n');out.flush();os.fsync(out.fileno())
   try:
    res=ask(archives[arm,draw],req,transport)
    if res.cached:raise RuntimeError('unexpected cached result')
    out.write(json.dumps({**event,'status':'complete','answers':res.data,'input_tokens':res.input_tokens,'cost_usd':res.cost_usd})+'\n');out.flush();os.fsync(out.fileno())
   except Exception as e:
    out.write(json.dumps({**event,'status':'failed_or_ambiguous','error':type(e).__name__})+'\n');print('Stopped on incomplete request',i,key,arm,draw,type(e).__name__,flush=True);return 1
   print(f'{i+1}/{len(order)} {key} {arm} draw {draw+1}',flush=True)
 (dest/'complete').write_text('complete\n')
 for a in archives.values():a.conn.close()
 return 0

def main():
 manifest=json.loads((HERE/'probe-manifest.json').read_text());prep.check(manifest,prep.build());fake_checks(manifest)
 if sys.argv[1:]!=['--send']:
  if sys.argv[1:]:raise SystemExit('usage: probe_send.py [--send]')
  return
 registration=json.loads((HERE/'registration.json').read_text());verify_registration(registration)
 subprocess.run([sys.executable,str(HERE/'inspect_saved.py')],check=True,stdout=subprocess.DEVNULL)
 subprocess.run([sys.executable,str(HERE/'independent_check.py')],check=True)
 subprocess.run([sys.executable,str(HERE/'integration_check.py')],check=True)
 verify_registration(registration)
 return execute(manifest,HERE/'live-probe',registration,single_attempt)
if __name__=='__main__':raise SystemExit(main() or 0)
