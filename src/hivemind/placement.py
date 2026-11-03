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
        parts.append(f"the matter '{g['name']}'" + (f" (also called {', '.join(names)})" if names else '') + f": {g['scope']}")
    return '; '.join(parts)


def takes(view, paths_once=False):
    """What a question collects, from its key and its research group: the one sentence the placer reads beside the question.
    A file holds the question's own figures or steps and the evidence that bears on its answer (D259; the standard's 5.1 test: what
    makes the answer more or less likely, through demand, supply, competition or pricing, D250 item 2's four paths); the
    system prompt says how to apply it (whoever says it, with or without a size, the narrowest covering question only). With paths_once
    (extraction v74i, D274) a numeric line names only its quantity, scope and period: the four paths and the other-period allowance
    are stated once, in FILING_RULE_ROOT_FALLBACK, not repeated under every numeric question."""
    key = view.get('key') or {}
    measure, scope = key.get('measure') or '', key.get('scope') or view.get('looks_at') or view.get('object_id')
    tail = f"; statements about {matter(view)} belong here under any of those names" if matter(view) else ''
    if measure == 'policy_event':
        return (f"takes: the decisions, drafts, approvals, denials and deadlines of this process, its enforcement and evasion, any statement of "
                f"whether and how much the permitted or restricted activity is actually happening, and the affected parties' own plans and "
                f"statements about it: {scope}{tail}")
    if measure == 'event':
        if key.get('event_type') in ('launch', 'shipment', 'deployment'):
            return (f"takes: steps, dates, delays, cancellations, design or configuration changes, variants and stopgaps of this event, "
                    f"confirmations and denials, and named customers' statements about receiving it: {scope}{tail}")
        return (f"takes: the terms, amounts, counterparties, agreements and approvals of this obligation or deal, its steps, confirmations and "
                f"denials, and the counterparties' own plans, financing and demand that bear on it: {scope}{tail}")
    measure_name = f"{measure} " if measure and measure != 'other' else ''   # 'other' is the key's catch-all, not a word for the reader
    # D268 (2026-11-02, the first prompt audit, design-v72.md §12 row D): the period is named as the question's own, not as a bound on what
    # the file takes; an estimate for another period or population of the same quantity is filed here when no open question covers it
    # (D248 allows calendar-year estimates under fiscal-year questions; D240: a missing period is no reason to drop)
    if paths_once:
        return f"takes: {measure_name}figures, guidance, estimates and revisions for {scope}, this question's period {key.get('period_start')}..{key.get('period_end')}{tail}"
    return (f"takes: {measure_name}figures, guidance, estimates and revisions for {scope} (this question's period is {key.get('period_start')}..{key.get('period_end')}; "
            f"an estimate for another period or population of the same quantity is filed here when no open question covers it), "
            f"and what makes that figure more or less likely: the demand, supply, competition and pricing behind it{tail}")


# Extraction v72 (D256; Alex, 2026-11-02: the open questions and their takes lines decide the extraction): the one decider is the
# extraction, which reads the day's open questions with the same takes lines the placer read and files each statement through its
# links. The rule the placer's system prompt (placement-narrow-v4) states for the separate call is written here as the schema
# description of the evidence field `links`, so the field has its definition beside it (AGENTS §6: a field without a definition is a
# coin flip per send; D256). This constant is the rule's owner for the extraction; v4's file stays the separate call's wording.
FILING_RULE = ('The questions this statement is filed under: the id of the narrowest open question in [Open questions] whose takes line covers it '
               '(that one only, never a broader question beside it; whoever says it, and even when it gives no period, basis or exact amount, '
               'because the weight is judged later, not here; a period in a takes line tells apart questions about the same quantity for different '
               'periods and bars no figure or driver from another period when no open question covers that period), plus the ids of this answer\'s '
               'candidates the statement supports; empty when no takes line and no candidate covers it, however important it sounds.')

# Extraction v74i, the frozen production prompt (D274; design-v78-fields.md §13, the second Codex review): the takes lines' shared tail and period
# allowance are stated once here, beside the field, with the company-wide revenue question as the home of indirect evidence no specific question takes.
FILING_RULE_ROOT_FALLBACK = ('The questions this statement is filed under, decided after you have decided it is evidence: the id of the narrowest open question in '
                             '[Open questions] whose answer this statement makes more or less likely, as that question\'s own figure, step or estimate or through '
                             'the demand, supply, competition or pricing behind its answer; compare the specific questions before a company-wide revenue or margin '
                             'question and take that one only, never a broader question beside it; a shared company, industry, event or ecosystem is not a '
                             'connection, and the statement need not repeat the question\'s words (a variant, sibling or other name of the subject counts); whoever '
                             'says it, and even when it gives no period, basis or exact amount, because the weight is judged later; an estimate for another period '
                             'or population of a question\'s quantity is filed under it when no open question covers that period; when no specific question is '
                             'connected, a statement that moves the demand, supply, competition or pricing behind the company\'s results goes to the company-wide '
                             'revenue question of its period; plus the ids of this answer\'s candidates the statement supports; empty when no question and no '
                             'candidate is connected, however important it sounds.')


def question_lines(shown, paths_once=False):
    """One line per open question with its takes line below it: what the placer reads, and from extraction v72 what the extraction
    reads under [Open questions]. One writer for both requests."""
    return [f"  - {v['view_id']} ({v['object_id']}, due {v['due_day']}): {v['question']}\n      {takes(v, paths_once)}" for v in shown]


def build_request(statements, shown, item=None):
    head = f"[Item] {item.get('publisher') or ''}, {item.get('publication_day') or ''}: {item.get('title') or ''}\n\n" if item else ''
    lines = question_lines(shown)
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
