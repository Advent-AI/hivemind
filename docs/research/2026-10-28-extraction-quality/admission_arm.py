"""Admission arm (2026-10-28 night): one sentence of the role changes (binding_obligation gets the already-taken-on form, results/role-v21-draft.txt);
control = the production bytes stored in the runs' archives (v36b for the twelve ACP articles, the v34 snapshot for the three Ohio articles),
arm = the same request with only the system text swapped. Three draws each, eight threads, answers through the production sift
(code checks), scored against the frozen results/gold-admission-acp.json. Raw answers kept in results/admission-arm-answers.json."""
import concurrent.futures, hashlib, json, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction, model, universe
cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v36.json'))
UNI = universe.load(os.path.join(ROOT, 'poc', 'universe.json'))
ARCH = {'v36b': '/Users/lchingen/hivemind/poc/data/english-v36b-nvda-1w-2026-10-28/archive.sqlite',
        'v34': '/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450/archive.sqlite'}
ITEMS = sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); ITEMS.row_factory = sqlite3.Row
gold = json.load(open(os.path.join(HERE, 'results', 'gold-admission-acp.json')))
ITEM_ROWS = {c['input_id']: dict(r) for c in gold['cases'] for r in ITEMS.execute('select * from items where input_id=?', (c['input_id'],))}   # read before the threads start
assert hashlib.sha256(json.dumps(gold, indent=1, ensure_ascii=False).encode()).hexdigest() == open(os.path.join(HERE, 'results', 'gold-admission-acp.sha256')).read().split()[0]
ROLE = open(os.path.join(ROOT, 'src', 'hivemind', 'prompts', 'role-v20.txt')).read()
ARM_ROLE = open(os.path.join(HERE, 'results', 'role-v21-draft.txt')).read()
DRAWS = int(sys.argv[1]) if len(sys.argv) > 1 else 3


def stored_request(case):
    a = sqlite3.connect(f'file:{ARCH[case["source_archive"]]}?mode=ro', uri=True)
    row = a.execute("select request_json from model_calls where purpose='extract' and request_json like ? and request_sha256 not like '%:%' order by call_id desc limit 1",
                    (f'%[Item] id {case["input_id"]},%',)).fetchone()
    if not row:
        return None                      # the run skipped this item (no handover): nothing to send, reported as such
    req = json.loads(row[0])
    sysm = next(m for m in req['messages'] if m['role'] == 'system')
    assert sysm['content'] == ROLE, 'stored system text is not role-v20'
    return req


def arm_request(req):
    out = json.loads(json.dumps(req))
    next(m for m in out['messages'] if m['role'] == 'system')['content'] = ARM_ROLE
    return out


def sift(case, req, answer):
    user = next(m for m in req['messages'] if m['role'] == 'user')['content']
    shown = set(re.findall(r'^\s*- (v\d+) \(', user, re.M)); groups = re.findall(r'^\s*- (g\d+)\b', user, re.M)
    item = ITEM_ROWS[case['input_id']]
    evidence, cands, dropped, _ = extraction.sift_with_groups(answer, item, item['text'], shown, UNI, english=True, shown_group_ids=groups, version='20', keep_unlinked=True)
    return cands, [d for d in dropped if d[0].startswith('c')], item


def score(case, raw, cands, dropped):
    m = case['must_open']; rx = re.compile(m['scope_regex'], re.I)
    def names(c): return rx.search(' '.join([c.get('question', ''), c.get('scope', ''), c.get('looks_at', '')]))
    hits = [c for c in cands if c.get('opens_as') == m['opens_as'] and names(c)]
    proposed = [c for c in raw.get('candidates', []) if c.get('opens_as') == m['opens_as'] and names(c)]
    if hits:
        best = hits[0]; form = 'right' if best.get('measure') in m['measure'] else ('acceptable' if best.get('measure') in m['measure_acceptable'] else 'wrong_measure')
        cell = f'opened_{form}'
    elif proposed:
        cell = 'proposed_refused: ' + '; '.join(d[1][:40] for d in dropped if d[0] in {c['id'] for c in proposed})
    else:
        cell = 'none'
    extras = len(cands) - len(hits[:1])
    return cell, extras, [(c.get('opens_as'), c.get('measure'), c.get('due_day'), c.get('question', '')[:90]) for c in cands]


def send(job):
    arm, draw, case, req = job
    resp = model.openai_transport(cfg.provider, req)
    msg = resp['choices'][0]['message']['content']
    try:
        data = json.loads(msg)
    except Exception as error:
        return {'arm': arm, 'draw': draw, 'case': case['id'], 'cell': f'malformed: {error!r}'[:60], 'extras': 0, 'cands': [], 'raw': msg[:2000], 'usage': resp.get('usage')}
    try:
        cands, dropped, item = sift(case, req, data)
        cell, extras, listed = score(case, data, cands, dropped)
    except Exception as error:                 # keep the paid answer whatever the scorer does
        return {'arm': arm, 'draw': draw, 'case': case['id'], 'cell': f'scorer error: {error!r}'[:80], 'extras': 0, 'cands': [], 'raw': data.get('candidates', []), 'usage': resp.get('usage')}
    return {'arm': arm, 'draw': draw, 'case': case['id'], 'cell': cell, 'extras': extras, 'cands': listed, 'raw': data.get('candidates', []), 'usage': resp.get('usage')}


jobs = []; unsent = []
for case in gold['cases']:
    req = stored_request(case)
    if req is None:
        unsent.append(case['id']); continue
    for draw in range(1, DRAWS + 1):
        jobs.append(('control', draw, case, req)); jobs.append(('arm', draw, case, arm_request(req)))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(send, jobs))
json.dump(results, open(os.path.join(HERE, 'results', 'admission-arm-answers.json'), 'w'), indent=1, ensure_ascii=False)
print(f'| case | ' + ' | '.join(f'control d{d}' for d in range(1, DRAWS + 1)) + ' | ' + ' | '.join(f'arm d{d}' for d in range(1, DRAWS + 1)) + ' |')
print('|---|' + '---|' * (2 * DRAWS))
by = {(r['arm'], r['draw'], r['case']): r for r in results}
for case in [c for c in gold['cases'] if c['id'] not in unsent]:
    cells = [by[('control', d, case['id'])] for d in range(1, DRAWS + 1)] + [by[('arm', d, case['id'])] for d in range(1, DRAWS + 1)]
    print(f'| {case["id"]} {case.get("publisher", "ohio")[:14]} | ' + ' | '.join(f'{r["cell"]} (+{r["extras"]})' for r in cells) + ' |')
for arm in ('control', 'arm'):
    for d in range(1, DRAWS + 1):
        rows = [r for r in results if r['arm'] == arm and r['draw'] == d]
        opened = sum(1 for r in rows if r['cell'].startswith('opened')); refused = sum(1 for r in rows if r['cell'].startswith('proposed_refused'))
        print(f'{arm} draw {d}: opened {opened}/{len(rows)} (right {sum(1 for r in rows if r["cell"]=="opened_right")}), proposed-but-refused {refused}, none {sum(1 for r in rows if r["cell"]=="none")}, extras {sum(r["extras"] for r in rows)}')
print('not sent (the run skipped the item, no stored request):', unsent)
toks = sum((r['usage'] or {}).get('prompt_tokens', 0) for r in results); print('sends', len(results), 'prompt tokens', toks)
