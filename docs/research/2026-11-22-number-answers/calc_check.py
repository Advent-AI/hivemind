"""judging-v13's calculation checks (DESIGN.md v5, harness-only). Code owns identity and arithmetic, never importance.

check(family, passages, calc) -> {'errors': [(code, detail)], 'recorded': [...]}
- family: {'members': {view_id: {'what': {...}, 'bands': [[lo, hi], ...]}}, 'relations': [{'type': 'part_of'|'same_base', ...}],
           'shared': [what, ...], 'compare_periods': [period, ...]}
- passages: {evidence_id: {'text': str, 'speaker': str}}
- calc: {'figures': [...], 'answers': [...]}, the format of DESIGN.md §2.
Values are in the figure's unit; money is normalised to 'USD bn'.
"""
import re

QUAL = {'more than': '>', 'over': '>', 'at least': '>=', 'nearly': 'approx_below', 'almost': 'approx_below',
        'approximately': 'approx', 'about': 'approx', 'around': 'approx', 'roughly': 'approx',
        'up to': '<=', 'less than': '<', 'below': '<', 'under': '<'}
SCALE = {'trillion': 1000.0, 'tn': 1000.0, 't': 1000.0, 'billion': 1.0, 'bn': 1.0, 'b': 1.0, 'million': 0.001, 'm': 0.001}
NUM = r'(\d[\d,]*(?:\.\d+)?)'
UNIT = r'(trillion|billion|million|bn|tn|T|B|M)\b'
QWORDS = '|'.join(sorted(QUAL, key=len, reverse=True))
PATTERNS = [
    ('relative', re.compile(r'\$\s?' + NUM + r'\s*' + UNIT + r',?\s*(?:plus or minus|±)\s*' + NUM + r'%')),
    ('range', re.compile(r'\$\s?' + NUM + r'\s*(?:' + UNIT + r')?\s*(?:–|-)\s*\$?\s?' + NUM + r'\s*' + UNIT)),   # "to" is ambiguous ("from $253 billion to $392 billion")
    ('range', re.compile(r'\bbetween\s+\$\s?' + NUM + r'\s*(?:' + UNIT + r')?\s+and\s+\$?\s?' + NUM + r'\s*' + UNIT, re.I)),
    ('qualified', re.compile(r'\b(' + QWORDS + r')\s+\$\s?' + NUM + r'\s*' + UNIT, re.I)),
    ('money', re.compile(r'\$\s?' + NUM + r'\s*' + UNIT)),
    ('money_plain', re.compile(r'\$\s?' + NUM + r'(?![\d,.]*\s*(?:trillion|billion|million|bn|tn|T|B|M)\b)')),
    ('multiplier', re.compile(r'\b(more than\s+)?(double|triple)\b', re.I)),
    ('percent', re.compile(r'\b(?:(' + QWORDS + r')\s+)?' + NUM + r'%', re.I)),
]
OPERATIONS = {'sum', 'difference', 'product', 'ratio', 'growth', 'apply_growth', 'share', 'range_from_relative', 'roll_forward'}
ARITY = {'difference': (2, 2), 'ratio': (2, 2), 'growth': (2, 2), 'apply_growth': (2, 2), 'share': (2, 2), 'range_from_relative': (2, 2),
         'product': (2, 99), 'sum': (1, 99), 'roll_forward': (2, 99)}          # [46m.1] every operand an operation lists is one it uses
KINDS = {'source', 'computed', 'estimate', 'prior'}
BASES = {'reported', 'guidance', 'consensus', 'third_party', 'forecast', 'prior_forecast'}
EXTERNAL = {'consensus', 'guidance', 'third_party'}


def _num(text):
    return float(text.replace(',', ''))


def _scale(unit):
    return SCALE[unit.lower()] if unit else 1.0


def extract(text):
    """Every complete numeric expression in a passage, longest forms first, never overlapping: [{'text', 'form', ...}]."""
    taken, found = [], []
    for form, pattern in PATTERNS:
        for m in pattern.finditer(text):
            if any(m.start() < end and start < m.end() for start, end in taken):
                continue
            taken.append((m.start(), m.end()))
            g = m.groups()
            item = {'text': m.group(0), 'form': form, 'start': m.start()}
            if form == 'relative':
                item.update(midpoint=_num(g[0]) * _scale(g[1]), relative=_num(g[2]), unit='USD bn')
            elif form == 'range':
                unit = g[3]
                item.update(low=_num(g[0]) * _scale(g[1] or unit), high=_num(g[2]) * _scale(unit), unit='USD bn')
            elif form == 'qualified':
                item.update(bound=QUAL[g[0].lower()], value=_num(g[1]) * _scale(g[2]), unit='USD bn')
            elif form == 'money':
                item.update(value=_num(g[0]) * _scale(g[1]), unit='USD bn')
            elif form == 'money_plain':
                item.update(value=_num(g[0]), unit='USD')
            elif form == 'multiplier':
                item.update(multiplier=2.0 if g[1].lower() == 'double' else 3.0, bound='>' if g[0] else None, unit='x')
            elif form == 'percent':
                item.update(value=_num(g[1]), bound=QUAL[g[0].lower()] if g[0] else None, unit='%')
            found.append(item)
    return sorted(found, key=lambda item: item['start'])


def _same(a, b):
    return a is not None and b is not None and abs(a - b) <= 1e-9 * max(1.0, abs(b))


def _source_errors(fig, passages):
    passage = passages.get(fig.get('evidence'))
    if passage is None:
        return [('C1', f'{fig["id"]}: evidence {fig.get("evidence")} was not shown')]
    matches = [e for e in extract(passage['text']) if e['text'] == fig.get('expression')]
    if not matches:
        return [('C1', f'{fig["id"]}: "{fig.get("expression")}" is not a complete numeric expression of {fig["evidence"]}')]
    expr, comp = matches[0], fig.get('component', 'value')
    bound, unit = fig.get('bound'), fig.get('unit')
    ok = False
    if comp == 'value' and expr['form'] in ('money', 'money_plain', 'percent'):
        ok = _same(fig.get('value'), expr['value']) and unit == expr['unit'] and bound == expr.get('bound')
    elif comp == 'bound' and expr['form'] in ('qualified', 'percent'):
        ok = _same(fig.get('value'), expr['value']) and unit == expr['unit'] and bound == expr['bound'] and bound is not None
    elif comp == 'midpoint' and expr['form'] == 'relative':
        ok = _same(fig.get('value'), expr['midpoint']) and unit == 'USD bn' and bound is None
    elif comp == 'relative' and expr['form'] == 'relative':
        ok = _same(fig.get('value'), expr['relative']) and unit == '%' and bound is None
    elif comp in ('low', 'high') and expr['form'] == 'range':
        ok = _same(fig.get('value'), expr[comp]) and unit == 'USD bn' and bound is None
    elif comp == 'multiplier' and expr['form'] == 'multiplier':
        ok = _same(fig.get('value'), expr['multiplier']) and unit == 'x' and bound == expr['bound']
    if not ok:
        return [('C1', f'{fig["id"]}: value {fig.get("value")} {unit} bound {bound} does not equal "{expr["text"]}" as component {comp}')]
    return []


