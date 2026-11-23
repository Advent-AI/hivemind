"""Asserts BudgetTransport and SharedLedger (budget_replay.py) with fake services: no network, no credential.

  python3 check_budget.py <scratch folder> [module path]     (the module path lets a mutant copy be checked)
"""
import importlib.util
import json
import sys
import threading
from pathlib import Path

scratch = Path(sys.argv[1]); scratch.mkdir(parents=True, exist_ok=True)
module_path = sys.argv[2] if len(sys.argv) > 2 else str(Path(__file__).resolve().parent / 'budget_replay.py')
spec = importlib.util.spec_from_file_location('budget_replay_checked', module_path)
budget = importlib.util.module_from_spec(spec); spec.loader.exec_module(budget)
model, jev = budget.model, budget.jev

REQUEST = {'model': 'gpt-6-luna', 'max_completion_tokens': 16000, 'messages': [{'role': 'user', 'content': 'x' * 20000}]}
JEV_REQUEST = {'model': 'jev-1.14.0', 'state': 'y' * 20000, 'questions': {}}
ONE_LLM = budget.llm_estimate(REQUEST)
ONE_JEV = budget.jev_estimate(JEV_REQUEST)
judged = 0


def fresh(name, ceiling):
    path = scratch / f'{name}.json'
    for p in (path, path.with_suffix('.lock')):
        if p.exists():
            p.unlink()
    budget.SharedLedger.init(path, ceiling)
    return budget.SharedLedger(path)


def ok(response_usage=(10000, 3000)):
    def fake(provider, request, timeout=180, max_attempts=3):
        assert max_attempts == 1, 'each attempt must go out once'
        return {'choices': [{'message': {'content': '{}'}}], 'usage': {'prompt_tokens': response_usage[0], 'completion_tokens': response_usage[1]}}
    return fake


def check(label, condition):
    global judged
    judged += 1
    assert condition, label
    print('ok ', label)


# 1. concurrency: 16 threads, a ceiling that holds about 5 reservations at once; the ledger never passes the ceiling
ledger = fresh('concurrency', 5.5 * ONE_LLM)
worst = [0.0]
original_reserve = ledger.reserve
def watched_reserve(amount):
    result = original_reserve(amount)
    state = ledger.read()
    worst[0] = max(worst[0], state['spent'] + state['reserved'])
    return result
ledger.reserve = watched_reserve
model.openai_transport = ok()
transport = budget.BudgetTransport(ledger, sleep=lambda s: None)
outcomes = []
def worker():
    for _ in range(20):
        try:
            transport('openai', REQUEST); outcomes.append('sent')
        except model.TransportError:
            outcomes.append('refused')
threads = [threading.Thread(target=worker) for _ in range(16)]
[t.start() for t in threads]; [t.join() for t in threads]
state = ledger.read()
check('concurrency: spent plus reserved never passed the ceiling', worst[0] <= state['ceiling'] + 1e-12)
check('concurrency: some calls refused once the ceiling was near', outcomes.count('refused') > 0 and outcomes.count('sent') > 0)
check('concurrency: nothing left reserved after every call settled', abs(state['reserved']) < 1e-9)

# 2. Jev: called with one argument, reserves three attempts, settles at its usage
ledger = fresh('jev', 10.0)
jev.transport = lambda request, timeout=60: {'answers': {}, 'usage': {'input_tokens': 1000}}
budget.BudgetTransport(ledger)(JEV_REQUEST)
state = ledger.read()
check('jev: one-argument call settles at three times its reported input tokens', abs(state['spent'] - 3 * 1000 * model.PRICES['jev-1.14.0'][0] / 1e6) < 1e-15 and state['reserved'] == 0)
check('jev: the reservation covers its three internal attempts', abs(ONE_JEV - 3 * (2 * len(json.dumps(JEV_REQUEST, sort_keys=True, ensure_ascii=False).encode()) + 4096) * model.PRICES['jev-1.14.0'][0] / 1e6) < 1e-15)

