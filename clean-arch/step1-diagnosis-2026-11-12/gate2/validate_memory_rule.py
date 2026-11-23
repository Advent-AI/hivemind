"""Validates memory_rule.py by simulation before any send: the false-proceed rate at the margin (true difference about -22.2 points,
equal and unequal state rates), coverage of the interval, and the decision rates under plausible true rates. 18 sends per state per arm.

  python3 clean-arch/step1-diagnosis-2026-11-12/gate2/validate_memory_rule.py
"""
import random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import memory_rule

def simulate(rates_candidate, rates_control, level, reps=20000, n=18, seed=20261113):
    rng = random.Random(seed)
    out = {'proceed': 0, 'stop': 0, 'inconclusive': 0}
    covered = 0
    true_diff = sum(rates_candidate) / 3 - sum(rates_control) / 3
    for _ in range(reps):
        k1 = sum(sum(rng.random() < p for _ in range(n)) for p in rates_candidate)
        k0 = sum(sum(rng.random() < p for _ in range(n)) for p in rates_control)
        out[memory_rule.decide(k1, 3 * n, k0, 3 * n, control_exercised=k0 > 0, level=level)] += 1
        low, high = memory_rule.newcombe(k1, 3 * n, k0, 3 * n, level)
        covered += low <= true_diff <= high
    return {k: round(v / reps, 3) for k, v in out.items()}, round(covered / reps, 3), round(true_diff, 3)

for level in (0.90, 0.95):
    print(f'== two-sided level {level} (one-sided {1 - (1 - level) / 2:.3f})')
    print('  at the margin (an erroneous proceed should be at most the one-sided error):')
    for label, cand, ctrl in (('equal states, 0.111 vs 0.333', (1/9,) * 3, (1/3,) * 3),
                              ('unequal states (0.28,0.11,0.03) vs (0.5,0.33,0.25)', (0.278, 0.111, 0.028), (0.5, 1/3, 0.25)),
                              ('sparse states (0.15,0.0,0.0) vs (0.45,0.15,0.2)', (0.15, 0.0, 0.0), (0.45, 0.15, 0.2)),
                              ('high rates 0.53 vs 0.75', (0.528,) * 3, (0.75,) * 3)):
        rates, coverage, diff = simulate(cand, ctrl, level)
        print(f'   {label}: true difference {diff}: {rates}; interval coverage {coverage}')
    print('  decision rates:')
    for label, cand, ctrl in (('no effect 0.33', (1/3,) * 3, (1/3,) * 3), ('0.25 vs 0.33', (0.25,) * 3, (1/3,) * 3),
                              ('0.14 vs 0.33', (1/7,) * 3, (1/3,) * 3), ('0.0 vs 0.33', (0.0,) * 3, (1/3,) * 3),
                              ('both zero (unexercised)', (0.0,) * 3, (0.0,) * 3)):
        rates, coverage, diff = simulate(cand, ctrl, level)
        print(f'   {label}: {rates}; coverage {coverage}')
