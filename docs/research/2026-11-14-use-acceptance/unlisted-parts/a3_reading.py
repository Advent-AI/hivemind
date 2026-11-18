"""DESIGN-A3.md v11's two added readings: the blind classer's packet and the named-way adjudication's packet, and their loaders.

  python3 a3_reading.py classer-packet <reading folder> <key path>   -> <reading>/a3/class-packet-<n>.json
  python3 a3_reading.py named-packet <reading folder>                -> <reading>/a3/named-packet-<n>.json (from the classer's answers)

The classer sees each entry listed on the four event topics, with the topic, the choices as the judge is shown them (from the first
readers' packets) and the topic's matters; never the arm, the pass or the design. Item numbers are the reading's shuffled ones.
"""
import json
import sys
from pathlib import Path

EVENT_TOPICS = ['fortnight:c1/clean-6', 'fortnight:c1/clean-7', 'july:c1/clean-5', 'fortnight:c1/clean-3']
MATTERS = {   # written before the send from both arms' stored entries (DESIGN-A3.md v11, "parts kept"); 'other' for anything else
    'fortnight:c1/clean-6': ["the deal's price or value", 'a repricing', 'signing apart from closing', 'when the agreement was made',
                             'a delay past the check date', 'a termination or withdrawal'],
    'fortnight:c1/clean-7': ['a cap on the quantities approved', 'Nvidia shipping to China or booking the revenue',
                             'earlier signals of intent or purchase plans', 'the sales being allowed to proceed', 'MIIT blocking or rejecting the purchases',
                             'a delay'],
    'july:c1/clean-5': ['whether DeepSeek accessed the chips', 'a conclusion without a finding, penalty or measure',
                        "the investigation's conclusion as such"],
    'fortnight:c1/clean-3': ['U.S. permission for H200 exports', 'Chinese restrictions on shipments', 'China data-center revenue resuming',
                             'a comparison with H200'],
}
KINDS = ('restates happening', 'restates ruled out unnamed', 'restates still awaited', 'named way', 'other', 'cannot tell')
RESTATING = KINDS[:3]
H_VALUES = ('part', 'already_judged', 'settlement', 'cannot_tell')
PER_PACKET = 60


def topic_of(case_name):
    return case_name.split('|', 1)[1]


def classer_packet(reading, key_path):
    reading = Path(reading)
    key = json.loads(Path(key_path).read_text())
    shown = {str(item['item']): item for path in sorted((reading / 'readers').glob('packet-*.json')) for item in json.loads(path.read_text())}
    entries = []
    for item in sorted(key, key=int):
        case_name, _ = key[item]
        if case_name.startswith('plant|') or topic_of(case_name) not in EVENT_TOPICS or item not in shown:
            continue
        packet_item = shown[item]
        for position, part in enumerate(packet_item['other_fields'].get('not_judged') or []):
            entries.append({'id': f'{item}-H-{position}', 'topic': packet_item['thesis'],
                            'choices_as_shown': packet_item['ladder_as_the_judge_is_shown_it'].get('rungs'),
                            'entry': part['part'], 'why': part.get('why', ''), 'matters': MATTERS[topic_of(case_name)] + ['other']})
    out = reading / 'a3'
    out.mkdir(exist_ok=True)
    for number, start in enumerate(range(0, len(entries), PER_PACKET), start=1):
        (out / f'class-packet-{number}.json').write_text(json.dumps(entries[start:start + PER_PACKET], ensure_ascii=False, indent=1) + '\n')
    print(f'{len(entries)} entries in {(len(entries) + PER_PACKET - 1) // PER_PACKET} classer packets')
    return entries


def json_lines(path):
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('```'):
            yield json.loads(line)


def read_classes(reading):
    """{entry id: [{'text', 'kind', 'matter'}, ...]} from the classer's answers, checked against its packets: every entry exactly once,
    a known kind, a matter from the entry's list."""
    reading = Path(reading) / 'a3'
    asked = {entry['id']: entry for path in sorted(reading.glob('class-packet-*.json')) for entry in json.loads(path.read_text())}
    given = {}
    for path in sorted(reading.glob('class-codex-*.jsonl')):
        for row in json_lines(path):
            entry, parts = asked.get(row.get('id')), row.get('parts')
            if entry is None or row['id'] in given or not isinstance(parts, list) or not parts:
                raise SystemExit(f'NOT SCORED: classer row not valid or repeated: {str(row)[:100]}')
            for part in parts:
                if part.get('kind') not in KINDS or part.get('matter') not in entry['matters'] or not str(part.get('text', '')).strip():
                    raise SystemExit(f'NOT SCORED: classer part not valid in {row["id"]}: {part}')
            given[row['id']] = parts
    if set(given) != set(asked):
        raise SystemExit(f'NOT SCORED: classer answers missing for {sorted(set(asked) - set(given))[:5]}')
    return given


def named_packet(reading):
    reading = Path(reading)
    classes = read_classes(reading)
    asked = {entry['id']: entry for path in sorted((reading / 'a3').glob('class-packet-*.json')) for entry in json.loads(path.read_text())}
    points = [{'id': f'{entry_id}-{number}', 'part': part['text'], 'entry': asked[entry_id]['entry'], 'topic': asked[entry_id]['topic'],
               'choices_as_shown': asked[entry_id]['choices_as_shown']}
              for entry_id in sorted(classes, key=lambda name: [int(piece) if piece.isdigit() else piece for piece in name.split('-')])
              if any(part['kind'] == 'named way' for part in classes[entry_id])
              for number, part in enumerate(classes[entry_id])]
    for number, start in enumerate(range(0, len(points), PER_PACKET), start=1):
        (reading / 'a3' / f'named-packet-{number}.json').write_text(json.dumps(points[start:start + PER_PACKET], ensure_ascii=False, indent=1) + '\n')
    print(f'{len(points)} parts of entries with a named way, in {(len(points) + PER_PACKET - 1) // PER_PACKET} packets')
    return points


def read_named(reading):
    """{point id: {family: ruling}} from both families' answers; every point of the packets ruled once by each family, or refused."""
    reading = Path(reading) / 'a3'
    asked = {point['id'] for path in sorted(reading.glob('named-packet-*.json')) for point in json.loads(path.read_text())}
    given = {}
    for family in ('codex', 'claude'):
        for path in sorted(reading.glob(f'named-{family}-*.jsonl')):
            for row in json_lines(path):
                if row.get('id') not in asked or row.get('ruling') not in H_VALUES or family in given.get(row['id'], {}):
                    raise SystemExit(f'NOT SCORED: named-way ruling not valid or repeated ({family}): {str(row)[:100]}')
                given.setdefault(row['id'], {})[family] = row['ruling']
    missing = sorted(point for point in asked if len(given.get(point, {})) != 2)
    if missing:
        raise SystemExit(f'NOT SCORED: named-way rulings missing for {missing[:5]}')
    return given


if __name__ == '__main__':
    command, arguments = sys.argv[1], sys.argv[2:]
    sys.exit(0 if (classer_packet(*arguments) if command == 'classer-packet' else named_packet(*arguments)) is not None else 1)
