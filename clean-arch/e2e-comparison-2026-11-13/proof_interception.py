"""The $0 interception proof (WIRING-DESIGN.md §C1, §C2 for Stage A, §C4; D448). `urllib.request.urlopen` is replaced by a trap: a call
from a thread that holds no live reservation on the shared ledger is counted and refused; a call that holds one is answered from the
stored run the component made (by the request's own bytes), and a request no stored run holds is counted as a miss and refused. Each
component then runs through its real entry point with a real `SharedLedger`:

  step1   one stored day (2026-07-01) of unseeded draw u1, forward from empty; the sent bytes equal the stored sent request
  step2   the whole stored draw u1 through `budget_step2` (embeddings and Jev); library.json and decisions.json byte for byte
  stageA  run 4 rebuilt from its archives, one pass at a time: every outcome by case and pass
  judge   Stage B's draw u1 through the adapter's live path (no injected transport): every table row for row
  prod    production v118 for 2026-07-01 through `budget_replay` (16 extraction workers): every request found in draw q1's archive
  stop    (§C5) a refusal in Step 1 stops every other component before it sends; a process that crashes between its reservation and
          its settlement leaves the reservation counted
  retry   (council mo R1) a stop written during a Jev or an embeddings retry pause: the retry sends nothing
  bytes   (§C1) the ladder step (run 4, pass 1), the judge (u1) and production (one day) send the same bytes with the ledger as without it

The trap sits under the stop gate (`budget_replay.install_stop_gate`), installed around every component as its entry point installs it,
so it sees only actual sends.

No credential is read (the key readers return a placeholder) and no request leaves the process.

  python3 proof_interception.py <scratch folder> [component ...]
"""
import collections
import concurrent.futures
import importlib.util
import io
import json
import shutil
import sqlite3
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STEP4 = ROOT / 'clean-arch/step4-2026-11-10'
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/e2e-2026-11-09'), str(STEP4 / 'stage_a'), str(STEP4 / 'stage_b'),
                str(STEP4 / 'ladder'), str(ROOT / 'clean-arch/step1')]
from hivemind import jev, model, search, universe  # noqa: E402

PLACEHOLDER = 'proof-placeholder-not-a-credential'
model._key = lambda *arguments: PLACEHOLDER
jev._key = lambda *arguments: PLACEHOLDER
DATA = ROOT / 'poc/data'
U1_TRACE = DATA / 'clean-unseeded-2026-11-10/draw-d1/trace.sqlite'
U1_STEP2 = DATA / 'clean-unseeded-2026-11-10/draw-d1/step2'
RUN4 = DATA / 'clean-ladder-stage-a-2026-11-10/run-4'
Q1 = DATA / 'clean-e2e-comparison-2026-11-13/draw-q1'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


budget_replay = load('budget_replay', HERE / 'budget_replay.py')
budget_step2 = load('budget_step2', HERE / 'budget_step2.py')
budget_step2.budget_replay = budget_replay            # one module, so the trap and the wrappers read the same live-reservation mark


class FakeResponse:
    def __init__(self, payload):
        self.raw, self.status = json.dumps(payload).encode('utf-8'), 200

    def read(self):
        return self.raw

    def __enter__(self):
        return self

    def __exit__(self, *arguments):
        return False


class Trap:
    def __init__(self):
        self.lock = threading.Lock()
        self.handler = None
        self.reset()

    def reset(self, require_reservation=True):
        self.with_reservation = self.without_reservation = 0
        self.misses, self.bodies, self.require_reservation = [], [], require_reservation

    def __call__(self, request, timeout=None):
        with self.lock:
            self.bodies.append(request.data)
        if self.require_reservation and not budget_replay.holds_live_reservation():
            with self.lock:
                self.without_reservation += 1
            # a client refusal, which no component retries, so a bypass fails at once
            raise urllib.error.HTTPError(request.full_url, 403, 'trap: a call without a live ledger reservation', {},
                                         io.BytesIO(b'{"error": {"type": "proof_unreserved"}}'))
        with self.lock:
            self.with_reservation += 1
        try:
            return FakeResponse(self.handler(request.full_url, request.data))
        except LookupError as miss:
            with self.lock:
                self.misses.append(str(miss)[:160])
            raise urllib.error.HTTPError(request.full_url, 400, 'not in the stored run', {}, io.BytesIO(b'{"error": {"type": "proof_miss"}}'))


TRAP = Trap()
urllib.request.urlopen = TRAP


