"""The readers' packets of Stage A ($0): every written ladder and every refusal by the model, as the form
`ladder/stage-a-reader-brief.md` describes an item, in a shuffled order, a few packets of a size one reader can finish.

An answer refused twice by code has nothing to read and gets no item. The key from item number to case and pass is written to a
path outside the readers' folder: readers are told to open only the brief and their packet.

  python3 clean-arch/step4-2026-11-10/stage_a/build_reader_packets.py <run folder> <key path>
  python3 clean-arch/step4-2026-11-10/stage_a/build_reader_packets.py <key path> --run <run folder>=<cases file> [--run ...] --readers <folder>

The second form (the full run, D452 gate 1) reads several runs, each with its own cases file (case names are draw-qualified, so they are
unique across runs), and writes the packets to the named readers' folder; it checks that every written ladder and every refusal of every
pass is an item exactly once and that the key holds exactly those (case, pass) pairs.
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import universe  # noqa: E402

COMPANY = 'NVDA'
ITEMS_A_PACKET = 22
SHUFFLE_SEED = 20261110


def item_of(outcome, case, research_list):
    """One outcome as the form describes an item (without its number)."""
    thesis, article = case['thesis'], case['item']
    item = {'thesis': {field: thesis[field] for field in ('description', 'outcome', 'period', 'opens_as', 'settled_by')},
            'article': {field: article[field] for field in ('publication_date', 'title', 'text')},
            'fiscal_year_note': research_list.fiscal_note(COMPANY, article['publication_date'], english=True)}
    if outcome['status'] == 'no ladder':
        item['ladder_as_the_judge_is_shown_it'] = {'no_ladder': outcome['reason']}
        item['other_fields'] = {'not_judged': None, 'reference': None, 'favourable_end': None, 'favourable_why': None, 'ruled_out_by': None, 'due_day_basis': None}
        return item
    ladder, view = outcome['answer']['ladder'], outcome['view']
    item['ladder_as_the_judge_is_shown_it'] = {
        'object': view['object_id'], 'kind': view['kind'], 'focus': view['looks_at'], 'question': view['question'], 'year': view['year'],
        'due_day': view['due_day'], 'rungs': [{'label': rung['label'], 'condition': rung['condition']} for rung in view['rungs']]}
    reference = ladder['reference']
    figure = ladder.get('figure')
    ruled_out = ladder['event']['ruled_out'] if ladder.get('event') else None
    item['other_fields'] = {
        'not_judged': ladder['not_judged'],
        'reference': None if reference is None else {'words': outcome['passage'], 'kind': reference.get('kind', 'expected'), 'value': reference['value'],
                                                    'value_to': reference.get('value_to')},
        'favourable_end': figure['favourable_end'] if figure else None, 'favourable_why': figure['favourable_why'] if figure else None,
        'ruled_out_by': ruled_out['by_whom'] if isinstance(ruled_out, dict) else None,
        'due_day_basis': ladder['due_day_basis']}
    return item


def arguments():
    """(runs as [(run folder, cases file)], key path, readers folder): the stored form or the full run's."""
    if '--run' not in sys.argv:
        run_folder, key_path = Path(sys.argv[1]), Path(sys.argv[2])
        return [(run_folder, HERE / 'cases.json')], key_path, run_folder / 'readers'
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('key')
    parser.add_argument('--run', action='append', required=True)
    parser.add_argument('--readers', required=True)
    parsed = parser.parse_args()
    runs = [(Path(pair.split('=', 1)[0]), Path(pair.split('=', 1)[1])) for pair in parsed.run]
    return runs, Path(parsed.key), Path(parsed.readers)


def main():
    runs, key_path, readers_folder = arguments()
    if key_path.resolve().is_relative_to(readers_folder.resolve()):
        raise SystemExit('the key must not sit in the readers\' folder')
    cases, outcomes = {}, []
    for run_folder, cases_path in runs:
        run_cases = {case['case']: case for case in json.loads(cases_path.read_text())}
        if set(run_cases) & set(cases):
            raise SystemExit(f'{cases_path}: a case name already given by another run: refused')
        cases.update(run_cases)
        outcomes += [json.loads(line) for pass_folder in sorted(run_folder.glob('send-*'))
                     for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines()]
    if any(outcome['case'] not in cases for outcome in outcomes):
        raise SystemExit('an outcome names a case no cases file holds: refused')
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    to_read = [outcome for outcome in outcomes if outcome['status'] in ('ladder', 'no ladder')]
    order = sorted(to_read, key=lambda outcome: (outcome['case'], outcome['pass']))
    random.Random(SHUFFLE_SEED).shuffle(order)
    readers_folder.mkdir(exist_ok=False)
    key, packets = {}, []
    for number, outcome in enumerate(order, start=1):
        key[str(number)] = [outcome['case'], outcome['pass']]
        if (number - 1) % ITEMS_A_PACKET == 0:
            packets.append([])
        packets[-1].append({'item': number, **item_of(outcome, cases[outcome['case']], research_list)})
    for packet_number, packet in enumerate(packets, start=1):
        (readers_folder / f'packet-{packet_number}.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_text(json.dumps(key, indent=1) + '\n')
    if sorted(map(tuple, key.values())) != sorted((outcome['case'], outcome['pass']) for outcome in to_read) or \
            len(set(map(tuple, key.values()))) != len(to_read) or sum(len(packet) for packet in packets) != len(to_read):
        raise SystemExit('check failed: not every written ladder and refusal is an item exactly once')
    refused_twice = len(outcomes) - len(to_read)
    print(f'{len(outcomes)} outcomes; {len(to_read)} to read in {len(packets)} packets of at most {ITEMS_A_PACKET}; {refused_twice} refused twice, not read')
    print('items a packet:', [len(packet) for packet in packets])


if __name__ == '__main__':
    main()
