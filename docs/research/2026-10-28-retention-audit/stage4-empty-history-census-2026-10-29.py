"""Count historical-only relation ID refusals and replay the no-history transformation."""
import collections
import copy
import importlib.util
import json
from pathlib import Path

HERE=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-retention-audit')
OLD=Path('/Users/lchingen/hivemind/poc/reports/2026-10-27-stage34-gold')
OUT=HERE/'stage4-empty-history-census-2026-10-29.json'
RELATIONS=('same_claim_as','revises','opposes')
spec=importlib.util.spec_from_file_location('stage4',HERE/'stage4-haiku-luna-v3-2026-10-29.py')
stage4=importlib.util.module_from_spec(spec);spec.loader.exec_module(stage4)
counts=collections.Counter();violations=[];changed_content=0

def complete_relations(answer,ids):
    result=copy.deepcopy(answer)
    if not ids:
        for field in RELATIONS:
            result.pop(field)
        for field in RELATIONS:
            result[field]=[]
    return result

sample={'same_claim_as':['e7'],'revises':[],'opposes':[],'reason':'supported'}
if complete_relations(sample,{'e7'})!=sample or complete_relations(sample,set())['same_claim_as']:
    raise ValueError('history or no-history positive control failed')

def judge(group,name,answer,user,metadata=None):
    global changed_content
    ids={piece['id'] for piece in user['stored_pieces']}
    state='history' if ids else 'no_history';counts[(group,state,'answers')]+=1
    bad={field:[ident for ident in answer[field] if ident not in ids] for field in RELATIONS}
    bad={field:value for field,value in bad.items() if value}
    if not ids:
        transformed=complete_relations(answer,ids)
        if {k:v for k,v in transformed.items() if k not in RELATIONS}!={k:v for k,v in answer.items() if k not in RELATIONS}:
            changed_content+=1
        if not bad and any(answer[field] for field in RELATIONS):raise ValueError('valid historical relation without history')
    if bad:
        counts[(group,state,'invalid_relation_answers')]+=1
        if metadata is None or ids:raise ValueError('unexpected violation outside the observed class')
        before=copy.deepcopy(answer);after=copy.deepcopy(transformed)
        for value in (before,after):
            if isinstance(value['independent_judgement'],dict):
                value['independent_judgement']=value['independent_judgement']['investment_inference']
        before_errors=stage4.answer_checks(before,metadata)[0];after_errors=stage4.answer_checks(after,metadata)[0]
        if not before_errors or after_errors:raise ValueError('stored replay did not flip precisely: '+name+' '+str(after_errors))
        violations.append({'group':group,'sample':name,'invalid_relations':bad,'before_errors':before_errors,'after_errors':after_errors})

for group in ('arm2','fresh2'):
    for path in sorted((OLD/group).glob('*.analyst.answer.json')):
        answer=json.loads(path.read_text());request=json.loads(path.with_name(path.name.replace('.answer.json','.request.json')).read_text())
        judge(group,path.name,answer,request['user'])
for group in ('stage4-haiku-luna-v3-2026-10-29','stage4-scope-arm-2026-10-29','stage4-fact-inference-arm-v4-2026-10-29','stage4-evidence-first-arm-2026-10-29'):
    directory=HERE/group;summary=json.loads((directory/'run-v5-summary.json').read_text());manifest=json.loads((directory/'manifest.json').read_text())
    for sample in summary['samples']:
        stem=f"{sample['case']}-{sample['provider']}-{sample['sample']}";answer=json.loads((directory/(stem+'.json')).read_text())['answer']
        request=json.loads((directory/(sample['case']+'-'+sample['provider']+'-request.json')).read_text())
        user=json.loads(next(m['content'] for m in request['messages'] if m['role']=='user'))
        judge(group,stem,answer,user,manifest['cases'][sample['case']])
if sum(v for (g,s,k),v in counts.items() if k=='answers')!=182 or len(violations)!=7 or changed_content:
    raise ValueError('population or control differs')
if not any(v['sample']=='science-control-luna-1' for v in violations):raise ValueError('known refusal missing')
output={'scope':'182 saved research answers; repeated sends are not independent stories. Replacing no-history relation values on stored copies proves code handling only, not future model quality.',
        'counts':[{'group':g,'history_state':s,'kind':k,'count':v} for (g,s,k),v in sorted(counts.items())],
        'changed_non_relation_values':changed_content,'violations':violations}
if OUT.exists():
    if json.loads(OUT.read_text())!=output:raise ValueError('saved results changed; no overwrite')
else:
    with OUT.open('x',encoding='utf-8') as f:json.dump(output,f,ensure_ascii=False,indent=2);f.write('\n')
print('Judged 182 answers; 87 with no historical pieces, 95 with history; 7 invalid relation answers replayed, 0 other answer fields changed.')
