"""The readers' packet of the second-look test ($0): the first answer of every sampled send and, as an item of its own, every
kept second answer that differs, shuffled; no item says which it is. The key from item number to send and version is written
outside the readers' folder.

  python3 clean-arch/step4-2026-11-10/probe-second-look-2026-11-10/build_packet.py <probe data folder> <key path>
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(STEP / 'ladder'), str(STEP / 'stage_a')]
import build_reader_packets  # noqa: E402
import ladder_step  # noqa: E402
import stage_a  # noqa: E402
from hivemind import extraction, universe  # noqa: E402

RUN = ROOT / 'poc' / 'data' / 'clean-ladder-stage-a-2026-11-10' / 'run-4'
ITEMS_A_PACKET = 21
SEED = 20261111


def outcome_of(answer_text, case, research_list):
    """An outcome as the runner writes it, from an answer's text that code accepts."""
    answer = ladder_step.parse_exactly(answer_text)
    if answer['ladder'] is None:
        return {'status': 'no ladder', 'reason': answer['no_ladder'], 'answer': None, 'passage': None, 'view': None}
    reasons, passage = ladder_step.check_answer(answer, thesis=case['thesis'], article=case['item'], company=stage_a.COMPANY, research_list=research_list,
                                                repair_quote=extraction.repair_quote, normalise=extraction.normalise, quote_tokens=extraction._quote_tokens,
                                                beyond_next_year=extraction.beyond_next_year, binding_horizon_days=extraction.BINDING_HORIZON_DAYS)
    if reasons:
        raise SystemExit(f'an answer in the packet is refused by code: {reasons[:1]}')
    view = ladder_step.write_view(answer['ladder'], passage, thesis=case['thesis'], article_day=case['item']['publication_date'], company=stage_a.COMPANY,
                                  research_list=research_list)
    return {'status': 'ladder', 'reason': None, 'answer': json.loads(ladder_step.as_json(answer)), 'passage': passage, 'view': view}


def main():
    folder, key_path = Path(sys.argv[1]), Path(sys.argv[2])
    if key_path.resolve().is_relative_to(folder.resolve()):
        raise SystemExit('the key must sit outside the readers\' folder')
    cases = {case['case']: case for case in json.loads((STEP / 'stage_a' / 'cases.json').read_text())}
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    entries = []
    for line in (folder / 'second-looks.jsonl').read_text().splitlines():
        row = json.loads(line)
        entries.append((row['case'], row['pass'], 'first', row['first_text']))
        if row['kept'] == 'second':
            entries.append((row['case'], row['pass'], 'second', row['second_text']))
    random.Random(SEED).shuffle(entries)
    (folder / 'readers').mkdir(exist_ok=False)
    key, packets = {}, []
    for number, (case, pass_number, version, text) in enumerate(entries, start=1):
        key[str(number)] = [case, pass_number, version]
        if (number - 1) % ITEMS_A_PACKET == 0:
            packets.append([])
        packets[-1].append({'item': number, **build_reader_packets.item_of(outcome_of(text, cases[case], research_list), cases[case], research_list)})
    for packet_number, packet in enumerate(packets, start=1):
        (folder / 'readers' / f'packet-{packet_number}.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    key_path.write_text(json.dumps(key, indent=1) + '\n')
    print(f'{len(entries)} items ({sum(1 for entry in entries if entry[2] == "first")} first answers, {sum(1 for entry in entries if entry[2] == "second")} second) '
          f'in {len(packets)} packets: {[len(packet) for packet in packets]}')


if __name__ == '__main__':
    main()
