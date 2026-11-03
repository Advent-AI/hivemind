"""Problem A arm ($0.01): the 2026-07-08 Straits Times H200 item re-sent through the production request builder with the
theme theses added to the shown list. Control = the stored request rebuilt (its identity must equal the archived one, which
proves the harness sends production bytes) and sent again; arm = the same with every theme thesis open at that time added.
Three samples each in separate scratch archives (an archive serves an identical request from store). Read-only on the run."""
import json, os, sqlite3, sys
ROOT = '/Users/lchingen/hivemind-admission-v12-2026-10-26'; sys.path.insert(0, ROOT + '/src')
from hivemind import config, extraction, model, universe
from hivemind.views import store
R = '/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28'
HERE = os.path.dirname(os.path.abspath(__file__))
ITEM = sys.argv[1] if len(sys.argv) > 1 else 'gnews:c8c39f971721fd820aab5c1c'
cfg = config.load(ROOT + '/poc/config/poc-v34.json'); uni = universe.load(ROOT + '/poc/universe.json')
t = sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); t.row_factory = sqlite3.Row
item = dict(t.execute('select * from items where input_id=?', (ITEM,)).fetchone()); item['object_identifiers'] = json.loads(item['object_identifiers'] or '[]')
v = sqlite3.connect(f'file:{R}/views.sqlite?mode=ro', uri=True); v.row_factory = sqlite3.Row
seq = v.execute('select min(sequence_no) from processing_steps where input_id=?', (ITEM,)).fetchone()[0]
objects = [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
def shown_at(kinds):
    rows = v.execute('select view_id from views where created_seq<? order by created_seq', (seq,))
    out = []
    for r in rows:
        vw = store.view(v, r['view_id'])
        if vw['object_id'] in objects or (vw['kind'] in kinds): out.append(dict(vw, open=True, depends_on=[], dependencies=[]))
    return out
groups = store.groups_for_prompt(v, objects, item.get('title') or '')
created = {r['view_id']: r['created_seq'] for r in v.execute('select view_id, created_seq from views')}
groups = [g for g in groups if g['created_seq'] < seq]      # groups declared later did not exist at the item's turn
for g in groups:        # the group block as it stood at the item's turn: members opened later are not shown
    g['members'] = [m for m in g['members'] if created.get(m['view_id'] if isinstance(m, dict) else m, 10**9) < seq]
a = sqlite3.connect(f'file:{R}/archive.sqlite?mode=ro', uri=True)
stored = a.execute("select request_sha256 from model_calls where purpose='extract' and request_json like ? limit 1", (f'%{ITEM}%',)).fetchone()[0].split(':')[0]
results = {}
for label, kinds in (('control', ()), ('arm_theme_shown', ('theme',))):
    shown = shown_at(kinds)
    setting, system, user, schema = extraction.request_for(cfg, item, item['text'], shown, uni, groups)
    _, ident = model.request_identity(model.build_request(setting, system, user, schema, 'extraction', cfg.provider))
    print(f'{label}: shown {[s["view_id"] for s in shown]}; user chars {len(user)}; identity equals the archived request: {ident == stored}')
    if label == 'control': assert ident == stored, 'harness bytes differ from production (AGENTS §5)'
    results[label] = []
    for sample in (1, 2, 3):
        archive = model.Archive(os.path.join(HERE, f'ab-archive-{label}-s{sample}.sqlite'))
        answer = model.call(archive, cfg, setting, system, user, schema, 'extraction', 'extract')
        data = answer.data if hasattr(answer, 'data') else answer
        ev = data.get('evidence', []); links = sum(1 for e in ev for l in e.get('links', []) if l == 'v3')
        cands = [c['question'][:90] for c in data.get('candidates', [])]
        results[label].append({'pieces': len(ev), 'unlinked': sum(1 for e in ev if not e.get('links')), 'links_to_v3': links, 'candidates': cands})
        print(f'  sample {sample}: pieces {len(ev)}, unlinked {results[label][-1]["unlinked"]}, links to v3 {links}, candidates {cands}')
json.dump(results, open(os.path.join(HERE, 'theme_shown_arm-results.json'), 'w'), indent=1, ensure_ascii=False)
