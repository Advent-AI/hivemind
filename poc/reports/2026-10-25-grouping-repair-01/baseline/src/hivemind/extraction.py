"""Extraction (docs/prd/05-extraction.md): the whole item goes to the model with the five-block prompt of its
category; the answer is evidence linked to the shown views or to this item's candidate views, and candidate views
written in full. Code checks the sources (the quote is in the text, every link points at a shown view or a
candidate), the ladders (five rungs or two) and the rule that quarterly numbers are evidence, not views."""
import dataclasses
import json
import os
import re

from . import config, model

PROMPTS = os.path.join(os.path.dirname(__file__), 'prompts')
TIERS = ['发生的事', '当事人说的', '第三方看法', '传闻']
MAX_TEXT_CHARS = 400_000

SCHEMA = {
    'type': 'object', 'additionalProperties': False, 'required': ['evidence', 'candidates'],
    'properties': {
        'evidence': {'type': 'array', 'items': {
            'type': 'object', 'additionalProperties': False,
            'required': ['id', 'quote', 'one_line', 'speaker', 'original_who', 'original_day', 'tier', 'event_time', 'links'],
            'properties': {
                'id': {'type': 'string'}, 'quote': {'type': 'string'}, 'one_line': {'type': 'string'}, 'speaker': {'type': 'string'},
                'original_who': {'type': 'string'}, 'original_day': {'type': 'string'}, 'tier': {'type': 'string', 'enum': TIERS},
                'event_time': {'type': 'string'}, 'links': {'type': 'array', 'items': {'type': 'string'}}}}},
        'candidates': {'type': 'array', 'items': {
            'type': 'object', 'additionalProperties': False,
            'required': ['id', 'object', 'kind', 'looks_at', 'question', 'rungs', 'due_day', 'year', 'evidence_ids'],
            'properties': {
                'id': {'type': 'string'}, 'object': {'type': 'string'}, 'kind': {'type': 'string', 'enum': ['对象观点', '主题观点']},
                'looks_at': {'type': 'string'}, 'question': {'type': 'string'},
                'rungs': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['label', 'condition'],
                                                       'properties': {'label': {'type': 'string'}, 'condition': {'type': 'string'}}}},
                'due_day': {'type': 'string', 'pattern': r'^\d{4}-\d{2}-\d{2}$'},      # a date, enforced by the schema, not by prose
                'year': {'type': 'string'}, 'evidence_ids': {'type': 'array', 'items': {'type': 'string'}}}}},
    },
}

# keyed-views-plan.md 2.1: the key a candidate carries from prompt version v4 on; the ladder's rungs carry numeric bounds
MEASURES = ['total_revenue', 'segment_revenue', 'product_revenue', 'gross_margin', 'operating_margin', 'operating_expense_growth', 'total_expenses', 'operating_loss',
            'tax_rate', 'capex', 'shipments_or_capacity', 'run_rate', 'design_wins', 'event', 'spend_total', 'financing_amount', 'price', 'capacity', 'growth_rate', 'policy_event', 'other']
EVENT_TYPES = ['launch', 'shipment', 'licence', 'approval', 'deal_close', 'deployment', 'other', 'n/a']
BASES = ['GAAP', 'non_GAAP', 'n/a']
UNITS = ['USD', 'percent', 'count', 'GW', 'MW', 'TWD', 'multiple', 'n/a']
KEY_FIELDS = {'measure': {'type': 'string', 'enum': MEASURES}, 'scope': {'type': 'string'},
              'period_start': {'type': 'string', 'pattern': r'^\d{4}-\d{2}-\d{2}$'}, 'period_end': {'type': 'string', 'pattern': r'^\d{4}-\d{2}-\d{2}$'},
              'basis': {'type': 'string', 'enum': BASES}, 'unit': {'type': 'string', 'enum': UNITS}, 'event_type': {'type': 'string', 'enum': EVENT_TYPES}}
