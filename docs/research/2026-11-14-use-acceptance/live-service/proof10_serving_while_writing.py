"""Proof 10 (OPERATING-CONTRACT.md, "Proof 10's design"; council rounds 140 and 141; $0): serving while the built writer runs.

The extension draw's c1 is judged again through the accepted loop into a new scratch store to an end day past its due days, every
judge request answered from the stored archive by identity (a request with none stops the run). The writer is the built `replay`
(WAL, its lock, the checks before each day, its end). At the D573 harness's seven pauses the API (lexical, started on the store being
written), MCP's tool functions (module level, not its transport), the lock, preflight and the snapshot route are checked; a poller
reads `/library` back to back between pauses. It exits 1 unless every check holds.

  python3 proof10_serving_while_writing.py <extension proof folder> <new scratch folder> [end day]
"""
import hashlib
import importlib.util
import json
import sqlite3
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


D573 = load('serving_while_writing', ROOT / 'docs/research/2026-11-14-use-acceptance/page-contract/serving_while_writing.py')
ladder_adapter = D573.ladder_adapter
from hivemind import live_lock, model, service  # noqa: E402

preflight = load('preflight', ROOT / 'scripts/preflight.py')
FIRST_DAY_BODY = {'error': "the store's first day has not completed"}
SNAPSHOTS = {('2026-09-25', 'before judging'): 'a day\'s articles committed, the day not completed',
             ('2027-01-31', 'before close'): 'a due-day closing not yet completed, no articles that day'}


def canonical(body):
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def load_mcp(store, scratch):
    """The MCP module as its entry point builds it, lexical; its tool functions are called in-process (not through the transport)."""
    saved = sys.argv
    sys.argv = ['hivemind_mcp.py', '--views', str(store), '--index', str(scratch / 'mcp-index.sqlite'), '--items',
                str(scratch / 'no-items.sqlite'), '--lexical']
    try:
        return load('hivemind_mcp_proof10', ROOT / 'scripts/hivemind_mcp.py')
    finally:
        sys.argv = saved


def snapshot(store, destination):
    finished = subprocess.run([sys.executable, str(ROOT / 'scripts/snapshot_store.py'), str(store), str(destination)],
                              capture_output=True, text=True)
    if finished.returncode != 0:
        return {'refused': finished.stderr.strip()[-300:]}
    with sqlite3.connect(f'file:{destination}?mode=ro', uri=True) as conn:
        return {'last day': conn.execute('select max(day) from days_completed').fetchone()[0],
                'mode': conn.execute('pragma journal_mode').fetchone()[0],
                'integrity': conn.execute('pragma integrity_check').fetchone()[0],
                'steps by day': dict(conn.execute('select publication_day, count(*) from processing_steps group by publication_day')),
                'closed views': sorted(r[0] for r in conn.execute('select view_id from view_switches s where id = (select max(id) from view_switches '
                                                                  'where view_id = s.view_id) and open = 0'))}


