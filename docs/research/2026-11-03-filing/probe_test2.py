"""Test 2 failed (the two-uses examples did not bring Broadcom's figures to the custom-chip question). Ask the model for its own account in
the test-2 conversation: the v3 request as sent, its answer, then one question with the links rule quoted. Two independent sends, about a
cent each."""
import json, re, sys
sys.path.insert(0, '.'); sys.path.insert(0, '/Users/lchingen/hivemind/src')
import sqlite3, variants
from hivemind import config, model
A = json.load(open('test2-answers.json'))
cfg = config.load('/Users/lchingen/hivemind/poc/config/poc-v108.json')
db = sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/e2e-r9-frozen-v108-2026-11-03/d1/archive.sqlite?mode=ro', uri=True)
pick = None
for key, ans in A.items():
    call, arm, n = key.split('|')
    if arm != 'v3': continue
    for e in ans.get('evidence', []):
        t = e.get('quote', '') + e.get('one_line', '')
        if re.search('broadcom', t, re.I) and re.search(r'10\.8|16(\.0)? billion', t) and set(e.get('links') or []) >= {'v1', 'v2'}:
            pick = (call, n, ans, e); break
    if pick: break
call, n, ans, e = pick
req = json.loads(db.execute('select request_json from model_calls where call_id=?', (int(call.split(':')[1]),)).fetchone()[0])
body = variants.apply('v3', req)
rule = body['response_format']['json_schema']['schema']['properties']['evidence']['items']['properties']['links']['description']
q = ('The schema of your answer defined the links field as follows: "' + rule + '" '
     f"About your answer: {e['id']} ({e['quote'][:220]!r}) has links {e.get('links')}. Question v16 asks: \"How much will cloud providers spend on "
     "custom AI silicon (ASICs) in calendar 2026?\" Answer each in two or three sentences, quoting the instruction you followed: (1) Would an analyst "
     f"use {e['id']} to estimate v16's answer? (2) Why did you file it under v1 and v2 and not under v16, and which words in v16's takes line or in the "
     "links rule decided it? (3) What would have to be true of a statement about a chip supplier's revenue for you to file it under v16?")
body.pop('response_format', None)
body['messages'] = body['messages'] + [{'role': 'assistant', 'content': json.dumps(ans, ensure_ascii=False)}, {'role': 'user', 'content': q}]
print(f'## {call} v3 send {int(n) + 1} | {e["id"]} links {e.get("links")} | {e["quote"][:160]}')
for i in range(2):
    print(f'--- send {i + 1}'); print(model.openai_transport(cfg.provider, body, timeout=300)['choices'][0]['message']['content'])
