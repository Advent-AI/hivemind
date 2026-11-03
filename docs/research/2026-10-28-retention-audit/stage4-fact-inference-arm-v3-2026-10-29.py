"""Freeze and send a paired fourth-step prompt comparison using the reviewed sender."""
import concurrent.futures
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
HERE = ROOT / 'docs/research/2026-10-28-retention-audit'
RUN = HERE / 'stage4-fact-inference-arm-v3-2026-10-29'
SENDER = HERE / 'stage4-haiku-luna-v3-send-v5-2026-10-29.py'
DESIGN = HERE / 'stage4-fact-inference-arm-v3-2026-10-29.md'
CAP = .60
CASES = {'nvidia': ('stage4-scope-arm-2026-10-29', 'nvidia-scope'),
         'nn': ('stage4-scope-arm-2026-10-29', 'nn-scope'),
         'corning': ('stage4-scope-arm-2026-10-29', 'corning-scope'),
         'sharon': ('stage4-haiku-luna-v3-2026-10-29', 'sharon')}
REPLACEMENTS = [('Keep conditions and periods exactly as the texts state them.',
                 'Separate source facts, inference and unknowns; preserve conditions and periods.'),
                ('Comparison opinions are hints with scores; the texts decide.', 'Comparison opinions are hints; texts decide.'),
                ('The argument is the deliverable.', 'The argument is the output.')]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

if globals().get('__executed_sha256__') != digest(Path(__file__)):
    raise ValueError('adapter must run verified bytes')
raw = SENDER.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
sender = {'__name__': 'fact_inference_sender', '__file__': str(SENDER), '__executed_sha256__': sha}
exec(compile(raw, str(SENDER), 'exec'), sender)
if sha != digest(SENDER):
    raise ValueError('sender changed while loading')
sender['RUN'] = RUN
sender['CONTRACT'] = DESIGN
sender['COUNTS'] = 'counts.json'
sender['CAP'] = CAP
base_dependencies = sender['dependency_hashes']

def dependencies():
    result = base_dependencies()
    paths = [Path(__file__), DESIGN]
    for directory, name in CASES.values():
        paths.append(HERE / directory / 'manifest.json')
        paths.extend(HERE / directory / (name + '-' + provider + '-request.json') for provider in ('luna', 'haiku'))
    for path in paths:
        result[str(path.relative_to(ROOT))] = digest(path)
    return result

sender['dependency_hashes'] = dependencies
sender['STARTUP_DEPENDENCIES'] = dependencies()

def revised(text):
    original = text
    for before, after in REPLACEMENTS:
        if text.count(before) != 1:
            raise ValueError('prompt segment missing or ambiguous')
        text = text.replace(before, after, 1)
    if len(text) > len(original):
        raise ValueError('system prompt grew')
    return text

def originals():
    cases, requests = {}, {}
    for name, (directory, source_name) in CASES.items():
        source = HERE / directory
        manifest = json.loads((source / 'manifest.json').read_text())
        metadata = copy.deepcopy(manifest['cases'][source_name])
        metadata['source_split'] = metadata['split']
        metadata['split'] = 'development'
        for provider in ('luna', 'haiku'):
            path = source / (source_name + '-' + provider + '-request.json')
            if digest(path) != metadata['request_hashes'][provider]:
                raise ValueError('original request differs from frozen manifest')
            control = json.loads(path.read_text())
            treatment = copy.deepcopy(control)
            if provider == 'haiku':
                control_system = control['system']
                treatment['system'] = revised(control_system)
            else:
                control_system = control['messages'][0]['content']
                if control['messages'][0]['role'] != 'system':
                    raise ValueError('missing system message')
                treatment['messages'][0]['content'] = revised(control_system)
            cases[name + '-control'] = metadata
            cases[name + '-separate'] = metadata
            requests[(name + '-control', provider)] = control
            requests[(name + '-separate', provider)] = treatment
        for arm in ('control', 'separate'):
            gpt, haiku = requests[(name+'-'+arm, 'luna')], requests[(name+'-'+arm, 'haiku')]
            if gpt['messages'] != [{'role': 'system', 'content': haiku['system']}, *haiku['messages']]:
                raise ValueError('provider messages differ')
            sender['check_wire'](gpt['response_format']['json_schema']['schema'], haiku['output_config']['format']['schema'])
    if len(cases) != 8 or len(requests) != 16:
        raise ValueError('case population changed')
    return cases, requests

