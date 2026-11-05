"""Census of every stored coverage-start reading (Alex, 2026-11-05: "我需要你深度看完所有失败trace给我准信下一步你要跑什么才能收敛"), $0. Every read of
every version (the pilot, round 13, the third version's trial and registered reading, the fourth version's trial, May and August readings) is put
against one answer key written from the two reports' own text: for each question, the figures an analyst reads its quantity off (its own figure,
the lines it is computed from, the report's own line for it), for the latest period or another period labelled as such; the questions whose
quantity the report does not state are expected empty. Each kept figure, each refused figure and each empty read is classed:
  kept right · kept, another period labelled · kept WRONG (not this question's quantity) · kept DEBATABLE (a broader line the gold's own reader
  uses with a share) · refused but RIGHT (the code check refused a right figure) · refused and wrong or not a figure (the check did its job) ·
  MISSED (the question has a figure in this report and the read kept none) · empty and right.

usage: python3 census_all_reads.py > census-all-reads.txt
"""
import json
import re
import sqlite3
import sys

HERE = '/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end'
sys.path[:0] = ['/Users/lchingen/hivemind/src', '/Users/lchingen/hivemind/scripts', HERE]
import baseline_read as br  # noqa: E402
import baseline_read_measure as brm  # noqa: E402
from baseline_heldout_measure import half_label, quarter_label  # noqa: E402

# the answer key, from the reports' text (values as printed, any scale the report prints them in)
MAY = {'v1': {81615, 81.6}, 'v2': {75246, 75.2}, 'v3': {75.0, 74.9}, 'v10': {53783, 53536, 81615, 81.6}, 'v11': {1.87, 2.39},
       'v12': {1757, 50344, 48554}, 'v22': {81615, 81.6}, 'v20': {60.4}, 'v6': {60.4}}
MAY_DEBATABLE = {'v20': {75246, 75.2, 14.8}}
AUGUST = {'v1': {96221, 96.2, 177837}, 'v2': {89023, 89.0, 164269}, 'v3': {75.0}, 'v9': {108.5, 105.0, 3.5, 56, 36, 20},
          'v10': {63956, 63734, 96221, 96.2, 117270, 117739, 177837}, 'v11': {2.22, 2.46, 4.09, 4.85}, 'v12': {2677, 4434, 24077, 21341, 74421, 69895}, 'v22': {96221, 96.2, 177837}}
EXPECTED = {'2026-05-20': ('v1', 'v2', 'v3', 'v10', 'v11', 'v12', 'v22'), '2026-08-26': ('v1', 'v2', 'v3', 'v9', 'v10', 'v11', 'v12', 'v22')}
# the same quantity for another period (next quarter's guidance, the previous and the year-ago quarters): kept with its own label it is
# "another period, labelled", never wrong
MAY_OTHER = {'v1': {91.0, 68127, 44062}, 'v2': {62314, 39112}, 'v3': {75.1, 60.8, 75.0, 60.5}, 'v10': {44474, 21801, 44299, 21638, 68127, 44062},
             'v11': {1.59, 0.78, 1.76, 0.76}, 'v12': {1284, 1227}, 'v22': {91.0, 68127, 44062}}
AUGUST_OTHER = {'v1': {81615, 46743, 90805}, 'v2': {75246, 41096}, 'v3': {72.5, 72.4, 74.9, 74.0}, 'v10': {53783, 53536, 81615, 28541, 28440, 46743, 50078, 50341, 90805},
                'v11': {1.87, 2.39, 1.01, 1.08}, 'v12': {1757, 1894, 3122}, 'v22': {81615, 46743, 90805}}
DATED = re.compile(r'July 26|Jul\.? 26|August 2026|SB Energy', re.I)    # a balance or exposure stated as of the quarter's end or at the report
READINGS = [('pilot (2nd version, release only)', 'baseline-read.json', 2), ('round 13 (2nd version)', 'baseline-all-reading.json', 2),
            ('3rd version trial', 'baseline-v3-pilot-reading.json', 3), ('3rd version registered', 'baseline-v3-reading.json', 3),
            ('4th version trial', 'baseline-v4-trial-reading.json', 4), ('4th version May', 'baseline-v4-reading.json', 4),
            ('4th version August (held out)', 'baseline-v4-heldout-reading.json', 4)]


def latest(day, text):
    return brm.first_quarter_fy27(text) if day == '2026-05-20' else (quarter_label(text) or half_label(text) or bool(DATED.search(text)))


def forms(value):
    """How a key value can be printed: 81615 -> 81,615; 81.6 -> 81.6; 1.87 -> 1.87; 108.5 -> 108.5."""
    if float(value).is_integer() and value >= 1000:
        return {f'{int(value):,}'}
    return {f'{value:.1f}', f'{value:.2f}', f'{value:g}'}


