"""Score the self-report diagnostic by the rule frozen in DESIGN.md ($0). It reads the letter on the reply's first non-empty line
only in the form "LETTER: X" (bold marks allowed); anything else is unresolved. It judges nothing else.

  python3 score_self_report.py --self-test
  python3 score_self_report.py <output folder>
"""
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIRST_LINE = re.compile(r'^\W*LETTER\W*:\W*([A-E])\b\W*$')
WARNING = {'C', 'D'}
CLEAR = {'A', 'B', 'C', 'D'}    # E (mixed, cannot tell) is counted with the unresolved, and reported apart


def letter_of(account):
    if not account:
        return None
    first = next((line for line in account.splitlines() if line.strip()), '')
    found = FIRST_LINE.match(first.strip())
    return found.group(1) if found else None


SELF_TEST = [('LETTER: C\nThe 50% discount is mine.', 'C'), ('**LETTER: D**\nNothing sizes it.', 'D'), ('LETTER:B\n...', 'B'),
             ('  \nLETTER: E\nmixed', 'E'), ('Answer: C\n...', None), ('A: the figure e12 places it', None), ('', None), (None, None),
             ('LETTER: C or D\n...', None), ('LETTER: F\n', None), ('The letter is C', None)]


def self_test():
    failed = [(text, want, letter_of(text)) for text, want in SELF_TEST if letter_of(text) != want]
    print(f'self-test: {len(SELF_TEST)} examples, {len(failed)} failed', failed)
    return not failed


def main(folder):
    cases = {c['case']: c for c in json.loads((HERE / 'cases.json').read_text())}
    records = json.loads((Path(folder) / 'accounts.json').read_text())
    seen = collections.Counter(record['case'] for record in records)
    unknown = [case for case in seen if case not in cases]
    duplicated = [case for case, count in seen.items() if count > 1]
    if unknown or duplicated:
        raise SystemExit(f'unknown cases {unknown}, duplicated cases {duplicated}: refused')
    by_case = {record['case']: record for record in records}
    missing = [case for case in cases if case not in by_case]
    print(f'records {len(records)} of {len(cases)} cases; missing (scored unresolved) {missing}')
    rows = [{'case': name, 'group': case['group'], 'path': (case['draw'], case['view']), 'letter': letter_of(by_case.get(name, {}).get('account'))}
            for name, case in cases.items()]
    for group in ('failed', 'passed'):
        mine = [r for r in rows if r['group'] == group]
        letters = collections.Counter(r['letter'] or 'unresolved' for r in mine)
        warned = sum(r['letter'] in WARNING for r in mine)
        unresolved = sum(r['letter'] not in CLEAR for r in mine)
        print(f'{group}: {len(mine)} | letters {dict(letters)} | warnings {warned} | unresolved {unresolved}')
    failed = [r for r in rows if r['group'] == 'failed']
    passed = [r for r in rows if r['group'] == 'passed']
    print(f"unresolved or E in all: {sum(r['letter'] not in CLEAR for r in rows)} (E alone {sum(r['letter'] == 'E' for r in rows)}); more than 4 makes the result unclear")
    for label, as_warning in (('unresolved and E counted as no warning', False), ('unresolved and E counted as a warning', True)):
        warn = lambda r: r['letter'] in WARNING or (as_warning and r['letter'] not in CLEAR)
        misses = sum(not warn(r) for r in failed)
        false_alarms = sum(warn(r) for r in passed)
        print(f'{label}: misses {misses} of {len(failed)}, false alarms {false_alarms} of {len(passed)}')
    print('per path (warning share, failed against passed):')
    for path in sorted({r['path'] for r in rows}):
        f = [r for r in failed if r['path'] == path]
        p = [r for r in passed if r['path'] == path]
        print(f"   {path}: failed {sum(r['letter'] in WARNING for r in f)}/{len(f)}, passed {sum(r['letter'] in WARNING for r in p)}/{len(p)}, "
              f"unresolved or E {sum(r['letter'] not in CLEAR for r in f + p)}")


if __name__ == '__main__':
    if sys.argv[1] == '--self-test':
        sys.exit(0 if self_test() else 1)
    main(sys.argv[1])
