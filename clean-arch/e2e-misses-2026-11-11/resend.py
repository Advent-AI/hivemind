#!/usr/bin/env python3
"""Re-send saved judge requests of the D392 clean draws as production sends them, several times each, and read the answers through the
frozen judge's own checks. Each send is a fresh answer: no archive stands in between.

A case is (draw, question, day, which): `accepted` is the request whose answer the saved run accepted for that question on that day;
`first` is the day's first request of that question when the check refused its answer and the day re-asked with a note. Both come
from the offline replay of the draw (`poc/data/clean-e2e-misses-2026-11-11/control-d<N>/control-requests.json`, which reproduced every saved
request of the draw). The answers are checked against the draw's ledger as it stood before that day's judging round, rebuilt by the
same replay stopped there.

  resend.py check --case 3 v17 2026-07-08 first [--case ...]         no send: every identity below, the ledgers, the worst cost
  resend.py send  <new folder> --case ... [--sends 3]                 the sends, all cases interleaved and concurrent, one spending limit
  resend.py read  <send folder> --case ...                            each answer through the schema and the frozen check; rungs by case

Checks before any send, each refusing the run: the request's sorted form is the saved archive's request of the accepted answer, byte
for byte; the request as production serializes it (json.dumps in the order model.build_request builds) equals what build_request
builds today from its system and user text; the saved accepted answer passes the frozen check against the rebuilt ledger (positive
control; for a `first` case, the saved refused answer is refused again), and the same answer with a citation of an id the request
does not show is refused (negative control). An answer the check refuses still has its rung read: the refusal is about citations."""
import argparse, concurrent.futures, contextlib, glob, hashlib, json, sqlite3, sys, threading, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT / 'clean-arch/step2-edge-effect-2026-11-10')]
import edge_replay  # noqa: E402  (puts clean-arch/e2e-2026-11-09 and src on the path)
import budget  # noqa: E402
from hivemind import config, model  # noqa: E402
from hivemind.views import judging  # noqa: E402

DATA = ROOT / 'poc/data/clean-e2e-misses-2026-11-11'
# The check's refusals that concern only which ids an answer names (judging.check_answer); a refused answer's rung is read only when
# every reason it was refused for is one of these. A refusal for the rung itself, or for `changed`, leaves the rung uncounted.
CITATION_REASONS = (' is not a dependency of ', ' is not among the evidence shown to ', ' is not a theme in force shown to ',
                    'push on ', ' is named twice in theme_pushes')
CAP_USD = 0.70


def write_new(path, text):
    """Every file the probe writes is created new (exclusive creation): an existing file or a symbolic link at the path refuses the write."""
    with open(path, 'x', encoding='utf-8') as handle:
        handle.write(text)


class StopBeforeRound(Exception):
    pass


def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def saved_first_request(draw, view, day):
    """The day's first request of the question, when its answer was refused: the refused row of the saved archive, and the reason the
    check gives for it."""
    edge_replay.use_draw(draw)
    rounds = json.loads((DATA / f'control-d{draw}' / 'control-rounds.json').read_text())
    entries = [entry for entry in rounds.get(day, []) if entry['view'] == view]
    if len(entries) < 2:
        raise SystemExit(f'draw {draw} asked {view} once on {day}: there is no refused first request')
    first_sha = entries[0]['sha256']
    with contextlib.closing(sqlite3.connect(f"file:{edge_replay.SAVED / 'archive.sqlite'}?mode=ro", uri=True)) as conn:
        rows = conn.execute("select request_sha256, request_json, answer_json from model_calls where request_sha256 like ?", (first_sha + ':refused:%',)).fetchall()
    if len(rows) != 1:
        raise SystemExit(f'draw {draw} {view} {day}: {len(rows)} refused rows for the first request')
    _, request_json, answer_json = rows[0]
    with contextlib.closing(sqlite3.connect(f"file:{edge_replay.SAVED / 'views.sqlite'}?mode=ro", uri=True)) as conn:
        rung = conn.execute('select rung from judgements where view_id=? and publication_day=?', (view, day)).fetchone()[0]
    return {'request_sha256': first_sha, 'rung': rung, 'request_json': request_json, 'answer': json.loads(answer_json)}