def stored_by_request(archive_paths):
    """{request sha256: deque of stored responses in call order}; a refused or schema-failed row keeps its key with a suffix."""
    stored = collections.defaultdict(collections.deque)
    for path in archive_paths:
        conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
        for key, response in conn.execute('select request_sha256, response_json from model_calls order by call_id'):
            stored[key.split(':', 1)[0]].append(json.loads(response))
        conn.close()
    return stored


def answer_from(stored, lock=threading.Lock()):
    def handler(url, body):
        _, sha = model.request_identity(json.loads(body))
        with lock:
            responses = stored.get(sha)
            if not responses:
                raise LookupError(f'{url}: request {sha[:12]} not stored')
            return responses.popleft() if len(responses) > 1 else responses[0]
    return handler


def fresh_ledger(path, ceiling=50.0):
    budget_replay.SharedLedger.init(path, ceiling)
    return budget_replay.SharedLedger(path)


def table_rows(db_path, query):
    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    try:
        return conn.execute(query).fetchall()
    finally:
        conn.close()


def gated(function):
    """Run a component with the stop gate installed, as its entry point installs it when given a shared ledger."""
    def run(scratch, ledger):
        remove = budget_replay.install_stop_gate(ledger)
        try:
            return function(scratch, ledger)
        finally:
            remove()
    run.__name__ = function.__name__
    return run


@gated
def step1(scratch, ledger):
    import live
    import runner
    rows = table_rows(U1_TRACE, 'select sequence, input_id, request, raw_response, result, after_state, status from trace order by sequence')
    day = [row for row in rows
           if json.JSONDecoder().raw_decode(json.loads(row[2])['messages'][1]['content'])[0]['source_item']['publication_date'] == '2026-07-01']
    by_item = {row[1]: row for row in day}
    byte_mismatches = []

    def handler(url, body):
        request = json.loads(body)
        item_id = json.JSONDecoder().raw_decode(request['messages'][1]['content'])[0]['source_item']['id']
        if item_id not in by_item:
            raise LookupError(f'step 1 item {item_id} not stored')
        raw = json.loads(by_item[item_id][3])
        sent = raw.pop('sent_request', None) or json.loads(by_item[item_id][2])
        if json.dumps(sent).encode('utf-8') != body:
            byte_mismatches.append(item_id)
        return raw
    TRAP.handler = handler
    manifest = json.loads((ROOT / 'clean-arch/e2e-2026-11-09/stage2-manifest.json').read_text())
    manifest.update(until_day='2026-07-01', item_limit=len(day), item_ids=[row[1] for row in day])
    limits = json.loads((ROOT / 'clean-arch/e2e-2026-11-09/stage2-limits.json').read_text())
    settings = dict(json.loads((ROOT / 'clean-arch/e2e-2026-11-09/stage2-settings.json').read_text()), live_limits=limits)
    result = runner.run(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite', scratch / 'step1-trace.sqlite', manifest, [], settings,
                        live.LiveTransport(limits, ledger=ledger), ROOT / 'clean-arch/PRD.md', None, None)
    rebuilt = table_rows(scratch / 'step1-trace.sqlite', 'select sequence, input_id, result, after_state, status from trace order by sequence')
    same = rebuilt == [(r[0], r[1], r[4], r[5], r[6]) for r in day]
    return {'status': result.get('status'), 'items': len(day), 'same results and states as stored': same,
            'sent bytes differ from the stored sent request': byte_mismatches}, same and not byte_mismatches and result.get('status') == 'complete'


