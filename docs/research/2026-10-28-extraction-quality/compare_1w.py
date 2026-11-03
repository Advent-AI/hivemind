"""The one-week poc-v36 run (placement) beside the same week of the poc-v35 run (A alone; same runner, same writer): statements kept,
unplaced, links by thesis, the two sinks, items with no evidence, cost. Reads two finished ledgers of this session's own runs."""
import collections, json, sqlite3
V35 = '/Users/lchingen/hivemind/poc/data/english-v35-nvda-2w-2026-10-28'
V36 = '/Users/lchingen/hivemind/poc/data/english-v36-nvda-1w-2026-10-28'
UNTIL = '2026-07-07'


def facts(path):
    c = sqlite3.connect(f'file:{path}/views.sqlite?mode=ro', uri=True); c.row_factory = sqlite3.Row
    cutoff = c.execute("select max(sequence_no) from processing_steps where publication_day<=?", (UNTIL,)).fetchone()[0]
    f = {}
    hand = [json.loads(r['handover_json']) for r in c.execute("select handover_json from handovers where seq<=?", (cutoff,))]
    f['items'] = len(hand)
    f['evidence handed over (placed)'] = sum(len(h['evidence']) for h in hand)
    f['unplaced kept'] = sum(len(h.get('unplaced', [])) for h in hand)
    f['dropped (code checks)'] = sum(len(h['dropped']) for h in hand)
    f['items with neither evidence nor unplaced'] = sum(1 for h in hand if not h['evidence'] and not h.get('unplaced'))
    f['items with no placed evidence'] = sum(1 for h in hand if not h['evidence'])
    links = collections.Counter(r['view_id'] for r in c.execute("select view_id from evidence_links where seq<=?", (cutoff,)))
    views = {r['view_id']: r['question'][:60] for r in c.execute("select view_id, question from views where created_seq<=?", (cutoff,))}
    f['theses opened'] = len(views)
    f['links total'] = sum(links.values())
    f['links by thesis (top 6)'] = [(v, n, views.get(v, '')[:50]) for v, n in links.most_common(6)]
    sinks = [v for v, q in views.items() if 'total revenue' in q or 'Data Center segment revenue' in q]
    f['links to the two sinks'] = sum(links[v] for v in sinks)
    f['pieces per placed statement (links)'] = round(f['links total'] / max(1, f['evidence handed over (placed)']), 2)
    a = sqlite3.connect(f'file:{path}/archive.sqlite?mode=ro', uri=True)
    f['calls and cost by purpose'] = {r[0]: (r[1], round(r[2], 3)) for r in a.execute("select purpose, count(*), sum(cost_usd) from model_calls group by purpose")}
    f['unplaced table rows'] = c.execute("select count(*) from unplaced_statements").fetchone()[0] if c.execute("select name from sqlite_master where name='unplaced_statements'").fetchone() else 'n/a'
    return f


old, new = facts(V35), facts(V36)
print('| measure | poc-v35 (A), week 1 of the two-week run | poc-v36 (A + placement), week 1 |\n|---|---|---|')
for k in old:
    print(f'| {k} | {old[k]} | {new[k]} |')
