#!/usr/bin/env python3
"""One judgement, with and without the record an unsupported revision relation carried into it: thesis v20 on 2026-07-06 of the saved
D392 clean draw 1. Protocol: PROTOCOL.md beside this file, written before the send.

The two requests are the ones `edge_replay.py counterfactual` wrote: the request the frozen judge was sent on that day, and the request
the same code builds when the one relation is removed from the library. Each is sent as the production transport sends it
(`model.openai_transport`: json.dumps of the request in the order `model.build_request` built it), through the measurement spending
limit (`e2e-2026-11-09/budget.py`), with no archive in between, so every draw is a fresh answer.

  judge_probe.py check <replay folder>                 no send: the identities and the checks below, and the worst cost
  judge_probe.py send <replay folder> <new folder>     the sends (draws per arm and cap from PROTOCOL.md's numbers below)
  judge_probe.py read <replay folder> <send folder>    the answers through the frozen judge's own check, one row per answer"""
import argparse, concurrent.futures, contextlib, hashlib, json, re, sqlite3, sys, threading, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path[:0] = [str(HERE)]
import edge_replay  # noqa: E402
import budget  # noqa: E402  (edge_replay put e2e-2026-11-09 and src on the path)
from hivemind import config, model  # noqa: E402
from hivemind.views import judging, store  # noqa: E402

OUTPUT_ROOTS = (edge_replay.ROOT / 'poc/data/clean-step2-edge-effect-2026-11-10', edge_replay.ROOT / 'poc/data/clean-step2-revision-links-2026-11-10')
VIEW, DAY, SEQ = 'v20', '2026-07-06', 76      # the case of 2026-11-10's first probe; `--case` names another
CARRIED = 'e185'                      # the record the relation carried into the question


def use_case(draw, view, day, seq, carried):
    """The judgement this probe sends both ways: a saved draw, a question, the day and sequence number of its judging round, and the
    evidence id of the record a relation carried into it."""
    global VIEW, DAY, SEQ, CARRIED
    edge_replay.use_draw(draw)
    VIEW, DAY, SEQ, CARRIED = view, day, seq, carried
ARMS = ('control', 'counterfactual')
DRAWS = 3
CAP_USD = 0.25
FIGURE = re.compile(r'\$\s?(\d{2,4}(?:\.\d+)?)(?:\s?[–-]\s?\$?(\d{2,4}(?:\.\d+)?))?\s?billion')


def load_requests(replay_folder):
    return {arm: json.loads((Path(replay_folder) / f'request-{VIEW}-{arm}.json').read_text()) for arm in ARMS}


def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def user_text(request):
    return request['messages'][-1]['content']


