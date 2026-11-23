"""judging-v13s checks: the small format (SMALL-DESIGN.md §2 [52] and [54], D737, D738). Harness-only. Code refuses an answer only for
the five named defects (S1 a number misread, S2 wrong arithmetic, S3/S8 a part above its whole or added into it, S4 two forecasts of one
quarter, S5 an own estimate passed off as the market's) and for broken structure (S6, S7), and only where the calculation's own
structure decides it (D738). Everything else is recorded for readers.

from_answer(data, family) -> the internal shape the harness reads ({'figures', 'answers', 'decode_errors'})
check(family, passages, calc) -> {'errors': [(rule, detail)], 'recorded': [...], 'published': {view_id: [low, high, None]}}
"""
import itertools
import math
import re

KINDS = {'source', 'computed', 'estimate'}
BASES = {'reported', 'guidance', 'consensus', 'third_party', 'forecast'}
EXTERNAL = {'consensus', 'guidance', 'third_party'}
UNITS = {'USD bn', '%', 'x'}
ARITY = {'sum': (2, None), 'product': (2, None), 'difference': (2, 2), 'ratio': (2, 2), 'share': (2, 2), 'growth': (2, 2),
         'apply_growth': (2, 2)}
QUALIFIERS_BEFORE = sorted(['more than', 'at least', 'up to', 'as much as', 'less than', 'over', 'about', 'approximately', 'around',
                            'roughly', 'nearly', 'almost', 'below', 'under', 'near', 'estimated'], key=len, reverse=True)
QUALIFIERS_AFTER = ['or more', 'or less']
QUALIFIERS = ['none'] + QUALIFIERS_BEFORE + QUALIFIERS_AFTER
SCALE = {'trillion': 1000.0, 'tn': 1000.0, 't': 1000.0, 'billion': 1.0, 'bn': 1.0, 'b': 1.0, 'million': 0.001, 'mn': 0.001, 'm': 0.001}
LIMIT = 1e9                                              # [54] a number beyond this is refused, not computed
MAX_RANGE_LEAVES = 12

_NUM = r'(\d[\d,]*(?:\.\d+)?)'
_CUR = r'(?:US)?\$\s?'
_SC = r'(?:\s*(trillion|billion|million|bn|tn|mn|t|b|m)\b)?'
_MINUS = r'([-−–]\s?)?'
_PCT = r'\s*(?:%|percent)'
_BODIES = [   # [54] the complete numeric expressions, longest forms first; a quote_number must be one of them, whole
    ('relative', _CUR + _NUM + _SC + r'\s*,?\s*\(?\s*(?:plus or minus|\+/-|±)\s*' + _NUM + r'\s*%\s*\)?'),
    ('range', _CUR + _NUM + _SC + r'\s*(?:–|—|-|to)\s*(?:' + _CUR + r')?' + _NUM + _SC),
    ('range', r'between\s+' + _CUR + _NUM + _SC + r'\s+and\s+(?:' + _CUR + r')?' + _NUM + _SC),
    ('percent_range', r'between\s+' + _NUM + r'\s*%?\s+and\s+' + _NUM + _PCT),
    ('percent_range', _NUM + r'\s*%?\s*(?:–|—|-|to)\s*' + _NUM + _PCT),
    ('money', _MINUS + _CUR + _NUM + _SC),
    ('percent', _MINUS + _NUM + _PCT),
    ('multiple', r'(double|triple|twice)'),
]
_ANCHORED = [(form, re.compile(r'^' + body + r'$', re.I)) for form, body in _BODIES]
_SCAN = [(form, re.compile(r'(?<![\w.,$])' + body + r'(?![\w%])', re.I)) for form, body in _BODIES]
_PERIOD = re.compile(r'^(FY|CY)(\d{4})(?:\s+(Q[1-4](?:-Q[1-4])?|H[12]))?$')


def _num(text):
    return float(text.replace(',', ''))


def _money(number, scale):
    return _num(number) * SCALE[scale.lower()] if scale else _num(number) / 1e9      # an amount with no scale is in dollars


def parse_number(text):
    """A quote_number as written: {'unit', 'value'} or {'unit', 'low', 'high'[, 'mid']}; None when it is not one complete form."""
    text = (text or '').strip()
    for form, pattern in _ANCHORED:
        m = pattern.match(text)
        if not m:
            continue
        g = m.groups()
        if form == 'relative':
            mid, rel = _money(g[0], g[1]), _num(g[2])
            return {'unit': 'USD bn', 'low': mid * (1 - rel / 100), 'high': mid * (1 + rel / 100), 'mid': mid}
        if form == 'range':
            if not (g[1] or g[3]):
                return None
            return {'unit': 'USD bn', 'low': _money(g[0], g[1] or g[3]), 'high': _money(g[2], g[3] or g[1])}
        if form == 'percent_range':
            return {'unit': '%', 'low': _num(g[0]), 'high': _num(g[1])}
        if form == 'money':
            return {'unit': 'USD bn', 'value': (-1.0 if g[0] else 1.0) * _money(g[1], g[2])}
        if form == 'percent':
            return {'unit': '%', 'value': (-1.0 if g[0] else 1.0) * _num(g[1])}
        return {'unit': 'x', 'value': 3.0 if g[0].lower() == 'triple' else 2.0}
    return None


