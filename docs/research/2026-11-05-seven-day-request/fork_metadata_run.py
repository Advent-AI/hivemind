"""Fork the failed seven-day diagnostic without replaying completed writes or A/B calls."""
import fcntl,hashlib,json,shutil,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path[:0]=[str(HERE),str(ROOT/'src')]
import split_seven_day_poc as p
from hivemind import config,model,testdb,universe

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def fork(parent,out,probe,seq):
 parent=parent.resolve();out=out.resolve();probe=probe.resolve()
 if out.exists():raise ValueError('fork output already exists')
 with (parent/'run.lock').open('a') as lock:
  try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:raise ValueError('parent run is still active')
  snapshot=parent/'snapshot';status=p.read(snapshot/'run-status.json');old=p.read(parent/'manifest.json')
  if status['status']!='failed' or not status['failures'] or 'metadata positions differ from A' not in status['failures'][-1]['error']:
   raise ValueError('parent failure is not the recorded metadata omission')
  current=p.select_manifest(None)
  for key in ('source_snapshot_sha256','initial_ledger_sha256','input_rows','excluded_rows','days'):
   if old[key]!=current[key]:raise ValueError('parent source selection differs: '+key)
  old_runtime=old['runtime_hashes'];new_runtime=current['runtime_hashes']
  split='docs/research/2026-11-05-seven-day-request/split_seven_day_poc.py'
  reviewed_repair='1b68c98901f38d53e0c868049cec35933a4382a7b84f053319cd417a1aa8a40f'
  if new_runtime.get(split)!=reviewed_repair:raise ValueError('current metadata repair differs from the reviewed runtime')
  if fsha:=old_runtime.get(split):
   if sha(HERE/'parent-runtime-1207.txt')!=fsha:raise ValueError('parent runtime reconstruction differs')
  else:raise ValueError('parent runtime hash missing')
  for name,value in old_runtime.items():
   if name==split or Path(name).name.startswith('test_'):continue
   if new_runtime.get(name)!=value:raise ValueError('non-metadata runtime changed: '+name)
  if any(name not in old_runtime and not (Path(name).name.startswith('test_') or name.endswith('/fork_metadata_run.py')) for name in new_runtime):
   raise ValueError('unexpected new runtime file')
  db=p.store.open_read_only(str(snapshot/'views.sqlite'))
  dispatch=db.execute('select input_id from processing_steps where sequence_no=? and step=\'dispatched\' order by id limit 1',(seq,)).fetchone()
  if not dispatch:raise ValueError('failed input dispatch absent')
  input_id=dispatch[0]
  if db.execute('select 1 from handovers where seq=?',(seq,)).fetchone() or p.store.is_processed(db,input_id):raise ValueError('failed input already handed over')
  if status['completed']!=len(status['completed_items']):raise ValueError('parent completion count differs')
  for completed_id,kind in status['completed_items'].items():
   if kind=='written':
    step=p.store.last_step(db,completed_id)
    if not p.store.is_processed(db,completed_id) or not step or step['sequence_no']>=seq:raise ValueError('completed writer marker differs')
   elif not db.execute('select 1 from poc_input_outcomes where input_id=? and kind=?',(completed_id,kind)).fetchone():
    raise ValueError('completed routing marker differs')
  for (table,) in db.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'"):
   cols={r[1] for r in db.execute('pragma table_info("'+table.replace('"','""')+'")')}
   for col in ('seq','created_seq','after_seq','sequence_no'):
    if col in cols:
     n=db.execute('select count(*) from "'+table.replace('"','""')+'" where "'+col+'">=?',(seq,)).fetchone()[0]
     if n and not (table=='processing_steps' and col=='sequence_no' and n==1):raise ValueError('unexpected data at or after failed sequence: '+table)
  inputs=testdb.open_db(str(p.INPUT));row=inputs.execute('select * from items where input_id=?',(input_id,)).fetchone()
  if not row:raise ValueError('original article missing')
  item=testdb.item_of(row);inputs.close()
  selected=next((r for r in current['input_rows'] if r['id']==input_id),None)
  if not selected or p.digest((item.get('text') or '').encode())!=selected['body_sha256']:raise ValueError('source article changed')
  uni=universe.load(str(ROOT/'poc/universe.json'));p.load_written_subjects(db,uni)
  shown=p.latest_library(db,seq);db.close();source_folder=parent/'items'/str(seq)
  if shown!=p.read(source_folder/'shown.json'):raise ValueError('parent shown library changed')
  cfg=config.load(str(ROOT/'poc/config/poc-v118.json'));setting,requests=p.item_requests(cfg,uni,item,shown)
  for arm,spec in requests.items():
   if p.completed_answer(cfg,setting,arm,spec,source_folder) is None:raise ValueError('missing complete '+arm+' result')
  a=p.read(source_folder/'a-answer.json');meta_spec=p.metadata_request(item,a)
  if p.completed_answer(cfg,setting,'meta',meta_spec,probe) is None:raise ValueError('repaired metadata missing')
  original_hashes={path.name:sha(path) for path in source_folder.glob('meta-*') if path.is_file()}
  old_ledger_hash=sha(snapshot/'views.sqlite');old_archive_hash=sha(snapshot/'match-judge-archive.sqlite')
  out.mkdir(parents=True);shutil.copyfile(snapshot/'views.sqlite',out/'views.sqlite');shutil.copyfile(snapshot/'match-judge-archive.sqlite',out/'match-judge-archive.sqlite')
  shutil.copytree(parent/'items',out/'items');shutil.copyfile(parent/'snapshot.sh',out/'snapshot.sh')
  if sha(out/'views.sqlite')!=old_ledger_hash or sha(out/'match-judge-archive.sqlite')!=old_archive_hash:raise ValueError('fork ledger/archive copy mismatch')
  dest=out/'items'/str(seq);backup=dest/'previous-preparation';backup.mkdir()
  for path in list(dest.glob('meta-*')):
   if path.is_file():shutil.move(str(path),str(backup/path.name))
  for path in probe.glob('meta-*'):
   if path.is_file():shutil.copyfile(path,dest/path.name)
  if p.completed_answer(cfg,setting,'meta',meta_spec,dest) is None:raise ValueError('repaired metadata copy failed')
  for arm in ('a','b'):
   for suffix in ('request.json','provider.json','answer.json'):
    name=arm+'-'+suffix
    if sha(dest/name)!=sha(source_folder/name):raise ValueError('original '+name+' changed')
  if {path.name:sha(path) for path in backup.iterdir()}!=original_hashes:raise ValueError('original metadata not preserved')
  p.write(out/'run-status.json',status)
  current['forked_from']={'parent':str(parent),'parent_manifest_sha256':sha(parent/'manifest.json'),'parent_snapshot_ledger_sha256':old_ledger_hash,'parent_snapshot_archive_sha256':old_archive_hash,'failed_sequence':seq,'failed_input_id':input_id,'repaired_metadata_source':str(probe),'original_metadata_sha256':original_hashes,'prior_completed':status['completed']}
  p.write(out/'manifest.json',current)
  print('Fork created; preserved',status['completed'],'completed items and original A/B; repaired metadata verified; manifest',sha(out/'manifest.json'))
if __name__=='__main__':
 if len(sys.argv)!=5:raise SystemExit('fork_metadata_run.py PARENT OUT PROBE SEQ')
 fork(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),int(sys.argv[4]))
