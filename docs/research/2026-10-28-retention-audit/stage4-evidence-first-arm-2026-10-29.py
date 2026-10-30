"""Test a structured, source-quoted research judgement with the existing capped sender."""
import concurrent.futures
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
HERE=ROOT/'docs/research/2026-10-28-retention-audit'
RUN=HERE/'stage4-evidence-first-arm-2026-10-29'
DESIGN=HERE/'stage4-evidence-first-design-2026-10-29.md'
PREVIOUS=HERE/'stage4-fact-inference-arm-v4-2026-10-29.py'
SENDER=HERE/'stage4-haiku-luna-v3-send-v5-2026-10-29.py'
CAP=.60
ORDER=('science','sharon','nvidia','nn','corning')

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
if globals().get('__executed_sha256__')!=digest(Path(__file__)):
    raise ValueError('adapter must execute verified bytes')
raw=PREVIOUS.read_bytes();sha=hashlib.sha256(raw).hexdigest()
prev={'__name__':'evidence_previous','__file__':str(PREVIOUS),'__executed_sha256__':sha}
exec(compile(raw,str(PREVIOUS),'exec'),prev)
if sha!=digest(PREVIOUS):raise ValueError('dependency changed')
sender=prev['sender'];sender['RUN']=RUN;sender['CONTRACT']=DESIGN;sender['COUNTS']='counts.json';sender['CAP']=CAP
base_deps=sender['dependency_hashes']

def dependencies():
    d=base_deps()
    for p in (Path(__file__),DESIGN,PREVIOUS):d[str(p.relative_to(ROOT))]=digest(p)
    return d
sender['dependency_hashes']=dependencies;sender['STARTUP_DEPENDENCIES']=dependencies()

ENTRY={'type':'object','additionalProperties':False,
       'properties':{'source_id':{'type':'string','description':'Evidence id: incoming, item:eN, eN, or source_article.'},
                     'quote':{'type':'string','description':'A verbatim substring of that source text.'}},
       'required':['source_id','quote']}
JUDGEMENT={'type':'object','additionalProperties':False,
    'properties':{'source_quotes':{'type':'array','items':ENTRY,
                                   'description':'Exact source passages that ground the new investment judgement.'},
                  'investment_inference':{'type':'string','description':'The analyst investment view, including any reasoned inference.'},
                  'assumptions':{'type':'array','items':{'type':'string'},'description':'Unconfirmed conditions the investment view relies on.'},
                  'unknowns':{'type':'array','items':{'type':'string'},'description':'Material details not established by the sources.'}},
    'required':['source_quotes','investment_inference','assumptions','unknowns']}

def schema(request,provider):
    return request['output_config']['format']['schema'] if provider=='haiku' else request['response_format']['json_schema']['schema']

def refs(request,provider):
    message=request['messages'][0 if provider=='haiku' else 1]
    if message['role']!='user':raise ValueError('user input missing')
    u=json.loads(message['content']);out={'source_article':u['source_article']}
    for piece in [u['source_record'],*u['other_source_records'],*u['stored_pieces']]:
        ident=piece['id']
        if ident in out:raise ValueError('duplicate source identity '+ident)
        out[ident]=piece['quote']
    return out

base_originals=prev['originals']
def originals():
    oldcases,oldreqs=base_originals(); cases={};reqs={}
    for name in ORDER:
        metadata=copy.deepcopy(oldcases[name+'-control'])
        for arm in ('control','evidence'):
            case=name+'-'+arm; item=copy.deepcopy(metadata); item['experiment_arm']=arm
            for provider in ('luna','haiku'):
                control=copy.deepcopy(oldreqs[(name+'-control',provider)])
                if arm=='evidence':
                    if schema(control,provider)['properties']['independent_judgement']!={'type':'string'}:
                        raise ValueError('baseline judgement shape changed')
                    schema(control,provider)['properties']['independent_judgement']=copy.deepcopy(JUDGEMENT)
                reqs[(case,provider)]=control
            gpt,haiku=reqs[(case,'luna')],reqs[(case,'haiku')]
            if gpt['messages']!=[{'role':'system','content':haiku['system']},*haiku['messages']]:
                raise ValueError('provider messages differ')
            sender['check_wire'](schema(gpt,'luna'),schema(haiku,'haiku'))
            if refs(gpt,'luna')!=refs(haiku,'haiku'):raise ValueError('provider sources differ')
            item['reference_texts']=refs(haiku,'haiku')
            cases[case]=item
    if len(cases)!=10 or len(reqs)!=20:raise ValueError('case population changed')
    for name in ORDER:
        for provider in ('luna','haiku'):
            a=copy.deepcopy(reqs[(name+'-evidence',provider)])
            schema(a,provider)['properties']['independent_judgement']={'type':'string'}
            sender['check_wire'](a,reqs[(name+'-control',provider)])
    return cases,reqs

