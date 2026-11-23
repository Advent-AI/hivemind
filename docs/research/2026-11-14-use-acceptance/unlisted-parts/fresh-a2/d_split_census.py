"""The D-mark split on code-set due days ($0; RESULT-FRESH-A2.md, "Where the families split").

A company figure whose due day the step gave as `expected_publication` is shown with the day code sets (D414: 60 days after the
fiscal year-end). The fiscal-year note shown beside it says the annual report appears "around <year>-<month>; use that day as the
due date". For every stored gate-1 reading, this counts the items of that class (the shown day not in the note's month), each
first-reader family's D failures on them, and the third readers' rulings on their D points.

  python3 d_split_census.py
  python3 d_split_census.py --reasons <output .jsonl>   (every Codex D failure in the class, with its reason and reason class)
"""
import collections
import glob
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
NOTE = re.compile(r'around (\d{4})-(\d{2}); use that day as the due date')
FAMILIES = ('codex', 'claude')


def items_of(reading):
    items = {}
    for packet in sorted(glob.glob(f'{reading}/readers/packet-*.json')):
        content = json.loads(Path(packet).read_text())
        for item in content if isinstance(content, list) else []:
            if isinstance(item, dict) and 'item' in item:
                items[item['item']] = item
    return items


def in_class(item):
    shown, other = item.get('ladder_as_the_judge_is_shown_it') or {}, item.get('other_fields') or {}
    note = NOTE.search(item.get('fiscal_year_note') or '')
    return bool(shown.get('kind') == 'asset' and other.get('due_day_basis') == 'expected_publication' and note and shown.get('due_day')
                and not shown['due_day'].startswith(f'{note.group(1)}-{note.group(2)}'))


def rows_of(reading, family):
    rows = {}
    files = sorted(glob.glob(f'{reading}/readers-answers/reader-{family}-packet-*.jsonl'), key=lambda name: ('-again-' in name, name))
    for answer_file in files:
        for line in Path(answer_file).read_text().splitlines():
            line = line.strip()
            if line.startswith('{'):
                try:
                    row = json.loads(line)
                    rows[row['item']] = row
                except (ValueError, KeyError):
                    pass
    return rows


def rulings_of(reading, family, members):
    found = collections.Counter()
    for ruling_file in glob.glob(f'{reading}/third-reader/rulings-{family}-*.jsonl'):
        for line in Path(ruling_file).read_text().splitlines():
            if line.strip().startswith('{'):
                try:
                    ruling = json.loads(line)
                except ValueError:
                    continue
                point = ruling.get('id', '')
                if point.endswith('-D') and point.split('-')[0].isdigit() and int(point.split('-')[0]) in members:
                    found[ruling.get('ruling')] += 1
    return dict(found)


def obligation_naming_the_filing(item, row):
    """The reason class read in round 104: a binding-obligation topic whose Codex reason says the next annual filing or report
    falls on another day than the one shown (the note's "around February", or "April 1 is an estimated publication date")."""
    reason = (row.get('why') or '').lower()
    return (item.get('thesis') or {}).get('opens_as') == 'binding_obligation' and ('annual filing' in reason or 'annual report' in reason)


def write_reasons(path):
    """One line for every Codex D failure on a class item, with the reason class; then the counts."""
    readings = sorted(os.path.dirname(found) for found in glob.glob(str(ROOT / 'poc/data/**/readers-answers'), recursive=True))
    lines, counts = [], collections.Counter()
    for reading in readings:
        items = items_of(reading)
        rows = {family: rows_of(reading, family) for family in FAMILIES}
        for number, item in sorted(items.items()):
            if not in_class(item) or rows['codex'].get(number, {}).get('D') != 'fails':
                continue
            kind = 'obligation: reason names the next annual filing or report' if obligation_naming_the_filing(item, rows['codex'][number]) else 'other'
            counts[kind] += 1
            shown = item['ladder_as_the_judge_is_shown_it']
            lines.append(json.dumps({'reading': os.path.relpath(reading, ROOT), 'item': number, 'class': kind,
                                     'opens_as': (item.get('thesis') or {}).get('opens_as'), 'year': shown.get('year'), 'due_day': shown.get('due_day'),
                                     'claude_D': rows['claude'].get(number, {}).get('D'), 'codex_why': rows['codex'][number].get('why')}, ensure_ascii=False))
    Path(path).write_text('\n'.join(lines) + '\n')
    print(f'{len(lines)} Codex D failures in the class: {dict(counts)} -> {path}')


def main():
    if sys.argv[1:2] == ['--reasons']:
        write_reasons(sys.argv[2])
        return
    readings = sorted(os.path.dirname(path) for path in glob.glob(str(ROOT / 'poc/data/**/readers-answers'), recursive=True))
    totals = collections.Counter()
    for reading in readings:
        items = items_of(reading)
        if not items:
            continue
        members = {number for number, item in items.items() if in_class(item)}
        rows = {family: rows_of(reading, family) for family in FAMILIES}
        fails = {family: sum(1 for number in members if rows[family].get(number, {}).get('D') == 'fails') for family in FAMILIES}
        rulings = {family: rulings_of(reading, family, members) for family in FAMILIES}
        print(f'{os.path.relpath(reading, ROOT)}: items {len(items)}; in the class {len(members)}; D fails on them {fails}; third rulings {rulings}')
        totals['items'] += len(items)
        totals['in the class'] += len(members)
        for family in FAMILIES:
            totals[f'{family} D fails'] += fails[family]
    print('TOTAL', dict(totals))


if __name__ == '__main__':
    main()
