"""Links between number questions, chosen in the matching step (D51, D368 item 2, D694, D695; the design and its four tables:
docs/research/2026-11-20-production-readiness/dependency-design/DESIGN.md).

Under the matching engine `jev-links` only, after matching has settled which candidates open: for each newly opened number question
C and each open number question T on C's list, Jev is asked whether one should be judged with the other's conclusion in view (READS)
and, for a pair that should, which way the read question moves the reading one (SIGN). Code decides only identity: which pairs are
number questions, the canonical candidate, circles, and the label the judge is shown (from the sign and the typed rung bounds). A
link is written with kind `reads`: judging reads it as a dependency; filing does not treat it as a narrower home (D694 (a)).
"""
import json

from .. import jev, model, vocabulary
from . import identity, jev_matching, store

ENGINE = 'jev-links'
KIND = 'reads'
THRESHOLD = jev_matching.THRESHOLD
LABELS = vocabulary.ASSET_LABELS                 # five-rung asset ladders run Strongly bullish .. Strongly bearish, or the reverse
CANDIDATE_READS, THESIS_READS, NEITHER = 'candidate_reads_thesis', 'thesis_reads_candidate', 'neither'
TOGETHER, OPPOSITE, NO_SIGN = 'together', 'opposite', 'no_clear_sign'

READS = {
    CANDIDATE_READS: "the CANDIDATE should be judged with the THESIS's current conclusion in view, because the THESIS's answer bounds "
                     "or drives the CANDIDATE's: a part read against its whole (one product line's sales against the company's total "
                     "sales; one region's loan book against the bank's total loans), or a quantity read against another it depends on "
                     "(a component supplier's revenue against its largest customer's capital spending; an airline's fuel bill against "
                     "its fuel volume)",
    THESIS_READS: "the THESIS should be judged with the CANDIDATE's current conclusion in view, for the same reasons with the roles swapped",
    NEITHER: "neither answer bounds or drives the other: unrelated quantities (a retailer's gross margin and its store openings in "
             "another country), or the same quantity for the same period and scope; sharing a company, industry or topic is not enough",
}
SIGN = {
    TOGETHER: "a higher answer to the question read makes a higher answer to the question reading it more likely (a company's total "
              "sales and one product line's sales, when that line's share of the total holds steady; a customer's capital spending "
              "and its component supplier's revenue)",
    OPPOSITE: "a higher answer to the question read makes a lower answer to the question reading it more likely (an airline's fuel "
              "bill and its operating margin; a retailer's markdowns and its gross margin)",
    NO_SIGN: "the question read only caps the other without moving its most likely answer (a regulator's cap on a bank's fees set far "
             "above what it charges), or the supplied text does not show which way it moves it",
}
# links-v2 (D703, D705; docs/research/2026-11-21-whole-window/WORDING-V2.md): links-v1 with a tie-break by the stronger full-period
# anchor, links across periods only when the supplied text states how, and a base-effect example of the opposite sign
READS_V2 = {
    CANDIDATE_READS: "the CANDIDATE should be judged with the THESIS's current conclusion in view, because the THESIS's answer bounds "
                     "or drives the CANDIDATE's: a part read against its whole (one product line's sales against the company's total "
                     "sales; one region's loan book against the bank's total loans), or a quantity read against another it depends on "
                     "(a component supplier's revenue against its largest customer's capital spending; an airline's fuel bill against "
                     "its fuel volume) When either question could be judged with the other in view, the one whose answer the supplied "
                     "text anchors less (no guidance, consensus or reported figure for the quantity and full period the question asks "
                     "about) is the one judged with the other's conclusion in view.",
    THESIS_READS: READS[THESIS_READS],
    NEITHER: "neither answer bounds or drives the other: unrelated quantities (a retailer's gross margin and its store openings in "
             "another country), or the same quantity for the same period and scope, or quantities of different periods when the "
             "supplied text does not state how one period's answer moves the other's (a retailer's sales this year and its sales "
             "growth next year, when the text only names both); sharing a company, industry or topic is not enough",
}
SIGN_V2 = {
    TOGETHER: SIGN[TOGETHER],
    OPPOSITE: "a higher answer to the question read makes a lower answer to the question reading it more likely (an airline's fuel "
              "bill and its operating margin; a retailer's markdowns and its gross margin; one year's sales and the next year's sales "
              "growth at a given next-year level, since a higher base lowers the growth)",
    NO_SIGN: SIGN[NO_SIGN],
}
QUESTION_SETS = {'links-v1': (READS, SIGN), 'links-v2': (READS_V2, SIGN_V2)}     # config.LINK_QUESTIONS names the same versions
READS_INSTRUCTIONS = ("Should one of these two questions be judged with the other's current conclusion in view? Use only the supplied "
                      "text. THESIS:\n")
