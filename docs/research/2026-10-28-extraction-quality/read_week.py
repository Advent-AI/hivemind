"""For reading, not scoring: what a week's ledger holds — every thesis with its question and ladder, the research groups and their
members, a sample of the pieces under each thesis, a sample of the unplaced statements, and the judgements' reasons. The reader is the
agent; the script only lays the material out.  python3 read_week.py <ledger dir> [until-day]"""
import collections, json, random, sqlite3, sys
random.seed(17)
path, until = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else '2026-07-07')
c = sqlite3.connect(f'file:{path}/views.sqlite?mode=ro', uri=True); c.row_factory = sqlite3.Row
cutoff = c.execute("select max(sequence_no) from processing_steps where publication_day<=?", (until,)).fetchone()[0]
views = [dict(r) for r in c.execute("select * from views where created_seq<=? order by created_seq", (cutoff,))]
print(f'# {path}  (to {until}, seq<={cutoff})\n\n## Theses ({len(views)})')
for v in views:
    rungs = [r['label'] for r in c.execute("select label from rungs where view_id=? order by position", (v['view_id'],))]
    key = c.execute("select measure, scope, period_start, period_end, event_type from view_keys where view_id=?", (v['view_id'],)).fetchone()
    print(f"- {v['view_id']} [{v['kind']} {v['object_id']}] due {v['due_day']} | {v['question']}\n    key: {dict(key) if key else None} | rungs: {rungs}")
print('\n## Research groups')
for g in c.execute("select * from thesis_groups where created_seq<=? order by created_seq", (cutoff,)):
    members = [r['view_id'] for r in c.execute("select view_id from thesis_group_members where group_id=?", (g['group_id'],))]
    print(f"- {g['group_id']} \"{g['name']}\" members {members} aliases {json.loads(g['aliases'] or '[]')}\n    scope: {g['scope'][:160]}")
links = collections.defaultdict(list)
for r in c.execute("select l.view_id, e.one_line, e.original_who, e.tier from evidence_links l join evidence e on e.evidence_id=l.evidence_id where l.seq<=?", (cutoff,)):
    links[r['view_id']].append(r)
print('\n## Pieces under each thesis (up to 8 random)')
for v in views:
    rows = links[v['view_id']]
    print(f"\n### {v['view_id']} ({len(rows)} pieces) {v['question'][:80]}")
    for r in random.sample(rows, min(8, len(rows))):
        print(f"  - [{r['tier'][:5]}] {(r['original_who'] or '')[:24]} | {r['one_line'][:140]}")
has_unplaced = c.execute("select name from sqlite_master where name='unplaced_statements'").fetchone()
if has_unplaced:
    rows = [json.loads(r['statement_json']) for r in c.execute("select statement_json from unplaced_statements where seq<=?", (cutoff,))]
    print(f'\n## Unplaced statements ({len(rows)}; 30 random)')
    for s in random.sample(rows, min(30, len(rows))):
        print(f"  - [{(s.get('tier') or '')[:5]}] {(s.get('original_who') or '')[:24]} | {s['one_line'][:140]}")
print('\n## Judgements (the latest of each thesis)')
for v in views:
    j = c.execute("select rung, reasons, cited_evidence_json, publication_day from judgements where view_id=? and seq<=? order by judgement_id desc limit 1", (v['view_id'], cutoff)).fetchone()
    n = c.execute("select count(*) from judgements where view_id=? and seq<=?", (v['view_id'], cutoff)).fetchone()[0]
    if j:
        print(f"\n### {v['view_id']} rung {j['rung']} ({n} judgements, last {j['publication_day']}, cites {len(json.loads(j['cited_evidence_json'] or '[]'))})\n{j['reasons'][:700]}")
