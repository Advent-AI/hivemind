"""The model's own account (AGENTS §1) of why gpt-6-luna opened no candidate on the Kyber-delay articles of 2026-07-05..07.

Each case continues the stored Luna conversation: the production system and user messages rebuilt byte-identical by
haiku_week.build (sha256 checked against the stored answer), the stored answer as the assistant turn, then one question.
Model and reasoning_effort are the production request's; the JSON response format is removed so the model answers in prose;
max_completion_tokens is lowered to 3000. Every request body (no credentials) and reply goes to probes.sqlite in this folder.

    python3 probe.py          # sends the cases that have no stored reply; prints cost at $0.10 / $0.50 per million tokens
"""
import concurrent.futures
import copy
import json
from pathlib import Path
import sqlite3
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import haiku_week as hw  # noqa: E402
from hivemind import model  # noqa: E402

DB = HERE / 'probes.sqlite'
ANSWERS = hw.RUN / 'answers.sqlite'
PRICE_IN, PRICE_OUT = 0.10, 0.50   # USD per million tokens, as instructed for this probe
MAX_COMPLETION_TOKENS = 3000
WORKERS = 8

NO_CANDIDATE = ("You opened no candidate about the timing of the Kyber rack (the reported slip from 2027 to 2028 and NVIDIA's denial). "
                "Which instruction led you there? Quote the instruction text you followed, then say which statements in the item you "
                "considered for a candidate and set aside.")
RUBIN_INSTEAD = ("You opened a candidate on current-generation Rubin shipping but none on the Kyber rack's reported slip from 2027 to 2028. "
                 "Which instruction led you there? Quote the instruction text you followed, then say which statements you considered "
                 "and set aside.")

# case_id, call id, input_id, stored Luna draw, question
CASES = [
    ('k195-d1', 195, 'gnews:68a3ed21f77b935d9fa7ec5e', 1, NO_CANDIDATE),
    ('k195-d2', 195, 'gnews:68a3ed21f77b935d9fa7ec5e', 2, NO_CANDIDATE),
    ('k288-d1', 288, 'gnews:d4c5dc540392f8df39aee250', 1, NO_CANDIDATE),
    ('k300-d1', 300, 'gnews:c0432377817a1c00a1bbadf0', 1, NO_CANDIDATE),
    ('k276-d1', 276, 'gnews:d5c48abb470f394f86549b6b', 1, NO_CANDIDATE),
    ('k315-d2', 315, 'gnews:c75f16a6d64cc27fc28fb571', 2, NO_CANDIDATE),
    ('k383-d2', 383, 'gnews:295fceb25273abae9bb6c995', 2, NO_CANDIDATE),
    ('k180-d1', 180, 'gnews:552f8c2bdfd080555d592587', 1, RUBIN_INSTEAD),
]


def store():
    conn = sqlite3.connect(DB)
    conn.execute('create table if not exists probes (case_id text primary key, call_id integer, input_id text, draw integer,'
                 ' original_request_sha256 text, question text, request_json text, response_json text, reply text,'
                 ' finish_reason text, input_tokens integer, cached_input_tokens integer, output_tokens integer,'
                 ' reasoning_tokens integer, cost_usd real, seconds real, error text)')
    return conn


def body_for(input_id, draw, question):
    item, uni, setting, schema, request, cfg = hw.build(input_id)
    sha = model.request_identity(request)[1]
    source = sqlite3.connect(f'file:{ANSWERS}?mode=ro', uri=True)
    stored_sha, content = source.execute("select request_sha256, content from answers where provider='luna' and draw=? and input_id=?",
                                         (draw, input_id)).fetchone()
    source.close()
    assert stored_sha == sha, (input_id, draw, 'rebuilt request differs from the stored one')
    body = copy.deepcopy(request)
    del body['response_format']
    body['max_completion_tokens'] = MAX_COMPLETION_TOKENS
    body['messages'] = request['messages'] + [{'role': 'assistant', 'content': content}, {'role': 'user', 'content': question}]
    return sha, body, cfg.provider


def one(case):
    case_id, call_id, input_id, draw, question = case
    sha, body, provider = body_for(input_id, draw, question)
    start = time.monotonic()
    response = reply = finish = error = None
    tin = cached = tout = reasoning = None
    cost = None
    try:
        response = model.openai_transport(provider, body)   # reads its own credentials
        choice = response['choices'][0]
        reply, finish = choice['message'].get('content'), choice.get('finish_reason')
        usage = response.get('usage', {})
        tin, tout = usage.get('prompt_tokens'), usage.get('completion_tokens')
        cached = (usage.get('prompt_tokens_details') or {}).get('cached_tokens')
        reasoning = (usage.get('completion_tokens_details') or {}).get('reasoning_tokens')
        cost = (tin * PRICE_IN + tout * PRICE_OUT) / 1e6
    except Exception as failure:   # stored with the case, never retried silently
        error = repr(failure)[:600]
    conn = store()
    conn.execute('insert or replace into probes values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                 (case_id, call_id, input_id, draw, sha, question, json.dumps(body, ensure_ascii=False),
                  None if response is None else json.dumps(response, ensure_ascii=False), reply, finish, tin, cached, tout, reasoning,
                  cost, round(time.monotonic() - start, 2), error))
    conn.commit()
    conn.close()
    return case_id, finish, tin, tout, cost, error


def main():
    conn = store()
    done = {r[0] for r in conn.execute('select case_id from probes where error is null')}
    conn.close()
    todo = [c for c in CASES if c[0] not in done]
    for case in todo:   # every body is built and checked before the first send
        body_for(case[2], case[3], case[4])
    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        for result in pool.map(one, todo):
            print('probed', *result, flush=True)
    conn = store()
    n, tin, tout, cost = conn.execute('select count(*), sum(input_tokens), sum(output_tokens), sum(cost_usd) from probes').fetchone()
    print(f'{n} probes stored; input {tin} tokens, output {tout} tokens; cost ${cost:.4f}')


if __name__ == '__main__':
    main()