def main(proof, scratch, end_day='2027-04-02'):
    scratch = Path(scratch)
    scratch.mkdir(parents=True)
    draw = Path(proof) / 'week/c1'
    stored = sqlite3.connect(f"file:{draw / 'judge/draw-c1/archive.sqlite'}?mode=ro", uri=True)
    answers = {sha: json.loads(r) for sha, r in stored.execute('select request_sha256, response_json from model_calls where response_json is not null')}

    def from_the_archive(provider, request):
        sha = model.request_identity(request)[1]
        if sha not in answers:
            raise SystemExit(f'a judge request with no stored answer: {sha[:16]}')
        return answers[sha]

    output = scratch / 'out'
    store = output / 'views.sqlite'
    api = {'port': D573.free_port(), 'process': None}
    page_shell = scratch / 'shell.html'
    subprocess.run([sys.executable, str(ROOT / 'scripts/mock_build.py'), '--out', str(page_shell)], check=True, capture_output=True)
    seen, completions, polls, mcp = {}, {}, [], {}
    stop_polling = threading.Event()

    def poll():
        while not stop_polling.is_set():
            sent = time.monotonic()
            status, body = D573.get(api['port'], '/library')
            polls.append({'sent': sent, 'received': time.monotonic(), 'status': status, 'as_of': body.get('as_of'),
                          'hash': canonical(body), 'body': body if status != 200 else None})
            time.sleep(0.02)

    def start_api():
        api['process'] = subprocess.Popen([sys.executable, str(ROOT / 'scripts/hivemind_api.py'), '--port', str(api['port']), '--lexical',
                                           '--config', '', '--views', str(store), '--index', str(scratch / 'index.sqlite'),
                                           '--archive', str(scratch / 'archive.sqlite')],
                                          stdout=open(scratch / 'api.log', 'w'), stderr=subprocess.STDOUT)
        for _ in range(120):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{api['port']}/days", timeout=2) as response:
                    if response.status == 200:
                        break
            except urllib.error.HTTPError as error:
                body = json.loads(error.read() or b'{}')
                if error.code == 503 and body == FIRST_DAY_BODY:
                    break
                raise SystemExit(f'the API answered {error.code} {body} while starting')
            except Exception:
                time.sleep(0.5)
        else:
            raise SystemExit('the API never became ready')
        threading.Thread(target=poll, daemon=True).start()

    def ask(day, phase):
        if (day, phase) not in D573.PAUSES:
            return
        if api['process'] is None:
            start_api()
            mcp['module'] = load_mcp(store, scratch)
        record = {'days': D573.get(api['port'], '/days'), 'library': D573.get(api['port'], '/library')}
        if (day, phase) in D573.PAGES:
            record['page'] = D573.render(api['port'], page_shell, scratch, f'{day}-{phase}'.replace(' ', '-'))
        module = mcp['module']
        record['mcp instructions'] = module.OBJECTS[:90]
        for name, call in (('thesis_library', module.thesis_library), ('views', module.views)):
            try:
                answer = call()
                record[f'mcp {name}'] = ({'as_of': answer.get('as_of'), 'ids': sorted(v['view_id'] for v in answer['views'])}
                                         if name == 'thesis_library' else {'count': len(answer)})
            except service.FirstDayNotCompleted:
                record[f'mcp {name}'] = 'first day refused'
        try:
            live_lock.release(live_lock.acquire(store))
            record['lock'] = 'free'
        except live_lock.LockRefused:
            record['lock'] = 'held'
        try:
            preflight.store_copies([str(store)])
            record['preflight'] = 'copied'
        except live_lock.LockRefused as refused:
            record['preflight'] = 'refused, naming the snapshot route' if 'snapshot_store.py' in str(refused) else f'refused: {refused}'
        with sqlite3.connect(f'file:{store}?mode=ro', uri=True) as conn:
            record['journal mode'] = conn.execute('pragma journal_mode').fetchone()[0]
        if (day, phase) in SNAPSHOTS:
            record['snapshot'] = snapshot(store, scratch / f'snapshot-{day}-{phase.replace(" ", "-")}.sqlite')
        seen[(day, phase)] = record
        lib = record['library']
        print(f"pause {day} {phase}: /days {record['days'][0]} {record['days'][1]} | /library {lib[0]} as_of {lib[1].get('as_of')} "
              f"questions {len(lib[1].get('views', []))} | mcp {record['mcp thesis_library']} | lock {record['lock']} | "
              f"preflight {record['preflight']} | mode {record['journal mode']}" + (f" | snapshot {record['snapshot']}" if 'snapshot' in record else ''),
              flush=True)

    real_judge, real_close = ladder_adapter.LadderAdapter.judge, ladder_adapter.LadderAdapter.close_and_complete

    def judge(self, day, seq, changed):
        ask(day, 'before judging')
        return real_judge(self, day, seq, changed)

    def close(self, day):
        ask(day, 'before close')
        started = time.monotonic()
        result = real_close(self, day)
        completions[day] = (started, time.monotonic())
        ask(day, 'after close')
        return result

    ladder_adapter.LadderAdapter.judge, ladder_adapter.LadderAdapter.close_and_complete = judge, close
    inputs = {'trace': str(draw / 'step1/trace.sqlite'), 'step2': str(draw / 'step2'), 'ladders': str(draw / 'ladder/send-1/outcomes.jsonl'),
              'ladder_archive': str(draw / 'ladder/send-1/archive.sqlite'), 'cases': str(draw / 'cases/cases.json'), 'output_root': str(scratch)}
    try:
        runner = ladder_adapter.replay('c1', output, transport=from_the_archive, cap_usd=5.0, inputs=inputs, end_day=end_day)
        stop_polling.set()
        time.sleep(0.2)
        after = {'counts end': {k: runner.counts.get(k) for k in ('store journal mode at the end', 'stopped in order')}}
        try:
            live_lock.release(live_lock.acquire(store))
            after['lock'] = 'free'
        except live_lock.LockRefused:
            after['lock'] = 'held'
        with sqlite3.connect(f'file:{store}?mode=ro', uri=True) as conn:
            after['journal mode'] = conn.execute('pragma journal_mode').fetchone()[0]
            after['last completed day'] = conn.execute('select max(day) from days_completed').fetchone()[0]
        after['days'] = D573.get(api['port'], '/days')
        after['library as_of'] = D573.get(api['port'], '/library')[1].get('as_of')
        dated = {}
        for day in sorted({p['as_of'] for p in polls if p['status'] == 200}):
            status, body = D573.get(api['port'], f'/library?as_of={day}')
            dated[day] = (status, canonical(body), body)
    finally:
        stop_polling.set()
        if api['process']:
            api['process'].terminate()
    checks = D573.check(seen)
    checks.update(new_checks(seen, completions, polls, dated, after))
    (scratch / 'seen.json').write_text(json.dumps({'pauses': {f'{d} {p}': r for (d, p), r in seen.items()}, 'after': after,
                                                   'completions': completions, 'polls': [{k: v for k, v in p.items() if k != 'body'} for p in polls]},
                                                  indent=1, ensure_ascii=False, default=str))
    failed = False
    for name, holds in checks.items():
        print(('ok   ' if holds else 'FAIL ') + name)
        failed |= not holds
    if failed:
        raise SystemExit(1)


