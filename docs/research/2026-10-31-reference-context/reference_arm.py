"""Research harness for design.md: the production extraction request of a configuration (bench_v23.build, the bytes production sends)
with, in the arm, an [Open questions as of <day>] block before the item and one instruction sentence, the questions taken from the sealed
three-month ledger as they stood at the end of the day before the article's publication day (views created at or before that day's
days_completed.seq; the ledger holds no closures). The control is the unchanged request. Answers are stored like loop.py's, under
docs/research/2026-10-29-analyst-standard/loop-2026-10-29/<tag>/answers.sqlite, so final_scores.py and score_gold.py read them.
Production code and prompt files are untouched.

    python3 reference_arm.py plan                       # $0: list sizes per article, one sample request, nothing sent
    python3 reference_arm.py send REF-v53-d1 control    # three draws each: REF-v53-d{1,2,3} control, REF-v53R-d{1,2,3} arm
    python3 reference_arm.py send REF-v53R-d1 arm
"""
import concurrent.futures
import copy
import json
import sqlite3
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LOOP = ROOT / 'docs/research/2026-10-29-analyst-standard'
LEDGER = ROOT / 'docs/research/2026-10-29-ledger-standard'
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'poc'), str(LOOP)]
import bench_v23 as bench  # noqa: E402
from hivemind import model  # noqa: E402

CONFIG = str(ROOT / 'poc/config/poc-v69.json')
VIEWS = '/Users/lchingen/hivemind/poc/data/sealed-2026-10-28-v34-nvda-3m-through-0828/views.sqlite'
GOLD = LEDGER / 'golden-v5/golden-v5-dev.json'
INSTRUCTION = ('In links, name the open question(s) this statement makes more or less likely by id, or your own candidate\'s id; leave it empty when '
               'it moves none. Write a candidate only for a question the list does not cover: another wording, deadline or milestone of a listed '
               'question is that question, not a new one.')
LINKS_NOTE = 'Ids of the open questions this statement makes more or less likely (from the [Open questions] list), or of your own candidates; empty when none.'
LOCK = threading.Lock()


def open_questions_before(day):
    """The ledger's questions open at the end of the day before `day`: created at or before that day's completed seq."""
    db = sqlite3.connect(f'file:{VIEWS}?mode=ro', uri=True)
    row = db.execute('select max(seq) from days_completed where day < ?', (day,)).fetchone()
    if row[0] is None:
        return []
    return [dict(view_id=v, kind=k, object_id=o, question=q, due_day=d)
            for v, k, o, q, d in db.execute('select view_id, kind, object_id, question, due_day from views where created_seq <= ? order by created_seq', (row[0],))]


def block(day, questions):
    lines = [f'  - {q["view_id"]} ({q["kind"]} {q["object_id"]}, due {q["due_day"]}): {q["question"]}' for q in questions]
    body = '\n'.join(lines) if lines else '  None yet.'
    return f'[Open questions as of {day}] {INSTRUCTION}\n{body}'


def arm_request(request, item):
    body = copy.deepcopy(request)
    user = body['messages'][-1]['content']
    marker = '[Item] id '
    at = user.index(marker)
    before = (sqlite3.connect(f'file:{VIEWS}?mode=ro', uri=True).execute('select max(day) from days_completed where day < ?', (item['publication_day'],)).fetchone()[0]) or item['publication_day']
    body['messages'][-1] = dict(body['messages'][-1], content=user[:at] + block(before, open_questions_before(item['publication_day'])) + '\n\n' + user[at:])
    fields = body['response_format']['json_schema']['schema']['properties']['evidence']['items']['properties']
    fields['links'] = dict(fields['links'], description=LINKS_NOTE)
    return body


def store(tag):
    (LOOP / 'loop-2026-10-29' / tag).mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(LOOP / 'loop-2026-10-29' / tag / 'answers.sqlite')
    conn.execute('create table if not exists answers (input_id text primary key, config text, request_sha256 text, response_json text, content text,'
                 ' completed integer, input_tokens integer, output_tokens integer, seconds real, error text)')
    return conn


def one(tag, mode, input_id):
    item, uni, setting, schema, request, cfg = bench.build(input_id, CONFIG)
    body = arm_request(request, item) if mode == 'arm' else request
    start = time.monotonic()
    response, content, completed, error, tin, tout = None, None, 0, None, None, None
    try:
        response = model.openai_transport(cfg.provider, body)
        choice = response['choices'][0]
        completed = int(choice['finish_reason'] == 'stop')
        content = choice['message'].get('content') or ''
        tin, tout = response.get('usage', {}).get('prompt_tokens'), response.get('usage', {}).get('completion_tokens')
    except Exception as exc:  # noqa: BLE001
        error = type(exc).__name__
    with LOCK:
        conn = store(tag)
        conn.execute('insert or replace into answers values (?,?,?,?,?,?,?,?,?,?)', (input_id, CONFIG, model.request_identity(body)[1], json.dumps(response),
                                                                                    content, completed, tin, tout, round(time.monotonic() - start, 2), error))
        conn.commit()
        conn.close()
    print(input_id[:30], 'ok' if completed else f'INCOMPLETE {error}', flush=True)


def dev_ids():
    return [a['input_id'] for a in json.loads(GOLD.read_text())['articles']]


if __name__ == '__main__':
    if sys.argv[1] == 'plan':
        sizes = {}
        for iid in dev_ids():
            item, *_ = bench.build(iid, CONFIG)
            sizes[iid] = len(open_questions_before(item['publication_day']))
        from collections import Counter
        print('articles by list size:', sorted(Counter(sizes.values()).items()))
        sample = next(i for i, n in sizes.items() if n >= 10)
        item, uni, setting, schema, request, cfg = bench.build(sample, CONFIG)
        arm = arm_request(request, item)
        user = arm['messages'][-1]['content']
        at = user.index('[Open questions')
        print('\n--- sample arm block for', sample, item['publication_day'], '---\n' + user[at:user.index('[Item] id ')])
        print('control user chars', len(request['messages'][-1]['content']), 'arm user chars', len(user), '| schema identical except links note:',
              json.dumps(arm['response_format'], sort_keys=True).replace(LINKS_NOTE, '') != json.dumps(request['response_format'], sort_keys=True))
        (HERE / 'list-sizes.json').write_text(json.dumps(sizes, indent=1))
    elif sys.argv[1] == 'send':
        tag, mode = sys.argv[2], sys.argv[3]
        done = {r[0] for r in store(tag).execute('select input_id from answers where completed=1')}
        todo = [i for i in dev_ids() if i not in done]
        print('sending', len(todo), 'as', mode, 'under', tag, flush=True)
        with concurrent.futures.ThreadPoolExecutor(8) as pool:
            list(pool.map(lambda i: one(tag, mode, i), todo))
        print(f'DONE {tag}', flush=True)
