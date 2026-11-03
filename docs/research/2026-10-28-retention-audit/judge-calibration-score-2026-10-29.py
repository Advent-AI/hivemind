"""Compare three blind semantic reviews with ten prewritten development expectations."""
import copy, hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
HASHES={'judge-calibration-input-2026-10-29.json':'4518e79bb8c09583ed62f2567f1bce8322a358a9283a6846fa66f16ef4eef150',
        'judge-calibration-expected-2026-10-29.json':'ab6c38243c8d3ec36f7052d988b0a23227b48ea3a7d151eb7343f6392ca6614a'}

def score(expected, answer):
    labels={x['id']:x for x in expected}; rows=answer['cases']
    assert len(labels)==len(expected)==10 and len(rows)==10
    assert {x['id'] for x in rows}==set(labels) and len({x['id'] for x in rows})==10
    details=[]
    for row in rows:
        assert row['faithful'] in ('yes','no','uncertain') and row['citation_supported'] in ('yes','no','uncertain') and row['reason']
        label=labels[row['id']]
        meaning=row['faithful']==('yes' if label['source_meaning_preserved'] else 'no')
        citation=row['citation_supported']==('yes' if label['citations_support_entire_statement'] else 'no')
        details.append({'id':row['id'],'meaning_correct':meaning,'citation_correct':citation})
    return {'cases_judged':10,'both_correct':sum(x['meaning_correct'] and x['citation_correct'] for x in details),
            'fields_correct':sum(x['meaning_correct']+x['citation_correct'] for x in details),'details':details}

def main():
    for filename,sha in HASHES.items():assert hashlib.sha256((HERE/filename).read_bytes()).hexdigest()==sha
    expected=json.loads((HERE/'judge-calibration-expected-2026-10-29.json').read_text())['cases']
    inputs=json.loads((HERE/'judge-calibration-input-2026-10-29.json').read_text())
    assert {x['id'] for x in inputs['cases']}=={x['id'] for x in expected}
    results=[]
    for sample in (1,2,3):
        answer=json.loads((HERE/f'judge-calibration-result-{sample}-2026-10-29.json').read_text())
        result=score(expected,answer);results.append({'sample':sample,**result})
        mutant=copy.deepcopy(answer);mutant['cases'][0]['faithful']='no' if mutant['cases'][0]['faithful']=='yes' else 'yes'
        assert score(expected,mutant)['fields_correct'] < result['fields_correct']
        mutant=copy.deepcopy(answer);mutant['cases'].pop()
        try:score(expected,mutant)
        except AssertionError:pass
        else:raise AssertionError('missing case was not caught')
    output={'scope':'prewritten development calibration; original sources and synthetic statements; not investment relevance, not product, not unseen',
            'judge':'gpt-6.1-terra, three independent read-only sessions', 'results':results, 'mutant_controls_passed':True}
    with (HERE/'judge-calibration-score-2026-10-29.json').open('x') as f:json.dump(output,f,ensure_ascii=False,indent=2);f.write('\n')
    for r in results:print('sample',r['sample'],'both fields',r['both_correct'],'/ 10','fields',r['fields_correct'],'/ 20')
if __name__=='__main__':main()
