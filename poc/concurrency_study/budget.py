"""Conservative admission and single-attempt HTTP for the isolated API study."""
import http.client
import json
from pathlib import Path
import sqlite3
import threading
import time
import urllib.error
import urllib.request

from hivemind import jev, model


class BudgetError(RuntimeError):
    pass


class RetryableError(model.TransportError):
    """No usable reply arrived (network failure, rate limit or server error); the attempt's usage stays unknown."""


def envelope(provider, request):
    """Reserve documented maximum usage, without guessing tokens from characters."""
    if provider == 'openai' and request.get('model') == 'gpt-6-luna':
        allowed = {'model', 'messages', 'response_format', 'reasoning_effort', 'max_completion_tokens'}
        if set(request) - allowed:
            raise BudgetError('unreviewed OpenAI request fields')
        cap = request.get('max_completion_tokens')
        if type(cap) is not int or not 1 <= cap <= 128000:
            raise BudgetError('unreviewed OpenAI output limit')
        # Full documented input bound and the requested output bound, including
        # highest reviewed Standard rates and the 10% regional premium.
        reserved = (922000 * 550 + cap * 825 + 999) // 1000
        return reserved, 922000, cap
    if provider == 'jev' and request.get('model') == 'jev-1.14.0':
        if set(request) != {'model', 'state', 'questions'} or not request['questions']:
            raise BudgetError('unreviewed Jev request shape')
        tokens = 65536 * (len(request['questions']) + 1)
        return (tokens * 42 + 999) // 1000, tokens, None
    raise BudgetError('unreviewed provider or model')


def request_envelope(provider, request):
    """Reserve from the request itself: a byte-level tokenizer never makes more input tokens than the request's UTF-8
    bytes; 2,048 tokens cover message framing. The output bound is the request's own cap; rates are as in envelope()."""
    reserved, _, cap = envelope(provider, request)
    if provider != 'openai':
        return reserved, _, cap
    bound = len(model.request_identity(request)[0].encode('utf-8')) + 2048
    return (bound * 550 + cap * 825 + 999) // 1000, bound, cap


def charge(provider, response, max_input, max_output):
    usage = response.get('usage', {}) if isinstance(response, dict) else {}
    names = ('prompt_tokens', 'completion_tokens') if provider == 'openai' else ('input_tokens', 'output_tokens')
    counts = [usage.get(k) for k in names]
    if any(type(n) is not int or n < 0 for n in counts) or counts[0] > max_input or (max_output is not None and counts[1] > max_output):
        raise BudgetError('missing, invalid or above-envelope usage')
    a, b = counts
    # Integer microdollars, rounded up. OpenAI uses the highest reviewed Standard rate,
    # not an estimate of a discount or the provider's eventual bill.
    cost = (a * 550 + b * 825 + 999) // 1000 if provider == 'openai' else (a * 42 + 999) // 1000
    return cost


