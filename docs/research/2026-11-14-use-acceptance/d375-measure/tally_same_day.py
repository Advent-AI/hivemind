"""Eligible cases for a measurement of D375, step 3 ($0; D528): the two reader families' marks joined with the key. It refuses when a
packet lacks its completion line or an item lacks a mark. It judges nothing: it counts, per question and per kind of statement, what
each family and both families marked as bearing, and how each family marked the known cases (statements the system itself filed under
the question that day).

  python3 tally_same_day.py <key folder outside the repository>
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')


def rows_of(path):
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find('{"', position)
        if start == -1:
            return out
        try:
            row, position = decoder.raw_decode(text, start)
            out.append(row)
        except json.JSONDecodeError:
            position = start + 1


def main():
    key = json.loads((Path(sys.argv[1]) / 'same-day-key.json').read_text())
    packets = [name for name, _ in json.loads((HERE / 'packets.json').read_text())]
    marks = {family: {} for family in FAMILIES}
    for family in FAMILIES:
        for name in packets:
            path = HERE / f'{family}-{name}.jsonl'
            rows = rows_of(path) if path.exists() else []
            if not any(row.get('done') for row in rows):
                raise SystemExit(f'{family} {name}: no completion line: refused')
            marks[family].update({row['item']: row for row in rows if 'item' in row})
        missing = [entry['item'] for entry in key if entry['item'] not in marks[family]]
        if missing:
            raise SystemExit(f'{family}: {len(missing)} items without a mark, such as {missing[:5]}: refused')
    yes = lambda family, item: str(marks[family][item].get('bears')).lower().startswith('yes')
    table = collections.defaultdict(collections.Counter)
    both_bear = []
    for entry in key:
        pair = [yes(family, entry['item']) for family in FAMILIES]
        for scope in ('all', entry['question']):
            table[(scope, entry['status'])]['items'] += 1
            table[(scope, entry['status'])]['codex'] += pair[0]
            table[(scope, entry['status'])]['claude'] += pair[1]
            table[(scope, entry['status'])]['both'] += all(pair)
        if all(pair) and entry['status'] != 'filed under this question that day':
            both_bear.append(entry)
    for status in ('filed under this question that day', 'kept under other questions', 'dropped for want of a question'):
        row = table[('all', status)]
        print(f"{status}: {row['items']} items; marked as bearing by Codex {row['codex']}, by Claude {row['claude']}, by both {row['both']}")
    print('\nby question (kept elsewhere + dropped; both families say it bears):')
    for question in sorted({entry['question'] for entry in key}, key=lambda v: int(v[1:])):
        kept, dropped, known = table[(question, 'kept under other questions')], table[(question, 'dropped for want of a question')], table[(question, 'filed under this question that day')]
        print(f"  {question}: kept elsewhere {kept['both']} of {kept['items']}; dropped {dropped['both']} of {dropped['items']}; known cases marked by both {known['both']} of {known['items']}")
    (HERE / 'both-bear.json').write_text(json.dumps([{**entry, 'codex_why': marks['codex'][entry['item']].get('why'), 'claude_why': marks['claude'][entry['item']].get('why')} for entry in both_bear], indent=1, ensure_ascii=False) + '\n')
    distinct = {(entry['question'], entry['stored_id']) for entry in both_bear}
    print(f"\nboth families: {len(both_bear)} statement-and-question items bear and did not reach the question that day ({len(distinct)} distinct pairs); "
          f"{sum(1 for e in both_bear if e['status'].startswith('dropped'))} of them were dropped for want of a question")


if __name__ == '__main__':
    main()
