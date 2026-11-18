"""The registered rule of DESIGN.md section 5 on the new week's reading ($0): the collector's own accounting, run on the wider and
the strict count of topics, each with every unresolved point counted for the answer and then against it, plus the facts code
establishes alone (the favourable end and the due day across a topic's attempts). It judges nothing itself.

  python3 second_week_account.py <stage-a folder> <key path>
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'clean-arch/step4-2026-11-10/stage_a'))
import accounting  # noqa: E402
import collect_readings  # noqa: E402


def main(run_folder, key_path):
    _, item_of, outcomes, readers, problems = collect_readings.read_rows(run_folder, key_path)
    families = collect_readings.third_reader_families(run_folder)
    of_family = {family: collect_readings.read_rulings(run_folder, item_of, outcomes, readers, family)[0] for family in families}
    topics = json.loads((HERE / 'topics-opening-articles.json').read_text())['topics']
    exposure = {topic['case']: topic['exposure'] for topic in topics}
    counts = {'every topic (description only)': set(exposure),
              'wider count (opening article not seen before)': {case for case, kind in exposure.items() if kind != 'seen before'},
              'strict count (opening article not found in the search)': {case for case, kind in exposure.items() if kind == 'not found in the search'}}
    rows = (readers['reader 1'], readers['reader 2'])
    out = {}
    for name, cases in counts.items():
        subset = [outcome for send, outcome in outcomes.items() if send[0] in cases]
        n = len(cases)
        need_right, need_ladder = math.ceil(35 * n / 44), math.ceil(28 * n / 44)
        print(f'===== {name}: {n} topics, {len(subset)} attempts; needs {need_right} right in two of three and {need_ladder} by written choices =====')
        verdicts = {}
        for label, unresolved_as in (('unresolved points counted for the answer', 'holds'), ('unresolved points counted against it', 'fails')):
            rulings = {}
            for send in of_family[families[0]]:
                if send[0] in cases:
                    rulings[send], _ = (accounting.rulings_of_two(of_family[families[0]][send], of_family[families[1]][send], unresolved_as)
                                        if len(families) == 2 else (of_family[families[0]][send], []))
            report = accounting.account(subset, *rows, rulings)
            lines = report['lines']
            five = lines[5][1] if isinstance(lines[5], tuple) else {}
            zero_fault = {number: (lines[number] if isinstance(lines[number], str) else f'{lines[number][0]} {[item_of[send] for send in lines[number][1]]}') for number in (1, 2, 3, 4)}
            scaled = isinstance(lines[5], tuple) and five['right'] >= need_right and five['right by a ladder'] >= need_ladder
            print(f'  -- {label}: reading {report["reading"]}; disputed marks {report["dispute share"]}')
            for number in (1, 2, 3, 4):
                print(f'     line {number}: {zero_fault[number]}')
            print(f"     line 5 (scaled): right {five.get('right')} of {n} (needs {need_right}), by written choices {five.get('right by a ladder')} (needs {need_ladder}): {'met' if scaled else 'missed'}")
            verdicts[label] = {'zero-fault lines': zero_fault, 'right': five.get('right'), 'by written choices': five.get('right by a ladder'), 'scaled line 5': scaled,
                               'reading': report['reading']}
        ladders_of = {case: [outcome for send, outcome in sorted(outcomes.items()) if send[0] == case and accounting.kind_of(outcome) not in ('refusal', 'refused twice')] for case in cases}
        figures = [case for case in cases if len(ladders_of[case]) == 3 and all(accounting.kind_of(o) == 'company figure' for o in ladders_of[case])]
        direction_differs = [case for case in figures if len({o['answer']['ladder']['figure']['favourable_end'] for o in ladders_of[case]}) > 1]
        all_ladders = [case for case in cases if len(ladders_of[case]) == 3]
        same_day = [case for case in all_ladders if len({o['view']['due_day'] for o in ladders_of[case]}) == 1]
        due_day_met = bool(all_ladders) and len(same_day) * 10 >= len(all_ladders) * 9
        print(f'  -- by code: favourable end the same in {len(figures) - len(direction_differs)} of {len(figures)} company figures; '
              f"due day the same in {len(same_day)} of {len(all_ladders)} topics with three written answers ({'met' if due_day_met else 'missed'}: nine in ten needed); "
              f"differing: {sorted(set(all_ladders) - set(same_day))}")
        out[name] = {'topics': n, 'needs': [need_right, need_ladder], 'verdicts': verdicts, 'direction differs': direction_differs,
                     'same due day': [len(same_day), len(all_ladders)], 'due day line': due_day_met}
    (Path(run_folder) / 'second-week-account.json').write_text(json.dumps(out, indent=1, ensure_ascii=False, default=list) + '\n')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
