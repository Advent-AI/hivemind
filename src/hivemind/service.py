"""Read-only answers over the views ledger, as of a calendar day (docs/poc/service.md).

Nothing here reads the clock (D12, D13): every function takes `as_of`, a day, and the default is the ledger's last
completed day. A row is visible as of a day when the sequence number it was written under belongs to an item or a
daily round dated on or before that day. Nothing here writes.
"""
import json
import re
from decimal import Decimal

from .views import store

TIER_FACT = '发生的事'
COMPARATORS = ('>=', '<', '=')


def open_ledger(path):
    """A read-only connection to a views database."""
    return store.open_read_only(path)


def default_as_of(conn):
    return store.last_completed_day(conn) or conn.execute('select max(publication_day) from judgements').fetchone()[0]


_SEQ_DAYS = {}      # id(connection) → (connection, (max sequence, rows), map); a sqlite3 connection cannot carry attributes


def seq_day_map(conn):
    """sequence number → the publication day of the item or daily round written under it. Cached per connection and
    rebuilt when processing_steps has grown (an open ledger gains steps while the pipeline runs); without the cache
    one view with 367 pieces of evidence cost 1,224 full scans (0.46 s, measured 2026-10-24)."""
    stamp = tuple(conn.execute('select max(sequence_no), count(*) from processing_steps').fetchone())
    entry = _SEQ_DAYS.get(id(conn))
    if entry is not None and entry[0] is conn and entry[1] == stamp:
        return entry[2]
    cache = {}
    for seq, day in conn.execute('select sequence_no, min(publication_day) from processing_steps where sequence_no > 0 group by sequence_no'):
        cache[seq] = day
    if len(_SEQ_DAYS) >= 64:
        _SEQ_DAYS.clear()
    _SEQ_DAYS[id(conn)] = (conn, stamp, cache)
    return cache


def day_of_seq(conn, seq):
    return seq_day_map(conn).get(seq)


def visible(conn, seq, as_of):
    day = day_of_seq(conn, seq)
    return day is not None and day <= as_of


# ---------- views

def view_exists(conn, record, as_of):
    return visible(conn, record['created_seq'], as_of)


def is_open_as_of(conn, view_id, as_of):
    for row in conn.execute('select open, after_seq from view_switches where view_id=? order by id desc', (view_id,)):
        if visible(conn, row['after_seq'], as_of):
            return bool(row['open'])
    return True


def state_as_of(conn, view_id, as_of):
    """The last judgement on or before the day, with the day the current position was first taken."""
    rows = [dict(r) for r in conn.execute('select judgement_id, seq, rung, changed, why_changed, reasons, publication_day from judgements where view_id=? and publication_day<=? order by judgement_id', (view_id, as_of))]
    if not rows:
        return None
    last = rows[-1]
    since, previous = last['publication_day'], None
    for row in reversed(rows[:-1]):
        if row['rung'] != last['rung']:
            previous = row['rung']
            break
        since = row['publication_day']
    return {'position': last['rung'], 'judgement_day': last['publication_day'], 'since_day': since, 'previous_position': previous,
            'rounds': len(rows), 'why_changed': last['why_changed'], 'reasons': last['reasons']}


def summaries(conn, as_of=None, include_closed=False):
    """Every view as of the day as a light record (id, object, kind, what it looks at, the question, due day, open,
    dependency and dependant ids): what a search ranks. The full record with its evidence counts is `view`; listing
    92 of those cost 0.29 s per search (1,205 evidence reads), measured 2026-10-24."""
    as_of = as_of or default_as_of(conn)
    out = []
    for record in conn.execute('select * from views order by created_seq'):
        record = dict(record)
        if not view_exists(conn, record, as_of):
            continue
        is_open = is_open_as_of(conn, record['view_id'], as_of)
        if not include_closed and not is_open:
            continue
        out.append({'view_id': record['view_id'], 'object': record['object_id'], 'object_kind': record['object_kind'], 'kind': record['kind'],
                    'looks_at': record['looks_at'], 'question': record['question'], 'due_day': record['due_day'], 'open': is_open,
                    'dependencies': [d['view_id'] for d in dependencies(conn, record['view_id'], as_of)], 'dependants': dependants(conn, record['view_id'], as_of)})
    return out


