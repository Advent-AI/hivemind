"""The paid acceptance probe's $0 rehearsal (PROBE-DESIGN.md v5 §4; D716): `probe.Probe` runs unchanged on the real budget transport,
the real `model.openai_transport` and the real stop gate, with the network call (`urllib.request.urlopen`) replaced by a stub that
compares each HTTP body, byte for byte, with a request it builds itself, counts the calls and answers by scenario. A dummy API key is
set in this process so no credential is read.

  python3 probe.py rehearse <new out folder> <scenario>
  scenarios: clean, format-invalid, a1-400, a1-timeout, 5xx-then-ok, low-ceiling, retry-exhausts, a2-stop, mutant-open-b, mutant-order,
             checks, verdicts, all
"""
import io
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / 'tests'))
import probe                                                            # noqa: E402
import probe_read                                                       # noqa: E402
from hivemind import model                                              # noqa: E402
from hivemind.views import judging                                     # noqa: E402

PLAN = json.loads(probe.PLAN.read_text())
ITEMS = {i['user']: i for i in PLAN['acceptance'] + PLAN['refused'] + PLAN['matched']}
BY_KEY = {probe.key_of(i): i for i in PLAN['acceptance'] + PLAN['refused'] + PLAN['matched']}
TARGETS, STORED = json.loads(probe_read.TARGETS.read_text()), json.loads(probe_read.STORED_V7.read_text())


def valid_answer(item, drop_marker=None):
    lists = item['lists']
    previous = re.search(r'^\[Previous conclusion, for comparison only\] rung (\d+);', item['user'], re.M)
    cites = lists['evidence'][:3]
    reasons = 'scripted reasons; the consensus growth estimate of 85.4% sits at rung 1; $393 billion is the reference.'
    if drop_marker:
        reasons = reasons.replace(drop_marker, 'an earlier figure')
    return {'rung': int(previous.group(1)) if previous else 1, 'reference': 'scripted reference', 'implied_outcome': 'scripted outcome',
            'reasons': reasons, 'cites': cites, 'cites_views': [], 'pushes': [{'evidence_id': e, 'push': 'none'} for e in cites],
            'changed': previous is None, 'why_changed': 'scripted', 'theme_pushes': [{'view_id': t, 'push': 'none'} for t in lists['themes'][:1]]}


class FakeResponse:
    def __init__(self, body):
        self.body, self.status = body, 200

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def http_error(url, code):
    return urllib.error.HTTPError(url, code, f'HTTP {code}', {}, io.BytesIO(json.dumps({'error': {'code': code}}).encode()))


class HttpStub:
    """Stands in for `urllib.request.urlopen`: the body must equal, byte for byte, the request this stub builds from the plan (never from
    the code under test); calls are counted per (request, format); the answer depends on the scenario."""

    def __init__(self, cfg, scenario, ledger):
        self.cfg, self.scenario, self.ledger, self.calls, self.problems = cfg, scenario, ledger, {}, []

    def __call__(self, http_request, *args, **kwargs):
        body = http_request.data
        request = json.loads(body)
        user = request['messages'][1]['content']
        item = ITEMS.get(user)
        if item is None or request['messages'][0]['content'] != item['system']:
            self.problems.append('a request whose text is not a planned one')
            raise http_error(http_request.full_url, 400)
        setting = self.cfg.rejudging
        expected = lambda schema: json.dumps({'model': setting.model, 'messages': [{'role': 'system', 'content': item['system']}, {'role': 'user', 'content': user}],
                                              'response_format': {'type': 'json_schema', 'json_schema': {'name': 'judgement', 'strict': True, 'schema': schema}},
                                              'max_completion_tokens': setting.max_output_tokens, 'reasoning_effort': setting.reasoning_effort}).encode('utf-8')
        form = next((f for f, schema in (('v12', judging.schema_for('judging-v12', item['lists'])), ('v7', judging.schema_for('judging-v7')))
                     if body == expected(schema)), None)
        key = probe.key_of(item)
        part = 'B' if item in PLAN['refused'] else ('C' if item in PLAN['matched'] else 'A')
        if form is None or (part in ('A', 'B') and form != 'v12'):
            self.problems.append(f'{key}: the body is not the planned request for part {part}')
        count_key = (key, form)
        self.calls[count_key] = self.calls.get(count_key, 0) + 1
        attempt, s = self.calls[count_key], self.scenario
        if s == 'a2-stop' and key == 'sealed-D358:6918':
            self.ledger.stop('rehearsal: the ledger stops during A2')
            raise http_error(http_request.full_url, 503)
        if s == 'a1-400' and key == 'old-1:5652':
            raise http_error(http_request.full_url, 400)
        if s == 'a1-timeout' and key == 'old-1:5652':
            raise TimeoutError('timed out')
        if s == '5xx-then-ok' and key == 'old-3:69' and attempt == 1:
            raise http_error(http_request.full_url, 503)
        if s == 'retry-exhausts' and part == 'C' and key == probe.key_of(PLAN['matched'][0]) and form == 'v12' and attempt == 2:
            raise http_error(http_request.full_url, 503)
        data = valid_answer(item, drop_marker='85.4' if s == 'clean' and key == 'control-1:8938' and attempt == 1 else None)
        if s == 'format-invalid' and key == 'old-2:591' and attempt == 1:
            data['cites'] = data['cites'] + ['e999999']
        usage = {'prompt_tokens': 1000, 'completion_tokens': 100}
        if s == 'retry-exhausts' and part == 'C':                      # each answer costs its full reservation, so a retry's extra charge exhausts the headroom
            usage = {'prompt_tokens': 2 * len(body) + 4096, 'completion_tokens': request['max_completion_tokens']}
        return FakeResponse(json.dumps({'choices': [{'message': {'content': json.dumps(data)}}], 'usage': usage}).encode('utf-8'))


