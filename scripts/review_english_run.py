"""Read an English-library ledger without model calls (D163 build, docs/research/2026-10-25-english/build-log.md): every
closed field in the canonical vocabulary, no Chinese in generated text (quotes are source text and exempt), every view's
year in its canonical spelling, duplicate keys among open views, same-quantity views that differ only by basis, the
review pool, and the cost from the run's archive. Exit status 1 when a check finds a breach.

  python3 scripts/review_english_run.py --views poc/data/english-2026-10-25/views.sqlite --archive poc/data/english-2026-10-25/archive.sqlite
"""
import argparse
import collections
import json
import os
import re
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import universe, vocabulary  # noqa: E402

CJK = re.compile('[一-龥]')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--views', required=True)
    parser.add_argument('--archive', required=True)
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    args = parser.parse_args()
    conn = sqlite3.connect(f'file:{args.views}?mode=ro', uri=True); conn.row_factory = sqlite3.Row
    uni = universe.load(args.universe)
    breaches = []
    views = [dict(r) for r in conn.execute('select v.*, k.measure, k.scope, k.scope_key, k.period_start, k.period_end, k.basis, k.unit, k.event_type, k.scope_source from views v left join view_keys k on k.view_id=v.view_id order by v.rowid')]
    open_ids = {r[0] for r in conn.execute('select view_id from view_switches where id in (select max(id) from view_switches group by view_id) and open=1')}
    print(f'views {len(views)} ({len(open_ids)} open); keyed {sum(1 for v in views if v["measure"])}')
    for v in views:
        rungs = [dict(r) for r in conn.execute('select * from rungs where view_id=? order by position', (v['view_id'],))]
        generated = ' '.join([v['question'], v['looks_at']] + [r['label'] + ' ' + r['condition'] for r in rungs])
        cjk = len(CJK.findall(generated))
        if cjk:
            breaches.append(f'{v["view_id"]}: {cjk} Chinese characters in generated text')
        if v['kind'] not in vocabulary.KINDS:
            breaches.append(f'{v["view_id"]}: kind {v["kind"]!r} not canonical')
        if v['year'] != uni.canonical_year(v['object_id'], v['year']):
            breaches.append(f'{v["view_id"]}: year {v["year"]!r} not canonical ({uni.canonical_year(v["object_id"], v["year"])!r})')
        if len(rungs) == 5 and v['kind'] == 'asset' and [r['label'] for r in rungs] != vocabulary.ASSET_LABELS:
            breaches.append(f'{v["view_id"]}: asset labels {[r["label"] for r in rungs]}')
        if len(rungs) == 2 and v['measure'] not in ('event', 'policy_event', None):
            breaches.append(f'{v["view_id"]}: two-rung ladder on a numeric measure {v["measure"]} (a figure takes five ranges)')
        print(f"  {v['view_id']:4s} {v['object_id']:14s} {str(v['measure']):22s} [{str(v['scope'] or '')[:22]:22s}] {v['period_start'] or '':10s}..{v['period_end'] or '':10s} {str(v['basis']):8s} {str(v['unit']):7s} {v['year']:7s} due {v['due_day']} {len(rungs)}r | {v['looks_at'][:48]:48s} ← {v['created_from_input'][:36]}")
    # evidence: canonical tiers, English one-lines (quotes are source text)
    tiers = collections.Counter(); cjk_lines = 0
    for e in conn.execute('select * from evidence'):
        tiers[e['tier']] += 1
        if CJK.search(e['one_line'] or ''):
            cjk_lines += 1
        if e['tier'] not in vocabulary.TIERS:
            breaches.append(f'{e["evidence_id"]}: tier {e["tier"]!r} not canonical')
    print(f'\nevidence {sum(tiers.values())}: tiers {dict(tiers)}; one-lines with Chinese: {cjk_lines}')
    if cjk_lines:
        breaches.append(f'{cjk_lines} evidence one-lines contain Chinese')
    # judgements: canonical pushes, English reasons
    pushes = collections.Counter(); cjk_reasons = 0; n_j = 0
    for j in conn.execute('select * from judgements'):
        n_j += 1
        if CJK.search(j['reasons'] or '') or CJK.search(j['why_changed'] or ''):
            cjk_reasons += 1
        for p in json.loads(j['pushes_json'] or '[]'):
            pushes[p['push']] += 1
            if p['push'] not in vocabulary.PUSHES:
                breaches.append(f'judgement {j["judgement_id"]}: push {p["push"]!r} not canonical')
    print(f'judgements {n_j}: pushes {dict(pushes)}; reasons with Chinese: {cjk_reasons}')
    if cjk_reasons:
        breaches.append(f'{cjk_reasons} judgements carry Chinese reasons')
    # dependencies: canonical directions, canonical wait years
    directions = collections.Counter()
    for d in conn.execute('select * from dependencies'):
        directions[d['direction']] += 1
        if d['direction'] not in vocabulary.DIRECTIONS:
            breaches.append(f'dependency {d["dependency_id"]}: direction {d["direction"]!r} not canonical')
    print(f'dependencies {sum(directions.values())}: {dict(directions)}; successions {conn.execute("select count(*) from successions").fetchone()[0]}')
    # identity: duplicate keys among open views; same object+measure+scope+period differing only by basis
    groups = collections.defaultdict(list); loose = collections.defaultdict(list)
    for v in views:
        if v['measure'] and v['view_id'] in open_ids:
            groups[(v['object_id'], v['measure'], v['scope_key'], v['period_start'], v['period_end'], v['basis'], v['unit'], v['event_type'])].append(v['view_id'])
            loose[(v['object_id'], v['measure'], v['scope_key'], v['period_start'], v['period_end'], v['unit'], v['event_type'])].append((v['view_id'], v['basis']))
    dups = {k: ids for k, ids in groups.items() if len(ids) > 1}
    basis_only = {k: ids for k, ids in loose.items() if len(ids) > 1 and len({b for _, b in ids}) > 1}
    print(f'\nduplicate keys among open views: {len(dups)} groups ' + ', '.join(f'{k[:3]}→{ids}' for k, ids in dups.items()))
    print(f'open views that differ only by basis: {len(basis_only)} groups ' + ', '.join(f'{k[:3]}→{ids}' for k, ids in basis_only.items()))
    if dups:
        breaches.append(f'{len(dups)} duplicate key groups among open views')
    # research groups (D149): every group with its members, theses without a group, groups spanning objects
    tables = {r[0] for r in conn.execute("select name from sqlite_master where type='table'")}
    if 'thesis_groups' in tables:
        groups = [dict(r) for r in conn.execute('select * from thesis_groups order by rowid')]
        member_rows = [dict(r) for r in conn.execute('select * from thesis_group_members order by id')]
        by_group = collections.defaultdict(list)
        for m in member_rows:
            by_group[m['group_id']].append(m['view_id'])
        grouped_views = {m['view_id'] for m in member_rows}
        view_by_id = {v['view_id']: v for v in views}
        print(f'\nresearch groups {len(groups)}; theses in a group {len(grouped_views)} of {len(views)}; memberships {len(member_rows)}')
        sizes = collections.Counter(len(ids) for ids in by_group.values())
        print(f'  members per group: {dict(sorted(sizes.items()))}; groups spanning several objects: {sum(1 for ids in by_group.values() if len({view_by_id[v]["object_id"] for v in ids if v in view_by_id}) > 1)}')
        for g in groups:
            ids = by_group.get(g['group_id'], [])
            aliases = json.loads(g.get('aliases') or '[]') if 'aliases' in g else []
            print(f'  {g["group_id"]:4s} "{g["name"]}" — {g["scope"][:90]}' + (f'  aliases {aliases}' if aliases else ''))
            basis_of = {m['view_id']: m.get('basis') for m in member_rows if m['group_id'] == g['group_id']}
            for v in ids:
                vv = view_by_id.get(v)
                print(f'        {v:4s} {vv["object_id"] if vv else "?":12s} {(vv["looks_at"] if vv else "?")[:66]:66s} {basis_of.get(v) or ""}')
        ungrouped = [v for v in views if v['view_id'] not in grouped_views]
        if ungrouped:
            print(f'  theses without a group ({len(ungrouped)}): ' + ', '.join(f"{v['view_id']} {v['looks_at'][:30]}" for v in ungrouped[:20]))
    pool = [dict(r) for r in conn.execute("select * from review_pool_entries order by id")]
    print(f'review pool: {len(pool)} entries ' + str(collections.Counter(p['kind'] for p in pool)))
    notes = 0
    for r in conn.execute('select checks_json from match_records'):
        c = json.loads(r['checks_json'] or '{}'); notes += len(c.get('notes') or [])
    steps = collections.Counter(r[0] for r in conn.execute("select step || ':' || result from processing_steps"))
    print(f'merges the key refused or made (notes): {notes}; processing steps: {dict(steps)}')
    a = sqlite3.connect(f'file:{args.archive}?mode=ro', uri=True)
    for row in a.execute("select purpose, count(*), round(sum(cost_usd), 3), round(sum(seconds), 0), sum(case when request_sha256 like '%:%' then 1 else 0 end) from model_calls group by purpose"):
        print(f'  calls {row[0]:12s} {row[1]:4d}  ${row[2]:<7} {row[3]:>6} s  refused by schema {row[4]}')
    print(f'  total ${a.execute("select round(sum(cost_usd), 3) from model_calls").fetchone()[0]}')
    print(f'\n{len(breaches)} breaches' + (':\n  ' + '\n  '.join(breaches) if breaches else ''))
    sys.exit(1 if breaches else 0)


if __name__ == '__main__':
    main()
