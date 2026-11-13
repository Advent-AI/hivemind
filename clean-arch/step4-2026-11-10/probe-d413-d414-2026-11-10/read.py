"""Read the small send of D413 and D414 as REGISTERED.md says ($0). Written before any answer exists.

  python3 clean-arch/step4-2026-11-10/probe-d413-d414-2026-11-10/read.py <probe folder>
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run  # noqa: E402

ARMS = ('with-tie-rule', 'without-tie-rule')      # the first small send; the second has the one arm `working`
NEW_REFUSAL = 'before that: a figure is published after the period it covers ends'


def short(text, length):
    text = ' '.join(str(text).split())
    return text if len(text) <= length else text[:length - 1] + '…'


def rows_of(folder, arm):
    return {(row['case'], row['pass']): row for pass_folder in sorted((Path(folder) / arm).glob('send-*'))
            for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)]}


def one_send(row):
    """One line for a send: what it ended as and, for a ladder, the days and the favourable end."""
    if row is None:
        return 'NOT COMPLETE: no outcome stored'
    back = [reason for request in row['requests'] for reason in request.get('reasons', [])]
    note = f" | sent back first for: {'; '.join(short(reason, 150) for reason in back)}" if back else ''
    if row['status'] == 'no ladder':
        return f"declined: {short(row['reason'], 170)}{note}"
    if row['status'] != 'ladder':
        return f"REFUSED TWICE{note}"
    ladder, view = row['answer']['ladder'], row['view']
    if ladder.get('figure'):
        figure = ladder['figure']
        return (f"{view['object_id']} figure {figure['year']} | wrote {ladder['due_day']} ({ladder['due_day_basis']}) -> due {view['due_day']} | "
                f"favourable {figure['favourable_end']}: {short(figure['favourable_why'], 120)}{note}")
    return f"{view['object_id']} event | due {view['due_day']} ({ladder['due_day_basis']}) | OUT: {short(ladder['event']['ruled_out'], 130)}{note}"


def main():
    folder = Path(sys.argv[1])
    arms = ('working',) if (folder / 'working').exists() else ARMS
    theses = run.SECOND_SEND_THESES if arms == ('working',) else run.THESES
    stored = {arm: rows_of(folder, arm) for arm in arms}
    groups = [('amounts the company owes or guarantees', run.OBLIGATIONS), ("not a year's figure", run.NOT_A_YEARS_FIGURE),
              ('other figures', run.OTHER_FIGURES), ('events', [name for name in theses if name in run.EVENTS + run.FRENCH_INVESTIGATION])]
    for title, names in groups:
        print('#' * 110)
        print(title)
        for name in names:
            print('-' * 110)
            print(name)
            for arm in arms:
                for pass_number in (1, 2, 3):
                    print(f'  {arm:17} send {pass_number}: {one_send(stored[arm].get((name, pass_number)))}')
    print('#' * 110)
    for arm in arms:
        rows = stored[arm]
        statuses = collections.Counter(row['status'] for row in rows.values())
        back = collections.Counter(short(reason, 60) for row in rows.values() for request in row['requests'] for reason in request.get('reasons', []))
        fired = sorted({case for (case, _), row in rows.items() for request in row['requests'] for reason in request.get('reasons', []) if NEW_REFUSAL in reason})
        print(f'{arm}: {len(rows)} of {len(theses) * 3} sends stored; {dict(statuses)}')
        print(f'  first answers sent back, by reason: {dict(back)}')
        print(f'  the new refusal fired on: {fired}')
        ends = {}
        for name in run.OBLIGATIONS:
            ends[name] = [row['answer']['ladder']['figure']['favourable_end'] if row and row['status'] == 'ladder' and row['answer']['ladder'].get('figure') else
                          ('-' if row is None else row['status']) for row in (rows.get((name, pass_number)) for pass_number in (1, 2, 3))]
        one_end = [name for name, values in ends.items() if len(values) == 3 and len(set(values)) == 1 and values[0] in ('higher', 'lower')]
        print(f'  the nine amounts: one end in all three sends: {len(one_end)}; the others: ' + str({name: values for name, values in ends.items() if name not in one_end}))
        days = collections.defaultdict(set)
        shapes = collections.defaultdict(set)
        for (case, _), row in rows.items():
            if row['status'] == 'ladder':
                ladder = row['answer']['ladder']
                days[case].add(row['view']['due_day'])
                shapes[case].add((ladder['figure']['year'] if ladder.get('figure') else 'event', ladder['due_day_basis'], row['view']['object_id']))
        whole = [case for case in theses if all(rows.get((case, pass_number)) and rows[(case, pass_number)]['status'] == 'ladder' for pass_number in (1, 2, 3))]
        print(f'  theses whose three sends are ladders: {len(whole)}; one due day: {sum(1 for case in whole if len(days[case]) == 1)}; '
              f'more than one: ' + str({case: sorted(days[case]) for case in whole if len(days[case]) > 1}))
        print(f'  of those with more than one day, one year, basis and object throughout: {[case for case in whole if len(days[case]) > 1 and len(shapes[case]) == 1]}')

        without_ruling_out = {name: [None if (row is None or row['status'] != 'ladder' or not row['answer']['ladder'].get('event')) else row['answer']['ladder']['event']['ruled_out'] is None
                                     for row in (rows.get((name, pass_number)) for pass_number in (1, 2, 3))]
                              for name in theses if name in run.EVENTS + run.FRENCH_INVESTIGATION}
        print(f'  events, a send with no ruling out (True), with one (False), not an event ladder (None): {without_ruling_out}')


if __name__ == '__main__':
    main()
