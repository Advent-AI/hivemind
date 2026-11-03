"""Test deterministic empty historical relations with the reviewed capped sender."""
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
RUN=HERE/'stage4-empty-history-arm-v3-2026-10-29'
DESIGN=HERE/'stage4-empty-history-design-v3-2026-10-29.md'
PREVIOUS=HERE/'stage4-fact-inference-arm-v4-2026-10-29.py'
SENDER=HERE/'stage4-haiku-luna-v3-send-v5-2026-10-29.py'
CAP=.60
RELATIONS=('same_claim_as','revises','opposes')
CASES={'valar':('stage4-empty-history-valar-source-2026-10-29','valar'),
       'sharon':('stage4-haiku-luna-v3-2026-10-29','sharon'),
       'science':('stage4-fact-inference-science-source-2026-10-29','science'),
       'nn':('stage4-scope-arm-2026-10-29','nn-scope')}

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
if globals().get('__executed_sha256__')!=digest(Path(__file__)):raise ValueError('adapter must execute verified bytes')
raw=PREVIOUS.read_bytes();sha=hashlib.sha256(raw).hexdigest();prev={'__name__':'empty_history_previous','__file__':str(PREVIOUS),'__executed_sha256__':sha}
exec(compile(raw,str(PREVIOUS),'exec'),prev)
if sha!=digest(PREVIOUS):raise ValueError('dependency changed')
sender=prev['sender'];sender['RUN']=RUN;sender['CONTRACT']=DESIGN;sender['COUNTS']='counts.json';sender['CAP']=CAP
base_deps=sender['dependency_hashes']

def dependencies():
    d=base_deps()
    paths=[Path(__file__),DESIGN,PREVIOUS,HERE/'stage4-empty-history-census-2026-10-29.py',
           HERE/'stage4-empty-history-valar-reference-2026-10-29.md',HERE/'stage4-empty-history-valar-prepare-2026-10-29.py']
    for directory,name in CASES.values():
        paths.append(HERE/directory/'manifest.json')
        paths.extend(HERE/directory/(name+'-'+provider+'-request.json') for provider in ('luna','haiku'))
    for p in paths:d[str(p.relative_to(ROOT))]=digest(p)
    return d
sender['dependency_hashes']=dependencies;sender['STARTUP_DEPENDENCIES']=dependencies()

def schema(request,provider):
    return request['output_config']['format']['schema'] if provider=='haiku' else request['response_format']['json_schema']['schema']

def remove_relations(req,provider):
    s=schema(req,provider)
    for field in RELATIONS:
        if field not in s['properties'] or field not in s['required']:raise ValueError('relation not in base schema')
        del s['properties'][field];s['required'].remove(field)

def complete(answer):
    result=copy.deepcopy(answer)
    if any(field in result for field in RELATIONS):raise ValueError('model returned a forbidden relation field')
    for field in RELATIONS:result[field]=[]
    return result

def originals():
    cases,reqs={},{}
    for name,(directory,source_name) in CASES.items():
        src=HERE/directory;manifest=json.loads((src/'manifest.json').read_text());metadata=copy.deepcopy(manifest['cases'][source_name]);metadata['source_split']=metadata['split'];metadata['split']='holdout' if name=='valar' else 'development'
        for arm in ('control','elide'):
            key=name+'-'+arm;case=copy.deepcopy(metadata);case['experiment_arm']=arm;cases[key]=case
            for provider in ('luna','haiku'):
                path=src/(source_name+'-'+provider+'-request.json')
                if digest(path)!=metadata['request_hashes'][provider]:raise ValueError('original request differs from manifest')
                req=json.loads(path.read_text())
                if arm=='elide' and not metadata['old_ids']:remove_relations(req,provider)
                reqs[(key,provider)]=req
            gpt,haiku=reqs[(key,'luna')],reqs[(key,'haiku')]
            if gpt['messages']!=[{'role':'system','content':haiku['system']},*haiku['messages']]:raise ValueError('provider messages differ')
            sender['check_wire'](schema(gpt,'luna'),schema(haiku,'haiku'))
        for provider in ('luna','haiku'):
            expected=copy.deepcopy(reqs[(name+'-control',provider)])
            if not metadata['old_ids']:remove_relations(expected,provider)
            sender['check_wire'](expected,reqs[(name+'-elide',provider)])
    if len(cases)!=8 or len(reqs)!=16 or not cases['sharon-elide']['old_ids'] or cases['valar-elide']['old_ids']:
        raise ValueError('case population or history control changed')
    return cases,reqs

base_checks=sender['prep'].answer_checks

def answer_checks(answer,case):
    if case.get('experiment_arm')=='elide' and not case['old_ids']:
        if not isinstance(answer,dict):return ['answer is not an object'],[]
        try:answer=complete(answer)
        except ValueError:return ['forbidden historical relation in model output'],[]
    return base_checks(answer,case)
sender['prep'].answer_checks=answer_checks
base_parse=sender['parse_response']

def parse_response(response,provider,case):
    result=base_parse(response,provider,case)
    if case.get('experiment_arm')=='elide' and not case['old_ids'] and isinstance(result.get('answer'),dict):
        result['model_answer']=copy.deepcopy(result['answer'])
        try:result['answer']=complete(result['answer'])
        except ValueError:pass
    return result
sender['parse_response']=parse_response
base_stop=sender['should_stop']

