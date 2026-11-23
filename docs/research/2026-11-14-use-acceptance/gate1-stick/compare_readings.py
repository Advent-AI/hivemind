"""Two gate-1 readings of the same sends, compared by the gate's own accounting ($0; gate1-stick/DESIGN.md). It judges nothing.

For each reading and each treatment of unresolved points it runs `accounting.account` as `collect_readings.py report` does, then
reports: each line's verdict in each reading ("not measured" kept apart from met and missed); for lines 1 to 3 the failing sends
in both readings, in the first only and in the second only, with each set's size; per send and mark (Q, L, R) the settled values
that changed; the upheld W faults of each reading with their reasons; line 5's counts of topics right; the dispute shares; and the
author-checked controls (`controls.json`) against each reading. It refuses two readings of different sends and a reading without
third readers of both families; a reading with a missing row or ruling is reported as not measured.

  python3 compare_readings.py <first stage-a folder> <second stage-a folder> <key path>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path('/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a')))
import accounting  # noqa: E402
import collect_readings as collector  # noqa: E402

TREATMENTS = (('unresolved counted for the answer', 'holds'), ('unresolved counted against it', 'fails'))


def reading(folder, key_path):
    _, item_of, outcomes, readers, _ = collector.read_rows(folder, key_path)
    families = collector.third_reader_families(folder)
    if families != ['claude', 'codex']:
        raise SystemExit(f'{folder}: third readers of both families are required, found {families}: refused (no one-reader fallback)')
    of_family, missing = {}, []
    for family in families:
        of_family[family], absent = collector.read_rulings(folder, item_of, outcomes, readers, family)
        missing += [f'{family}: {m}' for m in absent]
    out = {}
    for label, unresolved_as in TREATMENTS:
        rulings = {send: accounting.rulings_of_two(of_family[families[0]][send], of_family[families[1]][send], unresolved_as)[0]
                   for send in of_family[families[0]]}
        report = accounting.account(list(outcomes.values()), readers['reader 1'], readers['reader 2'], rulings)
        settled = {}
        for send, outcome in outcomes.items():
            rows = (readers['reader 1'].get(send), readers['reader 2'].get(send))
            if not all(rows) or accounting.kind_of(outcome) == 'refused twice':
                continue
            for mark in ('Q', 'L', 'R'):
                if mark in accounting.marks_that_apply(accounting.kind_of(outcome)):
                    settled[(send, mark)] = rows[0][mark] if rows[0][mark] == rows[1][mark] else rulings.get(send, {}).get('marks', {}).get(mark, 'no ruling')
        out[label] = {'report': report, 'settled': settled}
    return out, missing


def sends_of(folder):
    """The sends a reading read, as the stored outcomes give them (case, pass, status, answer), before any accounting runs."""
    return sorted(json.dumps({k: outcome.get(k) for k in ('case', 'pass', 'status', 'answer')}, sort_keys=True)
                  for outcome in collector.outcomes_of(folder))


def failing(line):
    return set(line[1]) if isinstance(line, tuple) and line[0] in ('met', 'missed') else None


def main(first, second, key_path):
    if sends_of(first) != sends_of(second):
        raise SystemExit('the two readings are not of the same sends (case, pass, status and answer): refused')
    print(f'the same {len(sends_of(first))} sends in both readings')
    a, missing_a = reading(first, key_path)
    b, missing_b = reading(second, key_path)
    print(f'missing rulings: first {missing_a or "none"} | second {missing_b or "none"}')
    for label, _ in TREATMENTS:
        ra, rb = a[label]['report'], b[label]['report']
        print(f'\n===== {label} =====')
        print(f"reading: {ra['reading']} / {rb['reading']} | dispute share {ra['dispute share']} / {rb['dispute share']}")
        for number in (1, 2, 3):
            la, lb = ra['lines'][number], rb['lines'][number]
            fa, fb = failing(la), failing(lb)
            verdicts = f"{la[0] if isinstance(la, tuple) else la} / {lb[0] if isinstance(lb, tuple) else lb}"
            if fa is None or fb is None:
                print(f'line {number}: {verdicts} (a reading not measured: no comparison of sends)')
                continue
            union = fa | fb
            print(f'line {number}: {verdicts} | failing first {len(fa)}, second {len(fb)}, union {len(union)}; both {len(fa & fb)}, '
                  f'first only {len(fa - fb)}, second only {len(fb - fa)}'
                  + ('' if union else ' (no failing send in either reading)'))
            for send in sorted(fa - fb):
                print(f'     first only: {send}')
            for send in sorted(fb - fa):
                print(f'     second only: {send}')
        for number in (4, 5):
            print(f"line {number}: {ra['lines'][number]} / {rb['lines'][number]}")
        if ra['reading'] != 'complete' or rb['reading'] != 'complete':
            print('marks, W faults and controls: not compared (a reading is not measured)')
            continue
        changed = [(k, a[label]['settled'][k], b[label]['settled'].get(k)) for k in sorted(a[label]['settled'])
                   if b[label]['settled'].get(k) != a[label]['settled'][k]]
        print(f'Q/L/R settled values changed: {len(changed)} of {len(a[label]["settled"])}')
        for (send, mark), va, vb in changed:
            print(f'     {send} {mark}: {va} -> {vb}')
        print(f"W upheld: first {[(s, r, why[:80]) for s, r, why in ra['upheld W']]}")
        print(f"W upheld: second {[(s, r, why[:80]) for s, r, why in rb['upheld W']]}")
        controls = json.loads((HERE / 'controls.json').read_text())['controls']
        for control in controls:
            send = (control['case'], control['pass'])
            got_a = {m: a[label]['settled'].get((send, m)) for m in control['expected']}
            got_b = {m: b[label]['settled'].get((send, m)) for m in control['expected']}
            print(f"control {send}: expected {control['expected']} | first {got_a} | second {got_b}")


if __name__ == '__main__':
    main(*sys.argv[1:4])