_CHANGE = re.compile(r'(?<!rang)(?<!range)(?<!ranges)(?<!ranging)\bfrom\s*$', re.I)


def expressions(text):
    """[54] Every complete numeric expression in a quote, as (start, end), longest forms first and never overlapping. [D740] An
    'X to Y' written after 'from' (not 'range(s) from' or 'ranging from') is a change between two values, so its two amounts are
    separate expressions."""
    taken = []
    for form, pattern in _SCAN:
        for m in pattern.finditer(text):
            if form == 'range' and re.search(r'\bto\b', m.group(0), re.I) and not m.group(0).lower().startswith('between'):
                before = text[:m.start()].rstrip().lower()
                if before.endswith('from') and not re.search(r'\b(range|ranges|ranged|ranging)\s+from$', before):
                    continue
            if not any(m.start() < e and s < m.end() for s, e in taken):
                taken.append((m.start(), m.end()))
    return sorted(taken)


def _key(what):
    return (what['population'], what['measure'], what['scope'], what['period'])


def _quantity(what):
    return (what['population'], what['measure'], what['scope'])


def _same(a, b):
    return a is not None and b is not None and abs(a - b) <= 1e-9 * max(1.0, abs(a), abs(b))


def _close(declared, expected, unit):
    return abs(declared - expected) <= max(0.005 * abs(expected), 0.05 if unit == '%' else 0.1)


def _is_range(fig):
    return isinstance(fig.get('low'), (int, float)) and isinstance(fig.get('high'), (int, float))


def _interval(fig):
    if _is_range(fig):
        return float(fig['low']), float(fig['high'])
    return float(fig['value']), float(fig['value'])


def _period(text):
    m = _PERIOD.match((text or '').strip())
    if not m:
        return None
    year, part = m.group(1) + m.group(2), m.group(3)
    if part is None:
        quarters = {1, 2, 3, 4}
    elif part.startswith('H'):
        quarters = {1, 2} if part == 'H1' else {3, 4}
    else:
        a, _, b = part.partition('-')
        lo, hi = int(a[1]), int((b or a)[1])
        if lo > hi:
            return None
        quarters = set(range(lo, hi + 1))
    return year, quarters


def _overlap(p1, p2):
    """[54] Two periods overlap: the same label, or parsed fiscal periods of one year that share a quarter."""
    if p1 == p2:
        return True
    a, b = _period(p1), _period(p2)
    return bool(a and b and a[0] == b[0] and a[1] & b[1])


# ---------- decoding the wire shape ----------
FIGURE_FIELDS = ('id', 'what', 'kind', 'basis', 'value', 'low', 'high', 'unit', 'quote_number', 'qualifier', 'inputs', 'operation',
                 'basis_text', 'rests_on')


def _text(value):
    return value if isinstance(value, str) and value.strip() else None


def from_answer(data, family):
    """The v13s wire answer as the internal shape: `evidence_id` becomes `evidence`; the markers become each answer's `outcome` and
    `reference`; marker errors go in `decode_errors` (S5, S6, S7). An empty string counts as absent."""
    errors, figures, outcome_for, reference_for = [], [], {}, {}
    members = family['members']
    for f in data.get('figures') or []:
        g = {k: f[k] for k in FIGURE_FIELDS if f.get(k) is not None}
        if f.get('evidence_id') is not None:
            g['evidence'] = f['evidence_id']
        for marks, store in (('outcome_for', outcome_for), ('reference_for', reference_for)):
            listed = f.get(marks) or []
            for v in sorted(set(listed)):
                if listed.count(v) > 1:
                    errors.append(('S7', f'{f.get("id")}: {marks} lists {v} more than once'))
                store.setdefault(v, []).append(f.get('id'))
        figures.append(g)
    answers = []
    for a in data.get('answers') or []:
        v = a.get('view_id')
        a2 = {k: a[k] for k in ('view_id', 'shape', 'rung', 'reasons', 'cites', 'pushes', 'theme_pushes') if a.get(k) is not None}
        if _text(a.get('why')):
            a2['why'] = a['why']
        if v not in members:
            answers.append(a2)
            continue
        outs, refs, reason = outcome_for.get(v, []), reference_for.get(v, []), _text(a.get('reference_unavailable'))
        if a.get('shape') == 'unresolved':
            if outs or refs or reason or a.get('rung') is not None or not _text(a.get('why')):
                errors.append(('S7', f'{v}: an unresolved answer has why, rung and reference_unavailable null, and no figure marked for it'))
        else:
            if len(outs) == 1:
                a2['outcome'] = outs[0]
            else:
                errors.append(('S6', f'{v}: {len(outs)} figures are marked as its outcome; exactly one is required'))
            if len(refs) == 1 and not reason:
                a2['reference'] = {'figure': refs[0]}
            elif not refs and reason:
                a2['reference'] = {'unavailable': reason}
            else:
                errors.append(('S5', f'{v}: needs exactly one of a figure marked as its reference or reference_unavailable'))
        answers.append(a2)
    for v in set(outcome_for) | set(reference_for):
        if v not in members:
            errors.append(('S7', f'{v} is marked on a figure but is not a member of the family'))
    return {'figures': figures, 'answers': answers, 'decode_errors': errors}


