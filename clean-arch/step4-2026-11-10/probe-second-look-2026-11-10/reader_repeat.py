"""How far a fresh reading round repeats the fourth Stage A's reading of the same answers ($0).

The 76 first answers of the second-look sample were read in the fourth Stage A and again, blind and mixed with second answers,
in this test's round, by fresh readers of the same two families with the same form. For each group the fourth run's reading
put an answer in, this prints what the new round says of the same answer, and whether the mark the fourth run agreed on is
agreed on again. It also lists the pairs in which the second look left a field untouched and the round marks the two items
differently on that field.

  python3 clean-arch/step4-2026-11-10/probe-second-look-2026-11-10/reader_repeat.py <probe data folder> <items key> <groups key>
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

    def faults(item):
        agreed, disputed = [], []
        for mark in MARKS:
            values = [first[family][int(item)].get(mark) for family in ('codex', 'claude')]
            if values == ['fails', 'fails']:
                agreed.append(mark)
            elif 'fails' in values:
                rulings = [third[family][f'{item}-{mark}']['ruling'] for family in ('codex', 'claude')]
                (agreed if rulings == ['fails', 'fails'] else disputed if 'fails' in rulings else []).append(mark)
        for point in sorted(point for point in third['codex'] if str(point).startswith(f'{item}-W')):
            upheld = [bool(third[family][point]['upheld']) for family in ('codex', 'claude')]
            (agreed if all(upheld) else disputed if any(upheld) else []).append('W')
        return agreed, disputed

    item_of = {(case, pass_number, version): item for item, (case, pass_number, version) in items_key.items()}
    table = collections.defaultdict(collections.Counter)
    same_mark = collections.Counter()
    for name, entries in groups_key.items():
        for send, sampled_for in entries:
            agreed, disputed = faults(item_of[(*send, 'first')])
            table[name]['an agreed fault' if agreed else 'a disputed fault only' if disputed else 'no fault'] += 1
            if name == 'agreed':
                same_mark['the same mark agreed again' if set(sampled_for) & set(agreed) else
                          'another mark agreed' if agreed else 'that mark disputed' if set(sampled_for) & set(disputed) else 'no agreed fault'] += 1
    print('the fourth run\'s reading of an answer (rows) against this round\'s reading of the same answer (columns)')
    for name in ('agreed', 'disputed', 'held', 'sound'):
        counts = table[name]
        print(f"  {name:9s} {sum(counts.values()):3d}: an agreed fault {counts['an agreed fault']:2d} | a disputed fault only {counts['a disputed fault only']:2d} | no fault {counts['no fault']:2d}")
    print('the 18 agreed in the fourth run, by the mark it agreed on:', dict(same_mark))
    points = [point for point in third['codex']]
    agree = sum(1 for point in points if (third['codex'][point].get('ruling'), third['codex'][point].get('upheld')) == (third['claude'][point].get('ruling'), third['claude'][point].get('upheld')))
    first_differ = sum(1 for item in items_key for mark in MARKS if len({first[family][int(item)].get(mark) for family in first}) == 2 and 'fails' in {first[family][int(item)].get(mark) for family in first})
    both_fail = sum(1 for item in items_key for mark in MARKS if [first[family][int(item)].get(mark) for family in first] == ['fails', 'fails'])
    print(f'this round, 102 items: marks both first readers fail {both_fail}; marks one fails {first_differ}; faults named outside the form {sum(1 for point in points if "-W-" in point)}; '
          f'the two third readers rule alike on {agree} of {len(points)} points')


if __name__ == '__main__':
    main()
