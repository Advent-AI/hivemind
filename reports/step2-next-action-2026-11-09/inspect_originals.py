"""Read-only: verify saved original full Jev requests and estimate baseline reservation.

No credential, network, modified request, or new reference is created.
"""
import collections,hashlib,importlib.util,json,pathlib,sqlite3
ROOT=pathlib.Path('/Users/lchingen/hivemind'); HIST=pathlib.Path('/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09');run=ROOT/'poc/data/clean-e2e-2026-11-09/stage2-clean-d1-segment-2/step2';out=ROOT/'reports/step2-next-action-2026-11-09'
ids=('C036','C057','C035','C073','C021','C059'); key={x['case']:x for x in json.loads((ROOT/'reports/step2-revision-census-2026-11-09/key-private.json').read_text())}; decisions={x['id']:x for x in json.loads((run/'decisions.json').read_text())};lib=json.loads((run/'library.json').read_text());rec={r['id']:r for g in lib['groups'].values() for r in [g['original']]+g['members']};spec=importlib.util.spec_from_file_location('jev_compare',ROOT/'clean-arch/step2/compare.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
rows=collections.defaultdict(list); db=sqlite3.connect(f'file:{run}/jev.sqlite?mode=ro',uri=True)
for sha,request,answer in db.execute("select request_sha256,request_json,answer_json from model_calls where purpose='clean_step2'"):
 if hashlib.sha256(request.encode()).hexdigest()!=sha:raise RuntimeError('archive SHA mismatch')
 payload=json.loads(request); rows[payload['state']].append((sha,request,json.loads(answer),payload))
results=[]
for case in ids:
 k=key[case];d=decisions[k['incoming']];state=m.piece_text(rec[k['incoming']],'INCOMING PIECE');questions={f'q{i}':m.piece_question(m.piece_text(lib['groups'][g]['original'],'STORED PIECE')) for i,g in enumerate(d['candidates'])};qid='q'+str(d['candidates'].index(k['stored_group']))
 hits=[(sha,request,answer,payload) for sha,request,answer,payload in rows[state] if payload['questions']==questions and answer[qid]['choice']==k['answer']['choice'] and answer[qid]['probabilities']==k['answer']['probabilities']]
 if len(hits)!=1:raise RuntimeError('not unique '+case)
 sha,request,answer,payload=hits[0]; canonical=json.dumps(payload,sort_keys=True,ensure_ascii=False)
 if canonical.encode()!=request.encode():raise RuntimeError('archive serialization mismatch '+case)
 results.append({'case':case,'incoming':k['incoming'],'stored_group':k['stored_group'],'target_qid':qid,'archive_sha256':sha,'body_bytes':len(request.encode()),'question_count':len(questions),'target_choice':answer[qid]['choice'],'target_probabilities':answer[qid]['probabilities']})
db.close()
chain=json.loads((HIST/'evidence-chain-DRAFT.json').read_text());b=next(x for x in chain['cases'] if x['id']=='B01');db=sqlite3.connect('file:'+b['historic_archive']+'?mode=ro',uri=True);hits=db.execute('select request_json,answer_json from model_calls where request_sha256=?',(b['historic_request_sha256'],)).fetchall()
if len(hits)!=1:raise RuntimeError('B01 not unique')
request,answer=hits[0];sha=hashlib.sha256(request.encode()).hexdigest();assert sha==b['historic_request_sha256'];payload=json.loads(request);assert json.dumps(payload,sort_keys=True,ensure_ascii=False)==request;answer=json.loads(answer); qid=b['question_id'];assert answer[qid]['choice']=='same_statement'
results.append({'case':'B01','target_qid':qid,'archive_sha256':sha,'body_bytes':len(request.encode()),'question_count':len(payload['questions']),'target_choice':answer[qid]['choice'],'target_probabilities':answer[qid]['probabilities']});db.close()
# Prior approved sender uses conservative two-times UTF-8 byte count plus 4096 tokens, all at dated Jev input price $0.042 / M; output free.
base_per_draw=sum(((2*x['body_bytes']+4096)*.042)/1e6 for x in results); print(json.dumps(results,indent=2));print('baseline 7 req, per draw reserved USD',round(base_per_draw,6));print('two arms, three draws baseline bytes only USD',round(6*base_per_draw,6),'plus candidate length change; estimate not guaranteed bill');print('checks:',len(results),'unique exact original archive SHA and original canonical transport bytes, only; no candidate has been bound')
(out/'originals-metadata.json').write_text(json.dumps(results,indent=2)+'\n')
