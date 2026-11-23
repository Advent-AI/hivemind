"""A4, the v13s end-to-end rehearsal (SMALL-DESIGN.md §5 [52]): the provider stubbed at urllib beneath the real budget transport, a v13s
plan built in memory, and each answer taken through the first attempt, the separate arm's reconciliation, the reader's card and recovery.
It also replays the old (v13) run from its journals with the ledger snapshot saved inside its results.json, which must reproduce byte
for byte. $0. Usage: python3 small_rehearsal.py <scratch folder>"""
import io
import json
import os
import shutil
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / 'src'))
import calc_small as cs  # noqa: E402
import paid_gate as pg  # noqa: E402

PLAN = pg.build_plan('v13s')
BY_USER = {it['user']: it for it in PLAN}
OLD_RUN = REPO / 'poc/data/judging-v13-paid-gate-2026-11-22'


class FakeResponse:
    def __init__(self, body):
        self.body, self.status = body, 200

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def blank():
    return {k: None for k in ('id', 'what', 'kind', 'basis', 'value', 'low', 'high', 'unit', 'evidence_id', 'quote_number', 'qualifier',
                              'inputs', 'operation', 'basis_text', 'rests_on')}


def answer(it, flavour):
    """A schema-valid v13s answer: one estimate outcome per member inside its second rung (the part below its whole), each resting on the
    family's one company Q3 forecast when the family has one, the reference unavailable. Flavours: 'ok'; 'dc-high' (the Data Center
    outcome above the total's highest value); 'two-q3' (a second company Q3 forecast); 'bad-rung'."""
    figures, answers = [], []
    shared = (it['family'].get('shared') or [None])[0]
    if shared:
        q3 = blank()
        q3.update(id='Q3', what=shared, kind='estimate', basis='forecast', value=110.0, unit='USD bn', basis_text='rehearsal Q3',
                  rests_on=[], outcome_for=[], reference_for=[])
        figures.append(q3)
        if flavour == 'two-q3':
            q3b = dict(q3, id='Q3b', value=112.0)
            figures.append(q3b)
    for n, view_id in enumerate(it['members']):
        m = it['family']['members'][view_id]
        lo, hi = m['bands'][1]
        value = ((lo + hi) / 2 if lo is not None and hi is not None else (lo or hi)) - 5.0 * n
        if flavour == 'dc-high' and m['what']['scope'] == 'Data Center':
            value = 440.0
        f = blank()
        f.update(id=f'O{n}', what=m['what'], kind='estimate', basis='forecast', value=value, unit='USD bn', basis_text='rehearsal estimate',
                 rests_on=(['Q3b'] if flavour == 'two-q3' and m['what']['scope'] == 'Data Center' else ['Q3']) if shared else [],
                 outcome_for=[view_id], reference_for=[])
        figures.append(f)
        rung = 99 if flavour == 'bad-rung' else next(k for k, (b_lo, b_hi) in enumerate(m['bands'], 1)
                                                      if (b_lo is None or value >= b_lo) and (b_hi is None or value < b_hi))
        answers.append({'view_id': view_id, 'shape': 'forecast', 'rung': rung, 'reference_unavailable': 'no market figure shown',
                        'reasons': 'rehearsal', 'why': None, 'cites': [], 'pushes': [], 'theme_pushes': []})
    if flavour in ('src-ok', 'src-misread'):                 # a real money expression from the request's own passages
        pid, (s0, e0) = next((p, sp) for p, sp in ((p, sp) for p in sorted(it['passages']) for sp in cs.expressions(it['passages'][p]['text']))
                             if (cs.parse_number(it['passages'][pid_text(it, p)]['text'][sp[0]:sp[1]]) or {}).get('unit') == 'USD bn'
                             and 'value' in cs.parse_number(it['passages'][p]['text'][sp[0]:sp[1]]))
        qn = it['passages'][pid]['text'][s0:e0]
        text_before = it['passages'][pid]['text'][:s0]
        qual = next((w for w in cs.QUALIFIERS_BEFORE if text_before.lower().rstrip().endswith(w)), 'none')
        src = blank()
        src.update(id='SRC', what=dict(it['family']['members'][it['members'][0]]['what'], measure='a quoted amount'), kind='source',
                   basis='reported', value=cs.parse_number(qn)['value'] * (1.1 if flavour == 'src-misread' else 1.0), unit='USD bn',
                   evidence_id=pid, quote_number=qn, qualifier=qual)
        figures.append(src)
    if flavour == 'arith':
        add = blank()
        add.update(id='ADD', what=dict(it['family']['members'][it['members'][0]]['what'], measure='two estimates'), kind='computed',
                   basis='forecast', value=999.0, unit='USD bn', inputs=['O0', 'O0'], operation='sum')
        figures.append(add)
    if flavour == 'ref-est':
        ref = blank()
        ref.update(id='REF', what=it['family']['members'][it['members'][0]]['what'], kind='estimate', basis='consensus', value=100.0,
                   unit='USD bn', basis_text='looks like the market', rests_on=[], reference_for=[it['members'][0]])
        figures.append(ref)
        answers[0]['reference_unavailable'] = None
    if flavour == 'dc-into-total':
        both = blank()
        total, dc = figures[-2], figures[-1]
        both.update(id='BOTH', what=dict(total['what'], measure='revenue, both'), kind='computed', basis='forecast',
                    value=total['value'] + dc['value'], unit='USD bn', inputs=[total['id'], dc['id']], operation='sum')
        figures.append(both)
    for f in figures:
        f.setdefault('outcome_for', [])
        f.setdefault('reference_for', [])
    return {'figures': figures, 'answers': answers}