def read_only_ledger(replay_folder):
    """The replay's ledger as it stood when this judgement was asked for, opened read-only with the row shape the store's readers expect."""
    conn = sqlite3.connect(f"file:{Path(replay_folder).resolve() / 'views.sqlite'}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def verdict(accepted):
    """PROTOCOL.md's reading rule over the accepted rungs of each arm."""
    if any(len(accepted[arm]) != DRAWS for arm in ARMS):
        return 'not decided: fewer than three accepted answers in an arm'
    if len(set(accepted['control'] + accepted['counterfactual'])) == 1:
        return 'no difference in the conclusion in these samples'
    if len(set(accepted['control'])) == 1 and len(set(accepted['counterfactual'])) == 1:
        return 'the conclusion differs in these samples'
    return 'not decided by this probe: the answers are mixed'


def saved_judgement():
    with contextlib.closing(sqlite3.connect(f"file:{edge_replay.SAVED / 'views.sqlite'}?mode=ro", uri=True)) as conn:
        request_sha, publication_day = conn.execute('select request_sha256, publication_day from judgements where view_id=? and seq=?', (VIEW, SEQ)).fetchone()
    with contextlib.closing(sqlite3.connect(f"file:{edge_replay.SAVED / 'archive.sqlite'}?mode=ro", uri=True)) as conn:
        answer_json, request_json = conn.execute('select answer_json, request_json from model_calls where request_sha256=?', (request_sha,)).fetchone()
    return request_sha, publication_day, json.loads(answer_json), request_json


def checks(replay_folder):
    """Every identity the send rests on; raises on the first that fails. Returns the facts printed by `check`."""
    requests = load_requests(replay_folder)
    saved_sha, saved_day, saved_answer, saved_request_json = saved_judgement()
    if saved_day != DAY:
        raise SystemExit(f'the saved judgement of {VIEW} at seq {SEQ} is of {saved_day}, not {DAY}')
    canonical = {arm: json.dumps(request, sort_keys=True, ensure_ascii=False) for arm, request in requests.items()}
    if sha256(canonical['control']) != saved_sha or canonical['control'] != saved_request_json:
        raise SystemExit('the control request is not the request the saved judgement answered')
    cfg = config.load(edge_replay.e2e_adapter.CONFIG)
    rebuilt = model.build_request(cfg.rejudging, requests['control']['messages'][0]['content'], user_text(requests['control']),
                                  judging.schema_for(cfg.rejudging.prompt_version), 'judgement', cfg.provider)
    if json.dumps(rebuilt) != json.dumps(requests['control']):
        raise SystemExit('the control request file is not, byte for byte, what model.build_request builds today from its system and user text')
    with_other_user_text = json.loads(json.dumps(requests['control']))
    with_other_user_text['messages'][-1]['content'] = user_text(requests['counterfactual'])
    if json.dumps(with_other_user_text) != json.dumps(requests['counterfactual']):
        raise SystemExit('the two requests differ outside the user text (a key, its order, the system text or the schema)')
    control_lines, counterfactual_lines = user_text(requests['control']).splitlines(), user_text(requests['counterfactual']).splitlines()
    start = next(n for n, line in enumerate(control_lines) if line.startswith(f'- {CARRIED} ['))
    end = next(n for n in range(start + 1, len(control_lines)) if not control_lines[n].startswith('    '))
    without_block = control_lines[:start] + control_lines[end:]
    count_line = next(n for n, line in enumerate(without_block) if line.startswith('[Evidence in view under this thesis, '))
    shown = judging.evidence_shown_in(user_text(requests['counterfactual']))
    without_block[count_line] = f'[Evidence in view under this thesis, {len(shown)} items]'
    if without_block != counterfactual_lines:
        raise SystemExit(f'the counterfactual request is not the control request less the {CARRIED} block and the item count')
    if CARRIED in shown or CARRIED not in judging.evidence_shown_in(user_text(requests['control'])):
        raise SystemExit(f'{CARRIED} is not shown in the control request only')
    # the frozen judge's own check, on the ledger as it stood when this judgement was asked for (the replay stopped in this round)
    ledger = read_only_ledger(replay_folder)
    try:
        last = store.current_state(ledger, VIEW)
        if ledger.execute('select 1 from judgements where view_id=? and seq=?', (VIEW, SEQ)).fetchone():
            raise SystemExit(f'the replay ledger already holds the {DAY} judgement of {VIEW}')
        accepted = judging.check_answer(ledger, VIEW, saved_answer, user_text(requests['control']))
        refused = judging.check_answer(ledger, VIEW, saved_answer, user_text(requests['counterfactual']))
    finally:
        ledger.close()
    if accepted:
        raise SystemExit(f'the saved answer does not pass the check on the control request: {accepted}')
    if not any(CARRIED in error for error in refused):
        raise SystemExit(f'positive control failed: the saved answer cites {CARRIED} and the check did not refuse it against the counterfactual request')
    worst = {arm: budget.worst_cost(request) for arm, request in requests.items()}
    return requests, {
        'saved judgement': {'request sha256': saved_sha, 'rung': saved_answer['rung'], 'previous rung': last['rung'] if last else None},
        'as sent, sha256 of json.dumps(request)': {arm: sha256(json.dumps(request)) for arm, request in requests.items()},
        'user text characters': {arm: len(user_text(request)) for arm, request in requests.items()},
        'lines removed with the block': end - start, 'evidence shown': {'control': len(shown) + 1, 'counterfactual': len(shown)},
        'answer key order of the saved answer': list(saved_answer),
        'worst cost per send (usd)': {arm: round(cost, 4) for arm, cost in worst.items()},
        'cost if every send answers at its first attempt, at the reserve (usd)': round(DRAWS * sum(worst.values()), 4),
        'worst cost of the probe, every send tried three times (usd)': round(budget.ATTEMPTS * DRAWS * sum(worst.values()), 4),
        'cap (usd)': CAP_USD, 'sends': DRAWS * len(ARMS)}


def send(replay_folder, output):
    requests, facts = checks(replay_folder)
    if facts['worst cost of the probe, every send tried three times (usd)'] > CAP_USD:
        raise SystemExit('the worst cost of the probe passes the cap')
    output = Path(output).resolve()
    if not any(root.resolve() in output.parents for root in OUTPUT_ROOTS):
        raise SystemExit(f'the probe writes only under {OUTPUT_ROOTS}')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'registration.json').write_text(json.dumps({'case': {'saved run': str(edge_replay.SAVED), 'question': VIEW, 'day': DAY, 'seq': SEQ, 'carried record': CARRIED},
                                                          **facts, 'registered at': time.strftime('%Y-%m-%dT%H:%M:%S%z')}, indent=1))
    (output / 'raw').mkdir()
    current = threading.local()          # the job whose attempt is in flight in this thread (Budget.send calls the attempt in its caller's thread)

    def attempt(provider, request):
        """One attempt through the production transport. The body that came back is on disk before anything else reads it, so an
        answer cannot be lost to a failure in the accounting or in this script."""
        current.attempts += 1
        response = model.openai_transport(provider, request, max_attempts=1)
        (output / 'raw' / f'{current.arm}-{current.draw}-attempt-{current.attempts}.json').write_text(json.dumps(response, ensure_ascii=False))
        current.returned = response
        return response

    limit = budget.Budget(CAP_USD, attempt=attempt)
    provider = config.load(edge_replay.e2e_adapter.CONFIG).provider

    def one(job):
        current.arm, current.draw = job
        current.attempts, current.returned = 0, None
        arm, draw = job
        started = time.time()
        outcome = {'arm': arm, 'draw': draw}
        try:
            outcome['response'] = limit.send(provider, requests[arm])
        except Exception as error:   # a failed send is an outcome of the probe, recorded and never re-sent by this script
            outcome['error'] = f'{type(error).__name__}: {error}'
            if getattr(error, 'response_body', None) is not None:
                outcome['response body of the failed attempt'] = error.response_body
            if current.returned is not None:   # the answer came back and the failure is after it: the answer stands, the failure is noted
                outcome['response'] = current.returned
                outcome['failure after the answer returned'] = outcome.pop('error')
        outcome.update(seconds=round(time.time() - started, 1), attempts=current.attempts)
        (output / f'{arm}-{draw}.json').write_text(json.dumps(outcome, ensure_ascii=False, indent=1))
        return outcome

    jobs = [(arm, draw) for draw in range(1, DRAWS + 1) for arm in ARMS]          # the arms interleaved, all sent at once
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(jobs)) as pool:
        outcomes = list(pool.map(one, jobs))
    (output / 'spent.json').write_text(json.dumps({'spent usd (from tokens; a lost answer at its reserve)': round(limit.spent_usd, 4),
                                                   'answered': sum('response' in o for o in outcomes), 'failed': sum('error' in o for o in outcomes)}, indent=1))
    print((output / 'spent.json').read_text())


