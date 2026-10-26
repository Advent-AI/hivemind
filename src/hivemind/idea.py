"""An idea mapped against the library in two model calls, with the service doing every lookup in between
(docs/poc/idea-card.md, D112, D135). Call 1 breaks the idea into typed parts (object, what to look for, period,
a search query) and reads a dollar claim. The service then searches once per part, keeps the candidates each part
got, and asks call 2 to map each part to its candidates and write the summary. The service admits only candidate
ids, follows the ledger's dependency graph from the mapped views to their upstream and downstream views, evaluates
the claim itself, and builds the card with every view in the front end's shape. An explicitly configured final
call writes the analyst summary after selection. The calls are archived; exact requests replay for $0."""
import json
import re
import time

from . import bundle, config, idea_composite, model, search, service
from .views import store

DECOMPOSE = {
    'type': 'object', 'additionalProperties': False, 'required': ['parts', 'claim'],
    'properties': {
        'parts': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['object', 'looks_for', 'period', 'query'],
                                             'properties': {'object': {'type': 'string'}, 'looks_for': {'type': 'string'}, 'period': {'type': 'string'}, 'query': {'type': 'string'}}}},
        'claim': {'anyOf': [{'type': 'null'},
                            {'type': 'object', 'additionalProperties': False, 'required': ['part', 'comparator', 'value_usd'],
                             'properties': {'part': {'type': 'integer'}, 'comparator': {'type': 'string', 'enum': ['>=', '<', '=']}, 'value_usd': {'type': 'number'}}}]},
    },
}
MAP = {
    'type': 'object', 'additionalProperties': False, 'required': ['parts', 'summary'],
    'properties': {
        'parts': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['index', 'views', 'why'],
                                             'properties': {'index': {'type': 'integer'},
                                                            'views': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['view_id', 'fit'],
                                                                                                 'properties': {'view_id': {'type': 'string'}, 'fit': {'type': 'string', 'enum': ['direct', 'driver', 'context']}}}},
                                                            'why': {'type': 'string'}}}},
        'summary': {'type': 'string'},
    },
}
MAP_LEAN = {
    'type': 'object', 'additionalProperties': False, 'required': ['parts', 'summary'],
    'properties': {
        'parts': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['index', 'views'],
                                             'properties': {'index': {'type': 'integer'},
                                                            'views': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['view_id', 'fit'],
                                                                                                 'properties': {'view_id': {'type': 'string'}, 'fit': {'type': 'string', 'enum': ['direct', 'driver', 'context']}}}}}}},
        'summary': {'type': 'string'},
    },
}


def full_payload(text, as_of, parts, candidates, idea_rows):
    """The mapping call's message up to idea-v7: every part with its candidates written out, then the idea's own rows."""
    return (f'Idea: {text}\nDay: {as_of}\n\nParts and the candidates the library found for each:\n'
            + json.dumps([{'index': i, 'object': p['object'], 'looks_for': p['looks_for'], 'period': p['period'], 'candidates': candidates[i]} for i, p in enumerate(parts)], ensure_ascii=False)
            + "\n\nThe idea's own search results:\n" + json.dumps(idea_rows, ensure_ascii=False))


def lean_payload(text, as_of, parts, candidates, idea_rows):
    """The mapping call's message from idea-v8: parts carry candidate ids, every candidate is written once (measured
    2026-10-24: 28 briefs per message, 15 distinct, 45% of the text a repeat), the idea's own results are ids."""
    table = {}
    for rows in candidates + [idea_rows]:
        for r in rows:
            table.setdefault(r['view_id'], r)
    return (f'Idea: {text}\nDay: {as_of}\n\nParts and the ids of the candidates the library found for each:\n'
            + json.dumps([{'index': i, 'object': p['object'], 'looks_for': p['looks_for'], 'period': p['period'], 'candidates': [r['view_id'] for r in candidates[i]]} for i, p in enumerate(parts)], ensure_ascii=False)
            + '\n\nThe candidates, each once:\n' + json.dumps(list(table.values()), ensure_ascii=False)
            + "\n\nThe idea's own search results (ids):\n" + json.dumps([r['view_id'] for r in idea_rows]))