original_answer_checks=sender['prep'].answer_checks

def answer_checks(answer,case):
    if case.get('experiment_arm')!='evidence':
        return original_answer_checks(answer,case)
    if not isinstance(answer,dict) or not isinstance(answer.get('independent_judgement'),dict):
        return ['structured judgement missing'],[]
    judgement=answer['independent_judgement'];errors=[]
    if set(judgement)!={'source_quotes','investment_inference','assumptions','unknowns'}:
        return ['structured judgement keys differ'],[]
    compatible=copy.deepcopy(answer);compatible['independent_judgement']=judgement['investment_inference']
    base_errors,observations=original_answer_checks(compatible,case);errors.extend(base_errors)
    if not isinstance(judgement['source_quotes'],list) or not isinstance(judgement['assumptions'],list) or not isinstance(judgement['unknowns'],list):
        return errors+['structured judgement arrays missing'],observations
    if not all(isinstance(x,str) for x in judgement['assumptions']+judgement['unknowns']):
        errors.append('assumptions or unknowns are not text')
    if answer['action']=='propose_new' and (not judgement['source_quotes'] or not isinstance(judgement['investment_inference'],str) or not judgement['investment_inference'].strip()):
        errors.append('new question needs source quote and inference')
    for q in judgement['source_quotes']:
        if not isinstance(q,dict) or set(q)!={'source_id','quote'} or not isinstance(q['source_id'],str) or not isinstance(q['quote'],str):
            errors.append('invalid quotation structure');continue
        source=case['reference_texts'].get(q['source_id'])
        if not isinstance(source,str) or not q['quote'].strip() or q['quote'] not in source:
            errors.append('quotation not in identified source')
    return errors,observations

sender['prep'].answer_checks=answer_checks

def exercise_checks(cases):
    case=cases['nvidia-evidence'];old=HERE/'stage4-fact-inference-arm-v4-2026-10-29/nvidia-control-haiku-2.json'
    answer=json.loads(old.read_text())['answer'];source=case['reference_texts']['incoming']
    answer['independent_judgement']={'source_quotes':[{'source_id':'incoming','quote':source}],
        'investment_inference':'A conditional investor view.','assumptions':['Provider is unconfirmed.'],'unknowns':['Credit provider.']}
    errors,_=answer_checks(answer,case)
    if errors:raise ValueError('positive check failed: '+str(errors))
    mutants=[]
    a=copy.deepcopy(answer);a['independent_judgement']['source_quotes'][0]['source_id']='e999999';mutants.append(a)
    a=copy.deepcopy(answer);a['independent_judgement']['source_quotes'][0]['quote']='This sentence is absent.';mutants.append(a)
    a=copy.deepcopy(answer);a['independent_judgement']['source_quotes']=[];mutants.append(a)
    a=copy.deepcopy(answer);a['independent_judgement']['investment_inference']='';mutants.append(a)
    a=copy.deepcopy(answer);a['independent_judgement']['unknowns']='unknown';mutants.append(a)
    for mutant in mutants:
        if not answer_checks(mutant,case)[0]:raise ValueError('invalid source or shape accepted')
    print('evidence positive and five missing/false-source/shape controls passed',flush=True)