def views(conn, object_id=None, as_of=None, include_closed=False):
    as_of = as_of or default_as_of(conn)
    rows = conn.execute('select * from views' + (' where object_id=?' if object_id else '') + ' order by created_seq', (object_id,) if object_id else ()).fetchall()
    out = []
    for record in rows:
        record = dict(record)
        if not view_exists(conn, record, as_of):
            continue
        if not include_closed and not is_open_as_of(conn, record['view_id'], as_of):
            continue
        out.append(view(conn, record['view_id'], as_of, record=record))
    return out


def dependencies(conn, view_id, as_of):
    """The view's dependencies recorded on or before the day, each pointing at the target resolved on or before it."""
    out = []
    for dep in conn.execute('select * from dependencies where view_id=? order by dependency_id', (view_id,)):
        if not visible(conn, dep['seq'], as_of):
            continue
        target = dep['depends_on']
        for res in conn.execute('select resolved_to, seq from dependency_resolutions where dependency_id=? order by id desc', (dep['dependency_id'],)):
            if visible(conn, res['seq'], as_of):
                target = res['resolved_to']
                break
        out.append({'view_id': target, 'direction': dep['direction'], 'wait_chain_view_id': dep['wait_chain_view_id'], 'wait_year': dep['wait_year'], 'since_day': day_of_seq(conn, dep['seq'])})
    return out


def dependants(conn, view_id, as_of):
    """The views recorded on or before the day as depending on this one (directly or by a resolution)."""
    direct = [r['view_id'] for r in conn.execute('select view_id, seq from dependencies where depends_on=?', (view_id,)) if visible(conn, r['seq'], as_of)]
    resolved = [r['view_id'] for r in conn.execute('select d.view_id, r.seq from dependency_resolutions r join dependencies d on d.dependency_id=r.dependency_id where r.resolved_to=?', (view_id,)) if visible(conn, r['seq'], as_of)]
    return sorted(set(direct + resolved))


def view(conn, view_id, as_of=None, record=None):
    as_of = as_of or default_as_of(conn)
    record = record or store.view(conn, view_id)
    if not record or not view_exists(conn, record, as_of):
        return None
    rungs = store.rungs_of(conn, view_id)
    state = state_as_of(conn, view_id, as_of)
    if state:
        rung = next((r for r in rungs if r['position'] == state['position']), None)
        state['label'] = rung['label'] if rung else None
        state['condition'] = rung['condition'] if rung else None
    in_force = evidence(conn, view_id, as_of)
    return {
        'view_id': view_id, 'object': record['object_id'], 'object_kind': record['object_kind'], 'kind': record['kind'],
        'looks_at': record['looks_at'], 'question': record['question'], 'due_day': record['due_day'], 'year': record['year'],
        'created_day': day_of_seq(conn, record['created_seq']), 'created_from': record['created_from_input'],
        'as_of': as_of, 'open': is_open_as_of(conn, view_id, as_of), 'rungs': rungs, 'state': state,
        'dependencies': dependencies(conn, view_id, as_of), 'dependants': dependants(conn, view_id, as_of),
        'counts': {'rounds': state['rounds'] if state else 0, 'evidence': len(in_force), 'facts': sum(1 for e in in_force if e['tier'] == TIER_FACT)},
    }


# ---------- evidence

