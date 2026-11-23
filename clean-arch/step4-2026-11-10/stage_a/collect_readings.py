"""Stage A's readings, from the readers' answer files to what the accounting takes ($0; DESIGN.md §8, "The accounting").

Three steps, each a command:

  rows     read both readers' answer files, join each row to its case and pass through the key, check every row with the
           accounting's own rule, and print the rows that are missing or not valid (a reader is asked again for those).
  disputes write the third reader's packets: every send on which the two valid rows differ on a mark that applies, and every
           send on which a reader named a fault under `W`, with the thesis and the article. Which reader is "a" and which "b"
           is drawn per send from a fixed seed, so the third reader cannot rule by family.
  report   read the rulings and print the six lines (accounting.account). With two third readers, one of each family
           (`third-reader/rulings-codex-<n>.jsonl` and `rulings-claude-<n>.jsonl`), a point they rule alike takes that ruling
           and a point they rule differently is unresolved: the lines are printed twice, with every unresolved point counted
           for the answer and then against it, and the unresolved points are listed. A run read before that rule has one third
           reader (`rulings-<n>.jsonl`).

  python3 clean-arch/step4-2026-11-10/stage_a/collect_readings.py rows <run folder> <key path>
  python3 clean-arch/step4-2026-11-10/stage_a/collect_readings.py disputes <run folder> <key path>
  python3 clean-arch/step4-2026-11-10/stage_a/collect_readings.py report <run folder> <key path>

Reader 1 is the Codex family (`readers-answers/reader-codex-packet-<n>*.jsonl`), reader 2 the Claude family
(`reader-claude-packet-<n>*.jsonl`). A later file of the same packet (an asked-again answer, named `...-again-<k>.jsonl`)
replaces the rows it gives and no others.
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import accounting  # noqa: E402

FAMILIES = {'reader 1': 'codex', 'reader 2': 'claude'}
ITEMS_A_RULING_PACKET = 12
SIDES_SEED = 20261110


def outcomes_of(run_folder):
    return [json.loads(line) for pass_folder in sorted(Path(run_folder).glob('send-*'))
            for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines()]


def rows_of(run_folder, key, family):
    """{(case, pass): row} for one reader, with the lines that could not be read as a row."""
    rows, unreadable = {}, []
    answer_files = sorted((Path(run_folder) / 'readers-answers').glob(f'reader-{family}-packet-*.jsonl'),
                          key=lambda answer_file: ('-again-' in answer_file.name, answer_file.name))     # first answers, then asked-again ones
    for answer_file in answer_files:
        for line_number, line in enumerate(answer_file.read_text().splitlines(), start=1):
            line = line.strip()
            if not line or line.startswith('```'):
                continue
            try:
                row = json.loads(line)
                send = key[str(row['item'])]
            except (ValueError, KeyError, TypeError):
                unreadable.append((answer_file.name, line_number, line[:80]))
                continue
            rows[(send[0], send[1])] = row
    return rows, unreadable


def read_rows(run_folder, key_path):
    key = json.loads(Path(key_path).read_text())
    item_of = {(case, pass_number): int(item) for item, (case, pass_number) in key.items()}
    outcomes = {(outcome['case'], outcome['pass']): outcome for outcome in outcomes_of(run_folder)}
    readers, problems = {}, {}
    for reader, family in FAMILIES.items():
        rows, unreadable = rows_of(run_folder, key, family)
        readers[reader] = rows
        problems[reader] = {'unreadable lines': unreadable, 'rows': []}
        for send, outcome in sorted(outcomes.items(), key=lambda pair: item_of.get(pair[0], 0)):
            if accounting.kind_of(outcome) == 'refused twice':
                continue
            problem = accounting.row_problem(rows.get(send), outcome)
            if problem:
                problems[reader]['rows'].append((item_of[send], send, problem))
    return key, item_of, outcomes, readers, problems


def disputes_of(outcomes, readers):
    """[(send, differing marks, [(reader, fault named)])] over the sends both readers gave a valid row for."""
    found = []
    for send, outcome in outcomes.items():
        if accounting.kind_of(outcome) == 'refused twice':
            continue
        rows = [readers[reader].get(send) for reader in FAMILIES]
        if any(accounting.row_problem(row, outcome) for row in rows):
            continue
        marks = [mark for mark in accounting.marks_that_apply(accounting.kind_of(outcome)) if rows[0][mark] != rows[1][mark]]
        faults = [(reader, row['W'].strip()) for reader, row in zip(FAMILIES, rows) if row['W'].strip()]
        if marks or faults:
            found.append((send, marks, faults))
    return found


def sides_of(send):
    """Which reader the third reader sees as "a" for this send: drawn from a fixed seed and the send's name."""
    order = list(FAMILIES)
    random.Random(f'{SIDES_SEED}|{send[0]}|{send[1]}').shuffle(order)
    return {'a': order[0], 'b': order[1]}


