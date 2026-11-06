"""The successor retains the exact stopped state and refuses altered cached calls."""
import copy,json,shutil,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path[:0]=[str(HERE),str(ROOT/'src')]
import fork_metadata_run as f
import split_seven_day_poc as p

def main():
 parent=ROOT/'poc/data/split-fresh-seven-day-2026-11-05-v1';probe=ROOT/'poc/data/split-metadata-repair-1207-v1';source=parent/'items'/'1207'
 with tempfile.TemporaryDirectory(prefix='metadata-fork-') as d:
  out=Path(d)/'fork';f.fork(parent,out,probe,1207)
  status=p.read(out/'run-status.json');manifest=p.read(out/'manifest.json');dest=out/'items'/'1207'
  assert status['completed']==2 and status['status']=='failed'
  assert manifest['forked_from']['failed_sequence']==1207
  assert f.sha(out/'views.sqlite')==f.sha(parent/'snapshot/views.sqlite')
  for arm in ('a','b'):
   for suffix in ('request.json','provider.json','answer.json'):
    assert f.sha(dest/(arm+'-'+suffix))==f.sha(source/(arm+'-'+suffix))
  for file in source.glob('meta-*'):
   if file.is_file():assert f.sha(dest/'previous-preparation'/file.name)==f.sha(file)
  assert f.sha(dest/'meta-answer.json')==f.sha(probe/'meta-answer.json')
  bad=Path(d)/'bad-probe';shutil.copytree(probe,bad)
  altered=p.read(bad/'meta-answer.json');del altered['evidence']['e2'];p.write(bad/'meta-answer.json',altered)
  try:f.fork(parent,Path(d)/'bad-fork',bad,1207)
  except ValueError:pass
  else:raise AssertionError('tampered metadata was reused')
  assert not (Path(d)/'bad-fork').exists()
  original_select=p.select_manifest
  def changed_runtime(pilot_id=None):
   result=original_select(pilot_id)
   result['runtime_hashes']['docs/research/2026-11-05-seven-day-request/split_seven_day_poc.py']='0'*64
   return result
  try:
   p.select_manifest=changed_runtime
   try:f.fork(parent,Path(d)/'bad-runtime',probe,1207)
   except ValueError as error:assert 'reviewed runtime' in str(error)
   else:raise AssertionError('unreviewed runtime was accepted')
  finally:p.select_manifest=original_select
 print('PASS: exact parent ledger and A/B reused; partial metadata preserved; tampered repair refused.')
if __name__=='__main__':main()
