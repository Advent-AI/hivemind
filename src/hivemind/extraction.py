"""Extraction (docs/prd/05-extraction.md): the whole item goes to the model with the five-block prompt of its
category; the answer is evidence linked to the shown views or to this item's candidate views, and candidate views
written in full. Code checks the sources (the quote is in the text, every link points at a shown view or a
candidate), the ladders (five rungs or two) and the rule that quarterly numbers are evidence, not views.

Prompt versions 1–5 ask and answer in Chinese; version 6 and later ask and answer in English (D163). The schema,
the request text and the retry note follow the version; every answer is read in the canonical vocabulary."""
import dataclasses
import datetime
import json
import re

from . import config, model, vocabulary

TIERS = vocabulary.TIERS
LEGACY_TIERS = list(vocabulary.LEGACY['tier'])
LEGACY_KINDS = list(vocabulary.LEGACY['kind'])
MAX_TEXT_CHARS = 400_000
ENGLISH_FROM = 6                  # the first extraction prompt version written in English
GROUPS_FROM = 7                   # the first version whose candidates carry research-group membership (D149)
ALIASES_FROM = 9                  # the first version whose declared groups carry aliases, so code decides identity and membership (D166)


def version_number(version):
    return int(str(version or '').lstrip('v') or 0)


def is_english(version):
    return version_number(version) >= ENGLISH_FROM


def has_groups(version):
    return version_number(version) >= GROUPS_FROM


def base_schema(english):
    kinds = vocabulary.KINDS if english else LEGACY_KINDS
    tiers = TIERS if english else LEGACY_TIERS
    return {
        'type': 'object', 'additionalProperties': False, 'required': ['evidence', 'candidates'],
        'properties': {
            'evidence': {'type': 'array', 'items': {
                'type': 'object', 'additionalProperties': False,
                'required': ['id', 'quote', 'one_line', 'speaker', 'original_who', 'original_day', 'tier', 'event_time', 'links'],
                'properties': {
                    'id': {'type': 'string'}, 'quote': {'type': 'string'}, 'one_line': {'type': 'string'}, 'speaker': {'type': 'string'},
                    'original_who': {'type': 'string'}, 'original_day': {'type': 'string'}, 'tier': {'type': 'string', 'enum': tiers},
                    'event_time': {'type': 'string'}, 'links': {'type': 'array', 'items': {'type': 'string'}}}}},
            'candidates': {'type': 'array', 'items': {
                'type': 'object', 'additionalProperties': False,
                'required': ['id', 'object', 'kind', 'looks_at', 'question', 'rungs', 'due_day', 'year', 'evidence_ids'],
                'properties': {
                    'id': {'type': 'string'}, 'object': {'type': 'string'}, 'kind': {'type': 'string', 'enum': kinds},
                    'looks_at': {'type': 'string'}, 'question': {'type': 'string'},
                    'rungs': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['label', 'condition'],
                                                           'properties': {'label': {'type': 'string'}, 'condition': {'type': 'string'}}}},
                    'due_day': {'type': 'string', 'pattern': r'^\d{4}-\d{2}-\d{2}$'},      # a date, enforced by the schema, not by prose
                    'year': {'type': 'string'}, 'evidence_ids': {'type': 'array', 'items': {'type': 'string'}}}}},
        },
    }


SCHEMA = base_schema(english=False)          # the shape of the answers stored under versions 1–3

# keyed-views-plan.md 2.1: the key a candidate carries from prompt version v4 on; the ladder's rungs carry numeric bounds
MEASURES = ['total_revenue', 'segment_revenue', 'product_revenue', 'gross_margin', 'operating_margin', 'operating_expense_growth', 'total_expenses', 'operating_loss',
            'tax_rate', 'capex', 'shipments_or_capacity', 'run_rate', 'design_wins', 'event', 'spend_total', 'financing_amount', 'price', 'capacity', 'growth_rate', 'policy_event', 'other']
