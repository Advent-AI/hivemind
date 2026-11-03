"""End-to-end noise on a production replay (Alex, 2026-10-31: extraction may be noisy, but what matters is what reaches judgement after
placement and Jev; an unfiled statement is as good as deleted). For every development-gold article processed by the run:
  stored:   evidence rows the writer stored from it (evidence.created_from_input), each linked to a thesis, so it reaches the judge;
            of those, hidden: marked by Jev as the same statement as an earlier piece (same_claims.new_evidence_id) or replaced later;
  dropped:  the handover's dropped records (reason text: no home / nothing shown / quote not in item / merged), with the quote recovered
            from the archived extraction answer so the gold can class it.
Each statement is classed against the version-5 gold: core/supp, optional, not_kept, unlisted. One replay is one draw; say so.

    python3 e2e_score.py poc/data/e2e-v69-dev14-2026-10-31
"""
import collections
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import score_ref as sr  # noqa: E402

run = ROOT / sys.argv[1] if not sys.argv[1].startswith('/') else Path(sys.argv[1])
views = sqlite3.connect(f'file:{run / "views.sqlite"}?mode=ro', uri=True)
views.row_factory = sqlite3.Row
archive = sqlite3.connect(f'file:{run / "archive.sqlite"}?mode=ro', uri=True)
articles = {a['input_id']: a for a in sr.articles}


def gold_class(a, quote, one_line=''):
    e = {'quote': quote, 'one_line': one_line}
    if any(sr.sg.same_matter(i, e) for i in a['items'] if i['weight'] in ('core', 'supporting')):
        return 'core/supp'
    if any(sr.sg.same_matter(i, e) for i in a['items'] if i['weight'] == 'optional'):
        return 'optional'
    if any(sr.sg.same(n['span'], quote) for n in a['not_kept'] if n['weight'] == 'not_kept'):
        return 'not_kept'
    if any(sr.sg.same(n['span'], quote) for n in a['not_kept'] if n['weight'] == 'optional'):
        return 'optional'
    return 'unlisted'


def archived_answer(input_id):
    row = archive.execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1",
                          (f'%[Item] id {input_id},%',)).fetchone()
    return json.loads(row[0]) if row and row[0] else None


# Ruler check (2026-10-31): a piece Jev marks as the same claim stays in force and is shown to the judge (store.evidence_in_force drops only
# replaced pieces; D248 item 7's show-once is not built), so it reaches judgement; only a replaced piece leaves the view.
same_claim_ids = {r[0] for r in views.execute('select new_evidence_id from same_claims')}
hidden_ids = {r[0] for r in views.execute('select old_evidence_id from replacements')}
counts = collections.Counter(); by_class = collections.Counter(); processed = 0; reasons = collections.Counter()
for iid, a in articles.items():
    stored = views.execute('select evidence_id, quote, one_line from evidence where created_from_input=?', (iid,)).fetchall()
    handover = views.execute('select handover_json from handovers where input_id=? order by id desc limit 1', (iid,)).fetchone()
    if handover is None and not stored:
        continue
    processed += 1
    for row in stored:
        g = gold_class(a, row['quote'], row['one_line'])
        linked = views.execute('select count(*) from evidence_links where evidence_id=?', (row['evidence_id'],)).fetchone()[0] > 0
        path = 'replaced (leaves the view)' if row['evidence_id'] in hidden_ids else ('reaches judgement, marked repeat' if row['evidence_id'] in same_claim_ids else 'reaches judgement' if linked else 'stored, unlinked')
        counts[path] += 1; by_class[(path, g)] += 1
    if handover:
        h = json.loads(handover['handover_json'])
        answer = archived_answer(iid) or {}
        by_id = {e['id']: e for e in answer.get('evidence', [])}
        for eid, reason in h.get('dropped', []):
            e = by_id.get(eid)
            reasons[reason.split(':')[0][:40]] += 1
            g = gold_class(a, e['quote'], e.get('one_line', '')) if e else 'unknown'
            counts['dropped'] += 1; by_class[('dropped', g)] += 1
print(f'{run.name}: {processed} of {len(articles)} gold articles processed (one draw)')
for path in ('reaches judgement', 'reaches judgement, marked repeat', 'replaced (leaves the view)', 'stored, unlinked', 'dropped'):
    parts = {g: by_class[(path, g)] for g in ('core/supp', 'optional', 'not_kept', 'unlisted', 'unknown')}
    print(f'  {path:<26} total {counts[path]:>4} | core/supp {parts["core/supp"]:>3}  optional {parts["optional"]:>3}  gold-not-kept {parts["not_kept"]:>3}  unlisted {parts["unlisted"]:>3}  unknown {parts["unknown"]}')
print('  dropped reasons:', dict(reasons.most_common(6)))
