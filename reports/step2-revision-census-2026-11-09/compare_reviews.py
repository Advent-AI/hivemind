import pathlib,json,collections
p=pathlib.Path('/Users/lchingen/hivemind/reports/step2-revision-census-2026-11-09');key={x['case']:x for x in json.loads((p/'key-private.json').read_text())};readers=[]
for x in 'ab':
 rows=json.loads((p/f'reader-{x}.json').read_text());r={v['case']:v for v in rows};assert len(r)==76 and set(r)==set(key) and len(rows)==76
 for z in rows: assert z['label'] in ('revision','repeat','different','uncertain') and all(k in z for k in ('case','label','stored_main','incoming_main','evidence','input_limit','confidence'))
 readers.append(r)
a,b=readers; rows=[]
for n,x in key.items():
 if x['answer']['choice']!='supersedes':continue
 rows.append({'case':n,'incoming':x['incoming'],'stored':x['stored_id'],'group':x['stored_group'],'final_group':x['final_group'],'label_a':a[n]['label'],'label_b':b[n]['label'],'reader_a':a[n],'reader_b':b[n]})
assert len(rows)==56
print('56 decisions: paired source labels',collections.Counter((x['label_a'],x['label_b']) for x in rows))
print('all 76 (A,B)',collections.Counter((a[n]['label'],b[n]['label']) for n in key))
# One actual edge per final-group and old-group: use `by` author, not a later decision.
lib=json.loads(pathlib.Path('/Users/lchingen/hivemind/poc/data/clean-e2e-2026-11-09/stage2-clean-d1-segment-2/step2/library.json').read_text());edge=[]
for x in rows:
 refs=lib['groups'][x['final_group']]['revises']
 if {'group':x['group'],'by':x['incoming']} in refs:edge.append(x)
assert len(edge)==30 and len({(x['final_group'],x['group']) for x in edge})==30
print('30 actual saved group edges:',collections.Counter((x['label_a'],x['label_b']) for x in edge))
print('disagreements',[(x['case'],x['label_a'],x['label_b'],x['incoming'],x['stored']) for x in rows if x['label_a']!=x['label_b']])
(p/'comparison.json').write_text(json.dumps({'all_cases':len(key),'revision_answers':rows,'saved_edges':edge},ensure_ascii=False,indent=2)+'\n')
