"""Ledger-blind arm (D211, 2026-10-28 night): the v22 request built by production code (poc-v38; no thesis, no group) for the week's
34 twice-sampled items and the 10 Kyber articles, three draws, eight threads, answers through the production sift. Control = the
two stored answers of each item under v21 (the week's run). Reports candidates per draw, agreement across draws, and every
question proposed, for reading. Raw answers kept in results/blind-arm-answers.json."""
import concurrent.futures, json, os, re, sqlite3, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction, model, universe
cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v38.json'))
UNI = universe.load(os.path.join(ROOT, 'poc', 'universe.json'))
R = '/Users/lchingen/hivemind/poc/data/english-v37-nvda-1w-2026-10-28'
c = sqlite3.connect(f'file:{R}/views.sqlite?mode=ro', uri=True); c.row_factory = sqlite3.Row
a = sqlite3.connect(f'file:{R}/archive.sqlite?mode=ro', uri=True)
ITEMS = sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); ITEMS.row_factory = sqlite3.Row
DRAWS = int(sys.argv[1]) if len(sys.argv) > 1 else 3

twice, stored = [], {}
for (iid,) in c.execute("select distinct input_id from handovers"):
    sends = [json.loads(x[0]) for x in a.execute("select answer_json from model_calls where purpose='extract' and request_json like ? and request_sha256 not like '%:%' order by call_id", (f'%[Item] id {iid},%',)) if x[0] and x[0].startswith('{')]
    stored[iid] = [[(x.get('opens_as'), x.get('measure'), x['question'][:90]) for x in s.get('candidates', [])] for s in sends]
    if len(sends) > 1:
        twice.append(iid)
kyber = [r[0] for r in ITEMS.execute("select input_id from items where publication_day between '2026-07-05' and '2026-07-07' and (lower(title) like '%kyber%' or lower(title) like '%rack%delay%' or lower(title) like '%delay%2028%')")]
ids = list(dict.fromkeys(twice + kyber))
rows = {i: dict(ITEMS.execute('select * from items where input_id=?', (i,)).fetchone()) for i in ids}
rows = {i: dict(r, object_identifiers=json.loads(r['object_identifiers']) if isinstance(r.get('object_identifiers'), str) else r.get('object_identifiers')) for i, r in rows.items()}
print(f'items: {len(ids)} ({len(twice)} twice-sampled, {len(kyber)} Kyber)')


def send(job):
    draw, iid = job
    item = rows[iid]
    setting, system, user, schema = extraction.request_for(cfg, item, item['text'], [], UNI, [])
    request = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
    resp = model.openai_transport(cfg.provider, request)
    msg = resp['choices'][0]['message']['content']
    try:
        data = json.loads(msg)
    except Exception as error:
        return {'draw': draw, 'item': iid, 'malformed': repr(error)[:80], 'cands': [], 'kept': []}
    evidence, cands, dropped, _ = extraction.sift_with_groups(data, item, item['text'], set(), UNI, english=True, shown_group_ids=(), version='22', keep_unlinked=True)
    return {'draw': draw, 'item': iid, 'cands': [(x.get('opens_as'), x.get('measure'), x.get('due_day'), x['question'][:100]) for x in data.get('candidates', [])],
            'kept': [(x.get('opens_as'), x.get('measure'), x.get('due_day'), x['question'][:100]) for x in cands],
            'refused': [d for d in dropped if d[0].startswith('c')], 'statements': len(evidence), 'usage': resp.get('usage')}


jobs = [(d, i) for i in ids for d in range(1, DRAWS + 1)]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(send, jobs))
json.dump({'stored_v21': stored, 'arm': results}, open(os.path.join(HERE, 'results', 'blind-arm-answers.json'), 'w'), indent=1, ensure_ascii=False)


def sig(x):
    words = set(re.findall(r'[a-z]{4,}', x[3].lower())) - {'what', 'will', 'nvidia', 'report', 'much', 'amount', 'does', 'year', 'calendar', 'fiscal', 'which', 'total'}
    return (x[0], x[1], frozenset(words))


def same(s, t): return s[0] == t[0] and s[1] == t[1] and len(s[2] & t[2]) >= max(2, len(s[2] | t[2]) // 3)


by = collections.defaultdict(dict)
for r in results: by[r['item']][r['draw']] = r
agree3 = agree2 = single = 0; proposals = 0
print('\n| item | v21 stored sends | arm d1 | arm d2 | arm d3 |\n|---|---|---|---|---|')
for iid in ids:
    draws = [by[iid].get(d, {'kept': []})['kept'] for d in range(1, DRAWS + 1)]
    allc = [(d, sig(x)) for d, ks in enumerate(draws) for x in ks]
    seen = []
    for d, s in allc:
        if any(same(s, t) for t in seen): continue
        seen.append(s); n = sum(1 for dd in range(DRAWS) if any(same(s, sig(x)) for x in draws[dd]))
        proposals += 1; agree3 += n == DRAWS; agree2 += n == 2; single += n == 1
    title = rows[iid]['title'][:40]
    cell = lambda ks: '; '.join(f'{x[0][:4]}/{x[1][:8]}: {x[3][:45]}' for x in ks) or '—'
    print(f"| {iid[-8:]} {title} | {' / '.join(cell(s) for s in stored.get(iid, [])) or '—'} | {' | '.join(cell(k) for k in draws)} |")
print(f'\ndistinct questions proposed by the arm: {proposals}; in all {DRAWS} draws: {agree3}; in 2: {agree2}; in 1: {single}')
print('refused by code:', collections.Counter(re.sub(r"\d{4}-\d{2}-\d{2}", "DATE", d[1])[:50] for r in results for d in r.get('refused', [])))
print('statements per answer, median:', sorted(r.get('statements', 0) for r in results)[len(results) // 2], '| sends:', len(results), '| prompt tokens:', sum((r.get('usage') or {}).get('prompt_tokens', 0) for r in results))
