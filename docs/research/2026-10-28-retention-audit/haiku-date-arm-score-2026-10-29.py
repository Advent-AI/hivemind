"""Record a model analyst's predeclared target-by-target reading, with raw and sifted dates."""
import collections
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
RUN=HERE/'haiku-date-arm-2026-10-29'
OUT=RUN/'analyst-read-v1.json'
# Records and content outcomes are from reading each source and the complete answer; matching is not keyword-based.
TARGETS={
 'memory_sk':('memory','unknown',{'control':[['e5'],['e6'],['e5']],'arm':[['e4'],['e3'],['e3']]}, {'control':['complete']*3,'arm':['complete']*3}),
 'amd_compare':('amd','unknown',{'control':[['e4'],['e3'],['e3','e4']],'arm':[['e4','e5'],['e3','e4'],['e3','e4']]}, {'control':['partial']*3,'arm':['partial']*3}),
 'growth_spend':('growth','unknown',{'control':[['e1'],['e1'],['e1']],'arm':[['e1'],['e1'],['e1']]}, {'control':['complete']*3,'arm':['complete']*3}),
 'growth_revenue':('growth','unknown',{'control':[['e2'],['e2'],['e2']],'arm':[['e2'],['e2'],['e2']]}, {'control':['partial','partial','error'],'arm':['partial','partial','error']}),
 'policy_treasury':('policy','2026-07-21',{'control':[['e2'],['e2'],['e3']],'arm':[['e3'],['e3'],['e3']]}, {'control':['complete']*3,'arm':['partial']*3}),
 'policy_adviser':('policy','2026-07-22',{'control':[['e6'],['e3'],['e4']],'arm':[['e4'],['e7'],['e4']]}, {'control':['complete']*3,'arm':['complete']*3}),
 'holdout_spending':('spending_holdout','unknown',{'control':[['e2'],['e2'],['ev2']],'arm':[['e3'],['e3'],['e2']]}, {'control':['partial']*3,'arm':['partial']*3}),
 'holdout_valar':('valar_holdout','2026-07-01',{'control':[['e1','e2','e3'],['e1','e2','e5'],['e1','e2']],'arm':[['e1','e2','e3'],['e1','e2','e3'],['e1','e2','e3']]}, {'control':['complete']*3,'arm':['complete']*3}),
 'holdout_deepseek':('deepseek_holdout','unknown',{'control':[['e1','e2','e7'],['e1','e2','e5'],['e1','e2','e3']],'arm':[['e1','e2'],['e1'],['e1']]}, {'control':['partial']*3,'arm':['partial']*3})}


def main():
 summary=json.loads((RUN/'run-summary.json').read_text());assert summary['sent']==summary['planned']==42 and not summary['not_sent']
 rows=[]
 for target,(name,expected,ids,grades) in TARGETS.items():
  for group in ('control','arm'):
   for idx in range(3):
    raw=json.loads((RUN/f'{name}-{group}-{idx+1}.json').read_text())
    assert raw['completed'] and not raw['schema_errors'] and 'sift' in raw
    rawmap={e['id']:e for e in raw['answer']['evidence']};keptmap={e['id']:e for e in raw['sift']['evidence']}
    records=[]
    for id in ids[group][idx]:
     assert id in rawmap and id in keptmap
     r=rawmap[id];k=keptmap[id]
     records.append({'id':id,'raw_day':r['original_day'],'kept_day':k['original_day'],'speaker':k['speaker'],
                     'original_who':k['original_who'],'summary':k['one_line'],'quote':k['quote']})
    values=[r['raw_day'] for r in records]
    if expected=='unknown':date='correct_unknown' if all(v=='' for v in values) else 'unsupported'
    else:date='correct_known' if all(v==expected for v in values) else 'missing_known' if all(v in ('',expected) for v in values) else 'unsupported'
    rows.append({'target':target,'article':name,'split':'test' if name.endswith('_holdout') else 'development',
                 'group':group,'sample':idx+1,'expected_day':expected,'date':date,
                 'content_and_quote':grades[group][idx], 'records':records})
 assert len(rows)==54
 result={'judgement':'Codex reading against registered source-backed target definitions; a model-authored analysis, not independent human gold.',
         'rows':rows,'limitations':['Date grade inspects raw values, with normalized values separately retained.',
          'Quote support is a semantic reading, with punctuation normalization by the production checker; literal punctuation differences are a separate issue.',
          'Selected cases and three samples each cannot establish a population rate.']}
 with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
 for split in ('development','test'):
  for group in ('control','arm'):
   x=[r for r in rows if r['split']==split and r['group']==group]
   print(split,group,'date',dict(collections.Counter(r['date'] for r in x)), 'content',dict(collections.Counter(r['content_and_quote'] for r in x)))

if __name__=='__main__':main()