def _interval(fig):
    if 'low' in fig and 'high' in fig:
        return fig['low'], fig['high']
    return fig['value'], fig['value']


def _terms(fig):
    """[46w] The operands a calculation uses, with a sum's or roll_forward's repeated operands netted (x - x cancels exactly)."""
    ids = list(fig.get('inputs', []))
    if fig.get('operation') == 'difference' and len(ids) == 2 and ids[0] == ids[1]:
        return [], []                                 # [46x.2] x - x is exactly zero
    if fig.get('operation') not in ('sum', 'roll_forward'):
        return ids, fig.get('signs')
    net = {}
    for i, k in zip(ids, fig.get('signs') or [1] * len(ids)):
        net[i] = net.get(i, 0) + k
    kept = [i for i in dict.fromkeys(ids) if net[i] != 0]
    return kept, [net[i] for i in kept]


def _compute(op, inputs, signs, out_unit=None):
    """inputs: [(lo, hi, unit)]; returns (lo, hi) in out_unit."""
    los = [i[0] for i in inputs]
    his = [i[1] for i in inputs]
    if op in ('sum', 'roll_forward'):
        s = signs or [1] * len(inputs)
        return (sum((a if k > 0 else b) * k for a, b, k in zip(los, his, s)), sum((b if k > 0 else a) * k for a, b, k in zip(los, his, s)))
    if op == 'difference':
        return los[0] - his[1], his[0] - los[1]
    if op == 'product':
        lo = hi = 1.0
        for a, b in zip(los, his):
            lo, hi = lo * a, hi * b
        units = [i[2] for i in inputs]
        if 'units' in units and 'USD' in units and out_unit == 'USD bn':     # units times a dollar price, in billions
            lo, hi = lo / 1e9, hi / 1e9
        return lo, hi
    if op == 'ratio':
        units = [i[2] for i in inputs]
        if 'USD' in units and 'USD bn' in units:                # a dollar total over a per-unit price
            los = [x * 1e9 if u == 'USD bn' else x for x, u in zip(los, units)]
            his = [x * 1e9 if u == 'USD bn' else x for x, u in zip(his, units)]
        return los[0] / his[1], his[0] / los[1]
    if op == 'share':
        return los[0] * los[1] / 100.0, his[0] * his[1] / 100.0
    if op == 'growth':
        return (los[1] / his[0] - 1) * 100.0, (his[1] / los[0] - 1) * 100.0
    if op == 'apply_growth':
        return los[0] * (1 + los[1] / 100.0), his[0] * (1 + his[1] / 100.0)
    if op == 'range_from_relative':
        return los[0] * (1 - los[1] / 100.0), his[0] * (1 + his[1] / 100.0)
    raise ValueError(op)


DIRECTION = {'>': 'lower', '>=': 'lower', 'approx_above': 'lower', '<': 'upper', '<=': 'upper', 'approx_below': 'upper',
             'approx': 'two-sided', 'mixed': 'mixed', None: None}
FLIP = {'lower': 'upper', 'upper': 'lower', 'two-sided': 'two-sided', 'mixed': 'mixed', None: None}


def _bound_direction(op, ins, signs=None):
    """For positive operands: which side the result is bounded on, from its inputs' bounds (None: a point). [46u.2] A term a sum or
    roll_forward subtracts flips its side."""
    dirs = [DIRECTION.get(i.get('bound')) for i in ins]
    if op in ('sum', 'roll_forward') and signs:
        dirs = [FLIP[d] if k < 0 else d for d, k in zip(dirs, signs)]
    if op == 'ratio' and len(dirs) == 2:
        dirs = [dirs[0], FLIP[dirs[1]]]
    if op == 'difference' and len(dirs) == 2:
        dirs = [dirs[0], FLIP[dirs[1]]]
    found = {d for d in dirs if d}
    if not found:
        return None
    if 'mixed' in found or {'lower', 'upper'} <= found:     # [46v] opposing bounds leave the result unbounded
        return 'mixed'
    return found.pop() if len(found) == 1 and 'two-sided' not in found else 'two-sided'


def _outcome_set(fig):
    """The values an outcome allows: (low, low_closed, high, high_closed); a bound keeps its side open or closed."""
    lo, hi = _interval(fig)
    b = fig.get('bound')
    inf = float('inf')
    if b == '>':
        return (lo, False, inf, False)
    if b in ('>=', 'approx_above'):
        return (lo, True, inf, False)
    if b == '<':
        return (-inf, False, hi, False)
    if b in ('<=', 'approx_below'):
        return (-inf, False, hi, True)
    if b == 'mixed':                                    # [46v] any value: only possible crossings
        return (-inf, False, inf, False)
    return (lo, True, hi, True)


def _overlaps(values, band):
    """A band [low, high) (None: open-ended) shares at least one value with the outcome's set."""
    lo, lo_c, hi, hi_c = values
    b_lo = band[0] if band[0] is not None else float('-inf')
    b_hi = band[1] if band[1] is not None else float('inf')
    low, low_closed = (lo, lo_c) if lo > b_lo else ((b_lo, True) if b_lo > lo else (lo, lo_c))
    high, high_closed = (hi, hi_c) if hi < b_hi else ((b_hi, False) if b_hi < hi else (hi, False))
    return low < high or (low == high and low_closed and high_closed)


def _exceeds(part, whole):
    """[46t.2] With a bound on either side, the part exceeds its whole only when no pair of allowed values fits (part min above whole
    max). Closed ranges and points keep the paired-end rule (each end of the part at most the same end of the whole)."""
    (plo, plc, phi, phc), (wlo, wlc, whi, whc) = part, whole
    inf = float('inf')
    if inf in (abs(plo), abs(phi), abs(wlo), abs(whi)):
        return plo > whi + 1e-9 or (abs(plo - whi) <= 1e-9 and not (plc and whc))
    return plo > wlo + 1e-9 or phi > whi + 1e-9


def _below(values, edge):
    lo, lo_c, hi, hi_c = values
    return hi < edge or (hi == edge and not hi_c)


