"""Ruling-anchored checks of a probe (no model calls): Alex's four rulings (LOG §11) applied to their matching contexts, plus guards.
Keyword matching only finds the candidate items; every flagged item is printed for reading, and the reading decides.

  margin   (d1-40, d1-57): a kept gross-margin statement linked to an open thesis, and no separate margin thesis opened
  eps      (d1-66, d2-66): the analysts' EPS forecast kept and linked; the author's target price not kept
  cash     (d1-57, d1-62): operating or free cash flow and cash-balance statements not kept
  supplier (d2-8): no new thesis about cooling or supply
  guards   (d1-22, d1-29, d1-113, empty-108): no new theses

Usage: ruling_checks.py <records.json> [arm,...]"""
import collections, json, re, sys

MARGIN = re.compile(r'gross margin', re.I)
EPS = re.compile(r'\bEPS\b|earnings per share', re.I)
TARGET = re.compile(r'price target|target price|worth roughly|\$3\d\d per share|multiple of|times (forward )?earnings', re.I)
CASH = re.compile(r'free cash flow|operating cash flow|cash flow|cash balance|cash and (cash equivalents|marketable)', re.I)
SUPPLY = re.compile(r'cool|suppl|thermal', re.I)


def main():
    records = json.loads(open(sys.argv[1]).read())
    arms = sys.argv[2].split(',') if len(sys.argv) > 2 else sorted({r['arm'] for r in records})
    score = collections.defaultdict(collections.Counter)
    for r in records:
        if r['arm'] not in arms:
            continue
        a = score[r['arm']]
        if 'kept' not in r:
            a['failed answers'] += 1
            continue
        case, kept, new = r['case'], r['kept'], r['new_theses']
        if case in ('d1-40', 'd1-57'):
            linked = [ev for ev in kept if MARGIN.search(ev['summary']) and ev['links']]
            margin_thesis = [t for t in new if MARGIN.search(t['description'])]
            a['margin conformant'] += bool(linked) and not margin_thesis
            a['margin answers'] += 1
        if case in ('d1-66', 'd2-66'):
            eps_kept = [ev for ev in kept if EPS.search(ev['summary']) and ev['links'] and not TARGET.search(ev['summary'])]
            target_kept = [ev for ev in kept if TARGET.search(ev['summary'])]
            a['eps conformant'] += bool(eps_kept) and not target_kept
            a['eps answers'] += 1
        if case in ('d1-57', 'd1-62'):
            a['cash conformant'] += not [ev for ev in kept if CASH.search(ev['summary'])]
            a['cash answers'] += 1
        if case == 'd2-8':
            a['supplier conformant'] += not [t for t in new if SUPPLY.search(t['description'])]
            a['supplier answers'] += 1
        if case in ('d1-22', 'd1-29', 'd1-113', 'empty-108'):
            a['guard new theses'] += len(new)
        if case.startswith('empty-') and case != 'empty-108':
            a['empty-state theses'] += len(new)
            a['empty-state margin or cash theses'] += len([t for t in new if MARGIN.search(t['description']) or CASH.search(t['description'])])
    for arm in arms:
        a = score[arm]
        total = sum(a[f'{k} conformant'] for k in ('margin', 'eps', 'cash', 'supplier'))
        print(f"{arm:5s} rulings held {total}/{sum(a[f'{k} answers'] for k in ('margin', 'eps', 'cash', 'supplier'))} "
              f"(margin {a['margin conformant']}/{a['margin answers']}, eps {a['eps conformant']}/{a['eps answers']}, cash {a['cash conformant']}/{a['cash answers']}, "
              f"supplier {a['supplier conformant']}/{a['supplier answers']}) | guard new theses {a['guard new theses']} | empty-state theses {a['empty-state theses']} "
              f"(margin or cash {a['empty-state margin or cash theses']}) | failed {a['failed answers']}")


if __name__ == '__main__':
    main()