MAP_CLAUSE = {
    'type': 'object', 'additionalProperties': False, 'required': ['parts', 'summary'],
    'properties': {
        'parts': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['index', 'views', 'why'],
                                             'properties': {'index': {'type': 'integer'},
                                                            'views': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['view_id', 'fit', 'clause'],
                                                                                                 'properties': {'view_id': {'type': 'string'}, 'fit': {'type': 'string', 'enum': ['direct', 'driver', 'context']},
                                                                                                                'clause': {'type': 'string'}}}},
                                                            'why': {'type': 'string'}}}},
        'summary': {'type': 'string'},
    },
}

# the mapping schema and payload shape belong to the prompt that describes them (an example is an instruction):
# a prompt version not listed here uses the idea-v7 contract
CONTRACTS = {'idea-v8': (MAP_LEAN, lean_payload), 'idea-v9': (MAP_LEAN, full_payload), 'idea-v10': (MAP_CLAUSE, full_payload), 'idea-v12': (MAP, lean_payload)}
SUMMARY = {'type': 'object', 'additionalProperties': False, 'required': ['summary'],
           'properties': {'summary': {'type': 'string'}}}
MARKET_READING = re.compile(r'share price|stock price|price target|market cap|valuation|multiple|p/e\b|股价|市值|估值', re.I)
CJK = re.compile(r'[\u4e00-\u9fff]')
YEAR = re.compile(r'(FY\s?20\d\d|20\d\d)', re.I)
MONEY_IN_IDEA = re.compile(r'\$\s?\d|\d[\d,.]*\s*(?:billion|bn|trillion|tn|million|mn|[bBmMtT]\b|万亿|千亿|亿|万美元|美元|%)', re.I)
NO_COST = {'usd': 0.0, 'input_tokens': 0, 'output_tokens': 0, 'seconds': 0.0, 'cached': False, 'turns': 0}
PER_PART = 8          # candidates kept per part
DRIVERS_PER_PART = 3  # the model orders drivers most direct first; the rest is noise on the canvas (measured 2026-10-24: six-driver parts on a one-line idea)
IDEA_ROWS = 5         # candidates kept from the idea's own search
MAX_PARTS = 4


def prompts(setting):
    """The two system prompts of the setting's file, split at the marker line."""
    with open(config.prompt_path(setting.prompt_version + '.txt'), encoding='utf-8') as handle:
        decompose, _, mapping = handle.read().partition('=== map ===')
    if not mapping.strip():
        raise config.ConfigError(f'{setting.prompt_version}.txt has no "=== map ===" section')
    return decompose.strip(), mapping.strip()


def object_list(ledger, as_of, aliases=None):
    """What the library covers, in one line: each object with open views as of the day and its count, then the
    universe's objects with no view yet. About 250 characters on the sealed ledger against 5,095 for a full catalog."""
    counts, kinds = {}, {}
    for record in service.views(ledger, None, as_of):
        counts[record['object']] = counts.get(record['object'], 0) + 1
        kinds[record['object']] = record['object_kind']
    covered = '; '.join(f'{obj} ({kinds[obj]}) {n}' for obj, n in sorted(counts.items(), key=lambda kv: -kv[1]))
    missing = sorted(o for o in (aliases or {}) if o not in counts)
    return (f'Objects with open views as of {as_of} (object, kind, number of views): {covered}.'
            + (f' Objects in the universe with no view yet: {", ".join(missing)}.' if missing else ''))


def judged(ledger, view_id, as_of, detailed=False):
    state = service.state_as_of(ledger, view_id, as_of)
    if not state:
        return None
    rung = next((g for g in store.rungs_of(ledger, view_id) if g['position'] == state['position']), {})
    result = {'position': state['position'], 'label': rung.get('label', '')}
    if detailed:
        result.update(condition=rung.get('condition', ''), day=state['judgement_day'], reasons=state['reasons'])
    return result


