"""One-article, three-sample comparison of the actual v38 extraction request."""
import concurrent.futures
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zipfile

from hivemind import config, extraction, model, universe
from tokenizers import Tokenizer

ROOT = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
HERE = ROOT / 'docs/research/2026-10-28-retention-audit'
RUN = HERE / 'deepseek-extraction-probe-2026-10-29'
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
ARCHIVE = '/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/archive.sqlite'
INPUT_ID = 'gnews:71df54965281684cc500960f'
EXPECTED = '99dc1c7e9f97d09ba8f9480db32e267c0f57465051f50cccf2e7e190af507007'
TOKENIZER_HASH = 'e7310d1dafe0a86d8a5629fe78a7c763760f651db9b8682718a1781dcd6fe495'
CAP = .60


def put(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def read(name):
    return json.loads((RUN / name).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wire(value):
    return json.dumps(value).encode('utf-8')


def source():
    db = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    item = dict(db.execute('select * from items where input_id=?', (INPUT_ID,)).fetchone())
    item['object_identifiers'] = json.loads(item['object_identifiers'])
    cfg = config.load(str(ROOT / 'poc/config/poc-v38.json'))
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    setting, system, user, schema = extraction.request_for(cfg, item, item['text'], [], uni, [])
    request = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
    assert model.request_identity(request)[1] == EXPECTED
    assert request['model'] == 'gpt-6-luna' and request['max_completion_tokens'] == 8000
    assert '82% growth' in item['text'] and '41%' in item['text'] and '$650 billion' in item['text']
    return item, uni, setting, schema, request


def key(provider):
    name = 'OPENAI_API_KEY' if provider == 'gpt' else 'DEEPSEEK_API_KEY'
    value = os.environ.get(name)
    if not value:
        value = json.loads(Path('~/.config/hivemind/credentials.json').expanduser().read_text())[name]
    return value


def api(provider, url, request):
    req = urllib.request.Request(url, wire(request), {'Authorization': 'Bearer ' + key(provider), 'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=180) as response:
        return json.loads(response.read())


def prepare():
    item, uni, setting, schema, gpt = source()
    deep = {'model': 'deepseek-flash', 'input': copy.deepcopy(gpt['messages']),
            'text': {'format': {'type': 'json_schema', 'name': 'extraction', 'schema': copy.deepcopy(schema)}},
            'reasoning': {'effort': 'high'}, 'max_output_tokens': 8000}
    assert wire(gpt['messages']) == wire(deep['input'])
    assert wire(gpt['response_format']['json_schema']['schema']) == wire(deep['text']['format']['schema'])
    RUN.mkdir(exist_ok=False)
    put(RUN / 'gpt-request.json', gpt)
    put(RUN / 'deepseek-request.json', deep)
    put(RUN / 'gold.json', {'source_input_id': INPUT_ID,
        'facts': ['Analyst forecast: revenue growth 82% for the rest of 2026 and 41% for 2027.',
                  'Management forecast: hyperscaler spending projected $650 billion in 2026 and over $1 trillion in 2027.'],
        'eps_2028': 'May retain; weight and destination not adjudicated.', 'scope': 'one selected article; not a whole-week score'})
    put(RUN / 'manifest.json', {'request_sha256': EXPECTED, 'source_text_sha256': hashlib.sha256(item['text'].encode()).hexdigest(),
        'design_sha256': digest(HERE / 'deepseek-extraction-probe-design-2026-10-29.md'),
        'files': {n: digest(RUN / n) for n in ('gpt-request.json', 'deepseek-request.json', 'gold.json')},
        'reasoning': {'gpt': gpt.get('reasoning_effort'), 'deepseek': 'high'}, 'max_output_tokens': 8000})
    print('prepared production request', EXPECTED)


def verify():
    item, uni, setting, schema, built = source()
    manifest = read('manifest.json')
    assert manifest['source_text_sha256'] == hashlib.sha256(item['text'].encode()).hexdigest()
    assert manifest['design_sha256'] == digest(HERE / 'deepseek-extraction-probe-design-2026-10-29.md')
    for n, h in manifest['files'].items():
        assert digest(RUN / n) == h
    gpt, deep = read('gpt-request.json'), read('deepseek-request.json')
    assert wire(gpt) == wire(built) and wire(gpt['messages']) == wire(deep['input'])
    assert wire(schema) == wire(deep['text']['format']['schema'])
    conn = sqlite3.connect(f'file:{ARCHIVE}?mode=ro', uri=True)
    original = json.loads(conn.execute('select answer_json from model_calls where request_sha256=?', (EXPECTED,)).fetchone()[0])
    assert not model.check_schema(original, schema)
    invalid = copy.deepcopy(original)
    del invalid['evidence'][0]['quote']
    assert model.check_schema(invalid, schema)
    evidence, candidates, dropped, groups = extraction.sift_with_groups(original, item, item['text'], set(), uni, english=True, shown_group_ids=(), version=setting.prompt_version.rpartition('-')[2], keep_unlinked=True)
    assert any(e['id'] == 'e2' and 'metric' in e.get('one_line', '').lower() for e in evidence)
    print('verified exact production request, historical answer and broken-schema control', flush=True)


def count():
    verify()
    gpt, deep = read('gpt-request.json'), read('deepseek-request.json')
    req = {'model': gpt['model'], 'input': gpt['messages'], 'text': {'format': {'type': 'json_schema', 'name': 'extraction', 'strict': True, 'schema': gpt['response_format']['json_schema']['schema']}}}
    raw = urllib.request.urlopen('https://cdn.deepseek.com/api-docs/deepseek_v4_tokenizer.zip', timeout=60).read()
    assert hashlib.sha256(raw).hexdigest() == TOKENIZER_HASH
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        tokenizer = Tokenizer.from_str(archive.read('deepseek_v4_tokenizer/tokenizer.json').decode())
    estimate = len(tokenizer.encode(json.dumps({'input': deep['input'], 'text': deep['text']}, ensure_ascii=False, separators=(',', ':'))).ids)
    # Refuse before the token-count request if a conservative byte reserve alone exceeds the cap.
    gb0 = 2 * len(wire(gpt)) + 16384
    db = max(3 * estimate, 2 * len(wire(deep))) + 16384
    assert (4 * gb0 * .10 + 3 * 8064 * .50 + 3 * db * .30 + 3 * 8064 * 1.20) / 1e6 < CAP
    result = api('gpt', 'https://api.openai.com/v1/responses/input_tokens', req)
    assert result.get('object') == 'response.input_tokens' and result.get('input_tokens', 0) > 0
    gb = max(3 * result['input_tokens'], 2 * len(wire(gpt))) + 16384
    reserve = (4 * gb * .10 + 3 * 8064 * .50 + 3 * db * .30 + 3 * 8064 * 1.20) / 1e6
    assert reserve < CAP
    put(RUN / 'counts.json', {'gpt_count': result['input_tokens'], 'deepseek_token_estimate': estimate,
        'gpt_input_reserve_each': gb, 'deepseek_input_reserve_each': db, 'output_reserve_each': 8064,
        'reserved_usd': reserve, 'cap_usd': CAP, 'tokenizer_sha256': TOKENIZER_HASH,
        'note': 'Unknown usage keeps full reserve. This is a conservative estimate, not a provider spending ceiling.'})
    print('counts and reserved USD', result['input_tokens'], estimate, round(reserve, 6), flush=True)


def one(provider, number):
    started = time.monotonic()
    try:
        url = 'https://api.openai.com/v1/chat/completions' if provider == 'gpt' else 'https://api.deepseek.com/responses'
        response = api(provider, url, read(provider + '-request.json'))
        if provider == 'gpt':
            completed = response['choices'][0]['finish_reason'] == 'stop'
            content = response['choices'][0]['message'].get('content') or ''
        else:
            completed = response.get('status') == 'completed'
            content = ''.join(p.get('text', '') for x in response.get('output', []) if x.get('type') == 'message' for p in x.get('content', []) if p.get('type') == 'output_text')
        try:
            answer = json.loads(content)
        except (ValueError, TypeError):
            answer = None
        item, uni, setting, schema, _ = source()
        errors = model.check_schema(answer, schema)
        record = {'response': response, 'answer': answer, 'schema_errors': errors, 'completed': completed, 'seconds': round(time.monotonic() - started, 2)}
        if completed and not errors:
            e, c, d, g = extraction.sift_with_groups(answer, item, item['text'], set(), uni, english=True, shown_group_ids=(), version=setting.prompt_version.rpartition('-')[2], keep_unlinked=True)
            record['sift'] = {'evidence': e, 'candidates': c, 'dropped': d, 'new_groups': g}
    except urllib.error.HTTPError as error:
        record = {'error': 'HTTP error', 'http_status': error.code, 'seconds': round(time.monotonic() - started, 2)}
    except Exception as error:
        record = {'error': type(error).__name__, 'seconds': round(time.monotonic() - started, 2)}
    put(RUN / f'{provider}-{number}.json', record)
    print(provider, number, 'complete', record.get('completed', False), 'error', record.get('error'), flush=True)
    return {'sample': f'{provider}-{number}', 'completed': record.get('completed', False), 'schema_errors': record.get('schema_errors'),
            'sifted': 'sift' in record, 'usage': record.get('response', {}).get('usage'), 'error': record.get('error'), 'http_status': record.get('http_status')}


def worker():
    verify()
    counts = read('counts.json')
    assert counts['reserved_usd'] < CAP
    jobs = [(p, i) for p in ('gpt', 'deepseek') for i in (1, 2, 3)]
    assert all(not (RUN / f'{p}-{i}.json').exists() for p, i in jobs)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(one, p, i) for p, i in jobs]
        results = [f.result() for f in futures]
    put(RUN / 'run-summary.json', {'samples': results, 'semantic_status': 'pending human review'})
    print('all calls finished', flush=True)


def launch():
    verify()
    assert read('counts.json')['reserved_usd'] < CAP and not (RUN / 'run.pid').exists()
    with (RUN / 'run.log').open('x') as log:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), 'worker'], stdout=log, stderr=log, start_new_session=True, env=dict(os.environ, PYTHONPATH=str(ROOT / 'src')))
    (RUN / 'run.pid').write_text(str(process.pid) + '\n')
    print('detached pid', process.pid)


if __name__ == '__main__':
    {'prepare': prepare, 'verify': verify, 'count': count, 'worker': worker, 'launch': launch}[sys.argv[1]]()
