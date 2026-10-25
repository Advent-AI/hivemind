"""06-views.md steps 3–5: build the search lists, ask the model where each candidate view and each piece of evidence
goes (two calls: direct evidence with the candidates; evidence linked to candidates once their destination is
known), and check the answers by code (ids in the lists, attach only to open views, the object on the list,
succession unique and oriented, dependencies among shown views or a waited year, no cycles).

matching-v1 asks and answers in Chinese; matching-v2 and later ask and answer in English (D163). The schema, the
request text and the retry note follow the prompt version; every answer is checked in the canonical vocabulary."""
import dataclasses
import json
import os
import re

from .. import config, model, vocabulary
from . import identity, store

PROMPTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')
OUTCOMES = vocabulary.CANDIDATE_OUTCOMES
EVIDENCE_OUTCOMES = vocabulary.EVIDENCE_OUTCOMES
LEGACY_OUTCOMES = list(vocabulary.LEGACY['candidate_outcome'])
LEGACY_EVIDENCE_OUTCOMES = list(vocabulary.LEGACY['evidence_outcome'])
ENGLISH_FROM = 2                  # the first matching prompt version written in English


def version_number(prompt_version):
    return int(str(prompt_version or '').rpartition('-v')[2] or 0)


def is_english(prompt_version):
    return version_number(prompt_version) >= ENGLISH_FROM


def schema_for(prompt_version):
    english = is_english(prompt_version)
    outcomes = OUTCOMES if english else LEGACY_OUTCOMES
    evidence_outcomes = EVIDENCE_OUTCOMES if english else LEGACY_EVIDENCE_OUTCOMES
    direction = {'type': 'string', 'enum': vocabulary.DIRECTIONS} if english else {'type': 'string'}
    return {
        'type': 'object', 'additionalProperties': False, 'required': ['candidates', 'evidence'],
        'properties': {
            'candidates': {'type': 'array', 'items': {
                'type': 'object', 'additionalProperties': False, 'required': ['id', 'outcome', 'target_view_id', 'reason', 'dependencies'],
                'properties': {
                    'id': {'type': 'string'}, 'outcome': {'type': 'string', 'enum': outcomes}, 'target_view_id': {'type': 'string'},
                    'reason': {'type': 'string'},
                    'dependencies': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False,
                                                                'required': ['view_id', 'wait_chain_view_id', 'wait_year', 'direction'],
                                                                'properties': {'view_id': {'type': 'string'}, 'wait_chain_view_id': {'type': 'string'},
                                                                               'wait_year': {'type': 'string'}, 'direction': direction}}}}}},
            'evidence': {'type': 'array', 'items': {
                'type': 'object', 'additionalProperties': False, 'required': ['id', 'view_id', 'outcome', 'target_evidence_id', 'said_day', 'reason'],
                'properties': {'id': {'type': 'string'}, 'view_id': {'type': 'string'}, 'outcome': {'type': 'string', 'enum': evidence_outcomes},
                               'target_evidence_id': {'type': 'string'}, 'said_day': {'type': 'string'}, 'reason': {'type': 'string'}}}},
        },
    }


SCHEMA = schema_for('matching-v1')          # the shape of the answers stored under matching-v1


NUMBER_WITH_UNIT = re.compile(r'(-?\d+(?:[.,]\d+)?)\s*(万亿|亿|百万|%|trillion|billion|million|tn|bn|mn)?', re.I)
YEAR_LIKE = re.compile(r'(?:FY|财年)\s*\d{4}|\d{4}\s*(?:年|财年)|\d{4}-\d{2}-\d{2}')
SCALE = {'万亿': 1e4, 'trillion': 1e3, 'tn': 1e3, 'million': 1e-3, 'mn': 1e-3}      # 亿 and billion are the unscaled magnitudes of their language


def first_value(condition):
    """The first quantity in a rung condition, years removed, magnitudes brought to one scale within a language."""
    for found in NUMBER_WITH_UNIT.finditer(YEAR_LIKE.sub(' ', condition or '')):
        value = float(found.group(1).replace(',', ''))
        unit = (found.group(2) or '').lower()
        return value * SCALE.get(unit, 1)
    return None


