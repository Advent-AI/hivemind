"""The matching step answered by Jev instead of a generative call (log row 34). For each candidate: its relation to every
thesis on its list (one `choice` per thesis) and its membership of every visible research group (one `noul` per group);
for each incoming piece of evidence: its relation to every stored piece on its list under each linked thesis (one
`choice` per stored piece). Code turns the probabilities into an answer in the matching schema, so `matching.check` and
`writing.write` run unchanged: `merge` when a listed open thesis is the same quantity or event, `succession` when a
listed thesis carries the same key for an earlier period and has no successor, else `new`; `repeat` when a stored
piece is the same statement, `replace` when the incoming piece supersedes it, else `new`. Dependencies are not asked.
Thresholds are pre-set (0.5); a membership above the threshold is added to the candidate's group references."""
import dataclasses
import hashlib
import concurrent.futures
import copy

from .. import config, jev, model, universe as _universe
from . import identity, matching, store

THRESHOLD = 0.5
# D190: the collision judge. Jev reads wording and calls a population variant of one aggregate 'part of' (six 2026 aggregates on the r3
# ledger, each judged 'new'); the generative model, asked the analyst's question, merged five of six. It is asked only for the theses of
# the candidate's own object and measure, and its verdict on those replaces Jev's.
COLLISION_RELATIONS = ['same_question', 'same_question_other_period', 'distinct_question_same_matter', 'different']
COLLISION_SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['relations'],
                    'properties': {'relations': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['thesis_id', 'relation', 'why'],
                                   'properties': {'thesis_id': {'type': 'string'}, 'relation': {'type': 'string', 'enum': COLLISION_RELATIONS}, 'why': {'type': 'string'}}}}}}
RELATIONS = {"same_quantity_or_event": "both ask about the same defined quantity or the same event: alternative wordings, or two estimates or figures of that one quantity",
             "same_quantity_other_period": "the same defined quantity or event series for another period, such as the next fiscal or calendar year",
             "part_of": "one asks about a strict component or subset of the other, in either direction; not identical",
             "same_matter_different_quantity": "one ongoing matter, two distinct quantities or events, neither a component of the other",
             "different": "different matters; sharing a company or industry is not enough",
             "cannot_tell": "the supplied material is insufficient or inconsistent"}
MEMBER_CRITERIA = {"true": "the CANDIDATE tracks this matter, one of its stated components, its implementation, or a deployment the supplied material connects to it",
                   "false": "the supplied material shows a different matter, or a question outside the GROUP's stated scope"}
# 06-views.md, the evidence table: repeat = "the same evidence already exists under the thesis: a retelling, the same number in text and
# table, or the same speaker repeating the same statement"; replace = "a later account of the same matter: a speaker revises guidance,
# forecast or event progress; an official confirms/denies a rumour; or the original source revises its statement". The criteria carry
# those words; the first seed run (log row 35) read "same occasion" into them and missed six cross-document repeats.
PIECES = {"same_statement": "the same evidence: a retelling, the same number stated in text and in a table or in another document, or the same speaker repeating the same statement; wording, precision and document may differ",
          "supersedes": "a later version of the same statement or number, changed: the same speaker revises that guidance, forecast or event-progress statement, an official confirms or denies that reported claim, or the original source revises that statement; another statement on the same topic is not this",
          "different": "a different fact, figure or matter, or a figure for another period or quantity, even if on the same topic"}


@dataclasses.dataclass
class Decision:
    data: dict
    call_id: int
    request_sha256: str
    cached: bool
    prompt_chars: int
    input_tokens: int
    output_tokens: int
    cost_usd: float
    calls: int = 0
    request_records: list = dataclasses.field(default_factory=list)


def candidate_state(c, evidence):
    rungs = ' / '.join(f'{r["label"]}: {r["condition"]}' for r in c['rungs'])
    fields = ', '.join(f'{f}={c[f]}' for f in ('measure', 'scope', 'period_start', 'period_end', 'basis', 'unit', 'event_type') if c.get(f) not in (None, '', 'n/a'))
    own = ' | '.join(f'[{e["speaker"]} {e["original_day"]}] {e["quote"][:400]}' for e in evidence if e['id'] in c.get('evidence_ids', []))[:1600]
    return (f'CANDIDATE ({c["kind"]}, object {c["object"]}, focus "{c["looks_at"]}", {c["year"]}, due {c["due_day"]}): {c["question"]}\n'
            f'Key: {fields}\nLadder: {rungs}\nIts evidence: {own}')


