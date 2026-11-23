"""The paid acceptance probe of judging-v12 (PROBE-DESIGN.md v5, D715, D716). Harness-only; nothing here is product code.

  python3 probe.py send <new out folder> <approved ceiling>     # paid: refuses any ceiling but Alex's $0.50
  python3 probe.py rehearse <new out folder> <scenario>         # $0: the provider stubbed beneath the real budget transport

Order (§2): A1, A0; Part B (16 refused requests x 3 under v12, 4 at a time); Part C (12 comparisons, cheapest first, one at a time,
each starting only when the ledger's headroom covers its six first attempts' reservations; its six sends one after another); A2 last
and only when the headroom covers its reservation. Every send has its own archive, so no draw is answered from an earlier one. Each
answer goes through `model.call` (the format check) and the request-time check, and is written to answers.jsonl.
"""
import concurrent.futures
import importlib.util
import json
import re
import sys
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / 'src'))
from hivemind import config, model                                      # noqa: E402
from hivemind.views import judging                                     # noqa: E402

PLAN = HERE / 'probe-plan.json'
V121 = REPO / 'poc/config/poc-v121.json'
APPROVED_CEILING = 0.50                                                 # Alex, D715
B_WORKERS = 4
EXPECTED = {'A': 2, 'B': 48, 'C': 72}


