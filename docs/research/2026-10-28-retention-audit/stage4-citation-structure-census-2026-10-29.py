"""Enumerate argument citation fields in the stored step-4 samples; no semantic classification."""
import json
from pathlib import Path

HERE=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-retention-audit')
OLD=Path('/Users/lchingen/hivemind/poc/reports/2026-10-27-stage34-gold')
NEW=HERE/'stage4-haiku-luna-v3-2026-10-29'
OUT=HERE/'stage4-citation-structure-census-2026-10-29.json'


def classify(own,old_ids,arg):
    ids=arg['support_ids']+arg['opposing_ids']
    incoming=[x for x in ids if x=='incoming' or (own and x==own)]
    return {'incoming_reference':incoming,'same_article_reference':[x for x in ids if x.startswith('item:')],
            'incoming_id_collides_with_history':bool(own and own in old_ids),
            'ambiguous_incoming_reference':bool(own and own in old_ids and own in ids)}

if not classify('incoming',{'e1'},{'support_ids':['incoming'],'opposing_ids':[]})['incoming_reference']:
    raise ValueError('new-reference positive control failed')
if classify('incoming',{'e1'},{'support_ids':['e1'],'opposing_ids':[]})['incoming_reference']:
    raise ValueError('old-only negative control failed')
if not classify('e1',{'e1'},{'support_ids':['e1'],'opposing_ids':[]})['ambiguous_incoming_reference']:
    raise ValueError('collision positive control failed')

answers=[]
for arm in ('arm2','fresh2'):
    files=sorted((OLD/arm).glob('*.analyst.answer.json'))
    if not files:raise ValueError('missing historical answers')
    for f in files:
        req=f.with_name(f.name.replace('.answer.json','.request.json'))
        if not req.is_file():raise ValueError('missing request '+f.name)
        answer=json.loads(f.read_text());user=json.loads(req.read_text())['user']
        answers.append({'group':arm,'file':f.name,'answer':answer,'user':user})
summary=json.loads((NEW/'run-v5-summary.json').read_text())
if summary['attempted']!=30 or len(summary['samples'])!=30:raise ValueError('new sample population changed')
for s in summary['samples']:
    stem=f"{s['case']}-{s['provider']}-{s['sample']}";f=NEW/(stem+'.json');req=NEW/(f"{s['case']}-{s['provider']}-request.json")
    record=json.loads(f.read_text());request=json.loads(req.read_text())
    user=json.loads(next(m['content'] for m in request['messages'] if m['role']=='user'))
    answers.append({'group':'five_case','file':f.name,'answer':record['answer'],'user':user})

rows=[];counts={}
for r in answers:
    answer,user=r['answer'],r['user']
    if not isinstance(answer,dict) or 'arguments' not in answer or 'source_record' not in user or 'stored_pieces' not in user:
        raise ValueError('unidentifiable request or answer '+r['file'])
    own=user['source_record'].get('id');old_ids={x['id'] for x in user['stored_pieces']}
    c=counts.setdefault(r['group'],{'answers':0,'answers_with_incoming_id_collision':0,'arguments':0,
        'arguments_with_incoming_reference':0,'arguments_without_incoming_reference':0,'ambiguous_argument_references':0})
    c['answers']+=1;c['answers_with_incoming_id_collision']+=bool(own and own in old_ids)
    for arg in answer['arguments']:
        k=classify(own,old_ids,arg);c['arguments']+=1;c['arguments_with_incoming_reference']+=bool(k['incoming_reference'])
        c['arguments_without_incoming_reference']+=not bool(k['incoming_reference']);c['ambiguous_argument_references']+=k['ambiguous_incoming_reference']
        rows.append({'group':r['group'],'file':r['file'],'action':answer['action'],'question_id':arg['question_id'],
                     'incoming_id':own,'support_ids':arg['support_ids'],'opposing_ids':arg['opposing_ids'],**k})
known=[r for r in rows if r['group']=='five_case' and r['file']=='product_progress-haiku-1.json' and r['question_id']=='v11']
if len(known)!=1 or known[0]['incoming_reference'] or known[0]['same_article_reference']:
    raise ValueError('known Kyber control missing')
if len(answers)!=102 or len(rows)!=81:raise ValueError('stored population differs; investigate')
payload={'scope':'102 saved answers, 81 argument occurrences; repeated samples and multi-question arguments are not independent stories; no semantic correctness inferred',
         'counts':counts,'arguments':rows}
if OUT.exists():
    if json.loads(OUT.read_text())!=payload:raise ValueError('saved census differs; do not overwrite')
else:
    with OUT.open('x',encoding='utf-8') as f:json.dump(payload,f,ensure_ascii=False,indent=2);f.write('\n')
for key,value in counts.items():print(key,value)