def ladder_direction(rungs):
    """+1 when the quantities rise from the first rung to the last, -1 when they fall, None when undecidable. The rungs'
    numeric bounds decide when both ends carry them; the prose is read only for a ladder without bounds."""
    first, last = rungs[0], rungs[-1]
    if any(r.get('lo') is not None or r.get('hi') is not None for r in rungs):
        if first.get('hi') is not None and last.get('lo') is not None and float(first['hi']) <= float(last['lo']):
            return 1
        if first.get('lo') is not None and last.get('hi') is not None and float(last['hi']) <= float(first['lo']):
            return -1
        return None
    numbers = [first_value(rung['condition']) for rung in rungs]
    known = [n for n in numbers if n is not None]
    if len(known) < 2 or known[0] == known[-1]:
        return None
    return 1 if known[0] < known[-1] else -1


def same_orientation(previous, candidate):
    """06-views: a successor's ladder keeps the predecessor's direction. Asset views carry the fixed labels, so equal
    labels settle it; a theme view's labels are results that change with the period, so the direction of the numbers
    is compared instead, and an undecidable pair is left to the model."""
    if [vocabulary.canonical('label', r['label']) for r in previous] == [vocabulary.canonical('label', r['label']) for r in candidate]:
        return True
    before, after = ladder_direction(previous), ladder_direction(candidate)
    return before is None or after is None or before == after


@dataclasses.dataclass
class Lists:
    candidate_lists: dict      # candidate id -> [view_id]
    evidence_lists: dict       # (evidence handover id, view_id) -> [evidence_id]


CJK_RUN = re.compile(r'[一-鿿]+')


def _words(text):
    """Tokens for the within-view ranking: latin words and numbers, and character bigrams for Chinese runs (a
    Chinese one-line has no spaces, so whole clauses would otherwise be single tokens that never overlap)."""
    text = (text or '').lower()
    words = set(re.findall(r'[a-z0-9]+(?:[.,][0-9]+)?%?', text))
    for run in CJK_RUN.findall(text):
        words.update(run[i:i + 2] for i in range(len(run) - 1))
    return words


def rank_evidence(conn, view_id, one_line, top_n):
    """The view's evidence in force ranked by word overlap with the new piece's one-line (the within-view search)."""
    pieces = store.evidence_in_force(conn, view_id)
    target = _words(one_line)
    scored = sorted(pieces, key=lambda p: -len(target & _words(p['one_line'] + ' ' + p['quote'])))
    return [p['evidence_id'] for p in scored[:top_n]]


def _same_key(key, c, view_object=None):
    """Only a complete, corrected, code-owned key authorizes automatic identity."""
    target = identity.automatic_key(c)
    return target is not None and bool(key) and identity.automatic_key(key, view_object) == target


def key_matches(conn, c):
    """keyed-views-plan.md 2.5: the open views a keyed candidate must be confirmed against (same object, measure and scope,
    overlapping period); empty for a candidate without a key."""
    if not c.get('measure'):
        return []
    from .. import universe as _universe
    # a model-written scope is wording, not identity: such a candidate is compared with every open view of its measure and period
    scope_key = _universe.scope_key(c.get('scope', '')) if c.get('scope_source') in ('none', 'watch') else None
    return store.open_views_with_key(conn, c['object'], c['measure'], scope_key, c.get('period_start', ''), c.get('period_end', ''), c.get('basis', 'n/a'), c.get('unit', 'n/a'), c.get('event_type', 'n/a'))


def build_lists(conn, handover, shown_views, top_n):
    candidate_lists = {}
    for c in handover.candidates:
        same_key = key_matches(conn, c)
        if same_key:                      # a keyed candidate is compared with the views that share its key, a narrow question
            exact = store.exact_key_views(conn, c)
            candidate_lists[c['id']] = list(dict.fromkeys(exact + same_key))[:top_n]
            continue
        hits = store.search_views(conn, f'{c["object"]} {c["looks_at"]} {c["question"]}', top_n)
        for v in shown_views:
            if v['view_id'] not in hits and v['object_id'] == c['object']:
                hits.append(v['view_id'])
        candidate_lists[c['id']] = hits[:top_n]
    evidence_lists = {}
    candidate_ids = {c['id'] for c in handover.candidates}
    for e in handover.evidence:
        for view_id in e['links']:
            if view_id in candidate_ids:
                continue
            evidence_lists[(e['id'], view_id)] = rank_evidence(conn, view_id, e['one_line'], top_n)
    return Lists(candidate_lists, evidence_lists)