BOUND = {'anyOf': [{'type': 'number'}, {'type': 'null'}]}


def keyed_schema():
    """SCHEMA with the key fields on every candidate and numeric bounds on every rung."""
    schema = json.loads(json.dumps(SCHEMA))
    candidate = schema['properties']['candidates']['items']
    candidate['properties'].update(KEY_FIELDS)
    candidate['required'] += list(KEY_FIELDS)
    rung = candidate['properties']['rungs']['items']
    rung['properties'].update({'lo': BOUND, 'hi': BOUND})
    rung['required'] += ['lo', 'hi']
    return schema


def schema_for(version):
    return keyed_schema() if version and int(version.lstrip('v') or 0) >= 4 else SCHEMA


@dataclasses.dataclass
class Handover:
    evidence: list
    candidates: list
    dropped: list
    call_id: int
    request_sha256: str
    cached: bool
    cost_usd: float


SELF_PUBLISHER_TYPE = 'self'      # the owner's own memo (02-classification T8, D59): its judgements are candidates without evidence


def _read(name):
    with open(config.prompt_path(name), encoding='utf-8') as handle:
        return handle.read()


def _categories(version):
    return json.loads(_read(f'categories-{version}.json'))


def normalise(text):
    return re.sub(r'\s+', ' ', text).strip().lower()


def build_prompt(item, text, shown_views, universe, version='v1'):
    """The five blocks of 05-extraction: role; this category and how to read it; who it is about plus the list's
    themes; what to read out; the objects' existing views with who depends on whom (no state, no evidence)."""
    category = item['category']
    categories = _categories(version)
    blocks = categories.get(category) or categories['T7']
    objects = [o['value'] for o in item.get('object_identifiers') or []]
    themes = '\n'.join(f'  - {theme_id}：{name}' for theme_id, name in universe.theme_list())
    fiscal = '\n'.join(note for note in (universe.fiscal_note(o, item['publication_day']) for o in objects) if note)
    system = _read(f'role-{version}.txt')
    parts = [
        f'【这一类是什么、怎么读】{category}。{blocks["what"]}',
        f'【讲的是谁】这条信息的相关对象：{"、".join(objects) or "（上游没有标）"}。候选观点讲的是公司时，object 写股票代码；讲的是主题时，从下面名单里挑一个写编号，名单里没有的写清是什么事：\n{themes}'
        + (f'\n财年说明（数字观点的年份和到期日按这个算）：\n{fiscal}' if fiscal else ''),
        f'【这一类要读出什么】{blocks["read"]}',
    ]
    if version and int(version.lstrip('v') or 0) >= 4:      # keyed-views-plan.md 2.4: the quantities the analyst watches, with the exact scope names to copy
        watched = []
        for o in objects:
            entries = universe.watch_list(o) if hasattr(universe, 'watch_list') else []
            if entries:
                watched.append(f'  - {o}：' + '；'.join(e['measure'] + (f"[{e['scope']}]" if e.get('scope') else '') + (f"({e['event_type']})" if e.get('event_type') else '') for e in entries))
        if watched:
            parts.append('【要盯的量】这些对象分析师盯的量（measure[scope](event_type)）。候选观点的 measure 和 scope 照这里的写法填；清单外的量照样写出来，代码会放进复核池而不开：\n' + '\n'.join(watched))
    if shown_views:
        lines = []
        for v in shown_views:       # 05-extraction block 5: question, looks_at, due day and who depends on whom; no state, no evidence
            deps = f'；依赖：{"、".join(v["depends_on"])}' if v.get('depends_on') else ''
            lines.append(f'  - {v["view_id"]}（{v["object_id"]}，看的是「{v["looks_at"]}」，到期 {v["due_day"]}）：{v["question"]}{deps}')
        parts.append('【这些对象已有的观点】证据连到这些观点上，用它们的编号；它们管不到的才写候选观点：\n' + '\n'.join(lines))
    else:
        parts.append('【这些对象已有的观点】还没有。该开的都写成候选观点。')
    parts.append(f'【信息】编号 {item["input_id"]}，类别 {category}，作者 {item.get("publisher")}（{item.get("publisher_type")}），发布日 {item.get("publication_day")}，标题：{item.get("title") or ""}\n\n' + text[:MAX_TEXT_CHARS])
    parts.append('按 JSON schema 交出 evidence 和 candidates。候选观点的 evidence_ids 填它自己的证据编号；证据的 links 填已有观点编号或这次候选观点的编号（如 c1）。没有可抽的就都交空数组。')
    return system, '\n\n'.join(parts)


