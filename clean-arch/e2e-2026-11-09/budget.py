"""A hard spending limit for the D392 measurement harnesses, independent of production's own cap (replay.run checks its cap only after
an item or a day finishes, with calls already in flight).

Every model attempt is sent alone (`model.openai_transport(..., max_attempts=1)`) and the limit applies production's retry rule around
it: up to three attempts, no retry after HTTP 400/401/403/404 or an undecodable answer, waits of 5 s and then 10 s. Before an attempt is
sent it reserves its worst case under a lock (every request character priced as an uncached input token at the request model's
published rate, plus the request's output cap) and is refused if spent plus in flight plus the reserve would pass the cap. Afterwards,
in the same locked step, the reserve is released and the attempt is charged: its cost from tokens when it answered with usable token
counts, its full reserve otherwise (a lost answer, or one without usage, may still be billed).

A Jev call (one argument, as replay.run passes one transport to both) goes through `jev.transport`, which retries inside itself out of
sight, so it reserves and is always charged three attempts of its input at Jev's input rate (its output is free).

Called as a transport: (provider, request) for a model call, (request,) for a Jev call."""
import json, sys, threading, time
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parents[2] / 'src')]
from hivemind import jev, model  # noqa: E402

ATTEMPTS = 3                                # model.openai_transport's default max_attempts
NOT_RETRIED = (400, 401, 403, 404)          # model.openai_transport raises these at once
UNDECODABLE = ('invalid UTF-8 HTTP response', 'malformed HTTP response')   # raised at once by production too


class OverBudget(Exception):
    pass


def worst_cost(request):
    """The body as sent (json.dumps, non-ASCII escaped) is at least as long in bytes as the UTF-8 text it carries, and a byte-level
    tokenizer emits at most one token per byte; the JSON keys and syntax in the body more than cover the chat template's few tokens.
    Rates are model.PRICES, the published rates (AGENTS §7.2)."""
    input_rate, output_rate = model.PRICES[request['model']]
    output_cap = request.get('max_completion_tokens') or request.get('max_tokens')
    if not output_cap:
        raise OverBudget(f"a request to {request['model']} has no output cap, so its worst cost is unbounded")
    return (len(json.dumps(request).encode('utf-8')) * input_rate + output_cap * output_rate) / 1e6


def cost(request, response):
    """The answer's cost from its reported tokens; None when the answer reports no usable token counts."""
    usage = response.get('usage') if isinstance(response, dict) else None
    counts = [usage.get(name) for name in ('prompt_tokens', 'completion_tokens')] if isinstance(usage, dict) else [None, None]
    if not all(isinstance(count, int) and not isinstance(count, bool) and count >= 0 for count in counts):
        return None
    cached = (usage.get('prompt_tokens_details') or {}).get('cached_tokens') or usage.get('prompt_cache_hit_tokens') or 0
    input_rate, output_rate = model.PRICES[request['model']]
    fresh = counts[0] - min(cached, counts[0])
    return (fresh * input_rate + min(cached, counts[0]) * input_rate * model.CACHED_INPUT_SHARE + counts[1] * output_rate) / 1e6


class Budget:
    def __init__(self, cap_usd, attempt=None, sleep=time.sleep, jev_transport=None):
        """attempt(provider, request) sends one attempt; the default is the production transport with a single attempt.
        jev_transport(request) sends a Jev call; the default is production's."""
        self.cap_usd, self.spent_usd, self.reserved_usd = cap_usd, 0.0, 0.0
        self.attempt = attempt or (lambda provider, request: model.openai_transport(provider, request, max_attempts=1))
        self.jev_transport = jev_transport or jev.transport
        self.sleep = sleep
        self.lock = threading.Lock()

    def send(self, provider, request):
        reserve = worst_cost(request)
        for attempt_number in range(ATTEMPTS):
            with self.lock:
                if self.spent_usd + self.reserved_usd + reserve > self.cap_usd:
                    raise OverBudget(f'spent ${self.spent_usd:.4f}, ${self.reserved_usd:.4f} in flight; '
                                     f'${reserve:.4f} more would pass the ${self.cap_usd:.2f} cap')
                self.reserved_usd += reserve
            response, failure = None, None
            try:
                response = self.attempt(provider, request)
            except model.TransportError as error:
                failure = error
            finally:
                with self.lock:   # one step: the reserve is released only as the attempt is charged
                    self.reserved_usd -= reserve
                    charged = cost(request, response) if response is not None else None
                    self.spent_usd += reserve if charged is None else charged   # no answer, or no usable usage: the full reserve
            if response is not None:
                return response
            retried = getattr(failure, 'http_status', None) not in NOT_RETRIED and str(failure) not in UNDECODABLE
            if not retried or attempt_number + 1 == ATTEMPTS:
                raise failure
            self.sleep(5 * (attempt_number + 1))

    def send_jev(self, request):
        input_rate, _ = model.PRICES[request['model']]
        charge = ATTEMPTS * len(json.dumps(request, sort_keys=True, ensure_ascii=False).encode('utf-8')) * input_rate / 1e6   # jev.transport's body bytes
        with self.lock:
            if self.spent_usd + self.reserved_usd + charge > self.cap_usd:
                raise OverBudget(f'spent ${self.spent_usd:.4f}, ${self.reserved_usd:.4f} in flight; a Jev call of ${charge:.4f} would pass '
                                 f'the ${self.cap_usd:.2f} cap')
            self.spent_usd += charge
        return self.jev_transport(request)

    def __call__(self, *arguments):
        return self.send(*arguments) if len(arguments) == 2 else self.send_jev(*arguments)
