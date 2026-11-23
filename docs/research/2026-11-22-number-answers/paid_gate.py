"""The paid gate of judging-v13 (D725's registered test; D729, D730). Harness-only; nothing here is product code.

  python3 paid_gate.py plan <out.json>                        # $0: build every request from the stored runs and check them
  python3 paid_gate.py send <new out folder> <ceiling>        # paid: only at the ceiling Alex names (APPROVED_CEILING)
  python3 paid_gate.py packets <out folder> <key folder>      # $0: blind reading packets, the arm hidden; the key kept outside the repo
  python3 paid_gate.py verdict <out folder> <readings.json> <key folder>   # $0: the registered pass and stop lines

The test (D725, RESULT.md): the 09-20 total and Data Center pair in each of three stored draws, judged jointly (one v13 family call)
and separately (each member alone, the same union of evidence, the same v13 format), three samples each; plus three samples each of
the O, S and E singletons. 9 + 18 + 9 = 36 first attempts. A calculation the checks refuse is retried once with its errors; a second
refusal makes the unit unresolved. The separate arm's two answers are then reconciled by the same checks over the pair's family.
"""
import hashlib
import json
import random
import re
import secrets
import sqlite3
import sys
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / 'src'))
import calc_check as cc                                                 # noqa: E402
import calc_small as cs                                                 # noqa: E402
import render_v13 as rv                                                 # noqa: E402
from hivemind import config, model                                      # noqa: E402

RUN = REPO / 'poc/data/comparison-2026-11-17/run'
CONFIG = REPO / 'poc/config/poc-v118.json'                              # its re-judging model setting: gpt-6-luna, medium, 16000 output tokens
SYSTEM = (HERE / 'judging-v13-draft.txt').read_text()
SYSTEM_S = (HERE / 'judging-v13s.txt').read_text()                      # the small format (D737): one sentence changed
CHECKERS = {None: cc, 'v13': cc, 'v13s': cs}
APPROVED_CEILING = 0.5                                                  # Alex, 2026-11-22 (D732): "0.5 美元 (推荐)"
PINNED_PLAN_SHA256 = (HERE / 'paid-plan.sha256').read_text().strip() if (HERE / 'paid-plan.sha256').exists() else None
AUTH = Path.home() / '.hivemind-keys/v13-paid-gate/authorization.json'
# D753: Alex's one-time exception, a v13s re-send. Its own reviewed plan pin and its own one-time authorization; the v13 ones stay.
PINNED_PLAN_V13S = (HERE / 'paid-plan-v13s.sha256').read_text().strip() if (HERE / 'paid-plan-v13s.sha256').exists() else None
AUTH_V13S = Path.home() / '.hivemind-keys/v13s-paid-gate/authorization.json'
DRAWS = (1, 2, 3)
RETRY_MARK = '\n\nThe code refused the previous answer because: '
PAIRS = [('old-1', ('v4', 9014), ('v8', 9022)), ('old-2', ('v14', 8729), ('v9', 8737)), ('old-3', ('v3', 9183), ('v35', 9177))]
SINGLETONS = [('O', 'old-2', 'v29', 8734, ('NVIDIA', 'equity investment commitments', 'company', 'end of FY2027')),
              ('S', 'old-2', 'v6', 8595, ('four largest AI hyperscalers', 'data-center capex', 'combined', 'CY2027')),
              ('E', 'old-3', 'v41', 9166, ('NVIDIA', 'revenue', 'Vera CPU', 'FY2028'))]


def W(population, measure, scope, period):
    return {'population': population, 'measure': measure, 'scope': scope, 'period': period}


def bands(draw, view_id):
    conn = sqlite3.connect(f'file:{RUN / draw / "prod/views.sqlite"}?mode=ro', uri=True)
    rows = conn.execute('select lo, hi from rungs where view_id=? order by position', (view_id,)).fetchall()
    return [[lo / 1e9 if lo is not None else None, hi / 1e9 if hi is not None else None] for lo, hi in rows]


def passages(draw, evidence_ids):
    """What each request showed of a passage: the quote cut at 400 characters (judging._lines_english)."""
    conn = sqlite3.connect(f'file:{RUN / draw / "prod/views.sqlite"}?mode=ro', uri=True)
    rows = conn.execute(f'select evidence_id, quote, speaker from evidence where evidence_id in ({",".join("?" * len(evidence_ids))})',
                        evidence_ids).fetchall()
    return {e: {'text': (q or '')[:400], 'speaker': s} for e, q, s in rows}


def pair_family(draw, total, dc):
    return {'members': {total[0]: {'what': W('NVIDIA', 'revenue', 'company', 'FY2027'), 'bands': bands(draw, total[0])},
                        dc[0]: {'what': W('NVIDIA', 'revenue', 'Data Center', 'FY2027'), 'bands': bands(draw, dc[0])}},
            'relations': [{'type': 'part_of', 'part': dc[0], 'whole': total[0]}],
            'shared': [W('NVIDIA', 'revenue', 'company', 'FY2027 Q3'), W('NVIDIA', 'revenue', 'company', 'FY2027 Q4')],
            'compare_periods': ['FY2027 Q3', 'FY2027 Q4', 'FY2027']}


def only(family, view_id):
    out = {'members': {view_id: family['members'][view_id]}, 'relations': [], 'shared': family['shared'], 'compare_periods': []}
    if 'part_scopes' in family:                                         # [53] the separate arm keeps S8's part-of scopes (D738)
        out['part_scopes'] = family['part_scopes']
    return out


def small_family(family, part_scopes=(), notes=None):
    """[D737] A family for the small format: each member's unit (USD bn: the bands are in billions), the part-of scopes S8 reads, and
    any note on a member's key."""
    out = json.loads(json.dumps(family))
    for v, m in out['members'].items():
        m['unit'] = 'USD bn'
        if notes and v in notes:
            m['key_note'] = notes[v]
    out['part_scopes'] = list(part_scopes)
    return out


PAIR_SCOPES = [{'population': 'NVIDIA', 'measure': 'revenue', 'part': 'Data Center', 'whole': 'company'}]
O_NOTE = 'the balance at the end of FY2027, as the FY2027 annual report publishes it'