# ---------- arithmetic ----------
def _result_unit(op, units):
    if any(u not in UNITS for u in units):
        return None
    if op in ('sum', 'difference'):
        return units[0] if len(set(units)) == 1 else None
    if op == 'product':
        money, pct = units.count('USD bn'), units.count('%')
        if money + pct > 1:                                  # never USD bn × % (use share), never two amounts or two percentages
            return None
        return 'USD bn' if money else ('%' if pct else 'x')
    if op == 'ratio':
        a, b = units
        return 'x' if a == b else (a if b == 'x' else None)  # [54] same units give x; a ÷ x keeps a's unit
    if op == 'share':
        return units[0] if units[1] == '%' else None         # [54] a share of a percentage is a percentage
    if op == 'growth':
        return '%' if units[0] == units[1] else None
    if op == 'apply_growth':
        return units[0] if units[1] == '%' else None
    return None


def _apply(op, xs):
    if op == 'sum':
        return sum(xs)
    if op == 'difference':
        return xs[0] - xs[1]
    if op == 'product':
        return math.prod(xs)
    if op == 'ratio':
        return xs[0] / xs[1]
    if op == 'share':
        return xs[0] * xs[1] / 100.0
    if op == 'growth':
        return (xs[1] / xs[0] - 1.0) * 100.0
    if op == 'apply_growth':
        return xs[0] * (1.0 + xs[1] / 100.0)
    raise ValueError(op)


class _Calc:
    """[54] Each figure's value as a function of the ranged figures it rests on through inputs (its range leaves): one uncertain number
    takes one value on every path, and a range's extremes come from every combination of its leaves' ends (and zero, when a leaf
    straddles it)."""

    def __init__(self, figs):
        self.figs, self._leaves, self._intervals = figs, {}, {}

    def leaves(self, fid):
        if fid not in self._leaves:
            f = self.figs[fid]
            if f.get('kind') == 'computed':
                out = set()
                for i in f.get('inputs') or []:
                    if i in self.figs:
                        out |= self.leaves(i)
                self._leaves[fid] = out
            else:
                self._leaves[fid] = {fid} if _is_range(f) else set()
        return self._leaves[fid]

    def point(self, fid, assign):
        f = self.figs[fid]
        if f.get('kind') == 'computed':
            return _apply(f['operation'], [self.point(i, assign) for i in f['inputs']])
        return assign[fid] if fid in assign else float(f['value'])

    def choices(self, fid):
        lo, hi = _interval(self.figs[fid])
        return sorted({lo, hi} | ({0.0} if lo < 0 < hi else set()))

    def assignments(self, ids):
        ids = sorted(ids)
        for combo in itertools.product(*[self.choices(i) for i in ids]):
            yield dict(zip(ids, combo))

    def interval(self, fid):
        """(low, high), or None when it cannot be evaluated."""
        if fid in self._intervals:
            return self._intervals[fid]
        f = self.figs[fid]
        try:
            if f.get('kind') != 'computed':
                result = _interval(f)
            else:
                leaves = self.leaves(fid)
                if len(leaves) > MAX_RANGE_LEAVES:
                    result = None
                else:
                    values = [self.point(fid, a) for a in self.assignments(leaves)]
                    result = (min(values), max(values)) if all(math.isfinite(v) for v in values) else None
        except (ZeroDivisionError, OverflowError, ValueError, KeyError, TypeError, RecursionError):
            result = None
        self._intervals[fid] = result
        return result

    def fits(self, part, whole):
        """[54] The part can be at most the whole: for every combination of the leaves they share, some value of each one's own leaves
        puts the part at or below the whole (independent ranges: the part's low end at most the whole's high end)."""
        lp, lw = self.leaves(part), self.leaves(whole)
        shared = lp & lw
        if len(lp | lw) > MAX_RANGE_LEAVES:
            return True
        for s in self.assignments(shared):
            low_part = min(self.point(part, dict(s, **a)) for a in self.assignments(lp - shared))
            high_whole = max(self.point(whole, dict(s, **a)) for a in self.assignments(lw - shared))
            if low_part > high_whole + 1e-9 * max(1.0, abs(high_whole)):
                return False
        return True


