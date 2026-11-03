"""One-change prompt arms on Haiku 5.5 against the D229 measurement's failures, each beside a fresh control (AGENTS §6).

Every arm edits one sentence of the extraction system text (role-v22 as production builds it) and is sent on the week pages
that showed its failure, plus guard pages where the same sentence must not break a passing item; the control is the
unchanged request on the union of those pages, sent in the same session. Three draws each, Haiku at the 16k cap (D230).
Answers go through the production sift exactly as in haiku_week.py.

    python3 arm_week.py plan      # $0: every old sentence found once in every request, sizes before/after, synthetic ladder check
    python3 arm_week.py send      # control and arms, eight threads; stored in arms-2026-10-29/answers.sqlite
    python3 arm_week.py sift      # production sift -> arms-2026-10-29/sifted.json
"""
import concurrent.futures
import json
from pathlib import Path
import sqlite3
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import haiku_week as hw  # noqa: E402
from hivemind import extraction, model  # noqa: E402

RUN = HERE / 'arms-2026-10-29'
DRAWS = 3

ARMS = {
    # role-v22 rejects the conditional valuation the standard keeps (§10.1); the model quoted this clause as its reason (probe valuation-108)
    'V': {'failure': 'conditional valuation dropped (w108-4, w209-4)',
          'edit': ('an author\'s general risks or valuation arithmetic ("if AI pulls back it would hurt"; "at 34 times earnings the stock is worth $305")',
                   'an author\'s general risks ("if AI pulls back it would hurt")'),
          'pages': [108, 209, 177, 141, 267, 196]},
    # the fiscal-year note's annual-report date was taken for a Kyber event (probe due-180)
    'D': {'failure': 'Kyber event questions due before the 2027 plan or the 2028 slip can show',
          'edit': ('For an event, name the date at which its outcome is assessed.',
                   'For an event, name the date by which the timing the item states or reports can be checked; the fiscal-year note\'s date is for annual figures only.'),
          'pages': [180, 195, 198, 274, 276, 288, 300, 315, 383]},
    # opens_as definitions admit any policy process or any financing, whether or not it bears on a subject (probes policy-277, debt-34)
    'Q': {'failure': 'questions whose answer changes no view of a listed subject (Valar/NRC, Singapore charges, lidar bills, debt raise, IREN)',
          'edit': ('Open a candidate only for one of four reasons, named in opens_as.',
                   'Open a candidate only when its answer would change a view of a listed subject, and only for one of four reasons, named in opens_as.'),
          'pages': [7, 34, 35, 88, 107, 277, 312, 379, 381, 395, 356, 358, 3, 15, 39, 69, 146, 180]},
    # the model left the metric out because the 82% sentence does not name it (probe g01-metric)
    'G': {'failure': "'revenue' dropped from the 82% growth forecast (w209-2)",
          'edit': ('who did or said what, how much and for which period.',
                   'who did or said what, how much and for which period, naming the measure even when a neighbouring sentence gives it.'),
          'pages': [209, 146]},
    # obligation amount ladders labelled as neutral bands are refused by the asset-label check (5 obligation questions lost)
    'L': {'failure': 'obligation amount questions refused by the sift for neutral rung labels',
          'edit': ('A five-rung asset ladder runs from Strongly bullish',
                   'A five-rung asset ladder, which every candidate whose object is a ticker has (an obligation amount too), runs from Strongly bullish'),
          'pages': [3, 15, 37, 39, 82, 111, 143, 210, 262]},
}


def input_ids():
    manifest = json.loads((hw.RUN / 'manifest.json').read_text())
    return {e['call_id']: e['input_id'] for e in manifest['items'] if e['call_id'] is not None}


def control_pages():
    return sorted({p for arm in ARMS.values() for p in arm['pages']})


def request(arm, input_id):
    item, uni, setting, schema, req, cfg = hw.build(input_id)
    body = hw.to_haiku(req, schema)
    if arm != 'control':
        old, new = ARMS[arm]['edit']
        assert body['system'].count(old) == 1, (arm, input_id)
        body['system'] = body['system'].replace(old, new)
    return item, uni, schema, body


def plan():
    ids = input_ids()
    any_system = request('control', ids[209])[3]['system']
    print('control system text', len(any_system), 'characters')
    for name, arm in ARMS.items():
        for page in arm['pages']:
            request(name, ids[page])
        old, new = arm['edit']
        print(name, arm['failure'], '| pages', len(arm['pages']), '| characters', len(any_system), '->', len(any_system) - len(old) + len(new),
              f'({len(new) - len(old):+d})')
    # a prompt-conformant obligation candidate (arm L) through the ladder check the sift applies
    labels = ['Strongly bullish', 'Bullish', 'Neutral', 'Bearish', 'Strongly bearish']
    rungs = [{'label': l, 'condition': f'band {i}', 'lo': None if i == 0 else i * 1e9, 'hi': None if i == 4 else (i + 1) * 1e9} for i, l in enumerate(labels)]
    print('synthetic obligation ladder, asset kind:', extraction.check_ladder(rungs, 'asset') or 'passes')
    print('control pages', len(control_pages()), '; calls', DRAWS * (len(control_pages()) + sum(len(a['pages']) for a in ARMS.values())))


def store():
    RUN.mkdir(exist_ok=True)
    conn = sqlite3.connect(RUN / 'answers.sqlite')
    conn.execute('create table if not exists answers (arm text, draw integer, input_id text, system_chars integer, response_json text,'
                 ' content text, completed integer, input_tokens integer, output_tokens integer, seconds real, error text,'
                 ' primary key (arm, draw, input_id))')
    return conn


def one(job):
    arm, draw, input_id = job
    item, uni, schema, body = request(arm, input_id)
    start = time.monotonic()
    response, content, completed, error, tin, tout = None, None, 0, None, None, None
    try:
        response = hw.haiku_api('https://api.anthropic.com/v1/messages', body)
        completed = int(response.get('stop_reason') == 'end_turn')
        content = ''.join(c.get('text', '') for c in response.get('content', []) if c.get('type') == 'text')
        tin, tout = response.get('usage', {}).get('input_tokens'), response.get('usage', {}).get('output_tokens')
    except Exception as exc:  # noqa: BLE001  (a paid answer is never lost to a bookkeeping error)
        error = type(exc).__name__ + (f' {exc.code}' if hasattr(exc, 'code') else '')
    with hw.LOCK:
        conn = store()
        conn.execute('insert or replace into answers values (?,?,?,?,?,?,?,?,?,?,?)', (arm, draw, input_id, len(body['system']), json.dumps(response),
                                                                                    content, completed, tin, tout, round(time.monotonic() - start, 2), error))
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
        item, uni, schema, body = request(arm, input_id)
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