def thesis_text(conn, view_id):
    """The thesis as the judge should see it: the card and the quotes that define it (its first two pieces in force)."""
    pieces = store.evidence_in_force(conn, view_id)[:2]
    quotes = ''.join(f'\n    Evidence: [{p["speaker"]} {p["original_day"]}] {p["quote"][:400]}' for p in pieces)
    return matching.describe_view(conn, view_id, english=True) + quotes


def group_text(group):
    members = '; '.join(m['looks_at'] for m in group.get('members', []))
    return f'{group["name"]}. Scope: {group["scope"]} Also called: {", ".join(group.get("aliases") or [])}. Member questions: {members or "(none yet)"}'


def piece_state(e, said_day):
    return f'INCOMING PIECE [{e["tier"]}; {e["speaker"]}; original source {e["original_who"]}, stated {said_day}] {e["one_line"]} | quote: {e["quote"][:600]}'


def relation_question(text):
    return {'type': 'choice', 'criteria': RELATIONS,
            'instructions': 'What relationship holds between the CANDIDATE and the THESIS below? Use only the supplied text. Equal numbers and similar wording do not establish identity. THESIS:\n' + text}


def member_question(text):
    return {'type': 'noul', 'criteria': MEMBER_CRITERIA,
            'instructions': 'Does the CANDIDATE belong to the ongoing matter defined by GROUP below? Use only the supplied text; a shared company, industry or word is not enough. GROUP:\n' + text}


def piece_question(text):
    return {'type': 'choice', 'criteria': PIECES,
            'instructions': 'How does the INCOMING PIECE relate to the STORED PIECE below, already under the same thesis? Use only the supplied text. STORED PIECE:\n' + text}


def can_succeed(conn, view_id, key, c):
    """06-views succession: the candidate asks the same object's quantity (no typed field conflicts: measure, event type, a stated
    basis or unit, a code-owned scope) for a later period that does not overlap, and the thesis has no successor yet."""
    return bool(key) and (store.view(conn, view_id) or {}).get('object_id') == c['object'] \
        and not identity.conflicts(key, c, merging=False) \
        and bool(key.get('period_end') and c.get('period_start') and key['period_end'] < c['period_start']) \
        and not conn.execute('select 1 from successions where succeeds=?', (view_id,)).fetchone()


def succession_target(conn, c, listed):
    """The succession code decides alone: the same scope as well (a model-worded scope that differs goes to the judge)."""
    if not c.get('measure') or not c.get('period_start'):
        return None
    for view_id in listed:
        key = store.view_key(conn, view_id)
        if key and _universe.scope_key(key.get('scope', '')) == _universe.scope_key(c.get('scope', '')) and can_succeed(conn, view_id, key, c):
            return view_id
    return None


def _summary(answer):
    if answer['type'] == 'noul':
        return f'{answer["noul"]:.2f}'
    top = max(answer['probabilities'].items(), key=lambda kv: kv[1])
    return f'{top[0]} {top[1]:.2f}'


def _answers(archive, cfg, jobs, workers, transport):
    """Ask independent questions; equal concurrent requests share one archived result."""
    if not isinstance(workers, int) or isinstance(workers, bool) or workers < 1:
        raise ValueError('Jev workers must be a positive integer')

    def ask(job):
        state, questions = job
        return jev.ask(archive, cfg, cfg.matching, state, questions, 'match', transport=transport)

    if workers == 1:
        return [ask(job) if job[1] else None for job in jobs]
    keys, unique, replies = [], {}, {}
    for state, questions in jobs:
        if not questions:
            keys.append(None)
            continue
        _, key = model.request_identity(jev.request_for(cfg.matching, state, questions))
        keys.append(key)
        if key not in unique:
            unique[key] = (state, copy.deepcopy(questions))
    waiting, active = iter(unique.items()), {}
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=workers)
    try:
        def fill():
            while len(active) < workers:
                next_job = next(waiting, None)
                if next_job is None:
                    break
                key, job = next_job
                active[pool.submit(ask, job)] = key
        fill()
        while active:
            concurrent.futures.wait(active, return_when=concurrent.futures.FIRST_COMPLETED)
            completed = [future for future in active if future.done()]
            # Check the whole completed set before submitting any replacement work.
            for future in completed:
                future.result()
            for future in completed:
                replies[active.pop(future)] = future.result()
            fill()
    finally:
        for future in active:
            future.cancel()
        pool.shutdown(wait=True, cancel_futures=True)
    results, used = [], set()
    for key in keys:
        if key is None:
            results.append(None)
            continue
        answer = replies[key]
        # A later logical use is exactly what a serial archive lookup would return.
        results.append(dataclasses.replace(answer, cached=True, cost_usd=0.0) if key in used else answer)
        used.add(key)
    return results


