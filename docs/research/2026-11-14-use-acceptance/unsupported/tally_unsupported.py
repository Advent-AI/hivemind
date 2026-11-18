"""The census of unsupported judgements, step 2 ($0; D518): counts by what the answer did. The settled verdict of every judgement of the
two earlier readings comes from `inventory-earlier-readings.json` (built from the readers' stored files); the class of each comes from
`class-by-judgement.json`, written by hand after reading. The script refuses when a judgement of the inventory has no class or a class
names a judgement the inventory does not hold. The two later readings (the trial, the fresh week) are counted from the hand file, each
row naming its source.

  python3 tally_unsupported.py
"""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
READ = {'baseline': 159, 'stage-b': 236, 'trial': 21, 'week': 22}


def main():
    inventory = json.loads((HERE / 'inventory-earlier-readings.json').read_text())
    classes = json.loads((HERE / 'class-by-judgement.json').read_text())
    class_of = {}
    matter_of = {}
    for path in classes['earlier_readings']:
        for number, name in path['numbers'].items():
            class_of[(path['reading'], path['draw'], path['view'], int(number))] = name
            matter_of[(path['reading'], path['draw'], path['view'])] = path['matter']
    held = {(row['reading'], row['draw'], row['view'], row['number_in_view']) for row in inventory}
    if held != set(class_of):
        raise SystemExit(f'classes and inventory differ: without a class {sorted(held - set(class_of))}; not in the inventory {sorted(set(class_of) - held)}: refused')
    agreed = collections.Counter()          # (class, verdict) over judgements settled UNSUPPORTED or INSUFFICIENT
    open_marks = collections.Counter()      # class over judgements left unresolved or failed by one team only
    matters = collections.defaultdict(lambda: collections.Counter())
    paths = collections.defaultdict(set)
    per_reading = collections.defaultdict(collections.Counter)
    for row in inventory:
        name = class_of[(row['reading'], row['draw'], row['view'], row['number_in_view'])]
        if row['settled'] in ('UNSUPPORTED', 'INSUFFICIENT'):
            agreed[(name, row['settled'])] += 1
            matters[name][matter_of[(row['reading'], row['draw'], row['view'])]] += 1
            paths[name].add((row['reading'], row['draw'], row['view']))
            per_reading[row['reading']][row['settled']] += 1
        else:
            open_marks[(name, 'unresolved' if row['settled'] == 'unresolved' else 'settled SUPPORTED after a split')] += 1
            per_reading[row['reading']]['unresolved' if row['settled'] == 'unresolved' else 'split, settled SUPPORTED'] += 1
    for row in classes['later_readings']:
        if row['settled'] == 'UNSUPPORTED':
            agreed[(row['class'], 'UNSUPPORTED')] += 1
            matters[row['class']][row['matter']] += 1
            paths[row['class']].add((row['reading'], row['view']))
            per_reading[row['reading']]['UNSUPPORTED'] += 1
        else:
            open_marks[(row['class'], 'failed by one team only')] += 1
            per_reading[row['reading']]['failed by one team only'] += 1
    print('judgements read:', READ, '=', sum(READ.values()))
    for reading in READ:
        print(f'  {reading}: {dict(per_reading[reading])}')
    total = sum(agreed.values())
    print(f'\nsettled UNSUPPORTED or INSUFFICIENT (both first readers, or both third readers): {total} of {sum(READ.values())}')
    for name in classes['classes']:
        count = sum(v for (c, _), v in agreed.items() if c == name)
        print(f"  {name}: {count} ({count * 100 // total if total else 0}%) = UNSUPPORTED {agreed[(name, 'UNSUPPORTED')]}, INSUFFICIENT {agreed[(name, 'INSUFFICIENT')]}; "
              f"question paths {len(paths[name])}; by matter {dict(matters[name])}")
    print(f"  UNSUPPORTED alone: {sum(v for (_, verdict), v in agreed.items() if verdict == 'UNSUPPORTED')}: " + ', '.join(f"{name} {agreed[(name, 'UNSUPPORTED')]}" for name in classes['classes']))
    print('\nnot settled (unresolved, split and settled SUPPORTED, or failed by one team only):', sum(open_marks.values()))
    for name in classes['classes']:
        print(f"  {name}: " + ', '.join(f'{kind} {count}' for (c, kind), count in sorted(open_marks.items()) if c == name))


if __name__ == '__main__':
    main()
