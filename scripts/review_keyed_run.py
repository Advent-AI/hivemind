"""Read a keyed run's views database without model calls (keyed-views-plan.md T2/T4 metrics): the views opened with their
keys and sources, duplicate keys among open views, the review pool (candidates the watch list refused, by object and
measure), the matches the key refused, the watch-list coverage per object, and the cost from the run's archive.

  python3 scripts/review_keyed_run.py --views poc/data/views-2026-10-25-v15-T2.sqlite --archive poc/data/keyed-2026-10-25/archive-T2.sqlite
"""
import argparse
import collections
import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import universe  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--views', required=True)
    parser.add_argument('--archive', required=True)
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    args = parser.parse_args()
    conn = sqlite3.connect(args.views); conn.row_factory = sqlite3.Row
    uni = universe.load(args.universe)
    views = [dict(r) for r in conn.execute('select v.*, k.measure, k.scope, k.scope_key, k.period_start, k.period_end, k.basis, k.unit, k.event_type from views v left join view_keys k on k.view_id=v.view_id order by v.rowid')]
    open_ids = {r[0] for r in conn.execute('select view_id from view_switches where id in (select max(id) from view_switches group by view_id) and open=1')}
    print(f'views {len(views)} ({len(open_ids)} open); keyed {sum(1 for v in views if v["measure"])}')
    for v in views:
        print(f"  {v['view_id']:4s} {v['object_id']:14s} {str(v['measure']):22s} [{str(v['scope'] or '')[:22]:22s}] {v['period_start'] or '':10s}..{v['period_end'] or '':10s} {str(v['basis']):8s} | {v['looks_at'][:46]:46s} ← {v['created_from_input'][:40]}")
    groups = collections.defaultdict(list)
    for v in views:
        if v['measure'] and v['view_id'] in open_ids:
            groups[(v['object_id'], v['measure'], v['scope_key'], v['period_start'], v['period_end'], v['basis'], v['unit'])].append(v['view_id'])
    dups = {k: ids for k, ids in groups.items() if len(ids) > 1}
    print(f'\nduplicate keys among open views: {len(dups)} groups ' + ', '.join(f'{k[:3]}→{ids}' for k, ids in dups.items()))
    pool = [dict(r) for r in conn.execute("select * from review_pool_entries where kind='candidate_outside_watch' order by id")]
    by = collections.Counter()
    for e in pool:
        reason = e['key']; by[reason.split(' is not on ')[0].replace('watch: ', '')] += 1
    print(f'\nreview pool (candidates outside the watch list): {len(pool)} entries')
    for key, n in by.most_common(40):
        print(f'  {n:3d}  {key}')
    notes = 0
    for r in conn.execute('select checks_json from match_records'):
        c = json.loads(r['checks_json'] or '{}'); notes += len(c.get('notes') or [])
    print(f'\nmerges the key refused (opened as new views instead): {notes}')
    print('\nwatch-list coverage (objects with at least one item in this run):')
    objects_seen = {r[0] for r in conn.execute('select object_id from views')}
    for obj in sorted(objects_seen):
        entries = uni.watch_list(obj)
        have = [v for v in views if v['object_id'] == obj and v['view_id'] in open_ids and v['measure']]
        covered = sum(1 for e in entries if any(v['measure'] == e['measure'] and (not e.get('scope') or universe.scope_key(e['scope']) == v['scope_key']) and (not e.get('event_type') or e['event_type'] == v['event_type']) for v in have))
        print(f'  {obj:22s} {covered}/{len(entries)} watched quantities have an open view')
    steps = collections.Counter(r[0] for r in conn.execute('select step from processing_steps'))
    dropped = collections.Counter()
    for r in conn.execute("select reason from processing_steps where step='extracted'"):
        pass
    a = sqlite3.connect(args.archive)
    cost = a.execute('select count(*), round(sum(cost_usd), 3), round(sum(seconds), 0) from model_calls').fetchone()
    print(f'\nprocessing steps: {dict(steps)}')
    print(f'model calls {cost[0]}, ${cost[1]}, {cost[2]} s')


if __name__ == '__main__':
    main()