def brief(ledger, results, as_of, detailed=False):
    """Candidate state at the requested date; analyst context is explicit and versioned by the caller."""
    records = []
    for result in results:
        record = {'view_id': result['view_id'], 'object': result['object'], 'looks_at': result['looks_at'],
                  'judged': judged(ledger, result['view_id'], as_of, detailed)}
        if detailed:
            record['question'] = result['question']
        records.append(record)
    return records


def related_views(ledger, view_ids, as_of, exclude=()):
    """The given views' neighbours in the ledger's dependency graph, as of the day: what each depends on (upstream)
    and what depends on it (downstream), with the judged position; `exclude` are views already on the card.
    Deterministic and free; the model is not asked. The card follows the graph only from the views of the first
    part, the thing the idea is about: from every mapped view it fanned out to 12 cards on a one-line idea."""
    out, seen = [], set(view_ids) | set(exclude)
    for view_id in view_ids:
        for dep in service.dependencies(ledger, view_id, as_of):
            target = ledger.execute('select * from views where view_id=?', (dep['view_id'],)).fetchone()
            if dep['view_id'] not in seen and target is not None and service.view_exists(ledger, target, as_of):
                seen.add(dep['view_id'])
                out.append({'view_id': dep['view_id'], 'via': view_id, 'relation': 'upstream', 'direction': dep['direction'], 'judged': judged(ledger, dep['view_id'], as_of)})
        for other in service.dependants(ledger, view_id, as_of):
            if other not in seen:
                seen.add(other)
                out.append({'view_id': other, 'via': view_id, 'relation': 'downstream', 'direction': None, 'judged': judged(ledger, other, as_of)})
    return out


def service_direct(part, directs, looks_at):
    """The first part's direct view: among the views the model called direct, in the order the part's own search
    ranked them, the first whose text carries the part's year (a fiscal year that covers the calendar year counts:
    FY2027 for "2026"); a part that names no year takes the first. The model's label picks the quantity, the year
    check and the search order keep the pick the same across samples. Until 2026-10-24 the rule took the top search
    hit on object and year alone and overrode the model's label in 4 of 31 picks (TSMC capex → TSMC revenue, Meta
    capex → total expenses, NVIDIA total revenue → a segment, Rubin revenue → total revenue); there is no object
    test, because a theme's view (TSMC capex under supply-chain-shift) is a company part's direct view."""
    years = {y.upper().replace(' ', '') for y in YEAR.findall(part.get('period', '') + ' ' + part.get('looks_for', ''))}
    covered = set(years)
    for y in list(years):
        if y.isdigit():
            covered |= {f'FY{y}', f'FY{int(y) + 1}'}
    for view_id in directs:
        text_years = {y.upper().replace(' ', '') for y in YEAR.findall(looks_at.get(view_id) or '')}
        if not years or covered & text_years:
            return view_id
    return None


def english(*fields):
    return not any(CJK.search(str(f or '')) for f in fields)


def call_english(archive, cfg, setting, system, user, schema, name, transport, fields_of):
    """One model call whose answer must be English (D133): when a field comes back in Chinese the call is made once
    more with the instruction repeated; the second answer stands either way, and the slip is counted."""
    made = [model.call(archive, cfg, setting, system, user, schema, name, 'idea', transport=transport)]
    slips = 0
    if not english(*fields_of(made[-1].data)):
        slips = 1
        made.append(model.call(archive, cfg, setting, system, user + '\n\nWrite every field in English.', schema, name, 'idea', transport=transport))
        slips += 0 if english(*fields_of(made[-1].data)) else 1
    return made, slips


def canonical_query(part, aliases=None):
    """The service's own query for a part: the object's id (a ticker or theme id, itself an alias the search boosts),
    what the part looks for, the period. The model's free-text query varies between samples and so do its
    candidates; this one does not (iteration 8)."""
    return ' '.join(x for x in (part.get('object', ''), part.get('looks_for', ''), part.get('period', '')) if x).strip()