def read_outcome(outcome, arm, ledger, requests, schema, saved_answer):
    """One row for one saved outcome. Only an answer that passes the schema and the frozen judge's check is 'accepted'."""
    if 'error' in outcome:
        return {'status': 'not answered', 'detail': str(outcome['error'])}
    try:
        answer = json.loads(outcome['response']['choices'][0]['message']['content'])
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
        return {'status': 'malformed', 'detail': str(error)}
    schema_errors = model.check_schema(answer, schema)
    if schema_errors:            # not the answer's shape: nothing further is read from it
        return {'status': 'refused by the schema', 'detail': '; '.join(schema_errors[:3])}
    errors = judging.check_answer(ledger, VIEW, answer, user_text(requests[arm]))
    pushes = {push['evidence_id']: push['push'] for push in answer['pushes']}
    usage = outcome['response'].get('usage')
    usage = usage if isinstance(usage, dict) else {}
    return {'status': 'refused by the check' if errors else 'accepted', 'detail': '; '.join(errors[:3]),
            'rung': answer['rung'], 'changed': answer['changed'], 'cites': len(answer['cites']),
            f'cites {CARRIED}': CARRIED in answer['cites'], f'push on {CARRIED}': pushes.get(CARRIED),
            'figures in implied_outcome': [match.group(0) for match in FIGURE.finditer(answer['implied_outcome'])],
            'key order as production': list(answer) == list(saved_answer),
            'tokens': [usage.get('prompt_tokens'), usage.get('completion_tokens')],
            'implied_outcome': answer['implied_outcome'], 'reference': answer['reference'],
            'reasons': answer['reasons'], 'why_changed': answer['why_changed']}


