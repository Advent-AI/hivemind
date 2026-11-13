"""A supplementary readers' packet ($0): the sends whose outcome in the final folder differs from the one the readers' packets
were built from. Their old items are retired and they are read again under new item numbers.

It happened once: the readers' packets were built from a first replay of the stored run, the check of that replay was then
narrowed (round log §69), and four sends had another outcome in the final replay.

  python3 clean-arch/step4-2026-11-10/stage_a/supplement_reader_packet.py <folder the packets were built from> <final folder> <old key> <new key>

Writes `<final folder>/readers/packet-<n>.json` beside copies of the earlier packets, and the new key: the old one without the
retired items, with the new ones. A reader's row for a retired item joins to nothing and is not counted.
"""
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_reader_packets  # noqa: E402
from hivemind import universe  # noqa: E402


def outcome_lines(folder):
    return {(row['case'], row['pass']): (line, row) for pass_folder in sorted(Path(folder).glob('send-*'))
            for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)]}


def main():
    read_folder, final_folder, old_key_path, new_key_path = (Path(argument) for argument in sys.argv[1:5])
    old_key = json.loads(old_key_path.read_text())
    read, final = outcome_lines(read_folder), outcome_lines(final_folder)
    changed = sorted(send for send in final if final[send][0] != read[send][0])
    cases = {case['case']: case for case in json.loads((HERE / 'cases.json').read_text())}
    research_list = universe.load(str(build_reader_packets.ROOT / 'poc' / 'universe.json'))
    readers_folder = final_folder / 'readers'
    readers_folder.mkdir(exist_ok=False)
    earlier = sorted((read_folder / 'readers').glob('packet-*.json'))
    for packet_file in earlier:
        shutil.copyfile(packet_file, readers_folder / packet_file.name)
    retired = {item for item, send in old_key.items() if tuple(send) in changed}
    new_key = {item: send for item, send in old_key.items() if item not in retired}
    next_item = max(int(item) for item in old_key) + 1
    packet = []
    for send in changed:
        outcome = final[send][1]
        if outcome['status'] not in ('ladder', 'no ladder'):
            continue                                   # refused twice: nothing to read
        new_key[str(next_item)] = [send[0], send[1]]
        packet.append({'item': next_item, **build_reader_packets.item_of(outcome, cases[send[0]], research_list)})
        next_item += 1
    (readers_folder / f'packet-{len(earlier) + 1}.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    new_key_path.write_text(json.dumps(new_key, indent=1) + '\n')
    print(f'{len(changed)} sends differ: {changed}')
    print(f'retired items {sorted(int(item) for item in retired)}; packet-{len(earlier) + 1}.json holds items {[entry["item"] for entry in packet]}')


if __name__ == '__main__':
    main()
