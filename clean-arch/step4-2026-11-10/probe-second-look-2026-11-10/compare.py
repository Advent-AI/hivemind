"""The second-look test's count, from the one blind reading round ($0). Written before any reader's row exists.

For every sampled send the round holds marks on its first answer and, where a second answer differs and was kept, on that
second answer. A fault is "agreed" in this round when both first readers fail the same mark on the same item, or, where they
differ and third readers ruled, when both third readers rule it failed. An unchanged or refused second look leaves the first
answer, so its marks are the first answer's.

  python3 clean-arch/step4-2026-11-10/probe-second-look-2026-11-10/compare.py <probe data folder> <items key> <groups key>
"""
import collections
import json
import sys
from pathlib import Path

MARKS = ['Q', 'O', 'R', 'D', 'X', 'F', 'Y', 'L', 'XR', 'N']


def rows_of(folder, pattern, field):
    rows = {}
    for answer_file in sorted(Path(folder).glob(pattern)):
        for line in answer_file.read_text().splitlines():
            if line.strip().startswith('{'):
                row = json.loads(line)
                rows[row[field]] = row
    return rows


def main():
    folder, items_key, groups_key = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text()), json.loads(Path(sys.argv[3]).read_text())
    first = {family: rows_of(folder / 'readers-answers', f'reader-{family}-packet-*.jsonl', 'item') for family in ('codex', 'claude')}
    third = {family: rows_of(folder / 'third-reader', f'rulings-{family}-*.jsonl', 'id') for family in ('codex', 'claude')}
    missing = [item for item in items_key if any(int(item) not in first[family] for family in first)]
    if missing:
        raise SystemExit(f'{len(missing)} items lack a row from a reader: {missing[:8]}')
    looks = {(row['case'], row['pass']): row for line in (folder / 'second-looks.jsonl').read_text().splitlines() for row in [json.loads(line)]}

    def faults(item):
        """(agreed, disputed) marks of one item in this round."""
        agreed, disputed = [], []
        for mark in MARKS:
            values = [first[family][int(item)].get(mark) for family in ('codex', 'claude')]
            if values == ['fails', 'fails']:
                agreed.append(mark)
            elif 'fails' in values:
                rulings = [third[family].get(f'{item}-{mark}', {}).get('ruling') for family in ('codex', 'claude')]
                if rulings == ['fails', 'fails']:
                    agreed.append(mark)
                elif 'fails' in rulings or None in rulings:          # the third readers part, or have not ruled
                    disputed.append(mark)
        for point in sorted(point for point in third['codex'] if str(point).startswith(f'{item}-W')):      # a fault named outside the form
            upheld = [bool(third[family].get(point, {}).get('upheld')) for family in ('codex', 'claude')]
            if all(upheld):
                agreed.append('W')
            elif any(upheld):
                disputed.append('W')
        return agreed, disputed

    item_of = {(case, pass_number, version): item for item, (case, pass_number, version) in items_key.items()}
    group_of = {tuple(send): (name, marks) for name, entries in groups_key.items() for send, marks in entries}
    counts = collections.defaultdict(collections.Counter)
    for send, (group, sampled_for) in sorted(group_of.items(), key=lambda pair: (pair[1][0], pair[0])):
        look = looks[send]
        first_agreed, first_disputed = faults(item_of[(*send, 'first')])
        kept_second = look['kept'] == 'second'
        second_agreed, second_disputed = faults(item_of[(*send, 'second')]) if kept_second else (first_agreed, first_disputed)
        turned = kept_second and (json.loads(look['first_text'])['ladder'] is None) != (json.loads(look['second_text'])['ladder'] is None)
        state = 'unchanged' if look['same'] else 'refused by code, first kept' if look['second_refused_for'] else 'changed'
        counts[group]['sends'] += 1
        counts[group][state] += 1
        counts[group]['first answer faulted again as agreed'] += bool(first_agreed)
        mended = bool(first_agreed) and kept_second and not second_agreed
        new_fault = kept_second and bool(set(second_agreed) - set(first_agreed))
        counts[group]['mended'] += mended
        counts[group]['mended and no new agreed fault'] += mended and not new_fault
        counts[group]['a new agreed fault'] += new_fault
        counts[group]['a ladder turned into a decline or the reverse'] += turned
        counts[group]['sends with a new agreed fault, turned or refused by code'] += bool(new_fault or turned or look['second_refused_for'])
        if state != 'unchanged' or first_agreed or first_disputed:
            print(f"[{group} {sampled_for}] {send[0]} send {send[1]}: {state} | first: agreed {first_agreed} disputed {first_disputed}"
                  + (f" | second: agreed {second_agreed} disputed {second_disputed}" if kept_second else '')
                  + (' | MENDED' if mended else '') + (' | NEW FAULT' if new_fault else '') + (' | TURNED' if turned else ''))
    print('=' * 110)
    for group in ('agreed', 'disputed', 'held', 'sound'):
        print(f'{group}: {dict(counts[group])}')
    agreed, sound = counts['agreed'], counts['sound']
    damaged = sound['sends with a new agreed fault, turned or refused by code']      # sends, as the registered page counts: a send that is two kinds is one
    print(f"the 18 with an agreed fault: faulted again in this round {agreed['first answer faulted again as agreed']}; mended {agreed['mended']}; a new agreed fault {agreed['a new agreed fault']}")
    print(f"   of the mended, those that carry no new agreed fault: {agreed['mended and no new agreed fault']}")
    print(f"the 30 no reader faulted: a new agreed fault {sound['a new agreed fault']}, turned {sound['a ladder turned into a decline or the reverse']}, "
          f"refused by code {sound['refused by code, first kept']}; sends that are any of the three: {damaged}")
    unresolved = sum(1 for item in items_key for mark in MARKS
                     if 'fails' in [first[family][int(item)].get(mark) for family in first] and [first[family][int(item)].get(mark) for family in first] != ['fails', 'fails']
                     and not all(third[family].get(f'{item}-{mark}') for family in third))
    print(f'marks on which the two first readers differ and no third reader has ruled: {unresolved}')


if __name__ == '__main__':
    main()