def checker(fmt):
    return CHECKERS[fmt]


def decode(data, fmt, family):
    """The stored wire answer in the shape the checks and packets read, by the plan's format."""
    return cs.from_answer(data, family) if fmt == 'v13s' else strip(data)


def questions(draw, view_ids):
    conn = sqlite3.connect(f'file:{RUN / draw / "prod/views.sqlite"}?mode=ro', uri=True)
    out = {}
    for v in view_ids:
        q = conn.execute('select question from views where view_id=?', (v,)).fetchone()[0]
        ladder = [c for (c,) in conn.execute('select condition from rungs where view_id=? order by position', (v,))]
        out[v] = {'question': q, 'ladder': ladder}
    return out


def shown_lines(user):
    """Each evidence item exactly as the request showed it: its header line (tier, speaker, original source and date) and its quote."""
    m = re.search(r'\[Evidence in view for the family, \d+ items\]\n(.*?)(?:\n\n\[|\n\nAnswer per)', user, re.S)
    out = {}
    for chunk in re.split(r'\n(?=- e\d+ )', m.group(1) if m else ''):
        if chunk.startswith('- e'):
            out[chunk[2:].split(' ', 1)[0]] = chunk
    return out


def item(unit, arm, draw, calls, family, shown, fmt='v13'):
    archive = RUN / draw / 'prod/archive.sqlite'
    if fmt == 'v13s':
        user, evidence_ids, theme_ids = rv.render(archive, calls, family, shown=shown, fmt='v13s')
        return {'unit': unit, 'arm': arm, 'draw_store': draw, 'members': sorted(shown), 'format': 'v13s', 'system': SYSTEM_S, 'user': user,
                'schema': rv.v13s_schema(sorted(shown), evidence_ids, theme_ids), 'family': family, 'passages': passages(draw, evidence_ids),
                'evidence_ids': evidence_ids, 'questions': questions(draw, sorted(shown)), 'shown': shown_lines(user)}
    user, evidence_ids, theme_ids = rv.render(archive, calls, family, shown=shown)
    return {'unit': unit, 'arm': arm, 'draw_store': draw, 'members': sorted(shown), 'system': SYSTEM, 'user': user,
            'schema': rv.v13_schema(sorted(shown), evidence_ids, theme_ids), 'family': family, 'passages': passages(draw, evidence_ids),
            'evidence_ids': evidence_ids, 'questions': questions(draw, sorted(shown)), 'shown': shown_lines(user)}


def build_plan(fmt='v13'):
    items = []
    small = fmt == 'v13s'
    for draw, total, dc in PAIRS:
        family = pair_family(draw, total, dc)
        if small:
            family = small_family(family, PAIR_SCOPES)
        calls = [total, dc]
        items.append(item(f'pair-{draw}', 'joint', draw, calls, family, [total[0], dc[0]], fmt))
        for member in (total, dc):                            # the same union of evidence, one member's header and answer
            items.append(item(f'pair-{draw}', f'separate-{member[0]}', draw, calls, only(family, member[0]), [member[0]], fmt))
    for name, draw, view_id, call_id, what in SINGLETONS:
        family = {'members': {view_id: {'what': W(*what), 'bands': bands(draw, view_id)}}, 'relations': [], 'shared': [], 'compare_periods': []}
        if small:
            family = small_family(family, notes={view_id: O_NOTE} if name == 'O' else None)
        items.append(item(f'single-{name}', 'single', draw, [(view_id, call_id)], family, [view_id], fmt))
    return items


def plan(out, fmt='v13'):
    items = build_plan(fmt)
    report = []
    for it in items:
        missing = sorted(set(it['evidence_ids']) - set(it['passages']))
        report.append(f'{it["unit"]:14} {it["arm"]:14} members {it["members"]} user {len(it["user"])} chars, evidence {len(it["evidence_ids"])}, '
                      f'schema {len(json.dumps(it["schema"]))} chars, passages missing {missing or "none"}')
        if missing or 'Outcome keys' not in it['user']:
            raise SystemExit(f'{it["unit"]} {it["arm"]}: incomplete request; not planned')
    ids = [(i['unit'], i['arm']) for i in items]
    if len(set(ids)) != len(ids):
        raise SystemExit('duplicate (unit, arm) in the plan; not planned')
    text = json.dumps(items, indent=1)
    Path(out).write_text(text)
    Path(out).with_suffix('.sha256').write_text(hashlib.sha256(text.encode()).hexdigest() + '\n')
    print('\n'.join(report))
    print(f'{len(items)} requests x {len(DRAWS)} draws = {len(items) * len(DRAWS)} first attempts')


def strip(data):
    return rv.without_nulls(data)


