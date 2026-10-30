"""One-change prompt arms on gpt-6-luna (D234), each beside one shared fresh control (AGENTS §6).

Every arm replaces exactly one sentence of the extraction system text as production builds it (role-v22, poc-v38, the
production request bytes otherwise unchanged); no prompt file is edited. The control is the unchanged request. All jobs
(control and arms) are shuffled together and sent in one window, so no condition runs at a different time. Three draws.
Answers go through the production sift exactly as in haiku_week.py.

    python3 luna_arms.py plan     # $0: each old sentence found once in every request it edits, sizes, page lists
    python3 luna_arms.py send     # eight threads; luna-arms-2026-10-29/answers.sqlite
    python3 luna_arms.py sift     # production sift -> luna-arms-2026-10-29/sifted.json
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
from hivemind import extraction, model  # noqa: E402

RUN = HERE / 'luna-arms-2026-10-29'
DRAWS = 3
SEED = 20261029

QUESTION_PAGES = [6, 24, 34, 377, 7, 140, 260, 381] + [3, 15, 39, 69, 146, 180, 198, 111]          # ruled-out pages + guards
JUNK_PAGES = [355, 357, 200, 382, 378, 396, 4] + [381, 277, 79, 6, 210, 83] + [15, 37, 39, 312, 41, 146, 69]   # nothing-to-keep, partner, guards

ARMS = {
    # the standard's first test (§6, "值得追") is absent from the request; Luna opened amounts of a completed or unsized stake
    'A1': {'failure': 'questions whose outcome changes no revenue, profit, cash/credit risk or competitive position',
           'edit': ('Open a candidate only for one of four reasons, named in opens_as.',
                    'Open a candidate only when you can name the revenue, profitability, cash or credit risk, or competitive position its outcome changes (a large number alone is no reason), and only for one of four reasons, named in opens_as.'),
           'pages': QUESTION_PAGES},
    # the same failure, as a closed list in the existing "do not propose" sentence instead of a test
    'A2': {'failure': 'as A1, written as excluded kinds',
           'edit': ('routine litigation procedure, or buyback authorisations.',
                    'routine litigation procedure, buyback authorisations, an amount already fixed when the item appears, a stake whose size is not stated, or another party\'s licence, court case or bill that does not decide what the company may sell.'),
           'pages': QUESTION_PAGES},
    # the repetition clause tells the model to keep a release's performance figures as separate evidence items
    'C1': {'failure': 'product and benchmark figures kept as evidence',
           'edit': (', its figures ("up to 10x faster"; "40 data centers in 15 countries") a second and third', ''),
           'pages': JUNK_PAGES},
    # kind (2) admits any action of any customer, supplier, competitor or partner that has a size, date or name
    'C2': {'failure': "partners' and competitors' own business kept as evidence",
           'edit': ('(2) A customer\'s, supplier\'s, competitor\'s or partner\'s action with a size, date or name:',
                    '(2) A customer\'s, supplier\'s, competitor\'s or partner\'s action with a size, date or name that involves the company, its products or their market:'),
           'pages': JUNK_PAGES},
    # the reject list names the conditional valuation the standard keeps (§10.1); worked on Haiku (D232)
    'V': {'failure': 'conditional valuation dropped (w108-4, w209-4)',
          'edit': ('an author\'s general risks or valuation arithmetic ("if AI pulls back it would hurt"; "at 34 times earnings the stock is worth $305")',
                   'an author\'s general risks ("if AI pulls back it would hurt")'),
          'pages': [108, 209, 177, 141, 267, 196]},
    # the summary need not name a measure given in a neighbouring sentence; worked on Haiku (D232)
    'G': {'failure': "'revenue' dropped from the 82% growth forecast (w209-2)",
          'edit': ('who did or said what, how much and for which period.',
                   'who did or said what, how much and for which period, naming the measure even when a neighbouring sentence gives it.'),
          'pages': [209, 146]},
}


def input_ids():
    manifest = json.loads((hw.RUN / 'manifest.json').read_text())
    return {e['call_id']: e['input_id'] for e in manifest['items'] if e['call_id'] is not None}


def control_pages():
    return sorted({p for arm in ARMS.values() for p in arm['pages']})


def request(arm, input_id):
    item, uni, setting, schema, req, cfg = hw.build(input_id)
    req = copy.deepcopy(req)
    assert req['messages'][0]['role'] == 'system'
    if arm != 'control':
        old, new = ARMS[arm]['edit']
        system = req['messages'][0]['content']
        assert system.count(old) == 1, (arm, input_id)
        req['messages'][0]['content'] = system.replace(old, new)
    return item, uni, schema, req, cfg


def plan():
    ids = input_ids()
    base = request('control', ids[209])[3]['messages'][0]['content']
    print('control system text', len(base), 'characters')
    for name, arm in ARMS.items():
        for page in arm['pages']:
            request(name, ids[page])
        old, new = arm['edit']
        print(f'{name}: {arm["failure"]} | {len(arm["pages"])} pages | {len(new) - len(old):+d} characters')
    edited = [arm['edit'][0] for arm in ARMS.values()]
    assert all(base.count(e) == 1 for e in edited)
    for i, a in enumerate(edited):          # no two arms touch overlapping text: each arm is one variable
        for b in edited[i + 1:]:
            assert a == b or (a not in b and b not in a), (a[:30], b[:30])
    print('control pages', len(control_pages()), '| calls', DRAWS * (len(control_pages()) + sum(len(a['pages']) for a in ARMS.values())))


def store():
    RUN.mkdir(exist_ok=True)
    conn = sqlite3.connect(RUN / 'answers.sqlite')
    conn.execute('create table if not exists answers (arm text, draw integer, input_id text, system_chars integer, response_json text,'
                 ' content text, completed integer, input_tokens integer, output_tokens integer, seconds real, error text,'
                 ' primary key (arm, draw, input_id))')
    return conn


def one(job):
    arm, draw, input_id = job
    item, uni, schema, req, cfg = request(arm, input_id)
    start = time.monotonic()
    response, content, completed, error, tin, tout = None, None, 0, None, None, None
    try:
        response = model.openai_transport(cfg.provider, req)      # the bytes production sends, one sentence changed
        choice = response['choices'][0]
        completed = int(choice['finish_reason'] == 'stop')
        content = choice['message'].get('content') or ''
        tin, tout = response.get('usage', {}).get('prompt_tokens'), response.get('usage', {}).get('completion_tokens')
    except Exception as exc:  # noqa: BLE001  (a paid answer is never lost to a bookkeeping error)
        error = type(exc).__name__ + (f' {exc.code}' if hasattr(exc, 'code') else '')
    with hw.LOCK:
        conn = store()
        conn.execute('insert or replace into answers values (?,?,?,?,?,?,?,?,?,?,?)', (arm, draw, input_id, len(req['messages'][0]['content']),
                                                                                    json.dumps(response), content, completed, tin, tout,
                                                                                    round(time.monotonic() - start, 2), error))
        conn.commit()
        conn.close()
    print(arm, draw, input_id[:30], 'ok' if completed else f'INCOMPLETE {error}', flush=True)


def send():
    ids = input_ids()
    conn = store()
    done = {tuple(r) for r in conn.execute('select arm, draw, input_id from answers where completed=1')}
    conn.close()
    jobs = [('control', d, ids[p]) for p in control_pages() for d in range(1, DRAWS + 1)]
    jobs += [(name, d, ids[p]) for name, arm in ARMS.items() for p in arm['pages'] for d in range(1, DRAWS + 1)]
    jobs = [j for j in jobs if j not in done]
    random.Random(SEED).shuffle(jobs)          # control and arms interleaved in one window
    print('sending', len(jobs), 'calls', flush=True)
    with concurrent.futures.ThreadPoolExecutor(hw.WORKERS) as pool:
        list(pool.map(one, jobs))
    conn = store()
    for row in conn.execute('select arm, count(*), sum(completed), sum(input_tokens), sum(output_tokens) from answers group by arm'):
        print(row, 'usd', round((row[3] or 0) / 1e6 * 0.10 + (row[4] or 0) / 1e6 * 0.50, 4))


def sift():
    conn = store()
    out = {}
    for arm, draw, input_id, content, completed, error in conn.execute('select arm, draw, input_id, content, completed, error from answers'):
        item, uni, schema, req, cfg = request(arm, input_id)
        record = {'completed': bool(completed), 'error': error, 'answer': None, 'schema_errors': None, 'sift': None}
        try:
            record['answer'] = json.loads(content) if content else None
        except ValueError:
            pass
        if record['answer'] is not None:
            record['schema_errors'] = model.check_schema(record['answer'], schema)
            if completed and not record['schema_errors']:
                e, c, d, g = extraction.sift_with_groups(record['answer'], item, item['text'], set(), uni, english=True, shown_group_ids=(),
                                                         version='22', keep_unlinked=True)
                record['sift'] = {'evidence': e, 'candidates': c, 'dropped': d, 'new_groups': g}
        out.setdefault(f'{arm}-{draw}', {})[input_id] = record
    (RUN / 'sifted.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print('sifted', sum(len(v) for v in out.values()), 'answers')


if __name__ == '__main__':
    {'plan': plan, 'send': send, 'sift': sift}[sys.argv[1]]()
