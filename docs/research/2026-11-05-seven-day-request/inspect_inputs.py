"""Read-only seven-day feed and frozen-gold census; never launches a replay."""
from collections import Counter
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
import hashlib,json,sqlite3,sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'src'))
from hivemind import testdb
DATA=ROOT/'poc/data/parallel-thesis-evidence-input-2026-11-05'
GOLD=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/golden-v5')
HERE=Path(__file__).resolve().parent
DAYS=['2026-08-29','2026-08-30','2026-08-31','2026-09-01','2026-09-02','2026-09-03','2026-09-04']

def date(s):
 try:return parsedate_to_datetime(s).date().isoformat()
 except (TypeError,ValueError,OverflowError):
  try:return datetime.fromisoformat(s.replace('Z','+00:00')).date().isoformat()
  except (TypeError,ValueError,OverflowError):return None

def main():
 conn=testdb.open_db(str(DATA/'items.sqlite'))
 rows=[]
 for d in DAYS:
  for item in testdb.feed(conn,d,d):
   later=bool(date(item.get('published_at')) and date(item['published_at'])>d)
   known_update=item['input_id']=='gnews:b6c2330e01a0c4ddb500583a'
   rows.append({'id':item['input_id'],'day':d,'title':item['title'],'published_at':item.get('published_at'),'source_uri':item.get('source_uri'),'body_sha256':hashlib.sha256((item.get('text') or '').encode()).hexdigest(),'date_after_assigned_day':later,'known_updated_after_day':known_update})
 conn.close()
 if not rows or len({r['id'] for r in rows})!=len(rows):raise ValueError('empty or duplicate feed')
 # Positive controls: one clear two-month date mismatch and known source update.
 if not any(r['id']=='gnews:15f4133549cd22ba7b1c0996' and r['date_after_assigned_day'] for r in rows):raise ValueError('future-date control missing')
 gold=[]
 for name in ['golden-v5-dev.json','golden-v5-test.json']:
  p=GOLD/name; data=json.loads(p.read_text())
  for a in data['articles']:
   x=next((r for r in rows if r['id']==a['input_id']),None)
   if x:gold.append({'input_id':a['input_id'],'day':x['day'],'set':name,'must_open':len(a.get('questions',{}).get('must_open',[])),'may_open':len(a.get('questions',{}).get('may_open',[])),'issues':len(a.get('items',[])),'date_after_assigned_day':x['date_after_assigned_day'],'known_updated_after_day':x['known_updated_after_day']})
 with sqlite3.connect((DATA/'views.sqlite').resolve().as_uri()+'?mode=ro',uri=True) as c:
  end=c.execute("select seq from days_completed where day='2026-08-28' order by id desc limit 1").fetchone()[0]
  count=c.execute('select count(*) from views where created_seq<=?',(end,)).fetchone()[0]
 if end!=1204 or count!=68:raise ValueError('starting snapshot changed')
 summary={'status':'preparation only; no model test started', 'days':DAYS,'initial_completed_day':'2026-08-28','initial_seq':end,'initial_question_count':count,'feed_items':len(rows),'by_day':dict(Counter(r['day'] for r in rows)), 'later_timestamp_count':sum(r['date_after_assigned_day'] for r in rows),'known_updated_after_day_count':sum(r['known_updated_after_day'] for r in rows),'gold_articles':gold,'source_version_caveat':'timestamp and body quality not independently established; later timestamps are unresolved, not automatic proof of wrong day','rows':rows}
 out=HERE/'seven-day-source-census-2026-11-05.json'
 if out.exists():raise ValueError('output already exists')
 out.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k!='rows'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
