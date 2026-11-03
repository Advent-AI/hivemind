"""$0 acceptance of the identity rules R2-e (Jev's `part_of` verdict files the candidate under the open question) and R2-f (`event`
and `policy_event` are one measure family) on the stored matching records of finished draws: for every candidate that opened a
question, re-derive from the stored Jev verdicts (the decision's reason text) and the stored typed keys what the rules in the current
code would do, and print the merges the rules add, the questions that stay new, and every case where the merge target differs from
the question the candidate actually opened (the reader judges each). No model call.

    python3 replay_part_of.py <run folder> ...
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind.views import identity, jev_matching, store  # noqa: E402


VERDICT = re.compile(r'(v\d+): ([a-z_]+) ([0-9.]+)')


def replay(run):
    conn = store.open_read_only(f'{run}/views.sqlite')
    opened_by = {}
    for r in conn.execute("select view_id, created_from_input, question from views where created_from_input not like 'seed:%'"):
        opened_by.setdefault(r['created_from_input'], []).append((r['view_id'], r['question']))
    titles = {r['view_id']: r['question'] for r in conn.execute('select view_id, question from views')}
    added, kept_new, total = [], [], 0
    for m in conn.execute('select input_id, decisions_json from match_records where call_no=1 order by id'):
        if m['input_id'] not in opened_by:
            continue
        for c in json.loads(m['decisions_json']).get('candidates', []):
            if c['outcome'] not in ('new', 'succession'):
                continue
            total += 1
            # the candidate's typed fields: the question it opened carries them (the writer copies the candidate's key)
            own = next((vid for vid, _ in opened_by[m['input_id']]), None)
            own_key = store.view_key(conn, own) or {}
            cand = dict(own_key, object=conn.execute('select object_id from views where view_id=?', (own,)).fetchone()[0])
            verdicts = [(v, rel, float(p)) for v, rel, p in VERDICT.findall(c['reason'].split('collision judge')[0])]
            merge_to, why = None, ''
            for rel in ('same_quantity_or_event', 'same_quantity_other_period', 'part_of'):
                ranked = sorted(((p, v) for v, r, p in verdicts if r == rel and p >= jev_matching.THRESHOLD), reverse=True)
                for p, v in ranked:
                    key = store.view_key(conn, v)
                    if not key or v == own:
                        continue
                    if rel == 'same_quantity_other_period' and not jev_matching.event_home(conn, v, key, cand):
                        continue
                    if identity.conflicts(key, cand, merging=False):
                        continue
                    merge_to, why = v, f'{rel} {p:.2f}'
                    break
                if merge_to:
                    break
            if merge_to:
                added.append((m['input_id'][-10:], c['id'], own, titles.get(own, '')[:60], merge_to, titles.get(merge_to, '')[:60], why, c['outcome']))
            else:
                best = max(verdicts, key=lambda t: (t[1] != 'different', t[2]), default=None)
                kept_new.append((m['input_id'][-10:], c['id'], own, titles.get(own, '')[:70], best))
    print(f'\n# {run}: {total} candidates opened a question; under the current rules {len(added)} would merge, {len(kept_new)} stay new')
    print('## merges the rules add (read each: is the target the card an analyst holds?)')
    for row in added:
        print(f'- {row[0]} {row[1]} ({row[7]}) opened {row[2]} {row[3]!r}\n      -> {row[4]} {row[5]!r} by {row[6]}')
    print('## stay new (best non-different verdict about an open question)')
    for row in kept_new:
        print(f'- {row[0]} {row[1]} opened {row[2]} {row[3]!r} | best {row[4]}')


if __name__ == '__main__':
    for run in sys.argv[1:]:
        replay(run)