def command_rows(run_folder, key_path):
    _, _, outcomes, readers, problems = read_rows(run_folder, key_path)
    to_read = sum(1 for outcome in outcomes.values() if accounting.kind_of(outcome) != 'refused twice')
    for reader, family in FAMILIES.items():
        bad = problems[reader]
        print(f"{reader} ({family}): {len(readers[reader])} rows for {to_read} answers to read; "
              f"{len(bad['rows'])} missing or not valid; {len(bad['unreadable lines'])} lines not read as a row")
        for item, send, problem in bad['rows']:
            print(f'   item {item} ({send[0]} pass {send[1]}): {problem}')
        for entry in bad['unreadable lines']:
            print('   unreadable:', entry)
    return all(not problems[reader]['rows'] for reader in FAMILIES)


def command_disputes(run_folder, key_path):
    _, item_of, outcomes, readers, problems = read_rows(run_folder, key_path)
    if any(problems[reader]['rows'] for reader in FAMILIES):
        raise SystemExit('a row is missing or not valid: ask the reader again first (the `rows` command lists them)')
    packets = {}
    for packet_file in sorted((Path(run_folder) / 'readers').glob('packet-*.json')):
        for item in json.loads(packet_file.read_text()):
            packets[item['item']] = item
    found = sorted(disputes_of(outcomes, readers), key=lambda entry: item_of[entry[0]])
    third_folder = Path(run_folder) / 'third-reader'
    third_folder.mkdir(exist_ok=False)
    to_rule, pairs = [], 0
    for send, marks, faults in found:
        sides = sides_of(send)
        reader_of_side = {reader: side for side, reader in sides.items()}
        item_number = item_of[send]
        entry = dict(packets[item_number])
        entry['to_rule'] = []
        for mark in marks:
            pairs += 1
            entry['to_rule'].append({'id': f'{item_number}-{mark}', 'mark': mark,
                                     **{f'reader_{side}': readers[sides[side]][send][mark] for side in ('a', 'b')},
                                     **{f'reader_{side}_reason': readers[sides[side]][send]['why'] for side in ('a', 'b')
                                        if readers[sides[side]][send][mark] == 'fails'}})
        for reader, fault in faults:
            entry['to_rule'].append({'id': f'{item_number}-W-{reader_of_side[reader]}', 'mark': 'W', 'fault_named': fault,
                                     'the_reader_s_reason': readers[reader][send]['why']})
        to_rule.append(entry)
    for packet_number in range(0, len(to_rule), ITEMS_A_RULING_PACKET):
        packet = to_rule[packet_number:packet_number + ITEMS_A_RULING_PACKET]
        (third_folder / f'ruling-packet-{packet_number // ITEMS_A_RULING_PACKET + 1}.json').write_text(
            json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    rulings_asked = sum(len(entry['to_rule']) for entry in to_rule)
    print(f'{len(found)} sends to rule on: {pairs} differing marks and {rulings_asked - pairs} faults named under W; '
          f'{-(-len(to_rule) // ITEMS_A_RULING_PACKET)} packets of at most {ITEMS_A_RULING_PACKET}')


def third_reader_families(run_folder):
    """The families that ruled: ['codex', 'claude'] for two third readers, [None] for the single one of an earlier run."""
    names = {answer_file.name.split('-')[1] for answer_file in (Path(run_folder) / 'third-reader').glob('rulings-*.jsonl')}
    return sorted(name for name in names if not name[0].isdigit()) or [None]


def read_rulings(run_folder, item_of, outcomes, readers, family=None):
    """One third reader's rulings as the accounting takes them, with the ids asked for that have no valid ruling."""
    send_of_item = {item: send for send, item in item_of.items()}
    given = {}
    pattern = f'rulings-{family}-*.jsonl' if family else 'rulings-[0-9]*.jsonl'
    for answer_file in sorted((Path(run_folder) / 'third-reader').glob(pattern)):
        for line in answer_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith('```'):
                continue
            try:
                ruling = json.loads(line)
                given[ruling['id']] = ruling
            except (ValueError, KeyError, TypeError):
                continue
    rulings, missing = {}, []
    for send, marks, faults in disputes_of(outcomes, readers):
        item_number = item_of[send]
        sides = sides_of(send)
        reader_of_side = {reader: side for side, reader in sides.items()}
        entry = {'marks': {}, 'W': {}, 'why': {}}
        for mark in marks:
            ruling = given.get(f'{item_number}-{mark}', {})
            if ruling.get('ruling') in accounting.VERDICTS:
                entry['marks'][mark] = ruling['ruling']
                entry['why'][mark] = ruling.get('why', '')
            else:
                missing.append(f'{item_number}-{mark}')
        for reader, _ in faults:
            ruling_id = f'{item_number}-W-{reader_of_side[reader]}'
            ruling = given.get(ruling_id, {})
            if ruling.get('upheld') in (True, False):
                entry['W'][reader] = ruling['upheld']
                entry['why'][f'W of {reader}'] = ruling.get('why', '')
            else:
                missing.append(ruling_id)
        rulings[send] = entry
    assert all(send in send_of_item.values() for send in rulings)
    return rulings, missing


def print_report(report, outcomes, readers, rulings, item_of):
    print('sends:', report['sends'], dict(report['outcomes']))
    print('reading:', report['reading'], '| dispute share:', report['dispute share'])
    for number in (1, 2, 3, 4, 5):
        print(f'line {number}:', report['lines'][number])
    for name, value in report['lines'][6].items():
        print(f'line 6, {name}:', value)
    print('shares:')
    for mark, share in report['shares'].items():
        print(f'   {mark}: {share}')
    print('refusals by the model, each with N as the two readers gave it and as ruled:')
    for send, outcome in sorted(outcomes.items()):
        if accounting.kind_of(outcome) == 'refusal':
            values = [readers[reader].get(send, {}).get('N', 'not read') for reader in FAMILIES]
            ruled = rulings.get(send, {}).get('marks', {}).get('N', values[0] if values[0] == values[1] else 'no ruling')
            print(f"   {send[0]} pass {send[1]} | N {values[0]} / {values[1]} -> {ruled} | {outcome['reason'][:230]}")
    print('refused twice by code, with the reasons of each attempt:')
    for send, outcome in sorted(outcomes.items()):
        if accounting.kind_of(outcome) == 'refused twice':
            print(f"   {send[0]} pass {send[1]} | " + ' || '.join('; '.join(reason[:90] for reason in request.get('reasons', []))
                                                                    for request in outcome['requests']))
    print(f"W named: {len(report['W named'])}; upheld: {len(report['upheld W'])}")
    for send, reader, fault in report['upheld W']:
        print(f'   upheld, item {item_of[send]} ({send[0]} pass {send[1]}), {reader}: {fault}')


def as_stored(report, rulings):
    return {'reading': report['reading'], 'dispute share': report['dispute share'], 'outcomes': dict(report['outcomes']),
            'lines': {str(number): line for number, line in report['lines'].items()}, 'shares': report['shares'],
            'upheld W': report['upheld W'], 'W named': report['W named'], 'invalid rows': report['invalid rows'],
            'missing rulings': report['missing rulings'],
            'rulings': {f'{send[0]}|{send[1]}': ruling for send, ruling in rulings.items()}}


def command_report(run_folder, key_path):
    _, item_of, outcomes, readers, _ = read_rows(run_folder, key_path)
    families = third_reader_families(run_folder)
    rows = (readers['reader 1'], readers['reader 2'])
    if families == [None]:
        rulings, missing = read_rulings(run_folder, item_of, outcomes, readers)
        if missing:
            print('rulings missing or not valid:', missing)
        report = accounting.account(list(outcomes.values()), *rows, rulings)
        print_report(report, outcomes, readers, rulings, item_of)
        stored = as_stored(report, rulings)
    else:
        if len(families) != 2:
            raise SystemExit(f'two third readers are expected, one of each family; found {families}')
        of_family = {}
        for family in families:
            of_family[family], missing = read_rulings(run_folder, item_of, outcomes, readers, family)
            if missing:
                print(f'rulings of the {family} third reader missing or not valid:', missing)
        stored, unresolved_points = {}, []
        for label, unresolved_as in (('every unresolved point counted for the answer', 'holds'), ('every unresolved point counted against it', 'fails')):
            rulings = {}
            for send in of_family[families[0]]:
                rulings[send], unresolved = accounting.rulings_of_two(of_family[families[0]][send], of_family[families[1]][send], unresolved_as)
                if unresolved_as == 'holds':
                    unresolved_points.extend((send, point) for point in unresolved)
            report = accounting.account(list(outcomes.values()), *rows, rulings)
            print(f'===== {label} =====')
            print_report(report, outcomes, readers, rulings, item_of)
            stored[label] = as_stored(report, rulings)
        print('===== each line under both countings: met only when met under both, missed when missed under both =====')
        both = [stored[label]['lines'] for label in stored]
        for number in ('1', '2', '3', '4', '5'):
            verdicts = {line if isinstance(line, str) else line[0] for line in (lines[number] for lines in both)}
            print(f"line {number}: {verdicts.pop() if len(verdicts) == 1 else 'depends on the unresolved points: ' + ' / '.join(sorted(verdicts))}")
        print(f'===== unresolved: the two third readers differ on {len(unresolved_points)} points =====')
        for send, point in unresolved_points:
            whys = ' | '.join(f"{family}: {of_family[family][send]['why'].get(point, '')[:150]}" for family in families)
            print(f'   item {item_of[send]} ({send[0]} pass {send[1]}) {point}: {whys}')
        stored['unresolved'] = [[f'{send[0]}|{send[1]}', point] for send, point in unresolved_points]
    (Path(run_folder) / 'stage-a-report.json').write_text(json.dumps(stored, indent=1, ensure_ascii=False, default=list) + '\n')


if __name__ == '__main__':
    command, run_folder_argument, key_path_argument = sys.argv[1], sys.argv[2], sys.argv[3]
    if command == 'rows':
        raise SystemExit(0 if command_rows(run_folder_argument, key_path_argument) else 1)
    {'disputes': command_disputes, 'report': command_report}[command](run_folder_argument, key_path_argument)
