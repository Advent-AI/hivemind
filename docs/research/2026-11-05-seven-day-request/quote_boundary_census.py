import sqlite3,json,pathlib,re,collections
root=pathlib.Path('/Users/lchingen/hivemind-no-preseed-evidence-review');run=root/'poc/data/split-seven-day-optional-2026-11-05-v3';views=sqlite3.connect(run/'snapshot/views.sqlite');items=sqlite3.connect(root/'poc/data/parallel-thesis-evidence-input-2026-11-05/items.sqlite')
counts=collections.Counter();bad=[]
for folder in sorted((run/'items').iterdir(),key=lambda x:int(x.name)):
 if not folder.is_dir() or not (folder/'handover.json').exists():continue
 row=views.execute('select input_id from handovers where seq=?',(int(folder.name),)).fetchone()
 if not row:counts['missing_db_handover']+=1;continue
 result=items.execute('select text from items where input_id=?',(row[0],)).fetchone()
 if not result:counts['missing_article']+=1;continue
 text=result[0] or '';data=json.loads((folder/'handover.json').read_text());counts['handovers']+=1
 for e in data['evidence']:
  quote=e['quote'];counts['evidence']+=1;positions=[m.start() for m in re.finditer(re.escape(quote),text)] if quote else []
  if not positions:counts['not_exact']+=1;continue
  def invalid(i):
   l=text[i-1] if i else '';r=text[i+len(quote):i+len(quote)+1];a=quote[:1];z=quote[-1:]
   return bool((l and a and l.isalnum() and a.isalnum()) or (r and z and r.isalnum() and z.isalnum()) or (l and a.isdigit() and l in '-+−$€£¥'))
  if all(map(invalid,positions)):
   counts['partial_token']+=1;i=positions[0];bad.append({'seq':int(folder.name),'input_id':row[0],'evidence_id':e['id'],'quote':quote,'context':text[max(0,i-45):i+len(quote)+45]})
  else:counts['exact_boundary_ok']+=1
out={'counts':dict(counts),'partial_token_examples':bad};path=root/'docs/research/2026-11-05-seven-day-request/2026-11-05-quote-boundary-census.json';path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2)[:5000])