def run(out, scenario):
    budget = probe.budget_module()
    out.mkdir(parents=True)
    ledger_path = out / 'ledger.json'
    budget.SharedLedger.init(str(ledger_path), probe.APPROVED_CEILING)
    ledger = budget.SharedLedger(str(ledger_path))
    p = probe.Probe(out, budget.BudgetTransport(ledger, sleep=lambda seconds: None), ledger, budget)
    stub = HttpStub(p.cfg, scenario, ledger)
    saved = (urllib.request.urlopen, model.openai_transport, probe.answer_format, os.environ.get('OPENAI_API_KEY'))
    os.environ['OPENAI_API_KEY'] = 'rehearsal-dummy-not-a-key'
    urllib.request.urlopen = stub
    remove_gate = budget.install_stop_gate(ledger)                       # the gate wraps the stub, as it wraps the network in the send
    model.openai_transport = probe.counting(saved[1])                    # the real transport, with the send's counting wrapper
    if scenario == 'mutant-open-b':
        probe.answer_format = lambda item, form: judging.schema_for('judging-v7') if item in PLAN['refused'] else saved[2](item, form)
    if scenario == 'mutant-order':                                      # the same schema with its properties reversed: equal as a dict, not on the wire
        def reordered(item, form):
            schema = saved[2](item, form)
            return dict(schema, properties=dict(reversed(list(schema['properties'].items())))) if item in PLAN['refused'] else schema
        probe.answer_format = reordered
    first_c = probe.schedule(PLAN)[3][1][0]
    need_c1 = sum(p.reservation(s) for s in first_c)
    original_headroom = p.headroom

    def lowered():
        if scenario in ('low-ceiling', 'retry-exhausts') and not getattr(lowered, 'done', False) and \
                sum(1 for line in (out / 'answers.jsonl').read_text().splitlines() if '"part": "B"' in line) == 48:
            state = ledger.read()
            with ledger._locked() as s:
                s['ceiling'] = state['spent'] + (need_c1 * 0.5 if scenario == 'low-ceiling' else need_c1 + 0.0005)
            lowered.done = True
        return original_headroom()
    p.headroom = lowered
    try:
        summary = p.run(PLAN)
    finally:
        remove_gate()
        urllib.request.urlopen, model.openai_transport, probe.answer_format = saved[0], saved[1], saved[2]
        if saved[3] is None:
            os.environ.pop('OPENAI_API_KEY', None)
        else:
            os.environ['OPENAI_API_KEY'] = saved[3]
    return summary, stub, probe_read.load_answers(out)


def expect(name, condition, detail=''):
    print(f'  [{"ok" if condition else "FAIL"}] {name}{(": " + detail) if detail and not condition else ""}')
    return bool(condition)


