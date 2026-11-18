import json,pathlib,random
r=pathlib.Path('/Users/lchingen/hivemind'); base=r/'poc/data/clean-acceptance-2026-11-09'; out=r/'reports/step2-jev-strengthening-council-2026-11-09'
leads=json.loads((out/'repeat-trace-leads.json').read_text()); lib=json.loads((base/'step2/library.json').read_text()); sources={x['id']:x for x in json.loads((base/'reader-packet.json').read_text())}
records={}
for g in lib['groups'].values():
 for item in [g['original']]+g['members']:records[item['id']]=item
miss=[x for x in leads if x.get('prior_group_found') and not x.get('joined_prior_group')]
controls=[x for x in leads if x.get('prior_group_found') and x.get('joined_prior_group')]
rng=random.Random(241109); sample=miss+rng.sample(controls,4);rng.shuffle(sample)
pairs=[];key=[]
for i,x in enumerate(sample,1):
 candidate=x['final_group'] if x['joined_prior_group'] else next(g for g in x['earlier_group_ids'] if g in x['candidate_groups'])
 old=lib['groups'][candidate]['original'];new=records[x['item']]
 def obj(t):
  source=sources[t['input_id']];return {'record':{k:t.get(k) for k in ('summary','passages','tier','original_party','reporting_speaker','statement_date','statement_date_text','evidence_period')},'article':{k:source[k] for k in ('title','publisher','publication_date','text')}}
 alias=f'V{i:02}'; pairs.append({'case':alias,'stored':obj(old),'incoming':obj(new)});key.append({'case':alias,'incoming':x['item'],'candidate_group':candidate,'joined':x['joined_prior_group'],'reference_group':x['group']})
(out/'blind-12-packet.json').write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n');(out/'blind-12-key.json').write_text(json.dumps(key,indent=2)+'\n')
print('prepared',len(pairs),'blind pairs, eight leads and four controls; packet bytes', (out/'blind-12-packet.json').stat().st_size)
