"""Tally the reference reading ($0): per reader and per mark, on how many of the 36 production ladders the mark applies, holds and
fails; how many ladders hold every mark that applies; and, with two readers, on how many ladders they agree that it does.

Usage: python3 tally.py reader-codex.jsonl [reader-claude.jsonl]"""
import collections, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MARKS = ['ONE', 'O', 'R', 'D', 'X', 'F', 'Y', 'G']


def load(name):
    rows = {r['item']: r for r in (json.loads(l) for l in (HERE / name).read_text().splitlines() if l.strip().startswith('{'))}
    if sorted(rows) != list(range(1, 37)):
        raise SystemExit(f'{name}: items {sorted(rows)}, not 1..36')
    return rows


def sound(row):
    return not any(row.get(m) == 'fails' for m in MARKS) and not (row.get('W') or '').strip()


def main():
    packet = json.loads((HERE / 'packet.json').read_text())
    readers = {name: load(name) for name in sys.argv[1:]}
    for name, rows in readers.items():
        print(f'\n{name}: 36 ladders')
        for m in MARKS:
            c = collections.Counter(r.get(m) for r in rows.values())
            print(f'  {m:4} holds {c["holds"]:2}  fails {c["fails"]:2}  not assessable {c["not_assessable"]:2}  n/a {c["n/a"]:2}')
        print(f'  another fault named (W): {sum(1 for r in rows.values() if (r.get("W") or "").strip())}')
        print(f'  ladders holding every mark that applies, with no other fault: {sum(1 for r in rows.values() if sound(r))} of 36')
        five = [i for i, r in rows.items() if len(packet[i - 1]["ladder_as_the_judge_is_shown_it"]["rungs"]) == 5]
        print(f'  of the {len(five)} five-rung ladders: {sum(1 for i in five if sound(rows[i]))} sound; of the {36 - len(five)} yes/no: {sum(1 for i in rows if i not in five and sound(rows[i]))} sound')
    if len(readers) == 2:
        a, b = readers.values()
        print(f'\nboth readers call the ladder sound: {sum(1 for i in a if sound(a[i]) and sound(b[i]))}; both unsound: {sum(1 for i in a if not sound(a[i]) and not sound(b[i]))}; '
              f'they differ: {sum(1 for i in a if sound(a[i]) != sound(b[i]))}')
        for m in MARKS:
            print(f'  same value on {m}: {sum(1 for i in a if a[i].get(m) == b[i].get(m))} of 36')


if __name__ == '__main__':
    main()
