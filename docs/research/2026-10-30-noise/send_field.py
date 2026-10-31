"""Cheapest proof for a structural keep test (AGENTS §1 step 4): the production request of a configuration, with one required field put
first in each evidence item so the model writes the keep test's answer before the quote. Research harness only: production code and
prompts are unchanged. The answer is stored with the field removed (so the production sift and the scorers read it unchanged); the full
response, field included, is in response_json.

    python3 send_field.py <tag> <config> [--note=plain|anchored] [--verdict | --review | --tail | --tail2] <input_id ...>
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

FIELD = 'noted_because'
NOTES = {
    # F1: the keep test as standard 5.1 words it ("which question's answer does it change"; "is it new")
    'plain': ('Write this before the quote: what is new in the statement (a fresh event, figure or specific judgement) and the question whose '
              'answer it makes more or less likely, named. When you cannot name both, the statement is not material: leave it out.'),
    # F2: the question anchored to the analyst's key judgements (standard §6 关键判断; AGENTS §8: revenue, profitability, cash risk or
    # competitive position), because under F1 the model named a question about the statement itself (a server's opening, a game's feature)
    'anchored': ('Write this before the quote: the analyst question this statement moves and what is new in it. The question must be one '
                 "an analyst following the company bets on: its revenue, margins, cash or credit risk, demand for its products, the progress "
                 "of the product generation that carries its value, the supply or price of its key inputs, or its competitive position. A "
                 'question about the statement itself (whether one store opens on time, what one manager is paid, whether an app gains a '
                 'feature) is not one. When you cannot name such a question, leave the statement out.'),
}
NOTE = NOTES['plain']
# F3: the keep verdict written after the item, as the model gave it when asked afterwards in a second turn (4 of 4 noise items "no");
# items it marks "no" are discarded before storing (the model decides; the harness only executes its verdict)
VERDICT = 'analyst_note'
VERDICT_NOTE = ('Now read this item back as the analyst following the company: would you put it in this week\'s notes because it moves a '
                'question about the company\'s revenue, margins, cash or credit risk, demand for its products, the progress of the product '
                'generation that carries its value, its key inputs or its competitive position? "no" for a statement only about itself (one '
                'store opening, one manager\'s pay, an app gaining a feature) or for background the analyst already knew. Items marked "no" '
                'are discarded.')
LOCK = threading.Lock()


MODE = 'before'          # 'before': FIELD first; 'verdict': VERDICT last, "no" items discarded; 'review': a review list after the evidence
# S3: the whole evidence list reviewed in the same answer, after it is written (Alex: "为什么你不在prompt 里面要求做完自己复核一边就好"); the
# review text is the second turn's R3 (review-core-r3.txt); items the review drops are discarded
# T1: Alex, 2026-10-30: "这个完全就是再prompt 的最后面要求做完一遍基于'你刚才说的复核条件'再跑一次；写在同一个提示词里面": the review text
# appended at the very end of the user message, schema unchanged; the model returns only the items it keeps
TAIL = ('Before you return the answer, check it once: read each evidence item back, one by one, as the analyst following the company. '
        + (Path(__file__).resolve().parent / 'review-core-r3.txt').read_text().strip() + ' Return only the evidence items you keep after this check.')
# T2: the review written as a closed set (drop classes by the size of what T1 still kept, each with examples from other industries; a keep
# list for what the reviews dropped wrongly), every clause traced to the standard (review-core-t2.txt); the closing line's
# empty-answer condition (audit N9) is removed so the check may empty a page
TAIL_T2 = (Path(__file__).resolve().parent / 'review-core-t2.txt').read_text().strip()
EMPTY_LINE = ' Return empty arrays only for a page with no business content.'
REVIEW = 'review'
REVIEW_NOTE = ('After the evidence list is complete, read each item back, one by one, as the analyst following the company. '
               + (Path(__file__).resolve().parent / 'review-core-r3.txt').read_text().strip() + ' Give a verdict for every evidence id; items with keep false are discarded.')


def with_field(request):
    body = copy.deepcopy(request)
    item = body['response_format']['json_schema']['schema']['properties']['evidence']['items']
    if MODE == 'verdict':
        item['properties'] = {**item['properties'], VERDICT: {'type': 'string', 'enum': ['yes', 'no'], 'description': VERDICT_NOTE}}
        item['required'] = item['required'] + [VERDICT]
    elif MODE == 'tail':
        body['messages'][-1] = dict(body['messages'][-1], content=body['messages'][-1]['content'] + '\n\n' + TAIL)
    elif MODE == 'tail2':
        user = body['messages'][-1]['content']
        assert user.count(EMPTY_LINE) == 1, 'the closing line is not the one this arm removes'
        body['messages'][-1] = dict(body['messages'][-1], content=user.replace(EMPTY_LINE, '') + '\n\n' + TAIL_T2)
    elif MODE == 'review':
        top = body['response_format']['json_schema']['schema']
        review = {'type': 'array', 'description': REVIEW_NOTE, 'items': {'type': 'object', 'additionalProperties': False, 'required': ['id', 'keep'],
                                                                          'properties': {'id': {'type': 'string'}, 'keep': {'type': 'boolean'}}}}
        props = {}
        for name, prop in top['properties'].items():
            props[name] = prop
            if name == 'evidence':
                props[REVIEW] = review
        top['properties'] = props
        top['required'] = [n for n in props if n in top['required'] or n == REVIEW]
    else:
        item['properties'] = {FIELD: {'type': 'string', 'description': NOTE}, **item['properties']}
        item['required'] = [FIELD] + item['required']
    return body


def store(tag):
    (LOOP / 'loop-2026-10-29' / tag).mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(LOOP / 'loop-2026-10-29' / tag / 'answers.sqlite')
    conn.execute('create table if not exists answers (input_id text primary key, config text, request_sha256 text, response_json text, content text,'
                 ' completed integer, input_tokens integer, output_tokens integer, seconds real, error text)')
    return conn


def one(tag, config_path, input_id):
    item, uni, setting, schema, request, cfg = bench.build(input_id, config_path)
    body = with_field(request)
    start = time.monotonic()
    response, content, completed, error, tin, tout = None, None, 0, None, None, None
    try:
        response = model.openai_transport(cfg.provider, body)
        choice = response['choices'][0]
        completed = int(choice['finish_reason'] == 'stop')
        raw = choice['message'].get('content') or ''
        answer = json.loads(raw)
        if MODE == 'verdict':
            answer['evidence'] = [e for e in answer.get('evidence', []) if e.get(VERDICT) != 'no']
        if MODE == 'review':
            dropped = {v['id'] for v in answer.pop(REVIEW, []) if v.get('keep') is False}
            answer['evidence'] = [e for e in answer.get('evidence', []) if e['id'] not in dropped]
        for e in answer.get('evidence', []):
            e.pop(FIELD, None)
            e.pop(VERDICT, None)
        content = json.dumps(answer, ensure_ascii=False)
        tin, tout = response.get('usage', {}).get('prompt_tokens'), response.get('usage', {}).get('completion_tokens')
    except Exception as exc:  # noqa: BLE001
        error = type(exc).__name__
    with LOCK:
        conn = store(tag)
        conn.execute('insert or replace into answers values (?,?,?,?,?,?,?,?,?,?)', (input_id, config_path, model.request_identity(body)[1], json.dumps(response),
                                                                                    content, completed, tin, tout, round(time.monotonic() - start, 2), error))
        conn.commit()
        conn.close()
    print(input_id[:30], 'ok' if completed else f'INCOMPLETE {error}', flush=True)


if __name__ == '__main__':
    tag, config_path, ids = sys.argv[1], sys.argv[2], sys.argv[3:]
    if ids and ids[0].startswith('--note='):
        NOTE = NOTES[ids[0].split('=', 1)[1]]
        ids = ids[1:]
    if ids and ids[0] == '--verdict':
        MODE = 'verdict'
        ids = ids[1:]
    if ids and ids[0] == '--tail2':
        MODE = 'tail2'
        ids = ids[1:]
    if ids and ids[0] == '--tail':
        MODE = 'tail'
        ids = ids[1:]
    if ids and ids[0] == '--review':
        MODE = 'review'
        ids = ids[1:]
    done = {r[0] for r in store(tag).execute('select input_id from answers where completed=1')}
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        list(pool.map(lambda i: one(tag, config_path, i), [i for i in ids if i not in done]))