def _at_or_above(values, edge):
    lo, lo_c, hi, hi_c = values
    return lo >= edge


def _crossings(base, alt, bands):
    """Band edges between two value sets, each with its own certainty: definite when one set lies wholly below the edge and the other
    wholly at or above it; possible when the sets differ and the edge lies within their span."""
    edges = sorted({e for band in bands for e in band if e is not None})
    definite = [e for e in edges if (_below(base, e) and _at_or_above(alt, e)) or (_below(alt, e) and _at_or_above(base, e))]
    span_lo, span_hi = min(base[0], alt[0]), max(base[2], alt[2])
    possible = [e for e in edges if e not in definite and span_lo < e <= span_hi and base != alt]
    return definite, possible


STRICT = {'>', '<'}


def _evaluate_bounded(figs, refs, overrides):
    """[46t.1] Recompute (interval, bound) for every figure, carrying open and closed bounds through the arithmetic."""
    values, order, done = {}, [], set()

    def visit(fid):
        if fid in done:
            return
        done.add(fid)
        for r in refs(figs[fid]):
            if r in figs:
                visit(r)
        order.append(fid)
    for fid in figs:
        visit(fid)
    for fid in order:
        fig = figs[fid]
        if fid in overrides:
            values[fid] = overrides[fid]
        elif fig['kind'] == 'computed' and fig.get('operation') in OPERATIONS:
            t_ids, t_signs = _terms(fig)
            ins = [values[i] for i in t_ids]
            interval = _compute(fig['operation'], [iv + (figs[i]['unit'],) for (iv, _), i in zip(ins, t_ids)], t_signs, fig['unit']) if ins else (0.0, 0.0)
            pseudo = [{'bound': b} for _, b in ins]
            side = _bound_direction(fig['operation'], pseudo, t_signs)
            strict = any(b in STRICT for _, b in ins)
            bound = {'lower': '>' if strict else '>=', 'upper': '<' if strict else '<=', 'two-sided': 'approx', 'mixed': 'mixed', None: None}[side]
            values[fid] = (interval, bound)
        else:
            values[fid] = (_interval(fig), fig.get('bound'))
    return values


def _set_from(interval, bound):
    fig = {'low': interval[0], 'high': interval[1], 'bound': bound} if interval[0] != interval[1] else {'value': interval[0], 'bound': bound}
    return _outcome_set(fig)


def _close(declared, expected, unit):
    floor = 0.05 if unit == '%' else 0.1
    return abs(declared - expected) <= max(0.005 * abs(expected), floor)


QUARTERS = {'Q1': {1}, 'Q2': {2}, 'Q3': {3}, 'Q4': {4}, 'H1': {1, 2}, 'H2': {3, 4}}


def _quarters(period):
    """'FY2027' -> (FY2027, {1..4}); 'FY2027 Q3' -> (FY2027, {3}); 'FY2027 H1' -> {1, 2}; else None."""
    parts = period.split()
    if len(parts) == 1 and parts[0].startswith('FY'):
        return parts[0], {1, 2, 3, 4}
    if len(parts) == 2 and parts[0].startswith('FY') and parts[1] in QUARTERS:
        return parts[0], QUARTERS[parts[1]]
    return None


def _key(what):
    return (what['population'], what['measure'], what['scope'], what['period'])


def check(family, passages, calc):
    errors, recorded = [], []
    figs = {}
    for fig in calc['figures']:
        if fig['id'] in figs:
            errors.append(('C7', f'{fig["id"]} is defined twice'))
        figs[fig['id']] = fig

    def refs(fig):
        out = list(fig.get('inputs', []))
        out += [r for r in fig.get('rests_on', []) if r in figs or r not in passages]
        if fig.get('adjusts'):
            out.append(fig['adjusts']['figure'])
        if fig.get('bridge'):
            out.append(fig['bridge'])
        return out

    # C7 structure: kinds, operations, dangling, cycles, numbers
    for fig in figs.values():
        has_value = isinstance(fig.get('value'), (int, float))
        has_range = isinstance(fig.get('low'), (int, float)) and isinstance(fig.get('high'), (int, float))
        if has_value == has_range or (has_range and fig['low'] > fig['high']):          # [46o.2] exactly one: a value or an ordered range
            errors.append(('C7', f'{fig["id"]}: a figure needs either a value or a complete range with low at most high'))
        if fig.get('kind') not in KINDS or fig.get('basis') not in BASES:
            errors.append(('C7', f'{fig["id"]}: kind {fig.get("kind")} or basis {fig.get("basis")} outside the closed set'))
        if fig.get('kind') == 'computed' and fig.get('operation') not in OPERATIONS:
            errors.append(('C7', f'{fig["id"]}: operation {fig.get("operation")} outside the closed set'))
        elif fig.get('kind') == 'computed':
            lo_n, hi_n = ARITY[fig['operation']]
            if not lo_n <= len(fig.get('inputs', [])) <= hi_n:
                errors.append(('C7', f'{fig["id"]}: {fig["operation"]} takes {lo_n}' + (f' to {hi_n}' if hi_n != lo_n else '')
                                     + f' operands, not {len(fig.get("inputs", []))}'))
            signs = fig.get('signs')
            if signs is not None and (fig['operation'] not in ('sum', 'roll_forward') or len(signs) != len(fig.get('inputs', []))
                                      or any(x not in (1, -1) for x in signs)):
                errors.append(('C7', f'{fig["id"]}: signs must give one +1 or -1 per operand of a sum or roll_forward'))   # [46n]
        for r in refs(fig):
            if r not in figs:
                errors.append(('C7', f'{fig["id"]} refers to {r}, which is not defined'))
    state = {}

    def cyclic(fid):
        if state.get(fid) == 1:
            return True
        if state.get(fid) == 2 or fid not in figs:
            return False
        state[fid] = 1
        hit = any(cyclic(r) for r in refs(figs[fid]))
        state[fid] = 2
        return hit
    if any(cyclic(fid) for fid in figs):
        errors.append(('C7', 'the figure graph has a cycle'))
    if errors:                                         # [46n] a malformed calculation is refused before any arithmetic
        return {'errors': errors, 'recorded': recorded}

    # C1 sources, prior pointers
    for fig in figs.values():
        if fig['kind'] == 'source':
            errors += _source_errors(fig, passages)
        if fig['kind'] == 'prior' and not fig.get('pointer'):
            errors.append(('C7', f'{fig["id"]}: a prior forecast needs an exact pointer to an earlier answer shown in the request'))

    try:
        return _check_after_structure(family, passages, calc, figs, refs, errors, recorded, reachable_factory=None)
    except (ZeroDivisionError, OverflowError, ValueError) as error:          # [47.3] an arithmetic failure is a refusal, never a crash
        errors.append(('C2', f'the calculation cannot be evaluated: {type(error).__name__}: {error}'))
        return {'errors': errors, 'recorded': recorded}


