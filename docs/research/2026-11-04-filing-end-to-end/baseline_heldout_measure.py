"""The held-out reading of the August 26 report (baseline-design.md, round 18; round 25 for the third version: the latest quarter or the year-to-date
through it, each labelled, is the starting figure, and only a wrong figure stops), the conditions written before the send. No judgement (the ruler has
no window there):
  delivery  v10 keeps, in one send (two items together), the latest quarter's operating income and revenue, and v12 the latest quarter's purchases
            related to property and equipment and intangible assets, each kept, its printed figure in the quote, its value that figure, and its
            period or one-line naming the quarter ended July 26, 2026 (Q2 FY27); a six-month figure labelled as the six months is the question's own
            quantity of another period (allowed, not delivery); a kept figure of a stale column (the previous quarter, the year-ago quarter, either
            six-month column) labelled as the latest quarter, or the year-ago six months labelled as the latest six months, or the quarter labelled
            as the six months, is a misread and fails the send; each question in at least 2 of 3 sends;
  identity  every kept figure of the 22 questions has a final class from two readers, none misread, another quantity or not a figure (the
            classification file, checked by baseline_all_measure.judge's rules).
The reading must hold the 22 seed questions, each of the two chosen items, three readable replies each; anything less leaves it incomplete.

usage: python3 baseline_heldout_measure.py <reading.json> [<classified.json>]
"""
import json
import re
import sys

sys.path[:0] = ['/Users/lchingen/hivemind/src', '/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end']
import baseline_all_measure as bam  # noqa: E402
from baseline_read import numbers  # noqa: E402

SENDS = 3
QUARTER = {'v10': {'operating income': ('63,734', '63,956'), 'revenue': ('96,221',)}, 'v12': {'purchases': ('2,677',)}}
HALF = {'v10': ('117,270', '117,739', '177,837'), 'v12': ('4,434',)}                 # the six months ended July 26, 2026
STALE = {'v10': ('53,536', '53,783', '81,615', '28,440', '28,541', '46,743'), 'v12': ('1,757', '1,894')}   # previous and year-ago quarters
HALF_STALE = {'v10': ('50,078', '50,341', '90,805'), 'v12': ('3,122',)}                # the six months a year earlier
SEEDS = [f'v{k}' for k in range(1, 23)]


def quarter_label(text):
    if half_label(text) or re.search(r'six months|first half|\bH1\b|year[- ]to[- ]date', text, re.I):
        return False                                   # a half-year label is never also the quarter's
    return bool(re.search(r'July 26,? 2026|Jul\.? 26,? 2026|2026-07-26', text) or (re.search(r'\bQ2\b|second[- ]quarter', text, re.I)
                and re.search(r'FY ?27\b|FY ?2027|fiscal (?:year )?2027', text, re.I)))


def half_label(text):
    return bool(re.search(r'six months|first half|\bH1\b', text, re.I) and re.search(r'July 26,? 2026|FY ?27\b|FY ?2027|fiscal (?:year )?2027', text, re.I))


def is_figure(value_text, printed):
    return numbers(value_text) == [float(printed.replace(',', ''))]


HALF_LINES = {'v10': {'operating income': ('117,270', '117,739'), 'revenue': ('177,837',)}, 'v12': {'purchases': ('4,434',)}}


def delivered(view_id, figures, year_to_date=False):
    label = lambda f: f['period'] + ' ' + f['one_line']
    value_in = lambda f, printed: any(is_figure(f['value'], p) for p in printed)
    has = lambda needs, labelled: all(any(f['kept'] and p in f['quote'] and is_figure(f['value'], p) and labelled(label(f)) for f in figures for p in printed)
                                      for printed in needs.values())
    found = has(QUARTER[view_id], quarter_label) or (year_to_date and has(HALF_LINES[view_id], half_label))
    quarter_values = [p for printed in QUARTER[view_id].values() for p in printed]
    misread = [f for f in figures if f['kept'] and ((value_in(f, STALE[view_id] + HALF[view_id] + HALF_STALE[view_id]) and quarter_label(label(f)))
                                                   or (value_in(f, HALF_STALE[view_id] + STALE[view_id] + tuple(quarter_values)) and half_label(label(f))))]
    return found and not misread, misread


def main():
    reading = json.load(open(sys.argv[1]))
    if reading.get('report_day') != '2026-08-26':
        raise SystemExit('the reading is not of the August 26 report')
    year_to_date = reading.get('task_version') == 3          # round 25: the year-to-date through the latest quarter, labelled, is delivered too
    rows = bam.sheet_rows(reading)                     # refuses a reading whose items are not the chosen ones, an incomplete one, or a failed send
    sends = lambda v, n: [f for i in reading['report'] for f in reading['results'][v][i][n]['figures']]
    verdict = {}
    for view_id in ('v10', 'v12'):
        results = [delivered(view_id, sends(view_id, n), year_to_date) for n in range(SENDS)]
        verdict[view_id] = sum(ok for ok, _ in results)
        for n, (ok, misread) in enumerate(results):
            print(f'{view_id} send {n}: {"delivered" if ok else "not delivered"}; misread {len(misread)}')
            for f in sends(view_id, n):
                print(f'   kept {f["kept"]}: {f["value"]} | {f["period"][:45]} | {f["quote"][:90]!r}')
    print(f'kept figures over the 22 questions: {len(rows)}; by question ' + str({v: sum(1 for r in rows if r['view_id'] == v) for v in dict.fromkeys(r['view_id'] for r in rows)}))
    delivery_ok = all(v >= 2 for v in verdict.values())
    if year_to_date:
        print(f'recall, recorded and not a condition (round 25): v10, v12 delivered in {verdict} of 3 sends')
    else:
        print(f'delivery (v10, v12 each at least 2 of 3): {"pass" if delivery_ok else "FAIL"} {verdict}')
    if len(sys.argv) < 3:
        print('identity: the classification file is not given; not judged')
        return
    classified = json.load(open(sys.argv[2]))
    expected, given = {r['key'] for r in rows}, [c['key'] for c in classified]
    problems = [c['key'] for c in classified if not bam.decided(c, 'class', bam.CLASSES)]
    if set(given) != expected or len(given) != len(set(given)) or problems:
        raise SystemExit(f'classification incomplete: {len(expected - set(given))} missing, {len(set(given) - expected)} unknown, '
                         f'{len(given) - len(set(given))} duplicates, {len(problems)} not two readers\' classes with a final one that is theirs')
    wrong = [c['key'] for c in classified if c['class'] in bam.WRONG]
    print(f'{"the one stop condition, " if year_to_date else ""}identity (nothing misread, of another quantity or not a figure): {"pass" if not wrong else "FAIL " + str(wrong)}; '
          + str({k: sum(1 for c in classified if c['class'] == k) for k in bam.CLASSES}))


if __name__ == '__main__':
    main()
