"""The clean ladder step (clean-arch/step4-2026-11-10/DESIGN.md §5; D397 to D407).

For one thesis Step 1 opened, one model call writes the judged question, its answer ladder and its due day, or declines. Code
checks the answer (checks 1 to 6), writes the rungs' labels and conditions (check 7), and sends a refused answer back once with
the reasons (check 8). The request is the one first sent in the probe of 2026-11-10 (D407): the model keeps the judgement of
whether a topic has a main thing; code owns what can be seen in the text (a reference that is not the article's words, a theme's
state named with a company label, a question that says "this item").

Nothing here reads the wall clock, the environment or a path it was not given.
"""
import datetime
import json
import math
import re
from decimal import Decimal, InvalidOperation

COMPANY_LABELS = ['Strongly bullish', 'Bullish', 'Neutral', 'Bearish', 'Strongly bearish']   # position 1 to 5, as production stores them
NOT_A_FINITE_NUMBER = 'not a finite number'       # what NaN, Infinity or a token the decimal type cannot hold is read as
# D407: what the judge is shown must stand without the item. The three wordings seen or one step from them: "this item",
# "cited in the item", "the item's forecast"; an article of law ("the Article 232 tariffs") is not one of them.
REFERS_TO_THE_ITEM = re.compile(r"\bthis (item|article)\b|\bin the (item|article)\b|\bthe (item|article)['’]s\b", re.IGNORECASE)
COMPANY_YEAR = re.compile(r'FY\d{4}')
CALENDAR_YEAR = re.compile(r'\d{4}')
ISO_DAY = re.compile(r'\d{4}-\d{2}-\d{2}')
FIGURE_BASES = ('stated', 'expected_publication')
EVENT_BASES = ('stated', 'period_end')
RESEND_NOTE = ('\n\nYour previous answer was:\n{answer}\n\nIt was refused for the reasons below. Correct those problems and return the complete '
               'answer again.\n{reasons}')
RESEND_NOTE_UNREADABLE = ('\n\nYour previous answer could not be used: {reasons} Return the complete answer again, as JSON that fits the '
                          'schema.')


class CachedAnswer(Exception):
    """The model archive answered a ladder request from its cache: there is no text of the answer to read numbers from."""


# ---- reading the answer's own text -------------------------------------------------------------------------------------------

def read_number_token(token_text):
    """The exact decimal a JSON number token writes, whatever its spelling; NOT_A_FINITE_NUMBER when the decimal type cannot hold it."""
    try:
        return Decimal(token_text)
    except InvalidOperation:
        return NOT_A_FINITE_NUMBER


def parse_exactly(answer_text):
    """Parse the model's own text so that every number is the exact decimal it wrote. No number token makes this raise."""
    return json.loads(answer_text, parse_float=read_number_token, parse_int=read_number_token,
                      parse_constant=lambda name: NOT_A_FINITE_NUMBER)


def is_finite_number(number):
    """A bound or a reference's value: any finite number whose nearest float is finite too."""
    return isinstance(number, Decimal) and number.is_finite() and math.isfinite(float(number))


def written_number(number):
    """The text a rung shows for a number: plain notation, no exponent, no trailing zeros, thousands separators on a whole number
    of 1,000 or more in size."""
    if number == 0:
        return '0'
    plain = format(number, 'f')
    if '.' in plain:
        plain = plain.rstrip('0').rstrip('.')
    if '.' in plain:
        return plain
    digits = plain.lstrip('-')
    grouped = f'{int(digits):,}' if len(digits) > 3 else digits
    return ('-' if plain.startswith('-') else '') + grouped


def interval_text(lo, hi, unit):
    """One range in words: inclusive lower bound, exclusive upper bound; the unit is left out when it is "other"."""
    suffix = '' if unit == 'other' else f' {unit}'
    if lo is None:
        return f'below {written_number(hi)}{suffix}'
    if hi is None:
        return f'{written_number(lo)}{suffix} or more'
    return f'from {written_number(lo)}{suffix} to below {written_number(hi)}{suffix}'