def clean_readings(overrides=None, answers=None):
    """Clean readings, the overrides applied, then (when answers are given) only for answers received and comparisons complete."""
    b = {}
    for request in TARGETS['requests']:
        for d in (1, 2, 3):
            for target in request['targets']:
                cls = 'ambiguous' if target.get('ambiguous') else ('intended' if target['kind'] == 'evidence' else 'correct')
                b[f'{request["key"]}|{d}|{probe_read.target_ids(target)}'] = {'class': cls, 'valid_support': target['kind'] == 'evidence' and not target.get('ambiguous')}
    readings = {'B': b, 'C': {probe.key_of(i): {'read': True, 'harms': []} for i in PLAN['matched']}}
    for key, value in (overrides or {}).items():
        part, name = key.split('/', 1)
        if value is None:
            readings[part].pop(name, None)
        else:
            readings[part][name] = value
    if answers is not None:
        readings['B'] = {k: r for k, r in readings['B'].items()
                         if probe_read.received(answers.get(('B', k.split('|')[0], 'v12', int(k.split('|')[1]))))}
        readings['C'] = {k: r for k, r in readings['C'].items()
                         if all(probe_read.received(answers.get(('C', k, f, d))) for f in ('v12', 'v7') for d in (1, 2, 3))}
    return readings


def clean_answers():
    answers = {}
    for _, specs in probe.schedule(PLAN):
        for s in [s for group in specs for s in (group if isinstance(group, list) else [group])]:
            answers[(s['part'], s['key'], s['form'], s['draw'])] = {'part': s['part'], 'key': s['key'], 'form': s['form'], 'draw': s['draw'],
                                                                     'status': 'answered', 'check': [], 'data': valid_answer(BY_KEY[s['key']])}
    return answers


def verdict_of(answers, readings, summary=None):
    return probe_read.verdict(answers, readings, PLAN, TARGETS, STORED, summary or {'ledger': {'stopped': False}})


