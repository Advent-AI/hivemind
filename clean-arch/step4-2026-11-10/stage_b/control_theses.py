"""Line 3 of Stage B, the control theses ($0; design §8; `STAGE_B_READING.md`; D430): the 16 theses of the three draws the frozen
matching rule paired with a ruler question (`unseeded-2026-11-10/mapping-runs.json`).

  packets <reading folder> <facts path>   writes controls/control-packet-<n>.json (four controls a packet) for two readers, and
                                          the code's facts outside the readers' folder (they hold reader B's answers and the rungs)
  count <reading folder>                  after the readers (and third readers where they differ): eligibility, agreement, line 3

A control is **eligible** when the readers confirm (a) its judged question asks what the ruler's asks, for the same period and
quantity measured the same way, and (b) its due day is the ruler's: for an event, the same deadline; for a figure, a day that
marks the publication of the same period's figure (D430); and code finds (c) reader B's frozen gold answers the question and (d)
the view has a judgement on or before 2026-07-14. The literal reading (the same question, and the two due days equal) is counted
beside. Its answer is the view's last judgement on or before that day, compared by outcome as the frozen scorer compares
(`score_judgement.py`): for a figure, the chosen rung's band overlaps reader B's range; for an event, Yes against yes, and "Ruled
out" or "Still open" against no. The readers mark each of reader B's decisive items as shown or not shown to the judge by
that day, searching every evidence entry the judge's requests for the view listed on or before it (the design: "by searching
the judge's requests for the figure"); the material is shown when every item is. Line 3 passes when at least 8 eligible controls have the material shown and all but one
of those agree with reader B. The Ohio guarantee question's date differs from the window's, so it is listed apart (design §8).

The count takes nothing on trust it can rebuild: the facts and packets are made again from the run folders and the frozen files
and must equal the packets on disk; every answer file must hold exactly its packet's controls, each row in the closed set below;
every disagreement needs a ruling from both third readers, and a ruling where the readers agree is refused.
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import stored_judgements  # noqa: E402

GOLD = ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold'
MAPPING = ROOT / 'clean-arch/unseeded-2026-11-10/mapping-runs.json'
WINDOW_END = '2026-07-14'
FAMILIES = ('codex', 'claude')
CONTROLS_A_PACKET = 4
YES_NO = ('yes', 'no')
ITEM_MARKS = ('shown', 'not_shown')
FEWEST_SHOWN = 8
EVIDENCE_STARTS = re.compile(r'^- (e\d+) \[')


def evidence_entries(request_text):
    """[(evidence id, the entry's text)] of one judge request: an entry is its "- e<id> [...]" line and the indented lines under it."""
    entries, current = [], None
    for line in request_text.splitlines():
        match = EVIDENCE_STARTS.match(line)
        if match:
            current = [match.group(1), [line]]
            entries.append(current)
        elif current is not None and line.startswith('    '):
            current[1].append(line)
        else:
            current = None
    return [(evidence_id, '\n'.join(lines)) for evidence_id, lines in entries]


def facts():
    """One record a control: the ruler question, reader B's answer and decisive items, the view and its last judgement."""
    questions = {q['id']: q for q in json.loads((GOLD / 'questions-v1.json').read_text())['questions']}
    gold = {entry['question_id']: entry for entry in json.loads((GOLD / 'gold-v1.json').read_text())['entries']}
    items = {item['id']: item for item in json.loads((GOLD / 'packet-v1.json').read_text())['items']}
    folders = stored_judgements.stage_b_folders()
    out = []
    for draw, theses in json.loads(MAPPING.read_text())['questions'].items():
        connection = sqlite3.connect(f"file:{folders[draw] / 'views.sqlite'}?mode=ro", uri=True)
        connection.row_factory = sqlite3.Row
        stored_judgements.refuse_split_store(connection, 'control_theses')
        archive = sqlite3.connect(f"file:{folders[draw] / 'archive.sqlite'}?mode=ro", uri=True)
        for thesis, question_id in theses.items():
            ladder = connection.execute('select view_id, status from clean_ladders where thesis_id = ?', (thesis,)).fetchone()
            view_id = ladder['view_id'] if ladder else None
            view = dict(connection.execute('select * from views where view_id = ?', (view_id,)).fetchone()) if view_id else None
            rungs = [dict(row) for row in connection.execute('select position, label, condition, lo, hi from rungs where view_id = ? order by position', (view_id,))] if view_id else []
            judged = connection.execute('select judgement_id, rung, call_id, publication_day from judgements where view_id = ? and publication_day <= ? '
                                        'order by judgement_id', (view_id, WINDOW_END)).fetchall() if view_id else []
            last = judged[-1] if judged else None
            shown, seen = [], set()
            for judgement in judged:
                request = json.loads(archive.execute('select request_json from model_calls where call_id = ?', (judgement['call_id'],)).fetchone()[0])
                for evidence_id, text in evidence_entries(stored_judgements.user_text_of(request)):
                    if (evidence_id, text) not in seen:
                        seen.add((evidence_id, text))
                        shown.append(text)
            entry, ruler = gold[question_id], questions[question_id]
            missing = [item for item in entry.get('decisive_items', []) if item not in items]
            if missing:
                raise SystemExit(f'{draw}/{thesis}: reader B\'s decisive items {missing} are not in the frozen packet')
            out.append({'control': f'{draw}/{thesis}', 'question_id': question_id, 'ohio': 'Ohio' in ruler['question'],
                        'ruler': {key: ruler[key] for key in ('question', 'unit', 'due_day', 'rungs')},
                        'gold_answer': entry.get('implied_outcome'), 'gold_open': not entry.get('implied_outcome') or bool(entry.get('no_view')),
                        'decisive_items': [{key: items[item].get(key) for key in ('id', 'day', 'title', 'passage', 'meaning')} for item in entry.get('decisive_items', [])],
                        'view': None if view is None else {key: view[key] for key in ('view_id', 'question', 'looks_at', 'due_day', 'year', 'kind')},
                        'rungs': rungs, 'last_judgement': None if last is None else {'rung': last['rung'], 'day': last['publication_day']},
                        'requests_searched': len(judged), 'evidence_shown': shown})
    return out


def agrees(record):
    """The frozen scorer's comparison by outcome; None when it cannot be made (no judgement, no gold, a figure with no bounds)."""
    if record['last_judgement'] is None or record['gold_open']:
        return None
    chosen = record['rungs'][record['last_judgement']['rung'] - 1]
    implied = record['gold_answer']
    if record['ruler']['unit'] == 'yes/no':
        return (chosen['label'].lower() == 'yes') == bool(implied['yes_no'])
    if chosen['lo'] is None and chosen['hi'] is None:
        return None
    return (chosen['lo'] is None or implied['high'] >= chosen['lo']) and (chosen['hi'] is None or implied['low'] < chosen['hi'])


def packet_texts(records):
    """The readers' packets: what the readers see (no rung chosen, no reader B answer, the evidence entries the judge was shown for
    the view through the window's end), four controls a packet."""
    items = [{'control': number, 'ruler_question': record['ruler'], 'judged_question': record['view'], 'judged_rungs': record['rungs'],
              'reader_b_decisive_items': record['decisive_items'], 'evidence_shown_to_the_judge_through_2026_07_14': record['evidence_shown']}
             for number, record in enumerate(records, start=1)]
    return [json.dumps(items[start:start + CONTROLS_A_PACKET], indent=1, ensure_ascii=False) + '\n' for start in range(0, len(items), CONTROLS_A_PACKET)]


def packets(folder, facts_path):
    folder, facts_path = Path(folder), Path(facts_path)
    if facts_path.resolve().is_relative_to(folder.resolve()):
        raise SystemExit('the facts hold reader B\'s answers: they must sit outside the readers\' folder')
    records = facts()
    (folder / 'controls').mkdir(parents=True, exist_ok=False)
    for number, text in enumerate(packet_texts(records), start=1):
        (folder / 'controls' / f'control-packet-{number}.json').write_text(text)
    facts_path.parent.mkdir(parents=True, exist_ok=True)
    facts_path.write_text(json.dumps([{key: value for key, value in record.items() if key != 'evidence_shown'} for record in records], indent=1, ensure_ascii=False) + '\n')
    print(f'{len(records)} controls; with a ladder {sum(1 for r in records if r["view"])}; judged by {WINDOW_END} {sum(1 for r in records if r["last_judgement"])}; '
          f'literal due day equal {sum(1 for r in records if r["view"] and r["view"]["due_day"] == r["ruler"]["due_day"])}; Ohio {sum(1 for r in records if r["ohio"])}')


def row_problem(row, item_ids):
    if set(row) != {'control', 'same_question', 'same_due', 'items', 'why'}:
        return f'fields {sorted(row)}'
    if row['same_question'] not in YES_NO or row['same_due'] not in YES_NO:
        return 'same_question and same_due are "yes" or "no"'
    if not isinstance(row['items'], dict) or set(row['items']) != set(item_ids) or any(mark not in ITEM_MARKS for mark in row['items'].values()):
        return f'items must mark exactly {sorted(item_ids)}, each "shown" or "not_shown"'
    if not isinstance(row['why'], str) or not row['why'].strip():
        return 'no why'
    return None


def jsonl(path):
    rows, problems = [], []
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except ValueError:
                problems.append(f'{path.name} line {line_number}: not JSON')
    return rows, problems


def read(folder, records):
    """(rows {family: {control: row}}, rulings {family: {(control, field): ruling}}, problems)."""
    problems = []
    texts = packet_texts(records)
    on_disk = {path.name: path.read_text() for path in (folder / 'controls').glob('*')}
    expected = {f'control-packet-{number}.json': text for number, text in enumerate(texts, start=1)}
    for name in sorted(set(on_disk) | set(expected)):
        if on_disk.get(name) != expected.get(name):
            problems.append(f'controls/{name} is not the packet the builder makes' if name in expected else f'controls/{name} is not a packet of this reading')
    in_packet = {f'control-packet-{number}': [item['control'] for item in json.loads(text)] for number, text in enumerate(texts, start=1)}
    item_ids = {number: [item['id'] for item in record['decisive_items']] for number, record in enumerate(records, start=1)}
    rows = {family: {} for family in FAMILIES}
    for family in FAMILIES:
        for packet, controls in in_packet.items():
            path = folder / 'controls-answers' / f'reader-{family}-{packet}.jsonl'
            if not path.exists():
                problems.append(f'{family}: no answers for {packet}')
                continue
            found, bad = jsonl(path)
            problems += [f'{family}: {problem}' for problem in bad]
            numbers = [row.get('control') if isinstance(row, dict) else None for row in found]
            if sorted(numbers, key=str) != sorted(controls, key=str):
                problems.append(f'{family}: {path.name} does not hold each control of {packet} exactly once')
                continue
            for row in found:
                problem = row_problem(row, item_ids[row['control']])
                if problem:
                    problems.append(f'{family}: control {row["control"]}: {problem}')
                rows[family][row['control']] = row
        extra = [path.name for path in (folder / 'controls-answers').glob(f'reader-{family}-*.jsonl')
                 if path.stem.removeprefix(f'reader-{family}-') not in in_packet] if (folder / 'controls-answers').exists() else []
        problems += [f'{family}: {name} is not a packet of this reading' for name in extra]
    if problems:
        return rows, {}, problems
    disagreements = set()
    for number in range(1, len(records) + 1):
        pair = [rows[family][number] for family in FAMILIES]
        for field in ('same_question', 'same_due'):
            if pair[0][field] != pair[1][field]:
                disagreements.add((number, field))
        for item in item_ids[number]:
            if pair[0]['items'][item] != pair[1]['items'][item]:
                disagreements.add((number, f'item {item}'))
    rulings = {family: {} for family in FAMILIES}
    for family in FAMILIES:
        path = folder / 'controls-third' / f'rulings-{family}.jsonl'
        found, bad = jsonl(path) if path.exists() else ([], [])
        problems += [f'{family} third reader: {problem}' for problem in bad]
        for row in found:
            name = (row.get('control'), row.get('field'))
            allowed = ITEM_MARKS if str(row.get('field', '')).startswith('item ') else YES_NO
            if name not in disagreements:
                problems.append(f'{family} third reader: a ruling on {name}, where the readers do not differ')
            elif name in rulings[family]:
                problems.append(f'{family} third reader: {name} ruled twice')
            elif set(row) != {'control', 'field', 'ruling', 'why'} or row['ruling'] not in allowed or not (isinstance(row['why'], str) and row['why'].strip()):
                problems.append(f'{family} third reader: {name}: a ruling is {{control, field, ruling in {allowed}, why}}')
            rulings[family][name] = row.get('ruling')
        problems += [f'{family} third reader: no ruling on {name}' for name in sorted(disagreements, key=str) if name not in rulings[family]]
    return rows, rulings, problems


def count(folder):
    folder = Path(folder)
    records = facts()
    rows, rulings, problems = read(folder, records)
    if problems:
        print(f'INCOMPLETE: {len(problems)} problems; no result is printed')
        for problem in problems[:40]:
            print('  ', problem)
        raise SystemExit(2)

    def decided(number, field, value_of):
        values = [value_of(rows[family][number]) for family in FAMILIES]
        if values[0] == values[1]:
            return values[0]
        ruled = [rulings[family][(number, field)] for family in FAMILIES]
        return ruled[0] if ruled[0] == ruled[1] else 'unresolved'

    tallies = {reading: {'eligible': 0, 'shown': 0, 'agree': 0, 'on_window_end': 0} for reading in ('D430', 'literal')}
    apart = []
    for number, record in enumerate(records, start=1):
        same_question = decided(number, 'same_question', lambda row: row['same_question'])
        same_due = decided(number, 'same_due', lambda row: row['same_due'])
        marks = [decided(number, f'item {item["id"]}', lambda row, item=item: row['items'][item['id']]) for item in record['decisive_items']]
        material = 'not shown' if 'not_shown' in marks else ('unresolved' if 'unresolved' in marks else 'shown')   # every item must be shown
        judged = not record['gold_open'] and record['last_judgement'] is not None
        literal_due = record['view'] is not None and record['view']['due_day'] == record['ruler']['due_day']
        eligibility = {'D430': same_question == 'yes' and same_due == 'yes' and judged, 'literal': same_question == 'yes' and literal_due and judged}
        agreement = agrees(record) if judged else None
        line = (f"{record['control']:12s} {record['question_id']} same question {same_question}, same due {same_due} (literal {literal_due}), "
                f"material {material} (items shown {marks.count('shown')}, not shown {marks.count('not_shown')}, unresolved {marks.count('unresolved')}, of {len(marks)}); eligible {eligibility['D430']} (literal {eligibility['literal']}); "
                f"last judgement {record['last_judgement']}; agrees with reader B {agreement}")
        if record['ohio']:
            print('[Ohio, listed apart] ' + line)
            continue
        print(line)
        for reading, eligible in eligibility.items():
            if eligible:
                tallies[reading]['eligible'] += 1
                if material == 'shown':
                    tallies[reading]['shown'] += 1
                    tallies[reading]['agree'] += agreement is True
                    tallies[reading]['on_window_end'] += record['last_judgement']['day'] == WINDOW_END
                elif reading == 'D430' and agreement is not True:
                    apart.append(f"   {record['control']} {record['question_id']}: disagrees with reader B, " + (
                        'material not shown to the judge by that day (where it was lost is traced apart: linked and not shown, or never linked)' if material == 'not shown'
                        else 'material unresolved (the third readers split): not established either way'))
    print('== eligible controls that disagree with reader B and whose material is not shown or unresolved (reported apart, not in line 3)')
    print('\n'.join(apart) if apart else '   none')
    for reading, tally in tallies.items():
        shown, agree = tally['shown'], tally['agree']
        verdict = 'met' if shown >= FEWEST_SHOWN and agree >= shown - 1 else (
            f'UNEXERCISED: fewer than {FEWEST_SHOWN} eligible with the material shown; Stage B cannot pass' if shown < FEWEST_SHOWN else 'MISSED')
        print(f"== line 3, {reading} reading{' (the line)' if reading == 'D430' else ' (beside)'}: eligible {tally['eligible']}; with the material shown {shown}, "
              f"of them agreeing {agree} (compared answers made on {WINDOW_END}: {tally['on_window_end']}, earlier: {shown - tally['on_window_end']}): {verdict}")


if __name__ == '__main__':
    if sys.argv[1] == 'packets':
        packets(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'count':
        count(sys.argv[2])
    else:
        raise SystemExit('packets <reading folder> <facts path> | count <reading folder>')