EVENT_TYPES = ['launch', 'shipment', 'licence', 'approval', 'deal_close', 'deployment', 'other', 'n/a']
BASES = ['GAAP', 'non_GAAP', 'n/a']
UNITS = ['USD', 'percent', 'count', 'GW', 'MW', 'TWD', 'multiple', 'n/a']
# D167 (2026-10-25): from version 10 the vocabulary names a market's size and a project's cost as their own measures; the week filed an
# accelerator TAM and a data-center project's cost as spend_total, the aggregate of spending, which no identity rule could then tell apart
MEASURES_V10 = MEASURES[:MEASURES.index('spend_total') + 1] + ['market_size', 'project_cost'] + MEASURES[MEASURES.index('spend_total') + 1:]
MEASURES_V10_FROM = 10


def key_fields(measures=MEASURES):
    return {'measure': {'type': 'string', 'enum': list(measures)}, 'scope': {'type': 'string'},
            'period_start': {'type': 'string', 'pattern': r'^\d{4}-\d{2}-\d{2}$'}, 'period_end': {'type': 'string', 'pattern': r'^\d{4}-\d{2}-\d{2}$'},
            'basis': {'type': 'string', 'enum': BASES}, 'unit': {'type': 'string', 'enum': UNITS}, 'event_type': {'type': 'string', 'enum': EVENT_TYPES}}


BOUND = {'anyOf': [{'type': 'number'}, {'type': 'null'}]}


def keyed_schema(english=False, measures=MEASURES):
    """The base schema with the key fields on every candidate and numeric bounds on every rung."""
    schema = base_schema(english)
    candidate = schema['properties']['candidates']['items']
    fields = key_fields(measures)
    candidate['properties'].update(fields)
    candidate['required'] += list(fields)
    rung = candidate['properties']['rungs']['items']
    rung['properties'].update({'lo': BOUND, 'hi': BOUND})
    rung['required'] += ['lo', 'hi']
    return schema


LOCAL_GROUP = r'n[1-9][0-9]*'
# a company's own reported or guided lines: they belong to the company and never found a research group by themselves
FINANCIAL_LINES = {'total_revenue', 'segment_revenue', 'gross_margin', 'operating_margin', 'operating_expense_growth', 'total_expenses', 'operating_loss', 'tax_rate', 'capex', 'run_rate'}


def tracks_a_matter(candidate):
    """A candidate that can start a research group: a theme quantity, an event or policy event, a product or market figure;
    not a company's own financial line (which may join a group another thesis started, never found one)."""
    return candidate.get('kind') == 'theme' or candidate.get('measure') not in FINANCIAL_LINES


