"""The split probe's reading folder (DESIGN.md v4 §3 item 3): the items the two reader families read, blind, in one Stage A run folder,
so the Stage A collector and accounting read it unchanged.

Items: every yearly ladder of T and M (the split arm's children), every C1 ladder of both arms, and two plants. Yearly items carry
`split` ({asked_year, asked_separately}); every other item carries `split: null`. The arm and the topic are in the key only, outside
the repository. The plants are stored frozen ladders edited in one way each, with the field a reader must mark `yes`:
- `plant|1` asks the base year: a stored 2027 ladder of a topic that tracks 2027 with 2026 as context, rewritten for 2026 and given
  as that topic's 2026 yearly item (`BY`);
- `plant|2` drops a limit: a stored commodity-DRAM ladder whose question asks DRAM prices (`LQ`).

  python3 reading_split.py <probe data folder> <key folder outside the repository>
  python3 reading_split.py disputes <reading folder> <key path>        # the third readers' BY and LQ packet

Writes <probe data folder>/reading/ (send-{1,2,3}/outcomes.jsonl, cases.json, readers/packet-<n>.json) and, in the key folder,
key.json and plants-expected.json. Refuses an existing reading folder or a key folder inside the repository.
"""
import copy
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(HERE), str(ROOT / 'clean-arch/step4-2026-11-10/stage_a'), str(ROOT / 'src')]
import build_reader_packets  # noqa: E402
import probe_split  # noqa: E402
from hivemind import universe  # noqa: E402

READ_YEARLY = ('T',)
READ_BOTH_ARMS = ('C1',)
ITEMS_A_PACKET = build_reader_packets.ITEMS_A_PACKET
SHUFFLE_SEED = 20261117
PLANTS = {   # plant: (source, stored case, the edit, the field a reader must mark yes); stored frozen ladders outside the 44
    'plant|1': ('fortnight', 'c1/clean-9', ('base year', '2027', '2026'), 'BY'),
    'plant|2': ('july', 'c3/clean-7', ('limit dropped', 'commodity DRAM', 'DRAM'), 'LQ'),
}


def group_of():
    return {f'{source}:{name}': group for group, entries in probe_split.TOPICS.items() for source, name in entries}


def rows_of(arm_folder):
    return [json.loads(line) for pass_folder in sorted(Path(arm_folder).glob('send-*'))
            for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines() if line]


def replace_year(value, old, new):
    """Every string in a ladder or view with one year written for another."""
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, list):
        return [replace_year(item, old, new) for item in value]
    if isinstance(value, dict):
        return {key: replace_year(item, old, new) for key, item in value.items()}
    return value


def plants():
    """(rows, cases, expected): the two planted items as outcome rows of pass 1, their cases, and the field each must be marked yes."""
    rows, cases, expected = [], [], {}
    topics = {f'{source}:{name}': case for _, source, name, case in probe_split.load_topics()}
    for plant, (source, name, edit, field) in PLANTS.items():
        stored = copy.deepcopy(probe_split.stored_first(source, name))
        if stored['status'] != 'ladder':
            raise SystemExit(f'{plant}: the stored send of {source}:{name} wrote no ladder')
        answer, view = stored['answer'], stored['view']
        split = None
        kind, before, after = edit
        if kind == 'base year':
            if view['year'] != before or before not in view['question']:
                raise SystemExit(f'{plant}: the stored ladder of {name} is not a {before} question')
            answer, view = replace_year(answer, before, after), replace_year(view, before, after)
            split = {'asked_year': after, 'asked_separately': before}
        else:
            if before not in view['question']:
                raise SystemExit(f'{plant}: the stored question of {name} does not name {before}')
            view = dict(view, question=view['question'].replace(before, after))
            answer = copy.deepcopy(answer)
            answer['ladder']['question'] = answer['ladder']['question'].replace(before, after)
        rows.append(dict(stored, case=plant, **{'pass': 1}, answer=answer, view=view, split=split))
        cases.append(dict(topics[f'{source}:{name}'], case=plant))
        expected[plant] = {'field': field, 'expected': 'yes'}
    return rows, cases, expected