def evidence_record(conn, evidence_id, as_of, arrived_seq=None):
    """One piece of evidence with only the sources recorded on or before the day (a later outlet of the same
    sentence is not yet known on that day)."""
    piece = store.evidence(conn, evidence_id)
    if not piece:
        return None
    sources = [dict(s) for s in conn.execute('select input_id, category, publication_day, seq from evidence_sources where evidence_id=? order by id', (evidence_id,)) if visible(conn, s['seq'], as_of)]
    replaces = conn.execute('select old_evidence_id, seq from replacements where new_evidence_id=?', (evidence_id,)).fetchone()
    return {'evidence_id': piece['evidence_id'], 'one_line': piece['one_line'], 'quote': piece['quote'], 'tier': piece['tier'],
            'speaker': piece['speaker'], 'original_who': piece['original_who'], 'original_day': piece['original_day'], 'event_time': piece['event_time'],
            'day': day_of_seq(conn, arrived_seq if arrived_seq is not None else piece['created_seq']), 'sources': sources, 'outlets': len(sources),
            'replaces': replaces['old_evidence_id'] if replaces and visible(conn, replaces['seq'], as_of) else None}


def evidence(conn, view_id, as_of=None, tier=None):
    """Evidence linked to the view on or before the day and not replaced on or before it, with its sources."""
    as_of = as_of or default_as_of(conn)
    out = []
    for link in conn.execute('select evidence_id, seq from evidence_links where view_id=? order by id', (view_id,)):
        if not visible(conn, link['seq'], as_of):
            continue
        replacement = conn.execute('select new_evidence_id, said_day, seq from replacements where old_evidence_id=? order by id desc limit 1', (link['evidence_id'],)).fetchone()
        if replacement and visible(conn, replacement['seq'], as_of):
            continue
        piece = evidence_record(conn, link['evidence_id'], as_of, link['seq'])
        if tier and piece['tier'] != tier:
            continue
        out.append(piece)
    return out


# ---------- history

def history(conn, view_id, from_day=None, to_day=None):
    to_day = to_day or default_as_of(conn)
    from_day = from_day or '0000-00-00'
    judgements = []
    previous = None
    for row in conn.execute('select * from judgements where view_id=? order by judgement_id', (view_id,)):
        entry = {'day': row['publication_day'], 'seq': row['seq'], 'position': row['rung'], 'changed': bool(row['changed']), 'moved_from': previous if previous is not None and previous != row['rung'] else None,
                 'why_changed': row['why_changed'], 'reasons': row['reasons'], 'cited': _json(row['cited_evidence_json']), 'pushes': _json(row['pushes_json']), 'round': row['input_id']}
        previous = row['rung']
        if from_day <= row['publication_day'] <= to_day:
            judgements.append(entry)
    arrivals = {}
    for link in conn.execute('select evidence_id, seq from evidence_links where view_id=?', (view_id,)):
        day = day_of_seq(conn, link['seq'])
        if day and from_day <= day <= to_day:
            piece = store.evidence(conn, link['evidence_id'])
            bucket = arrivals.setdefault(day, {'evidence': 0, 'facts': 0})
            bucket['evidence'] += 1
            bucket['facts'] += int(piece['tier'] == TIER_FACT)
    replacements = [{'day': day_of_seq(conn, r['seq']), 'old': r['old_evidence_id'], 'new': r['new_evidence_id'], 'said_day': r['said_day']}
                    for r in conn.execute('select r.* from replacements r join evidence_links l on l.evidence_id=r.new_evidence_id where l.view_id=?', (view_id,))
                    if day_of_seq(conn, r['seq']) and from_day <= day_of_seq(conn, r['seq']) <= to_day]
    switches = [{'day': day_of_seq(conn, s['after_seq']), 'open': bool(s['open']), 'reason': s['reason']}
                for s in conn.execute('select * from view_switches where view_id=? order by id', (view_id,)) if day_of_seq(conn, s['after_seq']) and from_day <= day_of_seq(conn, s['after_seq']) <= to_day]
    return {'view_id': view_id, 'from_day': from_day, 'to_day': to_day, 'judgements': judgements,
            'changes': [j for j in judgements if j['moved_from'] is not None], 'arrivals': dict(sorted(arrivals.items())),
            'replacements': replacements, 'switches': switches}


class LedgerError(ValueError):
    """A ledger record the service cannot read (corrupt JSON): refused, never read as empty."""


