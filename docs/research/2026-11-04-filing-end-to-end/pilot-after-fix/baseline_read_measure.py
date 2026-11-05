"""The per-question reading's decision (baseline-design.md, step 1 second version). A question's starting figure is delivered in a send when the
send keeps (identity checked by code in baseline_read.py) every line the question needs from the quarter ended 2026-04-26, each with its figure in
the stored quote as printed, its value that figure, and its period or one-line naming that quarter:
  v10  operating income (53,536 GAAP or 53,783 non-GAAP) and revenue (81,615): the ratio's two lines, since the report states no margin;
  v12  purchases related to property and equipment and intangible assets (1,757).
Each of these figures, and each other-column figure below, is printed only in its own row of this report. A kept figure whose value is another
column's figure (the previous quarter or the year-ago quarter) while its period names the first quarter of FY2027 is a misread column and fails
the send. v10 and v12 each pass when delivered in at least 2 of 3 sends. v4 and v7 are controls that should return no figure: every figure they
return is listed for reading, and a kept figure that is not the question's own quantity fails the control.

usage: python3 baseline_read_measure.py baseline-read.json
"""
import json
import re
import sys

sys.path[:0] = ['/Users/lchingen/hivemind/src', '/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end']
from baseline_read import numbers  # noqa: E402  (one owner of what counts as a number)

NEEDS = {'v10': {'operating income': ('53,536', '53,783'), 'revenue': ('81,615',)}, 'v12': {'purchases of property and equipment': ('1,757',)}}
OTHER_COLUMNS = {'v10': ('44,299', '44,474', '21,638', '21,801', '68,127', '44,062'), 'v12': ('1,284', '1,227')}
CONTROLS = ('v4', 'v7')


def first_quarter_fy27(text):
    if re.search(r'April 26,? 2026|Apr\.? 26,? 2026|2026-04-26', text):
        return True
    return bool(re.search(r'\bQ1\b|first[- ]quarter|first fiscal quarter', text, re.I) and re.search(r'FY ?27\b|FY ?2027|fiscal (?:year )?2027', text, re.I))


def is_figure(value_text, printed):
    return numbers(value_text) == [float(printed.replace(',', ''))]


def lines_found(view_id, figures):
    return {line: [f for f in figures if f['kept'] and any(p in f['quote'] and is_figure(f['value'], p) for p in printed_set)
                   and first_quarter_fy27(f['period'] + ' ' + f['one_line'])]
            for line, printed_set in NEEDS[view_id].items()}


def misread(view_id, figures):
    return [f for f in figures if f['kept'] and any(is_figure(f['value'], p) for p in OTHER_COLUMNS[view_id]) and first_quarter_fy27(f['period'])]


def delivered(view_id, figures):
    return all(lines_found(view_id, figures).values()) and not misread(view_id, figures)


def main():
    results = json.load(open(sys.argv[1]))['results']
    verdict = {}
    for view_id in NEEDS:
        verdict[view_id] = 0
        for n, r in enumerate(results[view_id]):
            figures = r['figures']
            found, wrong = lines_found(view_id, figures), misread(view_id, figures)
            ok = delivered(view_id, figures)
            verdict[view_id] += ok
            bases = sorted({f['basis'] for fs in found.values() for f in fs})
            print(f'{view_id} send {n}: {"delivered" if ok else "not delivered"}; figures {len(figures)}, kept {sum(f["kept"] for f in figures)}; '
                  + '; '.join(f'{line}: {len(fs)}' for line, fs in found.items()) + f'; basis {bases}; misread columns {len(wrong)}')
            for f in figures:
                if not f['kept']:
                    print(f'   refused (in report {f["in_report"]}, labelled {f["labelled"]}, ends on value {f["ends_on_value"]}): {f["quote"][:120]!r} value {f["value"]!r}')
    for view_id in CONTROLS:
        for n, r in enumerate(results.get(view_id, [])):
            print(f'{view_id} (control) send {n}: figures {len(r["figures"])}, kept {sum(f["kept"] for f in r["figures"])}')
            for f in r['figures']:
                print(f'   kept {f["kept"]} | {f["value"]} {f["unit"]} | {f["period"]} | {f["quote"][:100]!r} | {f["one_line"][:120]}')
    ok = all(v >= 2 for v in verdict.values())
    print('\nper-question reading: ' + ', '.join(f'{v} {verdict[v]}/3' for v in verdict) + f' -> {"pass" if ok else "FAIL"} (each needs at least 2 of 3); '
          'controls v4, v7: read the figures listed above')


if __name__ == '__main__':
    main()
