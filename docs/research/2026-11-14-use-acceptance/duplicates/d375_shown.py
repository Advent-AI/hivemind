"""The D375 proof, the missing list checks (council round 18, point 1; $0). Fails (exit 1) on any breach.

1. What is shown, not only which questions: for every article read in the four stored runs, each question on the per-article list
   (production `extraction.shown_views`, the store read at the article's sequence minus one) must carry the groups, the groups'
   other names and the parent questions it had at that sequence. These are derived here independently, from the tables read with
   this script's own queries (members, groups, added names, dependencies), never through the store's functions.
2. Case D1, a same-day closure (synthetic): on a scratch copy of a rebuilt store, one question open at the day's start is closed
   before the tested article; the per-article list must drop it while the day-start list still holds it.

  python3 d375_shown.py <rebuilt scratch folder for case D1>
"""
import collections
import json
import shutil
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


def list_at(conn, cfg, item, objects, sequence):
    original = store.day_start_seq
    store.day_start_seq = lambda connection, publication_day: sequence
    try:
        return extraction.shown_views(conn, cfg, item, objects)
    finally:
        store.day_start_seq = original


def main():
    cfg, uni = config.load(str(ROOT / 'poc/config/poc-v118.json')), universe.load(str(ROOT / 'poc/universe.json'))
    items_db = testdb.open_db(str(DATA / 'items-nvda-2026-07-01-10-27.sqlite'))
    failures = []
    for name, folder in RUNS.items():
        conn = store.open_read_only(str(folder / 'views.sqlite'))
        raw = sqlite3.connect(f"file:{folder / 'views.sqlite'}?mode=ro", uri=True)
        members = raw.execute('select id, group_id, view_id, seq from thesis_group_members order by id').fetchall()
        groups = {row[0]: row for row in raw.execute('select group_id, name, scope, aliases from thesis_groups')}
        added = raw.execute('select id, group_id, alias, seq from thesis_group_aliases order by id').fetchall()
        dependencies = raw.execute("select dependency_id, view_id, depends_on, seq from dependencies where depends_on != '' order by dependency_id").fetchall()
        counts = collections.Counter()
        for day in [row[1] for row in raw.execute('select * from days_completed order by 1')]:
            for item in testdb.feed(items_db, day, day):
                sequence = raw.execute("select max(sequence_no) from processing_steps where input_id = ? and step = 'extracted'", (item['input_id'],)).fetchone()[0]
                if not sequence:
                    continue
                objects = [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
                counts['articles'] += 1
                for shown in list_at(conn, cfg, item, objects, sequence - 1):
                    counts['questions shown'] += 1
                    expected_groups = []
                    for _, group_id, view_id, member_seq in members:
                        if view_id == shown['view_id'] and member_seq <= sequence - 1:
                            _, group_name, scope, creation = groups[group_id]
                            names = list(json.loads(creation or '[]')) + [alias for _, g, alias, alias_seq in added if g == group_id and alias_seq <= sequence - 1]
                            expected_groups.append({'name': group_name, 'scope': scope, 'aliases': names})
                    expected_parents = list(dict.fromkeys(parent for _, view_id, parent, dependency_seq in dependencies if view_id == shown['view_id'] and dependency_seq <= sequence - 1))
                    counts['with a group'] += bool(expected_groups)
                    counts['with a parent'] += bool(expected_parents)
                    if shown['groups'] != expected_groups:
                        failures.append((name, sequence, shown['view_id'], 'groups or other names differ', shown['groups'], expected_groups))
                    if shown['parents'] != expected_parents:
                        failures.append((name, sequence, shown['view_id'], 'parents differ', shown['parents'], expected_parents))
        print(f"{name}: {dict(counts)}; breaches so far {len(failures)}")
    # case D1: a synthetic same-day closure
    scratch = Path(sys.argv[1])
    work = scratch.parent / (scratch.name + '-closure')
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(scratch, work)
    conn = store.open_db(str(work / 'views.sqlite'))
    day, article = '2026-09-27', 'gnews:2e603d9182199771803bce9b'
    item = next(i for i in testdb.feed(items_db, day, day) if i['input_id'] == article)
    objects = [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
    day_start = conn.execute('select max(seq) from days_completed where day < ?', (day,)).fetchone()[0]
    before_closure = [v['view_id'] for v in list_at(conn, cfg, item, objects, 174)]
    closed = 'v13'
    conn.execute("insert into view_switches (view_id, open, reason, by_whom, after_seq) values (?, 0, 'synthetic closure for the D375 proof (case D1)', 'proof', ?)", (closed, day_start + 5))
    conn.commit()
    at_start = [v['view_id'] for v in extraction.shown_views(conn, cfg, item, objects)]
    before_article = [v['view_id'] for v in list_at(conn, cfg, item, objects, 174)]
    print(f"case D1: {closed} closed at sequence {day_start + 5} (the day starts after {day_start}; the article is 175). On the day-start list: {closed in at_start}; "
          f"on the per-article list before the closure: {closed in before_closure}, after it: {closed in before_article}; the rest of the per-article list unchanged: "
          f"{[v for v in before_closure if v != closed] == before_article}")
    if not (closed in at_start and closed in before_closure and closed not in before_article and [v for v in before_closure if v != closed] == before_article):
        failures.append(('case D1', 175, closed, 'the closed question is not handled as required', at_start, before_article))
    for failure in failures[:8]:
        print('BREACH:', str(failure)[:500])
    print('RESULT:', 'no breach' if not failures else f'{len(failures)} breaches')
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
