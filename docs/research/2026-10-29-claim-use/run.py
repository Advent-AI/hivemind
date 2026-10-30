"""One paired Haiku research-reading experiment on immutable saved sources."""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = HERE.parent / '2026-10-29-model-capability/run.py'
spec = importlib.util.spec_from_file_location('prior', BASE)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def read(name):
    return json.loads((HERE / name).read_text())


def put(name, value):
    with (HERE / name).open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.flush()
        os.fsync(stream.fileno())


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate():
    plan, budget = read('plan.json'), read('counts.json')
    assert plan['planned_calls'] == 42 and plan['samples'] == 3
    assert budget['cap_usd'] == .60 and budget['combined_reserved_usd'] < .60
    assert len(budget['rows']) == 14
    for row in budget['rows']:
        assert digest(HERE / row['request']) == row['sha256']
    for case in plan['cases']:
        control = read(case + '-control-request.json')
        treatment = read(case + '-treatment-request.json')
        assert control['messages'] == treatment['messages']
        assert prior.schema(control)['properties']['proposal'] == prior.schema(treatment)['properties']['proposal']
        for arm, request in [('control', control), ('treatment', treatment)]:
            assert request['model'] == 'claude-haiku-5-5'
            assert request['max_tokens'] == 6000 and request['output_config']['effort'] == 'medium'
            assert request['system'] == (HERE / (arm + '-system.txt')).read_text()
            history, siblings, questions = prior.domains(request)
            assert history == questions == []
            if arm == 'treatment':
                props = prior.schema(request)['properties']['findings']['items']['properties']
                assert props['source_ids']['items']['enum'] == ['incoming'] + siblings


def freeze():
    validate()
    files = [p for p in HERE.iterdir() if p.is_file()]
    files += list((ROOT / 'src/hivemind').rglob('*.py'))
    files += list((ROOT / 'src/hivemind/prompts').glob('*'))
    files += [BASE, ROOT / 'docs/research/2026-10-28-retention-audit/haiku-extraction-probe-2026-10-29.py',
              ROOT / 'docs/research/2026-10-28-retention-audit/deepseek-extraction-probe-2026-10-29.py']
    put('manifest.json', {'files': {str(p): digest(p) for p in files if p.is_file()}})


def verify():
    for path, expected in read('manifest.json')['files'].items():
        assert digest(path) == expected, path


def jobs():
    plan = read('plan.json')
    result = [(case, arm, draw) for draw in (1, 2, 3)
              for case in plan['cases'] for arm in ('control', 'treatment')]
    random.Random(202610292).shuffle(result)
    return result


def worker():
    verify()
    bounds = {r['request']: r for r in read('counts.json')['rows']}
    stop = threading.Event()
    started = time.monotonic()

    def one(job):
        case, arm, draw = job
        ident = f'{case}-{arm}-{draw}'
        if stop.is_set():
            return {'id': ident, 'not_sent': True}
        filename = f'{case}-{arm}-request.json'
        request = read(filename)
        put(ident + '-attempt.json', {'request': filename, 'sha256': bounds[filename]['sha256']})
        before = time.monotonic()
        result = {'id': ident}
        try:
            response = prior.provider.haiku_api('https://api.anthropic.com/v1/messages', request)
            result['response'] = response
            result['completed'] = response.get('stop_reason') == 'end_turn'
            assert response['model'] == 'claude-haiku-5-5'
            usage = response['usage']
            assert 0 < usage['input_tokens'] <= bounds[filename]['input_bound']
            assert 0 < usage['output_tokens'] <= bounds[filename]['output_bound']
            text = ''.join(c.get('text', '') for c in response['content'] if c['type'] == 'text')
            result['answer'] = json.loads(text)
            result['errors'] = prior.check(result['answer'], request, arm)
            if not result['completed']:
                stop.set()
        except Exception as error:
            result['error'] = type(error).__name__
            stop.set()
        result['seconds'] = round(time.monotonic() - before, 2)
        put(ident + '-answer.json', result)
        print(ident, result.get('completed'), result.get('errors'), result.get('error'), flush=True)
        return {k: result[k] for k in ('id', 'completed', 'errors', 'error') if k in result}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(one, jobs()))
    verify()
    put('run-summary.json', {'status': 'stopped' if stop.is_set() else 'completed',
                             'elapsed_seconds': time.monotonic() - started, 'results': results})


def launch():
    verify()
    assert shutil.disk_usage(HERE).free > 500_000_000
    health = prior.provider.haiku_api('https://api.anthropic.com/v1/models/claude-haiku-5-5')
    put('launch.json', {'disk_free': shutil.disk_usage(HERE).free, 'model_access_ok': bool(health)})
    with (HERE / 'run.log').open('x') as log:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), 'worker'],
                                   stdout=log, stderr=log, start_new_session=True,
                                   env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(ROOT / 'src')))
    with (HERE / 'run.pid').open('x') as stream:
        stream.write(str(process.pid))
    print('Detached', process.pid)


if __name__ == '__main__':
    {'freeze': freeze, 'verify': verify, 'launch': launch, 'worker': worker}[sys.argv[1]]()
