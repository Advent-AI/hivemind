"""For reading, not scoring: every statement a week's ledger dropped, with its reason, grouped by article in day order. The handover's
dropped record holds ids and reasons; the statement text is the item's last extraction answer in the archive (the one the handover
came from).  python3 dump_drops.py <ledger dir> [until-day] [reason-substring]"""
import collections, json, sqlite3, sys
path = sys.argv[1]; until = sys.argv[2] if len(sys.argv) > 2 else '2026-07-07'; only = sys.argv[3] if len(sys.argv) > 3 else ''
c = sqlite3.connect(f'file:{path}/views.sqlite?mode=ro', uri=True); c.row_factory = sqlite3.Row
a = sqlite3.connect(f'file:{path}/archive.sqlite?mode=ro', uri=True)
t = sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True)
cutoff = c.execute("select max(sequence_no) from processing_steps where publication_day<=?", (until,)).fetchone()[0]
rows = []
latest = {}                      # one handover per item: the last written (a re-sent item writes a new row)
for r in c.execute("select h.id, h.input_id, h.handover_json, p.publication_day from handovers h join processing_steps p on p.input_id=h.input_id where h.seq<=? order by h.id", (cutoff,)):
    latest[r['input_id']] = r
for r in sorted(latest.values(), key=lambda r: (r['publication_day'], r['input_id'])):
    h = json.loads(r['handover_json'])
    drops = [(i, why) for i, why in h['dropped'] if i.startswith('e') and only in why]
    if not drops:
        continue
    ans = a.execute("select answer_json from model_calls where purpose='extract' and request_json like ? and request_sha256 not like '%:%' order by call_id desc limit 1", (f'%[Item] id {r["input_id"]},%',)).fetchone()
    by_id = {e['id']: e for e in (json.loads(ans[0]).get('evidence', []) if ans else [])}
    title = t.execute("select publisher, title from items where input_id=?", (r['input_id'],)).fetchone()
    rows.append((r['publication_day'], r['input_id'], title, [(i, why, by_id.get(i)) for i, why in drops]))
n = sum(len(x[3]) for x in rows)
print(f'# Statements dropped in {path.rsplit("/", 1)[-1]} to {until}{" with reason containing " + repr(only) if only else ""} ({n})')
k = 0
for day, iid, title, drops in rows:
    print(f"\n## {day} {iid[-8:]} {title[0]} | {title[1][:90]}")
    for i, why, e in drops:
        k += 1
        print(f"{k}. [{(e or {}).get('tier', '?')[:5]}] ({why[:28]}) {(e or {}).get('one_line', '<text not in the archive>')[:170]}")