class Gate:
    def __init__(self, out, transport, ledger=None):
        self.out, self.transport, self.ledger = out, transport, ledger
        self.cfg = config.load(str(CONFIG))
        self.lock = threading.Lock()
        (out / 'archives').mkdir(parents=True, exist_ok=True)

    def request(self, it, user):
        return model.build_request(self.cfg.rejudging, it['system'], user, it['schema'], 'judgement', self.cfg.provider)

    def record(self, line):
        """[47g] Scored first attempts go to answers.jsonl, diagnostic retries to retries.jsonl, so damage to a retry's record can be
        seen without touching the scored record."""
        name = 'answers.jsonl' if line['attempt'] == 1 else 'retries.jsonl'
        with self.lock, open(self.out / name, 'a') as handle:
            handle.write(json.dumps(line, ensure_ascii=False) + '\n')

    def attempt(self, it, draw, user, n):
        name = f'{it["unit"]}-{it["arm"]}-d{draw}-a{n}.sqlite'
        archive = model.Archive(str(self.out / 'archives' / name))
        line = {'unit': it['unit'], 'arm': it['arm'], 'draw': draw, 'attempt': n,
                'request_sha256': model.request_identity(self.request(it, user))[1]}
        self.record(dict(line, status='started'))                          # [47.3] recorded before the provider is called
        data = None
        try:
            answer = model.call(archive, self.cfg, self.cfg.rejudging, it['system'], user, it['schema'], 'judgement', 'judge', transport=self.transport)
            data = answer.data
            line.update(cost_usd=answer.cost_usd, data=data)
            fmt = it.get('format')
            calc = decode(data, fmt, it['family'])
            result = checker(fmt).check(it['family'], it['passages'], calc)
            decision = checker(fmt).publish_decision(it['family'], calc, result)
            line.update(status='answered', errors=result['errors'], recorded=result['recorded'], published=result.get('published'), decision=decision)
        except model.SchemaError as error:
            row = archive.conn.execute('select response_json from model_calls order by call_id desc limit 1').fetchone()
            line.update(status='format invalid', error=str(error)[:500], decision='refused', errors=[('schema', str(error)[:300])],
                        raw=row[0] if row and row[0] else None)           # [47f.2] whole, as the archive stores it
        except model.TransportError as error:
            line.update(status='transport error', error=str(error)[:500], decision='transport')
        except Exception as error:                                       # [47.3] a checker failure is recorded with the raw answer and refused
            line.update(status='checker error', error=f'{type(error).__name__}: {error}'[:500], decision='refused',
                        errors=[('checker', f'{type(error).__name__}: {error}'[:300])], data=data)
        self.record(line)
        return line

    def stopped(self):
        return self.ledger is not None and self.ledger.read().get('stopped')

    def run(self, items):
        """[47f.1] Every first attempt (the scored ones) is sent before any retry (diagnostic only), so a retry's cost or failure can
        never stop a scored attempt from being sent."""
        try:
            refused = []
            for draw in DRAWS:
                for it in items:
                    if not self.stopped():
                        first = self.attempt(it, draw, it['user'], 1)
                        if first['decision'] == 'refused':
                            refused.append((it, draw, first))
            for it, draw, first in refused:
                if not self.stopped():
                    reasons = '; '.join(f'{c}: {d}' for c, d in first.get('errors', []))[:4000]
                    self.attempt(it, draw, it['user'] + RETRY_MARK + reasons, 2)
        finally:                                          # [47b.2] the results come from the attempt records, written even after an abort
            summary = summarise(self.out, items, self.ledger.read() if self.ledger else None)
        return summary


JOURNALS = ('answers.jsonl', 'retries.jsonl')


def attempt_records(out, damaged=None):
    """The committed entries of both journals, split on the writer's own delimiter ('\\n' only: an answer may hold other Unicode line
    separators). A line that does not parse (a write torn by a crash) is skipped and listed in `damaged` with its journal, so its
    attempt counts as unfinished."""
    records = []
    for name in JOURNALS:
        path = out / name
        text = path.read_text(encoding='utf-8', errors='replace') if path.exists() else ''
        for number, line in enumerate(text.split('\n'), 1):
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                if damaged is not None:
                    damaged.append({'journal': name, 'line': number, 'text': line[:200]})
    return records


ATTEMPT_FIELDS = ('attempt', 'status', 'decision', 'errors', 'data', 'raw')


def first_attempt(entry):
    """[47e.1] The attempt that is scored: the first one, on both arms (a retry is diagnostic). No attempt: not sent."""
    attempts = sorted(entry.get('attempts') or [], key=lambda a: a['attempt'])
    return attempts[0] if attempts else {'attempt': 1, 'status': 'not sent', 'decision': 'not sent'}


def derive_finals(out, items, damaged=None):
    """Each planned unit and draw: 'dispatched' (a started line), 'completed' (a finished line), and the decision of its last finished
    attempt (a second refusal is unresolved). A unit with no started line is not sent; one started but not finished is interrupted."""
    records = attempt_records(out, damaged)
    finals = {}
    for it in items:
        for draw in DRAWS:
            mine = [r for r in records if r['unit'] == it['unit'] and r['arm'] == it['arm'] and r['draw'] == draw]
            started = [r for r in mine if r['status'] == 'started']
            done = [r for r in mine if r['status'] != 'started']
            key = f'{it["unit"]}|{it["arm"]}|{draw}'
            if not started:
                finals[key] = {'decision': 'not sent', 'attempts': []}
                continue
            if len(done) < len(started):
                unfinished = [{'attempt': r['attempt'], 'status': 'interrupted', 'decision': 'interrupted'} for r in started
                              if r['attempt'] not in {d['attempt'] for d in done}]
                finals[key] = {'decision': 'interrupted', 'attempts': [{k: r.get(k) for k in ATTEMPT_FIELDS} for r in done] + unfinished}
                continue
            last = done[-1]
            decision = last['decision']
            if decision == 'refused':                          # a second refusal is unresolved; a first with no retry sent is incomplete
                decision = 'unresolved' if len(done) >= 2 else 'retry not sent'
            finals[key] = {k: last.get(k) for k in ('status', 'data', 'errors', 'recorded', 'published')}
            finals[key].update(decision=decision, attempts=[{k: r.get(k) for k in ATTEMPT_FIELDS} for r in done])
    return finals


def summarise(out, items, ledger_state):
    damaged = []
    finals = derive_finals(out, items, damaged)
    reconciled = {}
    fmt = items[0].get('format') if items else None
    ck = checker(fmt)
    for draw_store, total, dc in PAIRS:                     # the separate arm, reconciled over the pair's family
        for draw in DRAWS:
            a, b = (first_attempt(finals.get(f'pair-{draw_store}|separate-{m[0]}|{draw}', {})) for m in (total, dc))   # [47e.1]
            if a.get('decision') != 'publish' or b.get('decision') != 'publish':
                reconciled[f'pair-{draw_store}|{draw}'] = {'decision': 'not reconciled', 'members': [a.get('decision'), b.get('decision')]}
                continue
            joint = next(i for i in items if i['unit'] == f'pair-{draw_store}' and i['arm'] == 'joint')
            family = joint['family'] if fmt == 'v13s' else pair_family(draw_store, total, dc)
            merged = merge([(total[0], decode(a['data'], fmt, family)), (dc[0], decode(b['data'], fmt, family))],
                           {ck._key(s) for s in family['shared']}, ck)
            pas = joint['passages']
            result = ck.check(family, pas, {k: merged[k] for k in ('figures', 'answers')})
            reconciled[f'pair-{draw_store}|{draw}'] = {'decision': ck.publish_decision(family, merged, result), 'errors': result['errors'],
                                                     'published': result.get('published'), 'calc': merged}
    summary = {'finals': finals, 'reconciled': reconciled, 'ledger': ledger_state, 'damaged': damaged}
    (out / 'results.json').write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    return summary


