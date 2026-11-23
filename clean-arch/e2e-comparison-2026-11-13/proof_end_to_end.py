"""The $0 end-to-end proof through the real orchestrator (WIRING-DESIGN.md §C4; council mo R4; D448, D449). Every component runs as a
real subprocess started by `run_fresh.py`; every child process loads a trap at start (a generated `sitecustomize.py` on its import path)
that replaces `urllib.request.urlopen`: a call from a thread holding no live reservation on the shared ledger is refused and counted, a
call holding one is answered from the stored runs and counted, a request no stored run holds is a miss. The entry points install the
stop gate over the trap, so the trap sees only actual sends. HOME points at a temporary folder with placeholder keys, so no real
credential can be read even if a trap failed to load.

  day                 a clean draw and a production draw for 2026-07-01 (ladder pass 1), both complete; no unreserved call, no miss;
                      ledger attempts = trapped calls; Step 1's results and states, the cases and the ladder's outcomes equal the stored
                      runs'
  killed child        a child SIGKILLed after its first send: recorded as a crash, the run stopped
  killed orchestrator the orchestrator (a real process) SIGKILLed while its child runs: the child's next send is refused (the gate finds
                      the launcher's lock free and stops the ledger), the child ends, another draw starts nothing, and a relaunch
                      records the crash

  python3 proof_end_to_end.py <scratch folder> [scenario ...]
"""
import json
import os
import shutil
import signal
import sqlite3
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = ROOT / 'poc/data'
U1_TRACE = DATA / 'clean-unseeded-2026-11-10/draw-d1/trace.sqlite'
U1_STEP2 = DATA / 'clean-unseeded-2026-11-10/draw-d1/step2'
RUN4 = DATA / 'clean-ladder-stage-a-2026-11-10/run-4'
STAGE_B_U1 = DATA / 'clean-stage-b-2026-11-11/draw-u1'
Q1 = DATA / 'clean-e2e-comparison-2026-11-13/draw-q1'

SITECUSTOMIZE = r'''
"""Proof trap (proof_end_to_end.py): loaded at the start of every child process the proof launches. Never on a production path."""
import collections, io, json, os, sqlite3, sys, threading, time, urllib.error, urllib.request
_CONFIG = os.environ.get('HIVEMIND_PROOF_TRAP')
if _CONFIG:
    _config = json.load(open(_CONFIG))
    sys.path.insert(0, _config['src'])
    from hivemind import jev as _jev, model as _model
    _model._key = lambda *arguments: 'proof-placeholder-not-a-credential'
    _jev._key = lambda *arguments: 'proof-placeholder-not-a-credential'
    _state, _lock = {}, threading.Lock()

    def _load():
        stored = collections.defaultdict(collections.deque)
        for path in _config['archives']:
            conn = sqlite3.connect('file:%s?mode=ro' % path, uri=True)
            for key, response in conn.execute('select request_sha256, response_json from model_calls order by call_id'):
                stored[key.split(':', 1)[0]].append(response)
            conn.close()
        conn = sqlite3.connect('file:%s?mode=ro' % _config['step1_trace'], uri=True)
        trace = dict(conn.execute('select input_id, raw_response from trace'))
        conn.close()
        _state.update(stored=stored, trace=trace, vectors=json.load(open(_config['embeddings'])))

    def _record(entry):
        line = (json.dumps(dict(entry, pid=os.getpid(), at=time.time())) + '\n').encode()
        fd = os.open(_config['counts'], os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        os.write(fd, line)
        os.close(fd)

    class _Response:
        def __init__(self, payload):
            self.raw, self.status = json.dumps(payload).encode('utf-8'), 200
        def read(self):
            return self.raw
        def __enter__(self):
            return self
        def __exit__(self, *arguments):
            return False

    def _refuse(url, code, kind):
        raise urllib.error.HTTPError(url, code, 'proof trap: ' + kind, {}, io.BytesIO(json.dumps({'error': {'type': kind}}).encode()))

    def _trap(request, *arguments, **keywords):
        url, admitted = request.full_url, time.time()          # the moment the stop gate let this send through
        mark = sys.modules.get('hivemind_shared_ledger_live_mark')
        if mark is None or getattr(mark.local, 'depth', 0) <= 0:
            _record({'url': url, 'live': False})
            _refuse(url, 403, 'proof_unreserved')
        with _lock:
            if not _state:
                _load()
        if _config.get('delay'):
            time.sleep(_config['delay'])
        body = json.loads(request.data)
        try:
            if url == 'https://api.openai.com/v1/embeddings':
                missing = [t for t in body['input'] if t not in _state['vectors']]
                if missing:
                    raise LookupError('%d texts with no stored vector' % len(missing))
                payload = {'data': [{'index': i, 'embedding': _state['vectors'][t]} for i, t in enumerate(body['input'])],
                           'usage': {'total_tokens': sum(max(1, len(t) // 4) for t in body['input'])}}
            elif url == 'https://api.deepseek.com/chat/completions':              # Step 1 only: by the article it reads
                item = json.JSONDecoder().raw_decode(body['messages'][1]['content'])[0]['source_item']['id']
                if item not in _state['trace']:
                    raise LookupError('step 1 item %s not stored' % item)
                payload = json.loads(_state['trace'][item])
                payload.pop('sent_request', None)
            else:
                _, sha = _model.request_identity(body)
                with _lock:
                    responses = _state['stored'].get(sha)
                    if not responses:
                        raise LookupError('request %s not stored' % sha[:12])
                    payload = json.loads(responses.popleft() if len(responses) > 1 else responses[0])
        except LookupError as miss:
            _record({'url': url, 'live': True, 'miss': str(miss)})
            _refuse(url, 400, 'proof_miss')
        _record({'url': url, 'live': True, 'admitted': admitted})
        return _Response(payload)

    urllib.request.urlopen = _trap
'''


