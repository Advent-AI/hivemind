"""A probe transport for Claude models (Alex, 2026-11-16: "你试试看opus"): it takes the request the ladder step builds in OpenAI's
shape and sends it to Anthropic's Messages API, then returns the answer in the shape `model.call` reads. Production code is unchanged.

- The request: the same system text, user message and output cap; the step's reasoning effort as `output_config.effort`; the step's JSON
  schema as `output_config.format`, less the keywords Anthropic's structured outputs do not take. `model.call` still validates the full
  schema, as the SDKs do client-side.
- The key is `ANTHROPIC_API_KEY`, from the environment or the owner-only `~/.config/hivemind/credentials.json`, as `model._key` reads
  OpenAI's. It is never printed or logged.
- An HTTP error raises `model.TransportError` with its `http_status`, so the budget's retry rule applies as for OpenAI.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'src'))
from hivemind import model  # noqa: E402

ENDPOINT = 'https://api.anthropic.com/v1/messages'
API_VERSION = '2026-10-21'                 # the claude-api skill's required `anthropic-version`
KEY_NAME = 'ANTHROPIC_API_KEY'
NOT_TAKEN = {'pattern', 'minLength', 'maxLength', 'minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum', 'multipleOf',
             'minItems', 'maxItems', 'uniqueItems'}     # the skill's "Not supported" list; validated client-side by model.call


def api_schema(schema):
    """The schema with the keywords structured outputs do not take removed, at every depth."""
    if isinstance(schema, dict):
        return {key: api_schema(value) for key, value in schema.items() if key not in NOT_TAKEN}
    if isinstance(schema, list):
        return [api_schema(item) for item in schema]
    return schema


def to_anthropic(request):
    messages = request['messages']
    if len(messages) != 2 or messages[0]['role'] != 'system' or messages[1]['role'] != 'user':
        raise ValueError('the adapter takes the step\'s two-message request: one system, one user')
    return {'model': request['model'], 'max_tokens': request['max_completion_tokens'], 'system': messages[0]['content'],
            'messages': [{'role': 'user', 'content': messages[1]['content']}],
            'output_config': {'effort': request.get('reasoning_effort') or 'medium',
                              'format': {'type': 'json_schema', 'schema': api_schema(request['response_format']['json_schema']['schema'])}}}


def from_anthropic(data):
    """The Messages API answer as `model.call` reads one: the text blocks joined, the token counts with cache reads as cached input."""
    text = ''.join(block.get('text', '') for block in data.get('content', []) if block.get('type') == 'text')
    usage = data.get('usage') or {}
    cache_read = int(usage.get('cache_read_input_tokens') or 0)
    prompt = int(usage.get('input_tokens') or 0) + cache_read + int(usage.get('cache_creation_input_tokens') or 0)
    return {'choices': [{'message': {'content': text}, 'finish_reason': data.get('stop_reason')}],
            'usage': {'prompt_tokens': prompt, 'completion_tokens': int(usage.get('output_tokens') or 0),
                      'prompt_tokens_details': {'cached_tokens': cache_read}},
            'model': data.get('model'), 'stop_reason': data.get('stop_reason')}


def key():
    if os.environ.get(KEY_NAME):
        return os.environ[KEY_NAME]
    with open(model.CREDENTIALS, encoding='utf-8') as handle:
        credentials = json.load(handle)
    if KEY_NAME not in credentials:
        raise model.TransportError(f'no {KEY_NAME} in the environment or the credentials file')
    return credentials[KEY_NAME]


def send(provider, request, *, opener=urllib.request.urlopen, timeout=300):
    body = json.dumps(to_anthropic(request)).encode('utf-8')
    headers = {'x-api-key': key(), 'anthropic-version': API_VERSION, 'content-type': 'application/json'}
    try:
        with opener(urllib.request.Request(ENDPOINT, data=body, headers=headers, method='POST'), timeout=timeout) as response:
            data = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as error:
        detail = error.read().decode('utf-8', 'replace')[:300]
        failure = model.TransportError(f'{error.code} {error.reason}: {detail}')
        failure.http_status = error.code
        raise failure from None
    return from_anthropic(data)


def route(provider, request):
    """Claude models through this adapter; any other model through OpenAI's transport, one attempt (the budget retries)."""
    if request['model'].startswith('claude-'):
        return send(provider, request)
    return model.openai_transport(provider, request, max_attempts=1)
