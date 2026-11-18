"""The comparison's sizing, step 2 ($0; D516): how large a difference between the two systems could a comparison of a given shape detect?

For each line read as a share (answers supported; questions that are trivia or duplicates) it takes the counts seen so far, the number of
questions each system holds at the end of a week, and a set of comparison shapes (weeks of unread news x draws of each system), and
computes the smallest true difference that a two-sided test at 5% would detect four times in five, under two assumptions about repeated
draws of the same week: that they add nothing (the same questions come back; the independent unit is the week), and that they are as
good as new weeks (an upper bound on what repeats can give). The closed form is checked by simulation for one shape. Costs use the
fresh week's charged prices. Every input is printed with its source; nothing here is a measurement of a system.

  python3 sizing.py
"""
import math
import random

# what one week holds, from the fresh week of 2026-09-22..28 (week/WEEK-RESULT.md): questions with a latest answer
PER_WEEK = {'new': 7, 'old': 15}
# charged per week and draw: the new system's ledger $2.52; the old system at listed rates $0.47, rounded up
COST = {'new': 2.52, 'old': 0.50}
# shares seen so far, as (new: hits, of), (old: hits, of), with where they come from
SEEN = {
    'answers supported by both teams': [('July window, trial, one draw each (TRIAL-RESULT.md)', (7, 9), (10, 12)),
                                        ('fresh week, one draw each (WEEK-RESULT.md)', (6, 7), (10, 15))],
    'questions that are trivia or duplicates, both teams': [('fresh week, one draw each (WEEK-RESULT.md)', (1, 7), (6, 15))],
}
SHAPES = [(1, 3), (2, 3), (3, 1), (3, 2), (4, 1), (4, 3)]   # (weeks of unread news, draws of each system)
UNREAD_WEEKS = 3   # 2026-10-06..12, 10-13..19, 10-20..26 are in the article database; the week of 09-29 has 40 articles already read


def smallest_detectable(p, n_new, n_old):
    """Two shares near p, two-sided 5%, detected four times in five: 2.8 standard errors."""
    return 2.8 * math.sqrt(p * (1 - p) * (1 / n_new + 1 / n_old))


def simulated_power(p_new, p_old, n_new, n_old, runs=20000, seed=20261201):
    rng, hits = random.Random(seed), 0
    for _ in range(runs):
        a = sum(rng.random() < p_new for _ in range(n_new)) / n_new
        b = sum(rng.random() < p_old for _ in range(n_old)) / n_old
        pooled = (a * n_new + b * n_old) / (n_new + n_old)
        se = math.sqrt(max(pooled * (1 - pooled), 1e-9) * (1 / n_new + 1 / n_old))
        hits += abs(a - b) / se > 1.96
    return hits / runs


def main():
    print('SEEN SO FAR (one draw each; the two windows are different news)')
    baseline = {}
    for line, rows in SEEN.items():
        hits = sum(new[0] + old[0] for _, new, old in rows)
        of = sum(new[1] + old[1] for _, new, old in rows)
        baseline[line] = hits / of
        for source, new, old in rows:
            print(f'  {line}: new {new[0]} of {new[1]} ({new[0] / new[1]:.0%}), old {old[0]} of {old[1]} ({old[0] / old[1]:.0%}), '
                  f'difference {new[0] / new[1] - old[0] / old[1]:+.0%}  [{source}]')
        print(f'    pooled share {baseline[line]:.0%}')
    print(f"\nPER WEEK (fresh week): questions with a latest answer: new {PER_WEEK['new']}, old {PER_WEEK['old']}; "
          f"charged per week and draw: new ${COST['new']}, old ${COST['old']}; unread weeks in the article database: {UNREAD_WEEKS}")
    print('\nSMALLEST DIFFERENCE A COMPARISON WOULD DETECT (two-sided 5%, four times in five)')
    for weeks, draws in SHAPES:
        cost = weeks * draws * (COST['new'] + COST['old'])
        note = '' if weeks <= UNREAD_WEEKS else '  (needs more unread weeks than the database holds)'
        print(f'  {weeks} week(s) x {draws} draw(s) each, about ${cost:.2f}{note}')
        for line, p in baseline.items():
            floor = smallest_detectable(p, weeks * PER_WEEK['new'], weeks * PER_WEEK['old'])                        # repeats add nothing
            best = smallest_detectable(p, weeks * draws * PER_WEEK['new'], weeks * draws * PER_WEEK['old'])        # repeats as good as new weeks
            print(f'      {line}: {best:.0%} if repeated draws were as good as new weeks; {floor:.0%} if they add nothing')
    p = baseline['answers supported by both teams']
    n_new, n_old = 3 * PER_WEEK['new'], 3 * PER_WEEK['old']
    gap = smallest_detectable(p, n_new, n_old)
    print(f"\nCHECK BY SIMULATION (3 weeks x 1 draw: {n_new} and {n_old} answers; shares {min(p + gap / 2, 0.99):.2f} against {p - gap / 2:.2f}): "
          f"detected in {simulated_power(min(p + gap / 2, 0.99), p - gap / 2, n_new, n_old):.0%} of 20,000 simulated comparisons (the closed form says 80%)")
    print(f"   and a true difference of 10 points on the same shape: detected in {simulated_power(p + 0.05, p - 0.05, n_new, n_old):.0%}; of 20 points: "
          f"{simulated_power(min(p + 0.10, 0.99), p - 0.10, n_new, n_old):.0%}")


if __name__ == '__main__':
    main()