def read(replay_folder, send_folder):
    """Every outcome becomes a row. An outcome this reader cannot read, for whatever reason, is the row 'unreadable' and is not counted,
    so an unexpected shape can only lead to 'not decided', never to a verdict and never to no reading."""
    requests, facts = checks(replay_folder)
    registration = json.loads((Path(send_folder) / 'registration.json').read_text())
    sent = 'as sent, sha256 of json.dumps(request)'
    if registration.get(sent) != facts[sent]:           # the folder's answers must be answers to these two requests, and to no others
        raise SystemExit(f'{send_folder} registers other requests than this case\'s; nothing is read and nothing is written there')
    schema = requests['control']['response_format']['json_schema']['schema']
    _, _, saved_answer, _ = saved_judgement()
    ledger = read_only_ledger(replay_folder)
    rows = []
    try:
        for arm in ARMS:
            for draw in range(1, DRAWS + 1):
                try:
                    outcome = json.loads((Path(send_folder) / f'{arm}-{draw}.json').read_text())
                    row = read_outcome(outcome, arm, ledger, requests, schema, saved_answer)
                except Exception as error:
                    row = {'status': 'unreadable', 'detail': f'{type(error).__name__}: {error}'}
                rows.append({'arm': arm, 'draw': draw, **row})
    finally:
        ledger.close()
    accepted = {arm: sorted(row['rung'] for row in rows if row['arm'] == arm and row['status'] == 'accepted') for arm in ARMS}
    result = {'verdict by the protocol': verdict(accepted), 'accepted rungs by arm': accepted, 'saved answer rung': saved_answer['rung']}
    (Path(send_folder) / 'reading.json').write_text(json.dumps({**result, 'rows': rows}, ensure_ascii=False, indent=1))
    for row in rows:
        print(json.dumps({name: value for name, value in row.items() if name not in ('implied_outcome', 'reference', 'reasons', 'why_changed')}, ensure_ascii=False))
    print(json.dumps(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['check', 'send', 'read'])
    parser.add_argument('replay_folder')
    parser.add_argument('folder', nargs='?')
    parser.add_argument('--case', nargs=5, metavar=('DRAW', 'QUESTION', 'DAY', 'SEQ', 'EVIDENCE'),
                        help='another judgement than the first probe\'s, for example: 3 v22 2026-07-06 76 e176')
    args = parser.parse_args()
    if args.case:
        use_case(int(args.case[0]), args.case[1], args.case[2], int(args.case[3]), args.case[4])
    if args.mode == 'check':
        print(json.dumps(checks(args.replay_folder)[1], indent=1))
    elif not args.folder:
        parser.error(f'{args.mode} needs the send folder')
    elif args.mode == 'send':
        send(args.replay_folder, args.folder)
    else:
        read(args.replay_folder, args.folder)
