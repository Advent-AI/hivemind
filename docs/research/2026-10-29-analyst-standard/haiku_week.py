"""Haiku 5.5 against gpt-6-luna on the 98 extraction requests of the v38 week (2026-07-01..07), three draws each.

prepare: rebuild every production request from the items database with the v38 configuration, check its sha256 against the
         archived call, derive the Haiku request (same system text, same user text, same schema; Anthropic message shape),
         write the manifest with the cost reserve. No send.
verify:  the manifest's hashes still hold, the Haiku model answers a GET. No send.
send:    luna x3 and haiku x3 for every item, eight threads, every raw response stored in answers.sqlite; nothing is scored here.
sift:    every stored answer through the production sift (extraction.sift_with_groups, version 22, keep_unlinked) -> sifted.json.
"""
import concurrent.futures
import copy
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request

ROOT = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, extraction, model, universe  # noqa: E402

HERE = Path(__file__).resolve().parent
RUN = HERE / 'haiku-week'
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
ARCHIVE = '/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/archive.sqlite'
HAIKU = 'claude-haiku-5-5'
# USD per million tokens, read from platform.claude.com/docs/en/about-claude/pricing on 2026-10-29: Haiku 5.5 up to 100k-token
# prompts $0.10 in / $0.50 out; gpt-6-luna $0.10 / $0.50 (model.PRICES). Estimates only; the bill is the provider's.
PRICES = {HAIKU: (0.10, 0.50), 'gpt-6-luna': model.PRICES['gpt-6-luna']}
DRAWS = 3
# Alex, 2026-10-29, after the production caps (8000/12000) truncated 3 Haiku answers whose thinking took up to 6071 of 8000
# tokens: "直接改成16k token 上限吧我们不要纠结了". The answers made at the production caps are kept in answers_haiku_cap_production.
HAIKU_MAX_TOKENS = 16000
WORKERS = 8
LOCK = threading.Lock()


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def wire(value):
    return json.dumps(value).encode('utf-8')


def haiku_key():
    result = subprocess.run(['/usr/bin/security', 'find-generic-password', '-a', os.environ['USER'], '-s', 'hivemind-anthropic', '-w'],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True)
    key = result.stdout.decode().strip()
    if not key:
        raise RuntimeError('keychain entry hivemind-anthropic is empty')
    return key


def haiku_api(url, body=None, timeout=300):
    headers = {'x-api-key': haiku_key(), 'anthropic-version': '2026-10-21'}
    if body is not None:
        headers['content-type'] = 'application/json'
    request = urllib.request.Request(url, None if body is None else wire(body), headers, method='GET' if body is None else 'POST')
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())


def archived():
    """call_id -> (input_id, request_sha256, input_tokens, output_tokens) for the week's 98 extraction calls."""
    conn = sqlite3.connect(f'file:{ARCHIVE}?mode=ro', uri=True)
    rows = {}
    for call_id, request_json, sha, tin, tout in conn.execute(
            "select call_id, request_json, request_sha256, input_tokens, output_tokens from model_calls where purpose='extract' order by call_id"):
        user = json.loads(request_json)['messages'][1]['content']
        head = user[user.index('[Item] id ') + len('[Item] id '):]
        rows[call_id] = (head[:head.index(',')], sha, tin, tout)
    assert len(rows) == 98 and len({r[0] for r in rows.values()}) == 98
    return rows


def build(input_id):
    db = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    item = dict(db.execute('select * from items where input_id=?', (input_id,)).fetchone())
    item['object_identifiers'] = json.loads(item['object_identifiers'])
    cfg = config.load(str(ROOT / 'poc/config/poc-v38.json'))
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    setting, system, user, schema = extraction.request_for(cfg, item, item['text'], [], uni, [])
    request = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
    return item, uni, setting, schema, request, cfg


def to_haiku(request, schema):
    assert request['messages'][0]['role'] == 'system' and request['messages'][1]['role'] == 'user'
    return {'model': HAIKU, 'max_tokens': HAIKU_MAX_TOKENS,   # Alex 2026-10-29: 16k; Haiku's thinking shares max_tokens with the answer
            'system': request['messages'][0]['content'], 'messages': [request['messages'][1]],
            'output_config': {'format': {'type': 'json_schema', 'schema': copy.deepcopy(schema)}}}


