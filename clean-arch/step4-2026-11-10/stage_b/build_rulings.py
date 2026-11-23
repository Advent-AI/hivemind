"""The third readers' packets of the Stage B baseline reading ($0): every judgement on which the two families' verdicts
differ, a control's included, as the readers saw it, with both verdicts and reasons under sides drawn per judgement from a
fixed seed (`ladder/stage-b-third-reader-brief.md`).

  python3 clean-arch/step4-2026-11-10/stage_b/build_rulings.py <data folder>
"""
import json
import random
import sys
from pathlib import Path

SIDES_SEED = 20261113
MOST_A_PACKET, MOST_CHARACTERS = 5, 150_000


def rows_of(folder, family):
    rows = {}
    for answer_file in sorted((folder / 'readers-answers').glob(f'reader-{family}-packet-*.jsonl')):
        for line in answer_file.read_text().splitlines():
            if line.strip().startswith('{'):
                row = json.loads(line)
                rows[int(row['judgement'])] = row
    return rows


def main():
    folder = Path(sys.argv[1])
    rows = {family: rows_of(folder, family) for family in ('codex', 'claude')}
    items = {row['judgement']: row for packet in sorted((folder / 'readers').glob('packet-*.json')) for row in json.loads(packet.read_text())}
    missing = [number for number in items if any(number not in rows[family] for family in rows)]
    if missing:
        raise SystemExit(f'no row from a family for judgements {missing[:10]}: the first readings are not complete')
    to_rule = []
    for number in sorted(items):
        if rows['codex'][number]['verdict'] == rows['claude'][number]['verdict']:
            continue
        order = ['codex', 'claude']
        random.Random(f'{SIDES_SEED}|{number}').shuffle(order)
        sides = {f'reader_{side}': {field: rows[family][number].get(field) for field in ('verdict', 'rung_the_evidence_points_to', 'why')} for side, family in zip('ab', order)}
        to_rule.append({**items[number], 'to_rule': {'judgement': number, **sides}})
    (folder / 'third-reader').mkdir(exist_ok=False)
    packets, current, size = [], [], 0
    for item in to_rule:
        length = len(item['request_as_sent'])
        if current and (len(current) == MOST_A_PACKET or size + length > MOST_CHARACTERS):
            packets.append(current)
            current, size = [], 0
        current.append(item)
        size += length
    if current:
        packets.append(current)
    for number, packet in enumerate(packets, start=1):
        (folder / 'third-reader' / f'ruling-packet-{number}.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    print(f'{len(to_rule)} judgements to rule on of {len(items)}, in {len(packets)} packets: {[len(packet) for packet in packets]}')


if __name__ == '__main__':
    main()
