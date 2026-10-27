"""One model call, archived and replayable.

`call()` sends a system and user message with a strict JSON schema to an OpenAI-compatible chat endpoint (OpenAI,
or DeepSeek through the same wire format), checks the answer against the schema, and records the exact request and
raw answer in an archive (SQLite, a POC artefact kept beside the test database, never inside the views database).
A request whose sha256 is already in the archive is answered from it without a network call, so a rerun of a
replay costs nothing and gives the same answers. The provider key is read from the owner-only credentials file and
never appears in the archive, logs or arguments.
"""
import dataclasses
import hashlib
import http.client
import json
import re
import os
import sqlite3
import time
import uuid
import urllib.error
import urllib.request

CREDENTIALS = os.path.expanduser('~/.config/hivemind/credentials.json')
ENDPOINTS = {'openai': ('https://api.openai.com/v1/chat/completions', 'OPENAI_API_KEY'),
             'deepseek': ('https://api.deepseek.com/chat/completions', 'DEEPSEEK_API_KEY')}
# USD per million tokens, for the cost column only (an estimate; the provider's bill is the measurement)
# gpt-6-luna: the published standard rates on 2026-10-25 (developers.openai.com/api/docs/models/gpt-6-luna: $0.10/M input, $0.50/M output,
# cached input $0.01/M). Until this date the table carried (1.25, 10.0), so every cost_usd recorded before it is 12.5x (input) to 20x (output)
# the published rate; the token columns are the measurement, the bill is the provider's.
PRICES = {'gpt-6-luna': (0.10, 0.50), 'deepseek-flash': (0.30, 1.20), 'deepseek-v4-pro': (1.32, 3.96),
          'jev-1.14.0': (0.042, 0.0)}   # Jev: docs.typesafe.ai/models, 2026-10-25; output free   # DeepSeek: peak-hour list prices, cache misses (2026-10-23 pricing page)
CACHED_INPUT_SHARE = 0.10          # cached input tokens are priced at 10% of the input rate (gpt-6-luna page, read again 2026-10-27)

SCHEMA_SQL = """
create table if not exists model_calls (
  call_id integer primary key autoincrement, purpose text, config_version text, config_checksum text, model text,
  request_sha256 text unique, request_json text, response_json text, answer_json text, prompt_chars integer,
  input_tokens integer, output_tokens integer, cost_usd real, seconds real, created_at text
);
create index if not exists model_calls_sha on model_calls(request_sha256);
"""


class SchemaError(ValueError):
    pass


class TransportError(RuntimeError):
    pass


@dataclasses.dataclass
class Answer:
    data: dict
    call_id: int
    request_sha256: str
    cached: bool
    prompt_chars: int
    input_tokens: int
    output_tokens: int
    cost_usd: float


class Archive:
    """Shared by the extraction worker threads: one connection, every access under a lock."""

    def __init__(self, path):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.executescript(SCHEMA_SQL)
        import threading
        self.lock = threading.Lock()

    def lookup(self, sha):
        with self.lock:
            return self.conn.execute('select call_id, answer_json, prompt_chars, input_tokens, output_tokens from model_calls where request_sha256=?', (sha,)).fetchone()

    def record(self, **fields):
        """One row per distinct request; a second identical request recorded at the same moment (two threads, or a
        failed answer repeated within the same second) keeps the first row's id instead of failing."""
        columns = list(fields)
        with self.lock:
            cursor = self.conn.execute(f'insert or ignore into model_calls ({",".join(columns)}) values ({",".join("?" * len(columns))})',
                                       [fields[c] for c in columns])
            self.conn.commit()
            if cursor.rowcount == 0:
                return self.conn.execute('select call_id from model_calls where request_sha256=?', (fields['request_sha256'],)).fetchone()[0]
            return cursor.lastrowid

    def retire(self, call_id):
        """A code check refused this answer: the row stays for the record, but no later identical request is answered with it
        (the same shape as a schema-refused or malformed row, whose hash carries a suffix)."""
        with self.lock:
            self.conn.execute("update model_calls set request_sha256 = request_sha256 || ':refused:' || ? where call_id=? and request_sha256 not like '%:refused:%'",
                              (uuid.uuid4().hex[:8], call_id))
            self.conn.commit()

    def totals(self):
        with self.lock:
            return self.conn.execute('select count(*), coalesce(sum(cost_usd),0), coalesce(sum(input_tokens),0), coalesce(sum(output_tokens),0) from model_calls').fetchone()


def _key(provider):
    name = ENDPOINTS[provider][1]
    if os.environ.get(name):
        return os.environ[name]
    with open(CREDENTIALS, encoding='utf-8') as handle:
        return json.load(handle)[name]


def build_request(setting, system, user, schema, schema_name, provider):
    request = {
        'model': setting.model,
        'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}],
        'response_format': {'type': 'json_schema', 'json_schema': {'name': schema_name, 'strict': True, 'schema': schema}},
    }
    if provider == 'openai':
        # gpt-6-luna is a reasoning model: it refuses any temperature but the default, so the setting's temperature
        # is recorded in Config but not sent; reasoning_effort is what steers it.
        request['max_completion_tokens'] = setting.max_output_tokens
        if setting.reasoning_effort:
            request['reasoning_effort'] = setting.reasoning_effort
    else:
        request['temperature'] = setting.temperature
        request['max_tokens'] = setting.max_output_tokens
    return request


