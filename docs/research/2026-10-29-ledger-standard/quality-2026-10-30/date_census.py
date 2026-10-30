"""Census of the report-day defect (standard 5.4: an unknown original day is written unknown, never the report day, D220):
records whose original_day equals the publication day while the quote itself places the statement or event earlier
(an earlier month name, "last year", "earlier this month", "last week", "in Q1", "announced in"...). A lower bound: a quote
that carries no time word is not counted, and every flagged record is printed for reading.

    python3 date_census.py
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_gold as sg  # noqa: E402

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
EARLIER = re.compile(r"\b(last (year|month|week|quarter|fall|spring|summer|winter)|earlier this (year|month|week)|previously|"
                     r"in (19|20)\d\d|(19|20)\d\d\b|yesterday|ago\b|back in)\b", re.I)


def earlier_month(quote, pub):
    month = int(pub[5:7])
    for i, name in enumerate(MONTHS, start=1):
        if re.search(rf'\b{name}\b', quote, re.I) and i < month and not re.search(rf'\b{name}\s+(19|20)\d\d', quote, re.I):
            return name
    return None


def main():
    dev = json.load(open(HERE.parent / 'golden-v3/golden-v3-signed.json'))['articles']
    test = json.load(open(HERE.parent / 'test-set/golden-test-signed.json'))['articles']
    total = same_day = flagged = 0
    rows = []
    for a in dev + test:
        pub = a.get('publication_day') or ''
        for d in (1, 2, 3):
            s = sg.kept(sg.answers(f'P-v51-d{d}').get(a['input_id']), a['input_id'])
            for e in s['evidence']:
                total += 1
                if e.get('original_day') != pub:
                    continue
                same_day += 1
                q = e['quote']
                hit = earlier_month(q, pub)
                m = EARLIER.search(q)
                years = [y for y in re.findall(r'\b((?:19|20)\d\d)\b', q) if y < pub[:4]]
                if hit or (m and (not m.group(0)[-4:].isdigit() or years)):
                    flagged += 1
                    rows.append({'draw': d, 'input_id': a['input_id'], 'pub': pub, 'why': hit or m.group(0), 'quote': q[:240]})
    print(json.dumps({'statements': total, 'original_day = publication day': same_day, 'of which the quote places it earlier': flagged}, indent=1))
    (HERE / 'date-census.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1) + '\n')
    for r in rows[:40]:
        print(r['draw'], r['input_id'][:30], r['pub'], '|', r['why'], '|', r['quote'][:170])


if __name__ == '__main__':
    main()