def prepare():
    cases, reqs = originals()
    RUN.mkdir(exist_ok=False)
    manifest = {'cases': cases, 'planned_calls': 48, 'samples': 3, 'cap_usd': CAP,
                'dependencies': dependencies(), 'request_sha256': {}}
    for (case, provider), request in reqs.items():
        filename = case + '-' + provider + '-request.json'
        sender['put'](filename, request)
        manifest['request_sha256'][filename] = digest(RUN / filename)
    sender['put']('manifest.json', manifest)
    print('prepared', len(reqs), 'requests; system chars', len(reqs[('nvidia-control','haiku')]['system']), 'to', len(reqs[('nvidia-separate','haiku')]['system']))

def frozen_requests():
    cases, reqs = originals()
    manifest = json.loads((RUN/'manifest.json').read_text())
    if manifest['cases'] != cases or manifest['planned_calls'] != 48 or manifest['samples'] != 3 or manifest['cap_usd'] != CAP or manifest['dependencies'] != dependencies():
        raise ValueError('manifest or dependencies changed')
    for (case, provider), request in reqs.items():
        filename = case + '-' + provider + '-request.json'
        if digest(RUN/filename) != manifest['request_sha256'][filename]:
            raise ValueError('request digest differs')
        sender['check_wire'](json.loads((RUN/filename).read_text()), request)
    return manifest, cases, reqs

def check_counts(counts, reqs):
    fields = {'rows','reserved_total_usd','cap_usd','runner_sha256','contract_sha256','dependencies','note'}
    if set(counts) != fields or counts['cap_usd'] != CAP or counts['runner_sha256'] != digest(SENDER) or counts['contract_sha256'] != digest(DESIGN):
        raise ValueError('reservation configuration changed')
    if counts['dependencies'] != sender['STARTUP_DEPENDENCIES'] or dependencies() != sender['STARTUP_DEPENDENCIES']:
        raise ValueError('dependencies changed')
    rows = counts['rows']
    if len(rows) != 16 or {(x['case'],x['provider']) for x in rows} != set(reqs):
        raise ValueError('reservation population changed')
    for row in rows:
        key = (row['case'], row['provider'])
        if row != sender['reservation'](*key, reqs[key], row['estimated_input_tokens']):
            raise ValueError('reservation changed')
    total = sum(row['reserved_usd_per_call'] * 3 for row in rows)
    if total != counts['reserved_total_usd'] or total > CAP:
        raise ValueError('reservation exceeds cap or differs')

sender['frozen_requests'] = frozen_requests
sender['check_counts'] = check_counts

def count():
    _, _, reqs = frozen_requests()
    sender['selftest']()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(lambda job: sender['count_one'](job, reqs), reqs))
    total = sum(row['reserved_usd_per_call'] * 3 for row in rows)
    data = {'rows': rows, 'reserved_total_usd': total, 'cap_usd': CAP, 'runner_sha256': digest(SENDER),
            'contract_sha256': digest(DESIGN), 'dependencies': sender['STARTUP_DEPENDENCIES'],
            'note': 'Conservative bound; not provider-enforced. Unknown usage retains reservation.'}
    check_counts(data, reqs)
    sender['put']('counts.json', data)
    print('reserved 48 calls $', round(total, 6), flush=True)

def launch():
    sender['verify_counts']()
    if (RUN/'run-v5.pid').exists() or (RUN/'worker-v5.lock').exists():
        raise ValueError('already launched')
    bootstrap = "import sys,hashlib,pathlib; p=sys.argv[1]; raw=pathlib.Path(p).read_bytes(); h=hashlib.sha256(raw).hexdigest(); sys.argv=[p,sys.argv[2]]; exec(compile(raw,p,'exec'),{'__name__':'__main__','__file__':p,'__executed_sha256__':h})"
    with (RUN/'run-v5.log').open('x') as log:
        proc = subprocess.Popen([sys.executable, '-c', bootstrap, str(Path(__file__).resolve()), 'worker'], stdout=log, stderr=log, start_new_session=True, env=dict(os.environ, PYTHONPATH=str(ROOT/'src')))
    (RUN/'run-v5.pid').write_text(str(proc.pid) + '\n')
    print('detached pid', proc.pid)

if __name__ == '__main__':
    {'prepare': prepare, 'verify': frozen_requests, 'count': count, 'launch': launch, 'worker': sender['worker']}[sys.argv[1]]()