def prepare(scratch, delay=0.0, name='trap'):
    """The trap folder, its configuration and counts file, and a HOME with placeholder keys; returns (environment additions, counts)."""
    site = scratch / f'{name}-site'
    site.mkdir(parents=True)
    (site / 'sitecustomize.py').write_text(SITECUSTOMIZE)
    counts = scratch / f'{name}-counts.jsonl'
    config = {'src': str(ROOT / 'src'), 'counts': str(counts), 'delay': delay, 'step1_trace': str(U1_TRACE),
              'embeddings': str(U1_STEP2 / 'embeddings.json'),
              'archives': [str(U1_STEP2 / 'jev.sqlite'), str(RUN4 / 'send-1' / 'archive.sqlite'), str(STAGE_B_U1 / 'archive.sqlite'),
                           str(Q1 / 'archive.sqlite')]}
    (scratch / f'{name}-config.json').write_text(json.dumps(config))
    home = scratch / f'{name}-home'
    (home / '.config/hivemind').mkdir(parents=True)
    (home / '.config/hivemind/credentials.json').write_text(json.dumps(
        {key: 'proof-placeholder-not-a-credential' for key in ('OPENAI_API_KEY', 'DEEPSEEK_API_KEY', 'TYPESAFE_API_KEY')}))
    os.chmod(home / '.config/hivemind/credentials.json', 0o600)
    return {'PYTHONPATH': str(site), 'HIVEMIND_PROOF_TRAP': str(scratch / f'{name}-config.json'), 'HOME': str(home)}, counts


def lines(counts):
    return [json.loads(line) for line in counts.read_text().splitlines()] if counts.exists() else []


def new_ledger(path, ceiling=15.0):
    import importlib.util
    spec = importlib.util.spec_from_file_location('budget_replay_proof', HERE / 'budget_replay.py')
    budget_replay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(budget_replay)
    budget_replay.SharedLedger.init(path, ceiling)
    return budget_replay.SharedLedger(path)


