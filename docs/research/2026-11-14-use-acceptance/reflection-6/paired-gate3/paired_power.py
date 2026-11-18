"""Exact power of a paired (McNemar, exact binomial) comparison of the two systems on matched matters ($0 arithmetic).

For n matched pairs, each pair is discordant with probability d (one system's answer supported, the other's not). Among discordant
pairs, the new system wins with probability w. The test rejects at two-sided alpha when the discordant split is extreme by the exact
binomial. Power = P(reject). The effect on the share of supported answers is d * (2w - 1)."""
from math import comb


def reject_region(k, alpha=0.05):
    """Splits (wins) of k discordant pairs that the exact two-sided binomial test rejects."""
    out = set()
    for wins in range(k + 1):
        tail = min(wins, k - wins)
        p = 2 * sum(comb(k, i) for i in range(tail + 1)) / 2 ** k
        if p <= alpha:
            out.add(wins)
    return out


def power(n, d, w, alpha=0.05):
    total = 0.0
    for k in range(n + 1):
        pk = comb(n, k) * d ** k * (1 - d) ** (n - k)
        region = reject_region(k, alpha)
        total += pk * sum(comb(k, x) * w ** x * (1 - w) ** (k - x) for x in region)
    return total


if __name__ == '__main__':
    for n in (10, 15, 20, 30, 49):
        for d in (0.3, 0.5):
            best = next((w for w in [i / 100 for i in range(50, 101)] if power(n, d, w) >= 0.8), None)
            effect = None if best is None else round(100 * d * (2 * best - 1))
            print(f'pairs {n:2}, discordant {int(d*100)}%: 80% power needs the new system to win {best if best else ">100%"} of '
                  f'discordant pairs, a difference of {effect if effect is not None else "none reachable"} points in supported answers')
