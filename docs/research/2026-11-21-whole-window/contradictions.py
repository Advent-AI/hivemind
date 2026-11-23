"""The primary line P of the paid comparison (PAID-DESIGN.md §4): per store, for each calendar date from the link day to the window's
end on which both the Data Center question and the total revenue question (FY2027) hold a conclusion, compare their annual forecasts.

Each question's conclusion on a date is its last accepted judgement on or before that date (carried forward). Its annual forecast is
an amount or range in its `implied_outcome` between $200B and $1,000B, chosen by `annual` (the last one followed by "FY2027", else one
opening the text, else the last one): a range ("$400–410B", "$390 billion to $395 billion") gives its low and high ends; a single
amount gives both. A date is
  definite:  the segment's low end exceeds the company's high end (the part above the whole whatever the range);
  overlap:   the two ranges share some value without the part being wholly above (reported, not counted as a contradiction);
  clear:     the segment's high end is at or below the company's low end;
  ambiguous: either forecast fell to the last-amount rule with several distinct amounts (reported, read by hand);
  unparsed:  either forecast has no amount in that band.
Coverage = parsed dates / dates with both conclusions.

  python3 contradictions.py <views.sqlite> [<dc view> <total view>] [--from 2026-07-10] [--rows]
"""
import re
import sqlite3
import sys

UNIT = r'(?:B\b|bn\b|billion\b)'
NUMBER = r'(\d{1,4}(?:,\d{3})*(?:\.\d+)?)'
RANGE = re.compile(r'\$\s?' + NUMBER + r'\s?' + UNIT + r'?\s?(?:–|—|-|to)\s?\$?\s?' + NUMBER + r'\s?' + UNIT, re.I)
SINGLE = re.compile(r'\$\s?' + NUMBER + r'\s?' + UNIT, re.I)
BAND = (200.0, 1000.0)


def value(text):
    return float(text.replace(',', ''))


YEAR = re.compile(r'^[^.;$]{0,30}?\b(?:for |in )?(?:FY ?2027|fiscal 2027|fiscal year 2027)', re.I)
LEADING = 30


def amounts(text):
    """Every amount or range in the band: [(start, end, (low, high))], ranges taking precedence over the amounts inside them."""
    found = []
    for match in RANGE.finditer(text or ''):
        low, high = value(match.group(1)), value(match.group(2))
        if BAND[0] <= low <= BAND[1] and BAND[0] <= high <= BAND[1] and low <= high:
            found.append((match.start(), match.end(), (low, high)))
    for match in SINGLE.finditer(text or ''):
        amount = value(match.group(1))
        if BAND[0] <= amount <= BAND[1] and not any(start <= match.start() < end for start, end, _ in found):
            found.append((match.start(), match.end(), (amount, amount)))
    return sorted(found)


def annual(text):
    """(low, high, how) of the annual forecast, or None: the last amount followed within 30 characters by "FY2027" (or "fiscal
    2027"); else an amount opening the text (within its first 30 characters); else the last amount, marked ambiguous when the text
    holds more than one distinct amount in the band."""
    found = amounts(text)
    if not found:
        return None
    named = [f for f in found if YEAR.match(text[f[1]:])]
    if named:
        return (*named[-1][2], 'year')
    if found[0][0] <= LEADING:
        return (*found[0][2], 'leading')
    return (*found[-1][2], 'last' if len({f[2] for f in found}) == 1 else 'ambiguous')


def classify(segment, company):
    if segment is None or company is None:
        return 'unparsed'
    if 'ambiguous' in (segment[2], company[2]):
        return 'ambiguous'
    if segment[0] > company[1]:
        return 'definite'
    if segment[1] <= company[0]:
        return 'clear'
    return 'overlap'


def pair(conn):
    """The FY2027 Data Center and total revenue questions of a store, by their typed keys."""
    keys = conn.execute('select view_id, measure, scope, period_start from view_keys').fetchall()
    segment = [k[0] for k in keys if k[1] == 'segment_revenue' and 'data center' in (k[2] or '').lower() and k[3] == '2026-02-01']
    company = [k[0] for k in keys if k[1] == 'total_revenue' and k[3] == '2026-02-01']
    return (segment[0] if segment else None), (company[0] if company else None)


def daily(conn, segment_view, company_view, from_day='2026-07-10', until_day='2026-09-20'):
    """[(date, class, segment range, company range, segment text, company text)] for every calendar date in the span on which both
    questions hold a conclusion."""
    import datetime
    rows = {}
    for view_id in (segment_view, company_view):
        rows[view_id] = conn.execute('select publication_day, implied_outcome from judgements where view_id=? order by judgement_id',
                                     (view_id,)).fetchall()
    out = []
    day = datetime.date.fromisoformat(from_day)
    end = datetime.date.fromisoformat(until_day)
    while day <= end:
        iso = day.isoformat()
        latest = {}
        for view_id, judgements in rows.items():
            held = [text for published, text in judgements if published <= iso]
            latest[view_id] = held[-1] if held else None
        if latest[segment_view] is not None and latest[company_view] is not None:
            segment, company = annual(latest[segment_view]), annual(latest[company_view])
            out.append((iso, classify(segment, company), segment, company, latest[segment_view], latest[company_view]))
        day += datetime.timedelta(days=1)
    return out


def summary(rows):
    counts = {name: sum(1 for r in rows if r[1] == name) for name in ('definite', 'overlap', 'clear', 'ambiguous', 'unparsed')}
    counts['dates'] = len(rows)
    counts['coverage'] = round((len(rows) - counts['unparsed'] - counts['ambiguous']) / len(rows), 3) if rows else 0.0
    return counts


def main(argv):
    path = argv[0]
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    positional = [a for a in argv[1:] if not a.startswith('--')]
    segment_view, company_view = positional[:2] if len(positional) >= 2 else pair(conn)
    from_day = argv[argv.index('--from') + 1] if '--from' in argv else '2026-07-10'
    rows = daily(conn, segment_view, company_view, from_day)
    print(path, segment_view, company_view, summary(rows))
    if '--rows' in argv:
        for row in rows:
            print(row[0], row[1], row[2], row[3], '|', (row[4] or '')[:100].replace('\n', ' '), '||', (row[5] or '')[:100].replace('\n', ' '))


if __name__ == '__main__':
    main(sys.argv[1:])
