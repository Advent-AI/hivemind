"""06-views.md steps 3–5: build the search lists, ask the model where each candidate view and each piece of evidence
goes (two calls: direct evidence with the candidates; evidence linked to candidates once their destination is
known), and check the answers by code (ids in the lists, attach only to open views, the object on the list,
succession unique and oriented, dependencies among shown views or a waited year, no cycles)."""
import dataclasses
import json
import os
import re

from .. import config, model
from . import store

PROMPTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')
OUTCOMES = ['归入已有的', '接续', '新观点', '不开']
EVIDENCE_OUTCOMES = ['重复', '替代', '新证据']

SCHEMA = {
    'type': 'object', 'additionalProperties': False, 'required': ['candidates', 'evidence'],
    'properties': {
        'candidates': {'type': 'array', 'items': {
            'type': 'object', 'additionalProperties': False, 'required': ['id', 'outcome', 'target_view_id', 'reason', 'dependencies'],
            'properties': {
                'id': {'type': 'string'}, 'outcome': {'type': 'string', 'enum': OUTCOMES}, 'target_view_id': {'type': 'string'},
                'reason': {'type': 'string'},
                'dependencies': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False,
                                                            'required': ['view_id', 'wait_chain_view_id', 'wait_year', 'direction'],
                                                            'properties': {'view_id': {'type': 'string'}, 'wait_chain_view_id': {'type': 'string'},
                                                                           'wait_year': {'type': 'string'}, 'direction': {'type': 'string'}}}}}}},
        'evidence': {'type': 'array', 'items': {
            'type': 'object', 'additionalProperties': False, 'required': ['id', 'view_id', 'outcome', 'target_evidence_id', 'said_day', 'reason'],
            'properties': {'id': {'type': 'string'}, 'view_id': {'type': 'string'}, 'outcome': {'type': 'string', 'enum': EVIDENCE_OUTCOMES},
                           'target_evidence_id': {'type': 'string'}, 'said_day': {'type': 'string'}, 'reason': {'type': 'string'}}}},
    },
}


NUMBER_WITH_UNIT = re.compile(r'(-?\d+(?:[.,]\d+)?)\s*(万亿|亿|百万|%)?')
YEAR_LIKE = re.compile(r'(?:FY|财年)\s*\d{4}|\d{4}\s*(?:年|财年)|\d{4}-\d{2}-\d{2}')


def first_value(condition):
    """The first quantity in a rung condition, years removed, 万亿 brought to the same scale as 亿."""
    for found in NUMBER_WITH_UNIT.finditer(YEAR_LIKE.sub(' ', condition or '')):
        value = float(found.group(1).replace(',', ''))
        return value * 1e4 if found.group(2) == '万亿' else value
    return None


def ladder_direction(rungs):
    """+1 when the quantities in the rung conditions rise from the first rung to the last, -1 when they fall, None
    when the conditions carry no comparable numbers (states of an event, or labels only)."""
    numbers = [first_value(rung['condition']) for rung in rungs]
    known = [n for n in numbers if n is not None]
    if len(known) < 2 or known[0] == known[-1]:
        return None
    return 1 if known[0] < known[-1] else -1


def same_orientation(previous, candidate):
    """06-views: a successor's ladder keeps the predecessor's direction. Object views carry the fixed labels, so equal
    labels settle it; a theme view's labels are results that change with the period, so the direction of the numbers
    in the conditions is compared instead, and an undecidable pair is left to the model."""
    if [r['label'].strip() for r in previous] == [r['label'].strip() for r in candidate]:
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


def build_lists(conn, handover, shown_views, top_n):
    candidate_lists = {}
    for c in handover.candidates:
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


def describe_view(conn, view_id):
    v = store.view(conn, view_id)
    rungs = ' / '.join(f'{r["label"]}：{r["condition"]}' for r in store.rungs_of(conn, view_id))
    state = '开着' if store.is_open(conn, view_id) else '关了'
    successor = conn.execute('select view_id from successions where succeeds=?', (view_id,)).fetchone()
    tail = f'；已有下一期 {successor["view_id"]}' if successor else ''
    return f'{view_id}（{state}，{v["object_id"]}，{v["kind"]}，看的是「{v["looks_at"]}」，{v["year"] or ""}，到期 {v["due_day"]}）：{v["question"]}\n    梯子：{rungs}{tail}'


