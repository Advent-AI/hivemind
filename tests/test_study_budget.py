"""The isolated live study's admission table, with no credentials or live calls."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
import threading

import pytest

from hivemind import model

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'poc'))
from concurrency_study.budget import BudgetError, GuardedTransport, charge, envelope

REQUEST = {'model': 'gpt-6-luna', 'messages': [], 'max_completion_tokens': 16000}


def reply():
    return {'usage': {'prompt_tokens': 1000, 'completion_tokens': 100}, 'choices': [{'message': {'content': '{}'}}]}


def test_reservation_covers_maximum_documented_usage():
    """Value-reader: reviewed prices and maximum context fit the reservation; units are microdollars."""
    reserve, max_input, _ = envelope('openai', REQUEST)
    maximum = {'usage': {'prompt_tokens': max_input, 'completion_tokens': 16000}}
    assert charge('openai', reply(), max_input, 16000) == 633
    assert charge('openai', maximum, max_input, 16000) == reserve == 520300
    maximum['usage']['completion_tokens'] = 128000
    assert charge('openai', maximum, max_input, 128000) == envelope('openai', dict(REQUEST, max_completion_tokens=128000))[0] == 612700
    request = {'model': 'jev-1.14.0', 'state': '', 'questions': {'q': {}}}
    reserve, max_input, _ = envelope('jev', request)
    assert charge('jev', {'usage': {'input_tokens': max_input, 'output_tokens': 99}}, max_input, None) <= reserve


def test_concurrent_admission_cannot_overspend(tmp_path):
    """Ready/admit: reserve both in-flight costs before a third request can send."""
    entered, release = threading.Event(), threading.Event()
    count = 0
    lock = threading.Lock()
    def send(*args):
        nonlocal count
        with lock:
            count += 1
            position = count
            if count == 2:
                entered.set()
        if position <= 2:
            assert release.wait(5)
        return reply()
    guard = GuardedTransport(tmp_path / 'budget.sqlite', lambda *a: lambda: send(*a))
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(guard, 'openai', REQUEST)
        second = pool.submit(guard, 'openai', REQUEST)
        try:
            assert entered.wait(5)
            with pytest.raises(BudgetError):
                guard('openai', REQUEST)
            assert count == 2
            assert guard.summary()['held_microdollars'] == 1040600
        finally:
            release.set()
        first.result(); second.result()
    assert guard.summary()['held_microdollars'] == 1266


@pytest.mark.parametrize('outcome', ['timeout', 'missing_usage'])
def test_unknown_usage_survives_restart_and_refuses_send(tmp_path, outcome):
    """Reserved/unknown: neither timeout nor malformed usage releases reserved money."""
    def fail(*args):
        if outcome == 'timeout':
            raise TimeoutError('uncertain remote outcome')
        return {'choices': []}
    path = tmp_path / 'budget.sqlite'
    guard = GuardedTransport(path, lambda *a: lambda: fail(*a))
    with pytest.raises((BudgetError, TimeoutError)):
        guard('openai', REQUEST)
    assert guard.summary()['held_microdollars'] == 520300
    def forbidden(*args):
        raise AssertionError('closed admission reached HTTP')
    resumed = GuardedTransport(path, lambda *a: lambda: forbidden(*a))
    with pytest.raises(BudgetError):
        resumed('openai', REQUEST)
    assert resumed.summary()['held_microdollars'] == 520300


def test_cancellation_closes_admission_before_draining(tmp_path):
    """Cancellation: sent call drains with usage; unsent call never reaches HTTP."""
    entered, release = threading.Event(), threading.Event()
    calls = []
    def send(*args):
        calls.append(1); entered.set()
        if len(calls) == 1:
            assert release.wait(5)
        return reply()
    guard = GuardedTransport(tmp_path / 'budget.sqlite', lambda *a: lambda: send(*a))
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(guard, 'openai', REQUEST)
        try:
            assert entered.wait(5)
            guard.stop('cancelled')
            with pytest.raises(BudgetError):
                guard('openai', REQUEST)
        finally:
            release.set()
        future.result()
    assert calls == [1]
    assert guard.summary()['halted'] == 'cancelled'
    assert guard.summary()['held_microdollars'] == 633


def test_downstream_schema_failure_does_not_erase_usage(tmp_path):
    """Completed/invalid answer: accounting precedes model JSON validation."""
    guard = GuardedTransport(tmp_path / 'budget.sqlite', lambda *args: reply)
    response = guard('openai', REQUEST)
    assert model.check_schema(json.loads(response['choices'][0]['message']['content']), {'type': 'object', 'required': ['answer']})
    guard.stop('schema failure')
    assert guard.summary()['held_microdollars'] == 633
    assert guard.conn.execute('select response_json from attempts').fetchone()[0]


def test_dispatch_count_is_a_separate_limit(tmp_path):
    """Ready/refusal: cheap or zero-token replies cannot make more than the registered calls."""
    calls = []
    guard = GuardedTransport(tmp_path / 'budget.sqlite', lambda *args: lambda: calls.append(1) or reply(), max_calls=1)
    guard('openai', REQUEST)
    with pytest.raises(BudgetError):
        guard('openai', REQUEST)
    assert calls == [1]


def test_cancellation_during_preparation_never_dispatches(tmp_path):
    """Reserved/cancel: external request preparation must not bypass the dispatch decision."""
    prepared, release = threading.Event(), threading.Event()
    calls = []
    def prepare(*args):
        prepared.set()
        assert release.wait(5)
        return lambda: calls.append(1) or reply()
    guard = GuardedTransport(tmp_path / 'budget.sqlite', prepare)
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(guard, 'openai', REQUEST)
        try:
            assert prepared.wait(5)
            guard.stop('cancelled')
        finally:
            release.set()
        with pytest.raises(BudgetError, match='cancelled before dispatch'):
            future.result()
    assert calls == []
    assert guard.summary()['attempts'][0]['state'] == 'not_sent'
    assert guard.summary()['held_microdollars'] == 0


def test_request_sized_reservation_bounds_tokens_by_request_bytes():
    """D181 value-reader: input tokens never exceed the request's UTF-8 bytes plus framing; usage above it refuses."""
    from concurrency_study.budget import request_envelope
    request = dict(REQUEST, messages=[{'role': 'user', 'content': 'é' * 1000}])
    reserve, bound, cap = request_envelope('openai', request)
    assert bound == len(model.request_identity(request)[0].encode('utf-8')) + 2048
    assert reserve == charge('openai', {'usage': {'prompt_tokens': bound, 'completion_tokens': cap}}, bound, cap)
    with pytest.raises(BudgetError):
        charge('openai', {'usage': {'prompt_tokens': bound + 1, 'completion_tokens': 0}}, bound, cap)