def saved_judgement(draw, view, day):
    edge_replay.use_draw(draw)
    with contextlib.closing(sqlite3.connect(f"file:{edge_replay.SAVED / 'views.sqlite'}?mode=ro", uri=True)) as conn:
        row = conn.execute('select request_sha256, rung, seq from judgements where view_id=? and publication_day=?', (view, day)).fetchone()
    if not row:
        raise SystemExit(f'draw {draw} has no judgement of {view} on {day}')
    request_sha, rung, seq = row
    with contextlib.closing(sqlite3.connect(f"file:{edge_replay.SAVED / 'archive.sqlite'}?mode=ro", uri=True)) as conn:
        request_json, answer_json = conn.execute('select request_json, answer_json from model_calls where request_sha256=?', (request_sha,)).fetchone()
    return {'request_sha256': request_sha, 'rung': rung, 'seq': seq, 'request_json': request_json, 'answer': json.loads(answer_json)}


def ledger_before(draw, day):
    """The draw's ledger after the articles of `day` and before its judging round, rebuilt once by the offline replay."""
    folder = DATA / f'ledger-d{draw}-before-{day}'
    if (folder / 'views.sqlite').exists() and (folder / 'stopped-before.json').exists():
        return folder / 'views.sqlite'
    edge_replay.use_draw(draw)
    production_judge = edge_replay.e2e_adapter.Adapter.judge

    def stop_or_judge(self, round_day, seq, changed):
        if round_day == day:
            raise StopBeforeRound(round_day)
        return production_judge(self, round_day, seq, changed)

    edge_replay.e2e_adapter.Adapter.judge = stop_or_judge
    try:
        edge_replay.run_replay(folder, edge_replay.STEP2)
        raise SystemExit(f'the replay of draw {draw} never reached a judging round on {day}')
    except StopBeforeRound:
        pass
    finally:
        edge_replay.e2e_adapter.Adapter.judge = production_judge
    (folder / 'stopped-before.json').write_text(json.dumps({'draw': draw, 'day': day, 'saved run': str(edge_replay.SAVED)}))
    return folder / 'views.sqlite'


