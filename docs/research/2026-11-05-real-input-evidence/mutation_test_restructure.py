"""Check that source/link/ladder/no-home tests detect disabled production checks in scratch copies."""
import shutil,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
mutations={
 'quote':[("if len(quote) < 8 or quote not in body:","if False:")],
 'links':[("links = [l for l in e['links'] if l in shown_ids or l in candidate_ids]","links = list(e['links'])"),("e['links'] = [l for l in e['links'] if l in shown_ids or any(c['id'] == l for c in final_candidates)]","e['links'] = list(e['links'])")],
 'ladder':[("problem = check_ladder(c['rungs'], c['kind'])","problem = None")],
 'no_home':[("homeless = [e for e in evidence if not e['links']]","homeless = []")],
}
program='''import sys,importlib.util
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import hivemind.extraction
p=Path(sys.argv[2]);spec=importlib.util.spec_from_file_location('runner',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
_,uni,reqs=m.a.build()
try:m.checks(reqs,uni)
except AssertionError:
 import traceback;print('MUTANT_CAUGHT');traceback.print_exc();raise SystemExit(0)
raise SystemExit('MUTANT_ESCAPED')
'''
for name,changes in mutations.items():
 with tempfile.TemporaryDirectory(prefix='hivemind-prompt-mutant-') as tmp:
  target=Path(tmp)/'hivemind';shutil.copytree(ROOT/'src/hivemind',target,ignore=shutil.ignore_patterns('__pycache__'))
  path=target/'extraction.py';s=path.read_text()
  for before,after in changes:
   if s.count(before)!=1:raise SystemExit(f'{name}: mutation anchor differs')
   s=s.replace(before,after,1)
  path.write_text(s)
  result=subprocess.run([sys.executable,'-c',program,tmp,str(HERE/'run_restructure_pilot.py')],capture_output=True,text=True)
  if result.returncode or result.stdout.strip()!='MUTANT_CAUGHT':raise SystemExit(f'{name}: unexpected result\n{result.stdout}\n{result.stderr}')
  print(name,'caught',result.stderr.strip().splitlines()[-2:])
