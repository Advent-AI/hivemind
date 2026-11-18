import hashlib,importlib.util,json,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('probe_sender',H/'probe_send.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
reg={name:hashlib.sha256((H/name).read_bytes()).hexdigest() for name in m.REQUIRED};m.verify_registration(reg)
for mode in ['empty','missing','changed']:
 r=dict(reg)
 if mode=='empty':r={}
 if mode=='missing':r.pop(next(iter(r)))
 if mode=='changed':r[next(iter(r))]='0'*64
 try:m.verify_registration(r)
 except ValueError:print('registration control caught:',mode)
 else:raise AssertionError(mode)
manifest=json.loads((H/'probe-manifest.json').read_text());attempts=[];original_urlopen=m.urllib.request.urlopen;original_key=m.jev._key
try:
 m.jev._key=lambda:'fake-key'
 def lost(req,timeout):attempts.append(req);raise OSError('lost reply after dispatch')
 m.urllib.request.urlopen=lost
 with tempfile.TemporaryDirectory() as tmp:
  dest=Path(tmp)/'probe';rc=m.execute(manifest[:1],dest,reg,m.single_attempt)
  if rc!=1 or len(attempts)!=1:raise AssertionError('failure did not stop after one attempt')
  events=[json.loads(x) for x in (dest/'events.jsonl').read_text().splitlines()]
  if [x['status'] for x in events]!=['dispatching','failed_or_ambiguous']:raise AssertionError('bad ambiguity journal')
  try:m.execute(manifest[:1],dest,reg,m.single_attempt)
  except FileExistsError:pass
  else:raise AssertionError('restart allowed')
  if len(attempts)!=1:raise AssertionError('restart sent an extra call')
  print('integration: lost response produced one attempt, ambiguous event, stop and restart refusal')
finally:
 m.urllib.request.urlopen=original_urlopen;m.jev._key=original_key