def _same_value(a, b):
    """Two recomputed (interval, bound) values are the same when their bounds match and each end agrees within 1e-9 relative."""
    if a is None or b is None or a[1] != b[1]:
        return False
    return all(abs(x - y) <= 1e-9 * max(1.0, abs(x), abs(y)) for x, y in zip(a[0], b[0]))


def merge(parts, shared_keys, ck=cc):
    """Two separate answers as one calculation: each figure id prefixed by its member; then [47.1, 47c.1] a forecast of a declared
    shared quantity in the second call is unified with the first call's forecast of the same quantity and scenario when their
    recomputed values are the same (references point to the first, the duplicate kept beside the calculation). Duplicates inside one
    call are never unified, and forecasts that differ are both kept, so the family's checks judge them as they judge a joint answer."""
    figures, answers, recomputed, owner, units = [], [], {}, {}, {}
    for view_id, calc in parts:
        rename = {f['id']: f'{view_id}.{f["id"]}' for f in calc['figures']}
        figs = {f['id']: f for f in calc['figures']}
        refs = lambda f, figs=figs: list(f.get('inputs', [])) + [r for r in f.get('rests_on', []) if r in figs] + \
            ([f['adjusts']['figure']] if f.get('adjusts') else []) + ([f['bridge']] if f.get('bridge') else [])
        try:
            values = ck._evaluate_bounded(figs, refs, {})
        except Exception:
            values = {}
        for f in calc['figures']:
            g = dict(f, id=rename[f['id']])
            for key in ('inputs', 'rests_on', 'converts'):
                if key in g:
                    g[key] = [rename.get(x, x) for x in g[key]]
            for key in ('disputed', 'bridge'):
                if key in g:
                    g[key] = rename.get(g[key], g[key])
            if 'adjusts' in g:
                g['adjusts'] = dict(g['adjusts'], figure=rename.get(g['adjusts']['figure'], g['adjusts']['figure']))
            figures.append(g)
            recomputed[g['id']] = values.get(f['id'])
            owner[g['id']] = view_id
            units[g['id']] = f.get('unit')
        for a in calc['answers']:
            a2 = dict(a)
            if 'outcome' in a2:
                a2['outcome'] = rename.get(a2['outcome'], a2['outcome'])
            if a2.get('reference', {}).get('figure'):
                a2['reference'] = {'figure': rename.get(a2['reference']['figure'], a2['reference']['figure'])}
            answers.append(a2)
    key = lambda f: (f['what']['population'], f['what']['measure'], f['what']['scope'], f['what']['period'], f.get('scenario', 'base'))
    candidates = {}
    for g in figures:
        if g.get('basis') == 'forecast' and ck._key(g['what']) in shared_keys:
            candidates.setdefault(key(g), {}).setdefault(owner[g['id']], []).append(g['id'])
    alias, duplicates = {}, []
    for k, by_call in candidates.items():                  # [47d.2] one to one: each call holds exactly one candidate
        if len(by_call) == 2 and all(len(ids) == 1 for ids in by_call.values()):
            (a,), (b,) = (by_call[v] for v, _ in parts)
            if units[a] == units[b] and _same_value(recomputed.get(a), recomputed.get(b)):   # [47b.1] equal values, [47e.2] in one unit
                alias[b] = a
    if alias:
        kept = []
        for g in figures:
            if g['id'] in alias:
                duplicates.append(g)
                continue
            for k2 in ('inputs', 'rests_on', 'converts'):
                if k2 in g:
                    g[k2] = [alias.get(x, x) for x in g[k2]]
            for k2 in ('disputed', 'bridge'):
                if k2 in g:
                    g[k2] = alias.get(g[k2], g[k2])
            if 'adjusts' in g:
                g['adjusts'] = dict(g['adjusts'], figure=alias.get(g['adjusts']['figure'], g['adjusts']['figure']))
            kept.append(g)
        figures = kept
        for a in answers:
            if a.get('outcome') in alias:
                a['outcome'] = alias[a['outcome']]
            if a.get('reference', {}).get('figure') in alias:
                a['reference'] = {'figure': alias[a['reference']['figure']]}
    return {'figures': figures, 'answers': answers, 'unified': [{'kept': alias[d['id']], 'duplicate': d} for d in duplicates]}


def recover(out):
    """Read-only: rebuild results.json from the journal of a stopped run; nothing is sent."""
    items = json.loads((out / 'plan.json').read_text())
    ledger = json.loads((out / 'ledger.json').read_text()) if (out / 'ledger.json').exists() else None
    summary = summarise(out, items, ledger)
    print(json.dumps({'damaged': summary['damaged'], 'finals': {k: v['decision'] for k, v in summary['finals'].items()}}, indent=1))
    return summary


