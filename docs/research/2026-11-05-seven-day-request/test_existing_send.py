"""Exercise the exact saved A-pass/B send path with an injected fake provider."""
import copy,json,shutil,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path[:0]=[str(HERE),str(ROOT/'src')]
import existing_path as path

def main():
 cfg,uni,r,_=path.build();raw=path.fake_controls(cfg,uni,r)
 original=path.OUT;manifest=original/'manifest.json';expected=path.sha(manifest.read_bytes());calls=[]
 def fake(provider,request):
  if provider!=cfg.provider or path.wire(request)!=path.wire(r['request']):raise AssertionError('wire changed')
  calls.append(1);return {'choices':[{'message':{'content':json.dumps(raw)}}],'usage':{}}
 try:
  with tempfile.TemporaryDirectory(prefix='saved-b-send-') as tmp:
   path.OUT=Path(tmp);shutil.copyfile(manifest,path.OUT/'manifest.json')
   path.send(expected,provider_transport=fake)
   result=json.loads((path.OUT/'b-result.json').read_text())
   if len(calls)!=1 or result['answer']!=raw or len(result['handover']['evidence'])!=1:raise AssertionError('saved-manifest fake send failed')
  with tempfile.TemporaryDirectory(prefix='changed-b-send-') as tmp:
   path.OUT=Path(tmp);saved=json.loads(manifest.read_text());saved['meta']['derived_id']='changed';(path.OUT/'manifest.json').write_text(json.dumps(saved))
   try:path.send(expected,provider_transport=fake)
   except ValueError:pass
   else:raise AssertionError('changed manifest accepted')
   if len(calls)!=1:raise AssertionError('provider called on changed manifest')
  print('Saved manifest reached injected provider exactly once; changed manifest refused before call.')
 finally:path.OUT=original
if __name__=='__main__':main()