def _check_after_structure(family, passages, calc, figs, refs, errors, recorded, reachable_factory=None):
    # C2 arithmetic and bound propagation
    for fig in figs.values():
        if fig['kind'] != 'computed' or fig.get('operation') not in OPERATIONS:
            continue
        t_ids, t_signs = _terms(fig)
        ins = [figs[i] for i in t_ids if i in figs]
        expected = _compute(fig['operation'], [_interval(i) + (i['unit'],) for i in ins], t_signs, fig['unit']) if ins else (0.0, 0.0)   # [46x.2]
        lo, hi = _interval(fig)
        if not ins and (lo != 0 or hi != 0):              # [46y.2] an algebraic zero is exactly zero
            errors.append(('C2', f'{fig["id"]}: its operands cancel exactly, so it is 0, not {lo}–{hi}'))
            continue
        if fig['operation'] == 'range_from_relative' or ('low' in fig):
            ok = _close(lo, expected[0], fig['unit']) and _close(hi, expected[1], fig['unit'])
        else:
            ok = _close(lo, (expected[0] + expected[1]) / 2, fig['unit'])
        if not ok:
            errors.append(('C2', f'{fig["id"]}: declared {lo}–{hi} but {fig["operation"]} of {fig["inputs"]} gives {expected[0]:.2f}–{expected[1]:.2f}'))
        want = _bound_direction(fig['operation'], ins, t_signs)
        have = DIRECTION.get(fig.get('bound'))
        if want == 'mixed':
            errors.append(('C2', f'{fig["id"]}: its inputs are bounded on opposite sides, so its value is unbounded; state it as an estimate'))
        elif want is not None and have != want:
            errors.append(('C2', f'{fig["id"]}: its inputs make it a {want} bound, but it is declared {fig.get("bound") or "a point"}'))
        elif want is None and fig.get('bound'):
            errors.append(('C2', f'{fig["id"]}: its inputs are points, but it is declared a bound ({fig["bound"]})'))

    # C8 operand compatibility
    for fig in figs.values():
        if fig['kind'] != 'computed' or fig.get('operation') not in OPERATIONS:
            continue
        ins = [figs[i] for i in fig['inputs'] if i in figs]
        op, rel, out = fig['operation'], fig.get('relation'), fig['what']
        differing = [i['id'] for i in ins if i['unit'] not in ('%', 'x') and
                     (i['what']['population'], i['what']['scope'], i['what']['period'], i['what']['measure']) !=
                     (out['population'], out['scope'], out['period'], out['measure'])]
        if op in ('sum', 'difference'):
            money = [i for i in ins if i['unit'] not in ('%', 'x')]
            same_qty = all((i['what']['population'], i['what']['measure'], i['what']['scope']) ==
                           (out['population'], out['measure'], out['scope']) for i in money)
            if rel == 'time_aggregation':
                qs = [_quarters(i['what']['period']) for i in money]
                q_out = _quarters(out['period'])
                union = set().union(*[q[1] for q in qs]) if all(qs) else None
                disjoint = all(qs) and sum(len(q[1]) for q in qs) == len(union or ())
                if not (same_qty and q_out and all(qs) and disjoint and union == q_out[1] and all(q[0] == q_out[0] for q in qs)):
                    errors.append(('C8', f'{fig["id"]}: time aggregation needs one quantity over disjoint periods forming {out["period"]}'))
            elif rel in ('overlap_unknown', 'stated_in_addition'):
                if rel == 'overlap_unknown' and fig.get('disputed') not in fig['inputs']:
                    errors.append(('C8', f'{fig["id"]}: overlap_unknown must name a disputed operand among its inputs'))
            elif rel == 'accounting_parts':
                wholes = {(r['whole_scope'], tuple(r['part_scopes'])) for r in family.get('scope_parts', [])}
                if not any(out['scope'] == w and all(i['what']['scope'] in p for i in money) for w, p in wholes):
                    errors.append(('C8', f'{fig["id"]}: accounting_parts needs a declared split of {out["scope"]}'))
            elif differing:
                errors.append(('C8', f'{fig["id"]}: {op} of different quantities or periods ({", ".join(differing)}) states no relation'))
        elif op == 'roll_forward':
            opening = ins[0]['what']['period'] if ins else ''
            if not (opening.startswith('as of') and all(not i['what']['period'].startswith('as of') for i in ins[1:])
                    and out['period'].startswith(('as of', 'end of'))):
                errors.append(('C8', f'{fig["id"]}: roll_forward needs an opening balance as of a date, flows after it, and a closing balance'))
            if rel == 'overlap_unknown' and fig.get('disputed') not in fig['inputs']:
                errors.append(('C8', f'{fig["id"]}: overlap_unknown must name a disputed operand among its inputs'))
        elif op == 'share':
            pct = [i for i in ins if i['unit'] == '%']
            if len(pct) != 1:
                errors.append(('C8', f'{fig["id"]}: a share needs one share figure and one whole'))
        elif op == 'apply_growth' and any(r['type'] == 'same_base' for r in family.get('relations', [])) and \
                all(i['unit'] == '%' or i['what']['scope'] == out['scope'] for i in ins):
            pass
        elif op in ('range_from_relative', 'growth'):
            pass
        elif op in ('ratio', 'product') and _per_unit(op, ins, fig):
            pass                                   # a total over a per-unit price gives units; units times the price give the total
        elif op == 'product' and any(i['unit'] == 'x' for i in ins) and all(
                i['unit'] == 'x' or (i['what']['population'], i['what']['measure'], i['what']['scope']) ==
                (out['population'], out['measure'], out['scope']) for i in ins):
            pass                                   # a multiplier the source states between periods is its own bridge
        elif differing:
            bridge = figs.get(fig.get('bridge'))
            if not bridge or bridge['kind'] != 'estimate' or set(bridge.get('converts', [])) != set(differing):
                errors.append(('C8', f'{fig["id"]}: converts {", ".join(differing)} to {out["population"]} {out["scope"]} {out["period"]} '
                                     f'{out["measure"]} with no bridge naming those operands'))
            else:
                recorded.append({'type': 'bridge', 'figure': fig['id'], 'bridge': bridge['id'], 'alternate': 'undetermined'})

    # [46z.2] one recomputed result: every computed figure takes its recomputed value and bound for every later check and for publication
    recomputed = _evaluate_bounded(figs, refs, {})
    for fid, fig in list(figs.items()):
        if fig['kind'] == 'computed' and fig.get('operation') in OPERATIONS:
            (lo_r, hi_r), b_r = recomputed[fid]
            canon = {k: v for k, v in fig.items() if k not in ('value', 'low', 'high', 'bound')}
            canon.update({'value': lo_r} if lo_r == hi_r else {'low': lo_r, 'high': hi_r})
            if b_r:
                canon['bound'] = b_r
            figs[fid] = canon

    # answers: C7 coverage and ownership, C6 rung, C5 reference
    members = family['members']
    seen = {}
    for ans in calc['answers']:
        seen[ans['view_id']] = seen.get(ans['view_id'], 0) + 1
    for view_id in members:
        if seen.get(view_id, 0) != 1:
            errors.append(('C7', f'{view_id} has {seen.get(view_id, 0)} answers; exactly one is required'))
    for view_id in seen:
        if view_id not in members:
            errors.append(('C7', f'{view_id} is not a member of the family'))
    outcomes = {}
    for ans in calc['answers']:
        member = members.get(ans['view_id'])
        if member is None:
            continue
        if ans.get('shape') == 'unresolved':
            if 'outcome' in ans or 'rung' in ans or not ans.get('why'):
                errors.append(('C7', f'{ans["view_id"]}: an unresolved answer has a reason and neither outcome nor rung'))
            continue
        out = figs.get(ans.get('outcome'))
        if out is None:
            errors.append(('C7', f'{ans["view_id"]}: outcome {ans.get("outcome")} is not a figure'))
            continue
        if _key(out['what']) != _key(member['what']):
            errors.append(('C7', f'{ans["view_id"]}: outcome {out["id"]} measures {_key(out["what"])}, not the question\'s {_key(member["what"])}'))
        outcomes[ans['view_id']] = out['id']
        rung = ans.get('rung')
        if not isinstance(rung, int) or isinstance(rung, bool) or not 1 <= rung <= len(member['bands']):   # [46q] before any lookup
            errors.append(('C6', f'{ans["view_id"]}: rung {rung!r} is not one of 1..{len(member["bands"])}'))
            continue
        band = member['bands'][rung - 1]
        shown = _outcome_set(out)                         # [46y.2, 46z.2] the recomputed value for a computed outcome
        if not _overlaps(shown, band):                    # [46r] open and closed ends kept
            errors.append(('C6', f'{ans["view_id"]}: rung {rung} ({band}) contains no part of its outcome {shown}'))
        ref = ans.get('reference') or {}
        if ('figure' in ref) == ('unavailable' in ref):          # [46g.2] exactly one choice
            errors.append(('C5', f'{ans["view_id"]}: the reference must name exactly one of a figure or unavailable'))
        elif 'unavailable' in ref:
            if not ref['unavailable']:
                errors.append(('C5', f'{ans["view_id"]}: an unavailable reference needs a reason'))
        else:
            errors += _reference_errors(ans['view_id'], figs.get(ref.get('figure')), figs, passages, refs)

    # [46j.1] scenario membership derived from the estimates a figure rests on; related members cover the same scenarios
    def scen(fid):
        return figs[fid].get('scenario', 'base')

    def derived(fid):
        return {scen(g) for g in _upstream_of(fid, figs, refs) | {fid} if figs[g]['kind'] == 'estimate' and scen(g) != 'range'}
    for f in figs.values():
        sc = f.get('scenario', 'base')
        if sc == 'range' or f['kind'] not in ('computed', 'estimate'):
            continue
        other = derived(f['id']) - {sc}
        if other:
            errors.append(('C4', f'{f["id"]} ({sc}) rests on estimates of another scenario ({", ".join(sorted(other))})'))
    for rel in family.get('relations', []):
        if rel['type'] == 'part_of' and rel['part'] in outcomes and rel['whole'] in outcomes:
            sp, sw = derived(outcomes[rel['part']]), derived(outcomes[rel['whole']])
            if sp != sw:
                errors.append(('C4', f'{rel["part"]} covers scenarios {sorted(sp)} but {rel["whole"]} covers {sorted(sw)}; related members cover the same'))

    # [46i.1] a range summary is an estimate with low and high, is an answer's outcome, and no figure reads it
    outcome_ids = {a.get('outcome') for a in calc['answers']}
    for f in figs.values():
        if f.get('scenario') != 'range':
            continue
        readers = [g['id'] for g in figs.values() if f['id'] in refs(g)]
        if f['kind'] != 'estimate' or 'low' not in f or 'high' not in f or f['id'] not in outcome_ids or readers:
            errors.append(('C4', f'{f["id"]}: a range summary must be an estimate with low and high that is an answer\'s outcome and feeds no figure'
                                 + (f' (read by {", ".join(readers)})' if readers else '')))

    # C3 part within whole, C4 one forecast per shared quantity (every path)
    def reachable(start, stop=None):
        stops = set(stop) if isinstance(stop, (set, list, tuple)) else {stop}
        seen_ids, stack = set(), [start]
        while stack:
            fid = stack.pop()
            if fid in seen_ids or fid not in figs:
                continue
            seen_ids.add(fid)
            if fid not in stops:
                stack.extend(refs(figs[fid]))
        return seen_ids
    scenarios = {f.get('scenario', 'base') for f in figs.values() if f['basis'] == 'forecast'} or {'base'}
    for rel in family.get('relations', []):
        if rel['type'] != 'part_of' or rel['part'] not in outcomes or rel['whole'] not in outcomes:
            continue
        part_m, whole_m = members[rel['part']], members[rel['whole']]
        for sc in scenarios:
            for period in family.get('compare_periods', []):
                def node(view_id, member):
                    want = (member['what']['population'], member['what']['measure'], member['what']['scope'], period)
                    hits = sorted((figs[f] for f in reachable(outcomes[view_id]) if _key(figs[f]['what']) == want
                                   and figs[f]['basis'] == 'forecast' and figs[f].get('scenario', 'base') == sc), key=lambda f: f['id'])
                    if len(hits) > 1:                 # [46x.1] one forecast per member quantity, period and scenario
                        errors.append(('C3', f'{period} {sc}: {view_id} has {len(hits)} forecasts ({", ".join(f["id"] for f in hits)}); '
                                             'the comparison is ambiguous'))
                        return None
                    return hits[0] if hits else None
                p, w = node(rel['part'], part_m), node(rel['whole'], whole_m)
                if p and w and _exceeds(_outcome_set(p), _outcome_set(w)):          # [46s] open and closed ends kept
                    errors.append(('C3', f'{period} {sc}: {rel["part"]} {p["id"]} {_outcome_set(p)} exceeds {rel["whole"]} {w["id"]} {_outcome_set(w)}'))
    for shared in family.get('shared', []):
        want = _key(shared)
        nodes = [f for f in figs.values() if _key(f['what']) == want and f['basis'] == 'forecast']
        touched = [v for v, o in outcomes.items() if any(_key(figs[f]['what']) == want for f in reachable(o))]
        if not touched:
            continue
        per_scenario = {}
        for n in nodes:
            per_scenario.setdefault(n.get('scenario', 'base'), []).append(n['id'])
        if not nodes:
            errors.append(('C4', f'{want}: no forecast node, though {", ".join(touched)} depend on it'))
        for sc, ids in sorted(per_scenario.items()):
            if len(ids) != 1:
                errors.append(('C4', f'{want} {sc}: {len(ids)} forecast nodes ({", ".join(ids)}); exactly one per scenario is required'))
        stop = {n['id'] for n in nodes}
        for f in figs.values():                       # [46i.1] scenario membership is derived along the whole path, not declared
            sc = f.get('scenario', 'base')
            if sc == 'range' or f['kind'] not in ('computed', 'estimate'):
                continue
            upstream = _upstream_of(f['id'], figs, refs)
            borrowed = sorted(r for r in upstream if r in stop and figs[r].get('scenario', 'base') != sc)
            if borrowed:
                errors.append(('C4', f'{want}: {f["id"]} ({sc}) depends on {", ".join(borrowed)} of another scenario'))
        for view_id in touched:                      # [46g.3] a bypass reaches the quantity through no forecast node of any scenario
            bypass = [f for f in reachable(outcomes[view_id], stop=stop) if f not in stop and _key(figs[f]['what']) == want]
            if bypass:
                errors.append(('C4', f'{want}: {view_id} reaches {", ".join(sorted(bypass))} without passing a forecast node ({", ".join(sorted(stop))})'))
    for rel in family.get('relations', []):           # [46j.2] the later member rests on the earlier member's forecast nodes, per scenario
        if rel['type'] != 'same_base' or rel['later'] not in outcomes or rel['earlier'] not in outcomes:
            continue
        base_key = _key(members[rel['earlier']]['what'])
        earlier_graph = _upstream_of(outcomes[rel['earlier']], figs, refs) | {outcomes[rel['earlier']]}
        earlier_nodes = {f for f in earlier_graph if _key(figs[f]['what']) == base_key and figs[f]['basis'] == 'forecast'}
        reached = reachable(outcomes[rel['later']], stop=earlier_nodes)
        bypass = [f for f in reached if f not in earlier_nodes and _key(figs[f]['what']) == base_key]
        later_key = _key(members[rel['later']]['what'])
        e_out = outcomes[rel['earlier']]                  # [46z.1] the published forecast, or the scenario paths its range summary rests on
        if figs[e_out].get('scenario') == 'range':
            by_scenario = {}
            for n in sorted(r for r in figs[e_out].get('rests_on', []) if r in figs and _key(figs[r]['what']) == base_key
                            and figs[r]['basis'] == 'forecast'):
                by_scenario.setdefault(figs[n].get('scenario', 'base'), []).append(n)
        else:
            by_scenario = {figs[e_out].get('scenario', 'base'): [e_out]}
        later_graph = _upstream_of(outcomes[rel['later']], figs, refs) | {outcomes[rel['later']]}
        for f in sorted(later_graph):                 # [46k.1] every later scenario path reaches the earlier forecast of its own scenario
            sc = figs[f].get('scenario', 'base')
            if sc == 'range' or _key(figs[f]['what']) != later_key or figs[f]['basis'] != 'forecast':
                continue
            cands = by_scenario.get(sc) or (next(iter(by_scenario.values())) if len(by_scenario) == 1 else [])
            used = [c for c in cands if c in _determining(f, figs)]
            target = used[0] if used else None
            if target is None:                            # [46l.1] through value-determining inputs only
                errors.append(('C9', f'{f} ({sc}) of {rel["later"]} is not computed from {rel["earlier"]}\'s {sc} forecast'))
            else:                                     # [46o.1, 46p] its value moves when that forecast moves: one realisation per figure
                mid_t = sum(_interval(figs[target])) / 2
                before = _evaluate_points(figs, refs, {})[f]
                after = _evaluate_points(figs, refs, {target: mid_t * 1.1})[f]
                if abs(after - before) <= 1e-9 * max(1.0, abs(before)):
                    errors.append(('C9', f'{f} ({sc}) of {rel["later"]} does not change when {rel["earlier"]}\'s forecast {target} changes'))
        later_scen = {figs[f].get('scenario', 'base') for f in later_graph if _key(figs[f]['what']) == later_key
                      and figs[f]['basis'] == 'forecast' and figs[f].get('scenario', 'base') != 'range'}
        if earlier_nodes and not later_scen:              # [46m.2] a citation never stands in for a calculation
            errors.append(('C9', f'{rel["later"]} has no calculation from {rel["earlier"]}\'s forecast, only a range resting on it'))
        if len(by_scenario) > 1 and later_scen != set(by_scenario):     # [46l.1] the later member covers the earlier's scenarios
            errors.append(('C9', f'{rel["later"]} covers scenarios {sorted(later_scen)} but {rel["earlier"]} covers {sorted(by_scenario)}'))
        if not reached & earlier_nodes:
            errors.append(('C9', f'{rel["later"]} does not rest on {rel["earlier"]}\'s forecast ({", ".join(sorted(earlier_nodes))})'))
        if bypass:
            errors.append(('C9', f'{rel["later"]} reaches {", ".join(sorted(bypass))} for {base_key} without {rel["earlier"]}\'s forecast'))
    supplied = family.get('prior_answers', {})
    for fig in figs.values():
        earlier = fig['kind'] == 'prior' or fig.get('basis') == 'prior_forecast' or 'pointer' in fig   # [46i.2] derived, not labelled
        if not earlier:
            continue
        if fig['kind'] != 'prior' or fig.get('basis') != 'prior_forecast':
            errors.append(('C10', f'{fig["id"]}: an earlier forecast must be kind prior with basis prior_forecast'))
        ptr, ans_prior = fig.get('pointer', {}), supplied.get(fig.get('pointer', {}).get('view'), {})
        if ans_prior.get('day') != ptr.get('day') or not any(_same(fig.get('value'), v) for v in ans_prior.get('values', [])):
            errors.append(('C10', f'{fig["id"]}: no earlier answer of {ptr.get("view")} on {ptr.get("day")} shown in the request states {fig.get("value")}'))
        owners = [a['view_id'] for a in calc['answers'] if a.get('outcome') == fig['id']]
        if owners:                                    # [46h.2] nor the current outcome
            errors.append(('C10', f'{fig["id"]}: an earlier forecast cannot be the current outcome of {", ".join(owners)}'))
        users = [f['id'] for f in figs.values() if fig['id'] in refs(f)]
        if users:
            errors.append(('C10', f'{fig["id"]}: an earlier forecast is for comparison only and cannot feed {", ".join(users)}'))

    recorded += _assumptions(family, figs, outcomes, calc, refs)
    finite = lambda v: v if abs(v) != float('inf') else None
    published = {v: [finite(_outcome_set(figs[o])[0]), finite(_outcome_set(figs[o])[2]), figs[o].get('bound')] for v, o in outcomes.items()}
    return {'errors': errors, 'recorded': recorded, 'published': published}