# ---- the reference's words --------------------------------------------------------------------------------------------------

FOOTNOTE_MARKER_BEFORE_PUNCTUATION = re.compile(r"\s*\[\d{1,3}\]\s*(?=[.,;:!?)\"'”’])")
FOOTNOTE_MARKER = re.compile(r"\s*\[\d{1,3}\]\s*")


def without_footnote_markers(text):
    """The text with its footnote markers ([5]) taken out: a marker that stands before punctuation leaves nothing, any other
    leaves one space."""
    return FOOTNOTE_MARKER.sub(' ', FOOTNOTE_MARKER_BEFORE_PUNCTUATION.sub('', text))


def article_passage(words, article_text, repair_quote, normalise, quote_tokens):
    """The article's own passage for a reference's words, or None (check 6, D405: "an unbroken passage of the article's own
    words"). The words are accepted when they occur in the article exactly. Otherwise production's repair must find a passage
    that holds exactly the quote's words in the quote's order (nothing left out, added or moved), and the quote must occur
    whole in the article once the article's footnote markers are taken out and spacing, letter case and the forms of quote
    marks and dashes are set aside (production's `normalise`). A changed, added or dropped punctuation mark or sign is
    therefore a refusal. Production's repair looks at no quote of fewer than eight characters, so one that short is accepted
    only when exact."""
    if words in article_text:
        return words
    passage = repair_quote(words, article_text)
    quote = normalise(words)
    if (passage and passage in article_text and quote and words_of(passage, quote_tokens) == words_of(words, quote_tokens)
            and quote in normalise(without_footnote_markers(article_text))):
        return passage
    return None


def words_of(text, quote_tokens):
    """The words of a text in order, as production's quote tokeniser reads them."""
    return [token for token, _, _ in quote_tokens(text)]


# ---- checks 1 to 6 ----------------------------------------------------------------------------------------------------------

def ruling_out_of(event):
    """The sentence an event's ruling out is written as, or None when the answer names none. The answer carries it as one
    sentence, or (D416's candidate) as who decides and what they decide: `by_whom` forces the answer to name a decider, and
    `decision` is the sentence the judge is shown."""
    ruled_out = event['ruled_out']
    if isinstance(ruled_out, dict):
        return ruled_out['decision']
    return ruled_out


def texts_the_judge_is_shown(ladder):
    """The question and every condition the model wrote, as far as the shape can be read."""
    texts = [ladder['question']]
    if ladder.get('event') is not None:
        texts.extend(condition for condition in (ladder['event']['happened'], ruling_out_of(ladder['event'])) if condition is not None)
    return texts


def sorted_ranges(ranges):
    """The five ranges ordered by lower bound, the open-below range first."""
    return sorted(ranges, key=lambda bounds: (bounds['lo'] is not None, bounds['lo'] if bounds['lo'] is not None else Decimal(0)))


