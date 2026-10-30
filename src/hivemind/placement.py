"""Placement (D207, 2026-10-28; docs/research/2026-10-28-extraction-quality/routing-analysis.md): from extraction v20 the statements an
item yields are filed by a separate call that reads only the item's title line, the statements and the open questions, each question
with a 'takes' line written by code from its key and its research group. The rule is the placement prompt the configuration names:
`placement-narrow-v1` (one home, the narrowest question that names the matter; a company-wide figure question takes only its own
figures and guidance) or `placement-v1` (the old link rule, kept for comparison). A statement the placer files nowhere is dropped with the reason 'no home'
(D209: evidence is what bears on an open question; the handover's dropped record is where evaluation reads what was thrown away);
a link the extraction gave to one of its own candidates (c1 …) is kept as it is, the placer decides only the links to existing theses. Measured on the frozen gold over three draws: core statements filed right
55% → 82%, wrong links 9 → 3, links to the two revenue sinks 63/60/44 → 6/1/5."""
import re

from . import config, model

SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['placements'],
          'properties': {'placements': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False, 'required': ['id', 'links'],
                                                                     'properties': {'id': {'type': 'string'}, 'links': {'type': 'array', 'items': {'type': 'string'}}}}}}}
CANDIDATE_ID = re.compile(r'^c\d+$')


def matter(view):
    """The research group(s) the thesis belongs to: the matter's other names in the press and what is happening (D149 aliases)."""
    parts = []
    for g in view.get('groups') or []:
        names = [a for a in (g.get('aliases') or []) if a and a != g.get('name')]
        parts.append(f"the matter '{g['name']}'" + (f" (also called {', '.join(names[:6])})" if names else '') + f": {g['scope']}")
    return '; '.join(parts)


def takes(view):
    """What a question collects, from its key and its research group: the one sentence the placer reads beside the question."""
    key = view.get('key') or {}
    measure, scope = key.get('measure') or '', key.get('scope') or view.get('looks_at') or view.get('object_id')
    tail = f"; statements about {matter(view)} belong here under any of those names" if matter(view) else ''
    if measure == 'policy_event':
        return (f"takes: the decisions, drafts, approvals, denials and deadlines of this process, and any statement of whether and how much "
                f"the permitted or restricted activity is actually happening: {scope}{tail}")
    if measure == 'event':
        if key.get('event_type') in ('launch', 'shipment', 'deployment'):
            return f"takes: steps, dates, delays, confirmations and denials of this event, and named customers' statements about receiving it: {scope}{tail}"
        return f"takes: the terms, amounts, counterparties, agreements and approvals of this obligation or deal, and its steps, confirmations and denials: {scope}{tail}"
    population = ", including estimates for another population or wording of the same aggregate" if view.get('kind') == 'theme' else ''
    return (f"takes: {measure or 'the figure'} figures, guidance, estimates and revisions for {scope} over {key.get('period_start')}..{key.get('period_end')}{population}, "
            f"and the direct drivers of that figure stated with a size{tail}")


def build_request(statements, shown, item=None):
    head = f"[Item] {item.get('publisher') or ''}, {item.get('publication_day') or ''}: {item.get('title') or ''}\n\n" if item else ''
    lines = [f"  - {v['view_id']} ({v['object_id']}, due {v['due_day']}): {v['question']}\n      {takes(v)}" for v in shown]
    return (head + '[Open questions]\n' + '\n'.join(lines) + '\n\n[Statements]\n'
            + '\n'.join(f"  - {e['id']} [{e.get('tier')}] who: {e.get('original_who') or e.get('speaker') or ''} | {e.get('one_line')} | quote: {(e.get('quote') or '')[:240]}" for e in statements)
            + '\n\nReturn one placement per statement id, in order.')


def place(archive, cfg, statements, shown, *, item=None, transport=None, prompt=None):
    """Returns (placed, unfiled, answer): every statement with its links decided; the extraction's candidate links kept; the
    caller drops the unfiled.
    prompt names the placement prompt file; the configuration's is the default."""
    if not statements:
        return [], [], None
    with open(config.prompt_path((prompt or cfg.placement.prompt_version) + '.txt'), encoding='utf-8') as handle:
        system = handle.read()
    user = build_request(statements, shown, item=item)
    answer = model.call(archive, cfg, cfg.placement, system, user, SCHEMA, 'placement', 'place', transport=transport)
    allowed = {v['view_id'] for v in shown}
    decided = {}
    for p in answer.data['placements']:
        decided.setdefault(p['id'], [l for l in p['links'] if l in allowed])
    placed, unfiled = [], []
    for e in statements:
        links = list(dict.fromkeys([l for l in e.get('links', []) if CANDIDATE_ID.match(l)] + decided.get(e['id'], [])))
        (placed if links else unfiled).append(dict(e, links=links))
    return placed, unfiled, answer
