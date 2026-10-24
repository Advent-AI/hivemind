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
    system, user = build_prompt(item, text, shown_views, universe, setting.prompt_version.rpartition('-')[2])
    answer = model.call(archive, cfg, setting, system, user, SCHEMA, 'extraction', 'extract', transport=transport)
    evidence, candidates, dropped = sift(answer.data, item, text, {v['view_id'] for v in shown_views})
    return Handover(evidence, candidates, dropped, answer.call_id, answer.request_sha256, answer.cached, answer.cost_usd)


def sift(data, item, text, shown_ids):
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