def new_checks(seen, completions, polls, dated, after):
    out = {}
    first = seen[('2026-09-22', 'before close')]
    out['the first day: /days and /library both answer 503 with the first-day body'] = (
        first['days'] == (503, FIRST_DAY_BODY) and first['library'] == (503, FIRST_DAY_BODY))
    out['the first day: MCP says no day has completed, and thesis_library and views refuse'] = (
        first['mcp instructions'].startswith('No day of this ledger has completed yet') and
        first['mcp thesis_library'] == 'first day refused' and first['mcp views'] == 'first day refused')
    later = [(key, record) for key, record in seen.items() if key != ('2026-09-22', 'before close')]
    out[f'at every later pause ({len(later)}), MCP thesis_library has /library\'s day and view ids'] = all(
        record['mcp thesis_library'] == {'as_of': record['library'][1].get('as_of'), 'ids': sorted(v['view_id'] for v in record['library'][1]['views'])}
        for key, record in later)
    out[f'at every pause ({len(seen)}), the lock is held, preflight refuses naming the snapshot route, and the store is in WAL mode'] = all(
        r['lock'] == 'held' and r['preflight'] == 'refused, naming the snapshot route' and r['journal mode'] == 'wal' for r in seen.values())
    a = seen[('2026-09-25', 'before judging')]['snapshot']
    out[f"snapshot at 2026-09-25 before judging ({SNAPSHOTS[('2026-09-25', 'before judging')]}): last day 2026-09-24, steps dated 2026-09-25, out of WAL, integrity ok"] = (
        a.get('last day') == '2026-09-24' and a.get('steps by day', {}).get('2026-09-25', 0) > 0 and a.get('mode') == 'delete' and a.get('integrity') == 'ok')
    b = seen[('2027-01-31', 'before close')]['snapshot']
    out[f"snapshot at 2027-01-31 before close ({SNAPSHOTS[('2027-01-31', 'before close')]}): last day 2027-01-30, the three questions due that day (v3, v4, v7) not yet closed, out of WAL, integrity ok"] = (
        b.get('last day') == '2027-01-30' and not {'v3', 'v4', 'v7'} & set(b.get('closed views', ['?'])) and b.get('mode') == 'delete' and b.get('integrity') == 'ok')
    first_done = min(completions.values(), key=lambda bracket: bracket[1]) if completions else (0, 0)
    out[f'every poll ({len(polls)}) is 200, or 503 with the first-day body for a request sent before the first completion ended'] = all(
        p['status'] == 200 or (p['status'] == 503 and p['body'] == FIRST_DAY_BODY and p['sent'] < first_done[1]) for p in polls)
    ok = [p for p in polls if p['status'] == 200]
    compatible = []
    for p in ok:
        started_before_answer = p['as_of'] in completions and completions[p['as_of']][0] < p['received']
        floor = max((day for day, (s, e) in completions.items() if e < p['sent']), default=None)
        compatible.append(started_before_answer and (floor is None or p['as_of'] >= floor))
    out[f'every 200 poll ({len(ok)}) serves a day compatible with its completion brackets (started before the answer, no older than the last day done before the request)'] = all(compatible)
    out['the polled days never go backwards'] = all(a['as_of'] <= b['as_of'] for a, b in zip(ok, ok[1:]))
    out[f'every polled answer equals the dated read of its day on the finished store ({len(dated)} days)'] = all(
        dated[p['as_of']][0] == 200 and dated[p['as_of']][1] == p['hash'] for p in ok)
    straddled = [day for day, (started, ended) in completions.items()
                 if any(p['received'] < started and (p['status'] == 503 or p['as_of'] < day) for p in polls)
                 and any(p['sent'] > ended and p['status'] == 200 and p['as_of'] >= day for p in polls)]
    out[f'the polling is not vacuous: {len(polls)} answers (at least 20), {len(straddled)} completions with answers on both sides (at least 1)'] = (
        len(polls) >= 20 and len(straddled) >= 1)
    out['after the writer: the lock is free'] = after['lock'] == 'free'
    out[f"after the writer: out of WAL mode, or WAL kept with the reason recorded ({after['journal mode']}, {after['counts end']})"] = (
        after['journal mode'] == 'delete' or after['counts end'].get('stopped in order') == 'WAL kept: another connection held the store at the end')
    out[f"after the writer: the API answers as of the last completed day ({after['last completed day']})"] = (
        after['days'][1].get('last_day') == after['last completed day'] == after['library as_of'])
    return out


if __name__ == '__main__':
    main(*sys.argv[1:])