def pid_text(it, p):
    return p


class Stub:
    def __init__(self, cfg, scenario):
        self.cfg, self.scenario, self.problems, self.sent, self.draws = cfg, scenario, [], 0, {}

    def expected(self, it, user):
        s = self.cfg.rejudging
        return json.dumps({'model': s.model, 'messages': [{'role': 'system', 'content': it['system']}, {'role': 'user', 'content': user}],
                           'response_format': {'type': 'json_schema', 'json_schema': {'name': 'judgement', 'strict': True, 'schema': it['schema']}},
                           'max_completion_tokens': s.max_output_tokens, 'reasoning_effort': s.reasoning_effort}).encode('utf-8')

    def __call__(self, http_request, *args, **kwargs):
        body = http_request.data
        user = json.loads(body)['messages'][1]['content']
        retry = pg.RETRY_MARK in user
        it = BY_USER.get(user.split(pg.RETRY_MARK)[0])
        if it is None or body != self.expected(it, user):
            self.problems.append('a body that is not the planned request, byte for byte')
            raise urllib.error.HTTPError(http_request.full_url, 400, 'bad', {}, io.BytesIO(b'{}'))
        self.sent += 1
        flavour = 'ok'
        if self.scenario == 'separate-contradiction' and it['arm'] == 'separate-v9':
            flavour = 'dc-high'
        if self.scenario == 'joint-defects' and it['unit'] == 'pair-old-2' and it['arm'] == 'joint' and not retry:
            flavour = 'two-q3'
        if self.scenario == 'joint-defects' and it['unit'] == 'single-E' and not retry:
            flavour = 'bad-rung'
        if self.scenario == 'named-defects' and not retry:          # [54] a defective and a correct answer for each named defect
            draw = self.draws.setdefault(key := (it['unit'], it['arm']), 0) + 1
            self.draws[key] = draw
            flavour = {('single-O', 1): 'src-misread', ('single-O', 2): 'src-ok', ('single-O', 3): 'arith',
                       ('single-S', 1): 'ref-est', ('pair-old-1', 1): 'dc-into-total'}.get((it['unit'], draw), 'ok') \
                if it['arm'] in ('single', 'joint') else 'ok'
        usage = {'prompt_tokens': len(body) // 4, 'completion_tokens': 800}
        return FakeResponse(json.dumps({'choices': [{'message': {'content': json.dumps(answer(it, flavour))}}], 'usage': usage}).encode('utf-8'))


def scenario(scratch, name):
    out = scratch / name
    out.mkdir(parents=True)
    budget = pg.budget_module()
    budget.SharedLedger.init(str(out / 'ledger.json'), 0.5)
    ledger = budget.SharedLedger(str(out / 'ledger.json'))
    gate = pg.Gate(out, budget.BudgetTransport(ledger, sleep=lambda seconds: None), ledger)
    (out / 'plan.json').write_text(json.dumps(PLAN))
    stub = Stub(gate.cfg, name)
    saved = (urllib.request.urlopen, os.environ.get('OPENAI_API_KEY'))
    os.environ['OPENAI_API_KEY'] = 'rehearsal-dummy-not-a-key'
    urllib.request.urlopen = stub
    remove_gate = budget.install_stop_gate(ledger)
    try:
        summary = gate.run(PLAN)
    finally:
        remove_gate()
        urllib.request.urlopen = saved[0]
        if saved[1] is None:
            os.environ.pop('OPENAI_API_KEY', None)
        else:
            os.environ['OPENAI_API_KEY'] = saved[1]
    return out, summary, stub


def main(scratch):
    scratch = Path(scratch)
    if scratch.exists():
        raise SystemExit(f'{scratch} exists')
    checks = []

    def ok(name, cond, detail=''):
        checks.append(cond)
        print(f'{"PASS" if cond else "FAIL"}  {name}' + ('' if cond else f'  {detail}'))

    out, summary, stub = scenario(scratch, 'ok')
    ok('every request is the planned v13s body, byte for byte', not stub.problems, stub.problems)
    ok('36 first attempts sent, none refused', stub.sent == 36, stub.sent)
    decisions = {k: v['decision'] for k, v in summary['finals'].items()}
    ok('every first attempt publishes', set(decisions.values()) == {'publish'}, decisions)
    rec = {k: v['decision'] for k, v in summary['reconciled'].items()}
    ok('every separate pair reconciles and publishes', set(rec.values()) == {'publish'}, rec)
    joint = next(i for i in PLAN if i['arm'] == 'joint')
    data = summary['finals'][f'{joint["unit"]}|joint|1']['data']
    lines, grounds = pg.card_lines(joint, joint['family'], joint['members'][0], 'K1', data, 'no answer')
    text = '\n'.join(lines)
    ok('the reader card shows a recomputed outcome', 'Recomputed outcome: [' in text, text[:600])
    ok('the reader card maps the recorded estimate to the card\'s figure numbers', '"type": "estimate", "figure": "F' in text, text[:900])
    before = (out / 'results.json').read_bytes()
    pg.recover(out)
    ok('recovery rewrites results.json from the journals, identical', (out / 'results.json').read_bytes() == before)

    out, summary, stub = scenario(scratch, 'separate-contradiction')
    rec = summary['reconciled']
    first = {k: v['decision'] for k, v in summary['finals'].items() if 'separate-v9' in k and 'pair-old-2' in k}
    ok('the separate Data Center card alone publishes', set(first.values()) == {'publish'}, first)
    ok('reconciliation refuses the pair for S3', all(rec[f'pair-old-2|{d}']['decision'] == 'refused' and
                                                      any(e[0] == 'S3' for e in rec[f'pair-old-2|{d}']['errors']) for d in pg.DRAWS),
       {d: rec[f'pair-old-2|{d}'] for d in pg.DRAWS})

    out, summary, stub = scenario(scratch, 'joint-defects')
    fin = summary['finals']
    two = fin['pair-old-2|joint|1']
    ok('a joint answer with two company Q3 forecasts is refused on its first attempt (S4)', two['attempts'][0]['decision'] == 'refused'
       and any(e[0] == 'S4' for e in two['attempts'][0]['errors']), two['attempts'][0].get('errors'))
    ok('its diagnostic retry publishes', two['attempts'][-1]['decision'] == 'publish', two['attempts'][-1].get('decision'))
    e = fin['single-E|single|1']['attempts'][0]
    ok('a rung outside the ladder is refused (S6)', e['decision'] == 'refused' and any(x[0] == 'S6' for x in e['errors']), e.get('errors'))

    out, summary, stub = scenario(scratch, 'named-defects')
    fin = summary['finals']

    def first(key):
        return fin[key]['attempts'][0]
    for key, rule, label in (('single-O|single|1', 'S1', 'a misread source number'), ('single-O|single|3', 'S2', 'wrong arithmetic'),
                             ('single-S|single|1', 'S5', 'an estimate marked as the market reference'),
                             ('pair-old-1|joint|1', 'S8', 'Data Center added into total revenue')):
        a = first(key)
        ok(f'{label} is refused ({rule}) on the first attempt', a['decision'] == 'refused' and {e[0] for e in a['errors']} == {rule}, a.get('errors'))
    a = first('single-O|single|2')
    ok('its correct counterpart, a real quoted amount read right, publishes', a['decision'] == 'publish', a.get('errors'))
    ok('the other draws of the same units publish', all(first(f'pair-old-1|joint|{d}')['decision'] == 'publish' for d in (2, 3))
       and all(first(f'single-S|single|{d}')['decision'] == 'publish' for d in (2, 3)))

    copy = scratch / 'old-run-copy'
    shutil.copytree(OLD_RUN, copy, ignore=shutil.ignore_patterns('archives'))
    saved = json.loads((copy / 'results.json').read_text())
    items = json.loads((copy / 'plan.json').read_text())
    original = (copy / 'results.json').read_bytes()
    pg.summarise(copy, items, saved['ledger'])
    ok('the old v13 run reproduces results.json byte for byte from its journals (ledger snapshot from results.json)',
       (copy / 'results.json').read_bytes() == original)
    print(f'{sum(checks)} of {len(checks)} checks pass')
    return 0 if all(checks) else 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1]))
