"""The period split (docs/research/2026-11-14-use-acceptance/splitting/DESIGN.md v4; D616): a scratch version beside the frozen
answer-choice step (D426), which it imports and does not change.

A topic that asks one quantity for each of two years, this year and next (D38: one view a year), may be declined with the typed case
`one_quantity_two_periods` naming the two years. Code checks the years (identity only: two different years, exactly this year and
next, written alike) and re-asks the step once per year with one line restricting it to that year. A yearly re-ask must write a figure
ladder for its year or decline with another case. Whether the two years are asked independently, rather than one being a base or
comparison, is the model's judgement; code cannot tell, and the probe's controls measure it. Whether a part the model leaves out is
the other year's quantity is meaning too: the yearly line tells the model the other year is asked on its own, and code adds only what
it knows, that the other year has no question (`ladder_adapter.open_split`).

The refusal field becomes a closed set: the frozen description's decline cases, transcribed as they stand, plus the new case; the
system text's list of decline cases gains the same case, with one example on each side of its boundary (`split_system`).
"""
import copy
import re

import ladder_step

SPLIT_CASE = 'one_quantity_two_periods'
CASES = {
    'no_main': 'the topic has no main figure or event (none, or several with none the main one)',
    'not_checkable_on_a_date': 'nothing in it can be checked on a date (for an event: no date given and no period named, unless it is a '
                               "pending regulatory decision, which is due at the company's current fiscal year-end)",
    'quarter_or_half_year': "a company's figure for a quarter or a half-year",
    'not_one_year_period': "a figure for a period that is not one fiscal or calendar year, such as a survey's rolling twelve months, "
                           'with no publication day in the topic or the item',
    'year_ended': "a figure for a year that has already ended on the item's day",
    'beyond_next_year': "a figure for a year beyond next year (unless the topic's opens_as is binding_obligation)",
    'another_company_or_uncovered_matter': 'the question belongs to another company or to a matter no listed theme covers (name it)',
    SPLIT_CASE: 'the topic asks the value of one quantity for each of two years, this year and next, and neither year is named only as '
                "a base or a comparison (a comparison between the two does not make either a base when the value of each is asked; this "
                "case, not no_main): name the two years in periods, written as a figure's year is written "
                '(2026, or FY2027); each year is then asked as its own question',
}
RESTRICTION = ('Write the question for {year} only: this topic is split by year, and where the instructions above differ, this line '
               'prevails. The value for {other} is asked as its own question, so the two-year decline case does not apply here and that '
               'value alone is not listed in not_judged. List every other part as before; where a part joins the {other} value with '
               'another limit, a condition or a comparison, list that limit, condition or comparison.')
SYSTEM_REPLACEMENTS = [   # the frozen system text's decline list, extended by the eighth case (PROMPT-AUDIT.md row 2)
    ('Return no_ladder with the reason, and ladder null, in seven cases:', 'Return no_ladder with the reason, and ladder null, in eight cases:'),
    ("covers, in which case name that company or matter in the reason. Do not rewrite",
     "covers, in which case name that company or matter in the reason; or the topic asks the value of one quantity for each of two "
     "years, this year and next, and neither year is named only as a base or a comparison (a comparison between the two does not make "
     "either a base when the value of each is asked), which is this case rather than the first, "
     "since each year has its main figure, and rather than judging only one of the two years as the one the outcome names: name the "
     "two years in periods, "
     "and each year is then asked as its own question. A "
     "retailer's store openings in 2026 and in 2027 are this case; its 2027 revenue measured against 2026's is not, and is judged on "
     "2027. Do not rewrite"),
]
FAILED_TWICE = "the answers failed the step's checks twice"
CALENDAR = re.compile(r'\d{4}')
FISCAL = re.compile(r'FY(\d{4})')


def split_system(frozen_system):
    """The frozen system text with exactly the replacements above, each found once."""
    text = frozen_system
    for before, after in SYSTEM_REPLACEMENTS:
        if text.count(before) != 1:
            raise ValueError(f'the frozen system text holds {text.count(before)} copies of {before[:40]!r}, not one')
        text = text.replace(before, after)
    return text


