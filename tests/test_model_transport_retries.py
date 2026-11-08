"""The shared transport's retry contract (src/hivemind/model.py, openai_transport): by default a call is tried three times with 5,
10 and 15 seconds between failures, as production has always done; the final failure carries only the last attempt's HTTP details,
so a timeout after an earlier HTTP 500 is not reported with that 500's status and body."""
import io
import os
import sys
import urllib.error

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import model  # noqa: E402


def server_error():
    return urllib.error.HTTPError('https://api.example.test', 500, 'Internal Server Error', {}, io.BytesIO(b'{"error": "overloaded"}'))


def test_the_default_call_is_tried_three_times_with_growing_waits(monkeypatch):
    attempts, waits = [], []
    def urlopen(request, timeout):
        attempts.append(timeout)
        raise TimeoutError('read timed out')
    monkeypatch.setattr(model, '_key', lambda provider: 'test-key')
    monkeypatch.setattr(model.urllib.request, 'urlopen', urlopen)
    monkeypatch.setattr(model.time, 'sleep', waits.append)
    with pytest.raises(model.TransportError):
        model.openai_transport('deepseek', {'model': 'deepseek-flash'})
    assert len(attempts) == 3
    assert waits == [5, 10, 15]


def test_a_timeout_after_a_server_error_is_reported_without_the_server_error_details(monkeypatch):
    replies = [server_error(), TimeoutError('read timed out'), TimeoutError('read timed out')]
    def urlopen(request, timeout):
        raise replies.pop(0)
    monkeypatch.setattr(model, '_key', lambda provider: 'test-key')
    monkeypatch.setattr(model.urllib.request, 'urlopen', urlopen)
    monkeypatch.setattr(model.time, 'sleep', lambda seconds: None)
    with pytest.raises(model.TransportError) as failure:
        model.openai_transport('deepseek', {'model': 'deepseek-flash'})
    assert 'TimeoutError' in str(failure.value)
    assert not hasattr(failure.value, 'http_status')