def _json(text):
    if not text:
        return []
    try:
        return json.loads(text)
    except ValueError as error:
        raise LedgerError(f'a judgement record holds invalid JSON: {text[:60]!r}') from error


# ---------- the processing record

def record(conn, view_id, as_of=None):
    """The last check of the view on or before the day: when, by which round, how much came in that day."""
    as_of = as_of or default_as_of(conn)
    row = conn.execute('select input_id, publication_day, seq from judgements where view_id=? and publication_day<=? order by judgement_id desc limit 1', (view_id, as_of)).fetchone()
    if not row:
        return {'view_id': view_id, 'as_of': as_of, 'last_check': None}
    day = row['publication_day']
    items = [r['input_id'] for r in conn.execute("select distinct input_id from processing_steps where publication_day=? and step='handed_over' and result='ok' and input_id not like 'day:%'", (day,))]
    arrived = sum(1 for link in conn.execute('select seq from evidence_links where view_id=?', (view_id,)) if day_of_seq(conn, link['seq']) == day)
    return {'view_id': view_id, 'as_of': as_of, 'last_check': {'day': day, 'round': row['input_id'], 'items_processed_that_day': len(items), 'evidence_arrived_that_day': arrived}}


# ---------- changes since a day

def changes(conn, since_day, to_day=None):
    """Judgements that said 'changed' after since_day (exclusive) up to to_day, with their cited evidence."""
    to_day = to_day or default_as_of(conn)
    out = []
    previous = {}
    for row in conn.execute('select * from judgements order by judgement_id'):
        before = previous.get(row['view_id'])
        previous[row['view_id']] = row['rung']
        if not row['changed'] or not (since_day < row['publication_day'] <= to_day):
            continue
        cited = [piece for piece in (evidence_record(conn, e, row['publication_day']) for e in _json(row['cited_evidence_json'])) if piece]
        out.append({'view_id': row['view_id'], 'day': row['publication_day'], 'from_position': before, 'to_position': row['rung'],
                    'position_moved': before is not None and before != row['rung'], 'why_changed': row['why_changed'], 'cited': cited})
    return out


# ---------- a claim against a ladder
#
# A rung's condition is a sentence like "不低于 1650 亿美元且不高于 1690 亿美元，处于公司指引区间". The band is read from
# the comparator words and the amount that follows each; remarks after ；or ， are not part of it. The ladder is
# evaluable only when its bands form one unbroken partition of the line (06-views: 格和格不重叠、不留空), so a
# condition the parser cannot read makes the whole ladder "not evaluable" rather than a wrong verdict.

INF = float('inf')
UNIT_USD = {'万亿': Decimal('1e12'), '千亿': Decimal('1e11'), '亿': Decimal('1e8'), '万': Decimal('1e4'), None: Decimal(1)}   # exact: 269.79亿 is 26,979,000,000, not ...000.000004
# an amount: a number with a Chinese magnitude or followed by 美元; a bare number counts only right after a comparator
# or a range separator (大于或等于0, 小于-10亿), so years (2026年, FY2026) and model names (H100) are not amounts
AMOUNT_TOKEN = re.compile(r'(?<![A-Za-z\d.])(-?\d[\d,]*(?:\.\d+)?)\s*(万亿|千亿|亿|万)?(\s*美元)?')
COMPARATORS_RE = [
    ('lo_inc', re.compile(r'不低于|不少于|至少|大于或等于|大于等于|达到或超过|达到(?!或)|≥|>=')),
    ('lo_exc', re.compile(r'(?<!不)高于|(?<![不或])超过|大于(?!或等于|等于)|多于|>(?!=)')),
    ('hi_inc', re.compile(r'不高于|不超过|至多|小于或等于|小于等于|≤|<=')),
    ('hi_exc', re.compile(r'(?<!不)低于|不足|不到|(?<!不)少于|小于(?!或等于|等于)|<(?!=)')),
    ('exact', re.compile(r'恰为|恰好为|恰好|(?<![或大小])等于')),
]


