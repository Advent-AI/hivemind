"""Reproduce every D160 handover and measure the two complete first requests, without model calls."""
import json
import tempfile
from pathlib import Path
import ohio_sequence as o

out = Path(__file__).resolve().parent
old = out.parent/'2026-10-25-ohio-grouping-03'
items = o.read(old/'items.json')
uni = o.universe.load(old/'universe.json')
roles = {'control':(old/'role-questions.txt').read_text(), 'grouped':(out/'role-evidence.txt').read_text()}
results = {}
with tempfile.TemporaryDirectory() as d:
    conn = o.groups.open_db(Path(d)/'views.sqlite')
    for g in o.read(old/'reference-groups.json'):
        conn.execute('insert into threads values (?,?,?,?,?)', tuple(g[k] for k in ('thread_id','name','scope','seq','input_id')))
    conn.commit()
    for arm, role in roles.items():
        system, user, shown, offered = o.context(conn, items[0], uni, True, role_text=role)
        req = o.model.build_request(o.config.load(old/'config.json').extraction_setting('T7'), system, user, o.schema(offered), 'extraction', 'openai')
        o.write(out/f'{arm}-first-request.json', req)
        results[arm] = {'role_chars':len(role), 'request_chars':len(json.dumps(req, ensure_ascii=False))}
    conn.close()
checks = []
for folder in sorted(old.glob('*/item[123]')):
    if not (folder/'extraction.json').exists():
        continue
    item = items[int(folder.name[4:])-1]
    ctx, raw = o.read(folder/'context.json'), o.read(folder/'extraction.json')
    o.validate_references(raw, ctx['offered'])
    ev, ca, dr = o.extraction.sift(raw, item, item['text'], {v['view_id'] for v in ctx['shown']}, uni)
    prior = o.read(folder/'handover.json')
    assert ev == prior['evidence'] and ca == prior['candidates'] and [list(x) for x in dr] == prior['dropped']
    checks.append({'sample':str(folder.relative_to(old)), 'evidence':len(ev), 'candidates':len(ca), 'drops':dr})
assert len(checks) == 18
results['stored_answers_checked'] = checks
control, arm = o.read(out/'control-first-request.json'), o.read(out/'grouped-first-request.json')
control['messages'][0] = arm['messages'][0]
assert control == arm
results['only_system_differs'] = True
o.write(out/'offline-audit.json', results)
print({k:v for k,v in results.items() if k != 'stored_answers_checked'})
print('18 stored handovers reproduced exactly; no new refusal')