OBJECT_LABELS = ['强烈看多', '看多', '中性', '看空', '强烈看空']


def check_ladder(rungs, kind):
    """None when the ladder is well formed, else the problem. An object ladder written from 强烈看空 up to 强烈看多
    (the model often orders a revenue ladder by rising value) is the same ladder; normalise_ladder turns it round."""
    if len(rungs) not in (2, 5):
        return f'ladder has {len(rungs)} rungs, needs 5 (or 2 for yes/no)'
    if any(not r['label'].strip() or not r['condition'].strip() for r in rungs):
        return 'a rung has an empty label or condition'
    if kind == '对象观点' and len(rungs) == 5:
        labels = [r['label'].strip() for r in rungs]
        if labels != OBJECT_LABELS and labels != OBJECT_LABELS[::-1]:
            return f'object view rungs must be {OBJECT_LABELS}, got {labels}'
    return None


def normalise_ladder(rungs, kind):
    """Position 1 is 强烈看多 (06-views): a reversed object ladder is turned round, label and condition together."""
    if kind == '对象观点' and len(rungs) == 5 and [r['label'].strip() for r in rungs] == OBJECT_LABELS[::-1]:
        return list(reversed(rungs))
    return rungs


QUARTERLY = re.compile(r'(\bQ[1-4]\b|第[一二三四1-4]季|季度|\bquarter(?!ly report)|fiscal Q[1-4]|\bH[12]\b 收入|上半年收入|下半年收入)', re.I)


def extract(archive, cfg, item, text, shown_views, universe, *, transport=None):
    setting = cfg.extraction_setting(item['category'])
    version = setting.prompt_version.rpartition('-')[2]
    system, user = build_prompt(item, text, shown_views, universe, version)
    answer = model.call(archive, cfg, setting, system, user, schema_for(version), 'extraction', 'extract', transport=transport)
    evidence, candidates, dropped = sift(answer.data, item, text, {v['view_id'] for v in shown_views}, universe)
    return Handover(evidence, candidates, dropped, answer.call_id, answer.request_sha256, answer.cached, answer.cost_usd)


def check_bounds(rungs):
    """None when the rungs' numeric bounds form one unbroken partition (or none carries bounds), else the problem."""
    bounded = [r for r in rungs if r.get('lo') is not None or r.get('hi') is not None]
    if not bounded:
        return None
    if len(bounded) != len(rungs):
        return 'some rungs carry bounds and some do not'
    ordered = sorted(rungs, key=lambda r: -1e300 if r.get('lo') is None else float(r['lo']))
    for a, b in zip(ordered, ordered[1:]):
        if a.get('hi') is None or b.get('lo') is None or float(a['hi']) != float(b['lo']):
            return 'rung bounds overlap or leave a gap'
    if ordered[-1].get('hi') is not None:
        return 'the top rung must be open above'
    return None


