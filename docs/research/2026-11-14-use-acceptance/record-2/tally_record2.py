"""The record test on unread articles: the tally ($0; RECORD-TEST-2-DESIGN.md). Joins the two comparers' marks to the label key and prints,
for each of the six answer sets (two from the articles, four from the records), every part's mark by each comparer, then per record set
the questions exercised, the same, with an omission, wrong or open, and the line's verdict per record at the grain the design states
(both of a record's readers must meet it). It judges nothing itself. Marks the comparers give differently are open unless a settling
file gives the same mark from both fresh readers.

  python3 tally_record2.py <key folder outside the repository>
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')
PARTS = {'Q1': ['a', 'b'], 'Q2': ['a'], 'Q3': ['a', 'b'], 'Q4': ['a', 'b', 'c'], 'Q5': ['a', 'b'], 'Q6': ['a']}
RECORD_SETS = ['codex-record-A', 'claude-record-A', 'codex-record-B', 'claude-record-B']
REFERENCE_SETS = ['codex-reference', 'claude-reference']


def objects(path):
    if not path.exists():
        return []
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find('{"question"', position)
        if start == -1:
            return out
        row, position = decoder.raw_decode(text, start)
        out.append(row)


def main():
    key_folder = Path(sys.argv[1])
    labels = json.loads((key_folder / 'record-2-key-compare.json').read_text())
    arms = json.loads((key_folder / 'record-2-key-views.json').read_text())
    record_of = {arms[arm]['label']: arm for arm in ('c8', 'c22')}
    marks = {family: {(row['question'], str(row['part'])): row for row in objects(HERE / f'{family}-compare.jsonl')} for family in FAMILIES}
    settle = {family: {(row['question'], str(row['part'])): row for row in objects(HERE / f'{family}-compare-settle.jsonl')} for family in FAMILIES}
    for family in FAMILIES:
        missing = [f'{q}{p}' for q, parts in PARTS.items() for p in parts if (q, p) not in marks[family]]
        if missing:
            raise SystemExit(f'{family} comparer left parts unmarked: {missing}: refused')

    def mark_of(name, question, part):
        """(mark, state): agreed by the two comparers; else settled by the fresh pair; else open with both marks."""
        label = next(l for l, n in labels[question].items() if n == name)
        pair = [marks[family][(question, part)]['marks'].get(label) for family in FAMILIES]
        if pair[0] == pair[1]:
            return pair[0], 'agreed'
        again = [(settle[family].get((question, part)) or {}).get('marks', {}).get(label) for family in FAMILIES]
        if again[0] is not None and again[0] == again[1]:
            return again[0], 'settled'
        return f'open ({pair[0]} / {pair[1]})', 'open'

    print('WHAT THE ARTICLES HOLD, part by part (each comparer)')
    exercised = {}
    for question, parts in PARTS.items():
        for part in parts:
            holds = [marks[family][(question, part)].get('articles_hold') for family in FAMILIES]
            items = [len(marks[family][(question, part)].get('items') or []) for family in FAMILIES]
            exercised[(question, part)] = 'yes' if all(holds) else ('no' if not any(holds) else 'open')
            print(f'  {question}{part}: articles hold it: codex {holds[0]}, claude {holds[1]}; items listed: codex {items[0]}, claude {items[1]} -> {exercised[(question, part)]}')

    print('\nEVERY SET, every part (the mark, and how it was reached)')
    table = {}
    for name in REFERENCE_SETS + RECORD_SETS:
        cells = []
        for question, parts in PARTS.items():
            for part in parts:
                mark, state = mark_of(name, question, part)
                table[(name, question, part)] = (mark, state)
                cells.append(f'{question}{part} {mark}')
        shown = name if name in REFERENCE_SETS else f"{name} (the record of {record_of[name[-1]]})"
        print(f'  {shown}: ' + '; '.join(cells))
    print('  notes on marks that are not "supported":')
    for name in RECORD_SETS:
        for question, parts in PARTS.items():
            label = next(l for l, n in labels[question].items() if n == name)
            for part in parts:
                for family in FAMILIES:
                    row = marks[family][(question, part)]
                    if row['marks'].get(label) not in ('supported', None) and (row.get('notes') or {}).get(label):
                        print(f"    {name} {question}{part} ({family}: {row['marks'].get(label)}): {row['notes'][label]}")

    print('\nTHE LINE, per record (both of its readers)')
    verdict = {}
    for label in ('A', 'B'):
        states = []
        for reader in FAMILIES:
            name = f'{reader}-record-{label}'
            questions_exercised = [q for q in PARTS if exercised[(q, 'a')] == 'yes']
            same, omission, wrong, open_questions = [], [], [], []
            for question in questions_exercised:
                parts = [p for p in PARTS[question] if exercised[(question, p)] == 'yes']
                found = [table[(name, question, p)] for p in parts]
                if any(state == 'open' for _, state in found):
                    open_questions.append(question)
                elif any(mark == 'wrong' for mark, _ in found):
                    wrong.append(question)
                elif all(mark == 'supported' for mark, _ in found):
                    same.append(question)
                else:
                    omission.append(question)
            open_parts = [q for q in PARTS if exercised[(q, 'a')] == 'open']
            if len(questions_exercised) < 5:
                state = 'inconclusive'
            elif wrong or len(omission) > 1:
                state = 'NOT met'                      # a wrong statement, or more than one question not the same, whatever the open marks become
            elif open_questions or open_parts:
                state = 'undecided'                    # an open mark could still be a wrong statement or a second omission
            else:
                state = 'met'
            states.append(state)
            print(f"  record {label} ({record_of[label]}), {reader} reader: exercised {len(questions_exercised)} {questions_exercised}; same {same}; "
                  f"omission {omission}; wrong {wrong}; open {open_questions}; exercise disputed {open_parts} -> {state}")
        verdict[label] = ('inconclusive' if 'inconclusive' in states else 'NOT met' if 'NOT met' in states else 'undecided' if 'undecided' in states else 'met')
    for label in ('A', 'B'):
        print(f'  record {label} ({record_of[label]}): {verdict[label]}')


if __name__ == '__main__':
    main()
