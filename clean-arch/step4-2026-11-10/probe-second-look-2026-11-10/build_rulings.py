"""The third readers' packets of the second-look test's blind round ($0): every item on which the two first readers differ on a
mark, or on which one named a fault outside the form, with the item as the readers saw it. Which reader is "a" is drawn per
item from a fixed seed. The points have the form the third reader's brief describes.

  python3 clean-arch/step4-2026-11-10/probe-second-look-2026-11-10/build_rulings.py <probe data folder>
"""
import json
import random
import sys
from pathlib import Path

MARKS = ['Q', 'O', 'R', 'D', 'X', 'F', 'Y', 'L', 'XR', 'N']
ITEMS_A_PACKET = 12
SIDES_SEED = 20261112


def rows_of(folder, family):
    rows = {}
    for answer_file in sorted((folder / 'readers-answers').glob(f'reader-{family}-packet-*.jsonl')):
        for line in answer_file.read_text().splitlines():
            if line.strip().startswith('{'):
                row = json.loads(line)
                rows[row['item']] = row
    return rows


def main():
    folder = Path(sys.argv[1])
    rows = {family: rows_of(folder, family) for family in ('codex', 'claude')}
    items = {item['item']: item for packet in sorted((folder / 'readers').glob('packet-*.json')) for item in json.loads(packet.read_text())}
    to_rule = []
    for number in sorted(items):
        order = ['codex', 'claude']
        random.Random(f'{SIDES_SEED}|{number}').shuffle(order)
        sides = {'a': order[0], 'b': order[1]}
        points = []
        for mark in MARKS:
            values = {side: rows[family][number].get(mark) for side, family in sides.items()}
            if values['a'] != values['b'] and 'fails' in values.values():
                failing = 'a' if values['a'] == 'fails' else 'b'
                points.append({'id': f'{number}-{mark}', 'mark': mark, 'reader_a': values['a'], 'reader_b': values['b'],
                               f'reader_{failing}_reason': rows[sides[failing]][number].get('why', '')})
        for side, family in sides.items():
            named = (rows[family][number].get('W') or '').strip()
            if named:
                points.append({'id': f'{number}-W-{side}', 'mark': 'W', 'fault_named': named, 'the_reader_s_reason': rows[family][number].get('why', '')})
        if points:
            to_rule.append({**items[number], 'to_rule': points})
    (folder / 'third-reader').mkdir(exist_ok=True)
    packets = [to_rule[start:start + ITEMS_A_PACKET] for start in range(0, len(to_rule), ITEMS_A_PACKET)]
    for packet_number, packet in enumerate(packets, start=1):
        (folder / 'third-reader' / f'ruling-packet-{packet_number}.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    print(f'{len(to_rule)} items to rule on, {sum(len(item["to_rule"]) for item in to_rule)} points '
          f'({sum(1 for item in to_rule for point in item["to_rule"] if point["mark"] == "W")} faults named outside the form); '
          f'packets: {[(len(packet), sum(len(item["to_rule"]) for item in packet)) for packet in packets]}')


if __name__ == '__main__':
    main()