def budget_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location('budget_replay_v13', REPO / 'clean-arch/e2e-comparison-2026-11-13/budget_replay.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def send(out, approved, plan_path):
    if APPROVED_CEILING is None or approved != APPROVED_CEILING:
        raise SystemExit(f'the approved ceiling is {APPROVED_CEILING} (Alex names it); refused')
    if out.exists():
        raise SystemExit(f'{out} exists: the gate starts from an empty folder')
    text = Path(plan_path).read_text()
    items = json.loads(text)
    formats = {i.get('format') for i in items}
    if formats == {'v13s'}:                                                  # D753: the v13s re-send has its own pin and authorization
        pin, auth = PINNED_PLAN_V13S, AUTH_V13S
    elif 'v13s' in formats:
        raise SystemExit('the plan mixes formats; refused')
    else:
        pin, auth = PINNED_PLAN_SHA256, AUTH
    if pin is None or hashlib.sha256(text.encode()).hexdigest() != pin:          # [47.2] only the reviewed plan
        raise SystemExit('the plan is not the reviewed one (sha256 differs); refused')
    auth.parent.mkdir(parents=True, exist_ok=True)
    try:                                                                     # [47.2] one authorization, one ledger, one launch
        with open(auth, 'x') as handle:
            json.dump({'plan_sha256': pin, 'ceiling': approved, 'out': str(out)}, handle)
    except FileExistsError:
        raise SystemExit(f'{auth} exists: this authorization was already used; refused')
    if len({(i['unit'], i['arm']) for i in items}) != len(items):
        raise SystemExit('duplicate (unit, arm) in the plan; refused')
    out.mkdir(parents=True)
    (out / 'plan.json').write_text(json.dumps(items))
    budget = budget_module()
    budget.SharedLedger.init(str(out / 'ledger.json'), approved)
    ledger = budget.SharedLedger(str(out / 'ledger.json'))
    lock_handle = open(out / 'gate.launcher.lock', 'a+')
    if not ledger.claim_launcher('v13-gate', lock_handle):
        raise SystemExit('another launch is running')
    remove_gate = budget.install_stop_gate(ledger)
    try:
        summary = Gate(out, budget.BudgetTransport(ledger), ledger).run(items)
    finally:
        remove_gate()
        ledger.remove_launcher('v13-gate')
    print(json.dumps({k: v.get('decision') for k, v in summary['finals'].items()}, indent=1))


# ---------- blind reading ----------
QUESTIONS = {'usable': 'the outcome is usable and supported by the shown passages it rests on',
             'contradiction': 'with the other card of its packet, it states a hard numerical contradiction',
             'internal_reference': "the system's own forecast is presented as the market's expectation",
             'deciding_gap': 'an unresolved overlap, a change of scope or an unsized adjustment decides its band'}


FIGURE_TOKEN = re.compile(r'\b([A-Za-z0-9]*F\d+)\b')
PASSAGE_TOKEN = re.compile(r'\b(e\d+)\b')
PASSAGE_RANGE = re.compile(r'\be(\d+)\s*[-–]\s*e?(\d+)\b')


def renamed_text(text, rename):
    """[D753, council 70] Figure ids inside prose follow the renumbering, so a reference in the reasons still points to the figure the
    writer meant; an id the card does not show is left as written."""
    return FIGURE_TOKEN.sub(lambda m: rename.get(m.group(1), m.group(1)), text) if isinstance(text, str) else text


def named_in_text(text, figure_ids, shown_passages):
    """[D753, council 70] The figure ids and passage ids a prose field names, a written range e5399-e5404 included in full."""
    if not isinstance(text, str):
        return set(), set()
    figures = {t for t in FIGURE_TOKEN.findall(text) if t in figure_ids}
    passages = {t for t in PASSAGE_TOKEN.findall(text) if t in shown_passages}
    for lo, hi in PASSAGE_RANGE.findall(text):        # every shown passage inside a written range (council 70b: no width limit)
        lo, hi = int(lo), int(hi)
        if hi > lo:
            passages |= {f'e{n}' for n in range(lo, hi + 1) if f'e{n}' in shown_passages}
    return figures, passages


def normalise(calc, prefix=''):
    """Figure ids renumbered F1.. (after `prefix`) and member prefixes removed, so the arm cannot be read from the ids. Ids named in
    prose (reasons, why, basis_text) are renumbered with them."""
    rename = {f['id']: f'{prefix}F{n}' for n, f in enumerate(calc['figures'], 1)}
    out = []
    for f in calc['figures']:
        g = dict(f, id=rename[f['id']])
        if 'basis_text' in g:
            g['basis_text'] = renamed_text(g['basis_text'], rename)
        for key in ('inputs', 'rests_on', 'converts'):
            if key in g:
                g[key] = [rename.get(x, x) for x in g[key]]
        for key in ('disputed', 'bridge'):
            if key in g:
                g[key] = rename.get(g[key], g[key])
        if 'adjusts' in g:
            g['adjusts'] = dict(g['adjusts'], figure=rename.get(g['adjusts']['figure'], g['adjusts']['figure']))
        out.append(g)
    answers = []
    for a in calc['answers']:
        a2 = dict(a)
        for key in ('reasons', 'why'):
            if key in a2:
                a2[key] = renamed_text(a2[key], rename)
        if isinstance((a2.get('reference') or {}).get('unavailable'), str):
            a2['reference'] = {'unavailable': renamed_text(a2['reference']['unavailable'], rename)}
        if 'outcome' in a2:
            a2['outcome'] = rename.get(a2['outcome'], a2['outcome'])
        if (a2.get('reference') or {}).get('figure'):
            a2['reference'] = {'figure': rename.get(a2['reference']['figure'], a2['reference']['figure'])}
        answers.append(a2)
    return {'figures': out, 'answers': answers}, rename


def run_digest(out):
    h = hashlib.sha256()
    for name in ('answers.jsonl', 'retries.jsonl', 'results.json', 'plan.json'):
        path = out / name
        h.update(name.encode() + b'\0' + (path.read_bytes() if path.exists() else b''))
    return h.hexdigest()


def card_view(calc, view_id, recorded, prefix='', ck=cc, shown=()):
    """[47b.3] One card as its own derivation: the figures its outcome and reference rest on, renumbered F1.. (after `prefix`) for this
    card alone, and the recorded assumptions about its outcome or its own figures mapped to the same numbers. [D753, council 70] It also
    shows every figure and passage the card's prose names (reasons, why, the reference's unavailability, and the basis of a shown
    figure), with what those figures rest on, so an unresolved card keeps the passages it weighed and no prose reference dangles."""
    figs = {f['id']: f for f in calc['figures']}
    refs = lambda f: list(f.get('inputs', [])) + [r for r in f.get('rests_on', []) if r in figs] + \
        ([f['adjusts']['figure']] if f.get('adjusts') else []) + ([f['bridge']] if f.get('bridge') else [])
    ans = next(a for a in calc['answers'] if a['view_id'] == view_id)
    shown = set(shown)
    own, text_passages = set(), set()
    starts = {ans.get('outcome'), (ans.get('reference') or {}).get('figure')} - {None}
    for key in ('reasons', 'why'):
        found, passages = named_in_text(ans.get(key), figs, shown)
        starts |= found
        text_passages |= passages
    found, passages = named_in_text((ans.get('reference') or {}).get('unavailable'), figs, shown)
    starts |= found
    text_passages |= passages
    while starts:                                         # the closure over figures named in the prose of figures already shown
        for start in [s for s in starts if s in figs]:
            own |= ck._upstream_of(start, figs, refs) | {start}
        starts = set()
        for fid in own:
            found, passages = named_in_text(figs[fid].get('basis_text'), figs, shown)
            starts |= found - own
            text_passages |= passages
    sub = {'figures': [f for f in calc['figures'] if f['id'] in own], 'answers': [ans]}
    norm, rename = normalise(sub, prefix)
    mapped = []
    for r in recorded:                                    # an assumption about this card's outcome, or about one of its own figures
        named = [r[k] for k in ('figure', 'bridge') if isinstance(r.get(k), str)]
        if (r.get('outcome') == view_id or any(n in rename for n in named)) and all(n in rename for n in named):
            mapped.append({k: rename[v] if k in ('figure', 'bridge') else v for k, v in r.items()})
    pushed = {p.get('evidence_id') or p.get('evidence') for p in ans.get('pushes') or [] if isinstance(p, dict)} - {None}
    return norm, mapped, sorted({f['evidence'] for f in sub['figures'] if f.get('evidence')} | set(ans.get('cites', []))
                                | {x for f in sub['figures'] for x in f.get('rests_on', []) if str(x).startswith('e')} | text_passages
                                | pushed)                     # council 70b: the passages the card weighs in its pushes


NO_ANSWER = {'not sent': 'No request was sent for this card.', 'interrupted': 'The request was started; no answer was recorded.',
             'transport': 'No answer arrived.', 'retry not sent': 'The answer was refused and its retry was not sent.'}
FORMAT_INVALID = 'The answer did not match the required format.'


def packet_units(results, items):
    """Every packet the run gives, as (unit, arm, draw) -> (decision, per-card source): the joint and singleton answers from the finals,
    the separate arm's reconciled pairs with each card's own separate answer."""
    units = {}
    for key, entry in results['finals'].items():
        unit, arm, draw = key.split('|')
        if not arm.startswith('separate-'):
            first = first_attempt(entry)                    # [47e.1] the first attempt is scored on both arms
            units[(unit, arm, draw)] = (first.get('decision'), {v: first for v in items[(unit, arm)]['members']})
    for key, entry in results['reconciled'].items():
        unit, draw = key.split('|')
        per_card = {a.split('-', 1)[1]: first_attempt(results['finals'].get(f'{unit}|{a}|{draw}', {})) for (u, a) in items
                    if u == unit and a.startswith('separate-')}
        units[(unit, 'separate', draw)] = (entry.get('decision'), per_card)
    return units


def card_lines(base, fam, v, token, data, final_label, prefix=''):
    """One card's answer as a reader sees it: the passages it names, its own figures, its recomputed outcome and assumptions, the card.
    Returns (lines, ids a ground may name)."""
    if not data:
        return [f'  {final_label}'], set()
    fmt = base.get('format')
    calc = decode(data, fmt, fam)
    try:
        checked = checker(fmt).check(fam, base['passages'], calc)
    except Exception as error:
        checked = {'errors': [('checker', str(error))], 'recorded': [], 'published': {}}
    try:
        norm, recorded, named = card_view(calc, v, checked.get('recorded', []), prefix, checker(fmt), base.get('shown', {}))
    except StopIteration:
        return ['  The answer has no card for this question.'], set()
    lines = ['  Passages, as the request showed them:\n' + '\n'.join('  ' + base['shown'].get(e, f'- {e} (not shown)') for e in named),
             '  Figures (declared):\n' + '\n'.join(f'  - {json.dumps(f, ensure_ascii=False)}' for f in norm['figures']),
             '  Recomputed outcome: ' + json.dumps((checked.get('published') or {}).get(v)),
             '  Recorded assumptions: ' + json.dumps(recorded),
             f'  Card {token}: ' + json.dumps(norm['answers'][0], ensure_ascii=False)]
    return lines, set(named) | {f['id'] for f in norm['figures']}


def packet_body(items, unit, arm, decision, per_card):
    """[47d.3, 47e.1] One scoring packet: each card's scored (first) answer only. No attempt history, no code decision and no check code,
    which would tell separate calls from one joint call; the verdict applies the code's decision itself. Returns (lines, grounds, members)."""
    base = items[(unit, 'joint' if unit.startswith('pair') else 'single')]
    grounds, lines = set(), []
    for number, v in enumerate(base['members'], 1):
        q = base['questions'][v]
        token = f'K{number}'
        grounds.add(token)
        lines.append(f'### Card {token}: {q["question"]}\n  Ladder: ' + ' / '.join(f'rung {i + 1}: {c}' for i, c in enumerate(q['ladder'])))
        source = per_card.get(v, {})                         # the scored (first) attempt of this card
        label = NO_ANSWER.get(source.get('decision'), FORMAT_INVALID if source.get('status') == 'format invalid' else NO_ANSWER['not sent'])
        fam = base['family'] if arm != 'separate' else only(base['family'], v)
        body, named = card_lines(base, fam, v, token, source.get('data'), label)
        lines += body
        grounds |= named
    lines.append('For each card answer yes or no, each with a ground that names a card (K...), passage (e...) or figure (F...) of this packet: '
                 + '; '.join(f'{k}: {t}' for k, t in QUESTIONS.items()) + '\n')
    return lines, sorted(grounds), base['members']


def key_commitment(key):
    return hashlib.sha256(json.dumps(key, sort_keys=True).encode()).hexdigest()


def render_packets(out, key):
    """The scoring packets for a key {salt, run_digest, order}: the key's salted sha256 first (so the text the readers receive commits
    to the mapping), then each packet in the key's order, rendered from the run's results and plan."""
    results = json.loads((out / 'results.json').read_text())
    items = {(i['unit'], i['arm']): i for i in json.loads((out / 'plan.json').read_text())}
    units = packet_units(results, items)
    lines, rendered = [f'Key commitment: {key_commitment(key)}', ''], {}
    for pid, unit_key in key['order']:
        decision, per_card = units[tuple(unit_key)]
        body, grounds, members = packet_body(items, unit_key[0], unit_key[1], decision, per_card)
        lines += [f'## {pid}'] + body
        rendered[pid] = {'unit': unit_key[0], 'arm': unit_key[1], 'draw': unit_key[2], 'decision': decision, 'grounds': grounds,
                         'cards': {f'K{n}': v for n, v in enumerate(members, 1)}}
    return '\n'.join(lines), rendered, units


def returned_text(raw):
    """The model's text inside a stored provider response, or the stored response itself when it cannot be read."""
    if not raw:
        return '(no text was stored)'
    try:
        message = json.loads(raw)['choices'][0]['message']
    except (ValueError, KeyError, IndexError, TypeError):
        return str(raw)
    if not isinstance(message, dict):
        return str(raw)
    if isinstance(message.get('content'), str):
        return message['content']
    if message.get('refusal'):
        return f'(the model refused: {message["refusal"]})'
    return f'(no text returned: {json.dumps(message, ensure_ascii=False)})'


def render_attempts(out, labels):
    """[47d.3, 47e.3] For diagnostic reading only, never scored: every retry and every returned text that failed the format check, each
    under its own shuffled label (D01..), with the question, that attempt's own answer (or the text returned and the passages it names),
    and no link to a packet."""
    results = json.loads((out / 'results.json').read_text())
    items = {(i['unit'], i['arm']): i for i in json.loads((out / 'plan.json').read_text())}
    lines = []
    for label, (unit, arm, draw, v, attempt) in labels:
        entry = results['finals'][f'{unit}|{arm}|{draw}']
        a = next(x for x in entry['attempts'] if x['attempt'] == attempt)
        base = items[(unit, 'joint' if unit.startswith('pair') else 'single')]
        fam = base['family'] if arm in ('joint', 'single') else only(base['family'], v)
        lines.append(f'## {label}: {base["questions"][v]["question"]}')
        if a.get('status') == 'format invalid':
            returned = returned_text(a.get('raw'))
            named = sorted(set(re.findall(r'\be\d+\b', returned)) & set(base['shown']))
            lines.append(f'  {FORMAT_INVALID} The text returned:\n' + '\n'.join('    ' + l for l in returned.splitlines()))
            if named:
                lines.append('  Passages it names, as the request showed them:\n' + '\n'.join('  ' + base['shown'][e] for e in named))
            continue
        lines += card_lines(base, fam, v, 'K1', a.get('data'), NO_ANSWER.get(a.get('decision'), NO_ANSWER['transport']), 'T.')[0]
    return '\n'.join(lines)


def packets(out, key_dir):
    if (key_dir / 'packet-key.json').exists():            # [47b.4] the inventory and key are frozen once made
        raise SystemExit(f'{key_dir / "packet-key.json"} exists: the packets are frozen; refused')
    results = json.loads((out / 'results.json').read_text())
    items = {(i['unit'], i['arm']): i for i in json.loads((out / 'plan.json').read_text())}
    rng = random.Random(secrets.randbits(64))
    unit_keys = sorted(packet_units(results, items))
    rng.shuffle(unit_keys)
    earlier = sorted((k.split('|')[0], k.split('|')[1], k.split('|')[2], v, a['attempt'])     # every retry, and every format failure
                     for k, e in results['finals'].items() for a in (e.get('attempts') or [])
                     if a['attempt'] >= 2 or a.get('status') == 'format invalid'
                     for v in items[tuple(k.split('|')[:2])]['members'])
    rng.shuffle(earlier)
    key = {'salt': secrets.token_hex(16), 'run_digest': run_digest(out), 'order': [(f'P{n:02d}', list(u)) for n, u in enumerate(unit_keys, 1)],
           'attempts': [(f'D{n:02d}', list(e)) for n, e in enumerate(earlier, 1)]}
    text = render_packets(out, key)[0]
    attempts_text = render_attempts(out, key['attempts'])          # [47f.2] both rendered before anything is written
    if (out / 'packets.md').exists() or (out / 'attempts.md').exists():
        raise SystemExit(f'{out} already holds packets; refused')
    key_dir.mkdir(parents=True, exist_ok=True)
    with open(key_dir / 'packet-key.json', 'x') as handle:
        json.dump(key, handle, indent=1)
    with open(out / 'packets.md', 'x') as handle:
        handle.write(text)
    with open(out / 'attempts.md', 'x') as handle:
        handle.write(attempts_text)
    print(f'{len(key["order"])} packets, {len(key["attempts"])} diagnostic attempts; key in {key_dir}')


def _grounded(ground, grounds):
    """[47b.4] A ground is non-empty text that names at least one card, passage or figure of the packet."""
    return isinstance(ground, str) and ground.strip() != '' and any(re.search(rf'\b{re.escape(g)}\b', ground) for g in grounds)


def final_readings(pid, cards, members, grounds=()):
    """[47.4] Two independent readings per card (A, B), each question answered yes/no with its ground; a third decides each
    disagreement. Returns ({card: {question: answer}}, problems)."""
    problems, final = [], {}
    if sorted(cards) != sorted(members):
        return None, [f'{pid}: cards {sorted(cards)} are not the unit\'s {sorted(members)}']
    for v, r in cards.items():
        final[v] = {}
        for q in QUESTIONS:
            a, b = (r.get(x, {}).get(q, {}) for x in ('A', 'B'))
            for name, x in (('A', a), ('B', b)):
                if x.get('answer') not in ('yes', 'no') or not _grounded(x.get('ground'), grounds):
                    problems.append(f'{pid} {v} {q}: reader {name} gave no yes/no with a ground from this packet')
            if a.get('answer') == b.get('answer'):
                final[v][q] = a.get('answer')
            else:
                t = r.get('third', {}).get(q, {})
                if t.get('answer') not in ('yes', 'no') or not _grounded(t.get('ground'), grounds):
                    problems.append(f'{pid} {v} {q}: the readers disagree and no third reading decides')
                final[v][q] = t.get('answer')
    return final, problems


def verdict(out, readings_path, key_dir):
    """[47e.4] Seal the readings into the run (readings.json, created once), compute D725's lines once and write verdict.json bound to
    the readings, the key and the packets. A second verdict on the run is refused; `replay` recomputes and compares."""
    if (out / 'verdict.json').exists() or (out / 'readings.json').exists():
        raise SystemExit(f'{out} already has sealed readings or a verdict; refused (use replay)')
    data = Path(readings_path).read_bytes()
    with open(out / 'readings.json', 'xb') as handle:
        handle.write(data)
    summary = score(out, key_dir)
    frozen = json.loads((key_dir / 'packet-key.json').read_text())
    record = {'readings_sha256': hashlib.sha256(data).hexdigest(), 'key_commitment': key_commitment(frozen),
              'packets_sha256': hashlib.sha256((out / 'packets.md').read_bytes()).hexdigest() if (out / 'packets.md').exists() else None,
              'run_digest': run_digest(out), 'summary': summary}
    with open(out / 'verdict.json', 'x') as handle:
        json.dump(record, handle, indent=1)
    return summary


def replay(out, key_dir):
    """Recompute the verdict from the sealed readings and compare it with verdict.json."""
    record = json.loads((out / 'verdict.json').read_text())
    data = (out / 'readings.json').read_bytes()
    same = (hashlib.sha256(data).hexdigest() == record['readings_sha256'] and record['run_digest'] == run_digest(out)
            and record['key_commitment'] == key_commitment(json.loads((key_dir / 'packet-key.json').read_text())))
    summary = score(out, key_dir)
    matches = same and summary == record['summary']
    print(json.dumps({'reproduced': matches}, indent=1))
    return matches


def score(out, key_dir):
    """D725's registered lines on the sealed readings, bound to this run."""
    frozen = json.loads((key_dir / 'packet-key.json').read_text())
    submitted = json.loads((out / 'readings.json').read_text())
    problems = [] if frozen.get('run_digest') == run_digest(out) else ['the packet key does not belong to this run']   # [47b.4]
    text, key, units = render_packets(out, frozen)                  # [47c.2] every packet rendered again from the run
    if sorted(tuple(u) for _, u in frozen['order']) != sorted(units):
        problems.append('the key does not map one packet to each unit of the run')
    sha = hashlib.sha256(text.encode()).hexdigest()
    packets_path = out / 'packets.md'
    written = packets_path.read_text() if packets_path.exists() else ''
    if not written.startswith(f'Key commitment: {key_commitment(frozen)}\n'):      # [47d.1] the mapping the readers' text committed to
        problems.append('the key is not the one packets.md committed to')
    if hashlib.sha256(written.encode()).hexdigest() != sha:
        problems.append('packets.md is not the text the run and the key give')
    if submitted.get('packets_sha256') != sha:
        problems.append('the readings were not made on the frozen packets')
    readings = submitted.get('packets', {})
    results = json.loads((out / 'results.json').read_text())
    problems += [f'answers.jsonl line {d["line"]} is damaged' for d in results.get('damaged', [])
                 if d.get('journal') == 'answers.jsonl']                     # [47g] a damaged retry record stays diagnostic
    scored = {k: first_attempt(v)['decision'] for k, v in results['finals'].items()}            # [47f.1] completeness from the scored attempts
    problems += [f'{k}: {d}' for k, d in scored.items() if d not in ('publish', 'held', 'refused')]               # [47b.2] from the records
    problems += [f'{pid}: not read' for pid in key if pid not in readings] + [f'{pid}: not a packet' for pid in readings if pid not in key]
    usable_pairs = {'joint': {}, 'separate': {}}
    defects = []
    for pid, k in key.items():
        if pid not in readings:
            continue
        final, probs = final_readings(pid, readings[pid], list(k['cards']), k['grounds'])
        problems += probs
        if final is None:
            continue
        if k['decision'] == 'publish' and k['arm'] in ('joint', 'single'):      # D725: defects across the joint and singleton answers
            for v, r in final.items():
                if 'yes' in (r['contradiction'], r['internal_reference'], r['deciding_gap']):
                    defects.append((pid, k['unit'], k['arm'], k['cards'][v]))
        if k['unit'].startswith('pair') and k['arm'] in usable_pairs:
            usable_pairs[k['arm']].setdefault(k['unit'], []).append(k['decision'] == 'publish' and all(r['usable'] == 'yes' for r in final.values()))
    joint_total = sum(sum(v) for v in usable_pairs['joint'].values())
    separate_total = sum(sum(v) for v in usable_pairs['separate'].values())
    per_snapshot = {u: sum(v) for u, v in usable_pairs['joint'].items()}
    complete = (not problems and len(key) == 27 and len(usable_pairs['joint']) == 3 and len(usable_pairs['separate']) == 3
                and all(len(v) == 3 for arm in usable_pairs.values() for v in arm.values()))
    passes = complete and not defects and joint_total >= 8 and all(n >= 2 for n in per_snapshot.values()) and joint_total - separate_total >= 3
    summary = {'complete': complete, 'problems': problems[:20], 'joint usable pairs': joint_total, 'separate usable pairs': separate_total,
               'joint per snapshot': per_snapshot, 'published defects': defects,
               'verdict': 'PASS' if passes else ('INCOMPLETE' if not complete else 'STOP')}
    print(json.dumps(summary, indent=1))
    return summary


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'plan' and len(sys.argv) == 3:
        plan(sys.argv[2])
    elif cmd == 'plan-v13s' and len(sys.argv) == 3:                     # D737: the small format's plan, $0
        plan(sys.argv[2], 'v13s')
    elif cmd == 'send' and len(sys.argv) == 5 and not sys.argv[2].startswith('-'):
        send(Path(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
    elif cmd == 'packets' and len(sys.argv) == 4:
        packets(Path(sys.argv[2]), Path(sys.argv[3]))
    elif cmd == 'recover' and len(sys.argv) == 3:
        recover(Path(sys.argv[2]))
    elif cmd == 'verdict' and len(sys.argv) == 5:
        verdict(Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4]))
    elif cmd == 'replay' and len(sys.argv) == 4:
        replay(Path(sys.argv[2]), Path(sys.argv[3]))
    else:
        raise SystemExit(__doc__)