def read_only(path):
    conn = sqlite3.connect(f'file:{Path(path).resolve()}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def load_case(draw, view, day, which='accepted'):
    if which not in ('accepted', 'first'):
        raise SystemExit(f'a case is the accepted or the first request, not {which}')
    saved = saved_judgement(draw, view, day) if which == 'accepted' else saved_first_request(draw, view, day)
    requests = json.loads((DATA / f'control-d{draw}' / 'control-requests.json').read_text())
    report = json.loads((DATA / f'control-d{draw}' / 'control-report.json').read_text())
    if not report['passed'] or report['saved run'] != str(edge_replay.SAVED):
        raise SystemExit(f'the offline replay of draw {draw} did not pass or is of another run')
    request = requests.get(saved['request_sha256'])
    if request is None:
        raise SystemExit(f'the replay of draw {draw} holds no request {saved["request_sha256"]}')
    canonical = json.dumps(request, sort_keys=True, ensure_ascii=False)
    if canonical != saved['request_json'] or sha256(canonical) != saved['request_sha256']:
        raise SystemExit(f'draw {draw} {view} {day}: the rebuilt request is not the saved one')
    cfg = config.load(edge_replay.e2e_adapter.CONFIG)
    rebuilt = model.build_request(cfg.rejudging, request['messages'][0]['content'], request['messages'][-1]['content'],
                                  judging.schema_for(cfg.rejudging.prompt_version), 'judgement', cfg.provider)
    if json.dumps(rebuilt) != json.dumps(request):
        raise SystemExit(f'draw {draw} {view} {day}: the request is not, byte for byte, what model.build_request builds today')
    ledger = ledger_before(draw, day)
    with contextlib.closing(read_only(ledger)) as conn:
        if conn.execute('select 1 from judgements where view_id=? and publication_day=?', (view, day)).fetchone():
            raise SystemExit(f'the ledger before {day} already holds that day\'s judgement of {view}')
        user = request['messages'][-1]['content']
        errors = judging.check_answer(conn, view, saved['answer'], user)
        refused = judging.check_answer(conn, view, {**saved['answer'], 'cites': saved['answer']['cites'] + ['e999999']}, user)
    if which == 'accepted' and errors:
        raise SystemExit(f'draw {draw} {view} {day}: the saved answer fails the check on the rebuilt ledger: {errors}')
    if which == 'first' and not errors:
        raise SystemExit(f'draw {draw} {view} {day}: the saved refused answer passes the check on the rebuilt ledger')
    if not refused:
        raise SystemExit(f'draw {draw} {view} {day}: negative control failed, an unshown citation was not refused')
    return {'key': f'd{draw}-{view}-{day}-{which}', 'draw': draw, 'view': view, 'day': day, 'which': which, 'request': request,
            'ledger': str(ledger), 'saved rung': saved['rung'], 'saved answer': saved['answer'], 'saved answer rung': saved['answer']['rung'],
            'saved answer refused for': errors, 'as sent sha256': sha256(json.dumps(request)), 'worst cost per attempt (usd)': budget.worst_cost(request)}


def cases_of(arguments):
    return [load_case(int(draw), view, day, which) for draw, view, day, which in arguments.case]


def facts(cases, sends):
    worst = sum(case['worst cost per attempt (usd)'] for case in cases) * sends * budget.ATTEMPTS
    return {'cases': {case['key']: {'saved rung': case['saved rung'], 'saved answer to this request': case['saved answer rung'],
                                    'saved answer refused for': case['saved answer refused for'], 'as sent sha256': case['as sent sha256'], 'ledger': case['ledger'],
                                    'user text characters': len(case['request']['messages'][-1]['content'])} for case in cases},
            'sends per case': sends, 'sends': sends * len(cases), 'worst cost, every send tried three times (usd)': round(worst, 4), 'cap (usd)': CAP_USD}


def send(cases, output, sends):
    registered = facts(cases, sends)
    if registered['worst cost, every send tried three times (usd)'] > CAP_USD:
        raise SystemExit('the worst cost passes the cap')
    output = Path(output).resolve()
    if DATA.resolve() not in output.parents:
        raise SystemExit(f'the sends are written only under {DATA}')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'raw').mkdir()
    write_new(output / 'registration.json', json.dumps({**registered, 'registered at': time.strftime('%Y-%m-%dT%H:%M:%S%z')}, indent=1))
    current = threading.local()

    def attempt(provider, request):
        """One attempt through the production transport; the body is on disk before anything else reads it."""
        current.attempts += 1
        response = model.openai_transport(provider, request, max_attempts=1)
        current.returned = response                     # held before anything that can fail
        try:
            write_new(output / 'raw' / f'{current.name}-attempt-{current.attempts}.json', json.dumps(response, ensure_ascii=False))
        except Exception as error:                     # the answer stays in memory and reaches the outcome file
            current.raw_write_failure = f'{type(error).__name__}: {error}'
        return response

    limit = budget.Budget(CAP_USD, attempt=attempt)
    provider = config.load(edge_replay.e2e_adapter.CONFIG).provider

    def one(job):
        case, number = job
        current.name, current.attempts, current.returned, current.raw_write_failure = f"{case['key']}-{number}", 0, None, None
        outcome, started = {'case': case['key'], 'send': number}, time.time()
        try:
            outcome['response'] = limit.send(provider, case['request'])
        except Exception as error:   # recorded as an outcome; never re-sent by this script
            outcome['error'] = f'{type(error).__name__}: {error}'
            if getattr(error, 'response_body', None) is not None:
                outcome['response body of the failed attempt'] = error.response_body
            if current.returned is not None:
                outcome['response'] = current.returned
                outcome['failure after the answer returned'] = outcome.pop('error')
        outcome.update(seconds=round(time.time() - started, 1), attempts=current.attempts)
        if current.raw_write_failure:
            outcome['raw body not written'] = current.raw_write_failure
        try:
            write_new(output / f"{case['key']}-{number}.json", json.dumps(outcome, ensure_ascii=False, indent=1))
        except Exception as error:   # the outcome is still printed below and returned; the run goes on
            outcome['outcome file not written'] = f'{type(error).__name__}: {error}'
        print(json.dumps({'outcome': outcome}, ensure_ascii=False), flush=True)   # a second copy, in the launcher's log
        return outcome

    jobs = [(case, number) for number in range(1, sends + 1) for case in cases]
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(jobs), 16)) as pool:
        outcomes = list(pool.map(one, jobs))
    write_new(output / 'spent.json', json.dumps({'spent usd (from tokens; a lost answer at its reserve)': round(limit.spent_usd, 4),
                                                   'answered': sum('response' in o for o in outcomes), 'failed': sum('error' in o for o in outcomes)}, indent=1))
    print((output / 'spent.json').read_text())