def prepare():
    RUN.mkdir(exist_ok=False)
    rows = archived()
    holdout = json.loads((HERE / 'holdout-pick.json').read_text())
    manifest = {'items': [], 'draws': DRAWS, 'prices_usd_per_mtok': PRICES}
    reserve = 0.0
    jobs = [(call_id, input_id, sha, tin, tout, True) for call_id, (input_id, sha, tin, tout) in rows.items()]
    # the holdout has no archived call: the request is built the same way (ledger-blind, no theses, no groups); its tokens are
    # estimated from the text length (one token per 3.2 characters, the week's ratio) with the week's median output
    median_out = sorted(r[3] for r in rows.values())[len(rows) // 2]
    jobs += [(None, h['input_id'], None, int(h['chars'] / 3.2) + 2600, median_out, False) for h in holdout]
    for call_id, input_id, sha, tin, tout, is_archived in jobs:
        item, uni, setting, schema, request, cfg = build(input_id)
        identity = model.request_identity(request)[1]
        if is_archived:
            assert identity == sha, (input_id, identity, sha)
        assert request['model'] == 'gpt-6-luna'
        haiku = to_haiku(request, schema)
        assert wire(schema) == wire(haiku['output_config']['format']['schema'])
        manifest['items'].append({'call_id': call_id, 'input_id': input_id, 'request_sha256': identity, 'archived': is_archived,
                                  'set': 'week' if is_archived else 'holdout', 'category': item['category'],
                                  'day': item['publication_day'], 'text_sha256': digest_bytes(item['text'].encode()),
                                  'archived_tokens': [tin, tout], 'max_tokens': request['max_completion_tokens'], 'haiku_request_sha256': digest_bytes(wire(haiku))})
        # reserve: (archived or estimated) input tokens x 1.5 and the full output ceiling per draw, both models
        for name, (pin, pout) in PRICES.items():
            reserve += DRAWS * (tin * 1.5 * pin + request['max_completion_tokens'] * pout) / 1e6
    manifest['reserve_usd_upper_bound'] = round(reserve, 4)
    manifest['expected_usd_at_archived_tokens'] = round(sum(DRAWS * (tin * pin + tout * pout) / 1e6
                                                            for (_, _, _, tin, tout, _) in jobs for (pin, pout) in PRICES.values()), 4)
    (RUN / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + '\n')
    print('prepared', len(manifest['items']), 'items; expected USD', manifest['expected_usd_at_archived_tokens'],
          'upper bound', manifest['reserve_usd_upper_bound'])


def verify():
    manifest = json.loads((RUN / 'manifest.json').read_text())
    conn = sqlite3.connect(f'file:{ARCHIVE}?mode=ro', uri=True)
    for entry in manifest['items']:
        item, uni, setting, schema, request, cfg = build(entry['input_id'])
        assert model.request_identity(request)[1] == entry['request_sha256']
        if entry['archived']:
            assert conn.execute('select count(*) from model_calls where request_sha256=?', (entry['request_sha256'],)).fetchone()[0] == 1
        assert digest_bytes(wire(to_haiku(request, schema))) == entry['haiku_request_sha256']
        assert digest_bytes(item['text'].encode()) == entry['text_sha256']
    info = haiku_api(f'https://api.anthropic.com/v1/models/{HAIKU}')
    n_week = sum(1 for e in manifest['items'] if e['archived'])
    print('verified', n_week, 'week requests byte-identical to the archive,', len(manifest['items']) - n_week, 'holdout requests built the same way; model', info.get('id'), 'reachable')


def store():
    conn = sqlite3.connect(RUN / 'answers.sqlite')
    conn.execute('create table if not exists answers (provider text, draw integer, input_id text, request_sha256 text, response_json text,'
                 ' content text, completed integer, input_tokens integer, output_tokens integer, seconds real, error text,'
                 ' primary key (provider, draw, input_id))')
    return conn


def one(job):
    provider, draw, entry = job
    item, uni, setting, schema, request, cfg = build(entry['input_id'])
    start = time.monotonic()
    error = None
    response = content = None
    completed = 0
    tin = tout = None
    try:
        if provider == 'haiku':
            response = haiku_api('https://api.anthropic.com/v1/messages', to_haiku(request, schema))
            completed = int(response.get('stop_reason') == 'end_turn')
            content = ''.join(c.get('text', '') for c in response.get('content', []) if c.get('type') == 'text')
            usage = response.get('usage', {})
            tin, tout = usage.get('input_tokens'), usage.get('output_tokens')
        else:
            response = model.openai_transport(cfg.provider, request)   # the bytes production sends
            choice = response['choices'][0]
            completed = int(choice['finish_reason'] == 'stop')
            content = choice['message'].get('content') or ''
            usage = response.get('usage', {})
            tin, tout = usage.get('prompt_tokens'), usage.get('completion_tokens')
    except urllib.error.HTTPError as exc:
        error = f'HTTP {exc.code}'
    except Exception as exc:  # noqa: BLE001  (a paid answer is never lost to a bookkeeping error)
        error = type(exc).__name__
    seconds = round(time.monotonic() - start, 2)
    with LOCK:
        conn = store()
        conn.execute('insert or replace into answers values (?,?,?,?,?,?,?,?,?,?,?)',
                     (provider, draw, entry['input_id'], entry['request_sha256'], json.dumps(response), content, completed, tin, tout, seconds, error))
        conn.commit()
        conn.close()
    print(provider, draw, entry['input_id'][:40], 'completed' if completed else 'INCOMPLETE', error or '', seconds, flush=True)


def send(providers=('luna', 'haiku')):
    manifest = json.loads((RUN / 'manifest.json').read_text())
    done = set()
    if (RUN / 'answers.sqlite').exists():
        conn = store()
        done = {tuple(r) for r in conn.execute('select provider, draw, input_id from answers where error is null and completed=1')}
        conn.close()
    jobs = [(p, d, e) for p in providers for d in range(1, DRAWS + 1) for e in manifest['items'] if (p, d, e['input_id']) not in done]
    print('sending', len(jobs), 'jobs;', len(done), 'already stored', flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        list(pool.map(one, jobs))
    conn = store()
    for row in conn.execute('select provider, count(*), sum(completed), sum(error is not null), sum(input_tokens), sum(output_tokens) from answers group by provider'):
        print('stored', row)


def sift():
    manifest = json.loads((RUN / 'manifest.json').read_text())
    conn = store()
    out = {}
    for provider, draw, input_id, content, completed, error in conn.execute('select provider, draw, input_id, content, completed, error from answers order by provider, draw, input_id'):
        key = f'{provider}-{draw}'
        record = {'completed': bool(completed), 'error': error, 'answer': None, 'schema_errors': None, 'sift': None}
        item, uni, setting, schema, request, cfg = build(input_id)
        try:
            answer = json.loads(content) if content else None
        except ValueError:
            answer = None
        record['answer'] = answer
        if answer is not None:
            record['schema_errors'] = model.check_schema(answer, schema)
            if completed and not record['schema_errors']:
                e, c, d, g = extraction.sift_with_groups(answer, item, item['text'], set(), uni, english=True, shown_group_ids=(),
                                                         version='22', keep_unlinked=True)
                record['sift'] = {'evidence': e, 'candidates': c, 'dropped': d, 'new_groups': g}
        out.setdefault(key, {})[input_id] = record
    (RUN / 'sifted.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    for key, items in out.items():
        n = len(items); ok = sum(1 for r in items.values() if r['sift'] is not None)
        ev = sum(len(r['sift']['evidence']) for r in items.values() if r['sift'])
        ca = sum(len(r['sift']['candidates']) for r in items.values() if r['sift'])
        dr = sum(len(r['sift']['dropped']) for r in items.values() if r['sift'])
        print(key, 'items', n, 'sifted', ok, 'evidence', ev, 'candidates', ca, 'dropped', dr)


if __name__ == '__main__':
    command = sys.argv[1]
    if command == 'send':
        send(tuple(sys.argv[2:]) or ('luna', 'haiku'))
    else:
        {'prepare': prepare, 'verify': verify, 'sift': sift}[command]()
