"""The two-week poc-v35 run (A) beside the three-month run's own first two weeks (poc-v34, same writer; snapshot 2026-10-28T1450):
theme theses' evidence and judgements, open theses, duplicate H200 questions, items that kept no evidence, cost. Reads only the
snapshot and the finished two-week ledger."""
import collections, json, sqlite3
SNAP = '/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
NEW = '/Users/lchingen/hivemind/poc/data/english-v35-nvda-2w-2026-10-28'
UNTIL = '2026-07-14'


def ledger(path):
    c = sqlite3.connect(f'file:{path}/views.sqlite?mode=ro', uri=True); c.row_factory = sqlite3.Row
    return c


def facts(c, archive):
    f = {}
    cutoff = c.execute("select max(seq) from processing_steps where publication_day<=?", (UNTIL,)).fetchone()[0] if 'seq' in [x[1] for x in c.execute('pragma table_info(processing_steps)')] else None
    cutoff = c.execute("select max(sequence_no) from processing_steps where publication_day<=?", (UNTIL,)).fetchone()[0]
    views = [dict(r) for r in c.execute("select * from views where created_seq<=? order by created_seq", (cutoff,))]
    f['theses opened'] = len(views); f['theme theses opened'] = sum(1 for v in views if v['kind'] == 'theme')
    f['questions'] = [(v['view_id'], v['kind'], v['question'][:90]) for v in views]
    links = collections.Counter(r['view_id'] for r in c.execute("select view_id from evidence_links where seq<=?", (cutoff,)))
    judged = collections.Counter(r['view_id'] for r in c.execute("select view_id from judgements where seq<=?", (cutoff,)))
    f['theme evidence links'] = {v['view_id']: links[v['view_id']] for v in views if v['kind'] == 'theme'}
    f['theme judgements'] = {v['view_id']: judged[v['view_id']] for v in views if v['kind'] == 'theme'}
    f['asset evidence links'] = sum(links[v['view_id']] for v in views if v['kind'] == 'asset')
    hand = [json.loads(r['handover_json']) for r in c.execute("select handover_json from handovers where seq<=?", (cutoff,))]
    f['items handed over'] = len(hand); f['items with no evidence'] = sum(1 for h in hand if not h['evidence'])
    f['evidence kept'] = sum(len(h['evidence']) for h in hand); f['dropped pieces'] = sum(len(h['dropped']) for h in hand)
    f['dropped: links to nothing shown'] = sum(1 for h in hand for d in h['dropped'] if d[1].startswith('links to nothing shown'))
    f['candidates handed over'] = sum(len(h['candidates']) for h in hand)
    a = sqlite3.connect(f'file:{archive}?mode=ro', uri=True)
    f['cost (extract/match/judge, $)'] = {r[0]: round(r[1], 3) for r in a.execute("select purpose, sum(cost_usd) from model_calls where created_at<=? group by purpose", ('9999',))}
    return f


old = facts(ledger(SNAP), f'{SNAP}/archive.sqlite')
new = facts(ledger(NEW), f'{NEW}/archive.sqlite')
print('| measure | poc-v34 (control, first two weeks of the run) | poc-v35 (A) |\n|---|---|---|')
for k in ('items handed over', 'items with no evidence', 'evidence kept', 'dropped pieces', 'dropped: links to nothing shown', 'candidates handed over', 'theses opened', 'theme theses opened', 'asset evidence links', 'theme evidence links', 'theme judgements', 'cost (extract/match/judge, $)'):
    print(f'| {k} | {old[k]} | {new[k]} |')
print('\ncontrol questions:'); [print(' ', q) for q in old['questions']]
print('\nA questions:'); [print(' ', q) for q in new['questions']]
