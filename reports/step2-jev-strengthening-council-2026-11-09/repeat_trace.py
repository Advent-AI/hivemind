"""Construct leads for frozen repeat members using two existing independent item mappings.

A match is only a mapping lead: this does not score semantic identity or alter the reference.
"""
import collections,glob,json,pathlib
ROOT=pathlib.Path('/Users/lchingen/hivemind')
R=ROOT/'poc/data/clean-acceptance-2026-11-09'
ref=json.loads((R/'settled.json').read_text());library=json.loads((R/'step2/library.json').read_text());decisions={d['id']:d for d in json.loads((R/'step2/decisions.json').read_text())}
answers={}
for who in ('A','B'):
 mapping={}
 for path in sorted(glob.glob(str(R/'judge'/f'judge-{who}-*.json'))):
  for article in json.loads(pathlib.Path(path).read_text())['articles']:
   for m in article.get('matters',[]):
    if m['matter'] in mapping:raise ValueError('duplicate reader matter')
    mapping[m['matter']]={'status':m['status'],'item':m.get('item')}
 answers[who]=mapping
counts=collections.Counter(m['matter'] for g in ref['repeat_groups'] for m in g['members'])
byitem=collections.defaultdict(set)
for matter in set(answers['A']) & set(answers['B']):
 a=answers['A'][matter];b=answers['B'][matter]
 if a['status']==b['status']=='kept' and a['item'] and a['item']==b['item']:byitem[a['item']].add(matter)
def match(matter):
 a=answers['A'].get(matter);b=answers['B'].get(matter)
 if not a or not b:return None,'reader_missing'
 if a['status']==b['status']=='missed':return None,'both_missed'
 if a['status']!=b['status'] or a['item']!=b['item'] or a['status']!='kept' or not a['item']:return None,'reader_disagrees_or_other'
 if counts[matter]>1 or len(byitem[a['item']])>1:return None,'multiple_matters_or_groups'
 if a['item'] not in decisions or a['item'] not in library['placement']:return None,'record_missing'
 return a['item'],'two_readers_same_unambiguous_item_lead'
result=[]
for index,g in enumerate(ref['repeat_groups']):
 earlier=[]
 for member in g['members']:
  matter=member['matter'];item,state=match(matter)
  if member['kind']=='repeat':
   x={'group':index,'matter':matter,'kind':member['kind'],'item':item,'item_mapping':state,'earlier':list(earlier)}
   if item:
    d=decisions[item]; prior=[r for r in earlier if r['item'] and r['item']!=item];priorgroups={library['placement'][r['item']] for r in prior}
    x['earlier_group_ids']=sorted(priorgroups);x['candidate_groups']=d['candidates'];x['outcome']=d['outcome'];x['final_group']=library['placement'][item]
    x['prior_group_found']=bool(priorgroups & set(d['candidates'])) if priorgroups else None
    x['joined_prior_group']=library['placement'][item] in priorgroups if priorgroups else None
   result.append(x)
  earlier.append({'matter':matter,'item':item,'mapping':state})
if len(result)!=55:raise ValueError('unexpected repeat count')
known=next(x for x in result if x['item']=='20:ev-1')
if known['prior_group_found'] is not True or known['joined_prior_group'] is not False or '8:E1' not in [v['item'] for v in known['earlier']]:raise ValueError('H01 positive control failed')
out=ROOT/'reports/step2-jev-strengthening-council-2026-11-09/repeat-trace-leads.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('55 frozen later-repeat members; H01 known-path positive control passed; leads only, not scored')
print('current mapping',dict(collections.Counter(x['item_mapping'] for x in result)))
print('candidate/final status among item-mapped cases',dict(collections.Counter((x.get('prior_group_found'),x.get('joined_prior_group')) for x in result if x['item'])))
