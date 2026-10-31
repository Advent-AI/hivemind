"""For the match records that opened the given questions: what the candidate was compared with and the reason recorded."""
import sqlite3, json, sys
db = '/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/views.sqlite'
conn = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
conn.row_factory = sqlite3.Row
targets = sys.argv[1:]
for view_id in targets:
    view = conn.execute('select * from views where view_id=?', (view_id,)).fetchone()
    print('=====', view_id, 'created_seq', view['created_seq'], 'from', view['created_from_input'])
    key = conn.execute('select * from view_keys where view_id=?', (view_id,)).fetchone()
    if key:
        print('key:', {k: key[k] for k in key.keys() if key[k] not in (None, '')})
    for rec in conn.execute('select * from match_records where input_id=? order by id', (view['created_from_input'],)):
        decisions = json.loads(rec['decisions_json'] or '{}')
        for c in decisions.get('candidates', []):
            print('  candidate', c.get('id'), c.get('outcome'), c.get('target_view_id'), '|', c.get('reason', '')[:600])