def scenario_checks(out, scenario):
    summary, stub, answers = run(out / scenario, scenario)
    ok = True
    print(scenario)
    if scenario == 'clean':
        ok &= expect('no request problem', not stub.problems, str(stub.problems[:3]))
        ok &= expect('2 + 48 + 72 + A2 answers', sum(1 for a in answers.values() if a['part'] in ('A1', 'A0')) == 2 and
                     sum(1 for a in answers.values() if a['part'] == 'B') == 48 and sum(1 for a in answers.values() if a['part'] == 'C') == 72 and summary['A2'] == 'answered')
        ok &= expect('three fresh calls per planned request and format', all(v == 3 for (k, f), v in stub.calls.items()
                     if not k.startswith(('old-1:5652', 'old-3:69', 'sealed')) and f is not None), str({k: v for k, v in stub.calls.items() if v != 3}))
        ok &= expect('every answer answered and passing the request-time check', all(a['status'] == 'answered' and not a['check'] and not a['cached'] for a in answers.values()))
        ok &= expect('records carry provider attempts and charges', all('provider_attempts' in a and 'charged_usd' in a for a in answers.values())
                     and sum(a['provider_attempts'] for a in answers.values()) == 123)
        probe_read.packets(out / scenario)
        packet = json.loads((out / scenario / 'packet-B.json').read_text())
        flagged = [e for e in packet if e['id'].startswith('control-1:8938|') and e['id'].endswith('|e362') and '85.4' in e['markers not found']]
        ok &= expect('the 8938 packet flags the one answer that drops 85.4', len(flagged) == 1)
        ok &= packet_quotes_match_the_store(out / scenario)
        ok &= expect('the clean run verdict is pass', verdict_of(answers, clean_readings(answers=answers), summary)[0] == 'pass')
    elif scenario == 'format-invalid':
        ok &= expect('the format-invalid answer takes the SchemaError path', answers[('B', 'old-2:591', 'v12', 1)]['status'] == 'format invalid')
        ok &= expect('verdict not ready', verdict_of(answers, clean_readings(answers=answers), summary)[0] == 'not ready')
    elif scenario == 'a1-400':
        ok &= expect('A1 recorded as a 400', answers[('A1', 'old-1:5652', 'v12', 1)].get('http_status') == 400)
        ok &= expect('nothing after A1 is sent', set(a['part'] for a in answers.values()) == {'A1'} and set(k for k, f in stub.calls) == {'old-1:5652'})
    elif scenario == 'a1-timeout':
        line = answers[('A1', 'old-1:5652', 'v12', 1)]
        ok &= expect('A1 a transport error without a status, after three attempts', line['status'] == 'transport error' and line.get('http_status') is None
                     and stub.calls[('old-1:5652', 'v12')] == 3 and line.get('provider_attempts') == 3)
        ok &= expect('nothing after A1 is sent', set(a['part'] for a in answers.values()) == {'A1'})
    elif scenario == '5xx-then-ok':
        line = answers[('A0', 'old-3:69', 'v12', 1)]
        ok &= expect('A0 answered after a 503 retry, the failed attempt charged', line['status'] == 'answered' and stub.calls[('old-3:69', 'v12')] == 2
                     and line['provider_attempts'] == 2 and line['charged_usd'] > 0.001)
    elif scenario == 'low-ceiling':
        ok &= expect('the first Part C comparison is not started', summary['not started'] and summary['not started'][0]['key'] == probe.key_of(PLAN['matched'][0]))
    elif scenario == 'retry-exhausts':
        ok &= expect('the admitted comparison is interrupted by the refused retry reservation', summary['interrupted'] == [probe.key_of(PLAN['matched'][0])]
                     and summary['ledger']['stopped'])
    elif scenario == 'a2-stop':
        ok &= expect('the ledger stopped during A2, the core ledger did not', summary['ledger']['stopped'] and not summary['core ledger']['stopped'])
        ok &= expect('a stop during A2 leaves the core verdict pass', verdict_of(answers, clean_readings(answers=answers), summary)[0] == 'pass')
    elif scenario in ('mutant-open-b', 'mutant-order'):
        ok &= expect(f'the byte check catches {scenario}', any('not the planned request for part B' in p for p in stub.problems))
    if scenario in ('low-ceiling', 'retry-exhausts', 'a1-timeout', 'a1-400'):
        expected = 'not ready (format)' if scenario == 'a1-400' else 'inconclusive (incomplete)'
        result = verdict_of(answers, clean_readings(answers=answers), summary)
        ok &= expect(f'verdict {expected}', result[0] == expected, str(result))
    return ok


