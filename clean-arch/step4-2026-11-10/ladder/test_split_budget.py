"""The probe's spending bound (splitting/DESIGN.md v4 §0c item 4, D616): the answer-choice runner's existing limit, which the yearly
re-asks share with the topic's call. It reserves the worst cost before each send and charges the reported cost after. So the cap holds
while every charge stays within its reserve, and a charge above its reserve can pass the cap by at most that excess over the sends in
flight. Fake transports only; nothing is sent."""
import json
import sys
import threading
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE.parent / 'stage_a'), str(ROOT / 'src'), str(ROOT / 'clean-arch' / 'e2e-2026-11-09'), str(HERE)]
import budget  # noqa: E402
import stage_a  # noqa: E402

REQUEST = {'model': stage_a.SETTING.model, 'max_completion_tokens': 2000, 'messages': [{'role': 'user', 'content': 'x' * 400}]}
RESERVE = budget.worst_cost(REQUEST)


def answering(prompt_tokens, completion_tokens, barrier=None):
    def attempt(provider, request):
        if barrier is not None:
            barrier.wait(timeout=10)
        return {'choices': [{'message': {'content': '{}'}}], 'usage': {'prompt_tokens': prompt_tokens, 'completion_tokens': completion_tokens}}
    return attempt


def send_many(limit, count):
    outcomes = []

    def one(n):
        try:
            limit.send_labelled(f'case|1|{n}', 'openai', REQUEST)
            outcomes.append('sent')
        except (budget.OverBudget, stage_a.Stopped):
            outcomes.append('stopped')
    threads = [threading.Thread(target=one, args=(n,)) for n in range(count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return outcomes


def test_concurrent_sends_stop_at_the_cap_when_every_charge_is_within_its_reserve(tmp_path):
    """Three sends held in flight together take three reserves; the others, trying while they are in flight, would pass the cap of
    3.5 reserves and are refused, and the limit stops every later send."""
    in_flight = threading.Barrier(3)
    honest = answering(100, 100, in_flight)               # far below the worst cost
    limit = stage_a.StageALimit(3.5 * RESERVE, tmp_path / 'spend.jsonl', attempt=honest)
    outcomes = send_many(limit, 8)
    assert outcomes.count('sent') == 3 and outcomes.count('stopped') == 5
    known, in_full, _ = stage_a.ledger_total(tmp_path / 'spend.jsonl')
    assert known + in_full <= limit.cap_usd and limit.spent_usd <= limit.cap_usd


def test_a_charge_above_its_reserve_passes_the_cap_by_at_most_the_excess_of_the_sends_in_flight(tmp_path):
    """The bound's stated assumption, exercised: a provider reporting more tokens than the reserve assumed (here twice the output
    cap) is charged what it reports, so three sends allowed by the reserve rule end above the cap by exactly their excess."""
    barrier = threading.Barrier(3)
    over = answering(len(json.dumps(REQUEST).encode()), 2 * REQUEST['max_completion_tokens'], barrier)
    limit = stage_a.StageALimit(3.5 * RESERVE, tmp_path / 'spend.jsonl', attempt=over)
    outcomes = send_many(limit, 3)
    assert outcomes == ['sent'] * 3
    charge = budget.cost(REQUEST, {'usage': {'prompt_tokens': len(json.dumps(REQUEST).encode()), 'completion_tokens': 2 * REQUEST['max_completion_tokens']}})
    assert charge > RESERVE
    assert limit.spent_usd == pytest.approx(3 * charge)
    assert limit.spent_usd - limit.cap_usd <= 3 * (charge - RESERVE) + 1e-12
