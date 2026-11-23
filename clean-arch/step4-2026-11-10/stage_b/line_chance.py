"""How often the proposed Stage B lines would be missed, or passed, by chance ($0): the baseline's own verdicts, resampled.

A "draw" is a set of question paths (every judgement of a question over the window, with the verdicts the baseline gave
them) drawn with replacement from the baseline's 16, with a given share of figure questions. The judge and the readers are
those of the baseline, so this estimates how often an unchanged judge on baseline-like questions crosses each line, and
how the lines move with the mix of question shapes. It does not estimate anything about the ladder step's questions.

  python3 clean-arch/step4-2026-11-10/stage_b/line_chance.py <data folder> <key path>
"""
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import baseline_count  # noqa: E402

DRAWS_A_TEST, TRIALS, SEED = 3, 20000, 20261114


def paths_of(folder, key):
    first, third, _, problems = baseline_count.read(folder, key)
    if problems:
        raise SystemExit(f'the reading is not complete: {problems[:3]}')
    paths = {}
    for number, entry in key.items():
        if entry['kind'] != 'stored':
            continue
        pair = [first[family][int(number)]['verdict'] for family in baseline_count.FAMILIES]
        if pair[0] == pair[1]:
            verdict = pair[0]
        else:
            rulings = [third[family][int(number)]['verdict'] for family in baseline_count.FAMILIES]
            verdict = rulings[0] if rulings[0] == rulings[1] else 'unresolved'
        paths.setdefault((entry['draw'], entry['view']), {'shape': entry['shape'], 'judgements': []})['judgements'].append((entry['number_in_view'], verdict))
    for path in paths.values():
        path['judgements'].sort()
    return list(paths.values())


def shares(sample, unresolved_as):
    verdicts = [unresolved_as if verdict == 'unresolved' else verdict for path in sample for _, verdict in path['judgements']]
    decided = sum(1 for verdict in verdicts if verdict in ('SUPPORTED', 'UNSUPPORTED'))
    unsupported = sum(1 for verdict in verdicts if verdict == 'UNSUPPORTED')
    lasts = [unresolved_as if path['judgements'][-1][1] == 'unresolved' else path['judgements'][-1][1] for path in sample]
    last_decided = sum(1 for verdict in lasts if verdict in ('SUPPORTED', 'UNSUPPORTED'))
    figure = [unresolved_as if verdict == 'unresolved' else verdict for path in sample if path['shape'] == 'figure' for _, verdict in path['judgements']]
    figure_decided = sum(1 for verdict in figure if verdict in ('SUPPORTED', 'UNSUPPORTED'))
    return (unsupported / decided if decided else None,
            sum(1 for verdict in lasts if verdict == 'SUPPORTED') / last_decided if last_decided else None,
            sum(1 for verdict in figure if verdict == 'UNSUPPORTED') / figure_decided if figure_decided else None)


def main():
    folder, key = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
    paths = paths_of(folder, key)
    figures = [path for path in paths if path['shape'] == 'figure']
    others = [path for path in paths if path['shape'] != 'figure']
    print(f'{len(paths)} question paths: {len(figures)} figures, {len(others)} yes/no')
    chooser = random.Random(SEED)
    print('per test of three draws; the unresolved judgement counted UNSUPPORTED (the stricter reading)')
    print(f"{'theses a draw':>13} {'figure share':>12} | {'P(overall UNSUPPORTED > 8%)':>28} {'P(figure UNSUPPORTED > 13%)':>28} {'P(last SUPPORTED < 90%)':>24} | median overall")
    for theses in (7, 10, 12):
        for figure_share in (0.375, 0.56):
            over, figure_over, last_under, overall = 0, 0, 0, []
            for _ in range(TRIALS):
                sample = []
                for _ in range(DRAWS_A_TEST * theses):
                    sample.append(chooser.choice(figures) if chooser.random() < figure_share else chooser.choice(others))
                unsupported_share, last_share, figure_unsupported = shares(sample, 'UNSUPPORTED')
                overall.append(unsupported_share or 0)
                over += (unsupported_share or 0) > 0.08
                figure_over += (figure_unsupported or 0) > 0.13
                last_under += last_share is not None and last_share < 0.90
            overall.sort()
            print(f'{theses:>13} {figure_share:>12.3f} | {over / TRIALS:>28.1%} {figure_over / TRIALS:>28.1%} {last_under / TRIALS:>24.1%} | {overall[TRIALS // 2]:.1%}')
    print('The baseline has no UNSUPPORTED last judgement (0 of 16), so the resampling cannot show line 5 missed by chance;')
    print('with an unchanged judge whose true rate of unsupported last judgements is p, a test of 30 theses misses line 5 (at')
    print('most 3 unsupported) with probability:')
    from math import comb
    for p in (0.02, 0.05, 0.10, 0.15):
        miss = 1 - sum(comb(30, k) * p ** k * (1 - p) ** (30 - k) for k in range(4))
        print(f'   p = {p:.0%}: {miss:.1%}')
    print('0 of 16 is consistent with a true rate up to about 17% (the upper end of a 95% interval).')


if __name__ == '__main__':
    main()