def evaluate(figs):
    calc = _Calc(figs)
    return {fid: calc.interval(fid) for fid in figs}


def _evaluate_bounded(figs, refs, overrides):
    """The harness's reconciliation reads (interval, bound); v13s has no bounds."""
    try:
        return {fid: (v, None) for fid, v in evaluate(figs).items() if v is not None}
    except Exception:
        return {}


def _upstream_of(fid, figs, refs):
    seen_ids, stack = set(), list(refs(figs[fid]))
    while stack:
        f = stack.pop()
        if f in seen_ids or f not in figs:
            continue
        seen_ids.add(f)
        stack.extend(refs(figs[f]))
    return seen_ids


def _uses(fid, figs):
    """The figures fid uses through inputs, at any depth (fid excluded)."""
    return _upstream_of(fid, figs, lambda f: list(f.get('inputs') or []))


def _beneath(fid, figs):
    """The figures beneath fid through inputs and rests_on, at any depth (fid excluded)."""
    return _upstream_of(fid, figs, lambda f: list(f.get('inputs') or []) + [r for r in f.get('rests_on') or [] if r in figs])


def _tops(start, key, figs):
    """[54] The figures of `key` an answer adopts: those reached from its outcome (inputs and rests_on) before any other figure of
    that key."""
    found, stack, seen_ids = [], [start], set()
    while stack:
        fid = stack.pop()
        if fid in seen_ids or fid not in figs:
            continue
        seen_ids.add(fid)
        f = figs[fid]
        if _key(f['what']) == key:
            found.append(fid)
            continue
        stack.extend(list(f.get('inputs') or []) + [r for r in f.get('rests_on') or [] if r in figs])
    return sorted(found)


# ---------- the checks ----------
def _structure(family, passages, calc, figs):
    errors = list(calc.get('decode_errors') or [])
    ids = [f.get('id') for f in calc['figures']]
    for fid in sorted({i for i in ids if ids.count(i) > 1}, key=str):
        errors.append(('S7', f'{fid} is defined twice'))
    for f in calc['figures']:
        fid = f.get('id')
        if not isinstance(fid, str) or not fid:
            errors.append(('S7', 'a figure has no id'))
            continue
        if fid in passages:
            errors.append(('S7', f'{fid}: a figure id must not be a passage id'))
        if f.get('kind') not in KINDS or f.get('basis') not in BASES or f.get('unit') not in UNITS:
            errors.append(('S7', f'{fid}: kind, basis or unit outside the closed set'))
            continue
        numbers = [f.get(k) for k in ('value', 'low', 'high') if isinstance(f.get(k), (int, float))]
        if any(not math.isfinite(n) or abs(n) > LIMIT for n in numbers):
            errors.append(('S7', f'{fid}: a number that is not finite or beyond {LIMIT:g}'))
            continue
        has_value = isinstance(f.get('value'), (int, float))
        has_low, has_high = isinstance(f.get('low'), (int, float)), isinstance(f.get('high'), (int, float))
        if has_value == (has_low or has_high) or has_low != has_high:
            errors.append(('S7', f'{fid}: a figure has value, or low and high, never both and never one end alone'))
        elif has_low and has_high and f['low'] > f['high']:
            errors.append(('S7', f'{fid}: low is above high'))
        kind = f['kind']
        if kind != 'source' and (f.get('evidence') or f.get('quote_number') or (f.get('qualifier') or 'none') != 'none'):
            errors.append(('S7', f'{fid}: evidence_id, quote_number and qualifier are for source figures only'))
        if kind != 'computed' and (f.get('inputs') or f.get('operation')):
            errors.append(('S7', f'{fid}: inputs and operation are for computed figures only'))
        if kind != 'estimate' and f.get('rests_on'):
            errors.append(('S7', f'{fid}: rests_on is for estimates only'))
        if kind == 'source':
            if f['basis'] == 'forecast':
                errors.append(('S7', f'{fid}: a source cannot have basis forecast'))
            if not f.get('evidence') or not f.get('quote_number'):
                errors.append(('S7', f'{fid}: a source needs evidence_id and quote_number'))
        elif kind == 'computed':
            ins, op = f.get('inputs') or [], f.get('operation')
            if op not in ARITY or not ins:
                errors.append(('S7', f'{fid}: a computed figure needs inputs and an operation from the closed set'))
            else:
                lo_n, hi_n = ARITY[op]
                if len(ins) < lo_n or (hi_n is not None and len(ins) > hi_n):
                    errors.append(('S7', f'{fid}: {op} takes ' + (f'exactly {lo_n}' if hi_n == lo_n else f'{lo_n} or more') + f' inputs, not {len(ins)}'))
            for i in ins:
                if i in passages and i not in figs:
                    errors.append(('S7', f'{fid}: inputs name passage {i}; inputs name figures only'))
                elif i not in figs:
                    errors.append(('S7', f'{fid}: input {i} is not a figure'))
        elif not _text(f.get('basis_text')):
            errors.append(('S7', f'{fid}: an estimate needs basis_text'))
        for r in f.get('rests_on') or []:
            if r not in figs and r not in passages:
                errors.append(('S7', f'{fid}: rests_on names {r}, which is neither a figure nor a shown passage'))
    state = {}

    def cyclic(fid):
        if state.get(fid) == 1:
            return True
        if state.get(fid) == 2 or fid not in figs:
            return False
        state[fid] = 1
        f = figs[fid]
        hit = any(cyclic(r) for r in list(f.get('inputs') or []) + [r for r in f.get('rests_on') or [] if r in figs])
        state[fid] = 2
        return hit
    if any(cyclic(fid) for fid in figs):
        errors.append(('S7', 'a figure depends on itself (through inputs or rests_on)'))
    members = family['members']
    seen = {}
    for a in calc['answers']:
        seen[a.get('view_id')] = seen.get(a.get('view_id'), 0) + 1
    for v in members:
        if seen.get(v, 0) != 1:
            errors.append(('S7', f'{v} has {seen.get(v, 0)} answers; exactly one is required'))
    for v in seen:
        if v not in members:
            errors.append(('S7', f'{v} is not a member of the family'))
    return errors