SIGN_INSTRUCTIONS = {
    CANDIDATE_READS: "If the THESIS's answer turned out higher, which way would that move the CANDIDATE's most likely answer? Use only the supplied text. THESIS:\n",
    THESIS_READS: "If the CANDIDATE's answer turned out higher, which way would that move the THESIS's most likely answer? Use only the supplied text. THESIS:\n",
}


class Refused(RuntimeError):
    """The link step cannot finish for this article (a persistent circle, an unbound waiting row, a Jev failure); `record` says why."""

    def __init__(self, message, record):
        super().__init__(message)
        self.record = record


def reads_question(text, excluded=None, note='', version='links-v1'):
    criteria = {k: v for k, v in QUESTION_SETS[version][0].items() if k != excluded}
    return {'type': 'choice', 'criteria': criteria, 'instructions': READS_INSTRUCTIONS.replace('THESIS:\n', (note + ' ' if note else '') + 'THESIS:\n') + text}


def sign_question(text, direction, version='links-v1'):
    return {'type': 'choice', 'criteria': dict(QUESTION_SETS[version][1]), 'instructions': SIGN_INSTRUCTIONS[direction] + text}


# ---------- identity: which ladders are number ladders, and the label ----------

def typed_direction(rungs):
    """-1 when the values fall from the first rung to the last, +1 when they rise, None otherwise. Each rung is [lo, hi) of its typed
    bounds; only the first and last rung may leave one outer end open; an interval with lo >= hi is invalid; adjacent rungs may
    touch. Prose is never read."""
    if len(rungs) < 2:
        return None
    intervals = []
    for index, rung in enumerate(rungs):
        lo, hi = rung.get('lo'), rung.get('hi')
        outer = index in (0, len(rungs) - 1)
        if (lo is None and hi is None) or ((lo is None or hi is None) and not outer):
            return None
        if lo is not None and hi is not None and float(lo) >= float(hi):
            return None
        intervals.append((None if lo is None else float(lo), None if hi is None else float(hi)))

    def at_or_below(lower, upper):
        return lower[1] is not None and upper[0] is not None and lower[1] <= upper[0]

    pairs = list(zip(intervals, intervals[1:]))
    if all(at_or_below(after, before) for before, after in pairs):
        return -1
    if all(at_or_below(before, after) for before, after in pairs):
        return 1
    return None


def favourable_end(rungs):
    """'first' or 'last': the end whose stored label is Strongly bullish, on a five-rung ladder carrying the canonical labels in order
    or reversed; None otherwise."""
    labels = [vocabulary.canonical('label', r['label']) for r in rungs]
    if labels == LABELS:
        return 'first'
    if labels == LABELS[::-1]:
        return 'last'
    return None


def label_for(reader_rungs, read_rungs, sign):
    """The existing direction label (`first_is_bullish` / `last_is_bullish`): which end of the read question's ladder is favourable for
    the reading asset question, given the sign; None when undecidable."""
    reader_direction, read_direction, favourable = typed_direction(reader_rungs), typed_direction(read_rungs), favourable_end(reader_rungs)
    if None in (reader_direction, read_direction, favourable) or sign not in (TOGETHER, OPPOSITE):
        return None
    reader_high = 'first' if reader_direction == -1 else 'last'
    favourable_is_high = favourable == reader_high
    want_read_high = favourable_is_high if sign == TOGETHER else not favourable_is_high
    read_high = 'first' if read_direction == -1 else 'last'
    end = read_high if want_read_high else ('last' if read_high == 'first' else 'first')
    return 'first_is_bullish' if end == 'first' else 'last_is_bullish'


def is_number_question(kind, rungs, measure):
    """D695: an asset question with a five-rung number ladder (canonical labels, typed direction) and a measure that is not an event."""
    return (kind == 'asset' and len(rungs) == 5 and bool(measure) and measure not in identity.EVENT_MEASURES
            and typed_direction(rungs) is not None and favourable_end(rungs) is not None)


def stored_is_number_question(conn, view_id):
    v, key = store.view(conn, view_id), store.view_key(conn, view_id)
    return bool(v) and is_number_question(v['kind'], store.rungs_of(conn, view_id), (key or {}).get('measure'))


def candidate_rungs(conn, c, outcome, target):
    """The candidate's rungs as the writer will store them (a successor is oriented like its predecessor)."""
    if outcome == 'succession' and target:
        from .writing import oriented_like
        return oriented_like(c, store.rungs_of(conn, target), [])['rungs']
    return c['rungs']


# ---------- the reading graph ----------

