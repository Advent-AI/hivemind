"""Step 1's decision (baseline-design.md, round 4): per send, whether v10 and v12 each received the first-quarter FY2027 figure in the STORED quote
with a one-line tied to the quarter ended 2026-04-26, the basis (GAAP or non-GAAP), wrong-column figures, and refused v10/v12 items read from
the raw answer. Delivered in at least 2 of 3 sends passes.

usage: python3 baseline_measure.py baseline-extract.json
"""
import json
import re
import sys

Q1 = re.compile(r'first quarter|Q1 FY ?2027|Q1 fiscal 2027|April 26, 2026|2026-04-26|quarter ended April 26', re.I)
FIGURES = {'v10': {'53,536': 'GAAP operating income', '53,783': 'non-GAAP operating income', '65.6': 'GAAP operating margin'},
           'v12': {'1,757': 'purchases related to property and equipment'}}
WRONG = {'v10': ('44,299', '44,474', '21,638', '21,801'), 'v12': ('1,284', '1,227')}


def main():
    data = json.load(open(sys.argv[1]))
    delivered = {'v10': 0, 'v12': 0}
    for n, r in enumerate(data['sends']):
        print(f'--- send {n}')
        for q in ('v10', 'v12'):
            hits = []
            for s in r['kept']:
                if q not in s['links']:
                    continue
                figure = next((name for fig, name in FIGURES[q].items() if fig in s['quote']), None)
                wrong = [w for w in WRONG[q] if w in s['quote'] or w in s.get('one_line', '')]
                tied = bool(Q1.search(s.get('one_line', '')))
                hits.append((figure, tied, wrong, s['quote'][:120].replace('\n', ' / '), s.get('one_line', '')[:140]))
            ok = any(f and t and not w for f, t, w, _, _ in hits)
            delivered[q] += ok
            print(f'  {q}: {"DELIVERED" if ok else "not delivered"}')
            for f, t, w, quote, one_line in hits:
                print(f'     figure in quote: {f or "none"} | one-line tied to Q1 FY27: {t} | wrong column: {w or "-"}\n       quote: {quote}\n       one-line: {one_line}')
            refused_ids = {d[0] for d in r['dropped'] if 'quote not in item' in d[1]}
            for e in r['raw']:
                if e['id'] in refused_ids and q in e['links']:
                    print(f'     REFUSED by the quote check: {e["quote"][:120]!r} | {e["one_line"][:120]}')
    print(f'\nstep 1: v10 delivered {delivered["v10"]}/3, v12 delivered {delivered["v12"]}/3 -> '
          f'{"pass" if delivered["v10"] >= 2 and delivered["v12"] >= 2 else "FAIL"} (both need at least 2 of 3)')


if __name__ == '__main__':
    main()