def _per_unit(op, ins, fig):
    """The per-unit identity: ratio(total, price per unit) -> units, product(units, price per unit) -> total, for one population and
    scope. Labels are the judge's; a reader checks them against the passages."""
    out = fig['what']
    if len(ins) != 2:
        return False
    same = all((i['what']['population'], i['what']['scope']) == (out['population'], out['scope']) for i in ins)
    price = [i for i in ins if i['what']['measure'] == 'price per unit' and i['unit'] in ('USD', 'USD bn')]
    if op == 'ratio':
        return same and len(price) == 1 and ins[1] is price[0] and out['measure'] == 'units' and ins[0]['unit'] in ('USD', 'USD bn')
    units = [i for i in ins if i['what']['measure'] == 'units' and i['unit'] == 'units']
    return same and len(price) == 1 and len(units) == 1 and fig['unit'] in ('USD', 'USD bn')


def member_sources(answer, figs):
    """[46k.3, 46ac.1] The source figures a member's own outcome and reference rest on, each identified by its passage, expression and
    the component used."""
    refs = lambda f: list(f.get('inputs', [])) + [r for r in f.get('rests_on', []) if r in figs] + \
        ([f['adjusts']['figure']] if f.get('adjusts') else []) + ([f['bridge']] if f.get('bridge') else [])
    own = set()
    for start in (answer.get('outcome'), (answer.get('reference') or {}).get('figure')):
        if start in figs:
            own |= _upstream_of(start, figs, refs) | {start}
    return sorted(f'{figs[f]["evidence"]}|{figs[f]["expression"]}|{figs[f].get("component", "value")}' for f in own if figs[f]['kind'] == 'source')


