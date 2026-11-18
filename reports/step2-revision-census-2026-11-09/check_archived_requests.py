import pathlib,sys,sqlite3,json,collections,importlib.util
root=pathlib.Path('/Users/lchingen/hivemind');p=root/'poc/data/clean-e2e-2026-11-09/stage2-clean-d1-segment-2';out=root/'reports/step2-revision-census-2026-11-09';spec=importlib.util.spec_from_file_location('compare',root/'clean-arch/step2/compare.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
lib=json.loads((p/'step2/library.json').read_text());d={x['id']:x for x in json.loads((p/'step2/decisions.json').read_text())};records={r['id']:r for g in lib['groups'].values() for r in [g['original']]+g['members']};db=sqlite3.connect(f'file:{p}/step2/jev.sqlite?mode=ro',uri=True);by_state=collections.defaultdict(list)
for req,ans in db.execute('select request_json,answer_json from model_calls where purpose=?',('clean_step2',)):
 r=json.loads(req); by_state[r['state']].append((r,json.loads(ans)))
fail=[];count=0
for x in json.loads((out/'key-private.json').read_text()):
 dec=d[x['incoming']]; state=m.piece_text(records[x['incoming']],'INCOMING PIECE');qs={f'q{i}':m.piece_question(m.piece_text(lib['groups'][g]['original'],'STORED PIECE')) for i,g in enumerate(dec['candidates'])}; q='q'+str(dec['candidates'].index(x['stored_group']));hits=[(r,a) for r,a in by_state[state] if r['questions']==qs and a.get(q,{}).get('choice')==x['answer']['choice'] and a.get(q,{}).get('probabilities')==x['answer']['probabilities']]
 if len(hits)!=1:fail.append((x['case'],x['incoming'],x['stored_group'],len(hits),len(by_state[state])))
 else:count+=1
print('Matched full archived comparison request and exact candidate answer:',count,'of 76')
print('unmatched / duplicate:',fail)
if count!=76:raise SystemExit(1)
