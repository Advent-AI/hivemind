"""Run one frozen comparison using the existing provider and structural checker."""
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


probe = module('provider_probe', OLD / 'haiku-extraction-probe-2026-10-29.py')
checker = module('existing_checker', OLD / 'stage4-haiku-luna-v3-2026-10-29.py')


def read(name):
    return json.loads((HERE / name).read_text())


def put(name, value):
    with (HERE / name).open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def case_for(request):
    payload = json.loads(request['messages'][0]['content'])
    return {'old_ids': [x['id'] for x in payload['stored_pieces']],
            'item_ids': [x['id'] for x in payload.get('other_source_records', [])],
            'question_ids': [x.get('id', x.get('view_id')) for x in payload['catalog']]}


def validate_pair(a, b):
    assert a['model'] == b['model'] == 'claude-haiku-5-5'
    assert a['max_tokens'] == b['max_tokens'] == 6000
    assert a['messages'] == b['messages']
    assert a['output_config']['effort'] == b['output_config']['effort'] == 'medium'
    sa = a['output_config']['format']['schema']
    sb = b['output_config']['format']['schema']
    # Required-field order changes generation order, not schema acceptance.
    assert dict(sa, required=sorted(sa['required'])) == dict(sb, required=sorted(sb['required']))
    assert next(iter(sa['properties'])) == 'action'
    assert list(sb['properties'])[-1] == 'action'
    assert a['system'] == (HERE / 'control-system.txt').read_text()
    assert b['system'] == (HERE / 'treatment-system.txt').read_text()


def freeze():
    counts = read('counts.json')
    plan = read('case-plan.json')
    assert len(plan['cases']) == len(set(plan['cases'])) == 8 and plan['samples'] == 3
    assert len(counts['rows']) == 16 and counts['cap_usd'] == .60
    assert sum(r['reserved_per_call'] * 3 for r in counts['rows']) == counts['reserved_usd']
    assert counts['reserved_usd'] + counts['diagnostic_reserved_usd'] == counts['total_reserved_usd'] < .60
    expected = {name + '-' + arm + '-request.json' for name in plan['cases'] for arm in ('control', 'treatment')}
    assert {r['request'] for r in counts['rows']} == expected
    for row in counts['rows']:
        assert digest(HERE / row['request']) == row['sha256']
    for name in plan['cases']:
        validate_pair(read(name + '-control-request.json'), read(name + '-treatment-request.json'))
    paths = list(HERE.glob('*')) + list((ROOT / 'src/hivemind').rglob('*.py'))
    paths += list((ROOT / 'src/hivemind/prompts').glob('*'))
    paths += [OLD / 'haiku-extraction-probe-2026-10-29.py', OLD / 'deepseek-extraction-probe-2026-10-29.py', OLD / 'stage4-haiku-luna-v3-2026-10-29.py', ROOT / 'docs/research/2026-10-27-stage34-gold/run.py']
    put('manifest.json', {'files': {str(p): digest(p) for p in paths if p.is_file()}, 'planned_calls': 48})


def verify():
    for path, sha in read('manifest.json')['files'].items():
        assert digest(Path(path)) == sha, 'Frozen file changed: ' + path


def worker():
    verify()
    started = time.monotonic()
    put('started.json', {'pid': os.getpid()})
    stop = threading.Event()
    rows = {r['request'].removesuffix('-request.json'): r for r in read('counts.json')['rows']}
    jobs = [(name, draw) for draw in (1, 2, 3) for case in read('case-plan.json')['cases'] for name in (case + '-control', case + '-treatment')]

    def one(job):
        name, draw = job
        ident = name + '-' + str(draw)
        if stop.is_set():
            return {'id': ident, 'not_sent': True}
        request = read(name + '-request.json')
        put(ident + '-attempt.json', {'request': name + '-request.json', 'sha256': rows[name]['sha256']})
        start = time.monotonic()
        result = {'id': ident}
        try:
            response = probe.haiku_api('https://api.anthropic.com/v1/messages', request)
            result['response'] = response
            result['completed'] = response.get('stop_reason') == 'end_turn'
            text = ''.join(x['text'] for x in response.get('content', []) if x.get('type') == 'text')
            result['answer'] = json.loads(text)
            result['errors'], result['notes'] = checker.answer_checks(result['answer'], case_for(request))
            usage = response.get('usage', {})
            valid_usage = 0 < usage.get('input_tokens', 0) <= rows[name]['input_bound'] and 0 < usage.get('output_tokens', 0) <= rows[name]['output_bound']
            if not result['completed'] or result['errors'] or not valid_usage:
                stop.set()
        except Exception as error:
            result['error'] = type(error).__name__
            stop.set()
        result['seconds'] = round(time.monotonic() - start, 2)
        put(ident + '-answer.json', result)
        print(ident, result.get('completed'), result.get('errors'), result.get('error'), flush=True)
        return {'id': ident, 'completed': result.get('completed', False), 'errors': result.get('errors'), 'error': result.get('error')}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(one, jobs))
    verify()
    put('run-summary.json', {'results': results, 'status': 'stopped' if stop.is_set() else 'completed', 'semantic_review': 'pending', 'elapsed_seconds': time.monotonic() - started})


def launch():
    verify()
    put('launch-lock.json', {'parent_pid': os.getpid()})
    with (HERE / 'run.log').open('x') as log:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), 'worker'], stdout=log, stderr=log, start_new_session=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(ROOT / 'src')))
    (HERE / 'run.pid').write_text(str(process.pid) + '\n')
    print('Detached', process.pid)


if __name__ == '__main__':
    {'freeze': freeze, 'verify': verify, 'worker': worker, 'launch': launch}[sys.argv[1]]()