def describe_view(conn, view_id, english=False):
    v = store.view(conn, view_id)
    successor = conn.execute('select view_id from successions where succeeds=?', (view_id,)).fetchone()
    if english:
        rungs = ' / '.join(f'{r["label"]}: {r["condition"]}' for r in store.rungs_of(conn, view_id))
        state = 'open' if store.is_open(conn, view_id) else 'closed'
        tail = f'; successor already exists: {successor["view_id"]}' if successor else ''
        groups = store.groups_of_view(conn, view_id)
        tail += f'; research group: ' + ', '.join(f'{g["group_id"]} "{g["name"]}"' for g in groups) if groups else ''
        return f'{view_id} ({state}, {v["object_id"]}, {v["kind"]}, focus "{v["looks_at"]}", {v["year"] or ""}, due {v["due_day"]}): {v["question"]}\n    Ladder: {rungs}{tail}'
    rungs = ' / '.join(f'{r["label"]}：{r["condition"]}' for r in store.rungs_of(conn, view_id))
    state = '开着' if store.is_open(conn, view_id) else '关了'
    tail = f'；已有下一期 {successor["view_id"]}' if successor else ''
    return f'{view_id}（{state}，{v["object_id"]}，{v["kind"]}，看的是「{v["looks_at"]}」，{v["year"] or ""}，到期 {v["due_day"]}）：{v["question"]}\n    梯子：{rungs}{tail}'


def describe_evidence(conn, evidence_id, english=False):
    e = store.evidence(conn, evidence_id)
    if english:
        return f'{evidence_id} [{e["tier"]}; {e["speaker"]}; original source {e["original_who"]} {e["original_day"]}] {e["one_line"]} | quote: {e["quote"][:300]}'
    return f'{evidence_id}［{e["tier"]}；{e["speaker"]}；原始来源 {e["original_who"]} {e["original_day"]}］{e["one_line"]}｜原句：{e["quote"][:300]}'


def _user_text_chinese(conn, item, candidates, evidence, lists, shown_views, extra_views=()):
    parts = [f'信息：{item["input_id"]}，发布日 {item["publication_day"]}，类别 {item["category"]}。']
    if candidates:
        parts.append('【候选观点】')
        for c in candidates:
            rungs = ' / '.join(f'{r["label"]}：{r["condition"]}' for r in c['rungs'])
            listed = lists.candidate_lists.get(c['id'], [])
            parts.append(f'- {c["id"]}（{c["kind"]}，对象 {c["object"]}，看的是「{c["looks_at"]}」，{c["year"]}，到期 {c["due_day"]}）：{c["question"]}\n    梯子：{rungs}\n    它的证据：' +
                         '；'.join(e['one_line'] for e in evidence if e['id'] in c['evidence_ids'])[:1500])
            if listed:
                parts.append('    搜出来的已有观点：\n' + '\n'.join('    · ' + describe_view(conn, v) for v in listed))
            else:
                parts.append('    搜出来的已有观点：没有。')
    if shown_views:
        parts.append('【抽取时给模型看过的已有观点】\n' + '\n'.join('· ' + describe_view(conn, v['view_id']) for v in shown_views))
    for v in extra_views:
        parts.append('· ' + describe_view(conn, v))
    direct = [(e, vid) for e in evidence for vid in e['links'] if (e['id'], vid) in lists.evidence_lists]
    if direct:
        parts.append('【连在已有观点上的证据，和那条观点下已有的证据比】')
        for e, vid in direct:
            parts.append(f'- {e["id"]} → {vid}［{e["tier"]}；{e["speaker"]}；{e["original_who"]} {e["original_day"]}］{e["one_line"]}｜原句：{e["quote"][:300]}')
            listed = lists.evidence_lists[(e['id'], vid)]
            parts.append('    那条观点下已有的：\n' + ('\n'.join('    · ' + describe_evidence(conn, x) for x in listed) if listed else '    · 还没有证据'))
    parts.append('按 JSON schema 交出每个候选观点的去向和依赖、每条证据的去向。没有的数组交空。target 没有就写空字符串。')
    return '\n'.join(parts)


