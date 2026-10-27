"""Compare two ledgers over the same days: per item, the extraction step's counts (evidence, candidates, dropped) and
whether the answer was empty; per ledger, evidence rows written, theses opened, archive cost. Run:
python3 compare_week.py <ledger A views.sqlite> <archive A> <ledger B views.sqlite> <archive B> <from-day> <until-day>"""
import collections
import re
import sqlite3
import sys


def steps(views, from_day, until_day):
    conn = sqlite3.connect(f'file:{views}?mode=ro', uri=True); conn.row_factory = sqlite3.Row
    out = {}
    for r in conn.execute("select input_id, reason, publication_day from processing_steps where step='extracted' and result='ok' and publication_day between ? and ?", (from_day, until_day)):
        m = re.match(r'(\d+) evidence, (\d+) candidates, (\d+) dropped', r['reason'] or '')
        if m:
            out[r['input_id']] = (int(m.group(1)), int(m.group(2)), int(m.group(3)), r['publication_day'])
    evidence = conn.execute("select count(*) from evidence").fetchone()[0]
    views_n = conn.execute("select count(*) from views").fetchone()[0]
    return out, evidence, views_n


def cost(archive):
    conn = sqlite3.connect(f'file:{archive}?mode=ro', uri=True)
    return {p: (n, round(c or 0, 4)) for p, n, c in conn.execute("select purpose, count(*), sum(cost_usd) from model_calls group by purpose")}


def main(va, aa, vb, ab, from_day, until_day):
    a, ev_a, v_a = steps(va, from_day, until_day); b, ev_b, v_b = steps(vb, from_day, until_day)
    common = sorted(set(a) & set(b))
    print(f'items extracted: A {len(a)}, B {len(b)}, in both {len(common)}')
    for label, d in (('A', a), ('B', b)):
        items = [d[i] for i in common]
        empty = sum(1 for e, c, _, _ in items if e == 0 and c == 0)
        model_empty = sum(1 for e, c, dr, _ in items if e == 0 and c == 0 and dr == 0)
        pieces = sorted(e for e, _, _, _ in items)
        print(f"  {label}: empty {empty}/{len(items)} ({empty/max(1,len(items)):.0%}; model itself {model_empty}) | evidence per item median {pieces[len(pieces)//2]} mean {sum(pieces)/max(1,len(pieces)):.1f} | candidates {sum(c for _, c, _, _ in items)} | dropped {sum(dr for _, _, dr, _ in items)}")
    print(f'  evidence rows in the ledger: A {ev_a}, B {ev_b} (B counts its own run only) | theses: A {v_a} (whole run), B {v_b}')
    by_day = collections.defaultdict(lambda: [0, 0, 0, 0])
    for i in common:
        day = a[i][3]; by_day[day][0] += 1; by_day[day][1] += a[i][0] == 0 and a[i][1] == 0; by_day[day][2] += b[i][0] == 0 and b[i][1] == 0; by_day[day][3] += b[i][0] - a[i][0]
    print('  day | items | empty A | empty B | evidence B minus A')
    for day, (n, ea, eb, diff) in sorted(by_day.items()): print(f'  {day} | {n} | {ea} | {eb} | {diff:+d}')
    print('cost by purpose: B', cost(ab))


if __name__ == '__main__':
    main(*sys.argv[1:7])
