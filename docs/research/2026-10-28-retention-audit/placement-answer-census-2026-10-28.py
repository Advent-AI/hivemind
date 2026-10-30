"""Count incomplete placement answers in the stored v38 week, by statement ID."""
import collections, copy, json, re, sqlite3
from pathlib import Path
HERE = Path(__file__).resolve().parent
ARCHIVE = '/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/archive.sqlite'

def inspect(user, answer):
    questions, statements=user.split('\n\n[Statements]\n',1)
    expected=re.findall(r'^  - (e\d+) \[',statements,re.M)
    assert expected and len(expected)==len(set(expected))
    allowed=set(re.findall(r'^  - (v\d+) \(',questions,re.M))
    received=[p['id'] for p in answer['placements']]
    return {'missing':sorted(set(expected)-set(received)), 'extra':sorted(set(received)-set(expected)),
            'duplicate':sorted(k for k,n in collections.Counter(received).items() if n>1),
            'unknown_links':[{'id':p['id'],'links':sorted(set(p['links'])-allowed)}
                             for p in answer['placements'] if set(p['links'])-allowed]}

def main():
    conn=sqlite3.connect('file:'+ARCHIVE+'?mode=ro',uri=True); counts=collections.Counter(); cases=[]; good=None
    for call_id,request,answer in conn.execute("select call_id,request_json,answer_json from model_calls where purpose='place' and request_sha256 not like '%:%'"):
        user=json.loads(request)['messages'][1]['content']; data=json.loads(answer); issues=inspect(user,data)
        counts['calls']+=1; counts['statements']+=len(re.findall(r'^  - (e\d+) \[',user.split('\n\n[Statements]\n',1)[1],re.M))
        if any(issues.values()):
            cases.append({'call_id':call_id,'item':user.splitlines()[0],'issues':issues,
                          'missing_statement_lines':[x for x in user.splitlines() if any(x.startswith('  - '+k+' [') for k in issues['missing'])]})
        elif data['placements'] and good is None: good=(user,data)
    assert counts['calls']==95 and counts['statements']==831
    assert len(cases)==1 and cases[0]['call_id']==386 and cases[0]['issues']['missing']==['e5']
    assert good and not any(inspect(*good).values())
    mutant=copy.deepcopy(good[1]); removed=mutant['placements'].pop(); assert removed['id'] in inspect(good[0],mutant)['missing']
    duplicate=copy.deepcopy(good[1]);duplicate['placements'].append(copy.deepcopy(duplicate['placements'][0]));assert inspect(good[0],duplicate)['duplicate']
    out={'scope':'v38 archived placement responses, production historical week','counts':dict(counts),'calls_with_invalid_coverage':len(cases),
         'cases':cases,'removed_and_duplicate_mutants_detected':True,'meaning':'Production code treats a missing id as no links; this is not a model decision to reject.'}
    with (HERE/'placement-answer-census-2026-10-28.json').open('x') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'},ensure_ascii=False))
if __name__=='__main__':main()