def should_stop(record,provider,row):
    if not base_stop(record,provider,row):return False
    name=row.get('case','')
    if not name.endswith('-control') or record.get('error') or not record.get('provider_complete') or not sender['usage_ok'](record.get('response'),provider,row):return True
    answer=record.get('answer');errors=record.get('structural_errors')
    if not isinstance(answer,dict) or not isinstance(errors,list) or not errors:return True
    source_name=name.removesuffix('-control')
    if source_name not in CASES:return True
    directory,source=CASES[source_name]
    meta=json.loads((HERE/directory/'manifest.json').read_text())['cases'][source]
    if meta['old_ids']:return True
    allowed=set(meta['item_ids']);expected=[]
    for field in RELATIONS:
        values=answer.get(field)
        if not isinstance(values,list) or any(not isinstance(ident,str) for ident in values):return True
        for ident in values:
            if ident not in allowed:return True
            expected.append(field+': not a historical evidence id '+ident)
    return not expected or errors!=expected
sender['should_stop']=should_stop

def exercise_checks(cases):
    p=HERE/'stage4-evidence-first-arm-2026-10-29/science-control-haiku-1.json';original=json.loads(p.read_text())['answer'];model_answer={k:v for k,v in original.items() if k not in RELATIONS};case=cases['science-elide']
    errors,_=answer_checks(model_answer,case)
    if errors or complete(model_answer)!=original:raise ValueError('empty-history positive failed')
    mutant=copy.deepcopy(model_answer);mutant['same_claim_as']=['item:e1']
    if not answer_checks(mutant,case)[0]:raise ValueError('forbidden relation not rejected')
    mutant=copy.deepcopy(model_answer);del mutant['reason']
    if not answer_checks(mutant,case)[0]:raise ValueError('missing old field not rejected')
    history=cases['sharon-elide'];sample=json.loads((HERE/'stage4-haiku-luna-v3-2026-10-29/sharon-haiku-1.json').read_text())['answer']
    if answer_checks(sample,history)[0]:raise ValueError('historical positive failed')
    print('empty/history positives and two negative controls passed',flush=True)

def prepare():
    cases,reqs=originals();exercise_checks(cases);RUN.mkdir(exist_ok=False)
    manifest={'cases':cases,'planned_calls':48,'samples':3,'cap_usd':CAP,'dependencies':dependencies(),'request_sha256':{}}
    for (case,provider),request in reqs.items():
        name=case+'-'+provider+'-request.json';sender['put'](name,request);manifest['request_sha256'][name]=digest(RUN/name)
    sender['put']('manifest.json',manifest);print('prepared 16 requests; holdout and historical control first')

def frozen_requests():
    cases,reqs=originals();manifest=json.loads((RUN/'manifest.json').read_text())
    if list(manifest['cases'])!=list(cases):raise ValueError('frozen case order changed')
    if manifest['cases']!=cases or manifest['planned_calls']!=48 or manifest['samples']!=3 or manifest['cap_usd']!=CAP or manifest['dependencies']!=dependencies():raise ValueError('manifest or dependencies changed')
    exercise_checks(cases)
    for (case,provider),request in reqs.items():
        name=case+'-'+provider+'-request.json'
        if digest(RUN/name)!=manifest['request_sha256'][name]:raise ValueError('request digest differs')
        sender['check_wire'](json.loads((RUN/name).read_text()),request)
    return manifest,cases,reqs
sender['frozen_requests']=frozen_requests

def check_counts(counts,reqs):
    fields={'rows','reserved_total_usd','cap_usd','runner_sha256','contract_sha256','dependencies','note'}
    if set(counts)!=fields or counts['cap_usd']!=CAP or counts['runner_sha256']!=digest(SENDER) or counts['contract_sha256']!=digest(DESIGN):raise ValueError('reservation configuration changed')
    if counts['dependencies']!=sender['STARTUP_DEPENDENCIES'] or dependencies()!=sender['STARTUP_DEPENDENCIES']:raise ValueError('dependencies changed')
    rows=counts['rows']
    if len(rows)!=16 or {(r['case'],r['provider']) for r in rows}!=set(reqs):raise ValueError('reservation population changed')
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
    check_counts(data,reqs);sender['put']('counts.json',data);print('reserved 48 calls $',round(total,6),flush=True)

def launch():
    sender['verify_counts']()
    if (RUN/'run-v5.pid').exists() or (RUN/'worker-v5.lock').exists():raise ValueError('already launched')
    bootstrap="import sys,hashlib,pathlib; p=sys.argv[1]; raw=pathlib.Path(p).read_bytes(); h=hashlib.sha256(raw).hexdigest(); sys.argv=[p,sys.argv[2]]; exec(compile(raw,p,'exec'),{'__name__':'__main__','__file__':p,'__executed_sha256__':h})"
    with (RUN/'run-v5.log').open('x') as log:
        proc=subprocess.Popen([sys.executable,'-c',bootstrap,str(Path(__file__).resolve()),'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONPATH=str(ROOT/'src')))
    (RUN/'run-v5.pid').write_text(str(proc.pid)+'\n');print('detached pid',proc.pid)

if __name__=='__main__':{'prepare':prepare,'verify':frozen_requests,'count':count,'launch':launch,'worker':sender['worker']}[sys.argv[1]]()