def changed(previous, answer, figs):
    """D728: whether a member's conclusion changed, derived by code from its earlier rung, outcome and source figures."""
    if previous is None:
        return True, 'first judgement'
    was_unresolved = previous.get('shape') == 'unresolved'
    if answer.get('shape') == 'unresolved' or was_unresolved:          # [46ac.2] an unresolved answer is routed before any number
        if answer.get('shape') == 'unresolved' and was_unresolved:
            return False, 'still unresolved'
        return True, 'now unresolved' if answer.get('shape') == 'unresolved' else 'now a forecast'
    refs = lambda f: list(f.get('inputs', [])) + [r for r in f.get('rests_on', []) if r in figs] + \
        ([f['adjusts']['figure']] if f.get('adjusts') else []) + ([f['bridge']] if f.get('bridge') else [])
    out = figs[answer['outcome']]
    if out['kind'] == 'computed':                     # [46aa] the same recomputed outcome publication uses
        (lo_r, hi_r), b_r = _evaluate_bounded(figs, refs, {})[out['id']]
        out = {k: v for k, v in out.items() if k not in ('value', 'low', 'high', 'bound')}
        out.update({'value': lo_r} if lo_r == hi_r else {'low': lo_r, 'high': hi_r})
        if b_r:
            out['bound'] = b_r
    sources = member_sources(answer, figs)
    reasons = []
    if answer['rung'] != previous['rung']:
        reasons.append(f'rung {previous["rung"]} to {answer["rung"]}')
    # [46l.2, 46ab] the published outcome as published: both ends (None for an open-ended side) and the bound
    o_lo, _, o_hi, _ = _outcome_set(out)
    finite = lambda v: None if v is None or abs(v) == float('inf') else round(v, 6)
    cur = (finite(o_lo), finite(o_hi), out.get('bound'))
    prev = previous['outcome']
    if isinstance(prev, (int, float)):
        prev = (prev, prev, None)
    elif len(prev) == 2:
        prev = (prev[0], prev[1], None)
    prev = (finite(prev[0]), finite(prev[1]), prev[2])
    near = lambda a, b: (a is None and b is None) or (a is not None and b is not None and abs(a - b) <= 0.005 * max(abs(b), 1e-9))
    if cur[2] != prev[2] or not near(cur[0], prev[0]) or not near(cur[1], prev[1]):
        reasons.append(f'outcome {list(prev)} to {list(cur)}')
    added, dropped = sorted(set(sources) - set(previous['sources'])), sorted(set(previous['sources']) - set(sources))
    if added or dropped:
        reasons.append(f'source figures added {added}, dropped {dropped}')
    return bool(reasons), '; '.join(reasons) or 'unchanged'