def collision_peers(conn, c, listed):
    """The listed theses of the candidate's own object and measure: where one question may be held twice under other words."""
    peers = []
    for v in listed:
        key = store.view_key(conn, v) if c.get('measure') else None
        if key and key.get('measure') == c.get('measure') and (store.view(conn, v) or {}).get('object_id') == c['object']:
            peers.append(v)
    return peers


def ask_collision_judge(archive, cfg, conn, state, peers, llm_transport):
    """One generative call: the candidate's state and the peers' thesis texts; returns {thesis_id: relation}."""
    with open(config.prompt_path(cfg.collision.prompt_version + '.txt'), encoding='utf-8') as handle:
        system = handle.read()
    user = state + '\n\nTHESES:\n' + '\n'.join(f'--- {v}\n{thesis_text(conn, v)}' for v in peers) + '\n\nFor each thesis id, state the relation.'
    answer = model.call(archive, cfg, cfg.collision, system, user, COLLISION_SCHEMA, 'collision', 'match', transport=llm_transport)
    return answer, {r['thesis_id']: r['relation'] for r in answer.data['relations'] if r['thesis_id'] in peers}


def decide(archive, cfg, conn, item, candidates, evidence, lists, shown_views, *, extra_views=(), retry_note='', transport=None, llm_transport=None, workers=1):
    data = {'candidates': [], 'evidence': []}
    total = Decision(data, 0, '', True, 0, 0, 0, 0.0)
    shas = []
    jobs, candidate_jobs, evidence_jobs = [], [], []
    # All database reads and request construction stay on the coordinator thread.
    for c in candidates:
        listed = list(dict.fromkeys(list(lists.candidate_lists.get(c['id'], [])) + [v['view_id'] for v in shown_views]))
        questions = {f'rel__{v}': relation_question(thesis_text(conn, v)) for v in listed}
        groups = store.groups_for_prompt(conn, [c['object']], f'{c["looks_at"]} {c["question"]}')
        for g in groups:
            questions[f'member__{g["group_id"]}'] = member_question(group_text(g))
        candidate_jobs.append((c, listed, groups, len(jobs)))
        jobs.append((candidate_state(c, evidence), questions))
    for e in evidence:
        pairs = [(e['id'], v) for v in e['links'] if (e['id'], v) in lists.evidence_lists]
        if not pairs:
            continue
        questions = {f'piece__{v}__{x}': piece_question(matching.describe_evidence(conn, x, english=True)) for _, v in pairs for x in lists.evidence_lists[(e['id'], v)]}
        said_day = e.get('original_day') or item['publication_day']
        evidence_jobs.append((e, pairs, said_day, len(jobs)))
        jobs.append((piece_state(e, said_day), questions))
    replies = _answers(archive, cfg, jobs, workers, transport)

    def answers_for(index):
        answer = replies[index]
        if answer is None:
            return {}
        total.cost_usd += answer.cost_usd
        total.input_tokens += answer.input_tokens
        total.output_tokens += answer.output_tokens
        total.prompt_chars += answer.prompt_chars
        total.cached = total.cached and answer.cached
        total.call_id = answer.call_id
        total.calls += 1
        shas.append(answer.request_sha256)
        total.request_records.append({'call_id': answer.call_id, 'request_sha256': answer.request_sha256})
        return answer.data

    for c, listed, groups, job_index in candidate_jobs:
        answers = answers_for(job_index)
        same = sorted(((answers[f'rel__{v}']['probabilities']['same_quantity_or_event'], v) for v in listed
                       if answers[f'rel__{v}']['choice'] == 'same_quantity_or_event' and answers[f'rel__{v}']['probabilities']['same_quantity_or_event'] >= THRESHOLD),
                      reverse=True)
        joined = [g['group_id'] for g in groups if answers[f'member__{g["group_id"]}']['noul'] >= THRESHOLD]
        for group_id in joined:
            if group_id not in (c.get('group_refs') or []) and group_id not in (c.get('jev_group_refs') or []):
                c.setdefault('jev_group_refs', []).append(group_id)          # the writer records these with basis 'jev'
        reasons = '; '.join(f'{qid[5:]}: {_summary(a)}' for qid, a in answers.items() if qid.startswith('rel__'))
        outcome, target = 'new', ''
        for _, v in same:
            # the key decides what 'the same' may mean: a different quantity is declined here; the same quantity for a later period is a
            # succession (06-views), when the thesis has no successor yet; otherwise a merge into an open thesis
            key = store.view_key(conn, v) if c.get('measure') else None
            if key and identity.conflicts(key, c, merging=False):
                continue
            if key and identity.conflicts(key, c, merging=True):          # the same quantity for another period
                if can_succeed(conn, v, key, c):
                    outcome, target = 'succession', v
                    break
                continue
            if store.is_open(conn, v):
                outcome, target = 'merge', v
                break
        if outcome == 'new':
            # the judge says 'the same quantity for another period'; code decides the direction, the typed fields and the successor
            other = sorted(((answers[f'rel__{v}']['probabilities']['same_quantity_other_period'], v) for v in listed
                            if answers[f'rel__{v}']['choice'] == 'same_quantity_other_period' and answers[f'rel__{v}']['probabilities']['same_quantity_other_period'] >= THRESHOLD),
                           reverse=True)
            for _, v in other:
                key = store.view_key(conn, v) if c.get('measure') else None
                if can_succeed(conn, v, key, c):
                    outcome, target = 'succession', v
                    break
        if outcome == 'new':
            successor_of = succession_target(conn, c, listed)
            if successor_of:
                outcome, target = 'succession', successor_of
        peers = collision_peers(conn, c, listed) if getattr(cfg, 'collision', None) else []
        judged = ''
        if peers:
            answer, verdicts = ask_collision_judge(archive, cfg, conn, candidate_state(c, evidence), peers, llm_transport)
            total.cost_usd += answer.cost_usd
            total.input_tokens += answer.input_tokens
            total.output_tokens += answer.output_tokens
            total.calls += 1
            total.cached = total.cached and answer.cached
            shas.append(answer.request_sha256)
            total.request_records.append({'call_id': answer.call_id, 'request_sha256': answer.request_sha256})
            judged = '; collision judge: ' + ', '.join(f'{v}: {verdicts.get(v, "(no answer)")}' for v in peers)
            if target in peers and verdicts.get(target) not in ('same_question', 'same_question_other_period'):
                outcome, target = 'new', ''                      # Jev's merge or succession on a peer the judge keeps apart
            if outcome == 'new':
                for v in peers:
                    key = store.view_key(conn, v)
                    if verdicts.get(v) == 'same_question' and not identity.conflicts(key, c, merging=False):
                        if identity.conflicts(key, c, merging=True):
                            if can_succeed(conn, v, key, c):
                                outcome, target = 'succession', v
                                break
                            continue
                        if store.is_open(conn, v):
                            outcome, target = 'merge', v
                            break
                    if verdicts.get(v) == 'same_question_other_period' and can_succeed(conn, v, key, c):
                        outcome, target = 'succession', v
                        break
        data['candidates'].append({'id': c['id'], 'outcome': outcome, 'target_view_id': target or '', 'dependencies': [],
                                   'reason': f'jev: {reasons or "no list"}; groups joined: {joined or "none"}{judged}'})
    for e, pairs, said_day, job_index in evidence_jobs:
        answers = answers_for(job_index)
        for _, v in pairs:
            scored = [(answers[f'piece__{v}__{x}'], x) for x in lists.evidence_lists[(e['id'], v)]]
            repeats = sorted(((a['probabilities']['same_statement'], x) for a, x in scored if a['choice'] == 'same_statement' and a['probabilities']['same_statement'] >= THRESHOLD), reverse=True)
            replaces = sorted(((a['probabilities']['supersedes'], x) for a, x in scored if a['choice'] == 'supersedes' and a['probabilities']['supersedes'] >= THRESHOLD), reverse=True)
            outcome, target = ('repeat', repeats[0][1]) if repeats else ('replace', replaces[0][1]) if replaces else ('new', '')
            data['evidence'].append({'id': e['id'], 'view_id': v, 'outcome': outcome, 'target_evidence_id': target or '', 'said_day': said_day,
                                     'reason': 'jev: ' + '; '.join(f'{x}: {_summary(a)}' for a, x in scored)})
    total.request_sha256 = hashlib.sha256('+'.join(shas).encode('utf-8')).hexdigest() if shas else ''
    return total
