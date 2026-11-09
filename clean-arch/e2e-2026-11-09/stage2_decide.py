"""Apply Stage 2's frozen decision rule (stage2-frozen.md) to the six Stage 2 runs, each scored by the frozen judgement scorer. Prints
every question and draw for both arms, the totals with and without q09, q12 and q23, any collapse, and the verdict. It judges nothing
itself: outcomes are the frozen scorer's, read by calibrate.outcomes. Clean runs are scored from their adapter folders."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from calibrate import NOISE, collapse, outcomes, total  # noqa: E402

DATA = ROOT / 'poc/data/clean-e2e-2026-11-09'
CLEAN = [DATA / f'stage2-clean-d{d}/judged' for d in (1, 2, 3)]
CONTROL = [DATA / f'stage2-control-d{d}' for d in (1, 2, 3)]


def verdict(clean, control):
    difference_all = total(clean) - total(control)
    difference_quiet = total(clean, NOISE) - total(control, NOISE)
    collapsed = collapse(control, clean)
    q10_q12 = all(sum(o[q] == 'agree' for o in clean) >= 2 for q in ('q10', 'q12'))
    if collapsed or difference_all <= -3:
        return 'worse', difference_all, difference_quiet, collapsed
    if difference_all >= 3 and difference_quiet >= 4 and q10_q12:
        return 'better', difference_all, difference_quiet, collapsed
    return 'inconclusive', difference_all, difference_quiet, collapsed


def main():
    clean, control = [outcomes(run) for run in CLEAN], [outcomes(run) for run in CONTROL]
    print(f'{"q":<5}' + ''.join(f'clean-d{d:<6}' for d in (1, 2, 3)) + ''.join(f'ctrl-d{d:<7}' for d in (1, 2, 3)))
    for q in sorted(control[0]):
        print(f'{q:<5}' + ''.join(f'{o.get(q, "-"):<13}' for o in clean + control))
    print('totals all questions: clean', [total([o]) for o in clean], 'control', [total([o]) for o in control])
    print('totals without q09, q12, q23: clean', [total([o], NOISE) for o in clean], 'control', [total([o], NOISE) for o in control])
    result, difference_all, difference_quiet, collapsed = verdict(clean, control)
    print(f'difference all {difference_all:+d}, without noise questions {difference_quiet:+d}, collapse {collapsed}: {result.upper()}')


if __name__ == '__main__':
    main()
