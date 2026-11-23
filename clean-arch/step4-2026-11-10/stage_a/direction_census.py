"""Which end of a company's figure each send called good for the company, thesis by thesis, over stored runs ($0).

Line 6 of Stage A asks that the favourable end be the same in a thesis's three sends. This prints, for every thesis that drew a
company's figure in any send, the end each send gave in each run, the thesis's own words beside it, and the reasons the sends
gave where the ends differ. Nothing is sent.

  python3 clean-arch/step4-2026-11-10/stage_a/direction_census.py <run folder> [<run folder> ...]
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMPANY = 'NVDA'


def short(text, length):
    text = ' '.join(str(text).split())
    return text if len(text) <= length else text[:length - 1] + '…'


def rows_of(run_folder):
    return {(row['case'], row['pass']): row for pass_folder in sorted(Path(run_folder).glob('send-*'))
            for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)]}


def end_of(row):
    """higher or lower for a company's figure; otherwise what the send was instead."""
    if row is None:
        return 'not sent'
    if row['status'] != 'ladder':
        return 'declined' if row['status'] == 'no ladder' else 'refused twice'
    figure = row['answer']['ladder'].get('figure')
    if not figure:
        return 'an event'
    return figure['favourable_end'] if row['view']['object_id'] == COMPANY else "a theme's figure"


def main():
    run_folders = [Path(argument) for argument in sys.argv[1:]]
    if not run_folders:
        raise SystemExit('name at least one run folder')
    cases = json.loads((HERE / 'cases.json').read_text())
    runs = {run_folder.name: rows_of(run_folder) for run_folder in run_folders}
    judged, both_ends_in_a_run, both_ends_in_any = 0, {name: 0 for name in runs}, 0
    for case in cases:
        name_of_case = case['case']
        by_run = {name: [end_of(rows.get((name_of_case, pass_number))) for pass_number in (1, 2, 3)] for name, rows in runs.items()}
        ends_seen = {end for ends in by_run.values() for end in ends if end in ('higher', 'lower')}
        if not ends_seen:
            continue
        judged += 1
        both_ends_in_any += len(ends_seen) == 2
        for name, ends in by_run.items():
            both_ends_in_a_run[name] += len({end for end in ends if end in ('higher', 'lower')}) == 2
        print('-' * 110)
        print(f"{name_of_case} | {'BOTH ENDS' if len(ends_seen) == 2 else 'one end'} | " + ' | '.join(f'{name}: {ends}' for name, ends in by_run.items()))
        print('   the thesis:', short(case['thesis']['description'], 400))
        if len(ends_seen) == 2:
            for name, rows in runs.items():
                for pass_number in (1, 2, 3):
                    row = rows.get((name_of_case, pass_number))
                    if end_of(row) in ('higher', 'lower'):
                        figure = row['answer']['ladder']['figure']
                        print(f"   {name} send {pass_number}: {figure['favourable_end']}: {short(figure['favourable_why'], 230)}")
    print('=' * 110)
    print(f"theses with a company's figure in any send: {judged}")
    for name, count in both_ends_in_a_run.items():
        print(f'  both ends among the sends of {name}: {count}')
    print(f'  both ends in any send of any run named: {both_ends_in_any}')
    if judged == 0:
        raise SystemExit('no company figure found: nothing was judged')


if __name__ == '__main__':
    main()