def openai_transport(provider, request, timeout=600):
    url, _ = ENDPOINTS[provider]
    body = json.dumps(request).encode('utf-8')
    headers = {'Authorization': f'Bearer {_key(provider)}', 'Content-Type': 'application/json'}
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=body, headers=headers, method='POST'), timeout=timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as error:
            text = error.read().decode('utf-8', 'ignore')[:600]
            last = f'HTTP {error.code}: {text}'
            if error.code in (400, 401, 403, 404):
                raise TransportError(last)
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError, http.client.HTTPException) as error:   # a dropped or truncated response is retried like a network error
            last = repr(error)[:200]
        time.sleep(5 * (attempt + 1))
    raise TransportError(last or 'no answer')


def check_schema(value, schema, path='$', root=None):
    """A small validator for the subset of JSON Schema the prompts use: object/required/additionalProperties,
    array/items/minItems, string/enum/pattern, integer, number, boolean, null in anyOf, and $ref into the root's $defs."""
    root = root if root is not None else schema
    if '$ref' in schema:
        name = schema['$ref'].rsplit('/', 1)[1]
        schema = root['$defs'][name]
    kind = schema.get('type')
    if 'anyOf' in schema:
        errors = []
        for option in schema['anyOf']:
            errors = check_schema(value, option, path, root)
            if not errors:
                return []
        return errors or [f'{path}: matches no option']
    if kind == 'object':
        if not isinstance(value, dict):
            return [f'{path}: expected object']
        errors = []
        for name in schema.get('required', []):
            if name not in value:
                errors.append(f'{path}.{name}: required')
        properties = schema.get('properties', {})
        for name, item in value.items():
            if name in properties:
                errors.extend(check_schema(item, properties[name], f'{path}.{name}', root))
            elif schema.get('additionalProperties') is False:
                errors.append(f'{path}.{name}: not allowed')
        return errors
    if kind == 'array':
        if not isinstance(value, list):
            return [f'{path}: expected array']
        errors = []
        if len(value) < schema.get('minItems', 0):
            errors.append(f'{path}: fewer than {schema["minItems"]} items')
        for index, item in enumerate(value):
            errors.extend(check_schema(item, schema.get('items', {}), f'{path}[{index}]', root))
        return errors
    if kind == 'string':
        if not isinstance(value, str):
            return [f'{path}: expected string']
        if 'enum' in schema and value not in schema['enum']:
            return [f'{path}: {value!r} not in {schema["enum"]}']
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            return [f'{path}: {value!r} does not match {schema["pattern"]}']
        return []
    if kind == 'integer':
        return [] if isinstance(value, int) and not isinstance(value, bool) else [f'{path}: expected integer']
    if kind == 'number':
        return [] if isinstance(value, (int, float)) and not isinstance(value, bool) else [f'{path}: expected number']
    if kind == 'boolean':
        return [] if isinstance(value, bool) else [f'{path}: expected boolean']
    if kind == 'null':
        return [] if value is None else [f'{path}: expected null']
    return []


def request_identity(request):
    """The exact serialized request and its archive key, shared by callers and validation."""
    encoded = json.dumps(request, sort_keys=True, ensure_ascii=False)
    return encoded, hashlib.sha256(encoded.encode('utf-8')).hexdigest()


def call(archive, cfg, setting, system, user, schema, schema_name, purpose, *, transport=None):
    provider = cfg.provider
    request = build_request(setting, system, user, schema, schema_name, provider)
    request_json, sha = request_identity(request)
    hit = archive.lookup(sha)
    prompt_chars = len(system) + len(user)
    if hit:
        call_id, answer_json, _, input_tokens, output_tokens = hit
        return Answer(json.loads(answer_json), call_id, sha, True, prompt_chars, input_tokens or 0, output_tokens or 0, 0.0)
    started = time.time()
    response = (transport or openai_transport)(provider, request)
    seconds = round(time.time() - started, 1)
    try:
        content = response['choices'][0]['message']['content']
        data = json.loads(content)
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
        archive.record(purpose=purpose, config_version=cfg.version, config_checksum=cfg.checksum, model=setting.model,
                       request_sha256=sha + ':malformed:' + uuid.uuid4().hex[:8], request_json=request_json,
                       response_json=json.dumps(response)[:200000], answer_json=None, prompt_chars=prompt_chars,
                       input_tokens=0, output_tokens=0, cost_usd=0.0, seconds=seconds, created_at=time.strftime('%Y-%m-%dT%H:%M:%S'))
        raise SchemaError(f'malformed answer: {error}')
    errors = check_schema(data, schema)
    usage = response.get('usage') or {}
    input_tokens = int(usage.get('prompt_tokens') or 0)
    output_tokens = int(usage.get('completion_tokens') or 0)
    cached_tokens = min(input_tokens, int((usage.get('prompt_tokens_details') or {}).get('cached_tokens') or 0))
    price_in, price_out = PRICES.get(setting.model, (0.0, 0.0))
    cost = round((input_tokens - cached_tokens) / 1e6 * price_in + cached_tokens / 1e6 * price_in * CACHED_INPUT_SHARE + output_tokens / 1e6 * price_out, 6)
    call_id = archive.record(purpose=purpose, config_version=cfg.version, config_checksum=cfg.checksum, model=setting.model,
                             request_sha256=sha if not errors else sha + ':schema:' + uuid.uuid4().hex[:8], request_json=request_json,
                             response_json=json.dumps(response)[:200000], answer_json=json.dumps(data, ensure_ascii=False),
                             prompt_chars=prompt_chars, input_tokens=input_tokens, output_tokens=output_tokens, cost_usd=cost,
                             seconds=seconds, created_at=time.strftime('%Y-%m-%dT%H:%M:%S'))
    if errors:
        raise SchemaError('; '.join(errors[:5]))
    return Answer(data, call_id, sha, False, prompt_chars, input_tokens, output_tokens, cost)