def check_answer(answer, *, thesis, article, company, research_list, repair_quote, normalise, quote_tokens, beyond_next_year,
                 binding_horizon_days):
    """The reasons an answer is refused, an empty list when none; and, for an accepted ladder, the article's passage for its
    reference (or None). `answer` is the exact parse of the model's text. A `no_ladder` answer is accepted when its shape is right:
    whether declining was justified is a reader's judgement, not code's."""
    reasons = []
    no_ladder, ladder = answer.get('no_ladder'), answer.get('ladder')
    if (no_ladder is None) == (ladder is None):                                                   # check 1
        return ['exactly one of no_ladder and ladder must be null'], None
    if ladder is None:
        return [], None
    shapes = [name for name in ('event', 'figure') if ladder.get(name) is not None]
    if len(shapes) != 1:
        return [f'exactly one of event and figure must be filled; {len(shapes)} are'], None
    shape = shapes[0]
    if shape == 'event' and isinstance(ladder['event']['ruled_out'], dict):                       # D416's candidate: a typed ruling out
        typed = ladder['event']['ruled_out']
        if not typed['by_whom'].strip() or not typed['decision'].strip():
            reasons.append('ruled_out names who decides and what they decide: neither by_whom nor decision may be empty')
    if any(REFERS_TO_THE_ITEM.search(text) for text in texts_the_judge_is_shown(ladder)):
        reasons.append('The question or a condition refers to the item or the article ("this item", "in the item"). Replace that reference with '
                       'the specific information needed to understand it without the item.')

    object_id = research_list.resolve(ladder['object'])                                           # check 2
    object_kind = research_list.kind(object_id) if object_id else None
    if not (object_kind == 'theme' or (object_kind == 'company' and object_id == company)):
        reasons.append(f'The object {ladder["object"]!r} is not the company {company} or a listed theme. Choose the correct listed object if one '
                       'applies; otherwise return no_ladder and name the other company or uncovered matter.')
        return reasons, None

    ordered = None                    # the five ranges in ascending order, set only when they are a sound partition
    if shape == 'figure':                                                                         # checks 1 and 4
        figure = ladder['figure']
        ranges = figure['ranges']
        bounds = [bound for one_range in ranges for bound in (one_range['lo'], one_range['hi']) if bound is not None]
        if len(ranges) != 5:
            reasons.append(f'a figure has exactly five ranges; this one has {len(ranges)}')
        elif not all(is_finite_number(bound) for bound in bounds):
            reasons.append('every bound that is not null is a finite number')
        else:
            ascending = sorted_ranges(ranges)
            partition_reasons = []
            if sum(1 for one_range in ranges if one_range['lo'] is None) != 1 or ascending[0]['lo'] is not None:
                partition_reasons.append('exactly one range, the lowest, has lo null')
            if sum(1 for one_range in ranges if one_range['hi'] is None) != 1 or ascending[-1]['hi'] is not None:
                partition_reasons.append('exactly one range, the highest, has hi null')
            if not partition_reasons:
                for lower, upper in zip(ascending, ascending[1:]):
                    if lower['hi'] != upper['lo']:
                        partition_reasons.append(f'the ranges must meet end to end: one ends at {written_number(lower["hi"])} and the next starts at {written_number(upper["lo"])}')
                for one_range in ascending:
                    if one_range['lo'] is not None and one_range['hi'] is not None and not one_range['lo'] < one_range['hi']:
                        partition_reasons.append(f'a range from {written_number(one_range["lo"])} to below {written_number(one_range["hi"])} holds no value')
            if partition_reasons:
                reasons.extend(partition_reasons)
            else:
                ordered = ascending
        favourable_end, favourable_why = figure['favourable_end'], figure['favourable_why']
        if object_kind == 'company':
            if favourable_end not in ('higher', 'lower') or not favourable_why.strip():
                reasons.append("a company's figure names its favourable end, higher or lower, with one sentence why")
            if not COMPANY_YEAR.fullmatch(figure['year']):
                reasons.append(f"a company's figure carries its fiscal year as FY and four digits; got {figure['year']!r}")
        else:
            if favourable_end != 'n/a' or favourable_why.strip():
                reasons.append("a theme's figure has favourable_end n/a and an empty favourable_why")
            if not CALENDAR_YEAR.fullmatch(figure['year']):
                reasons.append(f"a theme's figure carries a calendar year as four digits; got {figure['year']!r}")

    article_day = datetime.date.fromisoformat(article['publication_date'])                        # check 5
    written_day = None
    if ISO_DAY.fullmatch(ladder['due_day']):
        try:
            written_day = datetime.date.fromisoformat(ladder['due_day'])
        except ValueError:
            written_day = None
    due_day = written_day
    if written_day is None:
        reasons.append(f'due_day is not a real date: {ladder["due_day"]!r}')
    elif shape == 'figure' and ladder['due_day_basis'] == 'expected_publication':                 # D414: code sets the day of a year's figure
        year_end = year_end_of(ladder['figure']['year'], object_kind, object_id, research_list)
        if year_end is not None:
            if written_day < year_end:                   # the figure the model has in mind is not that year's figure
                reasons.append(f"the figure is given the year {ladder['figure']['year']}, which ends on {year_end}, and you expect it published on "
                               f'{written_day}, before that: a figure is published after the period it covers ends, so this is not a figure for that '
                               f'year. A company\'s figure for a quarter or a half-year is returned as no_ladder. A figure for another period takes '
                               f'the publication day the topic or the item gives, with due_day_basis stated; when neither gives one, nothing in the '
                               f'topic can be checked on a date: return no_ladder')
            due_day = datetime.date.fromisoformat(due_day_of(ladder, object_kind, object_id, research_list))
    if due_day is not None:
        if due_day <= article_day:
            reasons.append(f'the due day {due_day} is not after the item\'s day {article_day}')
        if thesis['opens_as'] == 'binding_obligation' and due_day > article_day + datetime.timedelta(days=binding_horizon_days):
            reasons.append(f'a binding obligation is due at most {binding_horizon_days} days after the item; {due_day} is later')
    if shape == 'figure':
        year = ladder['figure']['year']
        year_is_well_formed = (COMPANY_YEAR if object_kind == 'company' else CALENDAR_YEAR).fullmatch(year)
        if year_is_well_formed:
            if thesis['opens_as'] != 'binding_obligation' and beyond_next_year(year, article['publication_date'], object_id, research_list):
                reasons.append(f'the figure is for {year}, a year beyond next year: return no_ladder')
            period = research_list.fiscal_period(object_id, year, bare_is_calendar=True)
            if period and datetime.date.fromisoformat(period[1]) < article_day:
                reasons.append(f'the figure is for {year}, a year that had ended on the item\'s day: return no_ladder')
    allowed_bases = FIGURE_BASES if shape == 'figure' else EVENT_BASES
    if ladder['due_day_basis'] not in allowed_bases:
        reasons.append(f'due_day_basis {ladder["due_day_basis"]!r} does not fit {"a figure" if shape == "figure" else "an event"}: use one of {", ".join(allowed_bases)}')

    passage = None                                                                                # check 6
    reference = ladder.get('reference')
    if reference is not None:
        passage = article_passage(reference['words'], article['text'], repair_quote, normalise, quote_tokens)
        if passage is None:
            reasons.append('the reference\'s words are not in the item: copy one unbroken passage from the item exactly, not reworded, not reordered, and not taken from the topic')
        value, value_to = reference['value'], reference['value_to']
        if reference['kind'] == 'last_reported' and shape != 'figure':
            reasons.append('a reference of kind last_reported belongs to a figure: an event\'s reference is of kind expected, or null')
        if (value is not None and not is_finite_number(value)) or (value_to is not None and not is_finite_number(value_to)):
            reasons.append('the reference\'s value and value_to are finite numbers, or null')
        elif value_to is not None and (value is None or not value < value_to):
            reasons.append('value_to is the upper end of a range the item states: it is null, or greater than value')
        elif value is not None and shape == 'figure' and ordered is not None:
            middle = ordered[2]
            if value_to is None and not (middle['lo'] <= value < middle['hi']):
                reasons.append(f'the reference\'s value {written_number(value)} must lie in the middle range, from {written_number(middle["lo"])} to below {written_number(middle["hi"])}')
            if value_to is not None and not (middle['lo'] <= value and value_to <= middle['hi']):       # the middle range spans the stated range, end to end
                reasons.append(f'the middle range, from {written_number(middle["lo"])} to below {written_number(middle["hi"])}, must run from at or below the '
                               f'lower end of the reference\'s range {written_number(value)} to {written_number(value_to)} to at or above its upper end')
    return reasons, passage


