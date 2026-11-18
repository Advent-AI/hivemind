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


NETWORK_ATTEMPTS = 3          # as production's transport (model.openai_transport): a dropped connection is tried up to three times
NETWORK_WAITS = (30, 60)      # seconds before the second and the third attempt
CALL_WAIT_SECONDS = 600       # the longest a call may wait on a silent connection before it counts as lost (D552)


def is_network_loss(error):
    """A send that brought no usable answer from the network: a TransportError with no HTTP status (reset, cut read, timeout), or 429 or 5xx."""
    if not isinstance(error, model.TransportError):
        return False
    status = getattr(error, 'http_status', None)
    return status is None or status == 429 or status >= 500


class LiveTransport:
    """With `ledger` (an object with `reserve(amount) -> bool` and `settle(reserved, actual)`, shared by every component of a run;
    D448), each attempt reserves its estimate on the ledger before it is sent and settles at the response's usage (its reservation when
    usage is missing or the send fails), and the cumulative `max_usd` check is not applied. Each network attempt is one send
    (`max_attempts=1`); a network loss (`is_network_loss`) is sent again, up to NETWORK_ATTEMPTS in all after NETWORK_WAITS, every attempt
    checked against the time and call limits and reserved and settled on its own; `network_errors` holds the losses of the last call, for
    the trace. A send waits on its connection for at most CALL_WAIT_SECONDS, or the run's remaining time when that is less: a
    connection that goes silent (the machine slept, the network dropped without an error) then times out and is a network loss
    like any other. The bound is on each wait for data, not on the whole call: an answer that keeps arriving is never cut.
    A resend may be a fresh sample (the provider may have produced an answer that never arrived). Anything else is raised."""

    def __init__(self, limits, send=None, clock=time.monotonic, ledger=None, wait=time.sleep):
        self.ledger = ledger
        self.wait = wait
        self.network_errors = []
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
        self.network_errors = []
        for attempt in range(NETWORK_ATTEMPTS):
            remaining = self.limits['max_seconds'] - (self.clock() - self.start)
            over_dollars = self.ledger is None and self.reserved + estimated > self.limits['max_usd']
            if remaining <= 0 or self.calls >= self.limits['max_calls'] or over_dollars:
                raise ValueError('live run limit reached before send')
            if self.ledger is not None and not self.ledger.reserve(estimated):
                raise ValueError('live run limit reached before send: the shared ledger refused')
            self.reserved += estimated
            self.calls += 1
            self.on_reserve(self.reserved)
            self.last_sent = request
            try:
                response = self.send(provider, request, timeout=min(remaining, CALL_WAIT_SECONDS), max_attempts=1)
            except BaseException as error:
                if self.ledger is not None:
                    self.ledger.settle(estimated, estimated)
                if attempt + 1 < NETWORK_ATTEMPTS and is_network_loss(error):
                    self.network_errors.append(f'attempt {attempt + 1}: {type(error).__name__}: {error}')
                    self.wait(NETWORK_WAITS[attempt])
                    continue
                raise
            if self.ledger is not None:
                self.ledger.settle(estimated, ledger_cost(request, response, estimated))
            return response


def ledger_cost(request, response, estimated):
    """A response's cost at the published rates (`model.PRICES`), every input token at the full input rate; its reservation when the
    usage is missing or not whole token counts."""
    usage = response.get('usage') if isinstance(response, dict) else None
    tokens_in = usage.get('prompt_tokens') if isinstance(usage, dict) else None
    tokens_out = usage.get('completion_tokens') if isinstance(usage, dict) else None
    if not all(isinstance(n, int) and not isinstance(n, bool) and n >= 0 for n in (tokens_in, tokens_out)) or request.get('model') not in model.PRICES:
        return estimated
    price_in, price_out = model.PRICES[request['model']]
    return (tokens_in * price_in + tokens_out * price_out) / 1_000_000
