"""Cheapest proof of a review turn (AGENTS §1 step 4, on stored data): continue each stored extraction conversation with one question
asking the model to read its evidence back as the analyst and say keep or drop for each item, as the probes did one item at a time
(4 of 4 noise items dropped). The stored answer with the dropped items removed is written under a new run tag, so score_small.py reads it
as it reads any run. Research harness only: production code and prompts are unchanged.

    python3 review_turn.py <source-run> <new-run> [--question=R1|R2] <input_id ...>        # e.g. N1-v53 R1-v53R; three draws each
"""
import concurrent.futures
import copy
import json
import sqlite3
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOOP = ROOT / 'docs/research/2026-10-29-analyst-standard'
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'poc'), str(LOOP)]
import bench_v23 as bench  # noqa: E402
from hivemind import model  # noqa: E402

QUESTIONS = {
    # R1: anchored to the company's own key judgements; narrower than standard 5.1, which also counts questions about customers,
    # suppliers, competitors, regulators and the economy (R1 dropped a national data-centre plan and a rival's backstops)
    'R1': ('Read each evidence item you returned back as the analyst following the company. Keep an item only when you would put it in '
           "this week's notes: it is new (a fresh event, figure or specific judgement, not background the analyst already knew) and it moves "
           "a question the analyst bets on — the company's revenue, margins, cash or credit risk, demand for its products, the progress of "
           'the product generation that carries its value, the supply or price of its key inputs, or its competitive position. A statement '
           'only about itself (one store opening, one manager\'s pay, an app gaining a feature) is dropped. Forecasts, rumours, '
           'counter-examples and named actions without an amount or a date are kept when they move such a question. Give a verdict for '
           'every item id.'),
    # R2: standard 5.1 (the keep rule, its question not limited to the company), 5.2 (incomplete evidence), the 5.3 rows, D243 item 6
    'R2': ('Read each evidence item you returned back, one by one, as the analyst following the company. Keep an item when you would write '
           "it in this week's notes because it makes some question's answer more or less likely — about the company or its customers, "
           'suppliers, competitors, regulators or the economy — and it is new: a fresh event, figure or specific judgement. Drop common '
           'knowledge and background the analyst already knew, a long-standing situation retold, general views and risk lists, product, '
           'game or benchmark details without business scale, and statements only about themselves (one store opening, one manager\'s pay, '
           'an app gaining a feature). A forecast, a rumour, a counter-example, a distant or conditional statement, or a named party\'s '
           'action without an amount or a date is kept when it moves such a question; guidance, a forecast or a plan still in force is kept '
           'even when retold. Give a verdict for every item id.'),
    # R3: R2 with the 5.3 product row's boundary (adoption or integration, and the main product's plan or configuration, are not
    # product details), which R2 left out and so dropped a cancelled rack design and partners' integrations; text in review-core-r3.txt,
    # shared with the in-call review of send_field.py
    'R3': ('Read each evidence item you returned back, one by one, as the analyst following the company. '
           + (Path(__file__).resolve().parent / 'review-core-r3.txt').read_text().strip() + ' Give a verdict for every item id.'),
}
QUESTION = QUESTIONS['R1']
SCHEMA = {'type': 'json_schema', 'json_schema': {'name': 'review', 'strict': True, 'schema': {
    'type': 'object', 'additionalProperties': False, 'required': ['verdicts'],
    'properties': {'verdicts': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['id', 'keep'],
                                                           'properties': {'id': {'type': 'string'}, 'keep': {'type': 'boolean'}}}}}}}}
LOCK = threading.Lock()


def store(tag):
    (LOOP / 'loop-2026-10-29' / tag).mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(LOOP / 'loop-2026-10-29' / tag / 'answers.sqlite')
    conn.execute('create table if not exists answers (input_id text primary key, config text, request_sha256 text, response_json text, content text,'
                 ' completed integer, input_tokens integer, output_tokens integer, seconds real, error text)')
    return conn


def one(source, target, input_id):
    src = sqlite3.connect(f'file:{LOOP / "loop-2026-10-29" / source / "answers.sqlite"}?mode=ro', uri=True)
    content, completed, config_path, sha = src.execute('select content, completed, config, request_sha256 from answers where input_id=?', (input_id,)).fetchone()
    item, uni, setting, schema, request, cfg = bench.build(input_id, config_path)
    assert model.request_identity(request)[1] == sha, f'{input_id}: stored request differs from the rebuilt one'
    answer = json.loads(content)
    start = time.monotonic()
    response, new_content, ok, error, tin, tout = None, None, 0, None, None, None
    if not answer.get('evidence'):
        new_content, ok = content, completed
    else:
        body = copy.deepcopy(request)
        body['response_format'] = SCHEMA
        body['messages'] = request['messages'] + [{'role': 'assistant', 'content': content}, {'role': 'user', 'content': QUESTION}]
        try:
            response = model.openai_transport(cfg.provider, body)
            verdicts = {v['id']: v['keep'] for v in json.loads(response['choices'][0]['message']['content'])['verdicts']}
            dropped = {e['id'] for e in answer['evidence'] if verdicts.get(e['id']) is False}
            reviewed = dict(answer, evidence=[e for e in answer['evidence'] if e['id'] not in dropped])
            new_content, ok = json.dumps(reviewed, ensure_ascii=False), completed
            tin, tout = response.get('usage', {}).get('prompt_tokens'), response.get('usage', {}).get('completion_tokens')
        except Exception as exc:  # noqa: BLE001
            error = type(exc).__name__
    with LOCK:
        conn = store(target)
        conn.execute('insert or replace into answers values (?,?,?,?,?,?,?,?,?,?)', (input_id, config_path, sha, json.dumps(response), new_content, ok,
                                                                                    tin, tout, round(time.monotonic() - start, 2), error))
        conn.commit()
        conn.close()
    print(input_id[:30], 'ok' if ok else f'INCOMPLETE {error}', flush=True)


if __name__ == '__main__':
    source, target, ids = sys.argv[1], sys.argv[2], sys.argv[3:]
    if ids and ids[0].startswith('--question='):
        QUESTION = QUESTIONS[ids[0].split('=', 1)[1]]
        ids = ids[1:]
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for d in (1, 2, 3):
            list(pool.map(lambda i: one(f'{source}-d{d}', f'{target}-d{d}', i), ids))
