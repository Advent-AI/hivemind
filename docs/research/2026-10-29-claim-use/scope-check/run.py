"""Preserve two diagnostic continuations, without semantic scoring or retries."""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('experiment', HERE.parent / 'run.py')
experiment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(experiment)

def write(name, value):
    with (HERE / name).open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)

def worker():
    budget = json.loads((HERE / 'budget.json').read_text())
    assert budget['total_reserved'] < budget['cap'] == .60
    def one(row):
        path = HERE / row['request']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
        request = json.loads(path.read_text())
        start = time.monotonic()
        response = experiment.prior.provider.haiku_api('https://api.anthropic.com/v1/messages', request)
        result = {'response': response, 'seconds': time.monotonic() - start,
                  'answer': '\n'.join(c['text'] for c in response['content'] if c['type'] == 'text')}
        write(path.name.replace('-request', '-answer'), result)
        assert response['stop_reason'] == 'end_turn'
        assert response['usage']['input_tokens'] <= row['input_bound']
        assert response['usage']['output_tokens'] <= row['output_bound']
        return path.name
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        write('summary.json', {'completed': list(pool.map(one, budget['rows']))})

def launch():
    assert shutil.disk_usage(HERE).free > 500_000_000
    assert experiment.prior.provider.haiku_api('https://api.anthropic.com/v1/models/claude-haiku-5-5')
    with (HERE / 'run.log').open('x') as log:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), 'worker'],
                                   stdout=log, stderr=log, start_new_session=True,
                                   env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    with (HERE / 'run.pid').open('x') as stream:
        stream.write(str(process.pid))
    print('Detached', process.pid)

if __name__ == '__main__':
    {'launch': launch, 'worker': worker}[sys.argv[1]]()