def stored_edges(conn):
    """Every stored dependency at its effective target (a bound wait counts through the question it is bound to)."""
    edges = {}
    for (view_id,) in conn.execute('select distinct view_id from dependencies'):
        for dep in store.dependencies_of(conn, view_id):
            if dep['resolved_to']:
                edges.setdefault(view_id, set()).add(dep['resolved_to'])
    return edges


def unbound_waits(conn):
    return conn.execute("select count(*) from dependencies where coalesce(depends_on, '')='' and coalesce(wait_year, '')!='' "
                        "and dependency_id not in (select dependency_id from dependency_resolutions)").fetchone()[0]


def circles(conn, proposed):
    """The proposed links (reader, read) that lie on a circle of the stored relation plus every proposed link, each with one path."""
    graph = {k: set(v) for k, v in stored_edges(conn).items()}
    for link in proposed:
        graph.setdefault(link['reader'], set()).add(link['read'])
    found = []
    for link in proposed:
        stack, seen = [(link['read'], [link['reader'], link['read']])], set()
        while stack:
            node, path = stack.pop()
            if node == link['reader']:
                found.append((link, path))
                break
            if node in seen:
                continue
            seen.add(node)
            stack.extend((nxt, path + [nxt]) for nxt in sorted(graph.get(node, ())))
    return found


# ---------- selection ----------

def _ask(archive, cfg, jobs, transport, record, stage):
    """One Jev request per job, asked in order; each job is written into the record before it is sent (its request sha, whether the
    archive held it) and completed as it is answered (its call id). A failure names the failing job's sha and leaves the later jobs
    marked not asked."""
    entries = []
    for state, questions in jobs:
        _, sha = model.request_identity(jev.request_for(cfg.matching, state, questions))
        entries.append({'stage': stage, 'request_sha256': sha, 'questions': sorted(questions), 'archived_before': bool(archive.lookup(sha)),
                        'status': 'not asked'})
    record['calls'].extend(entries)
    replies = []
    for entry, (state, questions) in zip(entries, jobs):
        try:
            reply = jev.ask(archive, cfg, cfg.matching, state, questions, 'match', transport=transport)
        except Exception as error:
            entry['status'] = 'failed'
            record['error'] = f'{type(error).__name__}: {error}'[:300]
            record['failed_request_sha256'] = entry['request_sha256']
            raise Refused(f'link question failed: {record["error"]}', record) from error
        entry['status'], entry['call_id'] = 'answered', reply.call_id
        replies.append(reply.data)
    return replies


def _passes(answer, accepted):
    choice = answer['choice']
    return choice if choice in accepted and answer['probabilities'][choice] >= THRESHOLD else None


def choose(archive, cfg, conn, handover, checked, lists, shown_views, *, transport=None):
    """The links this article proposes: [{'reader', 'read', 'candidate', 'direction', 'sign'}], reader and read being a candidate id
    (canonical) or a stored view id; and the record of how they were chosen. Raises Refused for an unbound waiting row, a Jev
    failure or a circle that remains after one correction (PRD 06)."""
    record = {'pairs': [], 'calls': [], 'corrections': [], 'proposed': []}
    if unbound_waits(conn):
        record['error'] = 'the store holds an unbound waiting dependency row'
        raise Refused(record['error'], record)
    aliases, problems = identity.batch_plan(handover.candidates, checked.outcomes)
    if problems:                                   # the writer refuses the same plan (WriteConflict); nothing to ask
        record['skipped'] = problems
        return [], record
    evidence = handover.evidence
    stage1, asked = [], []
    for c in handover.candidates:
        outcome, target, _ = checked.outcomes.get(c['id'], ('skip', None, []))
        if outcome not in ('new', 'succession') or aliases.get(c['id']) != c['id']:
            continue
        rungs = candidate_rungs(conn, c, outcome, target)
        if not is_number_question(c['kind'], rungs, c.get('measure')):
            record['pairs'].append({'candidate': c['id'], 'eligible': False, 'why': 'not a number question'})
            continue
        listed = list(dict.fromkeys(list(lists.candidate_lists.get(c['id'], [])) + [v['view_id'] for v in shown_views]))
        theses = []
        for view_id in listed:
            ok = store.is_open(conn, view_id) and stored_is_number_question(conn, view_id)
            record['pairs'].append({'candidate': c['id'], 'thesis': view_id, 'eligible': ok})
            if ok:
                theses.append(view_id)
        if theses:
            state = jev_matching.candidate_state(c, evidence)
            stage1.append((state, {f'reads__{v}': reads_question(jev_matching.thesis_text(conn, v), version=cfg.matching.link_questions) for v in theses}))
            asked.append((c, state, theses))
    if not stage1:
        return [], record
    answers = _ask(archive, cfg, stage1, transport, record, 'reads')
    directions = {}
    for (c, state, theses), reply in zip(asked, answers):
        for view_id in theses:
            answer = reply[f'reads__{view_id}']
            direction = _passes(answer, (CANDIDATE_READS, THESIS_READS))
            record['pairs'].append({'candidate': c['id'], 'thesis': view_id, 'reads': answer['choice'], 'probabilities': answer['probabilities']})
            if direction:
                directions[(c['id'], view_id)] = direction
    links = _signed(archive, cfg, conn, asked, directions, transport, record)
    on_circle = circles(conn, links)
    if on_circle:
        links = _corrected(archive, cfg, conn, asked, directions, links, on_circle, transport, record)
        remaining = circles(conn, links)
        if remaining:
            record['error'] = 'persistent cycle: ' + '; '.join(' -> '.join(path) for _, path in remaining)
            raise Refused(record['error'], record)
    record['proposed'] = links
    return links, record


