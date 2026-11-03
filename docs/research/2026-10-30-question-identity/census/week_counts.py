"""Pieces per question and distinct claims (same-claim pairs collapsed) in a ledger, top questions first."""
import sqlite3, sys
db = sys.argv[1]
conn = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
parent = {}
def find(x):
    parent.setdefault(x, x)
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
for old, new in conn.execute('select old_evidence_id, new_evidence_id from same_claims'):
    parent[find(old)] = find(new)
questions = conn.execute('select view_id, question from views').fetchall()
rows = []
for view_id, question in questions:
    ids = [r[0] for r in conn.execute('select evidence_id from evidence_links where view_id=?', (view_id,))]
    rows.append((len(ids), len({find(x) for x in ids}), view_id, question[:90]))
rows.sort(reverse=True)
print('questions', len(rows), 'evidence rows', conn.execute('select count(*) from evidence').fetchone()[0], 'days', conn.execute('select count(*) from days_completed').fetchone()[0])
for r in rows[:8]:
    print(r)