def describe_evidence(conn, evidence_id):
    e = store.evidence(conn, evidence_id)
    return f'{evidence_id}［{e["tier"]}；{e["speaker"]}；原始来源 {e["original_who"]} {e["original_day"]}］{e["one_line"]}｜原句：{e["quote"][:300]}'


def _user_text(conn, item, candidates, evidence, lists, shown_views, extra_views=()):
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


def decide(archive, cfg, conn, item, candidates, evidence, lists, shown_views, *, extra_views=(), retry_note='', transport=None):
    with open(config.prompt_path(cfg.matching.prompt_version + '.txt'), encoding='utf-8') as handle:
        system = handle.read()
    user = _user_text(conn, item, candidates, evidence, lists, shown_views, extra_views)
    if retry_note:
        user += '\n\n上一次的答案被代码退回，原因：' + retry_note + '\n请改正后再交。'
    answer = model.call(archive, cfg, cfg.matching, system, user, SCHEMA, 'matching', 'match', transport=transport)
    return answer


@dataclasses.dataclass
class Checked:
    outcomes: dict         # candidate id -> (outcome, target or None, dependencies list)
    evidence: dict         # (evidence id, view_id) -> (outcome, target_evidence_id or None, said_day)
    refusals: list
    not_opened: dict       # candidate id -> reason


def check(conn, universe, decisions, candidates, evidence, lists, shown_views):
    shown_ids = {v['view_id'] for v in shown_views}
    candidate_by_id = {c['id']: c for c in candidates}
    # D51: a dependency is chosen among the views the model has in front of it: every list shown in this call,
    # the views shown at extraction, and the candidates this answer opens
    listed_all = set(shown_ids)
    for hits in lists.candidate_lists.values():
        listed_all.update(hits)
    refusals, outcomes, not_opened = [], {}, {}
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
        if outcome in ('归入已有的', '接续'):
            if target not in listed:
                refusals.append(f'candidate {c["id"]}: target {target!r} not in its list')
                continue
            if outcome == '归入已有的' and not store.is_open(conn, target):
                refusals.append(f'candidate {c["id"]}: cannot attach to closed view {target}')
                continue
            if outcome == '接续':
                if conn.execute('select 1 from successions where succeeds=?', (target,)).fetchone():
                    refusals.append(f'candidate {c["id"]}: {target} already has a successor')
                    continue
                if target in succession_targets:
                    refusals.append(f'candidate {c["id"]}: {target} can have one successor; {succession_targets[target]} already succeeds it in this answer')
                    continue
                succession_targets[target] = c['id']
                previous = store.rungs_of(conn, target)
                if previous and not same_orientation(previous, c['rungs']):
                    refusals.append(f'candidate {c["id"]}: successor ladder orientation differs from {target}')
                    continue
        if outcome in ('新观点', '接续'):
            object_id = universe.resolve(c['object'])
            if not object_id:
                not_opened[c['id']] = f'object {c["object"]!r} not on the research list'
                if c['kind'] == '主题观点':
                    store.pool(conn, 'suggested_theme', c['object'], {'question': c['question'], 'input_id': None}, 0)
                outcomes[c['id']] = ('不开', None, [])
                continue
            outcomes[c['id']] = (outcome, target or None, [])
            raw_deps[c['id']] = d.get('dependencies', [])
        elif outcome == '归入已有的':
            outcomes[c['id']] = (outcome, target, [])
        else:
            outcomes[c['id']] = ('不开', None, [])
            not_opened[c['id']] = d.get('reason', '')
    # dependencies, once every candidate's outcome is known
    opened = {cid for cid, (outcome, _, _) in outcomes.items() if outcome in ('新观点', '接续')}
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
    evidence_out = {}
    answered_e = {(d['id'], d['view_id']): d for d in decisions.get('evidence', [])}
    for key, listed in lists.evidence_lists.items():
        d = answered_e.get(key)
        if not d:
            refusals.append(f'evidence {key[0]} under {key[1]} has no decision')
            continue
        outcome, target = d['outcome'], d['target_evidence_id'].strip()
        if outcome in ('重复', '替代'):
            if target not in listed:
                refusals.append(f'evidence {key[0]}: target {target!r} not among {key[1]}\'s evidence shown')
                continue
            evidence_out[key] = (outcome, target, d['said_day'].strip())
        else:
            evidence_out[key] = ('新证据', None, d['said_day'].strip())
    return Checked(outcomes, evidence_out, refusals, not_opened)