def orchestrator_module(environment):
    """run_fresh, loaded with the trap's environment in force (HOME included), so its children inherit it."""
    os.environ.update(environment)
    import importlib.util
    spec = importlib.util.spec_from_file_location('run_fresh_proof', HERE / 'run_fresh.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rows(path, query):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    try:
        return conn.execute(query).fetchall()
    finally:
        conn.close()


def day(scratch):
    environment, counts = prepare(scratch)
    run_fresh = orchestrator_module(environment)
    ledger = new_ledger(scratch / 'ledger.json')
    options = {'until_day': '2026-07-01', 'passes': 1}
    clean = run_fresh.Draw('clean', scratch / 'root', 's1', ledger.path, options).launch()
    prod = run_fresh.Draw('prod', scratch / 'root', 'sp1', ledger.path, options).launch()
    calls = lines(counts)
    state = ledger.read()
    folder = scratch / 'root' / 's1'
    stored_day = [r for r in rows(U1_TRACE, 'select sequence, input_id, result, after_state, status from trace order by sequence')][:13]
    step1_same = rows(folder / 'step1' / 'trace.sqlite', 'select sequence, input_id, result, after_state, status from trace order by sequence') == stored_day
    cases = json.loads((folder / 'cases' / 'cases.json').read_text())
    stored_cases = {c['case'].split('/', 1)[1]: c for c in json.loads((ROOT / 'clean-arch/step4-2026-11-10/stage_a/cases.json').read_text())
                    if c['case'].startswith('u1/')}
    cases_same = all(c['thesis'] == stored_cases[c['case'].split('/', 1)[1]]['thesis'] for c in cases) and len(cases) == 2
    keep = ('status', 'reason', 'requests', 'answer', 'passage', 'view')
    ladder = {json.loads(l)['case'].split('/', 1)[1]: {k: json.loads(l)[k] for k in keep}
              for l in (folder / 'ladder' / 'send-1' / 'outcomes.jsonl').read_text().splitlines()}
    stored_ladder = {json.loads(l)['case'].split('/', 1)[1]: {k: json.loads(l)[k] for k in keep}
                     for l in (RUN4 / 'send-1' / 'outcomes.jsonl').read_text().splitlines() if json.loads(l)['case'].startswith('u1/')}
    ladder_same = bool(ladder) and all(ladder[t] == stored_ladder[t] for t in ladder)
    import importlib.util
    spec = importlib.util.spec_from_file_location('spend_by_component', HERE / 'spend_by_component.py')
    spend = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(spend)
    by_component = spend.tally(scratch / 'root', ledger.path)
    timed = all(row['started at'] and row['ended at'] for key, row in by_component['by component'].items() if not key.startswith('unattributed'))
    report_spend = {key: (row['attempts'], round(row['charged'], 6)) for key, row in by_component['by component'].items()}
    step2_kinds = next(row['by kind'] for key, row in by_component['by component'].items() if key.startswith('s1/step2/'))
    split = sorted(step2_kinds) == ['embeddings', 'jev'] and all(kind['tokens reported'] > 0 for kind in step2_kinds.values())
    report = {'spend by component (attempts, charged)': report_spend, 'unattributed lines': by_component['unattributed lines'],
              'step 2 by kind': {k: (v['attempts'], round(v['charged'], 6), v['tokens reported']) for k, v in step2_kinds.items()},
              'every attempt timed': timed, 'clean': clean['state'], 'prod': prod['state'], 'prod totals': prod.get('prod totals'),
              'trapped calls': len(calls), 'unreserved': sum(not c['live'] for c in calls), 'misses': [c['miss'] for c in calls if 'miss' in c][:3],
              'child processes': len({c['pid'] for c in calls}), 'ledger attempts': state['attempts'], 'ledger spent': round(state['spent'], 6),
              'ledger reserved after': state['reserved'], 'step 1 as stored': step1_same, 'cases as stored': cases_same,
              'ladder outcomes as stored': ladder_same}
    ok = (clean['state'] == prod['state'] == 'complete' and calls and report['unreserved'] == 0 and not report['misses']
          and state['attempts'] == sum(c['live'] for c in calls) and state['reserved'] < 1e-9 and step1_same and cases_same and ladder_same
          and by_component['unattributed lines'] == 0 and abs(by_component['sum of lines'] - state['spent']) < 1e-9 and timed and split)
    return report, ok


def killed_child(scratch):
    environment, counts = prepare(scratch, delay=0.3)
    run_fresh = orchestrator_module(environment)
    ledger = new_ledger(scratch / 'ledger.json')

    def kill_after_first_send(argv, log_path, on_start=lambda process: None):
        def watch(process):
            while process.poll() is None:
                if any(c['pid'] == process.pid for c in lines(counts)):
                    os.kill(process.pid, signal.SIGKILL)
                    return
                time.sleep(0.05)

        def started(process):
            on_start(process)
            threading.Thread(target=watch, args=(process,), daemon=True).start()
        return run_fresh.execute(argv, log_path, started)
    record = run_fresh.Draw('clean', scratch / 'root', 'k1', ledger.path, {'until_day': '2026-07-01', 'passes': 1},
                            run_component=kill_after_first_send).launch()
    attempt = record['components']['step1']['attempts'][-1]
    report = {'state': record['state'], 'step 1 attempt': attempt['state'], 'reason': attempt.get('reason'),
              'ledger stop': ledger.read()['stop_reason'], 'sends before the kill': len(lines(counts))}
    return report, record['state'] == 'stopped' and attempt['state'] == 'crashed' and ledger.read()['stopped']


def killed_orchestrator(scratch):
    environment, counts = prepare(scratch, delay=1.0)
    ledger = new_ledger(scratch / 'ledger.json')
    root = scratch / 'root'
    env = dict(os.environ, **environment, PYTHONDONTWRITEBYTECODE='1')
    log = open(scratch / 'orchestrator.log', 'w')
    orchestrator = subprocess.Popen([sys.executable, HERE / 'run_fresh.py', 'clean', '--root', root, '--label', 'o1', '--ledger', ledger.path,
                                     '--until-day', '2026-07-01', '--passes', '1'], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    deadline = time.time() + 300
    while time.time() < deadline and not any(c['pid'] != orchestrator.pid for c in lines(counts)):
        if orchestrator.poll() is not None:
            break
        time.sleep(0.1)
    child_pid = next((c['pid'] for c in lines(counts) if c['pid'] != orchestrator.pid), None)
    os.kill(orchestrator.pid, signal.SIGKILL)
    orchestrator.wait()
    killed_at = time.time()
    child_ended = False
    while time.time() < killed_at + 120:
        try:
            os.kill(child_pid, 0)
        except (ProcessLookupError, TypeError):
            child_ended = True
            break
        time.sleep(0.2)
    after = [c for c in lines(counts) if c['live'] and c.get('admitted', c['at']) > killed_at]   # admitted after the kill
    state = ledger.read()
    environment_module = orchestrator_module(environment)
    other = environment_module.Draw('prod', root, 'p3', ledger.path, {'until_day': '2026-07-01', 'passes': 1}).launch()
    relaunch = environment_module.Draw('clean', root, 'o1', ledger.path, {'until_day': '2026-07-01', 'passes': 1}).launch()
    report = {'child pid': child_pid, 'child ended on its own': child_ended, 'child sends admitted after the kill': len(after),
              'child sends in all': sum(1 for c in lines(counts) if c['pid'] == child_pid),
              'ledger stop': state['stop_reason'], 'another draw': other.get('refused launches'),
              'relaunch step 1 attempt': relaunch['components'].get('step1', {}).get('attempts', [{}])[-1].get('state')}
    ok = (child_pid is not None and child_ended and not after and state['stop_reason'] == 'the launcher of o1 is gone'
          and other.get('refused launches') and report['relaunch step 1 attempt'] == 'crashed')
    return report, ok


SCENARIOS = {'day': day, 'killed child': killed_child, 'killed orchestrator': killed_orchestrator}


def main(scratch, names):
    scratch = Path(scratch)
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    saved = dict(os.environ)
    judged = passed = 0
    for name in names or list(SCENARIOS):
        folder = scratch / name.replace(' ', '-')
        folder.mkdir()
        try:
            report, ok = SCENARIOS[name](folder)
        except BaseException as error:
            report, ok = {'raised': f'{type(error).__name__}: {str(error)[:300]}'}, False
        finally:
            os.environ.clear()
            os.environ.update(saved)
        judged += 1
        passed += bool(ok)
        print(f"{'ok ' if ok else 'FAIL'} {name}: {json.dumps(report, default=str)}", flush=True)
    print(f'{judged} scenarios judged, {passed} passed')
    return judged > 0 and passed == judged


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2:]) else 1)
