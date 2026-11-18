"""The company record test: the tally ($0; RECORD-TEST-DESIGN.md). Joins the two reader families' fidelity marks to the key and the two
comparers' marks to the label key, and prints every count the frozen lines read. It judges nothing itself. A fidelity row is wrong when
any field is marked wrong and incomplete when none is wrong and one is missing; marks the two families give differently are listed for
the third reading (pass `--settled <file>` with one JSON line per settled entry: {"entry": n, "wrong": true|false, "incomplete": true|false}).

  python3 tally_record.py <key folder outside the repository> [--settled settled.jsonl]
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')
FIELDS = ('measure', 'basis', 'period', 'kind', 'value', 'original_party', 'date')
REQUIRED = {'Q1': ('a', 'b', 'c'), 'Q2': ('a',), 'Q3': ('a', 'b'), 'Q4': ('a', 'b', 'c'), 'Q5': ('a', 'b'), 'Q6': ('a',)}


def lines(name):
    return [json.loads(line) for line in (HERE / name).read_text().splitlines() if line.strip().startswith('{')]


def state(row):
    marks = [row.get(field) for field in FIELDS]
    return 'wrong' if 'wrong' in marks else ('incomplete' if 'missing' in marks else 'right')


def fidelity(key_folder, settled):
    key = {row['entry']: row for row in json.loads((key_folder / 'record-key-fidelity.json').read_text())}
    marks = {family: {row['entry']: row for row in lines(f'{family}-fidelity.jsonl')} for family in FAMILIES}
    for family in FAMILIES:
        if sorted(marks[family]) != sorted(key):
            raise SystemExit(f'{family} marked {len(marks[family])} of {len(key)} entries: refused')
    print('FIDELITY (full-week record; 20 rows of each stratum; not a rate for the whole record)')
    for stratum, allowed in (('R', 1), ('O', 2)):
        entries = [entry for entry, row in key.items() if row['stratum'] == stratum]
        per_family = {family: {'right': 0, 'wrong': 0, 'incomplete': 0} for family in FAMILIES}
        both_wrong, differ, final_wrong, final_incomplete = [], [], 0, 0
        for entry in entries:
            states = {family: state(marks[family][entry]) for family in FAMILIES}
            for family in FAMILIES:
                per_family[family][states[family]] += 1
            if states['codex'] == states['claude']:
                final_wrong += states['codex'] == 'wrong'
                final_incomplete += states['codex'] == 'incomplete'
                if states['codex'] == 'wrong':
                    both_wrong.append(entry)
            else:
                differ.append(entry)
                if entry in settled:
                    final_wrong += bool(settled[entry].get('wrong'))
                    final_incomplete += bool(settled[entry].get('incomplete')) and not settled[entry].get('wrong')
        unsettled = [entry for entry in differ if entry not in settled]
        verdict = 'UNDECIDED (marks to settle)' if unsettled else ('met' if final_wrong <= allowed else 'NOT met')
        print(f'  stratum {stratum} ({len(entries)} rows): ' + '; '.join(f'{family} {per_family[family]}' for family in FAMILIES))
        print(f'    wrong by both {both_wrong}; families differ on {differ}; after settling: wrong {final_wrong}, incomplete {final_incomplete} '
              f'(line: at most {allowed} wrong): {verdict}')
        for entry in sorted(set(both_wrong) | set(differ)):
            for family in FAMILIES:
                row = marks[family][entry]
                bad = {field: row.get(field) for field in FIELDS if row.get(field) in ('wrong', 'missing')}
                print(f"      entry {entry} (row {key[entry]['row']}) {family}: {bad or 'all right'} | {row.get('note', '')}")
        not_own = {family: [entry for entry in entries if marks[family][entry].get('own') is False] for family in FAMILIES}
        left_out = {family: [entry for entry in entries if marks[family][entry].get('revenue_or_margin') is True] for family in FAMILIES}
        print(f'    not the company\'s own figure: {not_own}')
        if stratum == 'O':
            print(f'    revenue or margin rows the view\'s filter leaves out: {left_out}')
    field_counts = {family: {field: {} for field in FIELDS} for family in FAMILIES}
    for family in FAMILIES:
        for row in marks[family].values():
            for field in FIELDS:
                field_counts[family][field][row.get(field)] = field_counts[family][field].get(row.get(field), 0) + 1
    for family in FAMILIES:
        print(f'  marks by field, {family}: ' + '; '.join(f'{field} {field_counts[family][field]}' for field in FIELDS))


def usability(key_folder):
    labels = json.loads((key_folder / 'record-key-compare.json').read_text())
    marks = {family: {(row['question'], str(row['part'])): row for row in lines(f'{family}-compare.jsonl')} for family in FAMILIES}
    print('\nUSABILITY (six questions; the record reader against the reference written from the same 40 articles)')
    verdicts = {}
    for question, parts in REQUIRED.items():
        record_label = 'P' if labels[question]['P'] == 'record' else 'Q'
        reference_label = 'Q' if record_label == 'P' else 'P'
        per_family = {}
        for family in FAMILIES:
            rows = [marks[family].get((question, part)) for part in parts]
            if any(row is None for row in rows):
                raise SystemExit(f'{family} left out a required part of {question}: refused')
            exercised = rows[0][reference_label] in ('supported', 'incomplete')
            answered = [row for row in rows if row[reference_label] in ('supported', 'incomplete')]
            same = all(row['agree'] and row[record_label] == 'supported' for row in answered)
            wrong = any(row[record_label] == 'wrong' for row in rows)
            per_family[family] = 'unexercised' if not exercised else ('wrong' if wrong else ('same' if same else 'not the same'))
            for part, row in zip(parts, rows):
                print(f"  {question}{part} {family}: record {row[record_label]}, reference {row[reference_label]}, agree {row['agree']}, "
                      f"articles hold {row.get('articles_hold')} | {row.get('note', '')}")
        verdicts[question] = per_family
        print(f'    -> {question}: {per_family}')
    for family in FAMILIES:
        exercised = [q for q, v in verdicts.items() if v[family] != 'unexercised']
        not_same = [q for q in exercised if verdicts[q][family] != 'same']
        wrong = [q for q in exercised if verdicts[q][family] == 'wrong']
        line = len(exercised) >= 5 and len(not_same) <= 1 and not wrong
        print(f'  {family}: exercised {len(exercised)}; not the same {not_same}; wrong {wrong}: {"met" if line else "NOT met"}')
    print('  questions on which the comparers differ:', [q for q, v in verdicts.items() if v['codex'] != v['claude']])


def main():
    key_folder = Path(sys.argv[1])
    settled = {}
    if '--settled' in sys.argv:
        settled = {row['entry']: row for row in lines(sys.argv[sys.argv.index('--settled') + 1])}
    fidelity(key_folder, settled)
    if (HERE / 'codex-compare.jsonl').exists() and (HERE / 'claude-compare.jsonl').exists():
        usability(key_folder)


if __name__ == '__main__':
    main()
