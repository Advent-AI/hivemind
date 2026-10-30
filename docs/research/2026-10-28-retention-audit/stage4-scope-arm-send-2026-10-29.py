"""Adapt the previously reviewed stage-4 sender to the frozen six-condition scope experiment."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
HERE=ROOT/'docs/research/2026-10-28-retention-audit'
RUN=HERE/'stage4-scope-arm-2026-10-29'
PREP=HERE/'stage4-scope-arm-prepare-2026-10-29.py'
SENDER=HERE/'stage4-haiku-luna-v3-send-v5-2026-10-29.py'
DESIGN=HERE/'stage4-scope-arm-design-v3-2026-10-29.md'
CAP=.60


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
if globals().get('__executed_sha256__')!=digest(Path(__file__)):raise ValueError('adapter must run verified bytes')


def load_verified(path,name):
    raw=path.read_bytes();sha=hashlib.sha256(raw).hexdigest()
    if sha!=digest(path):raise ValueError('dependency changed during load')
    namespace={'__name__':name,'__file__':str(path),'__executed_sha256__':sha}
    exec(compile(raw,str(path),'exec'),namespace)
    if sha!=digest(path):raise ValueError('dependency changed during import')
    return namespace


sender=load_verified(SENDER,'scope_sender')
prepare=load_verified(PREP,'scope_preparation')
if digest(Path(__file__))!=globals()['__executed_sha256__']:raise ValueError('adapter changed during imports')
sender['RUN']=RUN;sender['CONTRACT']=DESIGN;sender['COUNTS']='counts.json';sender['CAP']=CAP
original_dependencies=sender['dependency_hashes']


def dependencies():
    result=original_dependencies()
    for p in (Path(__file__),PREP,DESIGN):result[str(p.relative_to(ROOT))]=digest(p)
    return result


sender['dependency_hashes']=dependencies
sender['STARTUP_DEPENDENCIES']=dependencies()


def frozen_requests():
    manifest,cases=prepare['verify']();reqs={}
    for name,case in cases.items():
        luna,haiku=prepare['prior'].requests(case)
        for provider,expected in [('luna',luna),('haiku',haiku)]:
            actual=json.loads((RUN/(name+'-'+provider+'-request.json')).read_text())
            sender['check_wire'](actual,expected);reqs[(name,provider)]=expected
        if luna['messages']!=[{'role':'system','content':haiku['system']},*haiku['messages']]:raise ValueError('message mismatch')
        sender['check_wire'](luna['response_format']['json_schema']['schema'],haiku['output_config']['format']['schema'])
    if len(reqs)!=12 or len(cases)!=6:raise ValueError('wrong condition population')
    return manifest,cases,reqs


def check_counts(counts,reqs):
    fields={'rows','reserved_total_usd','cap_usd','runner_sha256','contract_sha256','dependencies','note'}
    if set(counts)!=fields or counts['cap_usd']!=CAP or counts['runner_sha256']!=digest(SENDER) or counts['contract_sha256']!=digest(DESIGN):raise ValueError('frozen sender or cap changed')
    if counts['dependencies']!=sender['STARTUP_DEPENDENCIES'] or dependencies()!=sender['STARTUP_DEPENDENCIES']:raise ValueError('frozen dependencies changed')
    rows=counts['rows'];keys={(r['case'],r['provider']) for r in rows}
    if len(rows)!=12 or keys!=set(reqs):raise ValueError('count population changed')
    for row in rows:
        key=(row['case'],row['provider'])
        if row!=sender['reservation'](*key,reqs[key],row['estimated_input_tokens']):raise ValueError('reservation changed')
    total=sum(r['reserved_usd_per_call']*3 for r in rows)
    if total!=counts['reserved_total_usd'] or total>CAP:raise ValueError('reservation exceeds cap or changed')


sender['frozen_requests']=frozen_requests;sender['check_counts']=check_counts


def count():
    manifest,cases,reqs=frozen_requests();sender['selftest']()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        rows=list(pool.map(lambda job:sender['count_one'](job,reqs),reqs))
    total=sum(r['reserved_usd_per_call']*3 for r in rows)
    data={'rows':rows,'reserved_total_usd':total,'cap_usd':CAP,'runner_sha256':digest(SENDER),
          'contract_sha256':digest(DESIGN),'dependencies':sender['STARTUP_DEPENDENCIES'],
          'note':'Conservative estimate; missing usage retains full reservation; not a provider-enforced cap.'}
    check_counts(data,reqs);sender['put']('counts.json',data)
    print('36 independent calls reserved $',round(total,6),flush=True)


def launch():
    sender['verify_counts']()
    if (RUN/'run-v5.pid').exists() or (RUN/'worker-v5.lock').exists():raise ValueError('already launched')
    bootstrap="import sys,hashlib,pathlib; p=sys.argv[1]; raw=pathlib.Path(p).read_bytes(); h=hashlib.sha256(raw).hexdigest(); sys.argv=[p,sys.argv[2]]; exec(compile(raw,p,'exec'),{'__name__':'__main__','__file__':p,'__executed_sha256__':h})"
    with (RUN/'run-v5.log').open('x') as log:
        p=subprocess.Popen([sys.executable,'-c',bootstrap,str(Path(__file__).resolve()),'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONPATH=str(ROOT/'src')))
    (RUN/'run-v5.pid').write_text(str(p.pid)+'\n');print('detached pid',p.pid)


if __name__=='__main__':{'verify':frozen_requests,'count':count,'launch':launch,'worker':sender['worker']}[sys.argv[1]]()