def budget_module():
    spec = importlib.util.spec_from_file_location('budget_replay_probe', REPO / 'clean-arch/e2e-comparison-2026-11-13/budget_replay.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def key_of(item):
    return f'{item["source"]}:{item["call_id"]}'


def answer_format(item, form):
    return judging.schema_for('judging-v12', item['lists']) if form == 'v12' else judging.schema_for('judging-v7')


def header_counts(user):
    """(evidence entries the header announces, themes the header announces): the text-read lists must match them."""
    evidence = re.search(r'\[Evidence in view under this thesis, (\d+) items\]', user)
    themes = re.search(r'\[Themes in force, (\d+)\]', user)
    return (int(evidence.group(1)) if evidence else None), (int(themes.group(1)) if themes else 0)


def check_at_request(data, user, lists):
    """`judging.check_answer` as at request time: membership against the request's lists; the rung range from its ladder line;
    first-judgement and changed from its previous-conclusion line; the stance fields; duplicate theme pushes. Same messages."""
    view_id = re.match(r'Thesis (v\d+) \(', user).group(1)
    errors, named = [], []
    for entry in data.get('theme_pushes', []):
        if entry['view_id'] in named:
            errors.append(f'{entry["view_id"]} is named twice in theme_pushes')
        elif entry['view_id'] not in lists['themes']:
            errors.append(f'{entry["view_id"]} is not a theme in force shown to {view_id}')
        named.append(entry['view_id'])
    ladder = re.search(r'^Ladder: (.*)$', user, re.M).group(1)
    rung_count = len(re.findall(r'(?:^|/ )rung \d+ ', ladder))
    if not 1 <= data['rung'] <= rung_count:
        errors.append(f'rung {data["rung"]} outside 1..{rung_count}')
    for cited in data['cites']:
        if cited not in lists['evidence']:
            errors.append(f'{cited} is not among the evidence shown to {view_id}')
    for cited in data['cites_views']:
        if cited not in lists['dependencies']:
            errors.append(f'{cited} is not a dependency of {view_id}')
    for push in data['pushes']:
        if push['evidence_id'] not in lists['evidence']:
            errors.append(f'push on {push["evidence_id"]} which was not shown to {view_id}')
    for field in judging.STANCE_FIELDS:
        if not str(data.get(field) or '').strip():
            errors.append(f'{field} is empty: state what the market expects and the figure or date the evidence implies')
    previous = re.search(r'^\[Previous conclusion, for comparison only\] rung (\d+);', user, re.M)
    if previous is None and '\n[Previous conclusion] none: this is the first judgement' in user and not data['changed']:
        errors.append('first judgement must say changed')
    if previous is not None and int(previous.group(1)) != data['rung'] and not data['changed']:
        errors.append(f'rung moved from {previous.group(1)} to {data["rung"]} but changed is false')
    return errors


def schedule(plan):
    """The sends in order, grouped: [('A1', [spec]), ('A0', ...), ('B', [48 specs]), ('C', [[6 specs] x 12]), ('A2', [spec])]."""
    spec = lambda part, item, form, draw: {'part': part, 'key': key_of(item), 'form': form, 'draw': draw, 'item': item}
    a1, a0, a2 = plan['acceptance']
    b = [spec('B', item, 'v12', d) for item in plan['refused'] for d in (1, 2, 3)]
    c = [[spec('C', item, form, d) for form in ('v12', 'v7') for d in (1, 2, 3)] for item in plan['matched']]
    return [('A1', [spec('A1', a1, 'v12', 1)]), ('A0', [spec('A0', a0, 'v12', 1)]), ('B', b), ('C', c), ('A2', [spec('A2', a2, 'v12', 1)])]


ACCOUNT = threading.local()                                            # per send: provider attempts and the amounts the ledger settled


def counting(transport):
    def wrapped(provider, request, *arguments, **keywords):
        ACCOUNT.attempts = getattr(ACCOUNT, 'attempts', 0) + 1
        return transport(provider, request, *arguments, **keywords)
    return wrapped


class Probe:
    def __init__(self, out, transport, ledger, budget):
        self.out, self.transport, self.ledger, self.budget = out, transport, ledger, budget
        self.cfg = config.load(str(V121))
        self.lock = threading.Lock()
        (out / 'archives').mkdir(parents=True)
        settle = ledger.settle

        def settled(reserved, actual, *arguments, **keywords):
            ACCOUNT.charged = getattr(ACCOUNT, 'charged', 0.0) + actual
            return settle(reserved, actual, *arguments, **keywords)
        ledger.settle = settled

    def request(self, spec):
        return model.build_request(self.cfg.rejudging, spec['item']['system'], spec['item']['user'], answer_format(spec['item'], spec['form']),
                                   'judgement', self.cfg.provider)

    def reservation(self, spec):
        return self.budget.llm_estimate(self.request(spec))

    def headroom(self):
        state = self.ledger.read()
        return state['ceiling'] - state['spent'] - state['reserved'], state

    def record(self, line):
        with self.lock, open(self.out / 'answers.jsonl', 'a') as handle:
            handle.write(json.dumps(line, ensure_ascii=False) + '\n')

    def send(self, spec):
        item, form = spec['item'], spec['form']
        name = f'{spec["part"]}-{spec["key"].replace(":", "-")}-{form}-{spec["draw"]}.sqlite'
        archive = model.Archive(str(self.out / 'archives' / name))
        line = {k: spec[k] for k in ('part', 'key', 'form', 'draw')}
        line['request_sha256'] = model.request_identity(self.request(spec))[1]
        ACCOUNT.attempts, ACCOUNT.charged = 0, 0.0
        try:
            answer = model.call(archive, self.cfg, self.cfg.rejudging, item['system'], item['user'], answer_format(item, form), 'judgement', 'judge',
                                transport=self.transport)
            line.update(status='answered', data=answer.data, cost_usd=answer.cost_usd, cached=answer.cached,
                        check=check_at_request(answer.data, item['user'], item['lists']))
        except model.SchemaError as error:
            row = archive.conn.execute('select answer_json from model_calls order by call_id desc limit 1').fetchone()
            line.update(status='format invalid', error=str(error)[:500], data=json.loads(row[0]) if row and row[0] else None)
        except model.TransportError as error:
            line.update(status='transport error', error=str(error)[:500], http_status=getattr(error, 'http_status', None))
        line.update(provider_attempts=ACCOUNT.attempts, charged_usd=round(ACCOUNT.charged, 6))
        self.record(line)
        return line

    def run(self, plan):
        for item in plan['acceptance'][:2] + plan['refused'] + plan['matched']:
            evidence, themes = header_counts(item['user'])
            if evidence is not None and (evidence != len(item['lists']['evidence']) or themes != len(item['lists']['themes'])):
                raise SystemExit(f'{key_of(item)}: the text-read lists do not match the header counts; not sent')
        summary = {'sent': {}, 'not started': [], 'interrupted': [], 'A2': None, 'stopped after': None}
        for group, specs in schedule(plan):
            if summary['stopped after']:
                break
            if group in ('A1', 'A0'):
                summary['sent'][group] = [self.send(s)['status'] for s in specs]
                if summary['sent'][group] != ['answered']:          # D715: the format checks decide whether to go on
                    summary['stopped after'] = group
            elif group == 'B':
                with concurrent.futures.ThreadPoolExecutor(max_workers=B_WORKERS) as pool:
                    summary['sent']['B'] = [line['status'] for line in pool.map(self.send, specs)]
            elif group == 'C':
                summary['sent']['C'] = []
                for comparison in specs:
                    need = sum(self.reservation(s) for s in comparison)
                    room, state = self.headroom()
                    if state.get('stopped') or room < need:
                        summary['not started'].append({'key': comparison[0]['key'], 'need': round(need, 4), 'headroom': round(room, 4)})
                        continue
                    statuses = []
                    for s in comparison:
                        statuses.append(self.send(s)['status'])
                        if statuses[-1] == 'transport error':
                            summary['interrupted'].append(comparison[0]['key'])
                            break
                    summary['sent']['C'].append({'key': comparison[0]['key'], 'statuses': statuses})
            else:
                summary['core ledger'] = self.ledger.read()          # the verdict reads the ledger as the core run left it
                need = 3 * self.reservation(specs[0])                   # its first attempt and two retries
                room, state = self.headroom()
                summary['A2'] = self.send(specs[0])['status'] if not state.get('stopped') and room >= need else f'skipped (headroom {room:.4f} < {need:.4f})'
        summary.setdefault('core ledger', self.ledger.read())
        summary['ledger'] = self.ledger.read()
        (self.out / 'run-summary.json').write_text(json.dumps(summary, indent=1))
        return summary


def send(out, approved):
    if approved != APPROVED_CEILING:
        raise SystemExit(f'the approved ceiling is ${APPROVED_CEILING} (D715); refused')
    if out.exists():
        raise SystemExit(f'{out} exists: the probe starts from an empty folder')
    out.mkdir(parents=True)
    budget = budget_module()
    ledger_path = out / 'ledger.json'
    budget.SharedLedger.init(str(ledger_path), approved)
    ledger = budget.SharedLedger(str(ledger_path))
    lock_handle = open(out / 'probe.launcher.lock', 'a+')
    if not ledger.claim_launcher('probe', lock_handle):
        raise SystemExit('another launch is running')
    remove_gate = budget.install_stop_gate(ledger)
    try:
        original = model.openai_transport
        model.openai_transport = counting(original)
        try:
            summary = Probe(out, budget.BudgetTransport(ledger), ledger, budget).run(json.loads(PLAN.read_text()))
        finally:
            model.openai_transport = original
    finally:
        remove_gate()
        ledger.remove_launcher('probe')
    print(json.dumps(summary, indent=1)[:4000])


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else ''
    if command == 'send' and len(sys.argv) == 4 and not sys.argv[2].startswith('-'):
        send(Path(sys.argv[2]), float(sys.argv[3]))
    elif command == 'rehearse' and len(sys.argv) == 4 and not sys.argv[2].startswith('-'):
        import probe_rehearsal
        probe_rehearsal.main(Path(sys.argv[2]), sys.argv[3])
    else:
        raise SystemExit(__doc__)
