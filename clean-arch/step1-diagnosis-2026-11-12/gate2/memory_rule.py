"""The memory diagnostic's decision rule (council round mj, D440), frozen before any send. Input: per arm, the count of usable-or-
conservatively-scored sends showing the outcome and the number of sends, pooled over the three stored states (each state has the same
number of sends per arm, so the pooled difference equals the Mantel-Haenszel risk difference). Interval: Newcombe's hybrid score
interval (method 10) for a difference of two proportions, from Wilson score intervals at a two-sided level `level`.

  decide(k_candidate, n_candidate, k_control, n_control, control_exercised) -> 'proceed' | 'stop' | 'inconclusive'
"""
import math

MARGIN = -2 / 9          # the original 2-of-9 tolerance, carried forward
Z = {0.90: 1.6448536269514722, 0.95: 1.959963984540054}


def wilson(k, n, z):
    if n <= 0:
        raise ValueError('no sends')
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, centre - half), min(1.0, centre + half)


def newcombe(k1, n1, k0, n0, level):
    """Interval for p1 - p0 (candidate minus control)."""
    z = Z[level]
    p1, p0 = k1 / n1, k0 / n0
    l1, u1 = wilson(k1, n1, z)
    l0, u0 = wilson(k0, n0, z)
    d = p1 - p0
    return d - math.sqrt((p1 - l1) ** 2 + (u0 - p0) ** 2), d + math.sqrt((u1 - p1) ** 2 + (p0 - l0) ** 2)


def decide(k1, n1, k0, n0, control_exercised, level=0.90):
    if not control_exercised:
        return 'inconclusive'
    try:
        low, high = newcombe(k1, n1, k0, n0, level)
    except (ValueError, ZeroDivisionError):
        return 'inconclusive'
    if not (math.isfinite(low) and math.isfinite(high)):
        return 'inconclusive'
    if low > MARGIN:
        return 'proceed'
    if high < MARGIN:
        return 'stop'
    return 'inconclusive'
