"""Prepare and run one capped, explicitly non-acceptance judge calibration."""
import concurrent.futures
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE / 'direct-judge-trial-2026-10-29'
DESIGN = HERE / 'direct-judge-trial-design-2026-10-29.md'
DATA = '/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28'
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
MODEL = 'gpt-6.1-terra'
OUTPUT_LIMIT = 8000
CAP = 0.60


def digest(data):
    return hashlib.sha256(data).hexdigest()


def put(path, obj):
    with path.open('x', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')


def read(name):
    return json.loads((RUN / name).read_text())


def obj(properties):
    return {'type': 'object', 'properties': properties, 'required': list(properties), 'additionalProperties': False}


def array(items):
    return {'type': 'array', 'items': items}


def schemas():
    string = {'type': 'string'}
    fact = obj({'quote': string, 'meaning': string, 'weight': {'type': 'string', 'enum': ['core', 'colour']},
                'pages': array(string), 'why': string})
    control = obj({'articles': array(obj({'input_id': string, 'facts': array(fact), 'excluded': string}))})
    entry = obj({'id': {'type': 'string', 'enum': list('abcdefghi')},
                 'label': {'type': 'string', 'enum': ['core', 'colour', 'exclude', 'uncertain']},
                 'meaning': string, 'quote': string, 'why': string})
    return control, obj({'items': array(entry)})


def response_request(system, user, schema, name):
    return {'model': MODEL, 'input': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
            'text': {'format': {'type': 'json_schema', 'name': name, 'strict': True, 'schema': schema}},
            'reasoning': {'effort': 'xhigh'}, 'service_tier': 'default', 'max_output_tokens': OUTPUT_LIMIT, 'store': False}


def validate(kind, answer, expected_articles):
    if not isinstance(answer, dict):
        return False
    if kind == 'trial':
        if set(answer) != {'items'} or not isinstance(answer['items'], list):
            return False
        items = answer['items']
        if len(items) != 9 or {x.get('id') for x in items if isinstance(x, dict)} != set('abcdefghi'):
            return False
        return all(set(x) == {'id', 'label', 'meaning', 'quote', 'why'}
                   and x['label'] in ('core', 'colour', 'exclude', 'uncertain')
                   and all(isinstance(x[k], str) and x[k].strip() for k in ('meaning', 'quote', 'why')) for x in items)
    if set(answer) != {'articles'} or not isinstance(answer['articles'], list):
        return False
    articles = answer['articles']
    if len(articles) != 6 or {a.get('input_id') for a in articles if isinstance(a, dict)} != set(expected_articles):
        return False
    for a in articles:
        if set(a) != {'input_id', 'facts', 'excluded'} or not isinstance(a['excluded'], str) or not isinstance(a['facts'], list):
            return False
        for e in a['facts']:
            if not isinstance(e, dict) or set(e) != {'quote', 'meaning', 'weight', 'pages', 'why'}:
                return False
            if e['weight'] not in ('core', 'colour') or not isinstance(e['pages'], list) or not all(isinstance(x, str) for x in e['pages']):
                return False
            if not all(isinstance(e[k], str) and e[k].strip() for k in ('quote', 'meaning', 'why')):
                return False
    return True


def prepare():
    design = DESIGN.read_text()
    source = json.loads((HERE / 'economic-judge-input-2026-10-29.json').read_text())
    articles = {a['input_id']: a for a in source['articles']}
    assert len(articles) == 6
    candidates, gold = [], {}
    for line in design.splitlines():
        if not re.match(r'^\| [a-i] / ', line):
            continue
        cells = line.split('|')
        ident = cells[1].strip().split()[0]
        input_id = cells[2].strip()
        spans = re.findall(r'`([^`]+)`', cells[3])
        label = cells[4].strip()
        assert ident not in gold and input_id in articles and spans and label in ('core', 'colour', 'exclude')
        assert all(s in articles[input_id]['source'] for s in spans), (ident, spans)
        candidates.append({'id': ident, 'input_id': input_id, 'source_fragments': spans})
        gold[ident] = label
    assert set(gold) == set('abcdefghi') and len(candidates) == 9
    control_system = re.search(r'对照实际系统消息逐字为：`([^`]+)`', design).group(1)
    trial_system = re.search(r'^> (你是投资 NVIDIA 的资深对冲基金分析师。逐篇读提供的正文和当时的问题。.*)$', design, re.M).group(1)
    control_schema, trial_schema = schemas()
    compact = lambda x: json.dumps(x, ensure_ascii=False, separators=(',', ':'))
    control = response_request(control_system, compact(source), control_schema, 'control')
    trial = response_request(trial_system, compact({'scope': source['scope'], 'articles': source['articles'], 'candidates': candidates}), trial_schema, 'trial')
    RUN.mkdir(exist_ok=False)
    put(RUN / 'gold.json', gold)
    put(RUN / 'control-request.json', control)
    put(RUN / 'trial-request.json', trial)
    manifest = {'design_sha256': digest(DESIGN.read_bytes()), 'source_sha256': digest((HERE / 'economic-judge-input-2026-10-29.json').read_bytes()),
                'files': {name: digest((RUN / name).read_bytes()) for name in ('gold.json', 'control-request.json', 'trial-request.json')},
                'article_ids': list(articles), 'model': MODEL, 'sample_count': 3, 'cap_usd': CAP}
    put(RUN / 'manifest.json', manifest)
    print('prepared: six articles, nine user decisions; raw requests and reference frozen')


def verify():
    m = read('manifest.json')
    assert m['design_sha256'] == digest(DESIGN.read_bytes())
    assert m['source_sha256'] == digest((HERE / 'economic-judge-input-2026-10-29.json').read_bytes())
    for name, sha in m['files'].items():
        assert digest((RUN / name).read_bytes()) == sha, name
    assert m['model'] == MODEL and m['sample_count'] == 3 and m['cap_usd'] == CAP
    for name in ('control-request.json', 'trial-request.json'):
        r = read(name)
        assert r['model'] == MODEL and r['max_output_tokens'] == OUTPUT_LIMIT and r['service_tier'] == 'default'
    valid = {'items': [{'id': i, 'label': 'core', 'meaning': 'x', 'quote': 'x', 'why': 'x'} for i in 'abcdefghi']}
    assert validate('trial', valid, m['article_ids'])
    assert not validate('trial', {'items': valid['items'][:-1]}, m['article_ids'])
    assert not validate('trial', {'items': valid['items'][:-1] + [valid['items'][0]]}, m['article_ids'])
    control = {'articles': [{'input_id': i, 'facts': [], 'excluded': ''} for i in m['article_ids']]}
    assert validate('control', control, m['article_ids'])
    assert not validate('control', {'articles': control['articles'][:-1]}, m['article_ids'])
    print('offline checks: 9 cases, 6 articles; missing and duplicate mutants rejected')


def api(path, body):
    credentials = os.environ.get('OPENAI_API_KEY')
    if not credentials:
        with open(os.path.expanduser('~/.config/hivemind/credentials.json'), encoding='utf-8') as f:
            credentials = json.load(f)['OPENAI_API_KEY']
    payload = json.dumps(body, ensure_ascii=False, separators=(',', ':')).encode()
    request = urllib.request.Request('https://api.openai.com/v1/' + path, payload,
                                     {'Authorization': 'Bearer ' + credentials, 'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.loads(response.read())


def count():
    verify()
    assert not (RUN / 'counts.json').exists()
    counts = {}
    for name in ('control', 'trial'):
        req = read(name + '-request.json')
        request = {k: req[k] for k in ('model', 'input', 'text')}
        result = api('responses/input_tokens', request)
        assert result.get('object') == 'response.input_tokens' and isinstance(result.get('input_tokens'), int) and result['input_tokens'] > 0
        counts[name] = result['input_tokens']
    # Three generations and one conservative token-count reservation per arm.
    upper = (4 * sum(counts.values()) * 1.25 + 6 * OUTPUT_LIMIT * 5) / 1_000_000
    put(RUN / 'counts.json', {'input_tokens': counts, 'reserved_upper_usd': upper, 'cap_usd': CAP,
                              'ready': upper < CAP, 'request_hashes': read('manifest.json')['files']})
    print(json.dumps({'input_tokens': counts, 'reserved_upper_usd': round(upper, 6), 'ready': upper < CAP}))
    assert upper < CAP


def answer_text(response):
    return ''.join(part.get('text', '') for item in response.get('output', []) if item.get('type') == 'message'
                   for part in item.get('content', []) if part.get('type') == 'output_text')


def one(kind, number):
    request = read(kind + '-request.json')
    target = RUN / f'{kind}-{number}.json'
    started = time.monotonic()
    try:
        response = api('responses', request)
        text = answer_text(response)
        try:
            answer = json.loads(text)
        except (ValueError, TypeError):
            answer = None
        structurally_valid = response.get('status') == 'completed' and validate(kind, answer, read('manifest.json')['article_ids'])
        record = {'response': response, 'answer': answer, 'structurally_valid': structurally_valid,
                  'semantic_status': 'pending human review', 'seconds': round(time.monotonic() - started, 2)}
    except urllib.error.HTTPError as e:
        record = {'error': 'HTTP error', 'http_status': e.code, 'structurally_valid': False, 'seconds': round(time.monotonic() - started, 2)}
    except (OSError, ValueError, KeyError) as e:
        record = {'error': type(e).__name__, 'structurally_valid': False, 'seconds': round(time.monotonic() - started, 2)}
    put(target, record)
    return {'sample': f'{kind}-{number}', 'structurally_valid': record['structurally_valid'],
            'usage': record.get('response', {}).get('usage'), 'error': record.get('error')}


def worker():
    verify()
    counts = read('counts.json')
    assert counts['ready'] and counts['cap_usd'] == CAP and counts['reserved_upper_usd'] < CAP
    assert counts['request_hashes'] == read('manifest.json')['files']
    work = [(kind, i) for kind in ('control', 'trial') for i in range(1, 4)]
    assert all(not (RUN / f'{kind}-{i}.json').exists() for kind, i in work)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(one, kind, i) for kind, i in work]
        results = [f.result() for f in futures]
    put(RUN / 'run-summary.json', {'samples': results, 'interpretation': 'Structural checks only; human semantic and refusal review pending.'})
    print(json.dumps(results, ensure_ascii=False), flush=True)


def launch():
    verify()
    assert read('counts.json')['ready'] and not (RUN / 'run.pid').exists()
    with (RUN / 'run.log').open('x') as log:
        proc = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), 'worker'], stdout=log, stderr=log, start_new_session=True)
    with (RUN / 'run.pid').open('x') as f:
        f.write(str(proc.pid) + '\n')
    print('detached worker pid', proc.pid)


if __name__ == '__main__':
    {'prepare': prepare, 'verify': verify, 'count': count, 'launch': launch, 'worker': worker}[sys.argv[1]]()