def verdict_cases():
    v = lambda answers, overrides=None, summary=None: verdict_of(answers, clean_readings(overrides, answers), summary)[0]
    unsupported = lambda key, bad: {f'B/{key}|{d}|{bad}': {'class': 'unsupported', 'valid_support': False} for d in (1, 2, 3)}
    misattributed = {f'B/old-2:591|{d}|e88': {'class': 'misattributed', 'valid_support': True} for d in (1, 2, 3)}
    two_wrong_one_omitted = {'B/control-1:8807|1|e393': {'class': 'misattributed', 'valid_support': False},
                             'B/control-1:8807|2|e393': {'class': 'misattributed', 'valid_support': False},
                             'B/control-1:8807|3|e393': {'class': 'omitted', 'valid_support': False}}
    variant = lambda changes: dict(clean_answers(), **{}) if not changes else {**clean_answers(), **changes}
    first_c = probe.key_of(PLAN['matched'][0])
    missing_two = clean_answers()
    for d in (2, 3):
        missing_two.pop(('B', 'control-1:8807', 'v12', d))
    c_incomplete = clean_answers()
    c_incomplete.pop(('C', probe.key_of(PLAN['matched'][-1]), 'v7', 3))
    a2_skipped = clean_answers()
    a2_skipped.pop(('A2', 'sealed-D358:6918', 'v12', 1))
    line = lambda part, key, form, draw, **fields: {(part, key, form, draw): dict({'part': part, 'key': key, 'form': form, 'draw': draw}, **fields)}
    cases = [
        ('clean set', v(clean_answers()), 'pass'),
        ('8938 85.4% unsupported in three draws', v(clean_answers(), unsupported('control-1:8938', 'e362')), 'inconclusive (unresolved)'),
        ('8807 $393B unsupported in three draws', v(clean_answers(), unsupported('control-1:8807', 'e393')), 'not ready'),
        ('three misattributions', v(clean_answers(), misattributed), 'not ready'),
        ('8807 two wrong, one omitted', v(clean_answers(), two_wrong_one_omitted), 'not ready'),
        ('8807 one unsupported, two missing', v(missing_two, {'B/control-1:8807|1|e393': {'class': 'unsupported', 'valid_support': False}}), 'inconclusive (incomplete)'),
        ('A1 rejected', v(variant(line('A1', 'old-1:5652', 'v12', 1, status='transport error', http_status=400, error='HTTP 400'))), 'not ready (format)'),
        ('A1 timed out', v(variant(line('A1', 'old-1:5652', 'v12', 1, status='transport error', http_status=None))), 'inconclusive (incomplete)'),
        ('misattribution excess with Part C incomplete', v(c_incomplete, misattributed), 'not ready'),
        ('unresolved Part C difference, all else clean', v(clean_answers(), {f'C/{first_c}': {'read': True, 'harms': [{'kind': 'a', 'status': 'unresolved'}]}}), 'inconclusive (unresolved)'),
        ('A2 skipped', v(a2_skipped), 'pass'),
        ('A2 rejected', v(variant(line('A2', 'sealed-D358:6918', 'v12', 1, status='transport error', http_status=400))), 'pass'),
        ('a refused v12 answer', v(variant(line('B', 'old-2:591', 'v12', 1, status='answered', check=['x'], data=valid_answer(BY_KEY['old-2:591'])))), 'not ready'),
        ('a ledger stop in the core run', v(clean_answers(), None, {'core ledger': {'stopped': True, 'stop_reason': 'ceiling'}}), 'inconclusive (incomplete)'),
        ('a Part C control with no content', v(variant(line('C', first_c, 'v7', 1, status='format invalid', data=None))), 'inconclusive (incomplete)'),
        ('a Part C control answering {}', v(variant(line('C', first_c, 'v7', 1, status='answered', check=[], data={}))), 'inconclusive (incomplete)'),
        ('a readable v7 control the request-time check refuses still counts', v(variant(line('C', first_c, 'v7', 1, status='answered', check=['x'], data=valid_answer(BY_KEY[first_c])))), 'pass'),
    ]
    ok = True
    print('verdicts')
    for name, got, want in cases:
        ok &= expect(f'{name} -> {want}', got == want, got)
    refusals = {
        '"false" as a string': clean_readings({f'B/control-1:8807|{d}|e393': {'class': 'unsupported', 'valid_support': 'false'} for d in (1, 2, 3)}),
        'omitted with valid support': clean_readings({f'B/control-1:8807|{d}|e393': {'class': 'omitted', 'valid_support': True} for d in (1, 2, 3)}),
        'harms on a comparison not read': clean_readings({f'C/{first_c}': {'read': False, 'harms': [{'kind': 'a', 'status': 'confirmed'}]}}),
        'a reading of a missing answer': clean_readings(),
        'a reading of no planned target': clean_readings({'B/old-2:591|1|e000': {'class': 'intended', 'valid_support': True}}),
        'misattributed on a target frozen as ambiguous': clean_readings({f'B/control-1:8938|{d}|e3111': {'class': 'misattributed', 'valid_support': False} for d in (1, 2, 3)}),
        'ambiguous on a target not frozen as ambiguous': clean_readings({f'B/control-1:8807|{d}|e393': {'class': 'ambiguous', 'valid_support': True} for d in (1, 2, 3)}),
    }
    for name, readings in refusals.items():
        answers = missing_two if name == 'a reading of a missing answer' else clean_answers()
        try:
            verdict_of(answers, readings)
            refused = False
        except ValueError:
            refused = True
        ok &= expect(f'readings refused: {name}', refused)
    return ok


