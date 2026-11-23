import json,pathlib,collections
p=pathlib.Path('/Users/lchingen/hivemind/reports/step2-revision-census-2026-11-09');a=json.loads((p/'comparison.json').read_text()); post={'C025':'uncertain','C030':'different','C034':'uncertain','C037':'repeat','C049':'uncertain','C051':'uncertain','C052':'different','C059':'different','C068':'uncertain'}
for kind in ('revision_answers','saved_edges'):
 for x in a[kind]:
  if x['label_a']==x['label_b']:x['after_challenge']=x['label_a']
  else:
   assert x['case'] in post;x['after_challenge']=post[x['case']]
 print(kind, len(a[kind]),dict(collections.Counter(x['after_challenge'] for x in a[kind])))
print('both-source differing before challenge',sum(x['label_a']==x['label_b']=='different' for x in a['revision_answers']))
print('post-challenge different IDs',','.join(x['case'] for x in a['revision_answers'] if x['after_challenge']=='different'))
print('actual edges IDs',','.join(x['case'] for x in a['saved_edges']))
(p/'comparison-after-challenge.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
