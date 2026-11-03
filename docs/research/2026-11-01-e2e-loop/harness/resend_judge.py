"""Cheapest proof of a judging-prompt change (AGENTS §1 step 4, §5 point 2): for each named thesis, take the last stored judgement
request of one run, replace the system prompt with the new version's and the response schema with `judging.schema_for(new version)`
(production's key order, not the archive's), send once, and print the stored answer beside the new one so a reader can judge the
reasoning, not a score. About a cent for a dozen theses.

    python3 resend_judge.py <run folder> <config json with the new rejudging prompt> v1 v2 ...
"""
import json
import sqlite3
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, model  # noqa: E402
from hivemind.views import judging  # noqa: E402

SENDERS = 8


def main():
    run, cfg, wanted = sys.argv[1], config.load(sys.argv[2]), sys.argv[3:]
    version = cfg.rejudging.prompt_version
    system = Path(config.prompt_path(version + '.txt')).read_text(encoding='utf-8')
    schema = judging.schema_for(version)
    archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
    last = {}
    for call_id, request_json, answer_json in archive.execute("select call_id, request_json, answer_json from model_calls where purpose='judge' order by call_id"):
        body = json.loads(request_json)
        view_id = body['messages'][-1]['content'].split('Thesis ', 1)[1].split(' ', 1)[0]
        last[view_id] = (call_id, body, json.loads(answer_json or '{}'))
    jobs = [(v, *last[v]) for v in wanted if v in last]
    stored_system = jobs[0][2]['messages'][0]['content']
    print(f'{len(jobs)} theses, last stored judgement request of each re-sent once with {version} ({len(system)} chars; stored prompt {len(stored_system)} chars)', flush=True)

    def send(body):
        edited = json.loads(json.dumps(body))
        edited['messages'][0]['content'] = system
        edited['response_format']['json_schema']['schema'] = schema
        content = model.openai_transport(cfg.provider, edited)['choices'][0]['message']['content']
        return json.loads(content)

    with ThreadPoolExecutor(SENDERS) as pool:
        futures = [(v, call_id, body, stored, pool.submit(send, body)) for v, call_id, body, stored in jobs]
        for v, call_id, body, stored, f in futures:
            new = f.result()
            question = views.execute('select question from views where view_id=?', (v,)).fetchone()[0]
            rungs = [f'{r[0]} {r[1]}' for r in views.execute('select position, label from rungs where view_id=? order by position', (v,))]
            user = body['messages'][-1]['content']
            counts = {k: sum(1 for p in new.get('pushes', []) if p['push'] == k) for k in ('toward_first', 'toward_last', 'none')}
            print('\n' + '=' * 110)
            print(f'{v} (call {call_id}) {question}\n  ladder: {" / ".join(rungs)}\n  request: {user.count(chr(10) + "- e")} evidence lines shown')
            print(f'  STORED  rung {stored.get("rung")} changed {stored.get("changed")}\n    reasons: {(stored.get("reasons") or "")[:700]}')
            print(f'  NEW     rung {new.get("rung")} changed {new.get("changed")} pushes {counts}')
            print(f'    reference: {new.get("reference")}')
            print(f'    implied_outcome: {new.get("implied_outcome")}')
            print(f'    reasons: {(new.get("reasons") or "")[:900]}')
            print(f'    why_changed: {(new.get("why_changed") or "")[:300]}', flush=True)


if __name__ == '__main__':
    main()
