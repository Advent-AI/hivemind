"""Budgeted use of the repository's existing transport for OpenAI Luna and, in JSON mode, DeepSeek."""
import json
import math
import time

from hivemind import model


SUPPORTED = {('openai', 'gpt-6-luna'), ('deepseek', 'deepseek-flash'), ('deepseek', 'deepseek-v4-pro')}


def deepseek_json_mode(request, reasoning_effort):
    """DeepSeek refuses a strict JSON schema: the same schema is stated at the end of the system text and JSON mode is requested.
    model.call still checks the answer against the schema, so a nonconforming answer fails the item and is never repaired."""
    schema = request['response_format']['json_schema']['schema']
    messages = [dict(m) for m in request['messages']]
    messages[0]['content'] += '\n\nReturn only one JSON object that conforms to this JSON Schema:\n' + json.dumps(schema)
    adapted = dict(request, messages=messages, response_format={'type': 'json_object'})
    if reasoning_effort:
        adapted['reasoning_effort'] = reasoning_effort
    return adapted


class LiveTransport:
    def __init__(self, limits, send=None, clock=time.monotonic):
        self.clock = clock
        self.start = clock()
        self.limits = limits
        self.send = send or model.openai_transport
        self.reserved = 0.0
        self.calls = 0
        self.on_reserve = lambda reserved: None
        self.reasoning_effort = None   # sent to DeepSeek; build_request sets it for OpenAI only
        self.last_sent = None          # the exact request sent, after any provider adaptation
        for key in ('max_usd', 'max_seconds', 'max_calls', 'input_usd_per_million', 'output_usd_per_million'):
            if isinstance(limits[key], bool) or not isinstance(limits[key], (int, float)) or not math.isfinite(limits[key]) or limits[key] <= 0:
                raise ValueError(f'{key} must be positive')
        if not isinstance(limits['max_calls'], int):
            raise ValueError('max_calls must be an integer')

    def __call__(self, provider, request):
        if (provider, request.get('model')) not in SUPPORTED:
            raise ValueError('live transport supports OpenAI gpt-6-luna and DeepSeek flash or v4-pro only')
        if provider == 'deepseek':
            request = deepseek_json_mode(request, self.reasoning_effort)
        output_cap = request.get('max_completion_tokens', request.get('max_tokens'))
        if isinstance(output_cap, bool) or not isinstance(output_cap, int) or not 0 < output_cap <= 128000:
            raise ValueError('max_completion_tokens must be a positive integer within the model limit')
        # Use the same serialization as model.openai_transport; reservation is not a bill guarantee.
        estimated_input = 2 * len(json.dumps(request).encode('utf-8')) + 4096
        estimated = (estimated_input * self.limits['input_usd_per_million'] +
                     output_cap * self.limits['output_usd_per_million']) / 1_000_000
        if not math.isfinite(estimated) or estimated <= 0:
            raise ValueError('invalid estimated reservation')
        remaining = self.limits['max_seconds'] - (self.clock() - self.start)
        if remaining <= 0 or self.calls >= self.limits['max_calls'] or self.reserved + estimated > self.limits['max_usd']:
            raise ValueError('live run limit reached before send')
        self.reserved += estimated
        self.calls += 1
        self.on_reserve(self.reserved)
        self.last_sent = request
        return self.send(provider, request, timeout=remaining, max_attempts=1)