def _comparators(clause):
    """(start, end, kind) for every comparator word, the longest match winning where words overlap
    ("大于或等于" is one lower-inclusive comparator, not also a "大于" and an "等于")."""
    found = []
    for kind, regex in COMPARATORS_RE:
        for match in regex.finditer(clause):
            found.append((match.start(), match.end(), kind))
    found.sort(key=lambda m: (m[0], -(m[1] - m[0])))
    kept = []
    for start, end, kind in found:
        if kept and start < kept[-1][1]:          # inside the previous, longer match
            continue
        kept.append((start, end, kind))
    return kept
POSTFIX_LO = re.compile(r'\s*(?:及以上|或以上|以上)')
POSTFIX_HI = re.compile(r'\s*(?:及以下|以下|以内)')
RANGE_SEP = re.compile(r'\s*(?:至|到|~|–|—)\s*(?:不足|低于)?\s*')


def operative_clause(condition):
    """The part of a condition that states the bound: the first clause (split at ；or ，) that names a money amount,
    joined with the clauses that continue it (且 / 并且 / 但 / 或 / 并); a dateline before it ("截至2026-12-31，") and a
    remark after it ("，处于公司指引区间", "；与公司所称…相符") are dropped. Parenthesised asides are removed first."""
    text = re.sub(r'（[^）]*）|\([^)]*\)', '', condition)
    clauses = [c for c in re.split(r'[；，;]', text) if c.strip()]
    chosen = []
    for clause in clauses:
        if not chosen:
            if _amounts(clause):
                chosen.append(clause)
        elif re.match(r'\s*(?:且|并且|并|但|或)', clause):
            chosen.append(clause)
        else:
            break
    return ''.join(chosen)


def _amounts(text):
    """(start, end, value_usd) for every money amount in the clause: a number with a Chinese magnitude or followed
    by 美元, or a bare zero ("大于或等于0", "小于0"). A bare non-zero number is not money (30%, 4吉瓦, 2025年)."""
    out = []
    for match in AMOUNT_TOKEN.finditer(text):
        number, unit, dollars = match.group(1), match.group(2), match.group(3)
        value = float(Decimal(number.replace(',', '')) * UNIT_USD[unit])
        following = text[match.end():match.end() + 1]
        if unit is None and dollars is None and (value != 0 or following not in ('', '且', '、', '，', '；', '）', ' ', '美', '至', '到')):
            continue          # 30%, 0%, 4吉瓦, 1个百分点, 2025年: not money
        out.append((match.start(), match.end(), value))
    return out


def band(condition):
    """(lo, lo_inclusive, hi, hi_inclusive) in USD, open ends as ±inf, read from the comparator words and the amount
    each binds to ("不低于 1650 亿美元且不高于 1690 亿美元"), a range ("650亿美元至720亿美元（含两端）", "0至不足1000亿"),
    a postfix ("9000亿美元及以上") or an exact amount ("恰为2500亿美元"). Remarks after ；or ， and parenthesised
    asides are not read. None when the condition names no amount or reads inconsistently."""
    clause = operative_clause(condition or '')
    inclusive_ends = bool(re.search(r'含两端|含端|包含两端', condition or ''))
    amounts = _amounts(clause)
    lo, lo_inc, hi, hi_inc, found = -INF, False, INF, False, False

    def next_amount(after):
        for start, end, value in amounts:
            if start >= after:
                return start, end, value
        return None

    for start, end, kind in _comparators(clause):
        hit = next_amount(end)
        if not hit or hit[0] - end > 40:
            continue
        value = hit[2]
        if kind == 'exact':
            return (value, True, value, True)
        if kind == 'lo_inc':
            lo, lo_inc = value, True
        elif kind == 'lo_exc':
            lo, lo_inc = value, False
        elif kind == 'hi_inc':
            hi, hi_inc = value, True
        else:
            hi, hi_inc = value, False
        found = True
    for start, end, value in amounts:
        tail = clause[end:]
        if POSTFIX_LO.match(tail):
            lo, lo_inc, found = value, True, True
        elif POSTFIX_HI.match(tail):
            hi, hi_inc, found = value, True, True
        sep = RANGE_SEP.match(tail)
        if sep:
            partner = next_amount(end + sep.end())
            if partner and partner[0] == end + sep.end() and partner[2] > value:
                lo, lo_inc, hi, found = value, True, partner[2], True
                hi_inc = inclusive_ends or not re.search(r'不足|低于', sep.group(0))
    if not found:
        return None
    if lo > hi or (lo == hi and not (lo_inc and hi_inc)):
        return None
    return (lo, lo_inc, hi, hi_inc)