def publish_decision(family, calc, result):
    """DESIGN.md §4: 'refused' when a check fails (the harness retries once); 'held' when a member is unresolved and a declared
    relation joins it to another member; else 'publish' (unresolved members shown as unresolved)."""
    if result['errors']:
        return 'refused'
    unresolved = {a['view_id'] for a in calc['answers'] if a.get('shape') == 'unresolved'}
    for rel in family.get('relations', []):
        ends = {rel.get('part'), rel.get('whole'), rel.get('later'), rel.get('earlier')} - {None}
        if ends & unresolved and ends - unresolved:
            return 'held'
    return 'publish'


def family_outcome(attempts):
    """The round's outcome from up to two attempts' decisions: a refusal is retried once; two refusals make the family unresolved."""
    if attempts[0] != 'refused':
        return attempts[0]
    if len(attempts) > 1 and attempts[1] != 'refused':
        return attempts[1]
    return 'unresolved'


def _determining(fid, figs):
    """The figures that determine fid's value: computed inputs only, at any depth (an estimate's rests_on explains, it does not compute)."""
    seen_ids, stack = set(), list(figs[fid].get('inputs', [])) if figs[fid]['kind'] == 'computed' else []
    while stack:
        f = stack.pop()
        if f in seen_ids or f not in figs:
            continue
        seen_ids.add(f)
        if figs[f]['kind'] == 'computed':
            stack.extend(figs[f].get('inputs', []))
    return seen_ids


