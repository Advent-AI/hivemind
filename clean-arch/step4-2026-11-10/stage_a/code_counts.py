"""What code counts on Stage A's outcomes, with no reader ($0; DESIGN.md §8, "By code, every answer").

For every answer: its outcome; for a figure, whether it has a reference figure; for a company figure, whether production's
quarterly pattern matches its thesis's outcome or its question. For every thesis: whether its three sends agree on the object,
the answer shape, the due day and the favourable end, and whether the middle ranges of its figures overlap. A thesis counts as
agreeing on a point only when all three sends wrote a ladder and the three are the same on it.

  python3 clean-arch/step4-2026-11-10/stage_a/code_counts.py <run folder>
"""
import collections
import json
import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[2] / 'src')]
import accounting  # noqa: E402
from hivemind import extraction  # noqa: E402


def middle_range(ladder):
    """The middle of a figure's five ranges, lowest first, as exact decimals."""
    ranges = sorted(ladder['figure']['ranges'], key=lambda one: (one['lo'] is not None, Decimal(str(one['lo'])) if one['lo'] is not None else 0))
    middle = ranges[2]
    return Decimal(str(middle['lo'])), Decimal(str(middle['hi']))


def main():
    run_folder = Path(sys.argv[1])
    cases = {case['case']: case for case in json.loads((HERE / 'cases.json').read_text())}
    outcomes = [json.loads(line) for pass_folder in sorted(run_folder.glob('send-*')) for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines()]
    print('sends:', len(outcomes), dict(collections.Counter(accounting.kind_of(outcome) for outcome in outcomes)))
    figures = [outcome for outcome in outcomes if accounting.kind_of(outcome) in ('company figure', 'theme figure')]
    with_value = [outcome for outcome in figures if (outcome['answer']['ladder']['reference'] or {}).get('value') is not None]
    print(f'figures: {len(figures)}; with a reference figure: {len(with_value)}; with none: {len(figures) - len(with_value)}')
    quarterly = [(outcome['case'], outcome['pass']) for outcome in outcomes if accounting.kind_of(outcome) == 'company figure'
                 and (extraction.QUARTERLY.search(cases[outcome['case']]['thesis']['outcome']) or extraction.QUARTERLY.search(outcome['view']['question']))]
    print(f"company figures whose thesis outcome or question matches production's quarterly pattern: {len(quarterly)} {quarterly}")
    sends_of = collections.defaultdict(list)
    for outcome in outcomes:
        sends_of[outcome['case']].append(outcome)
    all_ladders = {case: sends for case, sends in sends_of.items() if all(accounting.kind_of(one) not in ('refusal', 'refused twice') for one in sends)}
    print(f'theses: {len(sends_of)}; all three sends a ladder: {len(all_ladders)}; all three declined: '
          f"{sorted(case for case, sends in sends_of.items() if all(accounting.kind_of(one) == 'refusal' for one in sends))}")
    differing = collections.defaultdict(list)
    for case, sends in sorted(all_ladders.items()):
        ladders = [one['answer']['ladder'] for one in sends]
        if len({one['view']['object_id'] for one in sends}) > 1:
            differing['object'].append((case, [one['view']['object_id'] for one in sends]))
        if len({accounting.kind_of(one) for one in sends}) > 1:
            differing['answer shape'].append((case, [accounting.kind_of(one) for one in sends]))
        if len({one['view']['due_day'] for one in sends}) > 1:           # the day the question is due, which the view carries (D414)
            differing['due day'].append((case, [one['view']['due_day'] for one in sends]))
        if all(accounting.kind_of(one) == 'company figure' for one in sends) and len({ladder['figure']['favourable_end'] for ladder in ladders}) > 1:
            differing['favourable end'].append((case, [ladder['figure']['favourable_end'] for ladder in ladders]))
        if all(ladder['figure'] is not None for ladder in ladders):
            middles = [middle_range(ladder) for ladder in ladders]
            if max(lo for lo, _ in middles) >= min(hi for _, hi in middles):
                differing['middle ranges do not overlap'].append((case, [f'{lo:,} to {hi:,}' for lo, hi in middles]))
    for point in ('object', 'answer shape', 'due day', 'favourable end', 'middle ranges do not overlap'):
        print(f'{point}: differs in {len(differing[point])} of {len(all_ladders)} theses whose three sends are ladders')
        for case, values in differing[point]:
            print('   ', case, values)
    mixed = {case: [accounting.kind_of(one) for one in sends] for case, sends in sorted(sends_of.items())
             if case not in all_ladders and not all(accounting.kind_of(one) == 'refusal' for one in sends)}
    print('theses with a ladder in some sends and none in others:', len(mixed))
    for case, kinds in mixed.items():
        print('   ', case, kinds)


if __name__ == '__main__':
    main()