def _sources(passages, figs):
    errors = []
    for f in figs.values():
        if f['kind'] != 'source':
            continue
        fid, qn, ev = f['id'], f['quote_number'], f['evidence']
        if ev not in passages:
            errors.append(('S1', f'{fid}: evidence_id {ev} is not a shown passage'))
            continue
        text = passages[ev]['text']
        spans = expressions(text)
        starts = [(s, e) for s, e in spans if text[s:e] == qn]
        if not starts:
            inside = [text[s:e] for s, e in spans if qn in text[s:e]]
            errors.append(('S1', f'{fid}: "{qn}" is part of the longer expression "{inside[0]}" in {ev}; copy it whole' if inside else
                           f'{fid}: "{qn}" is not written in the quote of {ev} as a complete number'))
            continue
        parsed = parse_number(qn)
        if parsed is None:
            errors.append(('S1', f'{fid}: "{qn}" is not a US-dollar amount, a percentage or double, triple or twice, as written'))
            continue
        if f['unit'] != parsed['unit']:
            errors.append(('S1', f'{fid}: "{qn}" is in {parsed["unit"]}, not {f["unit"]}'))
            continue
        if 'low' in parsed:
            ok = (_same(f.get('low'), parsed['low']) and _same(f.get('high'), parsed['high'])) or \
                 ('mid' in parsed and _same(f.get('value'), parsed['mid']))
        else:
            ok = _same(f.get('value'), parsed['value'])
        if not ok:
            want = (f'low {parsed["low"]:g} and high {parsed["high"]:g}' + (f', or value {parsed["mid"]:g}' if 'mid' in parsed else '')
                    if 'low' in parsed else f'value {parsed["value"]:g}')
            errors.append(('S1', f'{fid}: "{qn}" gives {want} {parsed["unit"]}'))
            continue
        q = f.get('qualifier') or 'none'
        written = []
        for start, end in starts:
            before, after = text[:start], text[end:]
            found = next((w for w in QUALIFIERS_BEFORE if re.search(r'(?:^|\W)' + re.escape(w) + r'\s*$', before, re.I)), None)
            if found is None:
                found = next((w for w in QUALIFIERS_AFTER if re.match(r'^\s*,?\s*' + re.escape(w) + r'\b', after, re.I)), None)
            written.append(found or 'none')
        if q not in written:
            errors.append(('S1', f'{fid}: the quote writes "{written[0] if written else "none"}" with "{qn}", but the qualifier is {q}'))
    return errors


