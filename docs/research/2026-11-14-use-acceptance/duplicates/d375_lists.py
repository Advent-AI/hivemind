"""Cases D and E of the D375 proof ($0; D375-PROOF-DESIGN.md): the per-article list of open questions against the day-start list, over
every article the old system read in its stored runs. The lists are built by the production code (`extraction.shown_views`) on the
stored store; for the per-article list `store.day_start_seq` is answered with the article's sequence minus one. Read-only.

D (boundaries), per article: the per-article list equals the questions of the article's subjects and every theme with a creation
sequence below the article's own that are open at that sequence; it contains the day-start list; it equals it for the first article
of a day; it holds no question created at or after the article.
E (cases touched), per run: articles whose list gains a question; questions opened whose comparison (the stored matching record) did
not include a question the per-article list would have added.

  python3 d375_lists.py
"""
import collections
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, extraction, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

DATA = ROOT / 'poc/data'
RUNS = {'fresh week p1': DATA / 'clean-lean-week-2026-11-14/week/p1/prod', 'July p1': DATA / 'clean-e2e-full-2026-11-13/p1/prod',
        'July p2': DATA / 'clean-e2e-full-2026-11-13/p2/prod', 'July p3': DATA / 'clean-e2e-full-2026-11-13/p3/prod'}
HERE = Path(__file__).resolve().parent


def main():
    cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    items_db = testdb.open_db(str(DATA / 'items-nvda-2026-07-01-10-27.sqlite'))
    report = []
    for name, folder in RUNS.items():
        conn = store.open_read_only(str(folder / 'views.sqlite'))
        days = [row[1] for row in conn.execute('select * from days_completed order by 1')]
        created = {row['view_id']: row for row in conn.execute('select view_id, created_seq, created_from_input, object_id, kind from views')}
        counts, breaches, gains, uncompared = collections.Counter(), [], [], []
        for day in days:
            first_of_day = True
            read = sorted(((conn.execute('select max(sequence_no) from processing_steps where input_id = ?', (item['input_id'],)).fetchone()[0] or 0, item)
                           for item in testdb.feed(items_db, day, day)), key=lambda pair: pair[0])
            for seq, item in read:
                if not seq or not conn.execute("select 1 from processing_steps where input_id = ? and step = 'extracted'", (item['input_id'],)).fetchone():
                    continue
                objects = [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
                at_start = [v['view_id'] for v in extraction.shown_views(conn, cfg, item, objects)]
                original = store.day_start_seq
                store.day_start_seq = lambda connection, publication_day, seq=seq: seq - 1
                try:
                    before = [v['view_id'] for v in extraction.shown_views(conn, cfg, item, objects)]
                finally:
                    store.day_start_seq = original
                counts['articles read'] += 1
                expected = []
                for view_id, row in created.items():
                    if row['created_seq'] > seq - 1 or (row['kind'] != 'theme' and row['object_id'] not in objects):
                        continue
                    switch = conn.execute('select open from view_switches where view_id = ? and after_seq <= ? order by id desc limit 1', (view_id, seq - 1)).fetchone()
                    if switch and switch['open']:
                        expected.append(view_id)
                problems = []
                if sorted(before) != sorted(expected):
                    problems.append('not the questions committed and open before the article')
                if not set(at_start) <= set(before):
                    problems.append('loses a day-start question')
                if any(created[v]['created_seq'] >= seq for v in before):
                    problems.append('holds a question created at or after the article')
                if first_of_day and before != at_start:
                    problems.append('differs from the day-start list for the first article of the day')
                if problems:
                    breaches.append((day, seq, problems))
                first_of_day = False
                added = [v for v in before if v not in at_start]
                if added:
                    counts['articles whose list gains a question'] += 1
                    gains.append(len(added))
                opened_here = [v for v, row in created.items() if row['created_from_input'] == item['input_id']]
                if opened_here and added:
                    compared = set()
                    for decisions, in conn.execute('select decisions_json from match_records where input_id = ? order by id', (item['input_id'],)):
                        for candidate in json.loads(decisions).get('candidates') or []:
                            if candidate.get('outcome') == 'new':
                                compared |= set(re.findall(r'(v\d+):', (candidate.get('reason') or '').split('groups joined')[0]))
                    missing = [v for v in added if v not in compared]
                    counts['articles that opened a question and whose list gains one'] += 1
                    if missing:
                        counts['of those, a gained question was not among the compared'] += 1
                        uncompared.append({'article': seq, 'day': day, 'opened': opened_here, 'gained_and_not_compared': missing})
        print(f"\n{name}: {dict(counts)}; questions gained per touched article: {dict(collections.Counter(gains))}")
        print(f"   boundary breaches (case D): {len(breaches)}" + ''.join(f'\n      {b}' for b in breaches[:5]))
        for row in uncompared:
            print(f"   article {row['article']} ({row['day']}) opened {row['opened']}; the list would add, and the comparison did not include: {row['gained_and_not_compared']}")
        report.append({'run': name, 'counts': dict(counts), 'boundary_breaches': breaches, 'opened_without_comparing_a_gained_question': uncompared})
    (HERE / 'd375-lists.json').write_text(json.dumps(report, indent=1, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
