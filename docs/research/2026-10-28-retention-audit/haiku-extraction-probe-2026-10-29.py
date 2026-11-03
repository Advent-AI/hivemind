"""Compare one archived v38 extraction request with Haiku on one article."""
import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
RUN = HERE / 'haiku-extraction-probe-2026-10-29'
DESIGN = HERE / 'haiku-extraction-probe-design-2026-10-29.md'
CAP = .60
spec = importlib.util.spec_from_file_location('previous_probe', HERE / 'deepseek-extraction-probe-2026-10-29.py')
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)


def put(name, obj):
    with (RUN / name).open('x') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')


def read(name):
    return json.loads((RUN / name).read_text())


def haiku_key():
    result = subprocess.run(['/usr/bin/security', 'find-generic-password', '-a', os.environ['USER'], '-s', 'hivemind-anthropic', '-w'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True)
    key = result.stdout.decode().strip()
    if not key:
        raise RuntimeError('Keychain entry is empty')
    return key


def haiku_api(url, body=None):
    headers = {'x-api-key': haiku_key(), 'anthropic-version': '2026-10-21'}
    if body is not None:
        headers['content-type'] = 'application/json'
    request = urllib.request.Request(url, None if body is None else previous.wire(body), headers, method='GET' if body is None else 'POST')
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.loads(response.read())


def prepare():
    item, uni, setting, schema, gpt = previous.source()
    haiku = {'model': 'claude-haiku-5-5', 'max_tokens': 8000,
             'system': gpt['messages'][0]['content'], 'messages': [gpt['messages'][1]],
             'output_config': {'effort': 'low', 'format': {'type': 'json_schema', 'schema': schema}}}
    assert previous.wire(schema) == previous.wire(haiku['output_config']['format']['schema'])
    assert gpt['messages'] == [{'role': 'system', 'content': haiku['system']}, *haiku['messages']]
    # The higher long-context tariff is used for the whole reserve, regardless of input size.
    gb = 3 * len(previous.wire(gpt)) + 16384
    hb = 3 * len(previous.wire(haiku)) + 16384
    reserve = 3 * (gb * .10 + 8064 * .50) / 1e6 + 3 * (hb * .50 + 8064 * 2.50) / 1e6
    assert reserve < CAP
    RUN.mkdir(exist_ok=False)
    put('gpt-request.json', gpt)
    put('haiku-request.json', haiku)
    put('gold.json', json.loads((previous.RUN / 'gold.json').read_text()))
    put('manifest.json', {'production_request_sha256': previous.EXPECTED,
        'design_sha256': previous.digest(DESIGN),
        'files': {n: previous.digest(RUN / n) for n in ('gpt-request.json', 'haiku-request.json', 'gold.json')},
        'input_token_reserve_each': {'gpt': gb, 'haiku': hb}, 'output_token_reserve_each': 8064,
        'reserved_usd': reserve, 'cap_usd': CAP,
        'note': 'Conservative estimate, not a provider-enforced spending ceiling; unknown usage retains full reserve.'})
    print('prepared; maximum reserve USD', round(reserve, 6))


def verify():
    previous.verify()
    item, uni, setting, schema, gpt = previous.source()
    manifest = read('manifest.json')
    assert manifest['design_sha256'] == previous.digest(DESIGN) and manifest['reserved_usd'] < CAP
    for name, digest in manifest['files'].items():
        assert previous.digest(RUN / name) == digest
    h = read('haiku-request.json')
    assert previous.wire(read('gpt-request.json')) == previous.wire(gpt)
    assert gpt['messages'] == [{'role': 'system', 'content': h['system']}, *h['messages']]
    assert previous.wire(schema) == previous.wire(h['output_config']['format']['schema'])
    assert h['model'] == 'claude-haiku-5-5' and h['max_tokens'] == 8000
    print('verified production request, identical explicit text and schema', flush=True)


def one(provider, number):
    start = time.monotonic()
    try:
        if provider == 'haiku':
            response = haiku_api('https://api.anthropic.com/v1/messages', read('haiku-request.json'))
            complete = response.get('stop_reason') == 'end_turn'
            content = ''.join(c.get('text', '') for c in response.get('content', []) if c.get('type') == 'text')
        else:
            response = previous.api('gpt', 'https://api.openai.com/v1/chat/completions', read('gpt-request.json'))
            complete = response['choices'][0]['finish_reason'] == 'stop'
            content = response['choices'][0]['message'].get('content') or ''
        try:
            answer = json.loads(content)
        except (ValueError, TypeError):
            answer = None
        item, uni, setting, schema, _ = previous.source()
        errors = previous.model.check_schema(answer, schema)
        record = {'response': response, 'answer': answer, 'completed': complete, 'schema_errors': errors,
                  'seconds': round(time.monotonic() - start, 2)}
        if complete and not errors:
            e, c, d, g = previous.extraction.sift_with_groups(answer, item, item['text'], set(), uni, english=True,
                shown_group_ids=(), version=setting.prompt_version.rpartition('-')[2], keep_unlinked=True)
            record['sift'] = {'evidence': e, 'candidates': c, 'dropped': d, 'new_groups': g}
    except urllib.error.HTTPError as e:
        record = {'error': 'HTTP error', 'http_status': e.code, 'seconds': round(time.monotonic() - start, 2)}
    except Exception as e:
        record = {'error': type(e).__name__, 'seconds': round(time.monotonic() - start, 2)}
    put(f'{provider}-{number}.json', record)
    print(provider, number, 'completed', record.get('completed', False), 'error', record.get('error'), flush=True)
    return record


def worker():
    verify()
    first = one('haiku', 1)
    if 'error' in first:
        put('run-summary.json', {'status': 'stopped after first API error', 'first_http_status': first.get('http_status')})
        return
    # A response, including truncation, means the schema was accepted. Stop on anomalous provider usage.
    usage = first.get('response', {}).get('usage', {})
    bound = read('manifest.json')['input_token_reserve_each']['haiku']
    if usage.get('input_tokens', 0) > bound or usage.get('output_tokens', 0) > 8064:
        put('run-summary.json', {'status': 'stopped after first usage exceeded reserve'})
        return
    jobs = [('haiku', 2), ('haiku', 3), ('gpt', 1), ('gpt', 2), ('gpt', 3)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        records = [f.result() for f in [pool.submit(one, p, i) for p, i in jobs]]
    put('run-summary.json', {'status': 'complete; manual semantic review pending',
        'samples': [{'sample': f'{p}-{i}', 'completed': r.get('completed', False),
                     'usage': r.get('response', {}).get('usage'), 'error': r.get('error'), 'http_status': r.get('http_status')}
                    for (p, i), r in zip([('haiku', 1)] + jobs, [first] + records)]})


def launch():
    verify()
    try:
        haiku_api('https://api.anthropic.com/v1/models/claude-haiku-5-5')
    except urllib.error.HTTPError as error:
        print('model access failed; HTTP', error.code)
        return
    except (OSError, subprocess.CalledProcessError, RuntimeError) as error:
        print('model access failed:', type(error).__name__)
        return
    assert not (RUN / 'run.pid').exists()
    with (RUN / 'run.log').open('x') as log:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), 'worker'], stdout=log, stderr=log,
            start_new_session=True, env=dict(os.environ, PYTHONPATH=str(previous.ROOT / 'src')))
    (RUN / 'run.pid').write_text(str(process.pid) + '\n')
    print('detached pid', process.pid)


if __name__ == '__main__':
    {'prepare': prepare, 'verify': verify, 'launch': launch, 'worker': worker}[sys.argv[1]]()