def prepare():
    cases,reqs=originals();exercise_checks(cases);RUN.mkdir(exist_ok=False)
    manifest={'cases':cases,'planned_calls':60,'samples':3,'cap_usd':CAP,
              'dependencies':dependencies(),'request_sha256':{}}
    for (case,provider),request in reqs.items():
        name=case+'-'+provider+'-request.json';sender['put'](name,request);manifest['request_sha256'][name]=digest(RUN/name)
    sender['put']('manifest.json',manifest);print('prepared 20 requests; source-read holdout first')

def frozen_requests():
    cases,reqs=originals();manifest=json.loads((RUN/'manifest.json').read_text())
    if manifest['cases']!=cases or manifest['planned_calls']!=60 or manifest['samples']!=3 or manifest['cap_usd']!=CAP or manifest['dependencies']!=dependencies():
        raise ValueError('manifest or dependencies changed')
    exercise_checks(cases)
    for (case,provider),request in reqs.items():
        name=case+'-'+provider+'-request.json'
        if digest(RUN/name)!=manifest['request_sha256'][name]:raise ValueError('request digest differs')
        sender['check_wire'](json.loads((RUN/name).read_text()),request)
    return manifest,cases,reqs

sender['frozen_requests']=frozen_requests
# The previously reviewed count function remains bound to sender globals and checks this arm's hashes.

def check_counts(counts,reqs):
    fields={'rows','reserved_total_usd','cap_usd','runner_sha256','contract_sha256','dependencies','note'}
    if set(counts)!=fields or counts['cap_usd']!=CAP or counts['runner_sha256']!=digest(SENDER) or counts['contract_sha256']!=digest(DESIGN):raise ValueError('reservation configuration changed')
    if counts['dependencies']!=sender['STARTUP_DEPENDENCIES'] or dependencies()!=sender['STARTUP_DEPENDENCIES']:raise ValueError('dependencies changed')
    rows=counts['rows']
    if len(rows)!=20 or {(r['case'],r['provider']) for r in rows}!=set(reqs):raise ValueError('reservation population changed')
    for row in rows:
        key=(row['case'],row['provider'])
        if row!=sender['reservation'](*key,reqs[key],row['estimated_input_tokens']):raise ValueError('reservation changed')
    total=sum(r['reserved_usd_per_call']*3 for r in rows)
    if total!=counts['reserved_total_usd'] or total>CAP:raise ValueError('reservation exceeds cap or differs')
sender['check_counts']=check_counts

def count():
    _,_,reqs=frozen_requests();sender['selftest']()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:rows=list(pool.map(lambda job:sender['count_one'](job,reqs),reqs))
    total=sum(r['reserved_usd_per_call']*3 for r in rows)
    data={'rows':rows,'reserved_total_usd':total,'cap_usd':CAP,'runner_sha256':digest(SENDER),'contract_sha256':digest(DESIGN),
          'dependencies':sender['STARTUP_DEPENDENCIES'],'note':'Conservative bound; not provider-enforced. Unknown usage retains reservation.'}
    check_counts(data,reqs);sender['put']('counts.json',data);print('reserved 60 calls $',round(total,6),flush=True)

def launch():
    sender['verify_counts']()
    if (RUN/'run-v5.pid').exists() or (RUN/'worker-v5.lock').exists():raise ValueError('already launched')
    bootstrap="import sys,hashlib,pathlib; p=sys.argv[1]; raw=pathlib.Path(p).read_bytes(); h=hashlib.sha256(raw).hexdigest(); sys.argv=[p,sys.argv[2]]; exec(compile(raw,p,'exec'),{'__name__':'__main__','__file__':p,'__executed_sha256__':h})"
    with (RUN/'run-v5.log').open('x') as log:
        proc=subprocess.Popen([sys.executable,'-c',bootstrap,str(Path(__file__).resolve()),'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONPATH=str(ROOT/'src')))
    (RUN/'run-v5.pid').write_text(str(proc.pid)+'\n');print('detached pid',proc.pid)

if __name__=='__main__':{'prepare':prepare,'verify':frozen_requests,'count':count,'launch':launch,'worker':sender['worker']}[sys.argv[1]]()
