"""$0 rehearsal of the judging-v13 paid gate: the provider stubbed at urllib.request.urlopen beneath the real budget transport, the real
model.openai_transport and the real stop gate. Every HTTP body must equal, byte for byte, a request built here independently from the
plan. Usage: python3 paid_rehearsal.py <scratch folder>   (runs every scenario; prints one line per check; exit 1 on any failure)."""
import io
import json
import os
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paid_gate as pg                                                  # noqa: E402
from hivemind import model                                              # noqa: E402

PLAN = json.loads((HERE / 'paid-plan.json').read_text())
BY_USER = {it['user']: it for it in PLAN}



class FakeResponse:
    def __init__(self, body):
        self.body, self.status = body, 200

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def mid(band):
    lo, hi = band
    return (lo + hi) / 2 if lo is not None and hi is not None else (lo + 10 if lo is not None else hi - 10)


def valid_answer(it, flavour='ok'):
    """A schema-valid v13 answer that passes every check: one estimate outcome per member, inside its second rung (a part below its
    whole), the reference unavailable. Flavours: 'bad-rung'; 'q3-agree' / 'q3-disagree' (each outcome rests on a company Q3 forecast;
    'q3-disagree' gives the Data Center member a different one); 'div-zero' (a ratio over a zero figure)."""
    fprops = it['schema']['properties']['figures']['items']['properties']
    aprops = it['schema']['properties']['answers']['items']['properties']
    figures, answers = [], []
    shared = (it['family'].get('shared') or [None])[0]
    for n, view_id in enumerate(it['members']):
        m = it['family']['members'][view_id]
        band = m['bands'][1]
        value = mid(band) - (5.0 * n)
        rests = []
        if flavour in ('q3-agree', 'q3-disagree', 'q3-float', 'q3-unit') and shared:
            q3 = {k: None for k in fprops}
            q3_value = 115.0 if (flavour == 'q3-disagree' and m['what']['scope'] == 'Data Center') else 110.0
            if flavour == 'q3-float' and m['what']['scope'] == 'Data Center':
                q3_value = 110.00000000000001            # [47b.1] equal within floating-point error, not bit for bit
            q3_unit = 'USD' if (flavour == 'q3-unit' and m['what']['scope'] == 'Data Center') else 'USD bn'   # [47e.2] the same number, another unit
            q3.update(id=f'q3_{view_id}', what=shared, basis='forecast', scenario='base', kind='estimate', value=q3_value, unit=q3_unit,
                      basis_text='rehearsal Q3', rests_on=[])
            figures.append(q3)
            rests = [q3['id']]
        if flavour == 'div-zero':
            z = {k: None for k in fprops}
            z.update(id='zero', what=m['what'], basis='forecast', scenario='base', kind='estimate', value=0.0, unit='USD bn', basis_text='zero', rests_on=[])
            r = {k: None for k in fprops}
            r.update(id='ratio', what=m['what'], basis='forecast', scenario='base', kind='computed', value=1.0, unit='x', operation='ratio', inputs=['zero', 'zero'])
            figures += [z, r]
        if flavour == 'dc-q4-dup' and m['what']['scope'] == 'Data Center':   # [47c.1] two equal forecasts of one quarter in one answer
            for copy in ('a', 'b'):
                d = {k: None for k in fprops}
                d.update(id=f'dcq4_{copy}', what=dict(m['what'], period='FY2027 Q4'), basis='forecast', scenario='base', kind='estimate',
                         value=50.0, unit='USD bn', basis_text='rehearsal DC Q4', rests_on=[])
                figures.append(d)
            rests = rests + ['dcq4_a', 'dcq4_b']
        if flavour in ('q3-dup-total', 'q3-dup-dc') and shared:
            if (m['what']['scope'] == 'Data Center') == (flavour == 'q3-dup-total'):
                q3 = {k: None for k in fprops}
                q3.update(id=f'q3_one_{view_id}', what=shared, basis='forecast', scenario='base', kind='estimate', value=110.0, unit='USD bn',
                          basis_text='rehearsal Q3', rests_on=[])
                figures.append(q3)
                rests = [q3['id']]
            else:
                for copy in ('a', 'b'):
                    q3 = {k: None for k in fprops}
                    q3.update(id=f'q3_two_{copy}', what=shared, basis='forecast', scenario='base', kind='estimate', value=110.0,
                              unit='USD bn', basis_text='rehearsal Q3', rests_on=[])
                    figures.append(q3)
        if flavour == 'abstain':
            ans = {k: None for k in aprops}
            ans.update(view_id=view_id, shape='unresolved', why='the shown passages give no figure for this quantity', reasons='rehearsal',
                       cites=[], pushes=[], theme_pushes=[], outcome=None, rung=None, reference=None)
            answers.append(ans)
            continue
        fig = {k: None for k in fprops}
        fig.update(id=f'o_{view_id}', what=m['what'], basis='forecast', scenario='base', kind='estimate', value=value, unit='USD bn',
                   basis_text='rehearsal estimate', rests_on=rests)
        figures.append(fig)
        ans = {k: None for k in aprops}
        ans.update(view_id=view_id, shape='forecast', outcome=fig['id'], rung=99 if flavour == 'bad-rung' else 2,
                   reference={'figure': None, 'unavailable': 'no market figure in the shown passages'}, reasons='rehearsal', cites=[],
                   pushes=[], theme_pushes=[])
        answers.append(ans)
    if flavour == 'q3-agree' and len(it['members']) == 2:   # one shared node in a joint answer
        figures = [f for f in figures if f['id'] != f'q3_{it["members"][1]}']
        figures[-1]['rests_on'] = [f'q3_{it["members"][0]}']
    return {'figures': figures, 'answers': answers}


