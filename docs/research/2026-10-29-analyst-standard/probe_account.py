"""The model's own account of a stored answer (AGENTS §1): the stored Haiku conversation (same system text, same user text,
the stored assistant turn with its thinking signature) is continued with one question; the reply is stored in
haiku-week/answers.sqlite, table probes. One question per case; the question names what the answer did, not what it should
have done.

    python3 probe_account.py        # sends the cases below that have no stored reply
"""
import concurrent.futures
import json
from pathlib import Path
import sqlite3
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import haiku_week as hw  # noqa: E402

ASK = ' Quote the instruction text you followed, then say which statements in the item you considered for this and set aside.'
CASES = [
    ('g01-metric', 'gnews:71df54965281684cc500960f', 2,
     "In evidence e2 you wrote '(metric not specified in the item)'. Which instruction led you to write that?"),
    ('valuation-108', 'gnews:e4e5f1b5c0c68381e4c486e1', 1,
     "The item says Nvidia's average forward P/E was nearly 34 over two years and applies it to $8.97 of EPS to reach about $305 a share. "
     "You did not record that as evidence. Which instruction led you to leave it out?"),
    ('policy-277', 'gnews:417f6244f0aaa27123023deb', 1,
     "You opened candidate c1 about a court ruling on the NRC's licensing authority over microreactors. Which instruction led you to open it, "
     "and how would its answer change a view of NVDA?"),
    ('debt-34', 'gnews:d1364ee37c17c361ae74f563', 1,
     "You opened a candidate on whether Nvidia completes a debt offering of at least $20 billion. Which instruction led you to open it, "
     "and how would its answer change a view of NVDA?"),
    ('due-180', 'gnews:552f8c2bdfd080555d592587', 3,
     "Your Kyber candidate is due 2027-02-25. Which instruction led you to that due date?"),
    ('obligation-37', 'gnews:3854aeddaa3f31de00cf2816', 1,
     "You opened no binding_obligation candidate for the revenue-sharing and credit-support model the item describes. Which instruction led you there?"),
    ('obligation-111', 'gnews:9e0d5b0d6b3e603c60340128', 2,
     "You opened no candidate for the backstop Nvidia provides under the AI Compute Partnership. Which instruction led you there?"),
]


def store():
    conn = sqlite3.connect(hw.RUN / 'answers.sqlite')
    conn.execute('create table if not exists probes (case_id text primary key, input_id text, draw integer, question text,'
                 ' response_json text, reply text, input_tokens integer, output_tokens integer)')
    return conn


def one(case):
    case_id, input_id, draw, question = case
    conn = store()
    stored = conn.execute("select response_json from answers where provider='haiku' and draw=? and input_id=?", (draw, input_id)).fetchone()
    conn.close()
    original = json.loads(stored[0])
    item, uni, setting, schema, request, cfg = hw.build(input_id)
    first = hw.to_haiku(request, schema)
    body = {'model': hw.HAIKU, 'max_tokens': 4000, 'system': first['system'],
            'messages': [first['messages'][0], {'role': 'assistant', 'content': original['content']},
                         {'role': 'user', 'content': question + ASK}]}
    response = hw.haiku_api('https://api.anthropic.com/v1/messages', body)
    reply = ''.join(c.get('text', '') for c in response.get('content', []) if c.get('type') == 'text')
    usage = response.get('usage', {})
    conn = store()
    conn.execute('insert or replace into probes values (?,?,?,?,?,?,?,?)', (case_id, input_id, draw, question, json.dumps(response), reply,
                                                                          usage.get('input_tokens'), usage.get('output_tokens')))
    conn.commit()
    conn.close()
    return case_id


def main():
    conn = store()
    done = {r[0] for r in conn.execute('select case_id from probes')}
    conn.close()
    todo = [c for c in CASES if c[0] not in done]
    with concurrent.futures.ThreadPoolExecutor(hw.WORKERS) as pool:
        for case_id in pool.map(one, todo):
            print('probed', case_id, flush=True)


if __name__ == '__main__':
    main()