def _signed(archive, cfg, conn, asked, directions, transport, record, stage='sign'):
    jobs, owners = [], []
    for c, state, theses in asked:
        questions = {f'sign__{v}': sign_question(jev_matching.thesis_text(conn, v), directions[(c['id'], v)], version=cfg.matching.link_questions)
                     for v in theses if (c['id'], v) in directions}
        if questions:
            jobs.append((state, questions))
            owners.append(c)
    links = []
    if not jobs:
        return links
    for c, reply in zip(owners, _ask(archive, cfg, jobs, transport, record, stage)):
        for qid, answer in sorted(reply.items()):
            view_id = qid[len('sign__'):]
            sign = _passes(answer, (TOGETHER, OPPOSITE))
            record['pairs'].append({'candidate': c['id'], 'thesis': view_id, 'sign': answer['choice'], 'probabilities': answer['probabilities']})
            if sign:
                direction = directions[(c['id'], view_id)]
                reader, read = (c['id'], view_id) if direction == CANDIDATE_READS else (view_id, c['id'])
                links.append({'reader': reader, 'read': read, 'candidate': c['id'], 'thesis': view_id, 'direction': direction, 'sign': sign})
    return links


def _corrected(archive, cfg, conn, asked, directions, links, on_circle, transport, record):
    """PRD 06: refuse a circle and ask the model to correct it, once: the pair's READS question again, the offending direction removed
    and the circle named; the answer replaces the original."""
    offending = {(link['candidate'], link['thesis']): path for link, path in on_circle}
    jobs, owners = [], []
    for c, state, theses in asked:
        questions = {}
        for view_id in theses:
            path = offending.get((c['id'], view_id))
            if path is None:
                continue
            excluded = directions[(c['id'], view_id)]
            named = [('the CANDIDATE' if node == c['id'] else 'the THESIS' if node == view_id else node) for node in path]
            note = f'Reading this way would make {named[0]} read itself through {" -> ".join(named)}; a question cannot read its own conclusion.'
            questions[f'reads__{view_id}'] = reads_question(jev_matching.thesis_text(conn, view_id), excluded=excluded, note=note,
                                                            version=cfg.matching.link_questions)
            record['corrections'].append({'candidate': c['id'], 'thesis': view_id, 'rejected': excluded, 'path': path})
        if questions:
            jobs.append((state, questions))
            owners.append(c)
    kept = [link for link in links if (link['candidate'], link['thesis']) not in offending]
    corrected = {}
    for c, reply in zip(owners, _ask(archive, cfg, jobs, transport, record, 'correction')):
        for qid, answer in reply.items():
            view_id = qid[len('reads__'):]
            directions.pop((c['id'], view_id), None)
            direction = _passes(answer, (CANDIDATE_READS, THESIS_READS))
            record['corrections'].append({'candidate': c['id'], 'thesis': view_id, 'answer': answer['choice'], 'probabilities': answer['probabilities']})
            if direction:
                corrected[(c['id'], view_id)] = direction
    if corrected:
        directions.update(corrected)
        regrouped = [(c, state, [v for v in theses if (c['id'], v) in corrected]) for c, state, theses in asked]
        kept += _signed(archive, cfg, conn, [g for g in regrouped if g[2]], corrected, transport, record, stage='correction sign')
    return kept


# ---------- the record ----------

def attempt_id(conn, item):
    count = conn.execute('select count(distinct attempt_id) from link_selections where input_id=?', (item['input_id'],)).fetchone()[0]
    return f'{item["input_id"]}#{count + 1}'


def record(conn, attempt, seq, item, cfg, status, content):
    store.insert(conn, 'link_selections', attempt_id=attempt, seq=seq, input_id=item['input_id'], config_checksum=cfg.checksum,
                 status=status, record_json=json.dumps(content, ensure_ascii=False, sort_keys=True))