def packet_quotes_match_the_store(folder):
    """Every evidence entry quoted in the packets carries its quote as the request printed it (the stored quote's first 400 characters),
    read from the stores themselves, never from the packet parser; old-2's e4070 (a multiline quote ending with the closing date) included."""
    import sqlite3
    import t2_offline
    stores = {label: sqlite3.connect(f'file:{folder_ / "views.sqlite"}?mode=ro', uri=True) for label, folder_, _ in t2_offline.SOURCES}
    missing, checked = [], 0
    for packet_name in ('packet-B.json', 'packet-C.json'):
        for entry in json.loads((folder / packet_name).read_text()):
            key = entry['id'].split('|')[0] if 'id' in entry else entry['key']
            for evidence_id, text in entry['quotes'].items():
                if not evidence_id.startswith('e') or text == '(not listed)':
                    continue
                row = stores[key.split(':')[0]].execute('select quote from evidence where evidence_id=?', (evidence_id,)).fetchone()
                checked += 1
                if row is None or 'Quote: ' + row[0][:400] not in text:
                    missing.append(f'{key} {evidence_id}')
    e4070 = probe_read.entries(BY_KEY['old-2:6955']['user']).get('e4070', '')
    row = stores['old-2'].execute('select quote from evidence where evidence_id=?', ('e4070',)).fetchone()
    ok = expect(f'every packet quote carries its stored quote in full ({checked} checked)', checked > 0 and not missing, str(missing[:5]))
    ok &= expect('old-2:6955 e4070, a multiline quote, is kept whole', '\n' in row[0][:400] and 'Quote: ' + row[0][:400] in e4070)
    return ok


def check_equivalence():
    """check_at_request equals judging.check_answer on a ledger whose state is known, and on the planned requests' stored answers."""
    import test_theme_block as fixtures
    ok = True
    print('checks')
    with tempfile.TemporaryDirectory() as scratch:
        conn = fixtures.ledger(Path(scratch))
        fixtures.judged(conn, 'v2', 1, 'theme judged', 2)
        conn.commit()
        _, user, lists = judging.request_parts(conn, 'v1', 'judging-v12')
        base = {'rung': 2, 'reference': 'r', 'implied_outcome': 'o', 'reasons': 'x', 'cites': ['e1'], 'cites_views': [], 'pushes': [], 'changed': True,
                'why_changed': 'w', 'theme_pushes': [{'view_id': 'v2', 'push': 'none'}]}
        variants = [base, dict(base, rung=9), dict(base, changed=False), dict(base, reference=''), dict(base, cites=['e9']),
                    dict(base, theme_pushes=[{'view_id': 'v2', 'push': 'none'}] * 2), dict(base, cites_views=['v3'])]
        for data in variants:
            ok &= expect(f'equal on {json.dumps({k: data[k] for k in data if data[k] != base.get(k)})}',
                         probe.check_at_request(data, user, lists) == judging.check_answer(conn, 'v1', data, user, lists))
        fixtures.judged(conn, 'v1', 3, 'first', 3)
        conn.commit()
        _, user, lists = judging.request_parts(conn, 'v1', 'judging-v12')
        for data in (dict(base, rung=2, changed=False), dict(base, rung=3, changed=False)):
            ok &= expect(f'equal with a previous conclusion, rung {data["rung"]} changed false',
                         probe.check_at_request(data, user, lists) == judging.check_answer(conn, 'v1', data, user, lists))
    stored_ok = all(not probe.check_at_request(json.loads(i['stored answer']), i['user'], i['lists']) for i in PLAN['matched'])
    ok &= expect('every planned matched request\'s stored committed answer passes (linked-1 8834 included)', stored_ok)
    bad = [i for i in PLAN['refused'] if not all(any(b in e for e in probe.check_at_request(json.loads(i['stored answer']), i['user'], i['lists'])) for b in i['bad ids'] if b in json.dumps(json.loads(i['stored answer'])))]
    ok &= expect('every planned refused request\'s stored answer is refused on its bad ids', not bad, str([probe.key_of(i) for i in bad]))
    return ok


def main(out, scenario):
    if out.exists():
        raise SystemExit(f'{out} exists: a rehearsal starts from an empty folder')
    out.mkdir(parents=True)
    names = ['clean', 'format-invalid', 'a1-400', 'a1-timeout', '5xx-then-ok', 'low-ceiling', 'retry-exhausts', 'a2-stop', 'mutant-open-b', 'mutant-order'] if scenario == 'all' else [scenario]
    ok = True
    if scenario in ('all', 'checks'):
        ok &= check_equivalence()
    if scenario in ('all', 'verdicts'):
        ok &= verdict_cases()
    for name in names:
        if name in ('checks', 'verdicts'):
            continue
        ok &= scenario_checks(out, name)
    print('REHEARSAL', 'PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)
