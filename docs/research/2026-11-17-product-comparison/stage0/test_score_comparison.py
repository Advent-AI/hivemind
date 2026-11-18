"""Tests of the comparison's verdict (verdict-rule.json; D665, D672). Each names the rule it proves. Synthetic readings only.

Run: python3 -m pytest docs/research/2026-11-17-product-comparison/stage0/test_score_comparison.py
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_comparison as sc  # noqa: E402

DRAWS = [f'{s}-{d}' for s in ('new', 'old') for d in (1, 2, 3)]


def base(n=20, new_served=0, old_served=0, guard_cards=12):
    """N matters; the first `new_served` served by the new system in all draws, the next `old_served` by the old one; every draw has
    `guard_cards` guardrail cards of each type, all supported and worth (no breach)."""
    matters = [{'matter': f'M{i:02d}', 'company_figure': False} for i in range(1, n + 1)]
    mapping = {d: {} for d in DRAWS}
    cards = {d: {} for d in DRAWS}
    for i, m in enumerate(matters):
        for d in DRAWS:
            system = d.split('-')[0]
            served = (system == 'new' and i < new_served) or (system == 'old' and new_served <= i < new_served + old_served)
            if served:
                q = f'{d}-q{i}'
                mapping[d][m['matter']] = [{'question': q, 'covers': True}]
                cards[d][q] = {'worth': 'worth', 'answer': 'supported', 'type': 'figure', 'guardrail': False}
    for d in DRAWS:
        for t in ('figure', 'yes/no'):
            for j in range(guard_cards):
                cards[d][f'{d}-g-{t}-{j}'] = {'worth': 'worth', 'answer': 'supported', 'type': t, 'guardrail': True}
    return {'matters': matters, 'mapping': mapping, 'cards': cards,
            'distinct': {d: {'ids': 40, 'duplicates_both': 0, 'duplicates_split': 0} for d in DRAWS},
            'controls': {'plants': ['unsupported'] * 6, 'supported': ['supported'] * 4, 'repeats_same': [True] * 3}}


def test_a_plant_without_an_explicit_rejection_makes_the_reading_invalid():
    """Rule: invalid when a planted wrong answer is not explicitly rejected (a split or 'cannot tell' is not a rejection)."""
    r = base(new_served=10)
    r['controls']['plants'][0] = {'split': ['supported', 'unsupported']}
    assert sc.verdict(r)['verdict'] == 'invalid'


def test_fewer_than_three_supported_controls_or_two_repeats_is_invalid():
    """Rule: invalid with fewer than 3 of 4 supported controls accepted, or fewer than 2 of 3 repeats the same."""
    r = base(new_served=10)
    r['controls']['supported'] = ['supported', 'supported', 'unsupported', 'insufficient']
    assert sc.verdict(r)['verdict'] == 'invalid'
    r = base(new_served=10)
    r['controls']['repeats_same'] = [True, False, False]
    assert sc.verdict(r)['verdict'] == 'invalid'


def test_too_small_when_n_under_20_or_a_draw_under_30_distinct_bets_either_way():
    """Rule: too small when N < 20, or a draw has fewer than 30 distinct bets (split duplicates counted both ways)."""
    assert sc.verdict(base(n=19, new_served=10))['verdict'] == 'too small'
    r = base(new_served=10)
    r['distinct']['old-2'] = {'ids': 32, 'duplicates_both': 1, 'duplicates_split': 2}     # 31 one way, 29 the other
    assert sc.verdict(r)['verdict'] == 'too small'


def test_a_practical_lead_needs_the_margin_twice_b_and_every_guardrail_exercised_and_passing():
    """Rule: lead when a - b >= max(3, ceil(0.15 N)) and a >= 2b under both countings, with every guardrail exercised and passing."""
    r = base(n=20, new_served=5, old_served=1)               # a 5, b 1: margin max(3, 3) = 3; 5 - 1 = 4 >= 3; 5 >= 2
    assert sc.verdict(r)['verdict'] == 'practical lead'
    r = base(n=20, new_served=4, old_served=2)               # a 4, b 2: 4 - 2 = 2 < 3
    assert sc.verdict(r)['verdict'] == 'no practical winner'


def test_an_unexercised_guardrail_blocks_a_lead_but_not_a_loss():
    """Rule: a subgroup with fewer than 10 unsplit decided cards per system cannot breach; it blocks only a lead."""
    assert sc.verdict(base(n=20, new_served=5, old_served=1, guard_cards=3))['verdict'] == 'no practical winner'
    assert sc.verdict(base(n=20, new_served=1, old_served=5, guard_cards=3))['verdict'] == 'practical loss'


def test_a_guardrail_breach_under_both_countings_is_a_loss():
    """Rule: loss when the new system's unsupported share is more than 10 points above the old's, under both countings."""
    r = base(n=20, new_served=5, old_served=1)
    for d in ('new-1', 'new-2', 'new-3'):
        for j in range(3):                                     # 3 of 12 figure cards unsupported per draw: 25% against 0%
            r['cards'][d][f'{d}-g-figure-{j}']['answer'] = 'unsupported'
    out = sc.verdict(r)
    assert out['verdict'] == 'practical loss' and 'guardrail figure' in out['why']


def test_a_matter_counts_as_served_only_in_two_of_three_draws():
    """Rule: served by a system when served in at least 2 of its 3 draws."""
    r = base(n=20, new_served=5, old_served=1)
    for d in ('new-2', 'new-3'):
        r['mapping'][d].pop('M01')                             # M01 served by the new system in one draw only
    out = sc.verdict(r)
    assert out['countings']['1']['a'] == 4


def test_splits_resolve_for_the_favoured_system_in_each_counting():
    """Rule: counting 1 resolves the new system's splits favourably and the old's unfavourably; counting 2 the reverse."""
    r = base(n=20, new_served=5, old_served=1)
    for d in ('new-1', 'new-2', 'new-3'):
        q = r['mapping'][d]['M01'][0]['question']
        r['cards'][d][q]['answer'] = {'split': ['supported', 'unsupported']}
    out = sc.verdict(r)
    assert out['countings']['1']['a'] == 5 and out['countings']['2']['a'] == 4
    assert out['verdict'] == 'practical lead'                 # 4 - 1 = 3 >= 3 and 4 >= 2 under counting 2 as well


def test_a_resolved_insufficient_stays_out_of_the_decided_shares():
    """Rule: insufficient (final or resolved) is outside the decided denominators."""
    r = base(n=20, new_served=5, old_served=1)
    r['cards']['new-1']['new-1-g-figure-0']['answer'] = 'insufficient'
    g = sc.guardrails(r, '1')['figure']['new']
    assert g['decided'] == 35 and g['share'] == 0.0