def _arithmetic(figs, calc):
    errors = []
    for f in figs.values():
        if f['kind'] != 'computed':
            continue
        fid, op, ins = f['id'], f['operation'], f['inputs']
        unit = _result_unit(op, [figs[i]['unit'] for i in ins])
        if unit is None:
            hint = ' (use share for a whole times a percentage)' if op == 'product' else ''
            errors.append(('S2', f'{fid}: {op} cannot take inputs in {", ".join(figs[i]["unit"] for i in ins)}{hint}'))
            continue
        if unit != f['unit']:
            errors.append(('S2', f'{fid}: {op} of these inputs gives {unit}, not {f["unit"]}'))
            continue
        got = {i: calc.interval(i) for i in ins}
        if not all(got.values()):
            continue                                       # an input that cannot be evaluated is refused at that input
        if op in ('ratio', 'growth'):
            denominator = got[ins[1]] if op == 'ratio' else got[ins[0]]
            if denominator[0] <= 0 <= denominator[1]:
                errors.append(('S2', f'{fid}: divides by a figure whose value can be zero'))
                continue
        if op == 'share' and not (0 <= got[ins[1]][0] and got[ins[1]][1] <= 100):
            errors.append(('S2', f'{fid}: a share takes a percentage from 0 to 100'))
            continue
        value = calc.interval(fid)
        if value is None:
            errors.append(('S2', f'{fid}: the value cannot be evaluated'))
            continue
        lo, hi = value
        if _is_range(f):
            ok = _close(f['low'], lo, unit) and _close(f['high'], hi, unit)
        else:
            ok = _close(f['value'], (lo + hi) / 2, unit)
        if not ok:
            declared = f'{f["low"]:g}–{f["high"]:g}' if _is_range(f) else f'{f["value"]:g}'
            got_text = f'{lo:.4g}' if lo == hi else f'{lo:.4g}–{hi:.4g}'
            errors.append(('S2', f'{fid}: declared {declared} but {op} of {", ".join(ins)} gives {got_text}'))
    return errors


def _overlaps_band(interval, band):
    lo, hi = interval
    b_lo = band[0] if band[0] is not None else -math.inf
    b_hi = band[1] if band[1] is not None else math.inf
    if lo == hi:
        return b_lo <= lo < b_hi
    return lo < b_hi and hi >= b_lo


def _answers(family, figs, calc, answers):
    errors, outcomes = [], {}
    members = family['members']
    for a in answers:
        v = a.get('view_id')
        member = members.get(v)
        if member is None or a.get('shape') == 'unresolved':
            continue
        out = figs.get(a.get('outcome'))
        if out is None:
            continue                                       # reported by from_answer
        if out['kind'] not in ('computed', 'estimate') or out['basis'] != 'forecast':
            errors.append(('S6', f'{v}: its outcome {out["id"]} must be your own forecast (a computed or estimate figure with basis forecast)'))
        if _key(out['what']) != _key(member['what']):
            errors.append(('S6', f'{v}: outcome {out["id"]} measures {" | ".join(_key(out["what"]))}, not the question\'s {" | ".join(_key(member["what"]))}'))
        if out['unit'] != member.get('unit', 'USD bn'):
            errors.append(('S6', f'{v}: outcome {out["id"]} is in {out["unit"]}, not {member.get("unit", "USD bn")}'))
        outcomes[v] = out['id']
        rung = a.get('rung')
        if not isinstance(rung, int) or isinstance(rung, bool) or not 1 <= rung <= len(member['bands']):
            errors.append(('S6', f'{v}: rung {rung!r} is not one of 1..{len(member["bands"])}'))
            continue
        interval = calc.interval(out['id'])
        if interval is not None and not _overlaps_band(interval, member['bands'][rung - 1]):
            shown = f'{interval[0]:g}' if interval[0] == interval[1] else f'{interval[0]:g}–{interval[1]:g}'
            errors.append(('S6', f'{v}: rung {rung} {member["bands"][rung - 1]} does not hold its outcome {shown} as recomputed'))
        ref = (a.get('reference') or {}).get('figure')
        if ref in figs:
            chain = {ref} | _beneath(ref, figs)
            if any(figs[g]['kind'] == 'estimate' for g in chain):
                errors.append(('S5', f'{v}: its reference {ref} is or rests on an estimate'))
            elif any(figs[g]['basis'] == 'forecast' for g in chain):
                errors.append(('S5', f'{v}: its reference {ref} is or rests on a forecast'))
            elif not any(figs[g]['kind'] == 'source' and figs[g]['basis'] in EXTERNAL for g in chain):
                errors.append(('S5', f'{v}: its reference {ref} has no quoted consensus, guidance or outside figure'))
            else:                                          # [D741] a past period's reported share or multiple carried to another period
                carried = sorted(g for g in chain if figs[g]['basis'] == 'reported' and figs[g]['unit'] in ('%', 'x')
                                 and figs[g]['what']['period'] != figs[ref]['what']['period'])
                if carried:
                    errors.append(('S5', f'{v}: its reference {ref} carries the reported {", ".join(carried)} of another period to '
                                         f'{figs[ref]["what"]["period"]}; that makes it our comparison estimate, not the market\'s reference'))
    return errors, outcomes


def _adopted(outcomes, figs):
    """[54] The figures the outcomes adopt: each reached from an outcome (inputs and rests_on) with no figure of its own quantity and
    period between them. A figure beneath another of its own quantity and period (a point a final range rests on) is its basis, not a
    second value."""
    tops, seen_ids = set(), set()

    def walk(fid, keys):
        if fid not in figs or (fid, keys) in seen_ids:
            return
        seen_ids.add((fid, keys))
        f = figs[fid]
        k = _key(f['what'])
        if k not in keys:
            tops.add(fid)
        for r in list(f.get('inputs') or []) + [r for r in f.get('rests_on') or [] if r in figs]:
            walk(r, keys | {k})
    for out in outcomes.values():
        walk(out, frozenset())
    return tops


