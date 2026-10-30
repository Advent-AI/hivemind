"""Compare DeepSeek and the existing judge on the same frozen development inputs."""
import concurrent.futures
import copy
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE / 'direct-judge-trial-2026-10-29'
GOLD = HERE / 'gold-user-2026-10-29-v3' / 'reference.json'
DESIGN = HERE / 'deepseek-judge-trial-design-2026-10-29.md'
RUN = HERE / 'deepseek-judge-trial-2026-10-29'
CAP = 0.60
DS_INPUT_RESERVE = 36240
MAX_OUTPUT = 8000


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def read(name):
    return json.loads((RUN / name).read_text())


def compact(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':')).encode()


def prepare():
    old_manifest = json.loads((PRIOR / 'manifest.json').read_text())
    assert sha(PRIOR / 'trial-request.json') == old_manifest['files']['trial-request.json']
    assert sha(PRIOR / 'gold.json') == old_manifest['files']['gold.json']
    original = json.loads((PRIOR / 'trial-request.json').read_text())
    corrected = json.loads(GOLD.read_text())
    eps = next(x for x in corrected['decisions'] if x['question'] == '2')
    assert eps['decision'] == 'may_retain' and eps['weight'] == 'not_adjudicated'
    gold = json.loads((PRIOR / 'gold.json').read_text())
    assert set(gold) == set('abcdefghi') and gold['b'] == 'exclude'
    gold['b'] = None
    user = json.loads(original['input'][1]['content'])
    assert set(user) == {'scope', 'articles', 'candidates'} and len(user['articles']) == 6 and len(user['candidates']) == 9
    assert all(set(x) == {'id', 'input_id', 'source_fragments'} for x in user['candidates'])
    gpt = copy.deepcopy(original)
    deep = copy.deepcopy(original)
    deep['model'] = 'deepseek-flash'
    deep.pop('service_tier')
    deep.pop('store')
    deep['text']['format'].pop('strict')
    assert gpt['model'] == 'gpt-6.1-terra' and gpt['reasoning'] == deep['reasoning'] == {'effort': 'xhigh'}
    assert gpt['max_output_tokens'] == deep['max_output_tokens'] == MAX_OUTPUT
    assert compact(gpt['input']) == compact(deep['input']) == compact(original['input'])
    assert compact(gpt['text']['format']['schema']) == compact(deep['text']['format']['schema'])
    counts = json.loads((PRIOR / 'counts.json').read_text())
    assert counts['input_tokens']['trial'] == 12275
    # GPT: exact recorded input count, conservatively priced as cache writes;
    # DeepSeek: twice its official tokenizer estimate plus 8k formatting tokens.
    reserved = 3 * (12275 * 1.25 + MAX_OUTPUT * 5) / 1e6 + 3 * (DS_INPUT_RESERVE * .30 + MAX_OUTPUT * 1.20) / 1e6
    assert reserved < CAP
    assert len(compact({'input': deep['input'], 'text': deep['text']})) < DS_INPUT_RESERVE * 2
    RUN.mkdir(exist_ok=False)
    for name, value in [('gpt-request.json', gpt), ('deepseek-request.json', deep), ('gold.json', gold)]:
        put(RUN / name, value)
    put(RUN / 'manifest.json', {'source_request_sha256': sha(PRIOR / 'trial-request.json'), 'source_gold_sha256': sha(GOLD),
                                 'design_sha256': sha(DESIGN), 'files': {n: sha(RUN / n) for n in ('gpt-request.json', 'deepseek-request.json', 'gold.json')},
                                 'gpt_input_tokens': 12275, 'deepseek_tokenizer_estimate': 14120,
                                 'deepseek_input_reserve': DS_INPUT_RESERVE, 'tokenizer_sha256': 'e7310d1dafe0a86d8a5629fe78a7c763760f651db9b8682718a1781dcd6fe495',
                                 'max_output_tokens': MAX_OUTPUT, 'reserved_usd': reserved, 'cap_usd': CAP})
    print('prepared: identical messages and schema; EPS unscored; reserved USD', round(reserved, 6))


