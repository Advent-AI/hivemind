import importlib.util, json, sqlite3, sys, collections
from pathlib import Path
R=Path('/Users/lchingen/hivemind'); sys.path.insert(0,str(R/'src'))
def load(path):
 s=importlib.util.spec_from_file_location('step_runner',path); m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
runner=load(R/'clean-arch/step2/run_forward.py'); compare=runner.compare
base=R/'poc/data/clean-acceptance-2026-11-09'; p=base/'step2'
dec=json.loads((p/'decisions.json').read_text()); lib=json.loads((p/'library.json').read_text()); vec=json.loads((p/'embeddings.json').read_text()); arts,questions,_=runner.step1_records(str(base/'step1/trace.sqlite')); records={r['id']:r for article in arts for r in article}; groups=lib['groups']; conn=sqlite3.connect('file:'+str(p/'jev.sqlite')+'?mode=ro',uri=True)
rows=conn.execute("select request_json,answer_json from model_calls where purpose='clean_step2'").fetchall(); saved={r:json.loads(a) for r,a in rows}; good=0; multi=0; single=0; allpairs=0; samples=[]
for d in dec:
 if not d['candidates']:continue
 rec=records[d['id']]; qs={f'q{i}':compare.piece_question(compare.piece_text(groups[g]['original'],'STORED PIECE')) for i,g in enumerate(d['candidates'])}; state=compare.piece_text(rec,'INCOMING PIECE'); req=json.dumps({'model':'jev-1.14.0','state':state,'questions':qs},sort_keys=True,ensure_ascii=False)
 if req not in saved: raise RuntimeError('missing exact stored request '+d['id'])
 answers=saved[req]; expected={g:{'choice':answers[f'q{i}']['choice'],'probabilities':answers[f'q{i}']['probabilities']} for i,g in enumerate(d['candidates'])}
 if expected!=d['answers']: raise RuntimeError('stored answer differs '+d['id'])
 qv=compare.query_vectors(vec,rec,questions); multi+=len(qv)>1;single+=len(d['candidates'])==1;allpairs+=len(qs);good+=1
 if len(samples)<10:
  g=d['candidates'][0];item=groups[g]['original'];score=compare.cosine(qv[0],vec[compare.doc_text(item)]);a=answers['q0'];samples.append({'id':d['id'],'incoming':rec['summary'],'stored':item['summary'],'score_query_1':round(score,5),'answer':a['choice'],'probabilities':a['probabilities']})
print(json.dumps({'matched_stored_requests':good,'archive_rows':len(rows),'pairs':allpairs,'multi_query_records':multi,'single_candidate_records':single,'samples':samples},indent=2,ensure_ascii=False))
