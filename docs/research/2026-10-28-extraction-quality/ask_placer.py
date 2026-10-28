"""The model's own account (AGENTS §1): continue a stored placement conversation and ask which line led it to leave a statement
homeless, and which questions it rejected. A cent a case; answers saved to ask_placer.json. Reads only scratch archives."""
import json, sqlite3, sys
sys.argv=['x']; import ab_gold, place_gold as pg
from hivemind import model
CASES = [('a07-2', 'gnews:6832f79522b3a14c48cd352b', 1), ('a11-2', 'gnews:71df54965281684cc500960f', 2), ('t01-2', 'gnews:6c62a57b64473d2ac15a53ad', 1)]
gold = {}
for f in ('gold-extraction.json', 'gold-extraction-themes.json'):
    for a in json.load(open(f))['articles']:
        for s in a['statements']: gold[s['id']] = s
out = []
for sid, iid, draw in CASES:
    s = gold[sid]; st = pg.raw_statements(draw, iid)
    hit = next(e for e in st if any(ab_gold.overlap(e['quote'], sp) for sp in [s['span']] + s['also']))
    a = sqlite3.connect(f'file:results/archive-place-same2-s{draw}.sqlite?mode=ro', uri=True)
    row = next(((ans, req) for ans, req in a.execute("select answer_json, request_json from model_calls") if hit['quote'][:60] in req), None)
    req = json.loads(row[1]); answer = row[0]
    question = (f"For statement {hit['id']} you answered {[p['links'] for p in json.loads(answer)['placements'] if p['id']==hit['id']]}. The questions {s['bears_on_with_themes']} "
                f"were open. Which sentence of the instructions or of a question's 'takes' line led you to that answer, and which two questions did you consider and reject, "
                f"and why? Quote the sentence. Three sentences.")
    messages = req['messages'] + [{'role': 'assistant', 'content': answer}, {'role': 'user', 'content': question}]
    request = {'model': 'gpt-6-luna', 'messages': messages, 'max_completion_tokens': 3000, 'reasoning_effort': 'low',
               'response_format': {'type': 'json_schema', 'json_schema': {'name': 'account', 'strict': True, 'schema': {'type': 'object', 'additionalProperties': False, 'required': ['answer'], 'properties': {'answer': {'type': 'string'}}}}}}
    resp = model.openai_transport(ab_gold.cfg.provider, request)
    text = json.loads(resp['choices'][0]['message']['content'])['answer']
    out.append({'case': sid, 'statement': hit['one_line'], 'wanted': s['bears_on_with_themes'], 'account': text})
    print(f"\n## {sid} ({hit['one_line'][:90]}) wanted {s['bears_on_with_themes']}\n{text}")
json.dump(out, open('ask_placer.json', 'w'), indent=1, ensure_ascii=False)
