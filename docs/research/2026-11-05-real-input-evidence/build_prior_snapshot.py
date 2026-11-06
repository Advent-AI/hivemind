"""Create an isolated as-of 1204 copy of the actual v34 library for the paired pilot."""
import hashlib
import json
import sqlite3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'src'))
from hivemind import config,extraction,testdb,universe
from hivemind.views import store
SOURCE=Path('/Users/lchingen/hivemind/poc/data/served-2026-10-28-v34-nvda-3m-through-0828/views.sqlite')
TARGET=ROOT/'poc/data/pilot-d369-existing-library-v2'
ITEMS=ROOT/'poc/data/real-evidence-d369-variants-draft-v1/items.sqlite'
CONTEXT=Path(__file__).parent/'prior-context-68-v1.json'
if TARGET.exists():raise SystemExit('snapshot exists; refusing overwrite')
TARGET.mkdir(parents=True)
src=sqlite3.connect(SOURCE.resolve().as_uri()+'?mode=ro',uri=True)
tmp=sqlite3.connect(str(TARGET/'views.sqlite'));src.backup(tmp);tmp.close();src.close()
c=store.open_db(str(TARGET/'views.sqlite'))
# The existing library contains a partially processed August 29; remove only explicitly
# sequence-tagged records after the last completed day, in this new scratch copy.
columns={'evidence_links':'seq','evidence_sources':'seq','same_claims':'seq','handovers':'seq','match_records':'seq','processing_steps':'sequence_no','evidence':'created_seq'}
removed={}
for t,col in columns.items():
 removed[t]=c.execute(f'select count(*) from {t} where {col}>?',(1204,)).fetchone()[0]
 trigger_name=t+'_no_delete'
 trigger_sql=c.execute('select sql from sqlite_master where type=? and name=?',('trigger',trigger_name)).fetchone()[0]
 c.execute('drop trigger '+trigger_name)
 c.execute(f'delete from {t} where {col}>?',(1204,))
 c.execute(trigger_sql)
c.commit()
for t in ['views','thesis_groups','view_keys','thesis_group_members','dependencies','dependency_resolutions','replacements','revisions','successions','judgements','review_pool_entries','late_statements','days_completed']:
 cols={r[1] for r in c.execute('pragma table_info('+t+')')}
 for col in ('seq','created_seq'):
  if col in cols and c.execute(f'select count(*) from {t} where {col}>?',(1204,)).fetchone()[0]:raise ValueError('unhandled later rows: '+t+'.'+col)
if c.execute('select count(*) from view_switches where after_seq>1204').fetchone()[0]:raise ValueError('later switches')
if c.execute('pragma integrity_check').fetchone()[0]!='ok':raise ValueError('integrity')
expected=json.loads(CONTEXT.read_text()); items=sqlite3.connect(ITEMS.resolve().as_uri()+'?mode=ro',uri=True);items.row_factory=sqlite3.Row
cfg=config.load(ROOT/'poc/config/poc-v117.json');uni=universe.load(ROOT/'poc/universe.json')
for ref in expected['articles']:
 item=testdb.item_of(items.execute('select * from items where input_id=?',(ref['variant_id'],)).fetchone())
 shown=extraction.shown_views(c,cfg,item,[o['value'] for o in item['object_identifiers'] if uni.has(o['value'])])
 if shown!=ref['shown'] or store.day_start_seq(c,item['publication_day'])!=1204:raise ValueError('historical shown context differs')
c.close();items.close()
report={'source_db_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'snapshot_db_sha256':hashlib.sha256((TARGET/'views.sqlite').read_bytes()).hexdigest(),'context_sha256':hashlib.sha256(CONTEXT.read_bytes()).hexdigest(),'cutoff_seq':1204,'removed_after_cutoff':removed,'shown_per_article':68,'caveat':'historical question library as of Aug 28; source texts may not reconstruct original time and questions can be imperfect; not exact article-day production state'}
(TARGET/'snapshot.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