def read_outcome(outcome, case):
    if 'error' in outcome:
        return {'status': 'not answered', 'detail': str(outcome['error'])}
    try:
        answer = json.loads(outcome['response']['choices'][0]['message']['content'])
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
        return {'status': 'malformed', 'detail': str(error)}
    schema = case['request']['response_format']['json_schema']['schema']
    errors = model.check_schema(answer, schema)
    if errors:
        return {'status': 'refused by the schema', 'detail': '; '.join(errors[:3])}
    with contextlib.closing(read_only(case['ledger'])) as conn:
        errors = judging.check_answer(conn, case['view'], answer, case['request']['messages'][-1]['content'])
    rung_counts = not errors or all(any(reason in error for reason in CITATION_REASONS) for error in errors)
    return {'status': 'refused by the check' if errors else 'accepted', 'detail': '; '.join(errors), 'rung': answer['rung'], 'rung counts': rung_counts,
            'cites_views': answer['cites_views'], 'theme_pushes': answer['theme_pushes'],
            'changed': answer['changed'], 'cites': answer['cites'], 'reference': answer['reference'], 'implied_outcome': answer['implied_outcome'],
            'reasons': answer['reasons'], 'why_changed': answer['why_changed'], 'key order as production': list(answer) == list(case['saved answer'])}


def read(cases, send_folder):
    send_folder = Path(send_folder).resolve()
    if DATA.resolve() not in send_folder.parents:
        raise SystemExit(f'a reading is written only under {DATA}')
    if (send_folder / 'reading.json').exists():
        raise SystemExit(f'{send_folder} already holds a reading; nothing is overwritten')
    registration = json.loads((send_folder / 'registration.json').read_text())
    for case in cases:
        if registration['cases'].get(case['key'], {}).get('as sent sha256') != case['as sent sha256']:
            raise SystemExit(f"{send_folder} registers another request for {case['key']}; nothing is read")
    rows, summary = [], {}
    for case in cases:
        for number in range(1, registration['sends per case'] + 1):
            try:
                outcome = json.loads((send_folder / f"{case['key']}-{number}.json").read_text())
                if outcome.get('case') != case['key'] or outcome.get('send') != number:
                    raise ValueError(f"the file records case {outcome.get('case')} send {outcome.get('send')}")
                row = read_outcome(outcome, case)
            except Exception as error:   # an outcome this reader cannot read is reported and not counted
                row = {'status': 'unreadable', 'detail': f'{type(error).__name__}: {error}'}
            rows.append({'case': case['key'], 'send': number, **row})
        accepted = [row['rung'] for row in rows if row['case'] == case['key'] and row['status'] == 'accepted']
        refused = [row['rung'] for row in rows if row['case'] == case['key'] and row['status'] == 'refused by the check' and row['rung counts']]
        summary[case['key']] = {'saved rung of the day': case['saved rung'], 'saved answer to this request': case['saved answer rung'],
                                'accepted rungs': sorted(accepted), 'rungs of answers the check refused for a cited id only': sorted(refused),
                                'answers whose rung is not counted': registration['sends per case'] - len(accepted) - len(refused)}
    write_new(send_folder / 'reading.json', json.dumps({'summary': summary, 'rows': rows}, ensure_ascii=False, indent=1))
    for row in rows:
        print(json.dumps({k: v for k, v in row.items() if k in ('case', 'send', 'status', 'detail', 'rung', 'rung counts', 'changed', 'key order as production')}))
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['check', 'send', 'read'])
    parser.add_argument('folder', nargs='?')
    parser.add_argument('--case', nargs=4, action='append', required=True, metavar=('DRAW', 'QUESTION', 'DAY', 'WHICH'),
                        help='WHICH: accepted (the request whose answer the run kept) or first (the day\'s first request, refused)')
    parser.add_argument('--sends', type=int, default=3)
    arguments = parser.parse_args()
    cases = cases_of(arguments)
    if arguments.mode == 'check':
        print(json.dumps(facts(cases, arguments.sends), indent=1))
    elif not arguments.folder:
        parser.error(f'{arguments.mode} needs a folder')
    elif arguments.mode == 'send':
        send(cases, arguments.folder, arguments.sends)
    else:
        read(cases, arguments.folder)