def ladder_bands(rungs):
    """Every rung's band, or None with the reason when the ladder is not one unbroken partition by amount."""
    bands = [(r['position'], band(r['condition'])) for r in rungs]
    unreadable = [p for p, b in bands if b is None]
    if unreadable:
        return None, f'conditions not read as amounts: positions {unreadable}'
    ordered = sorted(bands, key=lambda pb: (pb[1][0], pb[1][2]))
    for (p1, a), (p2, b) in zip(ordered, ordered[1:]):
        if a[2] != b[0] or a[3] == b[1]:          # adjacent bands share the boundary amount and exactly one of them owns it
            return None, f'bands of positions {p1} and {p2} overlap or leave a gap'
    lowest, highest = ordered[0][1], ordered[-1][1]
    if not (lowest[0] == -INF or (lowest[0] == 0 and lowest[1])) or highest[2] != INF:     # an amount that cannot be negative may start at 0
        return None, 'the ladder does not cover the line up to +inf'
    return dict(bands), None


def _contains(b, yi):
    lo, lo_inc, hi, hi_inc = b
    return (lo < yi or (lo == yi and lo_inc)) and (yi < hi or (yi == hi and hi_inc))


def verdict_for(comparator, judged, yi):
    """Whether every value in the judged band satisfies the claim (holds), none does (not_yet), or some do."""
    lo, lo_inc, hi, hi_inc = judged
    all_at_least = lo > yi or (lo == yi)                       # every value >= yi (lo == yi exclusive gives values > yi)
    all_below = hi < yi or (hi == yi and not hi_inc)
    if comparator == '>=':
        return 'holds' if all_at_least else 'not_yet' if all_below else 'borderline'
    if comparator == '<':
        return 'holds' if all_below else 'not_yet' if all_at_least else 'borderline'
    if lo == hi == yi:
        return 'holds'
    return 'borderline' if _contains(judged, yi) else 'not_yet'


def evaluate(conn, view_id, comparator, value_usd, as_of=None):
    """A claim "quantity >= / < / = value" against the view's ladder as of the day: the rung the threshold sits in,
    the judged rung, and whether every value of the judged band satisfies the claim (holds), none does (not_yet), or
    only some do (borderline). Only a ladder whose rungs read as one unbroken partition by amount is evaluated."""
    as_of = as_of or default_as_of(conn)
    if comparator not in COMPARATORS:
        raise ValueError(f'comparator must be one of {COMPARATORS}')
    record = view(conn, view_id, as_of)
    if not record:
        return None
    yi = float(value_usd)          # bands are in USD too
    bands, problem = ladder_bands(record['rungs'])
    if bands is None:
        return {'view_id': view_id, 'as_of': as_of, 'evaluable': False, 'reason': problem}
    claim_position = next((p for p, b in bands.items() if _contains(b, yi)), None)
    state = record['state']
    if not state:
        return {'view_id': view_id, 'as_of': as_of, 'evaluable': True, 'comparator': comparator, 'value_usd': value_usd, 'claim_position': claim_position, 'judged_position': None, 'verdict': 'not_judged'}
    return {'view_id': view_id, 'as_of': as_of, 'evaluable': True, 'comparator': comparator, 'value_usd': value_usd,
            'claim_position': claim_position, 'judged_position': state['position'], 'judged_label': state['label'], 'judged_condition': state['condition'],
            'verdict': verdict_for(comparator, bands[state['position']], yi)}