def reading_rows(probe_folder):
    """(rows, cases): every item to read as an outcome row (with `split`), and a case under each row's name."""
    groups, topics = group_of(), {f'{source}:{name}': case for _, source, name, case in probe_split.load_topics()}
    rows, cases = [], {}
    for arm in probe_split.ARMS:
        for row in rows_of(Path(probe_folder) / arm):
            topic = row['case'].split('|', 1)[1]
            group = groups[topic]
            if arm == 'split' and group in READ_YEARLY and row['status'] == 'split':
                for year, child in row['children'].items():
                    if child['status'] != 'ladder':
                        continue
                    other = next(period for period in row['periods'] if period != year)
                    name = f"{row['case']}@{year}"
                    rows.append({'case': name, 'pass': row['pass'], 'status': 'ladder', 'reason': child['reason'], 'requests': child['requests'],
                                 'answer': child['answer'], 'passage': child['passage'], 'view': child['view'],
                                 'split': {'asked_year': year, 'asked_separately': other}})
                    cases[name] = dict(topics[topic], case=name)
            elif group in READ_BOTH_ARMS and row['status'] == 'ladder':
                rows.append(dict(row, split=None))
                cases[row['case']] = dict(topics[topic], case=row['case'])
    planted, planted_cases, _ = plants()
    rows += planted
    cases.update({case['case']: case for case in planted_cases})
    return rows, cases


def prep(probe_folder, key_folder):
    probe_folder, key_folder = Path(probe_folder), Path(key_folder)
    if key_folder.resolve().is_relative_to(ROOT.resolve()):
        raise SystemExit('the key folder must sit outside the repository')
    reading = probe_folder / 'reading'
    reading.mkdir(exist_ok=False)
    rows, cases = reading_rows(probe_folder)
    for pass_number in probe_split.PASSES:
        (reading / f'send-{pass_number}').mkdir()
        (reading / f'send-{pass_number}' / 'outcomes.jsonl').write_text(
            ''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows if row['pass'] == pass_number))
    (reading / 'cases.json').write_text(json.dumps(list(cases.values()), ensure_ascii=False, indent=1) + '\n')
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    order = sorted(rows, key=lambda row: (row['case'], row['pass']))
    random.Random(SHUFFLE_SEED).shuffle(order)
    (reading / 'readers').mkdir()
    key, packets = {}, []
    for number, row in enumerate(order, start=1):
        key[str(number)] = [row['case'], row['pass']]
        if (number - 1) % ITEMS_A_PACKET == 0:
            packets.append([])
        packets[-1].append({'item': number, **build_reader_packets.item_of(row, cases[row['case']], research_list), 'split': row['split']})
    for packet_number, packet in enumerate(packets, start=1):
        (reading / 'readers' / f'packet-{packet_number}.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / 'key.json').write_text(json.dumps(key, indent=1) + '\n')
    (key_folder / 'plants-expected.json').write_text(json.dumps(plants()[2], indent=1) + '\n')
    if sorted(map(tuple, key.values())) != sorted((row['case'], row['pass']) for row in rows) or len(set(map(tuple, key.values()))) != len(rows):
        raise SystemExit('check failed: not every item is in the key exactly once')
    yearly = sum(1 for row in rows if row['split'] and not row['case'].startswith('plant|'))
    print(f'{len(rows)} items in {len(packets)} packets: {yearly} yearly, {len(rows) - yearly - len(PLANTS)} C1, {len(PLANTS)} plants')
    return reading


SIDES_SEED = 20261118


def disputes(reading, key_path):
    """The third readers' BY and LQ packet (split-third-reader-brief.md): every point where the two first readers differ or either
    cannot tell, plants left out (a missed plant voids the reading instead). Each point carries the item as the first readers saw it,
    and the two marks as `a` and `b`, drawn per point from a fixed seed. Writes <reading>/third-reader/split-packet-1.json, refusing
    an existing one; returns the number of points."""
    import collect_readings as collector
    import score_split
    reading = Path(reading)
    _, item_of, outcomes, readers, _ = collector.read_rows(reading, key_path)
    packets = {item['item']: item for packet in sorted((reading / 'readers').glob('packet-*.json')) for item in json.loads(packet.read_text())}
    points = []
    for send, field in sorted(score_split.field_points(outcomes, readers, item_of), key=lambda point: (item_of[point[0]], point[1])):
        values = [readers[reader][send][field] for reader in collector.FAMILIES]
        random.Random(f'{SIDES_SEED}|{send[0]}|{send[1]}|{field}').shuffle(values)
        number = item_of[send]
        points.append({'id': f'{number}-{field}', 'item': packets[number], 'field': field, 'marks': {'a': values[0], 'b': values[1]}})
    folder = reading / 'third-reader'
    folder.mkdir(exist_ok=True)
    target = folder / 'split-packet-1.json'
    if target.exists():
        raise SystemExit(f'{target} exists: refused')
    target.write_text(json.dumps(points, indent=1, ensure_ascii=False) + '\n')
    return len(points)


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == 'disputes':
        print(disputes(sys.argv[2], sys.argv[3]), 'points')
    elif len(sys.argv) == 3:
        prep(sys.argv[1], sys.argv[2])
    else:
        sys.exit(__doc__)