# ---- check 7: the view as it will be written --------------------------------------------------------------------------------

FIGURE_DUE_LAG_DAYS = {'company': 60, 'theme': 90}      # D414: days after the end of the year a figure covers


def year_end_of(year, object_kind, object_id, research_list):
    """The last day of the year a figure covers: the company's fiscal year-end, or 31 December for a theme's figure. None when
    the year is not written as its kind asks or the company's fiscal calendar does not hold it."""
    if object_kind == 'company':
        if not COMPANY_YEAR.fullmatch(year):
            return None
        period = research_list.fiscal_period(object_id, year, bare_is_calendar=True)
        return datetime.date.fromisoformat(str(period[1])[:10]) if period else None
    return datetime.date(int(year), 12, 31) if CALENDAR_YEAR.fullmatch(year) else None


def due_day_of(ladder, object_kind, object_id, research_list):
    """The day the question is due, as an ISO string (D414). A figure whose day the model would estimate (due_day_basis
    expected_publication) is due a fixed number of days after the end of the year it covers; every other day is the answer's."""
    figure = ladder.get('figure')
    if figure is not None and ladder['due_day_basis'] == 'expected_publication':
        year_end = year_end_of(figure['year'], object_kind, object_id, research_list)
        if year_end is not None:
            return (year_end + datetime.timedelta(days=FIGURE_DUE_LAG_DAYS[object_kind])).isoformat()
    return ladder['due_day']