# 2b. Jev through its own retry: the real jev.transport, its network failing once (a fake urlopen, a fake key, no network), retries and
# answers; the ledger keeps three times the answered input; a reported zero, or no usage, keeps the whole reservation; a charge above the
# reservation sets the overrun flag
import os, io, urllib.error
os.environ[jev.KEY_NAME] = 'fake-key-for-the-check'          # not a credential: the fake service never reads it
real_transport = budget.jev.transport.__wrapped__ if hasattr(budget.jev.transport, '__wrapped__') else None
import importlib
jev_module = importlib.reload(jev)                             # the real transport again (the earlier checks replaced it)
budget.jev = jev_module
jev_module.time.sleep = lambda s: None
answers = {'n': 0}
class FakeReply(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False
def flaky_urlopen(req, timeout=60):
    answers['n'] += 1
    if answers['n'] == 1:
        raise urllib.error.URLError('dropped')
    return FakeReply(json.dumps(answers['body']).encode())
jev_module.urllib.request.urlopen = flaky_urlopen
def jev_call(body, ceiling=10.0, name='jev-retry'):
    answers['n'], answers['body'] = 0, body
    led = fresh(name, ceiling)
    budget.BudgetTransport(led)(JEV_REQUEST)
    return led.read(), answers['n']
state, attempts = jev_call({'answers': {}, 'usage': {'input_tokens': 5000}})
check('jev retry: the real client retried once and the ledger kept three times the answered input', attempts == 2 and abs(state['spent'] - 3 * 5000 * model.PRICES['jev-1.14.0'][0] / 1e6) < 1e-15)
state, _ = jev_call({'answers': {}, 'usage': {'input_tokens': 0}}, name='jev-zero')
state2, _ = jev_call({'answers': {}}, name='jev-none')
check('jev usage zero or missing: the whole reservation', abs(state['spent'] - ONE_JEV) < 1e-15 and abs(state2['spent'] - ONE_JEV) < 1e-15)
state, _ = jev_call({'answers': {}, 'usage': {'input_tokens': 10_000_000}}, name='jev-over')
check('jev charge above its reservation: settled in full and the overrun flag set', state['overrun'] and state['spent'] > ONE_JEV)

# 3. retries: two network failures then an answer: three attempts, the failures counted at their reservation
ledger = fresh('retry', 10.0)
calls = {'n': 0}
def flaky(provider, request, timeout=180, max_attempts=3):
    calls['n'] += 1
    if calls['n'] < 3:
        raise model.TransportError('URLError: dropped')
    return ok()(provider, request, max_attempts=max_attempts)
model.openai_transport = flaky
budget.BudgetTransport(ledger, sleep=lambda s: None)('openai', REQUEST)
state = ledger.read()
expected = 2 * ONE_LLM + (10000 * 0.10 + 3000 * 0.50) / 1e6
check('retry: three attempts sent, two failures at their reservation, the answer at its usage', calls['n'] == 3 and abs(state['spent'] - expected) < 1e-12)

# 4. a client HTTP error is not sent again
ledger = fresh('client', 10.0)
calls = {'n': 0}
def bad_request(provider, request, timeout=180, max_attempts=3):
    calls['n'] += 1
    error = model.TransportError('HTTP 400: bad'); error.http_status = 400
    raise error
model.openai_transport = bad_request
try:
    budget.BudgetTransport(ledger, sleep=lambda s: None)('openai', REQUEST)
except model.TransportError:
    pass
check('client error: HTTP 400 sent once, not again', calls['n'] == 1)

# 5. an answer costing more than its reservation refuses every later attempt
ledger = fresh('overrun', 10.0)
model.openai_transport = ok(response_usage=(10_000_000, 2_000_000))
budget.BudgetTransport(ledger, sleep=lambda s: None)('openai', REQUEST)
model.openai_transport = ok()
try:
    budget.BudgetTransport(ledger, sleep=lambda s: None)('openai', REQUEST); later = 'sent'
except model.TransportError:
    later = 'refused'
check('overrun: a later attempt is refused', ledger.read()['overrun'] and later == 'refused')

# 6. a request without an output cap is refused before any send; a response without usage settles at its reservation
ledger = fresh('nocap', 10.0)
try:
    budget.BudgetTransport(ledger)('openai', {'model': 'gpt-6-luna', 'messages': []}); nocap = 'sent'
except model.TransportError:
    nocap = 'refused'
model.openai_transport = lambda provider, request, timeout=180, max_attempts=3: {'choices': [{'message': {'content': '{}'}}]}
budget.BudgetTransport(ledger)('openai', REQUEST)
check('no output cap: refused; no usage: settled at the reservation', nocap == 'refused' and abs(ledger.read()['spent'] - ONE_LLM) < 1e-12)

# 7. a refusal persists: after one component is refused, a later affordable reservation in another process is refused too
import subprocess
ledger = fresh('persisted', ONE_LLM + 0.001)   # one whole reservation fits; after its spend (about $0.0025) a second does not
model.openai_transport = ok()
budget.BudgetTransport(ledger)('openai', REQUEST)                       # spends well under the ceiling
try:
    budget.BudgetTransport(ledger)('openai', REQUEST); refused_here = False  # a second whole reservation would pass it
except model.TransportError:
    refused_here = True
probe = subprocess.run([sys.executable, '-c', (
    "import importlib.util, sys; spec = importlib.util.spec_from_file_location('b', sys.argv[1]); b = importlib.util.module_from_spec(spec); "
    "spec.loader.exec_module(b); print(b.SharedLedger(sys.argv[2]).reserve(1e-9))"), module_path, str(ledger.path)], capture_output=True, text=True)
check('persisted stop: a refusal here refuses a tiny reservation in another process', refused_here and probe.stdout.strip() == 'False' and ledger.read()['stopped'])
ledger = fresh('explicit', 10.0)
ledger.stop('a component stopped')
check('explicit stop: every later reservation is refused, with its reason', ledger.reserve(1e-9) is False and ledger.read()['stop_reason'] == 'a component stopped')

# 8. an answered paid request never settles at nothing; malformed usage never raises between reserve and settle (council mo R3)
ledger = fresh('zero-charge', 10.0)
for charge in (0, 0.0, -0.5, None, float('nan'), True):
    assert ledger.reserve(0.01)
    ledger.settle(0.01, charge)
state = ledger.read()
check('a zero, negative, missing, non-finite or boolean charge settles at the whole reservation', abs(state['spent'] - 0.06) < 1e-12 and state['reserved'] < 1e-12)
malformed = [{'usage': {'prompt_tokens': -5, 'completion_tokens': 10}}, {'usage': {'prompt_tokens': 0, 'completion_tokens': 0}},
             {'usage': {'prompt_tokens': '12', 'completion_tokens': 3}}, {'usage': {'prompt_tokens': 10, 'completion_tokens': True}},
             {'usage': {'prompt_tokens': 10, 'completion_tokens': 3, 'prompt_tokens_details': {'cached_tokens': -1}}}, {'usage': None}]
check('malformed usage is no cost (settled at the reservation), never an error', all(budget.llm_cost(r, REQUEST) is None for r in malformed)
      and budget.llm_cost({'usage': {'prompt_tokens': 10, 'completion_tokens': 3}}, REQUEST) > 0)

# 9. the measurement record: one line per settled or refused attempt, with the process that made it
ledger = fresh('attempt-lines', 0.025)
assert ledger.reserve(0.01)
ledger.settle(0.01, 0.004)
ledger.reserve(0.05)                                    # refused: passes the ceiling
attempt_lines = [json.loads(line) for line in ledger.attempts_path.read_text().splitlines()]
check('every settled and refused attempt is one line with its process id and kind', [sorted(k for k in line if k != 'at') for line in attempt_lines]
      == [['charged', 'kind', 'pid', 'reserved'], ['pid', 'refused']] and all(line['pid'] == os.getpid() for line in attempt_lines))

# 10. a failed attempt-line append never blocks a refusal's stop or an overrun (council mo, slice round 2)
ledger = fresh('note-fails', 0.02)
ledger.attempts_path.mkdir()                             # every append now fails (a directory)
assert ledger.reserve(0.01)
ledger.settle(0.01, 0.015, kind='embeddings', tokens=10)  # an overrun
refused = ledger.reserve(1e-9)
state = ledger.read()
check('with the attempt line failing, the overrun and the stop are still saved and every later reservation refused',
      state['overrun'] and state['stopped'] and abs(state['spent'] - 0.015) < 1e-12 and refused is False)

print(f'{judged} of 18 checks judged and passed')
