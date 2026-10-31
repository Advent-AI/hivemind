"""The model's own account of a kept statement with empty links in the arm (design.md P3): continue the stored REF-v53R conversation
with one question. The arm request is rebuilt (reference_arm.arm_request on bench.build) and must hash to the stored one.
    python3 probe_unlinked.py <draw> <input_id> <first words of the gold span> ..."""
import copy, json, sqlite3, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import reference_arm as ra  # noqa: E402
import score_ref as sr  # noqa: E402

draw, pairs = int(sys.argv[1]), [p.split('|', 1) for p in sys.argv[2:]]
for iid, start in pairs:
    a = next(x for x in sr.articles if x['input_id'] == iid)
    item_gold = next(i for i in a['items'] if start in i['span'])
    db = sqlite3.connect(f'file:{ra.LOOP / "loop-2026-10-29" / f"REF-v53R-d{draw}" / "answers.sqlite"}?mode=ro', uri=True)
    sha, content = db.execute('select request_sha256, content from answers where input_id=?', (iid,)).fetchone()
    item, uni, setting, schema, request, cfg = ra.bench.build(iid, ra.CONFIG)
    body = ra.arm_request(request, item)
    assert ra.model.request_identity(body)[1] == sha, 'request mismatch'
    data = json.loads(content)
    e = next((e for e in data['evidence'] if sr.sg.same_matter(item_gold, e)), None)
    if e is None or e.get('links'):
        print(iid[:30], 'not an unlinked match; skipped'); continue
    q = (f'Your evidence item {e["id"]} ("{e["quote"][:160]}…") has empty links. Quote the open question from the [Open questions] list you '
         'considered for it, say in one sentence why you left links empty, and say which sentence of the request guided that choice.')
    body.pop('response_format', None)
    body['messages'] += [{'role': 'assistant', 'content': content}, {'role': 'user', 'content': q}]
    reply = ra.model.openai_transport(cfg.provider, body)['choices'][0]['message'].get('content') or ''
    (HERE / 'probes').mkdir(exist_ok=True)
    (HERE / 'probes' / f'unlinked-{iid.split(":")[-1][:12]}.txt').write_text(f'{iid} d{draw}\ngold: {item_gold["span"]}\nkept: {e["quote"]}\n\n{reply}\n')
    print(iid[:30], 'ok')
