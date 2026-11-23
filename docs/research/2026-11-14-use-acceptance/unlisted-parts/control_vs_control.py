"""Round 79's $0 check of the decision rule's rule 2: the unchanged request against itself. The same 18 topics were sent unchanged
three times in D577's probe and three times in A2's probe, each read blind with third readers. For each group and mark, the sends
failing under each treatment of unresolved points, side by side, and the marks where the two control runs differ by more than one
(what rule 2 would call harm if one of them were the arm).

  python3 control_vs_control.py
"""
import collections
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import probe  # noqa: E402
import probe_score as ps  # noqa: E402

DATA = HERE.parents[3] / 'poc/data'
KEYS = Path(os.path.expanduser('~/.hivemind-keys'))
RUNS = {'D577': (DATA / 'clean-unlisted-probe-2026-11-16/reading', KEYS / 'unlisted-probe/key.json', 'a'),
        'A2': (DATA / 'clean-unlisted-probe-a2-2026-11-16/reading', KEYS / 'unlisted-probe-a2/key.json', 'a2')}
GROUPS = ('motivating', 'regression watch', 'harm control')


def control_counts(reading, key_path, configuration, unresolved_as):
    probe.configure(configuration)
    _, item_of, outcomes, readers, _ = ps.collector.read_rows(reading, key_path)
    families = ps.collector.third_reader_families(reading)
    of_family = {family: ps.collector.read_rulings(reading, item_of, outcomes, readers, family)[0] for family in families}
    h_given = ps.h_rulings(reading)
    groups = ps.group_of()
    counts = collections.Counter()
    for send, outcome in outcomes.items():
        topic = send[0].split('|', 1)[1] if send[0].startswith('control|') else None
        if groups.get(topic) not in GROUPS:
            continue
        if ps.accounting.kind_of(outcome) == 'refused twice':
            failed = {'refused twice'}
        else:
            rows = (readers['reader 1'][send], readers['reader 2'][send])
            failed = ps.failed_marks(send, outcome, rows, of_family, families, h_given, item_of[send], unresolved_as)
        for mark in failed & set(ps.OTHER_MARKS + ['L']):
            counts[(groups[topic], mark)] += 1
    return counts


def main():
    for unresolved_as in ('holds', 'fails'):
        first, second = (control_counts(*RUNS[name], unresolved_as) for name in ('D577', 'A2'))
        keys = sorted(set(first) | set(second))
        print(f'== unresolved counted {"for" if unresolved_as == "holds" else "against"} the answer: control (D577 run) against control (A2 run)')
        for key in keys:
            flag = '  <- differs by more than 1' if abs(first[key] - second[key]) > 1 else ''
            print(f'   {key[0]:16} {key[1]:14} {first[key]:3} {second[key]:3}{flag}')
    probe.configure('a')
    return 0


if __name__ == '__main__':
    sys.exit(main())