def merged(first, second, limit):
    """Two ranked lists interleaved without repeats, the first list's top first."""
    out, seen = [], set()
    for a, b in zip(first + [None] * len(second), second + [None] * len(first)):
        for r in (a, b):
            if r is not None and r['view_id'] not in seen:
                seen.add(r['view_id'])
                out.append(r)
    return out[:limit]


def read_idea(ledger, index, items, archive, cfg, text, as_of=None, k=10, aliases=None, semantic=True, transport=None, bundles=True, embed=search.openai_embeddings, on_progress=None):
    """The idea card: idea, what the idea's own search found, the reading (typed parts, the candidates each got, the
    views each maps to, the summary, the claim), the related views from the dependency graph, the evaluation, every
    view's bundle, the days, the trace of searches, and all call costs. No recorded view → no model call."""
    text = (text or '').strip()
    if not text:
        raise ValueError('an idea needs text')
    as_of = as_of or service.default_as_of(ledger)
    report = on_progress or (lambda stage: None)
    report('search')
    found = search.search(ledger, index, text, k, as_of, aliases=aliases, semantic=semantic, embed=embed)
    card = {'idea': {'text': text, 'as_of': as_of}, 'search': {'mode': found['mode'], 'candidates': [r['view_id'] for r in found['results'] or []]},
            'reading': None, 'evaluation': None, 'related': [], 'views': [], 'days': bundle.days(ledger, as_of),
            'no_recorded_view': found['results'] is None, 'cost': dict(NO_COST)}
    if found['results'] is None:
        return card
    setting = cfg.idea
    if setting is None:
        raise config.ConfigError(f'config {cfg.version} has no idea setting')
    decompose_prompt, map_prompt = prompts(setting)
    started = time.time()
    cost = dict(NO_COST)
    cost['cached'] = True

    def spend(answer):
        cost['usd'] += answer.cost_usd
        cost['input_tokens'] += answer.input_tokens
        cost['output_tokens'] += answer.output_tokens
        cost['turns'] += 1
        cost['cached'] = cost['cached'] and answer.cached

    # call 1: the parts
    report('decompose')
    user = f'Idea: {text}\nDay: {as_of} (the library as judged on this day)\n\n{object_list(ledger, as_of, aliases)}'
    made, slips = call_english(archive, cfg, setting, decompose_prompt, user, DECOMPOSE, 'idea_decompose', transport,
                               lambda d: [f for p in d['parts'] for f in (p['looks_for'], p['period'])])
    for answer in made:
        spend(answer)
    first = made[-1]
    parts = [dict(p) for p in first.data['parts'][:MAX_PARTS]]
    # the service: one search per part, the candidates each part got
    report('retrieve')
    detailed = setting.prompt_version == 'idea-v12'
    idea_rows = brief(ledger, found['results'][:IDEA_ROWS], as_of, detailed)
    trace, candidates, ranks = [], [], []
    queries = [((part.get('query') or '').strip() or canonical_query(part, aliases), canonical_query(part, aliases)) for part in parts]
    if semantic and found['mode'] == 'semantic':
        search.warm_queries(index, [q for pair in queries for q in pair], embed)      # one embeddings round trip for every part instead of two per part
    # a part's candidates: the service's canonical query and the model's own, interleaved (tried 2026-10-25 and dropped:
    # the object's views ranked by the idea text alone lost the model's finds, gold direct right 17 → 15 of 19)
    for i, (part, (query, own)) in enumerate(zip(parts, queries)):
        hit = search.search(ledger, index, query, PER_PART, as_of, aliases=aliases, semantic=semantic, embed=embed)
        steady = search.search(ledger, index, own, PER_PART, as_of, aliases=aliases, semantic=semantic, embed=embed) if own.lower() != query.lower() else hit
        rows = brief(ledger, merged(steady['results'] or [], hit['results'] or [], PER_PART), as_of, detailed)
        candidates.append(rows)
        ranks.append({r['view_id']: n for n, r in enumerate(hit['results'] or [])})      # the part's own search order, the tie-break among the model's direct views
        trace.append({'tool': 'search', 'part': i, 'query': query, 'canonical': own, 'returned': [r['view_id'] for r in rows]})
    # call 2: the mapping
    report('map')
    map_schema, payload = CONTRACTS.get(setting.prompt_version, (MAP, full_payload))
    user = payload(text, as_of, parts, candidates, idea_rows)
    made, more = call_english(archive, cfg, setting, map_prompt, user, map_schema, 'idea_map', transport,
                              lambda d: [d['summary'], *(p.get('why', '') for p in d['parts'])])
    slips += more
    for answer in made:
        spend(answer)
    second = made[-1]
    # the service keeps the mapping honest: only candidates, in the parts' order; direct and driver views go on the
    # canvas, context stays on the card; the first part's direct view is the service's own pick when the rule holds
    idea_ids = {r['view_id'] for r in idea_rows}
    looks_at = {r['view_id']: r['looks_at'] for rows in candidates + [idea_rows] for r in rows}
    mapping = {m['index']: m for m in second.data['parts'] if isinstance(m.get('index'), int)}
    parts_out, chosen, dropped, seen = [], [], [], set()
    for i, part in enumerate(parts):
        m = mapping.get(i, {'views': [], 'why': 'the mapping call did not answer this part'})
        allowed = {r['view_id'] for r in candidates[i]} | idea_ids
        market = bool(MARKET_READING.search(part.get('looks_for', '') or ''))
        tiers = {'direct': [], 'driver': [], 'context': []}
        directs = [v.get('view_id') for v in m.get('views') or [] if v.get('fit') == 'direct' and v.get('view_id') in allowed]
        ordered = sorted(dict.fromkeys(directs), key=lambda v: (ranks[i].get(v, len(ranks[i])), directs.index(v)))
        decided = service_direct(part, ordered, looks_at) if i == 0 and not market else None
        if decided:
            tiers['direct'].append(decided)
        for v in m.get('views') or []:
            view_id, fit = v.get('view_id'), v.get('fit', 'context')
            if market:
                dropped.append({'view_id': view_id, 'why': f'part {i} is a market reading ({part["looks_for"][:50]}); the library holds no view on prices'})
            elif view_id not in allowed:
                dropped.append({'view_id': view_id, 'why': f'not among the candidates of part {i} ({part["looks_for"][:60]})'})
            elif all(view_id not in tiers[k] for k in tiers):
                if fit == 'driver' and len(tiers['driver']) >= DRIVERS_PER_PART and not (
                        cfg.idea_summary and cfg.idea_summary.prompt_version in ('idea-summary-v6', 'idea-summary-v7')):
                    tiers['context'].append(view_id)          # beyond the cap a driver is kept on the card, not the canvas
                else:
                    tiers[fit].append(view_id)
        mapped = tiers['direct'] + tiers['driver']
        parts_out.append({'index': i, 'object': part['object'], 'looks_for': part['looks_for'], 'period': part['period'], 'query': trace[i]['query'],
                          'candidates': [r['view_id'] for r in candidates[i]], 'view_ids': mapped, 'direct': tiers['direct'], 'driver': tiers['driver'],
                          'context': tiers['context'], 'service_direct': decided, 'market_reading': market,
                          'clauses': {v['view_id']: v['clause'] for v in m.get('views') or [] if v.get('clause')},     # idea-v10: how each driver moves the part
                          'why': 'a market reading: the library holds no view on prices' if market else m.get('why', '')})
        for view_id in mapped:
            if view_id not in seen:
                seen.add(view_id)
                chosen.append({'view_id': view_id, 'why': m.get('why', ''), 'part': part['looks_for'], 'fit': 'direct' if view_id in tiers['direct'] else 'driver'})
    # the claim: the idea must state an amount; the claimed part must map to a view; the service evaluates
    claim, evaluation = first.data['claim'], None
    if claim is not None:
        if not MONEY_IN_IDEA.search(text):
            dropped.append({'view_id': None, 'why': 'the claim states an amount the idea does not'})
            claim = None
        elif not (0 <= claim['part'] < len(parts_out)):
            dropped.append({'view_id': None, 'why': 'the claim names a part that does not exist'})
        elif parts_out[claim['part']]['market_reading']:
            dropped.append({'view_id': None, 'why': 'the claim is about a market price; the library holds no view on prices'})
        elif not parts_out[claim['part']]['direct']:
            dropped.append({'view_id': None, 'why': 'the claimed part has no direct view; a driver is not the quantity the idea names'})
        else:
            claim = dict(claim, view_id=parts_out[claim['part']]['direct'][0])
            evaluation = service.evaluate(ledger, claim['view_id'], claim['comparator'], float(claim['value_usd']), as_of)
    related = related_views(ledger, parts_out[0]['view_ids'] if parts_out else [], as_of, exclude=[c['view_id'] for c in chosen])
    summary = second.data['summary']
    composite = None
    if cfg.idea_summary is not None:
        report('summarize')
        summary_setting = cfg.idea_summary
        with open(config.prompt_path(summary_setting.prompt_version + '.txt'), encoding='utf-8') as handle:
            summary_prompt = handle.read().strip()
        records = {r['view_id']: r for r in service.summaries(ledger, as_of)}
        context = {'idea': text, 'as_of': as_of, 'evaluation': evaluation,
                   'parts': [{key: part[key] for key in ('object', 'looks_for', 'period', 'direct', 'driver', 'context', 'why')} for part in parts_out],
                   'theses': brief(ledger, [records[c['view_id']] for c in chosen], as_of, detailed=True)}
        composite_contract = idea_composite.contract(summary_setting.prompt_version, chosen, ledger)
        if composite_contract:
            context['theses'] = idea_composite.add_ladders(ledger, context['theses'], endpoints_only=summary_setting.prompt_version in ('idea-summary-v5', 'idea-summary-v6', 'idea-summary-v7'))
            for part in context['parts']:
                del part['why']
            if summary_setting.prompt_version == 'idea-summary-v7':
                context['candidate_theses'] = context.pop('theses')
        schema, prose, bind_composite = composite_contract or (SUMMARY, lambda d: [d['summary']], None)
        made, more = call_english(archive, cfg, summary_setting, summary_prompt, json.dumps(context, ensure_ascii=False),
                                  schema, 'idea_summary', transport, prose)
        slips += more
        for answer in made:
            spend(answer)
        summary = made[-1].data['summary']
        if bind_composite:
            composite = bind_composite(made[-1].data, chosen, records, as_of)
            if composite['version'] == 'idea-composite/4':
                mapped = {entry['view_id']: entry for entry in chosen}
                chosen = [mapped[entry['thesis_id']] for entry in composite['drivers']]
                adopted = {entry['view_id'] for entry in chosen}
                for part in parts_out:
                    for key in ('view_ids', 'direct', 'driver', 'context'):
                        part[key] = [ident for ident in part[key] if ident in adopted]
                    if part['service_direct'] not in adopted:
                        part['service_direct'] = None
                    part['clauses'] = {ident: clause for ident, clause in part['clauses'].items() if ident in adopted}
                if claim and claim['view_id'] not in adopted:
                    claim, evaluation = None, None
                related = []
    card['reading'] = {'summary': summary, 'parts': parts_out, 'chosen': chosen, 'claim': claim, 'dropped': dropped, 'trace': trace, 'language_slips': slips}
    if composite is not None:
        card['reading']['composite'] = composite
    card['evaluation'] = evaluation
    card['related'] = related
    if bundles:        # a page that fetches /thesis-bundles itself asks for the card alone: 20 KB instead of 2.7 MB
        item_of = bundle.item_lookup(items)
        card['views'] = [bundle.view_bundle(ledger, item_of, view_id, as_of) for view_id in [c['view_id'] for c in chosen] + [r['view_id'] for r in related]]
    cost['seconds'] = round(time.time() - started, 1)
    card['cost'] = cost
    return card
