"""For each judgement-gold question, the packet items the gold reader cited; for each run draw, where the statements written from
those items were filed: under the question (home), elsewhere (which views), or not in the ledger (not written or dropped). $0, read-only."""
import json, re, sqlite3, collections, sys
G = '/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold'
gold = json.load(open(f'{G}/gold-v1.json'))['entries']
packet = {i['id']: i for i in json.load(open(f'{G}/packet-v1.json'))['items']}
RUNS = {'v94': '/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-11-01-e2e-loop/arms/r7-combined-v94',
        'v108': '/Users/lchingen/hivemind/poc/data/e2e-r9-frozen-v108-2026-11-03'}
words = lambda s: set(re.findall(r'[a-z0-9$.%]+', (s or '').lower()))
def overlap(a, b):
    A, B = words(a), words(b)
    return len(A & B) / max(1, min(len(A), len(B)))
rows = collections.defaultdict(dict); totals = collections.Counter(); elsewhere = collections.Counter()
for name, base in RUNS.items():
    for d in (1, 2, 3):
        c = sqlite3.connect(f'file:{base}/d{d}/views.sqlite?mode=ro', uri=True)
        ev = collections.defaultdict(list)
        for eid, inp, quote, links in c.execute('select e.evidence_id, e.created_from_input, e.quote, group_concat(l.view_id) from evidence e left join evidence_links l on l.evidence_id=e.evidence_id group by e.evidence_id'):
            ev[inp].append((quote, set((links or '').split(',')) - {''}))
        for e in gold:
            q, v = e['question_id'], e.get('seed_view_id')
            if not v or e.get('no_view'): continue
            cited = list(dict.fromkeys((e.get('reference') or {}).get('items', []) + (e.get('implied_outcome') or {}).get('items', [])))
            for it in cited:
                item = packet.get(it)
                if not item: continue
                matches = [links for quote, links in ev.get(item['input_id'], []) if overlap(quote, item['passage']) >= 0.6]
                if not matches: state = 'not in ledger'
                elif any(v in links for links in matches): state = 'home'
                else:
                    state = 'elsewhere'
                    for links in matches:
                        for l in links: elsewhere[(name, l)] += 1
                rows[(q, it)][(name, d)] = state
                totals[(name, state)] += 1
qs = sorted({q for q, _ in rows}, key=lambda x: int(x[1:]))
print('per question: gold-cited items that reached the question (home), over 3 draws')
for q in qs:
    its = [it for (qq, it) in rows if qq == q]
    h94 = sum(rows[(q, it)].get(('v94', d)) == 'home' for it in its for d in (1, 2, 3))
    h108 = sum(rows[(q, it)].get(('v108', d)) == 'home' for it in its for d in (1, 2, 3))
    e108 = sum(rows[(q, it)].get(('v108', d)) == 'elsewhere' for it in its for d in (1, 2, 3))
    n108 = sum(rows[(q, it)].get(('v108', d)) == 'not in ledger' for it in its for d in (1, 2, 3))
    text = next(e['question'] for e in gold if e['question_id'] == q)[:60]
    print(f'{q} items {len(its):2d} | home v94 {h94:2d}/{3*len(its)} v108 {h108:2d}/{3*len(its)} | v108 elsewhere {e108:2d} not in ledger {n108:2d} | {text}')
print('totals:', {k: v for k, v in sorted(totals.items())})
print('v108 elsewhere went to:', collections.Counter({l: n for (nm, l), n in elsewhere.items() if nm == 'v108'}).most_common(8))
print('v94 elsewhere went to:', collections.Counter({l: n for (nm, l), n in elsewhere.items() if nm == 'v94'}).most_common(8))
