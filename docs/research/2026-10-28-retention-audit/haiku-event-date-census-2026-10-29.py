"""Count empty original dates with a distinct ISO event date in the stored treatment answers."""
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
RUN=HERE/'haiku-date-arm-2026-10-29'
OUT=HERE/'haiku-event-date-census-2026-10-29.json'


def main():
 files=sorted(RUN.glob('*-arm-[123].json'));assert len(files)==21
 rows=[];empty=0;total=0
 for f in files:
  d=json.loads(f.read_text());assert d['completed'] and not d['schema_errors']
  for e in d['sift']['evidence']:
   total+=1
   if e['original_day']=='':
    empty+=1
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}',e['event_time']):
     rows.append({'sample':f.name,'id':e['id'],'event_time':e['event_time'],'original_who':e['original_who'],
                  'speaker':e['speaker'],'one_line':e['one_line'],'quote':e['quote']})
 assert total==121 and empty==94 and len(rows)==34
 assert any(r['sample']=='memory-arm-1.json' and r['id']=='e4' and r['event_time']=='2026-07-18' for r in rows)
 assert any(r['sample']=='policy-arm-2.json' and r['id']=='e3' and r['event_time']=='2026-07-21' for r in rows)
 result={'samples':len(files),'evidence':total,'empty_original_day':empty,'empty_with_iso_event_day':len(rows),'rows':rows,
         'limit':'A shared field pattern is not an error count; event_time can refer to an event or article rather than the original statement.'}
 with OUT.open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in result.items() if k!='rows'},ensure_ascii=False))

if __name__=='__main__':main()
