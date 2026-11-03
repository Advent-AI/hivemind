"""Cheapest proof for one placement wording (AGENTS §1 step 4): re-send one stored placement request as sent and with one edit of the
system prompt, n times each, and print the links the placer gives one statement. A re-send of the stored bytes is the control.
    python3 resend_place.py <run folder> <config json> "<title fragment>" "<quote fragment>" <n> "<old text>" "<new text>" """
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, model  # noqa: E402

run, cfg, title, quote, n, old, new = sys.argv[1], config.load(sys.argv[2]), sys.argv[3], sys.argv[4], int(sys.argv[5]), sys.argv[6], sys.argv[7]
archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
row = archive.execute("select request_json from model_calls where purpose='place' and request_json like ? order by call_id desc limit 1",
                      (f'%{json.dumps(title, ensure_ascii=False)[1:-1]}%',)).fetchone()
body = json.loads(row[0])
system = body['messages'][0]['content']
current = open(config.prompt_path(cfg.placement.prompt_version + '.txt'), encoding='utf-8').read()
print('stored system prompt == current file:', system.strip() == current.strip())
assert system.count(old) == 1, 'the old text must occur once in the stored system prompt'
sid = next(l for l in body['messages'][-1]['content'].splitlines() if quote in l).strip().split(' ', 2)[1]
for label, text in (('control (as stored)', system), ('edited', system.replace(old, new))):
    results = []
    for _ in range(n):
        sent = json.loads(json.dumps(body)); sent['messages'][0]['content'] = text
        answer = json.loads(model.openai_transport(cfg.provider, sent)['choices'][0]['message']['content'])
        results.append(next(p['links'] for p in answer['placements'] if p['id'] == sid))
    print(f'{label}: statement {sid} links over {n} sends: {results}')
