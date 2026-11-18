"""The shared ledger inside the ladder step's and the judge's per-attempt loops (WIRING-DESIGN.md §B2, D448; council mo R1, R3): each
attempt reserves the ledger's own estimate (the agreed bound) in the locked step after the local cap check and settles at that attempt's
charge (None for a failed attempt: the ledger settles it at the reservation); a shared refusal stops the limit; every final local stop
(the local cap included) stops the shared ledger too. Fake attempts and a fake ledger only: no network, no credential."""
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch' / 'e2e-2026-11-09'), str(HERE / 'stage_a'), str(HERE / 'stage_b'), str(HERE / 'ladder')]
import budget  # noqa: E402
import stage_a  # noqa: E402
import ladder_adapter  # noqa: E402
from hivemind import model  # noqa: E402

REQUEST = {'model': 'gpt-6-luna', 'max_completion_tokens': 16000, 'messages': [{'role': 'user', 'content': 'x' * 4000}]}
ANSWER = {'choices': [{'message': {'content': '{}'}}], 'usage': {'prompt_tokens': 1000, 'completion_tokens': 500}}


ESTIMATE = 0.25            # distinct from budget.worst_cost(REQUEST), so a test can tell which bound was reserved


class FakeShared:
    def __init__(self, allow=True):
        self.allow, self.reservations, self.settlements, self.stops = allow, [], [], []

    def estimate(self, request):
        return ESTIMATE

    def stop(self, reason):
        self.stops.append(reason)

    def reserve(self, amount):
        self.reservations.append(amount)
        return self.allow

    def settle(self, reserved, actual):
        self.settlements.append((reserved, actual))


def limits(tmp_path, attempt, shared):
    """The two limits under test, each with its own local ledger file."""
    return [('stage A', stage_a.StageALimit(5.0, tmp_path / 'a.jsonl', attempt=attempt, sleep=lambda s: None, shared=shared),
             lambda limit: limit.send_labelled('case|1|1', 'openai', REQUEST)),
            ('judge', ladder_adapter.LedgerBudget(5.0, tmp_path / 'b.jsonl', attempt=attempt, sleep=lambda s: None, shared=shared),
             lambda limit: limit.send('openai', REQUEST))]


def test_each_attempt_reserves_on_the_shared_ledger_and_settles_at_its_charge(tmp_path):
    for name, limit, send in limits(tmp_path, lambda provider, request: ANSWER, None):
        shared = FakeShared()
        limit.shared = shared
        send(limit)
        assert ESTIMATE != budget.worst_cost(REQUEST)
        assert shared.reservations == [ESTIMATE], name
        assert shared.settlements == [(ESTIMATE, budget.cost(REQUEST, ANSWER))], name


def test_a_retried_attempt_reserves_again_and_a_failed_one_settles_at_its_reservation(tmp_path):
    for name, limit, send in limits(tmp_path, None, None):
        calls = {'n': 0}
        def flaky(provider, request):
            calls['n'] += 1
            if calls['n'] == 1:
                raise model.TransportError('dropped')
            return ANSWER
        limit.attempt = flaky
        shared = FakeShared()
        limit.shared = shared
        send(limit)
        assert shared.reservations == [ESTIMATE, ESTIMATE], name
        assert shared.settlements == [(ESTIMATE, None), (ESTIMATE, budget.cost(REQUEST, ANSWER))], name


def test_a_shared_refusal_sends_nothing_and_stops_the_limit(tmp_path):
    for name, limit, send in limits(tmp_path, None, None):
        sent = []
        limit.attempt = lambda provider, request: sent.append(1) or ANSWER
        limit.shared = FakeShared(allow=False)
        with pytest.raises(budget.OverBudget):
            send(limit)
        assert sent == [], name
        with pytest.raises((budget.OverBudget, stage_a.Stopped)):
            send(limit)                     # stopped: no later send begins
        assert sent == [], name


def test_a_local_cap_refusal_and_a_final_stop_stop_the_shared_ledger(tmp_path):
    for name, limit, send in limits(tmp_path, lambda provider, request: ANSWER, None):
        shared = FakeShared()
        limit.shared = shared
        limit.cap_usd = 1e-9                                   # the local cap refuses the first attempt
        with pytest.raises(budget.OverBudget):
            send(limit)
        assert shared.reservations == [] and shared.stops, name
    limit = ladder_adapter.LedgerBudget(5.0, tmp_path / 'c.jsonl', shared=FakeShared())
    limit.stop('u1 incomplete: its redo did not finish')       # run_stage_b's final stop
    assert limit.shared.stops == ['the judge: u1 incomplete: its redo did not finish']


def test_without_a_shared_ledger_nothing_changes(tmp_path):
    for name, limit, send in limits(tmp_path, lambda provider, request: ANSWER, None):
        assert send(limit) == ANSWER, name