def _user_text_english(conn, item, candidates, evidence, lists, shown_views, extra_views=()):
    parts = [f'Item: {item["input_id"]}, published {item["publication_day"]}, category {item["category"]}.']
    if candidates:
        parts.append('[Candidate theses]')
        for c in candidates:
            rungs = ' / '.join(f'{r["label"]}: {r["condition"]}' for r in c['rungs'])
            listed = lists.candidate_lists.get(c['id'], [])
            parts.append(f'- {c["id"]} ({c["kind"]}, object {c["object"]}, focus "{c["looks_at"]}", {c["year"]}, due {c["due_day"]}): {c["question"]}\n    Ladder: {rungs}\n    Its evidence: ' +
                         '; '.join(e['one_line'] for e in evidence if e['id'] in c['evidence_ids'])[:1500])
            if listed:
                parts.append('    Existing theses found by search:\n' + '\n'.join('    · ' + describe_view(conn, v, english=True) for v in listed))
            else:
                parts.append('    Existing theses found by search: none.')
    if shown_views:
        parts.append('[Existing theses shown to the model at extraction]\n' + '\n'.join('· ' + describe_view(conn, v['view_id'], english=True) for v in shown_views))
    for v in extra_views:
        parts.append('· ' + describe_view(conn, v, english=True))
    direct = [(e, vid) for e in evidence for vid in e['links'] if (e['id'], vid) in lists.evidence_lists]
    if direct:
        parts.append('[Evidence linked to existing theses, to compare with the evidence already under that thesis]')
        for e, vid in direct:
            parts.append(f'- {e["id"]} → {vid} [{e["tier"]}; {e["speaker"]}; {e["original_who"]} {e["original_day"]}] {e["one_line"]} | quote: {e["quote"][:300]}')
            listed = lists.evidence_lists[(e['id'], vid)]
            parts.append('    Already under that thesis:\n' + ('\n'.join('    · ' + describe_evidence(conn, x, english=True) for x in listed) if listed else '    · no evidence yet'))
    parts.append('Return, per the JSON schema, each candidate\'s destination and dependencies, and one decision for every evidence → thesis pair listed above (id and view_id exactly as listed). Empty arrays when there is nothing. An absent target is an empty string.')
    return '\n'.join(parts)


def _user_text(conn, item, candidates, evidence, lists, shown_views, extra_views=(), english=False):
    build = _user_text_english if english else _user_text_chinese
    return build(conn, item, candidates, evidence, lists, shown_views, extra_views)


def decide(archive, cfg, conn, item, candidates, evidence, lists, shown_views, *, extra_views=(), retry_note='', transport=None):
    english = is_english(cfg.matching.prompt_version)
    with open(config.prompt_path(cfg.matching.prompt_version + '.txt'), encoding='utf-8') as handle:
        system = handle.read()
    user = _user_text(conn, item, candidates, evidence, lists, shown_views, extra_views, english=english)
    if retry_note:
        if english:
            user += '\n\nThe code returned the previous answer because: ' + retry_note + '\nCorrect it and answer again.'
        else:
            user += '\n\n上一次的答案被代码退回，原因：' + retry_note + '\n请改正后再交。'
    answer = model.call(archive, cfg, cfg.matching, system, user, schema_for(cfg.matching.prompt_version), 'matching', 'match', transport=transport)
    return answer


@dataclasses.dataclass
class Checked:
    outcomes: dict         # candidate id -> (outcome, target or None, dependencies list)
    evidence: dict         # (evidence id, view_id) -> (outcome, target_evidence_id or None, said_day)
    refusals: list
    not_opened: dict       # candidate id -> reason
    notes: list = dataclasses.field(default_factory=list)


