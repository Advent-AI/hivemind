"""The Claude adapter at $0: the request it sends, the answer it returns, its errors and its routing, with a fake opener (no network)."""
import io
import json
import sys
import urllib.error
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import anthropic_adapter as adapter  # noqa: E402

REQUEST = {'model': 'claude-opus-5-5', 'max_completion_tokens': 20000, 'reasoning_effort': 'medium',
           'messages': [{'role': 'system', 'content': 'You are a senior analyst.'}, {'role': 'user', 'content': 'The topic …'}],
           'response_format': {'type': 'json_schema', 'json_schema': {'name': 'clean_ladder', 'strict': True, 'schema': {
               'type': 'object', 'additionalProperties': False, 'required': ['question'],
               'properties': {'question': {'type': 'string', 'pattern': '\\S', 'minLength': 1},
                              'items': {'type': 'array', 'minItems': 5, 'maxItems': 5, 'items': {'type': 'string'}}}}}}}
ANSWER = {'model': 'claude-opus-5-5', 'stop_reason': 'end_turn',
          'content': [{'type': 'thinking', 'thinking': ''}, {'type': 'text', 'text': '{"question": "Will it close?"}'}],
          'usage': {'input_tokens': 300, 'cache_read_input_tokens': 4800, 'cache_creation_input_tokens': 0, 'output_tokens': 900}}


class Opener:
    def __init__(self, answer=None, error=None):
        self.answer, self.error, self.seen = answer, error, []

    def __call__(self, request, timeout):
        self.seen.append(request)
        if self.error:
            raise self.error
        return io.BytesIO(json.dumps(self.answer).encode())


def test_the_request_carries_the_same_texts_effort_and_schema_without_untaken_keywords(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'test-key-not-real')
    opener = Opener(ANSWER)
    adapter.send('openai', REQUEST, opener=opener)
    sent = opener.seen[0]
    body = json.loads(sent.data)
    assert sent.full_url == adapter.ENDPOINT and sent.get_header('X-api-key') == 'test-key-not-real'
    assert sent.get_header('Anthropic-version') == adapter.API_VERSION
    assert body['system'] == 'You are a senior analyst.' and body['messages'] == [{'role': 'user', 'content': 'The topic …'}]
    assert body['max_tokens'] == 20000 and body['output_config']['effort'] == 'medium'
    schema = body['output_config']['format']['schema']
    assert 'pattern' not in json.dumps(schema) and 'minItems' not in json.dumps(schema) and schema['additionalProperties'] is False


def test_the_answer_is_returned_in_the_shape_model_call_reads(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'test-key-not-real')
    response = adapter.send('openai', REQUEST, opener=Opener(ANSWER))
    assert response['choices'][0]['message']['content'] == '{"question": "Will it close?"}'
    assert response['usage'] == {'prompt_tokens': 5100, 'completion_tokens': 900, 'prompt_tokens_details': {'cached_tokens': 4800}}


def test_an_http_error_raises_a_transport_error_with_its_status(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'test-key-not-real')
    error = urllib.error.HTTPError(adapter.ENDPOINT, 400, 'Bad Request', {}, io.BytesIO(b'{"error": "schema"}'))
    with pytest.raises(adapter.model.TransportError) as caught:
        adapter.send('openai', REQUEST, opener=Opener(error=error))
    assert caught.value.http_status == 400


def test_a_missing_key_refuses_before_any_send(monkeypatch, tmp_path):
    monkeypatch.delenv('ANTHROPIC_API_KEY', raising=False)
    (tmp_path / 'credentials.json').write_text(json.dumps({'OPENAI_API_KEY': 'x'}))
    monkeypatch.setattr(adapter.model, 'CREDENTIALS', str(tmp_path / 'credentials.json'))
    opener = Opener(ANSWER)
    with pytest.raises(adapter.model.TransportError, match='no ANTHROPIC_API_KEY'):
        adapter.send('openai', REQUEST, opener=opener)
    assert opener.seen == []


def test_only_claude_models_are_routed_to_the_adapter(monkeypatch):
    calls = []
    monkeypatch.setattr(adapter, 'send', lambda provider, request: calls.append('claude') or {})
    monkeypatch.setattr(adapter.model, 'openai_transport', lambda provider, request, max_attempts: calls.append('openai') or {})
    adapter.route('openai', REQUEST)
    adapter.route('openai', dict(REQUEST, model='gpt-6-luna'))
    assert calls == ['claude', 'openai']