def _shared(family, figs, outcomes):
    errors = []
    by_key = {}
    for fid in _adopted(outcomes, figs):                   # [54] forecasts the outcomes adopt; an unused alternative is not counted
        if figs[fid]['basis'] == 'forecast':
            by_key.setdefault(_key(figs[fid]['what']), []).append(fid)
    nodes = {}
    for fid, f in figs.items():
        if f['basis'] == 'forecast':
            nodes.setdefault(_key(f['what']), []).append(fid)
    for k, ids in sorted(by_key.items()):
        if len(ids) > 1:
            errors.append(('S4', f'{" | ".join(k)}: {len(ids)} forecasts ({", ".join(sorted(ids))}); compute it once and use that figure'))
    for want in family.get('shared', []):
        key = _key(want)
        node = by_key.get(key) or nodes.get(key, [])
        for v, out in sorted(outcomes.items()):
            reached, stack, seen_ids = [], [out], set()
            while stack:
                fid = stack.pop()
                if fid in seen_ids or fid not in figs:
                    continue
                seen_ids.add(fid)
                f = figs[fid]
                if _key(f['what']) == key:
                    reached.append(fid)
                    if f['basis'] == 'forecast':
                        continue                           # through the forecast figure: what lies beneath it is its basis
                stack.extend(f.get('inputs') or [])
            if not reached:
                continue
            if len(node) != 1:
                errors.append(('S4', f'{v}: uses {" | ".join(key)} but the calculation has {len(node)} forecast figures for it'))
                continue
            bypass = sorted(r for r in reached if r != node[0])      # the walk never descends below the forecast figure
            if bypass:
                errors.append(('S4', f'{v}: uses {", ".join(bypass)} for {" | ".join(key)} beside its forecast figure {node[0]}'))
    return errors


def _part_whole(family, figs, calc, outcomes):
    errors = []
    members = family['members']
    for rel in family.get('relations', []):
        if rel.get('type') != 'part_of' or rel['part'] not in outcomes or rel['whole'] not in outcomes:
            continue
        p_what, w_what = members[rel['part']]['what'], members[rel['whole']]['what']
        pairs = [(outcomes[rel['part']], outcomes[rel['whole']], 'outcome')]
        for period in family.get('compare_periods', []):
            if period == p_what['period']:
                continue
            p_key = (p_what['population'], p_what['measure'], p_what['scope'], period)
            w_key = (w_what['population'], w_what['measure'], w_what['scope'], period)
            for p in _tops(outcomes[rel['part']], p_key, figs):
                for w in _tops(outcomes[rel['whole']], w_key, figs):
                    pairs.append((p, w, period))
        for part, whole, label in pairs:
            pv, wv = calc.interval(part), calc.interval(whole)
            if pv is None or wv is None:
                continue
            if not calc.fits(part, whole):
                errors.append(('S3', f'{label}: the part {part} ({pv[0]:g}–{pv[1]:g}) exceeds the whole {whole} ({wv[0]:g}–{wv[1]:g})'))
    return errors


def _sums(family, figs):
    errors = []
    scopes = family.get('part_scopes', [])
    for f in figs.values():
        if f['kind'] != 'computed' or f['operation'] not in ('sum', 'difference'):
            continue
        fid, ins = f['id'], [figs[i] for i in f['inputs']]
        for ps in scopes:
            same = [i for i in ins if (i['what']['population'], i['what']['measure']) == (ps['population'], ps['measure'])]
            parts = [i for i in same if i['what']['scope'] == ps['part']]
            wholes = [i for i in same if i['what']['scope'] == ps['whole']]
            if not parts or not wholes:
                continue
            if f['operation'] == 'sum':
                if any(_overlap(p['what']['period'], w['what']['period']) for p in parts for w in wholes):
                    errors.append(('S8', f'{fid}: adds {ps["part"]} into {ps["whole"]} for the same period, which already includes it'))
            elif not (ins[0]['what']['scope'] == ps['whole'] and ins[1]['what']['scope'] == ps['part']
                      and ins[0]['what']['period'] == ins[1]['what']['period'] == f['what']['period']
                      and f['what']['scope'] not in (ps['part'], ps['whole'])):
                errors.append(('S8', f'{fid}: a difference may take {ps["part"]} from {ps["whole"]} of the same period only to give the rest'))
        group = ins + [f]
        if len({_quantity(g['what']) for g in group}) != 1:
            continue
        periods = [g['what']['period'] for g in group]
        inputs_periods = periods[:-1]
        if f['operation'] == 'sum' and len(set(inputs_periods)) < len(inputs_periods):
            errors.append(('S8', f'{fid}: adds one quantity for the same period more than once ({", ".join(inputs_periods)})'))
            continue
        if len(set(periods)) == 1:
            continue
        parsed = [_period(p) for p in periods]
        if not any(parsed):
            continue
        if not all(parsed):
            errors.append(('S8', f'{fid}: when periods of one quantity are added or subtracted, write each as FY2027, FY2027 Q3, FY2027 H1 or '
                                 f'FY2027 Q1-Q3 (or CY likewise); got {", ".join(periods)}'))
            continue
        years = {p[0] for p in parsed}
        *parts_p, out = parsed
        if len(years) != 1:
            ok = False
        elif f['operation'] == 'sum':
            total = [q for p in parts_p for q in p[1]]
            ok = len(total) == len(set(total)) and set(total) == out[1]
        else:
            ok = parts_p[1][1] <= parts_p[0][1] and parts_p[0][1] - parts_p[1][1] == out[1]
        if not ok:
            sign = ' + ' if f['operation'] == 'sum' else ' − '
            errors.append(('S8', f'{fid}: {sign.join(periods[:-1])} does not make up {periods[-1]}'))
    return errors


