"""Ask the frozen extraction model for its own account of where it filed two Broadcom statements (continue the stored conversation,
free text; about a cent a send). With --with-rule the links definition the original schema carried is quoted in the question, because the
free-text continuation drops the schema (Codex review r1, point 1)."""
import json, sqlite3, sys
sys.path.insert(0, '/Users/lchingen/hivemind/src')
from hivemind import config, model
RUN = '/Users/lchingen/hivemind/poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
cfg = config.load('/Users/lchingen/hivemind/poc/config/poc-v108.json')
a = sqlite3.connect(f'file:{RUN}/archive.sqlite?mode=ro', uri=True)
body, answer = [json.loads(x) for x in a.execute('select request_json, answer_json from model_calls where call_id=818').fetchone()]
rule = body['response_format']['json_schema']['schema']['properties']['evidence']['items']['properties']['links']['description']
question = ("About your answer: e2 (Broadcom's AI semiconductor sales of $10.80 billion growing 143%) and e3 (Hock Tan: the mix is "
            "\"driven by increasing demand for custom AI accelerators and AI networking\") both have links ['v1']. Answer each in two or three "
            "sentences, quoting the instruction or description you followed: (1) Which instruction led you to file them under v1 and not under "
            "v16 (How much will cloud providers spend on custom AI silicon (ASICs) in calendar 2026?) or v6 (NVIDIA's share of calendar-2026 "
            "data-center AI accelerator spending)? (2) As an analyst, does Broadcom's custom-accelerator revenue tell you anything about how much "
            "cloud providers spend on custom AI silicon, and what in v16's takes line made you decide it is or is not v16's own figure? "
            "(3) Which two statements in the instructions did you reject or weigh less when you decided?")
if '--with-rule' in sys.argv:
    question = ('The schema of your answer defined the links field as follows: "' + rule + '" ' + question)
body.pop('response_format', None)
body['messages'] = body['messages'] + [{'role': 'assistant', 'content': json.dumps(answer, ensure_ascii=False)}, {'role': 'user', 'content': question}]
for i in range(2):
    print(f'--- send {i + 1}'); print(model.openai_transport(cfg.provider, body)['choices'][0]['message']['content'])