class GuardedTransport:
    """One coordinator's journal; unresolved work survives crashes and closes admission."""

    def __init__(self, path, prepare, *, cap_microdollars=1500000, max_calls=36, envelope_for=envelope, halt_on_failure=True):
        path = Path(path)
        if not path.is_absolute() or type(cap_microdollars) is not int or cap_microdollars <= 0 or type(max_calls) is not int or max_calls <= 0:
            raise ValueError('absolute journal path and positive integer limits required')
        self.lock, self.prepare = threading.Lock(), prepare
        self.envelope_for, self.halt_on_failure = envelope_for, halt_on_failure
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.executescript('''
            create table if not exists settings (id integer primary key check(id=1), cap integer, max_calls integer, halted text);
            create table if not exists attempts (
              id integer primary key, provider text, request_sha256 text, request_json text,
              reserved integer, charged integer, state text, response_json text, error text,
              seconds real, completed_order integer);
        ''')
        row = self.conn.execute('select cap,max_calls,halted from settings').fetchone()
        if row is None:
            self.conn.execute('insert into settings values (1,?,?,NULL)', (cap_microdollars, max_calls))
        elif row[:2] != (cap_microdollars, max_calls):
            raise BudgetError('journal limits changed')
        # A crash leaves an attempt reserved or dispatched; a recorded retryable failure holds its reservation instead.
        unresolved = "state!='complete'" if halt_on_failure else "state in ('reserved','dispatched')"
        if self.conn.execute(f"select 1 from attempts where {unresolved} limit 1").fetchone():
            self.conn.execute("update settings set halted='unresolved prior attempt' where id=1")
        self.conn.commit()

    def stop(self, reason):
        with self.lock:
            self.conn.execute('update settings set halted=coalesce(halted,?) where id=1', (reason,))
            self.conn.commit()

    def summary(self):
        with self.lock:
            self.conn.row_factory = sqlite3.Row
            attempts = [dict(r) for r in self.conn.execute('select id,provider,request_sha256,reserved,charged,state,error,seconds,completed_order from attempts order by id')]
            halted = self.conn.execute('select halted from settings').fetchone()[0]
            self.conn.row_factory = None
        return {'attempts': attempts, 'halted': halted,
                'held_microdollars': sum(r['charged'] if r['charged'] is not None else r['reserved'] for r in attempts)}

    def __call__(self, *args):
        provider, request = args if len(args) == 2 else ('jev', args[0])
        reserved, max_input, max_output = self.envelope_for(provider, request)
        text, sha = model.request_identity(request)
        with self.lock:
            cap, max_calls, halted = self.conn.execute('select cap,max_calls,halted from settings').fetchone()
            count, held = self.conn.execute('select count(*),coalesce(sum(coalesce(charged,reserved)),0) from attempts').fetchone()
            if halted or count >= max_calls or held + reserved > cap:
                raise BudgetError('admission closed or study limit reached')
            cur = self.conn.execute("insert into attempts(provider,request_sha256,request_json,reserved,state) values (?,?,?,?,'reserved')", (provider, sha, text, reserved))
            ident = cur.lastrowid
            self.conn.commit()
        start = time.perf_counter()
        encoded = None
        dispatched = False
        try:
            # Preparation is local only. Cancellation and dispatch then share one
            # decision point; work committed here is in flight, even before socket I/O.
            send = self.prepare(provider, request)
            with self.lock:
                if self.conn.execute('select halted from settings').fetchone()[0]:
                    raise BudgetError('cancelled before dispatch')
                self.conn.execute("update attempts set state='dispatched' where id=?", (ident,))
                self.conn.commit()
                dispatched = True
            response = send()
            encoded = json.dumps(response, ensure_ascii=False)
            cost = charge(provider, response, max_input, max_output)
            if cost > reserved:
                raise BudgetError('usage exceeds reserved cost')
        except BaseException as exc:
            # No raw exception text: HTTP/SDK exceptions can contain credentials or headers.
            with self.lock:
                self.conn.execute('update attempts set state=?,charged=?,response_json=?,error=?,seconds=? where id=?',
                                  ('unknown' if dispatched else 'not_sent', None if dispatched else 0,
                                   encoded, type(exc).__name__, time.perf_counter()-start, ident))
                # A retryable failure keeps its reservation held as unknown usage; the caller may admit a new attempt.
                if self.halt_on_failure or not isinstance(exc, RetryableError):
                    self.conn.execute("update settings set halted=coalesce(halted,'unknown usage') where id=1")
                self.conn.commit()
            raise
        with self.lock:
            order = self.conn.execute('select coalesce(max(completed_order),0)+1 from attempts').fetchone()[0]
            self.conn.execute("update attempts set state='complete',charged=?,response_json=?,seconds=?,completed_order=? where id=?", (cost, encoded, time.perf_counter()-start, order, ident))
            self.conn.commit()
        return response


RETRYABLE_STATUSES = {429, 500, 502, 503, 504, 529}
TIMEOUTS = {'openai': 600, 'jev': 60}


def single_attempt_http():
    """Explicit live opt-in. Credentials are loaded once; tests supply a fake sender. A failure without a usable
    reply (network, rate limit, server error) is a RetryableError; any other HTTP status is final."""
    keys = {'openai': model._key('openai'), 'jev': jev._key()}
    urls = {'openai': model.ENDPOINTS['openai'][0], 'jev': jev.ENDPOINT}
    if any(not isinstance(k, str) or not k for k in keys.values()):
        raise BudgetError('configured provider credential missing')

    def prepare(provider, body):
        headers = {'Authorization': 'Bearer ' + keys[provider], 'Content-Type': 'application/json', 'Accept': 'application/json'}
        data = json.dumps(body, sort_keys=True, ensure_ascii=False).encode('utf-8')
        request = urllib.request.Request(urls[provider], data, headers)
        def send():
            try:
                with urllib.request.urlopen(request, timeout=TIMEOUTS[provider]) as reply:
                    raw = reply.read()
            except urllib.error.HTTPError as exc:
                kind = RetryableError if exc.code in RETRYABLE_STATUSES else model.TransportError
                raise kind(f'{provider} HTTP {exc.code}') from None
            except (OSError, http.client.HTTPException) as exc:   # URLError, timeouts, TLS EOF, truncated replies
                raise RetryableError(f'{provider} transport failed: {type(exc).__name__}') from None
            if any(k.encode('utf-8') in raw for k in keys.values()):
                raise model.TransportError('credential in response; response not saved')
            return json.loads(raw)
        return send
    return prepare
