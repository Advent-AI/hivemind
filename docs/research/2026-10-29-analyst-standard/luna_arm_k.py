"""Arm K on gpt-6-luna: the main_driver sentence names a product generation's launch or ship date (the probe of
luna-probes-2026-10-29: no opening reason fits a dated product milestone, so Luna opens the Kyber question 11 of 27 times;
every launch or shipment question either model wrote is labelled main_driver). One sentence changed; its own fresh control
on the same pages, shuffled together in one window; a separate store so the running luna_arms.py send is not touched.

    python3 luna_arm_k.py plan | send | sift
"""
import concurrent.futures
import copy
import json
from pathlib import Path
import random
import sqlite3
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import haiku_week as hw  # noqa: E402
import luna_arms as la  # noqa: E402
from hivemind import extraction, model  # noqa: E402

RUN = HERE / 'luna-arm-k-2026-10-29'
KYBER_PAGES = [180, 195, 198, 274, 276, 288, 300, 315, 383]
GUARD_PAGES = [377, 380, 371, 356, 109, 140]      # product news whose reference rules out a launch, roadmap or adoption question
OLD = ("main_driver: an annual quantity that carries the company's value (the segment that carries the business, gross margin, "
       "capital spending), whether or not the company guides it; the question's ranges settle it, not a guidance figure.")
NEW = ("main_driver: an annual quantity that carries the company's value (the segment that carries the business, gross margin, "
       "capital spending), whether or not the company guides it, or the date by which the product generation that carries it "
       "launches or ships; the question's ranges settle it, not a guidance figure.")


def request(arm, input_id):
    item, uni, setting, schema, req, cfg = hw.build(input_id)
    req = copy.deepcopy(req)
    if arm == 'K':
        system = req['messages'][0]['content']
        assert system.count(OLD) == 1, input_id
        req['messages'][0]['content'] = system.replace(OLD, NEW)
    return item, uni, schema, req, cfg


def plan():
    ids = la.input_ids()
    for page in KYBER_PAGES + GUARD_PAGES:
        request('K', ids[page])
    print('K', f'{len(NEW) - len(OLD):+d} characters;', len(KYBER_PAGES + GUARD_PAGES), 'pages;', 2 * 3 * len(KYBER_PAGES + GUARD_PAGES), 'calls')


def store():
    RUN.mkdir(exist_ok=True)
    conn = sqlite3.connect(RUN / 'answers.sqlite')
    conn.execute('create table if not exists answers (arm text, draw integer, input_id text, response_json text, content text,'
                 ' completed integer, input_tokens integer, output_tokens integer, seconds real, error text, primary key (arm, draw, input_id))')
    return conn


def one(job):
    arm, draw, input_id = job
    item, uni, schema, req, cfg = request(arm, input_id)
    start = time.monotonic()
    response, content, completed, error, tin, tout = None, None, 0, None, None, None
    try:
        response = model.openai_transport(cfg.provider, req)
        choice = response['choices'][0]
        completed = int(choice['finish_reason'] == 'stop')
        content = choice['message'].get('content') or ''
        tin, tout = response.get('usage', {}).get('prompt_tokens'), response.get('usage', {}).get('completion_tokens')
    except Exception as exc:  # noqa: BLE001
        error = type(exc).__name__
    with hw.LOCK:
        conn = store()
        conn.execute('insert or replace into answers values (?,?,?,?,?,?,?,?,?,?)', (arm, draw, input_id, json.dumps(response), content, completed,
                                                                                  tin, tout, round(time.monotonic() - start, 2), error))
        conn.commit()
        conn.close()
    print(arm, draw, input_id[:30], 'ok' if completed else f'INCOMPLETE {error}', flush=True)


def send():
    ids = la.input_ids()
    conn = store()
    done = {tuple(r) for r in conn.execute('select arm, draw, input_id from answers where completed=1')}
    conn.close()
    jobs = [(arm, d, ids[p]) for arm in ('control', 'K') for p in KYBER_PAGES + GUARD_PAGES for d in (1, 2, 3)]
    jobs = [j for j in jobs if j not in done]
    random.Random(la.SEED).shuffle(jobs)
    print('sending', len(jobs), flush=True)
    with concurrent.futures.ThreadPoolExecutor(4) as pool:
        list(pool.map(one, jobs))
    conn = store()
    for row in conn.execute('select arm, count(*), sum(completed), sum(input_tokens), sum(output_tokens) from answers group by arm'):
        print(row, 'usd', round((row[3] or 0) / 1e6 * 0.10 + (row[4] or 0) / 1e6 * 0.50, 4))


def sift():
    conn = store()
    out = {}
    for arm, draw, input_id, content, completed in conn.execute('select arm, draw, input_id, content, completed from answers'):
        item, uni, schema, req, cfg = request(arm, input_id)
        answer = json.loads(content) if content else None
        rec = {'answer': answer, 'sift': None}
        if answer is not None and completed and not model.check_schema(answer, schema):
            e, c, d, g = extraction.sift_with_groups(answer, item, item['text'], set(), uni, english=True, shown_group_ids=(), version='22', keep_unlinked=True)
            rec['sift'] = {'evidence': e, 'candidates': c, 'dropped': d}
        out.setdefault(f'{arm}-{draw}', {})[input_id] = rec
    (RUN / 'sifted.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print('sifted', sum(len(v) for v in out.values()))


if __name__ == '__main__':
    {'plan': plan, 'send': send, 'sift': sift}[sys.argv[1]]()