def check(conn, universe, decisions, candidates, evidence, lists, shown_views):
    decisions = vocabulary.matching_answer(decisions)
    candidates = [vocabulary.candidate(c) for c in candidates]
    shown_ids = {v['view_id'] for v in shown_views}
    candidate_by_id = {c['id']: c for c in candidates}
    # D51: a dependency is chosen among the views the model has in front of it: every list shown in this call,
    # the views shown at extraction, and the candidates this answer opens
    listed_all = set(shown_ids)
    for hits in lists.candidate_lists.values():
        listed_all.update(hits)
    refusals, outcomes, not_opened, notes = [], {}, {}, []
    raw_deps = {}
    succession_targets = {}
    answered = {d['id']: d for d in decisions.get('candidates', [])}
    for c in candidates:
        d = answered.get(c['id'])
        if not d:
            refusals.append(f'candidate {c["id"]} has no decision')
            continue
        outcome, target = d['outcome'], d['target_view_id'].strip()
        listed = set(lists.candidate_lists.get(c['id'], [])) | shown_ids
        if outcome in ('merge', 'succession') and target in candidate_by_id:
            # a candidate cannot merge into another candidate of the same answer: only a stored thesis has a ladder and a due day to
            # inherit. The model usually means "part of": both open, and the key coalesces them when they are the same quantity.
            notes.append(f'candidate {c["id"]}: {outcome} into candidate {target} is not a destination; opened as a new view')
            outcome, target = 'new', ''
            d = dict(d, outcome=outcome, target_view_id='')
        if outcome in ('merge', 'succession') and c.get('measure'):
            # keyed-views-plan.md 2.5 rule 1: a different quantity, or another period, is never the same view, whatever the model says
            target_key = store.view_key(conn, target) if target else None
            target_view = store.view(conn, target) if target else None
            if target_view and target_view['object_id'] != c['object']:
                notes.append(f'candidate {c["id"]}: {outcome} into {target} refused: another object ({target_view["object_id"]} ≠ {c["object"]}); opened as a new view')
                outcome, target, target_key = 'new', '', None
                d = dict(d, outcome=outcome, target_view_id='')
            if target_key and identity.conflicts(target_key, c, merging=outcome == 'merge'):
                notes.append(f'candidate {c["id"]}: {outcome} into {target} refused by key ({target_key["measure"]}[{target_key["scope"]}] {target_key["period_start"]}..{target_key["period_end"]} ≠ {c["measure"]}[{c.get("scope", "")}] {c.get("period_start", "")}..{c.get("period_end", "")}); opened as a new view')
                outcome, target = 'new', ''
                d = dict(d, outcome=outcome, target_view_id='')
        if outcome == 'new' and identity.automatic_key(c) is not None:
            # rule 2 for a key code owns entirely: one open view with the same key and period is the same quantity; the model is not asked twice
            twins = [v for v in lists.candidate_lists.get(c['id'], []) if _same_key(store.view_key(conn, v), c, (store.view(conn, v) or {}).get('object_id')) and store.is_open(conn, v)]
            if len(twins) == 1:
                notes.append(f'candidate {c["id"]}: opened as new by the model, merged into {twins[0]} by its key ({c["measure"]}[{c.get("scope", "")}] {c.get("period_start", "")}..{c.get("period_end", "")})')
                outcome, target = 'merge', twins[0]
                d = dict(d, outcome=outcome, target_view_id=target)
        if outcome in ('merge', 'succession'):
            if target not in listed:
                refusals.append(f'candidate {c["id"]}: target {target!r} not in its list')
                continue
            if outcome == 'merge' and not store.is_open(conn, target):
                refusals.append(f'candidate {c["id"]}: cannot attach to closed view {target}')
                continue
            if outcome == 'succession':
                if conn.execute('select 1 from successions where succeeds=?', (target,)).fetchone():
                    refusals.append(f'candidate {c["id"]}: {target} already has a successor')
                    continue
                if target in succession_targets:
                    refusals.append(f'candidate {c["id"]}: {target} can have one successor; {succession_targets[target]} already succeeds it in this answer')
                    continue
                succession_targets[target] = c['id']
                # 06-views: a successor keeps the predecessor's direction; the writer stores a numeric ladder in that direction (the first
                # real succession, 2027 hyperscaler capex after 2026, came low-to-high where its predecessor ran high-to-low), so no refusal here
        if outcome in ('new', 'succession'):
            object_id = universe.resolve(c['object'])
            if not object_id:
                not_opened[c['id']] = f'object {c["object"]!r} not on the research list'
                if c['kind'] == 'theme':
                    store.pool(conn, 'suggested_theme', c['object'], {'question': c['question'], 'input_id': None}, 0)
                outcomes[c['id']] = ('skip', None, [])
                continue
            outcomes[c['id']] = (outcome, target or None, [])
            raw_deps[c['id']] = d.get('dependencies', [])
        elif outcome == 'merge':
            outcomes[c['id']] = (outcome, target, [])
        else:
            outcomes[c['id']] = ('skip', None, [])
            not_opened[c['id']] = d.get('reason', '')
    # dependencies, once every candidate's outcome is known
    opened = {cid for cid, (outcome, _, _) in outcomes.items() if outcome in ('new', 'succession')}
    for cid, dependencies in raw_deps.items():
        deps = []
        bad = False
        for dep in dependencies:
            view_id, chain, year = dep['view_id'].strip(), dep['wait_chain_view_id'].strip(), dep['wait_year'].strip()
            if view_id:
                if view_id in candidate_by_id and view_id not in opened:
                    refusals.append(f'candidate {cid}: dependency {view_id} is a candidate that is not opened')
                    bad = True
                    break
                if view_id not in listed_all and view_id not in candidate_by_id:
                    refusals.append(f'candidate {cid}: dependency {view_id} was not shown')
                    bad = True
                    break
                if view_id == cid:
                    refusals.append(f'candidate {cid}: depends on itself')
                    bad = True
                    break
                deps.append({'view_id': view_id, 'wait_chain_view_id': None, 'wait_year': None, 'direction': dep['direction']})
            elif chain and year:
                if chain not in listed_all and chain not in candidate_by_id:
                    refusals.append(f'candidate {cid}: waited chain {chain} was not shown')
                    bad = True
                    break
                deps.append({'view_id': None, 'wait_chain_view_id': chain, 'wait_year': year, 'direction': dep['direction']})
        if bad:
            continue
        outcomes[cid] = (outcomes[cid][0], outcomes[cid][1], deps)
    # no cycle among the candidates of one answer (06-views: 会的话这条不收，退回给模型改)
    graph = {cid: [d['view_id'] for d in outcomes[cid][2] if d['view_id'] in candidate_by_id] for cid in raw_deps if cid in outcomes}
    for cid in graph:
        stack, seen = list(graph[cid]), set()
        while stack:
            current = stack.pop()
            if current == cid:
                refusals.append(f'candidate {cid}: its dependencies lead back to itself')
                break
            if current in seen:
                continue
            seen.add(current)
            stack.extend(graph.get(current, []))
    _, coalescing_errors = identity.batch_plan(candidates, outcomes)
    refusals.extend(coalescing_errors)
    evidence_out = {}
    answered_e = {(d['id'], d['view_id']): d for d in decisions.get('evidence', [])}
    shown_evidence = {e for listed in lists.evidence_lists.values() for e in listed}      # every evidence id this request shows the model
    shown_for_piece = {}                                                                     # handover piece -> ids shown for it under any thesis
    for (piece_id, _), listed in lists.evidence_lists.items():
        shown_for_piece.setdefault(piece_id, set()).update(listed)
    for key, listed in lists.evidence_lists.items():
        d = answered_e.get(key)
        if not d:
            refusals.append(f'evidence {key[0]} under {key[1]} has no decision')
            continue
        outcome, target = d['outcome'], d['target_evidence_id'].strip()
        if outcome in ('repeat', 'replace'):
            # 06-views step 5: the target is a piece under the destination view. Its list shows that view's top N; a piece the
            # request shows in another list is also a valid target when it is linked to this view (the model reads the whole request).
            # A repeat may also name a piece shown for this same evidence under another of its theses: a repeat adds a source and
            # any new thesis link (06-views step 6), and the writer resolves the piece to that one stored identity for all its theses.
            # A replacement stays within the destination thesis.
            same_piece_repeat = outcome == 'repeat' and target in shown_for_piece.get(key[0], set())
            if target not in listed and not same_piece_repeat and not (target in shown_evidence and target in set(store.evidence_ids_under(conn, key[1]))):
                refusals.append(f'evidence {key[0]}: target {target!r} not among {key[1]}\'s evidence shown')
                continue
            evidence_out[key] = (outcome, target, d['said_day'].strip())
        else:
            evidence_out[key] = ('new', None, d['said_day'].strip())
    return Checked(outcomes, evidence_out, refusals, not_opened, notes)