def sift(data, item, text, shown_ids, universe=None):
    """05-extraction step 3, the code checks on one answer: ladders, the quarter and year rules, due days, quotes in
    the text, links to shown views or kept candidates, one piece per sentence. Returns (evidence, candidates,
    dropped); the preflight runs it over every stored answer."""
    body = normalise(text)
    dropped = []
    candidates = []
    candidate_ids = set()
    for c in data.get('candidates', []):
        problem = check_ladder(c['rungs'], c['kind'])
        if problem:
            dropped.append((c['id'], f'candidate ladder: {problem}'))
            continue
        c = dict(c, rungs=normalise_ladder(c['rungs'], c['kind']))
        if QUARTERLY.search(c['looks_at'] + ' ' + c['question']) and c['kind'] == '对象观点':
            dropped.append((c['id'], 'quarterly number: evidence, not a view (06-views ladder rule 6)'))
            continue
        year_match = re.search(r'(\d{4})', c['year'] or '')
        if year_match and int(year_match.group(1)) > int(item['publication_day'][:4]) + 1:
            dropped.append((c['id'], f'year {c["year"]} is beyond next year: not opened (06-views 不开)'))
            continue
        if not re.match(r'\d{4}-\d{2}-\d{2}$', c['due_day']):
            dropped.append((c['id'], f'due_day not a date: {c["due_day"]!r}'))
            continue
        if c['due_day'] <= item['publication_day']:
            dropped.append((c['id'], f'due_day {c["due_day"]} not after the item'))
            continue
        if c.get('measure'):          # keyed candidates: bounds must partition, and the key must be on the object's watch list (2.4)
            problem = check_bounds(c['rungs'])
            if problem:
                dropped.append((c['id'], f'candidate ladder bounds: {problem}'))
                continue
            if universe is not None:
                object_id = universe.resolve(c['object']) or c['object']
                if not universe.watch_allows(object_id, c['measure'], c.get('scope', ''), c.get('event_type', 'n/a')):
                    dropped.append((c['id'], f'watch: {c["measure"]}[{c.get("scope", "")}] is not on {c["object"]}\'s list; review pool'))
                    continue
                scope, source = universe.scope_and_source(object_id, c['measure'], c.get('scope', ''), c.get('event_type', 'n/a'))
                c = dict(c, scope=scope, scope_source=source)                                                                            # code owns the scope's spelling
                if c['measure'] not in ('event', 'policy_event'):
                    period = universe.fiscal_period(object_id, c.get('year', ''))                                                        # and the period of a yearly number
                    if period:
                        c = dict(c, period_start=period[0], period_end=period[1])
        candidates.append(c)
        candidate_ids.add(c['id'])
    evidence = []
    kept_ids = set()
    by_quote = {}
    alias = {}
    for e in data.get('evidence', []):
        quote = normalise(e['quote'])
        if len(quote) < 8 or quote not in body:
            dropped.append((e['id'], 'quote not in item'))
            continue
        links = [l for l in e['links'] if l in shown_ids or l in candidate_ids]
        if not links:
            dropped.append((e['id'], f'links to nothing shown: {e["links"]}'))
            continue
        if quote in by_quote:            # the same sentence read out twice is one piece with both links
            first = by_quote[quote]
            first['links'].extend(l for l in links if l not in first['links'])
            alias[e['id']] = first['id']
            dropped.append((e['id'], f'same quote as {first["id"]}; merged'))
            continue
        e = dict(e, links=links)
        by_quote[quote] = e
        evidence.append(e)
        kept_ids.add(e['id'])
    final_candidates = []
    for c in candidates:
        ids = list(dict.fromkeys(alias.get(i, i) for i in c['evidence_ids'] if alias.get(i, i) in kept_ids))
        if not ids and item.get('publisher_type') != SELF_PUBLISHER_TYPE:
            dropped.append((c['id'], 'candidate without surviving evidence'))
            continue
        final_candidates.append(dict(c, evidence_ids=ids))
    for e in evidence:
        e['links'] = [l for l in e['links'] if l in shown_ids or any(c['id'] == l for c in final_candidates)]
    evidence = [e for e in evidence if e['links']]
    return evidence, final_candidates, dropped
