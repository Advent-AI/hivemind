"""Exercise actual isolated runner, writer, daily judging and reader with fake external services."""
import json,shutil,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path[:0]=[str(HERE),str(ROOT/'src')]
import existing_path as path
import real_existing_writer as runner
import test_existing_writer as writer_test
from hivemind import jev,model

def fake_judge(provider,request):
 answer={'rung':1,'reference':'Test-only reference','implied_outcome':'Test-only outcome','reasons':'Test-only reason','cites':[],'cites_views':[],'pushes':[],'changed':False,'why_changed':'No change in this fixture','theme_pushes':[]}
 return {'choices':[{'message':{'content':json.dumps(answer)}}],'usage':{}}

def main():
 cfg,uni,r,_=path.build();path.fake_controls(cfg,uni,r)
 original_dir=path.OUT;original_jev=jev.transport;original_openai=model.openai_transport
 try:
  with tempfile.TemporaryDirectory(prefix='existing-runner-fake-') as tmp:
   path.OUT=Path(tmp);shutil.copyfile(original_dir/'manifest.json',path.OUT/'manifest.json')
   shutil.copyfile(original_dir/'b-result.json',path.OUT/'b-result.json')
   shutil.copyfile(original_dir/'b-provider-response.json',path.OUT/'b-provider-response.json')
   jev.transport=writer_test.fake_jev;model.openai_transport=fake_judge
   runner.main()
   status=json.loads((path.OUT/'real-writer-status.json').read_text())
   if status['stage']!='complete' or len(status['records'])!=2 or len(status['next_boundary_evidence_ids'])!=2 or status['judged']!=1:raise AssertionError(status)
   try:runner.main()
   except ValueError as e:
    if 'previous real writer output exists' not in str(e):raise
   else:raise AssertionError('repeat run duplicated writer')
   print('Full isolated runner passed with fake Jev and fake judge; second execution refused.')
 finally:path.OUT=original_dir;jev.transport=original_jev;model.openai_transport=original_openai
if __name__=='__main__':main()