def verify():
    m = read('manifest.json')
    assert sha(PRIOR / 'trial-request.json') == m['source_request_sha256'] and sha(GOLD) == m['source_gold_sha256']
    assert sha(DESIGN) == m['design_sha256'] and m['reserved_usd'] < m['cap_usd'] == CAP
    for n, digest in m['files'].items():
        assert sha(RUN / n) == digest
    gpt, deep, original = read('gpt-request.json'), read('deepseek-request.json'), json.loads((PRIOR / 'trial-request.json').read_text())
    assert compact(gpt['input']) == compact(deep['input']) == compact(original['input'])
    assert compact(gpt['text']['format']['schema']) == compact(deep['text']['format']['schema'])
    assert read('gold.json')['b'] is None and len(read('gold.json')) == 9
    valid = {'items': [{'id': i, 'label': 'core', 'meaning': 'x', 'quote': 'x', 'why': 'x'} for i in 'abcdefghi']}
    assert valid_answer(valid) and not valid_answer({'items': valid['items'][:-1]})
    assert not valid_answer({'items': valid['items'][:-1] + [valid['items'][0]]})
    print('offline checks: messages and schema identical; missing and duplicate results rejected')


def valid_answer(answer):
    if not isinstance(answer, dict) or set(answer) != {'items'} or not isinstance(answer['items'], list):
        return False
    items = answer['items']
    if len(items) != 9 or {x.get('id') for x in items if isinstance(x, dict)} != set('abcdefghi'):
        return False
    return all(set(x) == {'id', 'label', 'meaning', 'quote', 'why'}
               and x['label'] in ('core', 'colour', 'exclude', 'uncertain')
               and all(isinstance(x[k], str) and x[k].strip() for k in ('meaning', 'quote', 'why')) for x in items)


def api(provider, body):
    keyname = 'OPENAI_API_KEY' if provider == 'gpt' else 'DEEPSEEK_API_KEY'
    key = os.environ.get(keyname)
    if not key:
        with open(os.path.expanduser('~/.config/hivemind/credentials.json'), encoding='utf-8') as f:
            key = json.load(f)[keyname]
    url = 'https://api.openai.com/v1/responses' if provider == 'gpt' else 'https://api.deepseek.com/responses'
    req = urllib.request.Request(url, compact(body), {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=180) as response:
        return json.loads(response.read())


def one(provider, number):
    target = RUN / f'{provider}-{number}.json'
    started = time.monotonic()
    try:
        response = api(provider, read(provider + '-request.json'))
        text = ''.join(p.get('text', '') for x in response.get('output', []) if x.get('type') == 'message'
                       for p in x.get('content', []) if p.get('type') == 'output_text')
        try:
            answer = json.loads(text)
        except (ValueError, TypeError):
            answer = None
        record = {'response': response, 'answer': answer,
                  'structurally_valid': response.get('status') == 'completed' and valid_answer(answer),
                  'semantic_status': 'pending human review', 'seconds': round(time.monotonic() - started, 2)}
    except urllib.error.HTTPError as e:
        record = {'error': 'HTTP error', 'http_status': e.code, 'structurally_valid': False, 'seconds': round(time.monotonic() - started, 2)}
    except (OSError, ValueError, KeyError) as e:
        record = {'error': type(e).__name__, 'structurally_valid': False, 'seconds': round(time.monotonic() - started, 2)}
    put(target, record)
    return {'sample': f'{provider}-{number}', 'structurally_valid': record['structurally_valid'],
            'usage': record.get('response', {}).get('usage'), 'error': record.get('error'), 'http_status': record.get('http_status')}


def worker():
    verify()
    work = [(p, i) for p in ('gpt', 'deepseek') for i in (1, 2, 3)]
    assert all(not (RUN / f'{p}-{i}.json').exists() for p, i in work)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = [f.result() for f in [pool.submit(one, p, i) for p, i in work]]
    put(RUN / 'run-summary.json', {'samples': results, 'status': 'Structural checks only; manual semantic review pending.'})
    print(json.dumps(results, ensure_ascii=False), flush=True)


def launch():
    verify()
    assert not (RUN / 'run.pid').exists()
    with (RUN / 'run.log').open('x') as log:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), 'worker'], stdout=log, stderr=log, start_new_session=True)
    with (RUN / 'run.pid').open('x') as f:
        f.write(str(process.pid) + '\n')
    print('detached worker pid', process.pid)


if __name__ == '__main__':
    {'prepare': prepare, 'verify': verify, 'launch': launch, 'worker': worker}[sys.argv[1]]()
