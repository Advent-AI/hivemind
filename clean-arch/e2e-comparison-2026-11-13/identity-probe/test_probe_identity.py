"""The identity probe's ledger (council round 15): a paid response is never settled below its reservation unless its usage is a pair of whole
nonnegative token counts with a positive price; an overrun stops the run; a reservation that would pass the ceiling is refused."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_identity  # noqa: E402

PRICE_IN, PRICE_OUT = 0.30, 1.20
REQUEST = {'max_tokens': 64000, 'messages': [{'role': 'user', 'content': 'x' * 1000}]}


def ledger(ceiling=5.0):
    return probe_identity.Ledger(ceiling, PRICE_IN, PRICE_OUT)


def test_zero_usage_settles_at_the_reservation():
    book = ledger()
    amount = book.reserve(REQUEST)
    assert book.settle(amount, {'prompt_tokens': 0, 'completion_tokens': 0}) == amount
    assert book.spent == amount and book.reserved == 0


def test_missing_or_malformed_usage_settles_at_the_reservation():
    for usage in (None, {}, {'prompt_tokens': 10}, {'prompt_tokens': -1, 'completion_tokens': 5}, {'prompt_tokens': True, 'completion_tokens': 5},
                  {'prompt_tokens': 1.5, 'completion_tokens': 5}):
        book = ledger()
        amount = book.reserve(REQUEST)
        assert book.settle(amount, usage) == amount


def test_real_usage_settles_at_its_token_price():
    book = ledger()
    amount = book.reserve(REQUEST)
    cost = book.settle(amount, {'prompt_tokens': 10000, 'completion_tokens': 9500})
    assert cost == (10000 * PRICE_IN + 9500 * PRICE_OUT) / 1e6 and not book.overrun


def test_a_settlement_above_its_reservation_stops_the_run():
    book = ledger()
    amount = book.reserve(REQUEST)
    book.settle(amount, {'prompt_tokens': 10_000_000, 'completion_tokens': 0})
    assert book.overrun and book.reserve(REQUEST, wait=False) is None


def test_a_reservation_that_would_pass_the_ceiling_is_refused():
    book = ledger(ceiling=0.05)
    assert book.reserve(REQUEST, wait=False) is None