def _recorded(family, figs, outcomes):
    recorded = []
    scopes = family.get('part_scopes', [])
    for f in figs.values():
        fid = f['id']
        if f['kind'] == 'estimate':
            recorded.append({'type': 'estimate', 'figure': fid, 'assumption': f.get('basis_text')})
            rested = {figs[r]['what']['scope'] for r in f.get('rests_on') or [] if r in figs}
            if any({ps['part'], ps['whole']} <= rested for ps in scopes):
                recorded.append({'type': 'part and whole in one estimate', 'figure': fid})
        elif f['kind'] == 'computed':
            money = [figs[i] for i in f['inputs'] if figs[i]['unit'] == 'USD bn']
            if any(_quantity(i['what']) != _quantity(f['what']) for i in money) and f['operation'] != 'share':
                recorded.append({'type': 'conversion between quantities', 'figure': fid})
            if f['operation'] in ('apply_growth', 'product') and any(i['what']['period'] != f['what']['period'] for i in money):
                recorded.append({'type': 'carried across periods', 'figure': fid})
            if f['operation'] == 'sum' and any({ps['part'], ps['whole']} <= {i['what']['scope'] for i in money} for ps in scopes):
                recorded.append({'type': 'part and whole added for different periods', 'figure': fid})
        elif (f.get('qualifier') or 'none') != 'none':
            recorded.append({'type': 'qualified source', 'figure': fid, 'qualifier': f['qualifier']})
    used = set()
    for out in outcomes.values():
        used |= {out} | _beneath(out, figs)
    by_key = {}
    for fid in used:
        by_key.setdefault(_key(figs[fid]['what']), []).append(fid)
    for k, ids in sorted(by_key.items()):
        if len(ids) > 1:
            recorded.append({'type': 'one quantity, several figures', 'figure': sorted(ids)[0], 'figures': sorted(ids), 'what': list(k)})
    return recorded


def check(family, passages, calc):
    figs = {f['id']: f for f in calc['figures'] if isinstance(f.get('id'), str)}
    errors = _structure(family, passages, calc, figs)
    if errors:
        return {'errors': errors, 'recorded': [], 'published': {}}
    engine = _Calc(figs)
    errors = _sources(passages, figs) + _arithmetic(figs, engine)
    for f in figs.values():
        if engine.interval(f['id']) is None and not any(e[1].startswith(f['id'] + ':') for e in errors):
            errors.append(('S2', f'{f["id"]}: the value cannot be evaluated'))
    if errors:
        return {'errors': errors, 'recorded': [], 'published': {}}
    answer_errors, outcomes = _answers(family, figs, engine, calc['answers'])
    errors = answer_errors + _shared(family, figs, outcomes) + _part_whole(family, figs, engine, outcomes) + _sums(family, figs)
    published = {v: list(engine.interval(o)) + [None] for v, o in outcomes.items()}
    return {'errors': errors, 'recorded': _recorded(family, figs, outcomes), 'published': published}


def publish_decision(family, calc, result):
    """'refused' when a check fails; 'held' when a member is unresolved and a declared relation joins it to another member; else
    'publish' (an unresolved member is shown as unresolved)."""
    if result['errors']:
        return 'refused'
    unresolved = {a['view_id'] for a in calc['answers'] if a.get('shape') == 'unresolved'}
    for rel in family.get('relations', []):
        ends = {rel.get('part'), rel.get('whole'), rel.get('later'), rel.get('earlier')} - {None}
        if ends & unresolved and ends - unresolved:
            return 'held'
    return 'publish'
