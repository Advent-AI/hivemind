import importlib.util,json,random,sqlite3,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('prep',H/'probe_prepare.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
manifest=json.loads((H/'probe-manifest.json').read_text());groups=json.loads((p.STEP/'library.json').read_text())['groups']; articles,_,_=p.run.step1_records(str(p.SOURCE/'step1/trace.sqlite'));records={r['id']:r for a in articles for r in a};c=sqlite3.connect('file:'+str(p.SOURCE/'step1/trace.sqlite')+'?mode=ro',uri=True)
sources={}
for (request,) in c.execute("select request from trace where status='complete'"):
 req=json.loads(request);o=json.JSONDecoder().raw_decode(req['messages'][1]['content'])[0]['source_item'];sources[o['id']]={k:o.get(k) for k in ('title','publisher','publication_date','source_uri','text')}
pack=[];key={}
for num,item in enumerate(manifest,1):
 rec=records[item['id']];group_ids=list(item['candidates']);random.Random(8120+num).shuffle(group_ids);candidates=[]; key[str(num)]={'record_id':item['id'],'groups':{}}
 for i,g in enumerate(group_ids,1):
  old=groups[g]['original'];code=f'C{i}'; key[str(num)]['groups'][code]=g
  candidates.append({'id':code,'summary':old['summary'],'passages':old['passages'],'original_party':old['original_party'],'statement_date':old['statement_date'] or old['statement_date_text'],'source':sources[old['input_id']]})
 pack.append({'case':str(num),'incoming':{'summary':rec['summary'],'passages':rec['passages'],'original_party':rec['original_party'],'statement_date':rec['statement_date'] or rec['statement_date_text'],'source':sources[rec['input_id']]},'candidates':candidates})
(H/'blind-packets.json').write_text(json.dumps(pack,ensure_ascii=False,indent=1)+'\n');(H/'blind-key.json').write_text(json.dumps(key,indent=1)+'\n');print('cases',len(pack),'pairs',sum(len(x['candidates']) for x in pack),'chars',(H/'blind-packets.json').stat().st_size,'packet sha256',hashlib.sha256((H/'blind-packets.json').read_bytes()).hexdigest())
