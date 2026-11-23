"""Asserts the probe's spending ceiling and single network attempt with a fake transport (no network, no credential).

  python3 clean-arch/step1-diagnosis-2026-11-12/gate1/check_probe_ceiling.py <scratch folder>
"""
import json, sys, runpy, shutil, threading
from pathlib import Path
probe_path = '/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/probe_c14.py'
cases_path = '/Users/lchingen/hivemind/clean-arch/step1-diagnosis-2026-11-12/cases-gate1.json'
scratch = Path(sys.argv[1])
sys.path[:0] = ['/Users/lchingen/hivemind/src']
from hivemind import model
calls, usage_of = [], {}
fail_first = {'left': 0, 'kind': 'network'}
def fake_transport(provider, request, timeout=180, max_attempts=3):
    calls.append(max_attempts)
    if fail_first['left'] > 0:
        fail_first['left'] -= 1
        if fail_first['kind'] == 'http400':
            error = model.TransportError('HTTP 400: bad request')
            error.http_status = 400
            raise error
        if fail_first['kind'] == 'not-object':
            return ['a list, not an object']
        raise model.TransportError('URLError: a network failure before any answer')
    answer = {'evidence': [], 'new_theses': [], 'unfiled_evidence': []}   # c8's schema refuses unfiled_evidence: a format failure, sent once more
    return {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(answer)}}], 'usage': usage_of['value']}
model.openai_transport = fake_transport
NORMAL = {'prompt_tokens': 10000, 'completion_tokens': 9000}
CASES = [  # label, ceiling, usage returned, expected network calls, expected 'not sent' attempts
    ('tiny ceiling', '0.001', NORMAL, 0, 3),
    ('ample ceiling', '5', NORMAL, 6, 0),
    # three jobs, each reserving about $0.10; two fit under $0.25 and settle at their reservation, so their format-failure resends and the
    # third job are not sent
    ('no usage, room for two reservations', '0.25', None, 2, 3),
    ('malformed usage (a string)', '0.25', 'bad', 2, 3),
    # the first answer's usage passes its reservation: first attempts already in flight still go (one to three, by timing), and every
    # later attempt, resend or first, is not sent, so each of the three jobs ends in exactly one attempt not sent
    # 700,000 input tokens cost $0.21, above the ~$0.10 reservation but far below the $5 ceiling, so only the overrun stop holds them
    ('usage above the reservation stops the run', '5', {'prompt_tokens': 700_000, 'completion_tokens': 0}, (1, 3), 3),
    # one network failure, two resends allowed: that attempt goes out again, so 1 failed call plus 3 jobs x 2 attempts
    ('a network failure is sent again', '5', NORMAL, 7, 0, ['--network-resends', '2'], 1),
    # the same failure with no resends allowed: that job ends lost, the others send both attempts
    ('a network failure is not sent again by default', '5', NORMAL, 5, 0, [], 1),
    # a client HTTP error is an unusable answer: not sent again even with resends allowed
    ('an HTTP 400 is not sent again', '5', NORMAL, 5, 0, ['--network-resends', '2'], 1, 'http400'),
    # a ceiling that holds one reservation (about $0.10) but not two: the non-object response must settle at its reservation, so the
    # other two jobs are refused at once; an unsettled reservation would leave them waiting for ever (the hang guard catches it)
    ('a non-object response settles and does not hang', '0.15', NORMAL, 1, 2, ['--network-resends', '2'], 1, 'not-object'),
]
judged = 0
for label, ceiling, usage, want_calls, want_not_sent, *extra in CASES:
    extra_args, failures, kind = (list(extra) + [[], 0, 'network'][len(extra):]) if extra else ([], 0, 'network')
    fail_first['left'], fail_first['kind'] = failures, kind
    out = scratch / f'out-{judged}'
    shutil.rmtree(out, ignore_errors=True)
    calls.clear(); usage_of['value'] = usage
    sys.argv = [probe_path, cases_path, str(out), '--cases', 'g1a', '--arms', 'c8', '--sends', '1', '--send', '--max-usd', ceiling, *extra_args]
    runner_thread = threading.Thread(target=runpy.run_path, args=(probe_path,), kwargs={'run_name': '__main__'}, daemon=True)
    runner_thread.start(); runner_thread.join(timeout=60)
    assert not runner_thread.is_alive(), f'{label}: the run hung'
    records = [json.loads(l) for l in (out / 'records.jsonl').read_text().splitlines()]
    not_sent = sum(1 for r in records for a in r['attempts'] if str(a.get('outcome', '')).startswith('not sent'))
    low, high = want_calls if isinstance(want_calls, tuple) else (want_calls, want_calls)
    assert low <= len(calls) <= high, f'{label}: {len(calls)} network calls, expected {want_calls}'
    low_ns, high_ns = want_not_sent if isinstance(want_not_sent, tuple) else (want_not_sent, want_not_sent)
    assert low_ns <= not_sent <= high_ns, f'{label}: {not_sent} attempts not sent, expected {want_not_sent}'
    assert set(calls) <= {1}, f'{label}: a send asked for more than one network attempt'
    judged += 1
    print(f'ok  {label}: {len(calls)} network calls, {not_sent} not sent')
print(f'{judged} of {len(CASES)} cases judged and passed')