def step2(scratch, ledger):
    vectors = json.loads((U1_STEP2 / 'embeddings.json').read_text())
    jev_stored = stored_by_request([U1_STEP2 / 'jev.sqlite'])
    jev_answer = answer_from(jev_stored)

    def handler(url, body):
        if url == search.EMBEDDINGS_URL:
            texts = json.loads(body)['input']
            missing = [t for t in texts if t not in vectors]
            if missing:
                raise LookupError(f'{len(missing)} texts with no stored vector')
            return {'data': [{'index': i, 'embedding': vectors[t]} for i, t in enumerate(texts)],
                    'usage': {'total_tokens': sum(max(1, len(t) // 4) for t in texts)}}
        if url == jev.ENDPOINT:
            return jev_answer(url, body)
        raise LookupError(f'step 2 called {url}')
    TRAP.handler = handler
    status = budget_step2.main(['--shared-ledger', str(ledger.path), str(U1_TRACE), str(scratch / 'step2')])
    same = {name: (scratch / 'step2' / name).read_bytes() == (U1_STEP2 / name).read_bytes() for name in ('library.json', 'decisions.json')}
    return {'exit status': status, 'byte for byte': same}, all(same.values())


@gated
def stage_a(scratch, ledger):
    import stage_a as stage_a_module
    cases = json.loads((STEP4 / 'stage_a/cases.json').read_text())
    research_list = universe.load(str(ROOT / 'poc/universe.json'))
    texts = stage_a_module.request_texts()
    report, ok = {}, True
    for pass_number in (1, 2, 3):
        TRAP.handler = answer_from(stored_by_request([RUN4 / f'send-{pass_number}' / 'archive.sqlite']))
        folder = scratch / f'stage-a-pass-{pass_number}'
        written, limit, jobs = stage_a_module.run(cases, [pass_number], folder, 5.0, research_list=research_list, texts=texts, shared=ledger)
        keep = ('status', 'reason', 'requests', 'answer', 'passage', 'view')
        def by_case(path):
            return {row['case']: {k: row[k] for k in keep} for row in map(json.loads, path.read_text().splitlines())}
        rebuilt = by_case(folder / f'send-{pass_number}' / 'outcomes.jsonl')
        stored = by_case(RUN4 / f'send-{pass_number}' / 'outcomes.jsonl')
        differing = sorted(case for case in stored if rebuilt.get(case) != stored[case])
        report[f'pass {pass_number}'] = {'outcomes': len(rebuilt), 'stored': len(stored), 'differing cases': differing[:6], 'differing': len(differing)}
        ok = ok and len(rebuilt) == len(stored) == 44 and not differing
    return report, ok


@gated
def judge(scratch, ledger):
    import ladder_adapter
    import stored_judgements
    proof_wiring = load('proof_wiring', HERE / 'proof_wiring.py')
    model._key = jev._key = lambda *arguments: PLACEHOLDER    # proof_wiring sets its own refusing readers when loaded
    stored_folder = stored_judgements.stage_b_folders()['u1']
    TRAP.handler = answer_from(stored_by_request([stored_folder / 'archive.sqlite']))
    ladder_adapter.replay('u1', scratch / 'judge-u1', transport=None, cap_usd=5.0, inputs={'output_root': str(scratch)}, shared=ledger)
    differing = proof_wiring.compare(scratch / 'judge-u1' / 'views.sqlite', stored_folder / 'views.sqlite')
    return {'tables differing from Stage B': differing}, not differing


def prod(scratch, ledger):
    TRAP.handler = answer_from(stored_by_request([Q1 / 'archive.sqlite']))
    saved = sys.argv
    sys.argv = ['budget_replay.py', '--ledger', str(ledger.path), '--from', '2026-07-01', '--until', '2026-07-01',
                '--views', str(scratch / 'prod' / 'views.sqlite'), '--archive', str(scratch / 'prod' / 'archive.sqlite'), '--workers', '16']
    try:
        budget_replay.main()
    finally:
        sys.argv = saved
    calls = table_rows(scratch / 'prod' / 'archive.sqlite', 'select count(*) from model_calls')[0][0]
    return {'calls archived': calls}, calls > 0


def stop(scratch, ledger):
    """One ledger with room for a single Step 1 reservation: the second Step 1 send is refused, and then every component refuses before
    any network call. A second ledger: a child process reserves and dies before settling."""
    import subprocess
    import live
    import stage_a as stage_a_module
    import ladder_adapter
    TRAP.handler = lambda url, body: {'choices': [{'message': {'content': '{}'}}], 'usage': {'prompt_tokens': 10, 'completion_tokens': 10}}
    limits = json.loads((ROOT / 'clean-arch/e2e-2026-11-09/stage2-limits.json').read_text())
    request = {'model': 'deepseek-flash', 'max_tokens': 1000, 'messages': [{'role': 'system', 'content': 's'}, {'role': 'user', 'content': 'x'}],
               'response_format': {'type': 'json_schema', 'json_schema': {'name': 'x', 'strict': True, 'schema': {'type': 'object'}}}}
    small = budget_replay.SharedLedger(scratch / 'small.json')
    budget_replay.SharedLedger.init(small.path, 0.006)             # the first request reserves about $0.0035 at the limits' rates
    transport = live.LiveTransport(limits, ledger=small)
    transport('deepseek', request)                                   # fits, sent, settled at its small usage
    outcomes = {}
    try:
        large = dict(request, messages=[request['messages'][0], {'role': 'user', 'content': 'x' * 20000}])
        transport('deepseek', large)                                 # within Step 1's own limits; its reservation (~$0.023) is refused by the ledger
        outcomes['step 1 refused'] = False
    except ValueError:
        outcomes['step 1 refused'] = True
    calls_before = TRAP.with_reservation + TRAP.without_reservation
    luna = {'model': 'gpt-6-luna', 'max_completion_tokens': 10, 'messages': [{'role': 'user', 'content': 'x'}]}
    attempts = {
        'stage A': lambda: stage_a_module.StageALimit(5.0, scratch / 'a.jsonl', sleep=lambda s: None, shared=small).send_labelled('c|1|1', 'openai', luna),
        'judge': lambda: ladder_adapter.LedgerBudget(5.0, scratch / 'b.jsonl', sleep=lambda s: None, shared=small).send('openai', luna),
        'production': lambda: budget_replay.BudgetTransport(small, sleep=lambda s: None)('openai', luna),
        'step 1 again': lambda: live.LiveTransport(limits, ledger=small)('deepseek', request),
    }
    restore = budget_step2.install(small)
    try:
        attempts['step 2 embeddings'] = lambda: search.openai_embeddings(['x'])
        attempts['step 2 jev'] = lambda: jev.transport({'model': 'jev-1.14.0', 'state': [], 'questions': []})
        for name, attempt in attempts.items():
            try:
                attempt()
                outcomes[name] = 'sent'
            except Exception as error:
                outcomes[name] = type(error).__name__
    finally:
        restore()
    no_send = TRAP.with_reservation + TRAP.without_reservation == calls_before
    crashed = budget_replay.SharedLedger(scratch / 'crash.json')
    budget_replay.SharedLedger.init(crashed.path, 1.0)
    child = subprocess.run([sys.executable, '-c', (
        'import importlib.util, os, sys; spec = importlib.util.spec_from_file_location("b", sys.argv[1]); b = importlib.util.module_from_spec(spec); '
        'spec.loader.exec_module(b); b.SharedLedger(sys.argv[2]).reserve(0.6); os._exit(9)'), str(HERE / 'budget_replay.py'), str(crashed.path)])
    held = crashed.read()['reserved']
    refused_after_crash = crashed.reserve(0.5) is False             # 0.6 held + 0.5 would pass 1.0: the dead reservation still counts
    report = {'step 1 refusal': outcomes.pop('step 1 refused'), 'later sends': outcomes, 'no network call after the stop': no_send,
              'ledger stop reason': small.read()['stop_reason'], 'crashed child exit': child.returncode, 'held after the crash': held,
              'a reservation that fits only if the dead one were released: refused': refused_after_crash}
    ok = (report['step 1 refusal'] and small.read()['stopped'] and report['ledger stop reason'] is not None
          and all(value != 'sent' for value in outcomes.values()) and no_send and child.returncode == 9
          and abs(held - 0.6) < 1e-9 and refused_after_crash)
    return report, ok


def retry(scratch, ledger):
    """The first attempt of each helper fails without a reply (both retry it) and, during it, another process stops the run; the
    helper's retry must send nothing."""
    import time
    saved_sleep = time.sleep
    time.sleep = lambda seconds: None
    report, ok = {}, True
    try:
        for name, call in (('jev', lambda: jev.transport({'model': 'jev-1.14.0', 'state': [], 'questions': []})),
                           ('embeddings', lambda: search.openai_embeddings(['a text']))):
            path = scratch / f'{name}.json'
            budget_replay.SharedLedger.init(path, 1.0)
            run_ledger = budget_replay.SharedLedger(path)
            sends = []

            def first_fails_and_the_run_stops(url, body):
                sends.append(url)
                run_ledger.stop('another draw: a reservation was refused')
                raise urllib.error.URLError('connection dropped')       # a reply-less failure: both helpers retry it
            remove_gate = budget_replay.install_stop_gate(run_ledger)
            restore = budget_step2.install(run_ledger)
            original_handler = TRAP.handler
            TRAP.handler = first_fails_and_the_run_stops
            try:
                try:
                    call()
                    outcome = 'answered'
                except Exception as error:
                    outcome = f'{type(error).__name__}: {str(error)[:80]}'
            finally:
                TRAP.handler = original_handler
                restore()
                remove_gate()
            report[name] = {'actual sends': len(sends), 'outcome': outcome, 'stop': run_ledger.read()['stop_reason']}
            ok = ok and len(sends) == 1 and outcome != 'answered'
    finally:
        time.sleep = saved_sleep
    return report, ok


def bytes_check(scratch, ledger):
    """The same component sent once with the ledger (the trap requiring a live reservation) and once without (recording only): the
    multiset of request bodies must be equal, byte for byte."""
    import ladder_adapter
    import stage_a as stage_a_module
    import stored_judgements
    from hivemind import config, parallel_day, replay
    report, ok = {}, True
    research_list = universe.load(str(ROOT / 'poc/universe.json'))
    cases = json.loads((STEP4 / 'stage_a/cases.json').read_text())
    judge_folder = stored_judgements.stage_b_folders()['u1']

    def prod_run(folder, transport):
        cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
        day_runner = parallel_day.ParallelDay(str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'), str(folder / 'manifests'),
                                              extraction_workers=16, jev_workers=8)
        replay.run(testdb_path=str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'), views_path=str(folder / 'views.sqlite'),
                   archive=model.Archive(str(folder / 'archive.sqlite')), cfg=cfg, universe=universe.load(str(ROOT / 'poc/universe.json')),
                   from_day='2026-07-01', until_day='2026-07-01', spend_cap_usd=None, log=lambda *a: None, only_objects={'NVDA'},
                   transport=transport, day_runner=day_runner)

    runs = {
        'ladder (run 4, pass 1)': ([RUN4 / 'send-1' / 'archive.sqlite'],
                                   lambda folder, shared: stage_a_module.run(cases, [1], folder, 5.0, research_list=research_list,
                                                                             texts=stage_a_module.request_texts(), shared=shared)),
        'judge (u1)': ([judge_folder / 'archive.sqlite'],
                       lambda folder, shared: ladder_adapter.replay('u1', folder, transport=None, cap_usd=5.0,
                                                                    inputs={'output_root': str(folder.parent)}, shared=shared)),
        'production (2026-07-01)': ([Q1 / 'archive.sqlite'],
                                    lambda folder, shared: (folder.mkdir(), prod_run(folder, budget_replay.BudgetTransport(shared, sleep=lambda s: None)
                                                                                     if shared is not None else None))),
    }
    for name, (archives, run) in runs.items():
        sent = {}
        for mode in ('without the ledger', 'with the ledger'):
            TRAP.reset(require_reservation=(mode == 'with the ledger'))
            TRAP.handler = answer_from(stored_by_request(archives))
            folder = scratch / f"{name.split()[0]}-{mode.split()[0]}"
            shared = None
            remove = lambda: None
            if mode == 'with the ledger':
                shared = budget_replay.SharedLedger(scratch / f"{name.split()[0]}-ledger.json")
                budget_replay.SharedLedger.init(shared.path, 50.0)
                remove = budget_replay.install_stop_gate(shared)
            try:
                run(folder, shared)
            finally:
                remove()
            sent[mode] = (sorted(TRAP.bodies), TRAP.without_reservation, len(TRAP.misses))
        same = sent['without the ledger'][0] == sent['with the ledger'][0]
        report[name] = {'bodies': len(sent['with the ledger'][0]), 'byte for byte the same': same,
                        'unreserved with the ledger': sent['with the ledger'][1], 'misses': [sent[m][2] for m in sent]}
        ok = ok and same and sent['with the ledger'][0] and sent['with the ledger'][1] == 0 and not any(sent[m][2] for m in sent)
    return report, ok


SELF_JUDGED = {'bytes'}       # judges its own interception, per mode, inside the component


COMPONENTS = {'step1': step1, 'step2': step2, 'stageA': stage_a, 'judge': judge, 'prod': prod, 'stop': stop, 'retry': retry,
              'bytes': bytes_check}


def main(scratch, names):
    scratch = Path(scratch)
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    passed = judged = 0
    for name in names or list(COMPONENTS):
        TRAP.reset()
        ledger = fresh_ledger(scratch / f'ledger-{name}.json')
        (scratch / name).mkdir(exist_ok=True)
        try:
            report, ok = COMPONENTS[name](scratch / name, ledger)
        except BaseException as error:              # a component that stops is reported, not hidden
            report, ok = {'raised': f'{type(error).__name__}: {str(error)[:300]}'}, False
        state = ledger.read()
        intercepted = name in SELF_JUDGED or (TRAP.without_reservation == 0 and TRAP.with_reservation > 0 and not TRAP.misses)
        report.update({'urlopen calls holding a reservation': TRAP.with_reservation, 'without one': TRAP.without_reservation,
                       'misses': TRAP.misses[:3], 'miss count': len(TRAP.misses), 'ledger attempts': state['attempts'],
                       'ledger spent': round(state['spent'], 6), 'ledger reserved after': round(state['reserved'], 9),
                       'ledger stopped': state['stopped']})
        ok = ok and intercepted and (name in ('stop', 'retry', 'bytes') or (state['reserved'] < 1e-9 and not state['stopped']))
        judged += 1
        passed += ok
        print(f"{'ok ' if ok else 'FAIL'} {name}: {json.dumps(report, default=str)}", flush=True)
    print(f'{judged} components judged, {passed} passed')
    return judged > 0 and passed == judged


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2:]) else 1)