def test_retryable_failure_holds_its_reservation_without_closing_admission(tmp_path):
    """D181 retry row: a failed attempt keeps its money held; the next attempt and a restart are admitted."""
    from concurrency_study.budget import RetryableError, request_envelope
    outcomes = [RetryableError('openai HTTP 503'), reply()]
    def send(*args):
        outcome = outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome
    path = tmp_path / 'budget.sqlite'
    guard = GuardedTransport(path, lambda *a: lambda: send(*a), envelope_for=request_envelope, halt_on_failure=False)
    with pytest.raises(RetryableError):
        guard('openai', REQUEST)
    guard('openai', REQUEST)
    held = guard.summary()
    assert [a['state'] for a in held['attempts']] == ['unknown', 'complete'] and held['halted'] is None
    assert held['held_microdollars'] == request_envelope('openai', REQUEST)[0] + 633
    resumed = GuardedTransport(path, lambda *a: reply, envelope_for=request_envelope, halt_on_failure=False)
    resumed('openai', REQUEST)
    final = GuardedTransport(path, lambda *a: lambda: (_ for _ in ()).throw(model.TransportError('openai HTTP 400')),
                             envelope_for=request_envelope, halt_on_failure=False)
    with pytest.raises(model.TransportError):
        final('openai', REQUEST)
    assert final.summary()['halted'] == 'unknown usage'


@pytest.mark.parametrize('failure, retryable', [('503', True), ('429', True), ('400', False), ('network', True)])
def test_http_failures_are_classified_without_credentials(monkeypatch, failure, retryable):
    """D181: only failures without a usable reply are retryable; tests never read the credentials file."""
    import io
    import urllib.error
    from concurrency_study import budget
    monkeypatch.setattr(budget.model, '_key', lambda provider: 'test-openai')
    monkeypatch.setattr(budget.jev, '_key', lambda: 'test-jev')
    def urlopen(request, timeout):
        if failure == 'network':
            raise urllib.error.URLError(ConnectionResetError('EOF occurred in violation of protocol'))
        raise urllib.error.HTTPError(request.full_url, int(failure), 'failed', {}, io.BytesIO(b''))
    monkeypatch.setattr(budget.urllib.request, 'urlopen', urlopen)
    send = budget.single_attempt_http()('openai', REQUEST)
    with pytest.raises(model.TransportError) as caught:
        send()
    assert isinstance(caught.value, budget.RetryableError) is retryable
