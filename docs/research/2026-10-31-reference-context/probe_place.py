"""The placer's own account of a statement it filed under no question (AGENTS §1: the model's own account before any design): continue
the stored placement conversation of one run (archive model_calls, purpose 'place', found by the item's title) with one question about one
statement, and store the reply under probes/. The body sent is the stored request plus the stored answer; the schema is dropped so the
model can answer in prose.
    python3 probe_place.py <run folder> <config json> "<title fragment>|<quote fragment>" ..."""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, model  # noqa: E402

run, cfg = sys.argv[1], config.load(sys.argv[2])
archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
QUESTION = ('Statement {sid} ("{quote}…") was filed under no question. Name the question from the [Open questions] list you considered for it, '
            'say in one sentence why you filed it under none, and quote the sentence of the instructions that guided that choice. '
            'If it was an oversight, say so.')
(HERE / 'probes').mkdir(exist_ok=True)
for pair in sys.argv[3:]:
    title, quote = pair.split('|', 1)
    row = archive.execute("select request_json, answer_json from model_calls where purpose='place' and request_json like ? order by call_id desc limit 1",
                          (f'%{json.dumps(title, ensure_ascii=False)[1:-1]}%',)).fetchone()
    if not row:
        print('no placement call for', title); continue
    body, answer = json.loads(row[0]), row[1]
    user = body['messages'][-1]['content']
    line = next((l for l in user.splitlines() if quote in l), None)
    if line is None:
        print('quote not in the placement request:', quote); continue
    sid = line.strip().split(' ', 2)[1]
    links = next((p['links'] for p in json.loads(answer)['placements'] if p['id'] == sid), None)
    body.pop('response_format', None)
    body['messages'] += [{'role': 'assistant', 'content': answer}, {'role': 'user', 'content': QUESTION.format(sid=sid, quote=quote[:120])}]
    reply = model.openai_transport(cfg.provider, body)['choices'][0]['message'].get('content') or ''
    out = HERE / 'probes' / f'place-{Path(run).name}-{sid}-{quote[:20].replace(" ", "_").replace("/", "_")}.txt'
    out.write_text(f'{run}\ntitle: {title}\nstatement {sid}, stored links {links}\nline: {line.strip()[:400]}\n\n{reply}\n')
    print(f'== {out.name}\n{reply}\n')