def split_schema(frozen_schema):
    """The frozen schema with only `no_ladder` changed: a case of the closed set, its reason, and the periods (two years for the split
    case, null otherwise), or null."""
    schema = copy.deepcopy(frozen_schema)
    listed = '; '.join(f'{name}: {meaning}' for name, meaning in CASES.items())
    schema['properties']['no_ladder'] = {
        'anyOf': [{'type': 'null'}, {
            'type': 'object', 'additionalProperties': False, 'required': ['case', 'reason', 'periods'],
            'properties': {
                'case': {'type': 'string', 'enum': list(CASES)},
                'reason': {'type': 'string', 'pattern': r'\S', 'description': 'Why this case applies, naming the words that decide it.'},
                'periods': {'anyOf': [{'type': 'null'}, {'type': 'array', 'items': {'type': 'string'}}],     # two: checked by code
                            'description': f'The two years, for {SPLIT_CASE} only; null for every other case.'}}}],
        'description': f'Why no judged question is written, as one case of this closed set, or null: {listed}. Exactly one of no_ladder '
                       'and ladder is null (checked by code).'}
    return schema


def period_reasons(periods, article_day, company, research_list):
    """Identity only: two different years, written alike, exactly this year and next as of the item's day (D38)."""
    if not isinstance(periods, list) or len(periods) != 2 or len(set(periods)) != 2 or not all(isinstance(p, str) for p in periods):
        return ['periods names two different years']
    if all(CALENDAR.fullmatch(p) for p in periods):
        this = int(article_day[:4])
        expected = {str(this), str(this + 1)}
    elif all(FISCAL.fullmatch(p) for p in periods):
        this = research_list.fiscal_year_of(company, article_day)
        expected = {f'FY{this}', f'FY{this + 1}'}
    else:
        return ['both periods are written the same way: two calendar years (2026) or two fiscal years (FY2027)']
    if set(periods) != expected:
        return [f'the two periods are this year and next year as of the item\'s day ({" and ".join(sorted(expected))}); '
                f'{SPLIT_CASE} does not apply to an ended year or a year beyond next year']
    return []


def checker(frozen_check, *, article_day, company, research_list, year=None):
    """The check for the topic (`year` None) or for one year's re-ask: the typed refusal's shape first, then the frozen checks."""
    def check(answer):
        reasons = []
        no_ladder = answer.get('no_ladder')
        if no_ladder is not None:
            if not isinstance(no_ladder, dict) or no_ladder.get('case') not in CASES or not str(no_ladder.get('reason') or '').strip():
                reasons.append('no_ladder names one case of the closed set and gives its reason')
            elif no_ladder['case'] == SPLIT_CASE:
                if year is not None:
                    reasons.append(f'this question is for {year} only: write its ladder for {year}, or decline with another case')
                else:
                    reasons += period_reasons(no_ladder.get('periods'), article_day, company, research_list)
            elif no_ladder.get('periods') is not None:
                reasons.append(f'periods is null unless the case is {SPLIT_CASE}')
        elif year is not None:
            figure = (answer.get('ladder') or {}).get('figure')
            if figure is None or str(figure.get('year')) != year:
                reasons.append(f'this question is for {year} only: write a figure ladder whose year is {year}')
        frozen_reasons, passage = frozen_check(answer)
        return reasons + frozen_reasons, passage
    return check


def shown_reason(outcome):
    """What a reader is shown for a year with no question: the model's own reason when it declined, code's words when its answers
    failed the checks twice; never one presented as the other."""
    if outcome['status'] == 'no ladder':
        return outcome['reason']['reason'] if isinstance(outcome['reason'], dict) else outcome['reason']
    return FAILED_TWICE


def ladder_for_thesis_split(payload, *, system_text, closing_text, schema, call_model, check_for):
    """The topic's outcome as the frozen step gives it; when it declines with a valid split case, the two years' re-asks are added as
    `children` and the status becomes `split`. `check_for(year)` returns the check for the topic (None) or for one year."""
    outcome = ladder_step.ladder_for_thesis(payload, system_text=system_text, closing_text=closing_text, schema=schema,
                                            call_model=call_model, check=check_for(None))
    reason = outcome['reason']
    if outcome['status'] != 'no ladder' or not isinstance(reason, dict) or reason.get('case') != SPLIT_CASE:
        return outcome
    periods = list(reason['periods'])
    children = {}
    for year, other in ((periods[0], periods[1]), (periods[1], periods[0])):
        children[year] = ladder_step.ladder_for_thesis(payload, system_text=system_text,
                                                       closing_text=closing_text + '\n\n' + RESTRICTION.format(year=year, other=other),
                                                       schema=schema, call_model=call_model, check=check_for(year))
    return dict(outcome, status='split', periods=periods, children=children)
