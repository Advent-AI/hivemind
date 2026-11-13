"""Stage A's result, broken down ($0): each send's marks after the rulings, by kind of answer and by thesis, and the two
bounds of line 5 when every disputed point is decided one way (all for the answer, all against it).

  python3 clean-arch/step4-2026-11-10/stage_a/result_tables.py <run folder> <key path>
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import accounting  # noqa: E402
import collect_readings  # noqa: E402


def final_values(outcomes, readers, rulings, disputed_as=None):
    """{send: (failed marks, upheld faults)} after the rulings; with `disputed_as`, every differing mark takes that value and a
    named fault is upheld when it is 'fails'."""
    values = {}
    for send, outcome in outcomes.items():
        kind = accounting.kind_of(outcome)
        if kind == 'refused twice':
            continue
        rows = [readers[reader][send] for reader in collect_readings.FAMILIES]
        failed = []
        for mark in accounting.marks_that_apply(kind):
            if rows[0][mark] == rows[1][mark]:
                value = rows[0][mark]
            else:
                value = disputed_as or rulings[send]['marks'][mark]
            if value == 'fails':
                failed.append(mark)
        named = [reader for reader, row in zip(collect_readings.FAMILIES, rows) if row['W'].strip()]
        upheld = [reader for reader in named if (disputed_as == 'fails' if disputed_as else rulings[send]['W'][reader])]
        values[send] = (failed, upheld)
    return values


def line_5(outcomes, values):
    sends_of = collections.defaultdict(list)
    for send, outcome in outcomes.items():
        sends_of[send[0]].append((send, outcome))
    right = by_ladder = 0
    for sends in sends_of.values():
        sound = [send in values and not values[send][0] and not values[send][1] for send, _ in sends]
        ladders = [is_sound and accounting.kind_of(outcome) != 'refusal' for is_sound, (_, outcome) in zip(sound, sends)]
        right += sum(sound) >= 2
        by_ladder += sum(ladders) >= 2
    return right, by_ladder, len(sends_of)


def rulings_under(run_folder, item_of, outcomes, readers, unresolved_as):
    """The rulings a run is counted with: its one third reader's, or, with two third readers, what they agree on with every
    point they leave unresolved taking `unresolved_as`."""
    families = collect_readings.third_reader_families(run_folder)
    if families == [None]:
        rulings, missing = collect_readings.read_rulings(run_folder, item_of, outcomes, readers)
        assert not missing, missing
        return rulings
    of_family = {}
    for family in families:
        of_family[family], missing = collect_readings.read_rulings(run_folder, item_of, outcomes, readers, family)
        assert not missing, missing
    return {send: accounting.rulings_of_two(of_family[families[0]][send], of_family[families[1]][send], unresolved_as)[0]
            for send in of_family[families[0]]}


def main():
    run_folder, key_path = sys.argv[1], sys.argv[2]
    _, item_of, outcomes, readers, _ = collect_readings.read_rows(run_folder, key_path)
    two = collect_readings.third_reader_families(run_folder) != [None]
    readings = [('every differing mark held, no named fault upheld (only what both first readers fail)', final_values(outcomes, readers, {}, 'holds'))]
    if two:
        readings.append(('as the two third readers agree; what they leave unresolved counted for the answer', final_values(outcomes, readers, rulings_under(run_folder, item_of, outcomes, readers, 'holds'))))
        readings.append(('as the two third readers agree; what they leave unresolved counted against it', final_values(outcomes, readers, rulings_under(run_folder, item_of, outcomes, readers, 'fails'))))
    else:
        readings.append(('as the third reader ruled', final_values(outcomes, readers, rulings_under(run_folder, item_of, outcomes, readers, None))))
    readings.append(('every differing mark failed, every named fault upheld', final_values(outcomes, readers, {}, 'fails')))
    for label, values in readings:
        right, by_ladder, of = line_5(outcomes, values)
        ladders = [send for send, outcome in outcomes.items() if accounting.kind_of(outcome) not in ('refusal', 'refused twice')]
        sound = sum(1 for send in ladders if not values[send][0] and not values[send][1])
        print(f'{label}:')
        print('   ' + ', '.join(f"{mark} fails on {sum(1 for failed, _ in values.values() if mark in failed)}" for mark in ('Q', 'L', 'R', 'N'))
              + f'; theses right {right}, by a ladder {by_ladder}, of {of}; ladders sound {sound} of {len(ladders)}')
    print()
    for label, values in readings[:1] + readings[-2:-1] if two else readings[:2]:
        print(f'by kind of answer, {label}: sends, sound, and the marks failed')
        by_kind = collections.defaultdict(list)
        for send, outcome in outcomes.items():
            by_kind[accounting.kind_of(outcome)].append(send)
        for kind, sends in sorted(by_kind.items()):
            if kind == 'refused twice':
                print(f'  {kind}: {len(sends)}')
                continue
            failed_marks = collections.Counter(mark for send in sends for mark in values[send][0])
            sound = sum(1 for send in sends if not values[send][0] and not values[send][1])
            print(f'  {kind}: {len(sends)} sends, {sound} sound; failed {dict(failed_marks)}; with an upheld fault {sum(1 for send in sends if values[send][1])}')
        print()
    label, values = readings[1]
    print(f'by thesis, {label}: the three sends (kind: failed marks, +W for an upheld fault)')
    for case in sorted({send[0] for send in outcomes}):
        cells, sound_count = [], 0
        for pass_number in (1, 2, 3):
            send = (case, pass_number)
            kind = accounting.kind_of(outcomes[send])
            if kind == 'refused twice':
                cells.append('refused twice')
                continue
            failed, upheld = values[send]
            sound_count += not failed and not upheld
            cells.append(f"{kind}: {' '.join(failed) or 'sound'}{' +W' if upheld else ''}")
        print(f"  {'RIGHT' if sound_count >= 2 else 'not  '} {case:<12} | " + ' | '.join(cells))


if __name__ == '__main__':
    main()