def grouped_schema(shown_group_ids, aliases=False, measures=MEASURES):
    """The English keyed schema plus research-group membership (D149, the D147 reference shape): each candidate cites one or
    more groups, each either a group id shown in this request or a local id declared in new_groups; the pattern is built
    from the shown ids, so an unseen group cannot be cited."""
    schema = keyed_schema(english=True, measures=measures)
    pattern = '^(?:' + LOCAL_GROUP + ''.join('|' + re.escape(g) for g in shown_group_ids) + ')$'
    candidate = schema['properties']['candidates']['items']
    candidate['properties']['group_refs'] = {'type': 'array', 'items': {'type': 'string', 'pattern': pattern}}
    candidate['required'].append('group_refs')
    group_fields = {'id': {'type': 'string', 'pattern': '^' + LOCAL_GROUP + '$'}, 'name': {'type': 'string'}, 'scope': {'type': 'string'}}
    if aliases:
        group_fields['aliases'] = {'type': 'array', 'items': {'type': 'string'}}
    schema['properties']['new_groups'] = {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': list(group_fields), 'properties': group_fields}}
    schema['required'].append('new_groups')
    return schema


def schema_for(version, shown_group_ids=()):
    number = version_number(version)
    measures = MEASURES_V10 if number >= MEASURES_V10_FROM else MEASURES
    if number >= GROUPS_FROM:
        return grouped_schema(shown_group_ids, aliases=number >= ALIASES_FROM, measures=measures)
    if number >= ENGLISH_FROM:
        return keyed_schema(english=True)
    return keyed_schema() if number >= 4 else SCHEMA


@dataclasses.dataclass
class Handover:
    evidence: list
    candidates: list
    dropped: list
    call_id: int
    request_sha256: str
    cached: bool
    cost_usd: float
    new_groups: list = dataclasses.field(default_factory=list)      # the declared groups a kept candidate cites: {id, name, scope}


SELF_PUBLISHER_TYPE = 'self'      # the owner's own memo (02-classification T8, D59): its judgements are candidates without evidence


def _read(name):
    with open(config.prompt_path(name), encoding='utf-8') as handle:
        return handle.read()


def _categories(version):
    return json.loads(_read(f'categories-{version}.json'))


def normalise(text):
    return re.sub(r'\s+', ' ', text).strip().lower()


def _watched_lines(objects, universe):
    """keyed-views-plan.md 2.4 / D155: the quantities the analyst watches, as a reference, with the exact scope names."""
    watched = []
    for o in objects:
        entries = universe.watch_list(o) if hasattr(universe, 'watch_list') else []
        if entries:
            sep = '; '
            watched.append(f'  - {o}: ' + sep.join(e['measure'] + (f"[{e['scope']}]" if e.get('scope') else '') + (f"({e['event_type']})" if e.get('event_type') else '') for e in entries))
    return watched


def _build_prompt_chinese(item, text, shown_views, universe, version, category, blocks, objects):
    themes = '\n'.join(f'  - {theme_id}：{name}' for theme_id, name in universe.theme_list(legacy=True))
    fiscal = '\n'.join(note for note in (universe.fiscal_note(o, item['publication_day']) for o in objects) if note)
    parts = [
        f'【这一类是什么、怎么读】{category}。{blocks["what"]}',
        f'【讲的是谁】这条信息的相关对象：{"、".join(objects) or "（上游没有标）"}。候选观点讲的是公司时，object 写股票代码；讲的是主题时，从下面名单里挑一个写编号，名单里没有的写清是什么事：\n{themes}'
        + (f'\n财年说明（数字观点的年份和到期日按这个算）：\n{fiscal}' if fiscal else ''),
        f'【这一类要读出什么】{blocks["read"]}',
    ]
    if version_number(version) >= 4:
        watched = []
        for o in objects:
            entries = universe.watch_list(o) if hasattr(universe, 'watch_list') else []
            if entries:
                watched.append(f'  - {o}：' + '；'.join(e['measure'] + (f"[{e['scope']}]" if e.get('scope') else '') + (f"({e['event_type']})" if e.get('event_type') else '') for e in entries))
        if watched:
            parts.append('【研究参考】已有的量和范围（measure[scope](event_type)）。含义相同可用现有名称；清单外的重要问题照常提出，保留实际范围：\n' + '\n'.join(watched))
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
    return '\n\n'.join(parts)


def dependency_text(view, english):
    """Who a shown view depends on, for block 5: resolved theses by id, a waiting dependency by its chain and year."""
    entries = view.get('dependencies')
    if entries is None:                                   # a caller that built the view without the structured list
        return list(view.get('depends_on') or [])
    out = []
    for entry in entries:
        if entry.get('view_id'):
            out.append(entry['view_id'])
        elif english:
            out.append(f'(waiting for the {entry["wait_year"]} thesis on chain {entry["wait_chain_view_id"]})')
        else:
            out.append(f'（等 {entry["wait_chain_view_id"]} 这条链上 {entry["wait_year"]} 年的那条）')
    return out


def groups_block(shown_groups):
    """05-extraction block 5b (D149): the research groups the model may cite, with each member's focus."""
    if not shown_groups:
        return ('[Research groups] None yet. For a candidate that tracks an ongoing matter (a product rollout, a deal, a policy process, an investment or demand cycle), '
                'declare the group in new_groups (local ids n1, n2 …) and cite it in group_refs; leave group_refs empty for a company\'s own financial lines.')
    lines = []
    for g in shown_groups:
        members = '; '.join(f'{m["view_id"]} ({m["object_id"]}) {m["looks_at"]}' for m in g.get('members', [])[:8])
        names = ', '.join(a for a in (g.get('aliases') or []) if a != g['name'])
        lines.append(f'  - {g["group_id"]} "{g["name"]}": {g["scope"]}' + (f' (also: {names})' if names else '') + (f' — members: {members}' if members else ''))
    return ('[Research groups] Cite one of these ids in group_refs when the candidate tracks that matter; declare a new group in new_groups for a matter none of them is; '
            'leave group_refs empty for a company\'s own financial lines:\n'
            + '\n'.join(lines))


def _build_prompt_english(item, text, shown_views, universe, version, category, blocks, objects, shown_groups=()):
    themes = '\n'.join(f'  - {theme_id}: {name}' for theme_id, name in universe.theme_list())
    fiscal = '\n'.join(note for note in (universe.fiscal_note(o, item['publication_day'], english=True) for o in objects) if note)
    parts = [
        f'[Category and how to read it] {category}. {blocks["what"]}',
        f'[Subjects] The objects this item concerns: {", ".join(objects) or "(not labelled upstream)"}. For a candidate thesis about a company, object is its ticker; '
        f'about a theme, choose an id from this list, or state what the matter is when none fits:\n{themes}'
        + (f'\nFiscal-year note (a numeric thesis takes its year and due date from it):\n{fiscal}' if fiscal else ''),
        f'[What to read out] {blocks["read"]}',
    ]
    watched = _watched_lines(objects, universe)
    if watched:
        parts.append('[Research reference] Existing quantities and scopes (measure[scope](event_type)). Reuse a name only when the meaning is the same; '
                     'propose important questions outside the list as usual, with their actual scope:\n' + '\n'.join(watched))
    if shown_views:
        lines = []
        for v in shown_views:       # 05-extraction block 5: question, looks_at, due day and who depends on whom; no state, no evidence
            deps = dependency_text(v, english=True)
            tail = f'; depends on: {", ".join(deps)}' if deps else ''
            lines.append(f'  - {v["view_id"]} ({v["object_id"]}, focus "{v["looks_at"]}", due {v["due_day"]}): {v["question"]}{tail}')
        parts.append('[Existing theses of these objects] Link evidence to them by id; write a candidate thesis only for a question they do not cover:\n' + '\n'.join(lines))
    else:
        parts.append('[Existing theses of these objects] None yet. Write every thesis that should open as a candidate.')
    if has_groups(version):
        parts.append(groups_block(shown_groups))
    parts.append(f'[Item] id {item["input_id"]}, category {category}, author {item.get("publisher")} ({item.get("publisher_type")}), published {item.get("publication_day")}, title: {item.get("title") or ""}\n\n' + text[:MAX_TEXT_CHARS])
    parts.append('Return evidence and candidates per the JSON schema. A candidate\'s evidence_ids are its own evidence ids; an evidence item\'s links are existing thesis ids '
                 'or this answer\'s candidate ids (such as c1). year names the fiscal or calendar year the figure covers (FY2027, or 2026 for a calendar year). '
                 'Return empty arrays when there is nothing to extract.')
    return '\n\n'.join(parts)


def build_prompt(item, text, shown_views, universe, version='v1', shown_groups=()):
    """The five blocks of 05-extraction: role; this category and how to read it; who it is about plus the list's
    themes; what to read out; the objects' existing views with who depends on whom (no state, no evidence)."""
    category = item['category']
    categories = _categories(version)
    blocks = categories.get(category) or categories['T7']
    objects = [o['value'] for o in item.get('object_identifiers') or []]
    system = _read(f'role-{version}.txt')
    if is_english(version):
        return system, _build_prompt_english(item, text, shown_views, universe, version, category, blocks, objects, shown_groups)
    return system, _build_prompt_chinese(item, text, shown_views, universe, version, category, blocks, objects)


OBJECT_LABELS = vocabulary.ASSET_LABELS


def check_ladder(rungs, kind):
    """None when the ladder is well formed, else the problem. An asset ladder written from Strongly bearish up to
    Strongly bullish (the model often orders a revenue ladder by rising value) is the same ladder; normalise_ladder
    turns it round. Labels are compared in the canonical vocabulary."""
    if len(rungs) not in (2, 5):
        return f'ladder has {len(rungs)} rungs, needs 5 (or 2 for yes/no)'
    if any(not r['label'].strip() or not r['condition'].strip() for r in rungs):
        return 'a rung has an empty label or condition'
    if kind == 'asset' and len(rungs) == 5:
        labels = [vocabulary.canonical('label', r['label']) for r in rungs]
        if labels != OBJECT_LABELS and labels != OBJECT_LABELS[::-1]:
            return f'object view rungs must be {OBJECT_LABELS}, got {labels}'
    return None


def normalise_ladder(rungs, kind):
    """Position 1 is Strongly bullish (06-views): a reversed asset ladder is turned round, label and condition together."""
    if kind == 'asset' and len(rungs) == 5 and [vocabulary.canonical('label', r['label']) for r in rungs] == OBJECT_LABELS[::-1]:
        return list(reversed(rungs))
    return rungs


# 06-views ladder rule 6: a quarterly or half-year figure is evidence, not a view. The half-year forms name a revenue
# or sales figure (H1 收入, first-half revenue); an event scheduled in a half-year (ships in H2 2026) is not a figure.
QUARTERLY = re.compile(r'(\bQ[1-4]\b|第[一二三四1-4]季|季度|\bquarter(?!ly report)|fiscal Q[1-4]|\b(?:[12]H|H[12])\b(?:\s+(?:FY)?\d{4})?\s*收入|上半年收入|下半年收入'
                       r'|\b(?:[12]H|H[12])\b(?:\s+(?:FY)?\d{4})?\s+(?:revenue|sales|net sales)|\b(?:first|second)[- ]half(?:[- ]year)?\s+(?:revenue|sales|net sales)'
                       r'|\bhalf[- ]year\s+(?:revenue|sales|net sales))', re.I)


def request_for(cfg, item, text, shown_views, universe, shown_groups=()):
    """Build the setting, complete prompt and schema without making a call."""
    setting = cfg.extraction_setting(item['category'])
    version = setting.prompt_version.rpartition('-')[2]
    system, user = build_prompt(item, text, shown_views, universe, version, shown_groups)
    group_ids = [g['group_id'] for g in shown_groups]
    return setting, system, user, schema_for(version, group_ids)


def extract(archive, cfg, item, text, shown_views, universe, *, shown_groups=(), transport=None):
    setting, system, user, schema = request_for(cfg, item, text, shown_views, universe, shown_groups)
    version = setting.prompt_version.rpartition('-')[2]
    group_ids = [g['group_id'] for g in shown_groups]
    answer = model.call(archive, cfg, setting, system, user, schema, 'extraction', 'extract', transport=transport)
    evidence, candidates, dropped, new_groups = sift_with_groups(answer.data, item, text, {v['view_id'] for v in shown_views}, universe, english=is_english(version), shown_group_ids=group_ids)
    return Handover(evidence, candidates, dropped, answer.call_id, answer.request_sha256, answer.cached, answer.cost_usd, new_groups)


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


def check_group_refs(c, shown_group_ids, declared):
    """None when a candidate's research-group references are well formed: no repeats, each a shown group id or a declared
    local id; empty is allowed (a company's own financial line belongs to the company, not to a group); else the problem."""
    refs = c.get('group_refs')
    if refs is None:
        return None                     # a version before groups
    if len(refs) != len(set(refs)):
        return 'group_refs repeats a group'
    unknown = [r for r in refs if r not in shown_group_ids and r not in declared]
    if unknown:
        return f'group_refs cites a group neither shown nor declared: {unknown}'
    return None


def sift_with_groups(data, item, text, shown_ids, universe=None, english=False, shown_group_ids=()):
    """sift, plus the research-group declarations (D149): candidates with bad references are dropped; a declared group is
    kept only when a kept candidate cites it (an unused declaration is ignored, D147). Returns (evidence, candidates, dropped, new_groups)."""
    declared = {}
    for g in data.get('new_groups', []) or []:
        if g['id'] in declared or not g['name'].strip() or not g['scope'].strip():
            declared = None
            break
        declared[g['id']] = {'id': g['id'], 'name': g['name'].strip(), 'scope': g['scope'].strip(), 'aliases': [a.strip() for a in g.get('aliases') or [] if a.strip()]}
    dropped_refs = []
    if declared is None:         # malformed declarations: every candidate citing a local id is dropped, shown ids still work
        declared = {}
    checked = dict(data, candidates=[])
    for c in data.get('candidates', []):
        problem = check_group_refs(c, set(shown_group_ids), declared)
        if problem:
            dropped_refs.append((c['id'], f'candidate group: {problem}'))
            continue
        checked['candidates'].append(c)
    evidence, candidates, dropped = sift(checked, item, text, shown_ids, universe, english=english)
    used = {r for c in candidates for r in c.get('group_refs', [])}
    return evidence, candidates, dropped_refs + dropped, [declared[g] for g in declared if g in used]


def sift(data, item, text, shown_ids, universe=None, english=False):
    """05-extraction step 3, the code checks on one answer: ladders, the quarter and year rules, due days, quotes in
    the text, links to shown views or kept candidates, one piece per sentence. Returns (evidence, candidates,
    dropped); the preflight runs it over every stored answer. The answer is read in the canonical vocabulary,
    whichever prompt version wrote it; english says which version's year contract applies (a bare year is a calendar
    year under the English versions, the company's fiscal year under the Chinese ones)."""
    data = vocabulary.extraction_answer(data)
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
        if QUARTERLY.search(c['looks_at'] + ' ' + c['question']) and c['kind'] == 'asset':
            dropped.append((c['id'], 'quarterly number: evidence, not a view (06-views ladder rule 6)'))
            continue
        year_match = re.search(r'(\d{4})', c['year'] or '')
        if c.get('measure') not in ('event', 'policy_event') and year_match and int(year_match.group(1)) > int(item['publication_day'][:4]) + 1:
            dropped.append((c['id'], f'year {c["year"]} is beyond next year: not opened (06-views 不开)'))
            continue
        if not re.match(r'\d{4}-\d{2}-\d{2}$', c['due_day']):
            dropped.append((c['id'], f'due_day not a date: {c["due_day"]!r}'))
            continue
        if c['due_day'] <= item['publication_day']:
            dropped.append((c['id'], f'due_day {c["due_day"]} not after the item'))
            continue
        if c.get('measure'):          # keyed candidates keep their actual scope; reference lists do not gate admission (D155)
            problem = check_bounds(c['rungs'])
            if problem:
                dropped.append((c['id'], f'candidate ladder bounds: {problem}'))
                continue
            if universe is not None:
                object_id = universe.resolve(c['object']) or c['object']
                scope, source = universe.scope_and_source(object_id, c['measure'], c.get('scope', ''), c.get('event_type', 'n/a'))
                c = dict(c, object=object_id, scope=scope, scope_source=source, key_version=2)
                if c['measure'] not in ('event', 'policy_event'):
                    period = universe.fiscal_period(object_id, c.get('year', ''), bare_is_calendar=english)                             # and the period of a yearly number
                    if period:
                        c = dict(c, period_start=period[0], period_end=period[1])
            try:
                start = datetime.date.fromisoformat(c['period_start'])
                end = datetime.date.fromisoformat(c['period_end'])
                if start > end:
                    raise ValueError('start after end')
            except (KeyError, ValueError):
                dropped.append((c['id'], 'invalid period: expected real dates with start <= end'))
                continue
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
