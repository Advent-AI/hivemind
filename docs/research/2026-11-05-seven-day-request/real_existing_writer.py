"""One isolated B handover through actual matcher/writer; refuses to reuse an output ledger."""
import copy,json,sqlite3,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path[:0]=[str(HERE),str(ROOT/'src')]
import existing_path as path
from hivemind import bundle,dispatch,extraction,model,pull,research_context
from hivemind.views import round as rounds,store


def main():
 cfg,uni,r,meta=path.build();out=path.OUT;manifest=out/'manifest.json';saved=json.loads(manifest.read_text());raw_result=json.loads((out/'b-result.json').read_text());provider=json.loads((out/'b-provider-response.json').read_text())
 answer=json.loads(provider['choices'][0]['message']['content'])
 if answer!=raw_result['answer'] or path.canonical(saved['meta'])!=path.canonical(meta) or saved['item']!=r['item'] or saved['shown']!=r['shown'] or path.wire(saved['b_request'])!=path.wire(r['request']):raise ValueError('pair, source, response or request changed')
 h,mapping=path.check(answer,r,uni)
 if h!=raw_result.get('handover') or mapping!=raw_result.get('id_mapping'):raise ValueError('saved B handover changed')
 if not h['evidence']:
  print('B returned no retained evidence: actual writer not exercised');return
 ledger=out/'real-writer-views.sqlite';archive_path=out/'real-writer-archive.sqlite';status=out/'real-writer-status.json';items_path=out/'real-writer-items.sqlite'
 if any(p.exists() for p in (ledger,archive_path,status,items_path)):raise ValueError('previous real writer output exists; inspect it before any recovery')
 src=sqlite3.connect(path.SNAP.resolve().as_uri()+'?mode=ro',uri=True);dst=sqlite3.connect(str(ledger));src.backup(dst);dst.close();src.close()
 conn=store.open_db(str(ledger));archive=model.Archive(str(archive_path));item=copy.deepcopy(r['item'])
 items=sqlite3.connect(str(items_path));items.row_factory=sqlite3.Row
 items.execute('create table items (input_id text primary key, title text, publisher text, publisher_type text, category text, publication_day text, source_uri text, text text)')
 item_fields=('input_id','title','publisher','publisher_type','category','publication_day','source_uri','text')
 items.execute('insert into items values (?,?,?,?,?,?,?,?)',tuple(item.get(k,'') for k in item_fields));items.commit()
 if bundle.item_lookup(items)(item['input_id'])['source_uri']!=meta['source_identity']['source_uri']:raise ValueError('derived source cannot be resolved')
 def save(stage,**extra):status.write_text(json.dumps({'stage':stage,**extra},ensure_ascii=False,indent=2)+'\n')
 try:
  shown=extraction.shown_views(conn,cfg,item,[o['value'] for o in item['object_identifiers'] if uni.has(o['value'])])
  if shown!=r['shown'] or store.last_completed_day(conn)!='2026-08-28':raise ValueError('actual starting state differs')
  route=dispatch.route(conn,item,uni)
  if route.kind!='extract':raise ValueError('unexpected route '+route.kind)
  handover=extraction.Handover(h['evidence'],h['candidates'],h['dropped'],0,path.sha(path.canonical(answer)),False,0,h['new_groups'])
  def extractor(*args,**kwargs):return copy.deepcopy(handover)
  save('matching',source_id=item['input_id'],seq=route.sequence_no,question_count=len(shown))
  result=rounds.run(conn,archive,cfg,uni,item,route.sequence_no,extractor=extractor)
  if result.failed:
   save('item_failed',error=result.failed,seq=route.sequence_no);print('Item failed:',result.failed,flush=True);return
  ids=[x[0] for x in conn.execute('select evidence_id from evidence where created_from_input=? order by rowid',(item['input_id'],))]
  written=[]
  for eid in ids:
   record=store.evidence(conn,eid);record['linked_views']=store.views_linked_to(conn,eid);written.append(record)
  save('written',seq=route.sequence_no,records=written,new_views=result.new_views)
  missing=[e['id'] for e in h['evidence'] if not any(w['quote']==e['quote'] and w['one_line']==e['one_line'] and set(e['links'])<=set(w['linked_views']) for w in written)]
  if missing or len(ids)!=len(h['evidence']):
   save('incomplete_write',seq=route.sequence_no,records=written,missing=missing);print('Evidence delivery incomplete:',missing,flush=True);return
  seq=store.next_sequence(conn)-1
  judged=rounds.judge_day(conn,archive,cfg,item['publication_day'],seq,log=print)
  if judged.failed:
   save('judge_failed',seq=seq,error=judged.failed,records=written);print('Daily judgement failed:',judged.failed,flush=True);return
  closed=pull.end_of_day(conn,item['publication_day'],seq)
  store.complete_day(conn,item['publication_day'],seq,'2026-08-29T23:59:59Z');conn.commit()
  next_item=dict(item,publication_day='2026-08-30');objects=[o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
  next_shown=extraction.shown_views(conn,cfg,next_item,objects)
  targets=sorted({v for record in written for v in record['linked_views']})
  next_evidence=[]
  with research_context.Reader(str(ledger),seq+1,objects,uni) as reader:
   catalog=reader.catalog();visible=[v for v in targets if any(q['view_id']==v for q in catalog['questions'])]
   if visible:next_evidence=reader.expand(visible)['evidence']
  found=[e['evidence_id'] for e in next_evidence if e['evidence_id'] in ids]
  if set(found)!=set(ids) or not judged.judged:
   save('incomplete_read',seq=seq,records=written,judged=judged.judged,next_boundary_evidence_ids=found);print('Next-boundary delivery incomplete',flush=True);return
  save('complete',seq=seq,records=written,judged=judged.judged,closed=closed,next_day_question_ids=[q['view_id'] for q in next_shown],next_boundary_evidence_ids=found)
  print('Matcher/writer stored',len(ids),'evidence; daily judgements',judged.judged,'next boundary read',len(found),flush=True)
 finally:items.close();archive.conn.close();conn.close()
if __name__=='__main__':main()
