"""D181: the live end-to-end study's transport retries only failures without a reply and keeps every attempt's money."""
from pathlib import Path
import sys

import pytest

from hivemind import model

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'poc'))
from concurrency_study.budget import GuardedTransport, RetryableError, request_envelope  # noqa: E402
from concurrency_study.e2e import LiveTransport  # noqa: E402

REQUEST = {'model': 'gpt-6-luna', 'messages': [{'role': 'user', 'content': 'x'}], 'max_completion_tokens': 1000,
           'response_format': {'type': 'json_schema', 'json_schema': {'name': 'extraction', 'strict': True, 'schema': {}}}}
REPLY = {'usage': {'prompt_tokens': 10, 'completion_tokens': 5}, 'choices': [{'message': {'content': '{}'}}]}


def transport(tmp_path, outcomes, attempts=3):
    sent = []
    def send(*args):
        outcome = outcomes.pop(0)
        sent.append(outcome)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome
    guard = GuardedTransport(tmp_path / 'budget.sqlite', lambda *a: lambda: send(*a), envelope_for=request_envelope, halt_on_failure=False)
    return LiveTransport(guard, outbound=2, attempts=attempts), guard, sent


def test_a_dropped_connection_is_sent_again_and_both_attempts_are_journaled(tmp_path, monkeypatch):
    monkeypatch.setattr('concurrency_study.e2e.threading.Event.wait', lambda self, seconds=None: True)
    live, guard, sent = transport(tmp_path, [RetryableError('openai transport failed: URLError'), REPLY])
    assert live('openai', REQUEST) == REPLY
    assert [a['state'] for a in guard.summary()['attempts']] == ['unknown', 'complete']
    assert [(e['attempt'], e['outcome']) for e in live.events] == [(1, 'openai transport failed: URLError'), (2, 'ok')]


def test_a_final_error_is_not_retried_and_retries_are_bounded(tmp_path, monkeypatch):
    monkeypatch.setattr('concurrency_study.e2e.threading.Event.wait', lambda self, seconds=None: True)
    live, guard, sent = transport(tmp_path, [model.TransportError('openai HTTP 400'), REPLY])
    with pytest.raises(model.TransportError):
        live('openai', REQUEST)
    assert len(sent) == 1
    (tmp_path / 'bounded').mkdir()
    live, guard, sent = transport(tmp_path / 'bounded', [RetryableError('503')] * 3 + [REPLY])
    with pytest.raises(RetryableError):
        live('openai', REQUEST)
    assert len(sent) == 3


def test_a_trial_passes_only_with_clean_audits_on_both_modes():
    """D181 review: a failed cross-replay audit stops the study like a table difference does."""
    from concurrency_study.e2e import passed
    clean = {'failure': None, 'audit': {'errors': []}, 'cross_replay': {'different_tables': [], 'audit_errors': []}}
    assert passed(clean)
    assert not passed(dict(clean, cross_replay={'different_tables': [], 'audit_errors': ['the runner accepted another request: x']}))
    assert not passed(dict(clean, cross_replay={'different_tables': ['views'], 'audit_errors': []}))
    assert not passed(dict(clean, audit={'errors': ['not audited']}))
    assert not passed(dict(clean, failure={'type': 'RuntimeError'}))

