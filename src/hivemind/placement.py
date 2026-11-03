"""What the extraction reads about each open question (D256, D274): one line per question with its 'takes' line, written by code from
the question's key and its research group, and the filing rule the schema states beside the evidence field `links`. A statement the
extraction links to no open question and to no kept candidate is dropped as 'no home' (D209); a link to one of the answer's own
candidates (c1 …) is matched by CANDIDATE_ID."""
import re

CANDIDATE_ID = re.compile(r'^c\d+$')


def matter(view):
    """The research group(s) the thesis belongs to: the matter's other names in the press and what is happening (D149 aliases)."""
    parts = []
    for g in view.get('groups') or []:
        names = [a for a in (g.get('aliases') or []) if a and a != g.get('name')]
        parts.append(f"the matter '{g['name']}'" + (f" (also called {', '.join(names)})" if names else '') + f": {g['scope']}")
    return '; '.join(parts)


def takes(view):
    """What a question collects, from its key and its research group: the one sentence the extraction reads beside the question.
    A file holds the question's own figures or steps and the evidence that bears on its answer (D259; the standard's 5.1 test: what
    makes the answer more or less likely, through demand, supply, competition or pricing, D250 item 2's four paths); the
    links field's rule says how to apply it (FILING_RULE_ROOT_FALLBACK). A numeric line names only its quantity, scope and period: the
    four paths and the other-period allowance are stated once, in that rule, not repeated under every numeric question (D274)."""
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
    return f"takes: {measure_name}figures, guidance, estimates and revisions for {scope}, this question's period {key.get('period_start')}..{key.get('period_end')}{tail}"


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


def question_lines(shown):
    """One line per open question with its takes line below it: what the extraction reads under [Open questions]."""
    return [f"  - {v['view_id']} ({v['object_id']}, due {v['due_day']}): {v['question']}\n      {takes(v)}" for v in shown]