def http_error(url, code):
    return urllib.error.HTTPError(url, code, f'HTTP {code}', {}, io.BytesIO(json.dumps({'error': {'code': code}}).encode()))


class Stub:
    def __init__(self, cfg, scenario, ledger):
        self.cfg, self.scenario, self.ledger, self.calls, self.problems, self.sent, self.sequence = cfg, scenario, ledger, {}, [], 0, []

    def expected(self, it, user):
        s = self.cfg.rejudging
        return json.dumps({'model': s.model, 'messages': [{'role': 'system', 'content': it['system']}, {'role': 'user', 'content': user}],
                           'response_format': {'type': 'json_schema', 'json_schema': {'name': 'judgement', 'strict': True, 'schema': it['schema']}},
                           'max_completion_tokens': s.max_output_tokens, 'reasoning_effort': s.reasoning_effort}).encode('utf-8')

    def __call__(self, http_request, *args, **kwargs):
        body = http_request.data
        request = json.loads(body)
        user = request['messages'][1]['content']
        base = user.split(pg.RETRY_MARK)[0]
        it = BY_USER.get(base)
        if it is None or body != self.expected(it, user):
            self.problems.append('a body that is not the planned request, byte for byte')
            raise http_error(http_request.full_url, 400)
        key = (it['unit'], it['arm'])
        self.calls[key] = self.calls.get(key, 0) + 1
        self.sent += 1
        n, s = self.calls[key], self.scenario
        retry = pg.RETRY_MARK in user
        self.sequence.append(retry)
        if s == 'ledger-stop' and self.sent == 5:
            self.ledger.stop('rehearsal: stopped after four sends')
            raise http_error(http_request.full_url, 503)
        flavour = 'ok'
        if s == 'retry' and key == ('single-O', 'single') and not retry and n == 1:
            flavour = 'bad-rung'
        if s == 'unresolved' and key == ('single-S', 'single'):      # every call refused: each draw's first answer and its retry
            flavour = 'bad-rung'
        if s in ('separate-agree', 'separate-disagree', 'separate-agree-float', 'separate-unit') and it['unit'] == 'pair-old-2':
            flavour = {'separate-agree': 'q3-agree', 'separate-disagree': 'q3-disagree', 'separate-agree-float': 'q3-float', 'separate-unit': 'q3-unit'}[s]
        if s == 'separate-within-dup' and it['unit'] == 'pair-old-2':
            flavour = 'dc-q4-dup'
        if s == 'separate-within-dup-shared' and it['unit'] == 'pair-old-2' and it['arm'].startswith('separate-'):
            flavour = 'q3-dup-total'
        if s == 'separate-within-dup-second' and it['unit'] == 'pair-old-2' and it['arm'].startswith('separate-'):
            flavour = 'q3-dup-dc'
        if s == 'abstain' and key == ('single-S', 'single'):
            flavour = 'abstain'
        if s == 'one-transport' and key == ('single-E', 'single') and n == 1:
            raise http_error(http_request.full_url, 400)
        if s == 'interrupt' and key == ('single-O', 'single'):       # stopped at single-O's second call: draw 2's first attempt
            if n == 1:
                flavour = 'bad-rung'
            else:
                raise KeyboardInterrupt('rehearsal: the launcher is stopped during a scored attempt')
        if s in ('interrupt-retry', 'retry-transport') and key == ('single-O', 'single'):
            if not retry:
                flavour = 'bad-rung'
            elif s == 'interrupt-retry':
                raise KeyboardInterrupt('rehearsal: the launcher is stopped during a diagnostic retry')
            else:
                raise http_error(http_request.full_url, 400)
        if s == 'null-content' and key == ('single-E', 'single') and n == 1:   # [47f.2] a provider refusal with no content
            return FakeResponse(json.dumps({'choices': [{'message': {'content': None, 'refusal': 'rehearsal refusal text'}}],
                                            'usage': {'prompt_tokens': len(body) // 4, 'completion_tokens': 5}}).encode('utf-8'))
        if s == 'div-zero' and key == ('single-O', 'single') and n == 1:
            flavour = 'div-zero'
        data = valid_answer(it, flavour)
        if s == 'separate-contradiction' and it['arm'].startswith('separate-v9'):   # the Data Center card alone, above the total's value
            data['figures'][-1]['value'] = 440.0
            data['answers'][0]['rung'] = 2
        if s == 'joint-retry-fix' and it['unit'] == 'pair-old-2' and not retry and (it['arm'] == 'joint' or it['arm'] == 'separate-v9'):
            data['figures'][-1]['value'] = 440.0                 # [47e.1] the Data Center card above the total, on the first attempt
        if s == 'format' and key == ('single-E', 'single') and n == 1:
            data['answers'][0].pop('reasons')
        if s == 'unicode' and key == ('single-O', 'single') and n == 1:    # [47g] other Unicode line separators inside an answer
            data['answers'][0]['reasons'] = 'first line\u2028second line\x85third line\u2029end'
        if s == 'long-raw' and key == ('single-E', 'single') and n == 1:   # [47f.2] a long malformed answer naming a passage at its end
            data['answers'][0]['why'] = 'x' * 25000 + ' see ' + sorted(it['shown'])[-1]
            data['answers'][0].pop('pushes')
        usage = {'prompt_tokens': len(body) // 4, 'completion_tokens': 800}
        return FakeResponse(json.dumps({'choices': [{'message': {'content': json.dumps(data)}}], 'usage': usage}).encode('utf-8'))


def scenario(scratch, name, ceiling=0.5, interrupted=False):
    out = scratch / name
    out.mkdir(parents=True)
    budget = pg.budget_module()
    budget.SharedLedger.init(str(out / 'ledger.json'), ceiling)
    ledger = budget.SharedLedger(str(out / 'ledger.json'))
    gate = pg.Gate(out, budget.BudgetTransport(ledger, sleep=lambda seconds: None), ledger)
    (out / 'plan.json').write_text(json.dumps(PLAN))
    stub = Stub(gate.cfg, name, ledger)
    saved = (urllib.request.urlopen, os.environ.get('OPENAI_API_KEY'))
    os.environ['OPENAI_API_KEY'] = 'rehearsal-dummy-not-a-key'
    urllib.request.urlopen = stub
    remove_gate = budget.install_stop_gate(ledger)
    summary = None
    try:
        summary = gate.run(PLAN)
    except KeyboardInterrupt:
        if not interrupted:
            raise
        summary = json.loads((out / 'results.json').read_text())   # written by the run's own finally
    finally:
        remove_gate()
        urllib.request.urlopen = saved[0]
        if saved[1] is None:
            os.environ.pop('OPENAI_API_KEY', None)
        else:
            os.environ['OPENAI_API_KEY'] = saved[1]
    lines = pg.attempt_records(out)                          # both journals: scored first attempts, then diagnostic retries
    starts = [l for l in lines if l['status'] == 'started']
    done = [l for l in lines if l['status'] != 'started']
    if len(starts) != len(done) and not interrupted:
        raise SystemExit(f'{name}: {len(starts)} started lines against {len(done)} finished attempts')
    return summary, done, stub, ledger.read()


def main(scratch):
    scratch = Path(scratch)
    checks = []

    def check(name, ok, detail=''):
        checks.append(ok)
        print(f'{"PASS" if ok else "FAIL"}  {name}  {detail}')

    s, lines, stub, led = scenario(scratch, 'clean')
    check('clean: 36 first attempts, no retry', len(lines) == 36 and all(l['attempt'] == 1 for l in lines), f'{len(lines)} attempts')
    check('clean: every body byte-equal to the planned request', not stub.problems, str(stub.problems[:1]))
    check('clean: every unit publishes', all(v['decision'] == 'publish' for v in s['finals'].values()))
    check('clean: the separate arm reconciles in all 9 pairs', all(v['decision'] == 'publish' for v in s['reconciled'].values()) and len(s['reconciled']) == 9)
    check('clean: spend settled under the ceiling', led['spent'] <= led['ceiling'] and not led.get('stopped'), f'spent {led["spent"]:.4f}')
    keydir = scratch / 'key-clean'
    pg.packets(scratch / 'clean', keydir)
    frozen = json.loads((keydir / 'packet-key.json').read_text())
    text = (scratch / 'clean' / 'packets.md').read_text()
    key = pg.render_packets(scratch / 'clean', frozen)[1]
    clean_sha = pg.hashlib.sha256(text.encode()).hexdigest()
    check('packets: 27 packets; no arm word or member prefix in the text', len(key) == 27 and 'joint' not in text and 'separate' not in text
          and not any(f'{v}.' in text for v in ('v4', 'v8', 'v14', 'v9', 'v3', 'v35')), f'{len(key)} packets')
    check('packets: the key is bound to the run, and the readers\' text commits to the key', frozen['run_digest'] == pg.run_digest(scratch / 'clean')
          and text.startswith(f'Key commitment: {pg.key_commitment(frozen)}\n') and len(frozen['salt']) == 32)
    check('packets: the scoring text holds final answers only (no attempt, code decision or check code)',
          'Attempt' not in text and 'Code decision' not in text and 'published' not in text and not any(f'(C{n}' in text for n in range(1, 11)))
    try:
        pg.packets(scratch / 'clean', keydir)
        again = ''
    except SystemExit as error:
        again = str(error)
    check('packets: a second packets run is refused, the key unchanged', 'frozen' in again
          and json.loads((keydir / 'packet-key.json').read_text()) == frozen, again[:80])
    yes = lambda a='yes': {'answer': a, 'ground': 'F1 rehearsal'}

    def card(usable='yes', gap='no', drop=None, b_differs=None, third=None):
        def one():
            r = {'usable': yes(usable), 'contradiction': yes('no'), 'internal_reference': yes('no'), 'deciding_gap': yes(gap)}
            if drop:
                r[drop] = {'answer': 'no', 'ground': ''}
            return r
        a, b = one(), one()
        if b_differs:
            b[b_differs] = yes('no' if a[b_differs]['answer'] == 'yes' else 'yes')
        out = {'A': a, 'B': b}
        if third:
            out['third'] = third
        return out

    def readings(good_separate, defect_arm=None, drop_packet=False, bad_card=False, missing_ground=False, disagree=None, null_ground=False,
                 foreign_ground=False):
        rd, seen_sep, defect_done = {}, 0, False
        for pid, k in sorted(key.items()):
            usable = 'yes'
            if k['arm'] == 'separate':
                seen_sep += 1
                usable = 'yes' if seen_sep <= good_separate else 'no'
            rd[pid] = {c: card(usable) for c in k['cards']}
            if defect_arm and k['arm'] == defect_arm and not defect_done:
                rd[pid]['K1'] = card(usable, gap='yes')
                defect_done = True
        first = sorted(rd)[0]
        if drop_packet:
            rd.pop(first)
        if bad_card:
            rd[first]['v999'] = rd[first].pop(sorted(rd[first])[0])
        if missing_ground:
            rd[first][sorted(rd[first])[0]] = card(drop='usable')
        if disagree is not None:
            rd[first][sorted(rd[first])[0]] = card(b_differs='usable', third=disagree)
        if null_ground:
            rd[first][sorted(rd[first])[0]]['A']['usable'] = {'answer': 'yes', 'ground': None}
        if foreign_ground:
            rd[first][sorted(rd[first])[0]]['A']['usable'] = {'answer': 'yes', 'ground': 'the passage about the total'}
        return rd

    def verdict_of(rd, name, out=None, keys=None, packets_sha=None):
        copy = scratch / f'verdict-{name}'                   # [47e.4] a run takes one verdict: each case reads its own copy of the run
        shutil.copytree(out or scratch / 'clean', copy, ignore=shutil.ignore_patterns('archives', 'readings.json', 'verdict.json'))
        path = scratch / f'readings-{name}.json'
        path.write_text(json.dumps({'packets_sha256': packets_sha or clean_sha, 'packets': rd}))
        return pg.verdict(copy, str(path), keys or keydir)
    v = verdict_of(readings(9), 'all-good')
    check('verdict: both arms usable everywhere: STOP (gain under 3)', v['verdict'] == 'STOP' and v['joint usable pairs'] == 9 and v['separate usable pairs'] == 9)
    try:
        pg.verdict(scratch / 'verdict-all-good', str(scratch / 'readings-all-good.json'), keydir)
        second = ''
    except SystemExit as error:
        second = str(error)
    sealed = scratch / 'verdict-all-good'
    replayed = pg.replay(sealed, keydir)
    (sealed / 'readings.json').write_text((sealed / 'readings.json').read_text().replace('"no"', '"yes"', 1))
    check('verdict: a run takes one verdict; replay reproduces it from the sealed readings, and fails once they are edited',
          'refused' in second and replayed and not pg.replay(sealed, keydir), second[:80])
    v = verdict_of(readings(5), 'gain-4')
    check('verdict: joint 9, separate 5: PASS', v['verdict'] == 'PASS', str(v['separate usable pairs']))
    v = verdict_of(readings(5, defect_arm='single'), 'single-defect')
    check('verdict: one published singleton defect: STOP', v['verdict'] == 'STOP' and len(v['published defects']) == 1)
    v = verdict_of(readings(5, defect_arm='separate'), 'separate-defect')
    check('verdict: a defect in the separate arm alone does not stop', v['verdict'] == 'PASS')
    for name, kw in (('missing packet', {'drop_packet': True}), ('invented card', {'bad_card': True}), ('missing ground', {'missing_ground': True}),
                     ('disagreement, no third', {'disagree': None, 'drop_packet': False})):
        rd = readings(5, **kw) if name != 'disagreement, no third' else readings(5, disagree={})
        v = verdict_of(rd, name.replace(' ', '-').replace(',', ''))
        check(f'verdict: {name}: INCOMPLETE', v['verdict'] == 'INCOMPLETE', '; '.join(v['problems'][:1]))
    v = verdict_of(readings(5, disagree={'usable': yes('yes')}), 'third-decides')
    check('verdict: a disagreement decided by the third reader is complete', v['complete'], '; '.join(v['problems'][:1]))
    for name, kw in (('null ground', {'null_ground': True}), ('ground naming nothing in the packet', {'foreign_ground': True})):
        v = verdict_of(readings(5, **kw), name.replace(' ', '-'))
        check(f'verdict: {name}: INCOMPLETE', v['verdict'] == 'INCOMPLETE', '; '.join(v['problems'][:1]))
    v = verdict_of(readings(5), 'other-packets', packets_sha='0' * 64)
    check('verdict: readings made on other packets: INCOMPLETE', v['verdict'] == 'INCOMPLETE', '; '.join(v['problems'][:1]))
    shutil.copytree(scratch / 'clean', scratch / 'clean-changed')
    changed = json.loads((scratch / 'clean-changed' / 'results.json').read_text())
    changed['finals']['single-O|single|1']['decision'] = 'held'
    (scratch / 'clean-changed' / 'results.json').write_text(json.dumps(changed))
    v = verdict_of(readings(5), 'changed-run', out=scratch / 'clean-changed')
    check('verdict: a run changed after the packets were frozen: INCOMPLETE', v['verdict'] == 'INCOMPLETE' and any('does not belong' in x for x in v['problems']),
          '; '.join(v['problems'][:1]))

    # [47b.3] one card's view: its own figures renumbered, its assumption records mapped to the same numbers, others left out
    calc = {'figures': [{'id': 'v14.q4f', 'kind': 'source', 'evidence': 'e7', 'rests_on': []},
                        {'id': 'v14.dc', 'kind': 'computed', 'inputs': ['v14.q4f', 'v14.q4f'], 'rests_on': []},
                        {'id': 'v9.other', 'kind': 'source', 'evidence': 'e8', 'rests_on': []}],
            'answers': [{'view_id': 'v14', 'outcome': 'v14.dc', 'reference': {'figure': None}, 'cites': ['e7']}]}
    norm, mapped, named = pg.card_view(calc, 'v14', [{'type': 'overlap', 'figure': 'v14.q4f', 'outcome': 'v14'},
                                                     {'type': 'bridge', 'figure': 'v9.other', 'bridge': 'v9.other', 'alternate': 'undetermined'}])
    blob = json.dumps([norm, mapped])
    check('card view: own figures only, renumbered; the assumption record mapped, the other card\'s left out',
          [f['id'] for f in norm['figures']] == ['F1', 'F2'] and mapped == [{'type': 'overlap', 'figure': 'F1', 'outcome': 'v14'}]
          and 'v14.' not in blob and 'v9' not in blob and named == ['e7'], blob[:160])

    s, lines, stub, led = scenario(scratch, 'separate-agree')
    rec = s['reconciled']['pair-old-2|1']
    check('separate-agree: equal shared Q3 forecasts are unified, and the pair reconciles', rec['decision'] == 'publish', str(rec.get('errors'))[:120])
    s, lines, stub, led = scenario(scratch, 'separate-disagree')
    rec = s['reconciled']['pair-old-2|1']
    check('separate-disagree: different shared Q3 forecasts are refused (C4)', rec['decision'] == 'refused' and any(c == 'C4' for c, _ in rec['errors']))
    s, lines, stub, led = scenario(scratch, 'div-zero')
    o = [l for l in lines if l['unit'] == 'single-O' and l['draw'] == 1]
    check('div-zero: recorded and refused (C2), then retried', [l['decision'] for l in o] == ['refused', 'publish']
          and any(c == 'C2' for c, _ in o[0]['errors']), str([l['decision'] for l in o]))
    s, lines, stub, led = scenario(scratch, 'reservation', ceiling=0.0001)
    check('reservation: a refused reservation never reaches the provider and is recorded', stub.sent == 0 and all(
        l['decision'] == 'transport' for l in lines) and len(lines) > 0, f'{stub.sent} provider calls')
    saved = (pg.APPROVED_CEILING, pg.AUTH)
    try:
        pg.APPROVED_CEILING, pg.AUTH = None, scratch / 'auth' / 'authorization.json'
        for name, setup, expect in (('no ceiling named', lambda: None, 'approved ceiling'),
                                    ('a changed plan', lambda: setattr(pg, 'APPROVED_CEILING', 0.5), 'not the reviewed one'),
                                    ('a used authorization', lambda: (pg.AUTH.parent.mkdir(parents=True, exist_ok=True), pg.AUTH.write_text('{}')), 'already used')):
            setup()
            plan_path = scratch / 'changed-plan.json' if name == 'a changed plan' else HERE / 'paid-plan.json'
            if name == 'a changed plan':
                plan_path.write_text((HERE / 'paid-plan.json').read_text() + ' ')
            try:
                pg.send(scratch / f'send-{name.replace(" ", "-")}', 0.5, str(plan_path))
                refused = ''
            except SystemExit as error:
                refused = str(error)
            check(f'send refuses {name}', expect in refused and not (scratch / f'send-{name.replace(" ", "-")}').exists(), refused[:80])
    finally:
        pg.APPROVED_CEILING, pg.AUTH = saved

    s, lines, stub, led = scenario(scratch, 'retry')
    o = [l for l in lines if l['unit'] == 'single-O' and l['draw'] == 1]
    check('retry: a refused calculation is retried once with its errors and then publishes', [l['decision'] for l in o] == ['refused', 'publish'], str([l['decision'] for l in o]))
    s, lines, stub, led = scenario(scratch, 'unresolved')
    check('unresolved: two refusals make the unit unresolved', s['finals']['single-S|single|1']['decision'] == 'unresolved')
    s, lines, stub, led = scenario(scratch, 'format')
    e = [l for l in lines if l['unit'] == 'single-E' and l['draw'] == 1]
    check('format: a schema-invalid answer is refused, then retried', [l['status'] for l in e] == ['format invalid', 'answered'], str([l['status'] for l in e]))
    fk = scratch / 'key-format'
    pg.packets(scratch / 'format', fk)
    fmt = pg.render_packets(scratch / 'format', json.loads((fk / 'packet-key.json').read_text()))[1]
    fpid = next(p for p, k in fmt.items() if k['unit'] == 'single-E' and k['draw'] == '1')
    fsection = (scratch / 'format' / 'packets.md').read_text().split(f'## {fpid}\n')[1].split('\n## ')[0]
    ftext = (scratch / 'format' / 'attempts.md').read_text()
    check('format: the scoring packet carries the neutral label; the returned text is in the unscored attempts file (with the retry)',
          pg.FORMAT_INVALID in fsection and 'The text returned' in ftext and '"view_id": "v41"' in ftext and ftext.count('## D') == 2, fpid)
    s, lines, stub, led = scenario(scratch, 'separate-contradiction')
    rec = s['reconciled']['pair-old-2|1']
    check('separate: two answers that each pass alone are refused when reconciled (C3)', rec['decision'] == 'refused' and any(c == 'C3' for c, _ in rec['errors']),
          rec['decision'])
    s, lines, stub, led = scenario(scratch, 'ledger-stop')
    not_sent = [k for k, v in s['finals'].items() if str(v.get('decision', '')).startswith('not sent')]
    check('ledger-stop: after the ledger stops, nothing more is sent', led.get('stopped') and len(lines) == 5 and len(not_sent) >= 30, f'{len(lines)} attempts, {len(not_sent)} not sent')
    s, lines, stub, led = scenario(scratch, 'separate-agree-float')
    rec = s['reconciled']['pair-old-2|1']
    check('separate-agree-float: Q3 forecasts equal within floating-point error are unified, and the pair reconciles',
          rec['decision'] == 'publish' and len(rec['calc']['unified']) == 1, str(rec.get('errors'))[:120])
    fkeys = scratch / 'key-float'
    pg.packets(scratch / 'separate-agree-float', fkeys)
    fkey = pg.render_packets(scratch / 'separate-agree-float', json.loads((fkeys / 'packet-key.json').read_text()))[1]
    pid = next(p for p, k in fkey.items() if k['unit'] == 'pair-old-2' and k['arm'] == 'separate' and k['draw'] == '1')
    section = (scratch / 'separate-agree-float' / 'packets.md').read_text().split(f'## {pid}\n')[1].split('\n## ')[0]
    check('packets: a reconciled card is shown with its own original derivation, not the unified copy',
          '110.00000000000001' in section and section.count('rehearsal Q3') == 2, pid)

    rkeys = scratch / 'key-retry'                            # the 'retry' scenario above: single-O's first answer refused, the retry published
    pg.packets(scratch / 'retry', rkeys)
    rfrozen = json.loads((rkeys / 'packet-key.json').read_text())
    rkey = pg.render_packets(scratch / 'retry', rfrozen)[1]
    pid = next(p for p, k in rkey.items() if k['unit'] == 'single-O' and k['draw'] == '1')
    section = (scratch / 'retry' / 'packets.md').read_text().split(f'## {pid}\n')[1].split('\n## ')[0]
    attempts_text = (scratch / 'retry' / 'attempts.md').read_text()
    check('packets: the scoring packet shows the first answer (scored); the retry is only in the unscored attempts file, unlinked',
          '"rung": 99' in section and '"rung": 2' not in section and rkey[pid]['decision'] == 'refused' and len(rfrozen['attempts']) == 1
          and '"rung": 2' in attempts_text and 'T.F1' in attempts_text and '## P' not in attempts_text and 'D01' in attempts_text, pid)

    s, lines, stub, led = scenario(scratch, 'one-transport')
    check('one-transport: a request that fails in transport is final as transport, not published', s['finals']['single-E|single|1']['decision'] == 'transport')
    tkeys = scratch / 'key-transport'
    pg.packets(scratch / 'one-transport', tkeys)
    tfrozen = json.loads((tkeys / 'packet-key.json').read_text())
    rd = {pid: {c: card() for c in k['cards']} for pid, k in pg.render_packets(scratch / 'one-transport', tfrozen)[1].items()}
    v = verdict_of(rd, 'transport', out=scratch / 'one-transport', keys=tkeys, packets_sha=pg.hashlib.sha256((scratch / 'one-transport' / 'packets.md').read_bytes()).hexdigest())
    check('verdict: a unit failed in transport makes the verdict INCOMPLETE', v['verdict'] == 'INCOMPLETE'
          and any('single-E|single|1: transport' in x for x in v['problems']), '; '.join(v['problems'][:2]))


    def read_all(folder, keys):
        pg.packets(scratch / folder, keys)
        kf = json.loads((keys / 'packet-key.json').read_text())
        rend = pg.render_packets(scratch / folder, kf)[1]
        rd = {pid: {c: card() for c in k['cards']} for pid, k in rend.items()}
        return verdict_of(rd, folder, out=scratch / folder, keys=keys,
                          packets_sha=pg.hashlib.sha256((scratch / folder / 'packets.md').read_bytes()).hexdigest())

    s, lines, stub, led = scenario(scratch, 'interrupt', interrupted=True)
    f = s['finals']
    v = read_all('interrupt', scratch / 'key-interrupt')
    check('interrupt during a scored attempt: results written; that attempt interrupted, later ones not sent, no retry yet; INCOMPLETE',
          (scratch / 'interrupt' / 'results.json').exists() and f['single-O|single|2']['decision'] == 'interrupted'
          and f['single-S|single|2']['decision'] == 'not sent' and f['single-O|single|1']['decision'] == 'retry not sent'
          and f['pair-old-1|joint|1']['decision'] == 'publish' and v['verdict'] == 'INCOMPLETE', '; '.join(v['problems'][:2]))
    s, lines, stub, led = scenario(scratch, 'interrupt-retry', interrupted=True)
    f = s['finals']
    v = read_all('interrupt-retry', scratch / 'key-interrupt-retry')
    firsts = [l for l in lines if l['attempt'] == 1]
    check('interrupt during a diagnostic retry: all 36 scored attempts are recorded and the verdict is complete',
          len(firsts) == 36 and f['single-O|single|1']['decision'] == 'interrupted' and pg.first_attempt(f['single-O|single|1'])['decision'] == 'refused'
          and v['complete'], '; '.join(v['problems'][:2]))
    s, lines, stub, led = scenario(scratch, 'retry-transport')
    v = read_all('retry-transport', scratch / 'key-retry-transport')
    check('a diagnostic retry that fails in transport leaves the scored test complete', s['finals']['single-O|single|1']['decision'] == 'transport'
          and v['complete'], '; '.join(v['problems'][:2]))
    check('every scored first attempt is sent before any retry (the provider\'s own call order)', True in stub.sequence
          and stub.sequence.index(True) == stub.sequence.count(False) == 36, str(stub.sequence.index(True) if True in stub.sequence else None))
    s, lines, stub, led = scenario(scratch, 'null-content')
    v = read_all('null-content', scratch / 'key-null-content')
    check('a provider refusal with null content: packets are made, and its text is in the attempts file',
          '(the model refused: rehearsal refusal text)' in (scratch / 'null-content' / 'attempts.md').read_text(), v['verdict'])
    s, lines, stub, led = scenario(scratch, 'long-raw')
    read_all('long-raw', scratch / 'key-long-raw')
    single_e = next(i for i in PLAN if i['unit'] == 'single-E')
    named = sorted(single_e['shown'])[-1]
    check('a long malformed answer is kept whole: the passage it names at its end is shown in the attempts file',
          single_e['shown'][named] in (scratch / 'long-raw' / 'attempts.md').read_text(), named)
    atomic = scratch / 'atomic'
    shutil.copytree(scratch / 'clean', atomic, ignore=shutil.ignore_patterns('archives', 'packets.md', 'attempts.md'))
    saved_render = pg.render_attempts
    pg.render_attempts = lambda *a, **k: (_ for _ in ()).throw(RuntimeError('rehearsal: rendering fails'))
    try:
        pg.packets(atomic, scratch / 'key-atomic')
    except RuntimeError:
        pass
    finally:
        pg.render_attempts = saved_render
    nothing = not (atomic / 'packets.md').exists() and not (atomic / 'attempts.md').exists() and not (scratch / 'key-atomic').exists()
    try:
        pg.packets(atomic, scratch / 'key-atomic')
        again = ''
    except SystemExit as error:
        again = str(error)
    check('packets are written only after both files render: a failed render leaves nothing, and a second call then succeeds',
          nothing and not again and (atomic / 'packets.md').exists() and (scratch / 'key-atomic' / 'packet-key.json').exists(), again[:80])
    # [47c.1] duplicates inside one answer are judged in both arms alike: never unified by the reconciliation
    s, lines, stub, led = scenario(scratch, 'separate-within-dup')
    rec, joint = s['reconciled']['pair-old-2|1'], s['finals']['pair-old-2|joint|1']
    check('separate-within-dup: two equal forecasts inside one answer are kept, so the reconciled pair is refused as the joint one is (C3)',
          rec['decision'] == 'refused' and any(c == 'C3' and 'ambiguous' in m for c, m in rec['errors']) and joint['decision'] == 'unresolved'
          and not rec['calc']['unified'], f"{rec['decision']} / joint {joint['decision']}")
    s, lines, stub, led = scenario(scratch, 'separate-within-dup-shared')
    rec = s['reconciled']['pair-old-2|1']
    check('separate-within-dup-shared: two equal shared forecasts within one call are not unified with each other, so C4 refuses as within one call',
          rec['decision'] == 'refused' and any(c == 'C4' and 'forecast nodes' in m for c, m in rec['errors']) and not rec['calc']['unified'],
          f"{rec['decision']} {[m for c, m in rec.get('errors', []) if c == 'C4'][:1]}")
    s, lines, stub, led = scenario(scratch, 'separate-within-dup-second')
    rec = s['reconciled']['pair-old-2|1']
    check('separate-within-dup-second: the second call\'s two equal shared forecasts are not both unified to the first call\'s one (C4 refuses)',
          rec['decision'] == 'refused' and any(c == 'C4' and '3 forecast nodes' in m for c, m in rec['errors']) and not rec['calc']['unified'],
          f"{rec['decision']} {[m for c, m in rec.get('errors', []) if c == 'C4'][:1]}")
    # [47c.3] an abstention can be read: its card is a ground
    s, lines, stub, led = scenario(scratch, 'abstain')
    akeys = scratch / 'key-abstain'
    pg.packets(scratch / 'abstain', akeys)
    afrozen = json.loads((akeys / 'packet-key.json').read_text())
    arend = pg.render_packets(scratch / 'abstain', afrozen)[1]
    apid = next(p for p, k in arend.items() if k['unit'] == 'single-S' and k['draw'] == '1')
    rd = {pid: {c: card() for c in k['cards']} for pid, k in arend.items()}
    for pid, k in arend.items():                            # every draw of single-S abstains
        if k['unit'] == 'single-S':
            rd[pid] = {'K1': {x: {q: {'answer': 'no', 'ground': 'K1 is unresolved: no figure in the shown passages'} for q in pg.QUESTIONS} for x in ('A', 'B')}}
    v = verdict_of(rd, 'abstain', out=scratch / 'abstain', keys=akeys, packets_sha=pg.hashlib.sha256((scratch / 'abstain' / 'packets.md').read_bytes()).hexdigest())
    check('abstain: an unresolved singleton is published and can be read with its card as the ground', s['finals']['single-S|single|1']['decision'] == 'publish'
          and arend[apid]['grounds'] == ['K1'] and v['complete'], '; '.join(v['problems'][:1]))
    # [47c.2, 47d.1] the key orders the packets, and the readers' text commits to it: a swap of two packets whose text is identical
    swapped = json.loads(json.dumps(frozen))   # (two draws of one unit and arm answer alike in the rehearsal) is still caught
    twin = next(n for n, (_, u) in enumerate(swapped['order']) if n and u[:2] == swapped['order'][0][1][:2])
    swapped['order'][0][1], swapped['order'][twin][1] = swapped['order'][twin][1], swapped['order'][0][1]
    (scratch / 'key-swapped').mkdir()
    (scratch / 'key-swapped' / 'packet-key.json').write_text(json.dumps(swapped))
    same_text = pg.render_packets(scratch / 'clean', swapped)[0].split('\n', 1)[1] == text.split('\n', 1)[1]
    v = verdict_of(readings(5), 'swapped', keys=scratch / 'key-swapped')
    check('verdict: a swap of two packets with identical text: INCOMPLETE (the key is not the committed one)', same_text and v['verdict'] == 'INCOMPLETE'
          and any('committed to' in x for x in v['problems']), '; '.join(v['problems'][:1]))
    claimed = dict(frozen, packets={pid: {'decision': 'held'} for pid, _ in frozen['order']})
    (scratch / 'key-claimed').mkdir()
    (scratch / 'key-claimed' / 'packet-key.json').write_text(json.dumps(claimed))
    forged = verdict_of(readings(5, defect_arm='single'), 'claimed', keys=scratch / 'key-claimed')
    check('verdict: decisions written into the key: INCOMPLETE (the key is not the committed one)', forged['verdict'] == 'INCOMPLETE'
          and any('committed to' in x for x in forged['problems']), forged['verdict'])
    # [47c.4] a torn journal entry: the committed entries are kept, the torn attempt is unfinished, the run incomplete, nothing sent
    shutil.copytree(scratch / 'clean', scratch / 'torn', ignore=shutil.ignore_patterns('packets.md', 'attempts.md', 'results.json'))
    journal = (scratch / 'torn' / 'answers.jsonl').read_text().split('\n')[:-1]
    last = json.loads(journal[-1])
    (scratch / 'torn' / 'answers.jsonl').write_text('\n'.join(journal[:-1] + [journal[-1][:len(journal[-1]) // 2]]) + '\n')
    saved_open = urllib.request.urlopen
    urllib.request.urlopen = lambda *a, **k: (_ for _ in ()).throw(AssertionError('recover sent a request'))
    try:
        rs = pg.recover(scratch / 'torn')
    finally:
        urllib.request.urlopen = saved_open
    torn_key = f"{last['unit']}|{last['arm']}|{last['draw']}"
    check('torn journal: recover keeps the committed entries, marks the torn attempt interrupted and the line damaged, sends nothing',
          len(rs['damaged']) == 1 and rs['finals'][torn_key]['decision'] == 'interrupted'
          and sum(v['decision'] == 'publish' for v in rs['finals'].values()) == 35, f"{torn_key}: {rs['finals'][torn_key]['decision']}")
    tk = scratch / 'key-torn'
    pg.packets(scratch / 'torn', tk)
    tf = json.loads((tk / 'packet-key.json').read_text())
    trend = pg.render_packets(scratch / 'torn', tf)[1]
    rd = {pid: {c: card() for c in k['cards']} for pid, k in trend.items()}
    v = verdict_of(rd, 'torn', out=scratch / 'torn', keys=tk, packets_sha=pg.hashlib.sha256((scratch / 'torn' / 'packets.md').read_bytes()).hexdigest())
    tpid = next(p for p, k in trend.items() if (k['unit'], k['arm'], k['draw']) == (last['unit'], last['arm'], str(last['draw'])))
    tsection = (scratch / 'torn' / 'packets.md').read_text().split(f'## {tpid}\n')[1].split('\n## ')[0]
    check('torn journal: the interrupted card\'s packet says the request was started and no answer recorded',
          'The request was started; no answer was recorded.' in tsection and rs['finals'][torn_key]['attempts'][-1]['status'] == 'interrupted', tpid)
    check('verdict: a damaged journal line makes the verdict INCOMPLETE', v['verdict'] == 'INCOMPLETE' and any('damaged' in x for x in v['problems']),
          '; '.join(v['problems'][:1]))
    # [47e.1] the first attempt is scored on both arms: a joint retry that repairs a cross-card conflict does not count
    s, lines, stub, led = scenario(scratch, 'joint-retry-fix')
    jk = scratch / 'key-joint-retry'
    pg.packets(scratch / 'joint-retry-fix', jk)
    jfrozen = json.loads((jk / 'packet-key.json').read_text())
    jrend = pg.render_packets(scratch / 'joint-retry-fix', jfrozen)[1]
    jpid = next(p for p, k in jrend.items() if (k['unit'], k['arm'], k['draw']) == ('pair-old-2', 'joint', '1'))
    rd = {pid: {c: card() for c in k['cards']} for pid, k in jrend.items()}
    v = verdict_of(rd, 'joint-retry', out=scratch / 'joint-retry-fix', keys=jk,
                   packets_sha=pg.hashlib.sha256((scratch / 'joint-retry-fix' / 'packets.md').read_bytes()).hexdigest())
    check('joint-retry-fix: the joint pair is final-published after its retry but scored on its refused first attempt, like the separate pair',
          s['finals']['pair-old-2|joint|1']['decision'] == 'publish' and jrend[jpid]['decision'] == 'refused'
          and s['reconciled']['pair-old-2|1']['decision'] == 'refused' and v['joint usable pairs'] == 6 and v['separate usable pairs'] == 6,   # all 3 draws of old-2
          f"joint {v['joint usable pairs']}, separate {v['separate usable pairs']}")
    s, lines, stub, led = scenario(scratch, 'separate-unit')
    rec = s['reconciled']['pair-old-2|1']
    check('separate-unit: the same number in another unit is not unified (C4 refuses)', rec['decision'] == 'refused'
          and any(c == 'C4' and 'forecast nodes' in m for c, m in rec['errors']) and not rec['calc']['unified'], rec['decision'])
    # [47g] a damaged retry record stays diagnostic; Unicode separators inside an answer are not record breaks
    shutil.copytree(scratch / 'retry', scratch / 'torn-retry', ignore=shutil.ignore_patterns('archives', 'packets.md', 'attempts.md', 'results.json'))
    rpath = scratch / 'torn-retry' / 'retries.jsonl'
    if not rpath.exists():
        check('a damaged retry record is reported and the retry is interrupted, but the scored test stays complete', False, 'no retries journal')
    else:
        rj = rpath.read_text().split('\n')[:-1]
        rpath.write_text('\n'.join(rj[:-1] + [rj[-1][:len(rj[-1]) // 2]]) + '\n')
        rs = pg.recover(scratch / 'torn-retry')
        v = read_all('torn-retry', scratch / 'key-torn-retry')
        check('a damaged retry record is reported and the retry is interrupted, but the scored test stays complete',
              [d['journal'] for d in rs['damaged']] == ['retries.jsonl'] and rs['finals']['single-O|single|1']['decision'] == 'interrupted'
              and v['complete'], '; '.join(v['problems'][:2]))
    s, lines, stub, led = scenario(scratch, 'unicode')
    v = read_all('unicode', scratch / 'key-unicode')
    check('Unicode line separators inside an answer are kept in one record: the unit publishes and the verdict is complete',
          '\u2028' in (scratch / 'unicode' / 'answers.jsonl').read_text() and not s['damaged']
          and s['finals']['single-O|single|1']['decision'] == 'publish' and v['complete'], '; '.join(v['problems'][:2]))
    synthetic = scratch / 'retry-not-sent'
    synthetic.mkdir()
    base = {'unit': 'single-O', 'arm': 'single', 'draw': 1, 'attempt': 1}
    (synthetic / 'answers.jsonl').write_text(json.dumps(dict(base, status='started')) + '\n'
                                             + json.dumps(dict(base, status='answered', decision='refused', errors=[['C6', 'x']])) + '\n')
    finals = pg.derive_finals(synthetic, [i for i in PLAN if i['unit'] == 'single-O'])
    check('a refused first answer whose retry was never sent is incomplete, not refused or not sent',
          finals['single-O|single|1']['decision'] == 'retry not sent' and finals['single-O|single|2']['decision'] == 'not sent')
    print(f'{sum(checks)} of {len(checks)} checks pass')
    return 0 if all(checks) else 1


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1].startswith('-'):
        raise SystemExit('usage: paid_rehearsal.py <scratch folder>')
    raise SystemExit(main(sys.argv[1]))
