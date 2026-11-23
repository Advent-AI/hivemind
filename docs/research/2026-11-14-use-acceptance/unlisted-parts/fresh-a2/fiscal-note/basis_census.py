"""D607's $0 audit of the shared fiscal-year note: on every company-figure answer the frozen answer-choice step wrote in the stored
gate-1 readings (probe readings: control sends only), the due-day basis the model chose ('stated', which code keeps, or
'expected_publication', which code replaces by D414's day), and whether a 'stated' day falls in the month the note names ("published …
around <year>-<month>; use that day as the due date"), with both first readers' D. Counted once per distinct answer. Judges nothing.

  python3 basis_census.py <output .jsonl>
"""
import collections
import glob
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parents[1]), str(HERE.parent / 'postponement')]
import d_split_census as census  # noqa: E402
from audit_collect import BEFORE_THE_FROZEN_STEP, KEYS  # noqa: E402

NOTE_MONTH = re.compile(r'published in the annual report around (\d{4}-\d{2}); use that day as the due date')


def main(output):
    readings = sorted(os.path.dirname(f) for f in glob.glob(str(census.ROOT / 'poc/data/**/readers-answers'), recursive=True))
    answers = {}
    for reading in readings:
        relative = str(Path(reading).relative_to(census.ROOT / 'poc/data'))
        if relative.startswith(BEFORE_THE_FROZEN_STEP):
            continue
        key_name = next((name for folder, name in KEYS.items() if relative.startswith(folder)), None)
        key = json.loads(Path(f'~/.hivemind-keys/{key_name}/key.json').expanduser().read_text()) if key_name else None
        items = census.items_of(reading)
        rows = {family: census.rows_of(reading, family) for family in census.FAMILIES}
        for number, item in sorted(items.items()):
            if key is not None and not key[str(number)][0].startswith('control|'):
                continue
            shown, other = item.get('ladder_as_the_judge_is_shown_it') or {}, item.get('other_fields') or {}
            if shown.get('kind') != 'asset' or other.get('due_day_basis') not in ('stated', 'expected_publication'):
                continue
            note = NOTE_MONTH.search(item.get('fiscal_year_note') or '')
            identity = json.dumps([shown.get('question'), shown.get('due_day'), other.get('due_day_basis')], ensure_ascii=False)
            entry = answers.setdefault(identity, {'question': shown.get('question'), 'due_day': shown.get('due_day'), 'basis': other['due_day_basis'],
                                                  'note_month': note.group(1) if note else None, 'article_day': (item.get('article') or {}).get('publication_date'),
                                                  'D': []})
            entry['D'].append(tuple(rows[family].get(number, {}).get('D') for family in census.FAMILIES))
    Path(output).write_text('\n'.join(json.dumps(entry, ensure_ascii=False) for entry in answers.values()) + '\n')
    tally = collections.Counter()
    for entry in answers.values():
        in_note_month = bool(entry['note_month'] and entry['due_day'] and entry['due_day'][:7] == entry['note_month'])
        tally[(entry['basis'], 'due day in the note\'s month' if in_note_month else 'another day')] += 1
    print(f'distinct company-figure answers: {len(answers)}')
    for key, count in sorted(tally.items()):
        print(f'   {count:4}  {key}')
    print('\nevery "stated" answer, read for whether the article states its day:')
    for entry in answers.values():
        if entry['basis'] == 'stated':
            print(f"   due {entry['due_day']} | note month {entry['note_month']} | D {entry['D']} | {entry['question'][:170]}")


if __name__ == '__main__':
    main(sys.argv[1])