def states(text, view_id, day):
    """Whether the item's text prints one of the question's key figures (else an empty read of it is right)."""
    key = (MAY if day == '2026-05-20' else AUGUST).get(view_id, set())
    return any(re.search(r'(?<![\d.,])' + re.escape(form) + r'(?![\d,]|\.\d)', text) for value in key for form in forms(value))


def class_of(day, view_id, f):
    key = (MAY if day == '2026-05-20' else AUGUST).get(view_id, set())
    debatable = MAY_DEBATABLE.get(view_id, set()) if day == '2026-05-20' else set()
    values = set(br.numbers(f['value']))
    label = f['period'] + ' ' + f['one_line']
    if not values:
        return 'not a figure'
    other = (MAY_OTHER if day == '2026-05-20' else AUGUST_OTHER).get(view_id, set())
    if values & key and latest(day, label):
        return 'right'
    if values & (key | other):
        return 'another period, labelled' if not latest(day, label) else 'MISREAD'
    if values & debatable:
        return 'DEBATABLE'
    return 'WRONG'


def main():
    pages = sqlite3.connect(f'file:{br.PAGES}?mode=ro', uri=True)
    pilot_text = pages.execute('select text from items where input_id=?', (br.RELEASE,)).fetchone()[0]
    texts = {}
    grand = {}
    for name, path, version in READINGS:
        data = json.load(open(f'{HERE}/{path}'))
        if path == 'baseline-read.json':      # the pilot: release only, re-checked with the current check
            day, report = '2026-05-20', [br.RELEASE]
            results = {v: {br.RELEASE: [{'figures': br.kept_figures({'figures': [{k: f[k] for k in ('quote', 'value', 'unit', 'period', 'basis', 'one_line')}
                                                                                for f in r['figures']]}, pilot_text)} for r in sends]}
                       for v, sends in data['results'].items()}
        else:
            day, report, results = data['report_day'], data['report'], data['results']
        for input_id in report:
            texts.setdefault(input_id, pages.execute('select text from items where input_id=?', (input_id,)).fetchone()[0])
        counts = {}
        rows = []
        for view_id in sorted(results, key=lambda v: int(v[1:])):
            for input_id in report:
                for n, r in enumerate(results[view_id].get(input_id, [])):
                    item = input_id.rsplit(':', 1)[-1][:10]
                    kept = [f for f in r['figures'] if f['kept']]
                    for f in r['figures']:
                        c = class_of(day, view_id, f)
                        if f['kept']:
                            tag = {'right': 'kept right', 'another period, labelled': 'kept, another period labelled', 'WRONG': 'kept WRONG',
                                   'DEBATABLE': 'kept DEBATABLE', 'not a figure': 'kept WRONG', 'MISREAD': 'kept MISREAD'}[c]
                        else:
                            tag = 'refused but RIGHT' if c in ('right', 'another period, labelled') else 'refused, wrong or not a figure'
                        counts[tag] = counts.get(tag, 0) + 1
                        if tag not in ('kept right', 'refused, wrong or not a figure'):
                            why = '' if f['kept'] else f' (in report {f["in_report"]}, value in quote {f["value_in_quote"]})'
                            rows.append(f'  {tag:30} {view_id:4} {item} send {n}: {f["value"]!r} | {f["period"][:36]!r} | {f["quote"][:80]!r}{why}')
                    if view_id in EXPECTED[day] and states(texts[input_id], view_id, day) and not any(class_of(day, view_id, f) == 'right' for f in kept):
                        tag = 'MISSED (model returned none)' if not r['figures'] else 'MISSED (none kept right)'
                        counts[tag] = counts.get(tag, 0) + 1
                        rows.append(f'  {tag:30} {view_id:4} {item} send {n}: wrote {[(f["value"], f["kept"]) for f in r["figures"]]}')
                    elif view_id not in EXPECTED[day] and not kept:
                        counts['empty and right'] = counts.get('empty and right', 0) + 1
        reads = sum(len(results[v].get(i, [])) for v in results for i in report)
        print(f'===== {name}: {reads} item reads; ' + '; '.join(f'{k} {v}' for k, v in sorted(counts.items())))
        for row in rows:
            print(row)
        grand[name] = counts
    print('\n===== by version (item reads)')
    for name, counts in grand.items():
        print(f'{name:34} ' + ' | '.join(f'{k} {counts.get(k, 0)}' for k in ('kept right', 'kept WRONG', 'kept MISREAD', 'kept DEBATABLE', 'refused but RIGHT',
                                                                          'MISSED (model returned none)', 'MISSED (none kept right)', 'kept, another period labelled')))


if __name__ == '__main__':
    main()
