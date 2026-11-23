"""D614's $0 design review, the census part: every distinct topic the frozen answer-choice step was given in the stored gate-1 readings
(probe readings: control sends only) whose description or outcome names two or more distinct years, with what the step did on each
send (refusal, a ladder for which year, or an event) and both first readers' N and L. Code finds only the years named; whether the two
years are one quantity tracked twice (D38's one view a year) is read by hand afterwards. Judges nothing.

  python3 two_year_census.py <output .jsonl>
"""
import collections
import glob
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRESH = HERE.parent / 'unlisted-parts' / 'fresh-a2'
sys.path[:0] = [str(FRESH), str(FRESH.parent), str(FRESH / 'postponement')]
import d_split_census as census  # noqa: E402
from audit_collect import BEFORE_THE_FROZEN_STEP, KEYS  # noqa: E402

YEAR = re.compile(r'\b(?:FY|fiscal (?:year )?|calendar (?:year )?)?(20(?:2[5-9]|3[0-2]))\b', re.I)


def main(output):
    readings = sorted(os.path.dirname(f) for f in glob.glob(str(census.ROOT / 'poc/data/**/readers-answers'), recursive=True))
    topics = collections.OrderedDict()
    for reading in readings:
        relative = str(Path(reading).relative_to(census.ROOT / 'poc/data'))
        if relative.startswith(BEFORE_THE_FROZEN_STEP):
            continue
        key_name = next((name for folder, name in KEYS.items() if relative.startswith(folder)), None)
        key = json.loads(Path(f'~/.hivemind-keys/{key_name}/key.json').expanduser().read_text()) if key_name else None
        items = census.items_of(reading)
        marks = {family: census.rows_of(reading, family) for family in census.FAMILIES}
        for number, item in sorted(items.items()):
            if key is not None and not key[str(number)][0].startswith('control|'):
                continue
            thesis = item.get('thesis') or {}
            text = f"{thesis.get('description', '')} || {thesis.get('outcome', '')}"
            years = sorted(set(YEAR.findall(text)))
            if len(years) < 2:
                continue
            shown = item.get('ladder_as_the_judge_is_shown_it') or {}
            kind = 'refusal' if not shown.get('rungs') else ('event' if any(r.get('label') == 'Ruled out' or r.get('label') == 'Yes' for r in shown.get('rungs') or []) else 'figure')
            entry = topics.setdefault(thesis.get('description'), {'description': thesis.get('description'), 'outcome': thesis.get('outcome'),
                                                                  'period': thesis.get('period'), 'years': years, 'sends': []})
            entry['sends'].append({'reading': relative, 'item': number, 'kind': kind, 'year': shown.get('year'), 'due_day': shown.get('due_day'),
                                   'N': tuple(marks[f].get(number, {}).get('N') for f in census.FAMILIES),
                                   'L': tuple(marks[f].get(number, {}).get('L') for f in census.FAMILIES)})
    Path(output).write_text('\n'.join(json.dumps(t, ensure_ascii=False) for t in topics.values()) + '\n')
    print(f'distinct topics naming two or more years: {len(topics)}')
    for t in topics.values():
        kinds = collections.Counter(s['kind'] for s in t['sends'])
        years_answered = collections.Counter(s['year'] for s in t['sends'] if s['kind'] == 'figure')
        print(f"- years {t['years']} | sends {dict(kinds)} | figure years answered {dict(years_answered)} | {t['description'][:150]}")


if __name__ == '__main__':
    main(sys.argv[1])