def _upstream_of(fid, figs, refs):
    """The figures that fid's own value is computed from (fid excluded)."""
    seen_ids, stack = set(), list(refs(figs[fid]))
    while stack:
        f = stack.pop()
        if f in seen_ids or f not in figs:
            continue
        seen_ids.add(f)
        stack.extend(refs(figs[f]))
    return seen_ids


def _reference_errors(view_id, ref, figs, passages, refs):
    if ref is None:
        return [('C5', f'{view_id}: the reference names no figure')]
    graph = [ref['id']] + sorted(_upstream_of(ref['id'], figs, refs))
    nodes = [figs[f] for f in graph]
    if any(n['kind'] in ('estimate', 'prior') or n['basis'] in ('forecast', 'prior_forecast') for n in nodes):
        return [('C5', f'{view_id}: the reference {ref["id"]} rests on the system\'s own forecast or an estimate')]
    leaves = [n for n in nodes if n['kind'] == 'source']
    if not any(n['basis'] in EXTERNAL and passages.get(n['evidence'], {}).get('speaker') != 'system' for n in leaves):
        return [('C5', f'{view_id}: the reference {ref["id"]} has no external source among its leaves')]
    if any(n['basis'] not in EXTERNAL | {'reported'} for n in leaves):
        return [('C5', f'{view_id}: the reference {ref["id"]} has a leaf that is neither external nor reported')]
    return []


def _evaluate(figs, refs, overrides):
    """Recompute computed figures from their inputs, with some figures' values replaced; estimates keep their values."""
    values, order, done = {}, [], set()

    def visit(fid):
        if fid in done:
            return
        done.add(fid)
        for r in refs(figs[fid]):
            if r in figs:
                visit(r)
        order.append(fid)
    for fid in figs:
        visit(fid)
    for fid in order:
        fig = figs[fid]
        if fid in overrides:
            values[fid] = overrides[fid]
        elif fig['kind'] == 'computed' and fig.get('operation') in OPERATIONS:
            t_ids, t_signs = _terms(fig)
            ins = [values[i] + (figs[i]['unit'],) for i in t_ids]
            values[fid] = _compute(fig['operation'], ins, t_signs, fig['unit']) if ins else (0.0, 0.0)
        else:
            values[fid] = _interval(fig)
    return values


def _evaluate_points(figs, refs, overrides):
    """Recompute with every figure at one point (its midpoint), the same wherever it appears; overrides set points."""
    values, order, done = {}, [], set()

    def visit(fid):
        if fid in done:
            return
        done.add(fid)
        for r in refs(figs[fid]):
            if r in figs:
                visit(r)
        order.append(fid)
    for fid in figs:
        visit(fid)
    for fid in order:
        fig = figs[fid]
        if fid in overrides:
            values[fid] = overrides[fid]
        elif fig['kind'] == 'computed' and fig.get('operation') in OPERATIONS:
            t_ids, t_signs = _terms(fig)
            ins = [(values[i], values[i], figs[i]['unit']) for i in t_ids]
            lo, hi = _compute(fig['operation'], ins, t_signs, fig['unit']) if ins else (0.0, 0.0)
            values[fid] = (lo + hi) / 2
        else:
            values[fid] = sum(_interval(fig)) / 2
    return values


def _boundaries(bands, a, b):
    edges = sorted({e for band in bands for e in band if e is not None})
    lo, hi = min(a, b), max(a, b)
    return [e for e in edges if lo < e <= hi]


def _assumptions(family, figs, outcomes, calc, refs):
    out = []
    members = family['members']

    def downstream_formula(start, outcome_id):
        """True when every figure between start and the outcome (the outcome included) is computed."""
        between = [f for f in [outcome_id] + sorted(_upstream_of(outcome_id, figs, refs)) if start in _upstream_of(f, figs, refs)]
        return all(figs[f]['kind'] == 'computed' for f in between)
    for fig in figs.values():
        alt, kind = None, None
        if fig['kind'] == 'computed' and fig.get('relation') == 'overlap_unknown' and fig.get('disputed') in fig.get('inputs', []):
            t_ids, t_signs = _terms(dict(fig, inputs=[i for i in fig['inputs'] if i != fig['disputed']],
                                         signs=[k for i, k in zip(fig['inputs'], fig.get('signs') or [1] * len(fig['inputs'])) if i != fig['disputed']]))
            keep, signs = t_ids, t_signs
            alt = _compute(fig['operation'], [_interval(figs[i]) + (figs[i]['unit'],) for i in keep], signs, fig['unit'])
            side = _bound_direction(fig['operation'], [figs[i] for i in keep], signs)      # [46u.1] the retained operands' bounds
            strict = any(figs[i].get('bound') in STRICT for i in keep)
            kind, bound = 'overlap', {'lower': '>' if strict else '>=', 'upper': '<' if strict else '<=', 'two-sided': 'approx', 'mixed': 'mixed', None: None}[side]
        elif fig['kind'] == 'estimate' and fig.get('adjusts'):
            target = figs[fig['adjusts']['figure']]
            alt, kind, bound = _interval(target), 'adjustment', target.get('bound')
        if kind is None:
            continue
        for view_id, outcome_id in outcomes.items():
            if fig['id'] != outcome_id and fig['id'] not in _upstream_of(outcome_id, figs, refs):
                continue
            if not downstream_formula(fig['id'], outcome_id):
                out.append({'type': kind, 'figure': fig['id'], 'outcome': view_id, 'certainty': 'undetermined'})
                continue
            base_vals = _evaluate_bounded(figs, refs, {})                 # [46s, 46t.1] bounds carried through recomputation
            alt_override = (alt, bound)
            alt_vals = _evaluate_bounded(figs, refs, {fig['id']: alt_override})
            base_set, alt_set = _set_from(*base_vals[outcome_id]), _set_from(*alt_vals[outcome_id])
            definite, possible = _crossings(base_set, alt_set, members[view_id]['bands'])
            finite = lambda v: v if abs(v) != float('inf') else None
            out.append({'type': kind, 'figure': fig['id'], 'outcome': view_id, 'value': [finite(base_set[0]), finite(base_set[2])],
                        'alternate': [finite(alt_set[0]), finite(alt_set[2])], 'alternate_bound': bound,
                        'definite': definite, 'possible': possible})                      # [46t.1] certainty per boundary
    return out
