"""The table test: the tally ($0; TABLE-TEST-DESIGN.md version 2). Joins the comparers' marks to the label key and prints every part of
every answer set with how the mark was reached, then check 2's line for each table reader (the eight parts all record readers had
supported in D500 are supported; no part wrong), then coverage per layout (the Q2 mark; the key pairs of Q6 found; a misstatement), the
D500 record readers and the fresh record readers apart. It judges nothing itself.

A part on which the two comparers differ for any set is disputed: the fresh pair's file (`*-compare-settle.jsonl`), when it holds the
part, gives the marks of every set of that part; a set on which the fresh pair differ is open. Disputed parts without fresh marks are
listed so the settling packet can be built.

  python3 tally_table.py <key folder outside the repository>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')
PARTS = {'Q1': ['a', 'b'], 'Q2': ['a'], 'Q3': ['a', 'b'], 'Q4': ['a', 'b', 'c'], 'Q5': ['a', 'b'], 'Q6': ['a']}
EIGHT = [('Q1', 'a'), ('Q3', 'a'), ('Q3', 'b'), ('Q4', 'a'), ('Q4', 'b'), ('Q4', 'c'), ('Q5', 'a'), ('Q5', 'b')]
TABLE_SETS = ['codex-table-1', 'codex-table-2', 'claude-table-1', 'claude-table-2']
RECORD_SETS = ['codex-record-old', 'claude-record-old', 'codex-record-new', 'claude-record-new']


def objects(paths):
    out = []
    for path in paths:
        if not path.exists():
            continue
        text, decoder, position = path.read_text(), json.JSONDecoder(), 0
        while True:
            start = text.find('{"question"', position)
            if start == -1:
                break
            row, position = decoder.raw_decode(text, start)
            out.append(row)
    return out


def view(row, label):
    """One set's mark on one part, in one comparable shape."""
    if row is None:
        return None
    if row['question'] == 'Q6':
        return (tuple(sorted(row.get('pairs', {}).get(label) or [])), bool(row.get('misstatement', {}).get(label)))
    return row.get('marks', {}).get(label)


def main():
    key_folder = Path(sys.argv[1])
    first_key = json.loads((key_folder / 'record-3-key-compare-whole.json').read_text())
    settle_key_path = key_folder / 'record-3-key-compare-settle.json'
    settle_key = json.loads(settle_key_path.read_text()) if settle_key_path.exists() else {}
    first = {'codex': objects([HERE / 'codex-compare-half1.jsonl', HERE / 'codex-compare-half2.jsonl']), 'claude': objects([HERE / 'claude-compare.jsonl'])}
    fresh = {family: objects([HERE / f'{family}-compare-settle.jsonl']) for family in FAMILIES}
    first = {family: {(row['question'], str(row['part'])): row for row in rows} for family, rows in first.items()}
    fresh = {family: {(row['question'], str(row['part'])): row for row in rows} for family, rows in fresh.items()}
    for family in FAMILIES:
        missing = [f'{q}{p}' for q, parts in PARTS.items() for p in parts if (q, p) not in first[family]]
        if missing:
            raise SystemExit(f'{family} comparer left parts unmarked: {missing}: refused')
    label_of = lambda key, question, name: next(label for label, set_name in key[question].items() if set_name == name)
    table, disputed, unsettled = {}, [], []
    for question, parts in PARTS.items():
        for part in parts:
            pairs = {name: [view(first[family][(question, part)], label_of(first_key, question, name)) for family in FAMILIES] for name in TABLE_SETS + RECORD_SETS}
            if all(pair[0] == pair[1] for pair in pairs.values()):
                for name, pair in pairs.items():
                    table[(name, question, part)] = (pair[0], 'agreed')
                continue
            disputed.append(f'{question}{part}')
            if not all((question, part) in fresh[family] for family in FAMILIES):
                unsettled.append(f'{question}{part}')
                for name, pair in pairs.items():
                    table[(name, question, part)] = ((pair[0], pair[1]), 'agreed' if pair[0] == pair[1] else 'disputed, not yet re-marked')
                    if pair[0] == pair[1]:
                        table[(name, question, part)] = (pair[0], 'agreed (part disputed, not yet re-marked)')
                continue
            for name in pairs:
                again = [view(fresh[family][(question, part)], label_of(settle_key, question, name)) for family in FAMILIES]
                table[(name, question, part)] = (again[0], 'fresh pair') if again[0] == again[1] else ((again[0], again[1]), 'open')
    print(f'parts the first comparers marked differently for some set: {disputed or "none"}; without fresh marks yet: {unsettled or "none"}')

    def show(mark):
        if isinstance(mark, tuple) and len(mark) == 2 and isinstance(mark[1], bool):
            return f"pairs {list(mark[0]) or 'none'}{', MISSTATEMENT' if mark[1] else ''}"
        return str(mark)

    print('\nEVERY SET, every part')
    for name in TABLE_SETS + RECORD_SETS:
        cells = []
        for question, parts in PARTS.items():
            for part in parts:
                mark, state = table[(name, question, part)]
                cells.append(f"{question}{part} {show(mark) if state in ('agreed', 'fresh pair') or state.startswith('agreed') else 'OPEN ' + ' / '.join(show(m) for m in mark)}{'' if state == 'agreed' else ' [' + state + ']'}")
        print(f'  {name}: ' + '; '.join(cells))
    print('  notes of the first comparers on marks that are not "supported":')
    for name in TABLE_SETS + RECORD_SETS:
        for question, parts in PARTS.items():
            for part in parts:
                for family in FAMILIES:
                    row = first[family][(question, part)]
                    label = label_of(first_key, question, name)
                    note = (row.get('notes') or {}).get(label)
                    if note and view(row, label) != 'supported':
                        print(f'    {name} {question}{part} ({family}: {show(view(row, label))}): {note}')

    print("\nCHECK 2, per table reader: the eight parts supported, no part wrong")
    states = []
    for name in TABLE_SETS:
        not_supported, wrong, open_parts = [], [], []
        for question, parts in PARTS.items():
            for part in parts:
                mark, state = table[(name, question, part)]
                settled = state == 'agreed' or state == 'fresh pair' or state.startswith('agreed')
                if not settled:
                    open_parts.append(f'{question}{part}')
                elif mark == 'wrong' or (isinstance(mark, tuple) and mark[1] is True):
                    wrong.append(f'{question}{part}')
                elif (question, part) in EIGHT and mark != 'supported':
                    not_supported.append(f'{question}{part} {mark}')
        state = 'NOT met' if wrong or not_supported else ('undecided' if open_parts else 'met')
        states.append(state)
        print(f'  {name}: of the eight not supported {not_supported or "none"}; wrong {wrong or "none"}; open {open_parts or "none"} -> {state}')
    print('  check 2:', 'NOT met' if 'NOT met' in states else ('undecided' if 'undecided' in states else 'met'))

    print('\nCOVERAGE (reported, not scored): the Q2 mark and the key pairs of Q6, per set')
    for title, names in (('the table', TABLE_SETS), ('the plain record, D500 readers', RECORD_SETS[:2]), ('the plain record, fresh readers', RECORD_SETS[2:])):
        for name in names:
            q2, q2_state = table[(name, 'Q2', 'a')]
            q6, q6_state = table[(name, 'Q6', 'a')]
            print(f'  {title}: {name}: Q2 {show(q2) if not isinstance(q2, tuple) else " / ".join(map(str, q2))} [{q2_state}]; Q6 '
                  f'{show(q6) if isinstance(q6[1], bool) else " / ".join(show(m) for m in q6)} [{q6_state}]')


if __name__ == '__main__':
    main()
