"""Run the fixed pilot and, after its recorded reading, the fixed regressions."""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = HERE.parent / '2026-10-28-retention-audit'

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

provider = module('provider', OLD / 'haiku-extraction-probe-2026-10-29.py')
oldcheck = module('oldcheck', OLD / 'stage4-haiku-luna-v3-2026-10-29.py')
from hivemind import model

def read(name):
    return json.loads((HERE / name).read_text())

def put(name, value):
    with (HERE / name).open('x') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def domains(request):
    payload = json.loads(next(m['content'] for m in request['messages'] if m['role']=='user'))
    old = [r['id'] for r in payload['stored_pieces']]
    siblings = [r['id'] for r in payload.get('other_source_records', [])]
    questions = [r.get('id', r.get('view_id')) for r in payload['catalog']]
    return old, siblings, questions

def schema(request):
    return request['output_config']['format']['schema'] if request['model']=='claude-haiku-5-5' else request['response_format']['json_schema']['schema']

def check(answer, request, arm):
    old, siblings, questions = domains(request)
    errors = model.check_schema(answer, schema(request))
    if errors:
        return errors
    compared = [r['evidence_id'] for r in answer.get('comparisons', [])]
    if len(set(compared)) != len(compared):
        errors.append('One historical record received multiple relations')
    return errors

def validate_requests():
    plan = read('case-plan.json')
    assert len(plan['cases']) == len(set(plan['cases'])) == 10
    assert plan['planned_calls'] == 60 and plan['samples'] == 3
    for name in plan['cases']:
        a, b = read(name+'-control-request.json'), read(name+'-treatment-request.json')
        assert a['model'] == 'claude-haiku-5-5' and b['model'] == 'gpt-6-luna'
        assert a['max_tokens'] == b['max_completion_tokens'] == 6000
        assert a['output_config']['effort'] == b['reasoning_effort'] == 'medium'
        assert b['messages'] == [{'role':'system','content':a['system']},*a['messages']]
        assert schema(a) == schema(b)
        assert provider.previous.wire(schema(a)) == provider.previous.wire(schema(b))
        assert a['system'] == (HERE/'system.txt').read_text()
        old, siblings, questions = domains(b)
        props = schema(b)['properties']
        assert ('updates' in props) == bool(questions)
        assert ('comparisons' in props) == bool(old)
        sources = ['incoming'] + siblings + old
        pp = props['proposal']['anyOf'][1]['properties']
        assert pp['support_ids']['items']['enum'] == sources
        if old:
            assert props['comparisons']['items']['properties']['evidence_id']['enum'] == old
        if questions:
            arg = props['updates']['items']['properties']
            assert arg['question_id']['enum'] == questions
            for key in ('support_ids', 'opposing_ids'):
                assert arg[key]['items']['enum'] == sources

def freeze():
    validate_requests()
    counts = read('counts.json')
    assert len(counts['rows']) == 20
    assert counts['cap_usd'] == .60 and counts['combined_reserved_usd'] < .60
    assert counts['reserved_usd'] == sum(r['reserved_per_call']*3 for r in counts['rows'])
    for row in counts['rows']:
        assert digest(HERE/row['request']) == row['sha256']
    files = list(HERE.glob('*')) + list((ROOT/'src/hivemind').rglob('*.py'))
    files += list((ROOT/'src/hivemind/prompts').glob('*'))
    files += [OLD/'haiku-extraction-probe-2026-10-29.py', OLD/'deepseek-extraction-probe-2026-10-29.py',
              OLD/'stage4-haiku-luna-v3-2026-10-29.py', ROOT/'docs/research/2026-10-27-stage34-gold/run.py']
    put('manifest.json', {'files': {str(p):digest(p) for p in files if p.is_file()}, 'planned_calls':60})

def verify():
    for path, expected in read('manifest.json')['files'].items():
        assert digest(Path(path)) == expected, 'Frozen file changed: '+path

def worker(phase):
    verify()
    plan = read('case-plan.json')
    cases = plan['pilot'] if phase == 'pilot' else [n for n in plan['cases'] if n not in plan['pilot']]
    jobs = [(case,arm,draw) for draw in (1,2,3) for case in cases for arm in ('control','treatment')]
    rows = {r['request']:r for r in read('counts.json')['rows']}
    stop = threading.Event()
    start = time.monotonic()
    def one(job):
        case,arm,draw = job
        ident = f'{case}-{arm}-{draw}'
        if stop.is_set():
            return {'id':ident,'not_sent':True}
        filename = f'{case}-{arm}-request.json'
        request = read(filename)
        put(ident+'-attempt.json', {'request':filename,'sha256':rows[filename]['sha256']})
        before = time.monotonic()
        result = {'id':ident}
        try:
            if arm == 'control':
                response = provider.haiku_api('https://api.anthropic.com/v1/messages',request)
                result['completed'] = response.get('stop_reason') == 'end_turn'
                text = ''.join(c.get('text','') for c in response.get('content',[]) if c['type']=='text')
                usage = response['usage']
                used_input, used_output = usage['input_tokens'], usage['output_tokens']
            else:
                response = provider.previous.api('gpt','https://api.openai.com/v1/chat/completions',request)
                result['completed'] = response['choices'][0]['finish_reason']=='stop'
                text = response['choices'][0]['message'].get('content') or ''
                usage = response['usage']
                used_input, used_output = usage['prompt_tokens'], usage['completion_tokens']
            result['response'] = response
            result['answer'] = json.loads(text)
            result['errors'] = check(result['answer'], request, arm)
            assert 0 < used_input <= rows[filename]['input_bound']
            assert 0 < used_output <= rows[filename]['output_bound']
            if not result['completed']:
                stop.set()
        except Exception as error:
            result['error'] = type(error).__name__
            stop.set()
        result['seconds'] = round(time.monotonic()-before,2)
        put(ident+'-answer.json',result)
        print(ident,result.get('completed'),result.get('errors'),result.get('error'),flush=True)
        return {'id':ident,'completed':result.get('completed',False),'errors':result.get('errors'),'error':result.get('error')}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(one,jobs))
    verify()
    put(phase+'-summary.json', {'results':results,'status':'stopped' if stop.is_set() else 'completed',
                              'elapsed_seconds':time.monotonic()-start,'semantic_reading':'pending'})

def launch(phase):
    assert phase in ('pilot','regressions')
    verify()
    if phase == 'regressions':
        assessment = read('pilot-reading.json')
        assert assessment['proceed'] is True and read('pilot-summary.json')['status']=='completed'
        for ident, sha in assessment['answers'].items():
            assert digest(HERE/(ident+'-answer.json')) == sha
        assert len(assessment['answers']) == 12
    put(phase+'-launch.json', {'parent_pid':os.getpid()})
    with (HERE/(phase+'.log')).open('x') as log:
        process = subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'worker',phase],
            stdout=log,stderr=log,start_new_session=True,
            env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(ROOT/'src')))
    (HERE/(phase+'.pid')).write_text(str(process.pid)+'\n')
    print('Detached',phase,process.pid)

if __name__ == '__main__':
    command = sys.argv[1]
    if command=='freeze': freeze()
    elif command=='verify': verify()
    elif command=='worker': worker(sys.argv[2])
    elif command=='launch': launch(sys.argv[2])