def event_rungs(event, due_day, article_day):
    """An event's rungs (D409): it happened; it is ruled out; neither. The model writes the first condition and, when something
    can rule the event out before the due day, the way it names for that. Code writes the rest, so that exactly one rung holds
    for every outcome whatever the two conditions say. The second rung takes the way the model names and every other decision
    against the event as a whole, or abandonment or withdrawal of it as a whole, and asks of each of them, the model's own
    included, that it was made after the article's day and stands on the due day: so a rejection the model did not name is
    never counted as still open, and one that was lifted, that concerns only a part, or that was already in place when the
    question opened, is not counted as a ruling out, whether or not the model's sentence says so. The second
    rung holds only when the first does not, and the last rung is the complement of the others. The labels answer the question
    as it is printed beside them: Yes and No, or Yes, Ruled out and Still open."""
    happened = {'label': 'Yes', 'condition': event['happened']}
    if event['ruled_out'] is None:
        return [happened, {'label': 'No', 'condition': f'Rung 1 does not hold on {due_day}.'}]
    ruled_out = ruling_out_of(event).rstrip()
    return [happened,
            {'label': 'Ruled out',
             'condition': f"{ruled_out}{'' if ruled_out.endswith('.') else '.'} This rung holds when that, or any other decision against the event of "
                          f'rung 1 as a whole, or a formal abandonment or withdrawal of it as a whole, was made after {article_day} and '
                          f'stands on {due_day}, and only when rung 1 does not.'},
            {'label': 'Still open', 'condition': f'Neither rung 1 nor rung 2 holds on {due_day}.'}]


def write_view(ladder, passage, *, thesis, article_day, company, research_list):
    """The view an accepted ladder is written as: its object, kind, focus, question, year, due day and its rungs in position
    order, each with the label and condition the judge is shown and, for a figure, its bounds as floats."""
    object_id = research_list.resolve(ladder['object'])
    object_kind = research_list.kind(object_id)
    reference = ladder.get('reference')
    reference_status = None
    if ladder.get('event') is not None:
        rungs = event_rungs(ladder['event'], ladder['due_day'], article_day)
        year = ladder['due_day'][:4]
    else:
        figure = ladder['figure']
        ascending = sorted_ranges(figure['ranges'])
        middle_text_suffix = ' (no reference figure when the question opened)'
        reference_status = 'no reference figure'
        if reference is not None and reference['value'] is not None:
            if reference['kind'] == 'last_reported':             # D411: named as that, never as what the market expects
                middle_text_suffix = f' (the amount last reported when the question opened: "{passage}")'
                reference_status = 'last reported figure'
            else:
                middle_text_suffix = f' (the reference when the question opened: "{passage}")'
                reference_status = 'reference figure'
        in_position_order = list(reversed(ascending)) if (object_kind == 'company' and figure['favourable_end'] == 'higher') else ascending
        rungs = []
        for position, bounds in enumerate(in_position_order, start=1):
            condition = interval_text(bounds['lo'], bounds['hi'], figure['unit'])
            label = COMPANY_LABELS[position - 1] if object_kind == 'company' else condition
            if bounds is ascending[2]:
                condition += middle_text_suffix
            rungs.append({'label': label, 'condition': condition,
                          'lo': None if bounds['lo'] is None else float(bounds['lo']), 'hi': None if bounds['hi'] is None else float(bounds['hi'])})
        year = figure['year']
    return {'object_id': object_id, 'object_kind': object_kind, 'kind': 'asset' if object_kind == 'company' else 'theme',
            'looks_at': thesis['outcome'], 'question': ladder['question'], 'due_day': due_day_of(ladder, object_kind, object_id, research_list),
            'year': year, 'rungs': rungs,
            'reference_status': reference_status}


