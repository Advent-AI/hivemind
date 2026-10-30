"""Ask the original model about three stored filing decisions; preserve model self-report as a lead."""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
import sqlite3
import subprocess
import sys
import time
import urllib.error
from pathlib import Path

HERE = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-retention-audit')
ROOT = HERE.parents[2]
RUN = HERE / 'placement-account-probe2-2026-10-29'
ARCHIVE = '/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/archive.sqlite'
spec = importlib.util.spec_from_file_location('prior_probe', HERE / 'deepseek-extraction-probe-2026-10-29.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
CASES = {
    'sharon': (70, 'e6', 'Why did you return no links for e6 about Sharon AI’s six-year agreement, 72 MW, and up to 40,000 GPUs? Which exact original instruction and source statements did you rely on? Which two alternative interpretations did you reject, and why? Separate what was shown from what you inferred.'),
    'kyber': (305, 'e3', 'Why did you return no links for e3 about the cancelled NVL72x2 design? Which exact original instruction and source statements did you rely on? Which two alternative interpretations did you reject, and why? Consider the whole request, and separate what was shown from what you inferred.'),
}


def put(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def build():
    result = {}
    with sqlite3.connect(f'file:{ARCHIVE}?mode=ro', uri=True) as db:
        for name, (call_id, evidence_id, question) in CASES.items():
            row = db.execute('select purpose,model,request_json,response_json,answer_json from model_calls where call_id=?', (call_id,)).fetchone()
            if not row or row[0:2] != ('place', 'gpt-6-luna'):
                raise ValueError('missing original placement: ' + name)
            old, raw, answer = map(json.loads, row[2:])
            matches = [p for p in answer['placements'] if p['id'] == evidence_id]
            assert len(matches) == 1 and matches[0]['links'] == []
            original_content = raw['choices'][0]['message']['content']
            assert json.loads(original_content) == answer
            request = {'model': old['model'], 'messages': old['messages'] + [
                {'role': 'assistant', 'content': original_content}, {'role': 'user', 'content': question}],
                'reasoning_effort': old['reasoning_effort'], 'max_completion_tokens': 6000}
            result[name] = {'call_id': call_id, 'request': request,
                            'old_schema': old['response_format']['json_schema']['schema']}
    return result


def prepare():
    requests = build()
    reserves = {n: (3 * len(prior.wire(r['request'])) + 16384) * 0.10 / 1e6 + 6064 * 0.50 / 1e6 for n, r in requests.items()}
    assert sum(reserves.values()) < .60
    RUN.mkdir(exist_ok=False)
    for name, item in requests.items():
        put(RUN / (name + '-request.json'), item['request'])
    put(RUN / 'manifest.json', {'case_ids': {n:r['call_id'] for n,r in requests.items()},
        'request_hashes': {n:prior.digest(RUN/(n+'-request.json')) for n in requests},
        'reserve_usd': reserves, 'cap_usd': .60,
        'limits': 'A continuation recreates system/user/assistant text; the historical structured-output instruction may have been injected by provider and is not present in this continuation. Self-reports are leads, not proof.'})
    print('prepared 2 original-conversation probes; reserved', round(sum(reserves.values()), 6))


def verify():
    m = json.loads((RUN/'manifest.json').read_text()); now = build()
    assert sum(m['reserve_usd'].values()) < m['cap_usd'] == .60
    for name, case in now.items():
        p = RUN/(name+'-request.json')
        assert prior.digest(p) == m['request_hashes'][name] and json.loads(p.read_text()) == case['request']
    print('verified 2 historical placements and conversation contents')


def one(name):
    request = json.loads((RUN/(name+'-request.json')).read_text()); start = time.monotonic()
    try:
        response = prior.api('gpt', 'https://api.openai.com/v1/chat/completions', request)
        record = {'response':response,'seconds':round(time.monotonic()-start,2)}
    except urllib.error.HTTPError as error:
        record = {'error':'HTTPError','status':error.code}
    except Exception as error:
        record = {'error':type(error).__name__}
    put(RUN/(name+'-response.json'),record)
    print(name,'finish',record.get('response',{}).get('choices',[{}])[0].get('finish_reason'),'error',record.get('error'),flush=True)
    return name


def worker():
    verify()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        completed = list(pool.map(one, CASES))
    put(RUN/'run-summary.json',{'completed':completed,'review':'pending'} )


def launch():
    verify()
    if (RUN/'run.pid').exists():
        raise ValueError('already launched')
    with (RUN/'run.log').open('x') as log:
        p=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'worker'], stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONPATH=str(ROOT/'src')))
    (RUN/'run.pid').write_text(str(p.pid)+'\n')
    print('detached pid',p.pid)


if __name__ == '__main__':
    {'prepare':prepare,'verify':verify,'launch':launch,'worker':worker}[sys.argv[1]]()
