"""Where the filed statements go ($0, finished run folders): links per question, the share on the three company-wide revenue questions
(v1 FY2027 total revenue, v2 FY2027 Data Center revenue, v22 FY2028 total revenue: D207's sink guard, ≤25% in arm 3), statements with
more than one open-question link, and a sample of the gold not-kept statements that reached the ledger with the questions they sit
under (the noise read of AGENTS §7.2). The gold is golden-v5 through score_ref.

    python3 links_by_question.py <run folder> [<run folder> ...] [--sample N]
"""
import argparse
import collections
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / 'docs/research/2026-10-31-reference-context'), str(ROOT / 'src')]
import score_ref as sr  # noqa: E402

SINK = ('v1', 'v2', 'v22')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('runs', nargs='+'); ap.add_argument('--sample', type=int, default=20)
    args = ap.parse_args()
    for run in args.runs:
        v = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); v.row_factory = sqlite3.Row
        looks = {r['view_id']: r['looks_at'][:40] for r in v.execute('select view_id, looks_at from views')}
        links = collections.Counter(r[0] for r in v.execute('select view_id from evidence_links'))
        per_piece = collections.Counter(r[0] for r in v.execute('select evidence_id from evidence_links'))
        total = sum(links.values()); sink = sum(links[k] for k in SINK)
        multi = sum(1 for n in per_piece.values() if n > 1)
        both_revenue = v.execute("select count(*) from (select evidence_id from evidence_links where view_id in ('v1','v2') group by evidence_id having count(distinct view_id) = 2)").fetchone()[0]
        print(f'\n== {run}')
        print(f'   links {total} on {len(per_piece)} filed statements; on v1/v2/v22 {sink} ({sink / max(1, total):.0%}); statements with >1 question {multi} '
              f'({multi / max(1, len(per_piece)):.0%}); under both v1 and v2 {both_revenue}')
        print('   top questions: ' + ', '.join(f'{k} {looks.get(k, "?")} {n}' for k, n in links.most_common(8)))
        replaced = {r[0] for r in v.execute('select old_evidence_id from replacements')}
        noise = []
        for a in sr.articles:
            for e in v.execute('select evidence_id, quote from evidence where created_from_input=?', (a['input_id'],)):
                if e['evidence_id'] in replaced:
                    continue
                if any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'not_kept'):
                    lk = [r[0] for r in v.execute('select view_id from evidence_links where evidence_id=? order by id', (e['evidence_id'],))]
                    noise.append((a['title'][:40], lk, e['quote'][:110]))
        on_sink = sum(1 for _, lk, _ in noise if any(l in SINK for l in lk))
        print(f'   gold not-kept statements in the ledger: {len(noise)}, of them under a revenue question {on_sink}')
        for title, lk, quote in noise[:args.sample]:
            print(f'   noise -> {lk} | {title} | {quote}')


if __name__ == '__main__':
    main()