# ---- check 8: one thesis, one or two requests -------------------------------------------------------------------------------

def user_text(payload, closing_text):
    """The user text of the request: the payload as one JSON object, a blank line, the closing check."""
    return json.dumps(payload, ensure_ascii=False) + '\n\n' + closing_text


def ladder_for_thesis(payload, *, system_text, closing_text, schema, call_model, check):
    """Ask for one thesis's ladder; send a refused answer back once, with the answer itself and the reasons, so that the model
    corrects what it wrote and does not start again. Returns the outcome record.

    `call_model(system_text, user_text, schema)` sends one request and returns a dict with `answer_text` (the model's own text, or
    None when the response carried none), `input_tokens`, `output_tokens`, `request_sha256`, `cached` and `error` (None, or the
    reason the answer could not be read or did not fit the schema). `check(answer)` returns (reasons, passage) as `check_answer`
    does, with the thesis and its article bound in. A cached answer raises CachedAnswer.
    """
    requests = []
    note = ''
    for _ in range(2):
        sent = call_model(system_text, user_text(payload, closing_text) + note, schema)
        if sent.get('cached'):
            raise CachedAnswer(f"thesis {payload['thesis']['id']}: the model archive answered from its cache")
        record = {'request_sha256': sent['request_sha256'], 'answer_text': sent['answer_text'], 'input_tokens': sent['input_tokens'],
                  'output_tokens': sent['output_tokens']}
        reasons, answer, passage = [], None, None
        if sent['error']:
            reasons = [sent['error']]
        else:
            try:
                answer = parse_exactly(sent['answer_text'])
            except (ValueError, RecursionError) as error:
                reasons = [f'the answer could not be read: {type(error).__name__}']
            else:
                reasons, passage = check(answer)
        if not reasons:
            if answer['ladder'] is None:
                record['result'] = 'no ladder'
                requests.append(record)
                return {'thesis_id': payload['thesis']['id'], 'status': 'no ladder', 'reason': answer['no_ladder'], 'requests': requests,
                        'answer': None, 'passage': None}
            record['result'] = 'ladder'
            requests.append(record)
            return {'thesis_id': payload['thesis']['id'], 'status': 'ladder', 'reason': None, 'requests': requests, 'answer': answer,
                    'passage': passage}
        record['result'] = 'refused'
        record['reasons'] = reasons
        requests.append(record)
        if answer is None:                               # the answer could not be read or did not fit the schema: nothing to show back
            note = RESEND_NOTE_UNREADABLE.format(reasons=' '.join(reasons))
        else:
            note = RESEND_NOTE.format(answer=sent['answer_text'], reasons='\n'.join(f'- {reason}' for reason in reasons))
    return {'thesis_id': payload['thesis']['id'], 'status': 'no ladder: refused', 'reason': None, 'requests': requests, 'answer': None,
            'passage': None}


def as_json(value):
    """An outcome record or a checked answer as JSON text: exact decimals as plain numbers in text form, every non-ASCII character
    escaped, so that any text an answer carried can be stored."""
    def encode(node):
        if isinstance(node, Decimal):
            return written_number(node).replace(',', '')
        raise TypeError(f'{type(node).__name__} is not stored')
    return json.dumps(value, ensure_ascii=True, default=encode)
