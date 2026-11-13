"""Tests of the clean ladder step. Each names the check of DESIGN.md §5.3, or the decision, that it proves.

Real objects throughout: production's research list, quote repair, date rules, model archive and spending limit. Only the model
transport is faked. Run: python3 -m pytest clean-arch/step4-2026-11-10/ladder/test_ladder_step.py
"""
import copy
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path[:0] = [str(HERE), str(ROOT / 'src'), str(ROOT / 'clean-arch' / 'e2e-2026-11-09')]
import budget  # noqa: E402
import ladder_step  # noqa: E402
import model_calls  # noqa: E402
from hivemind import config, extraction, model, universe  # noqa: E402

RESEARCH_LIST = universe.load(str(ROOT / 'poc' / 'universe.json'))
EXAMPLES = json.loads((HERE / 'examples.json').read_text())[1:]
STORED = {(entry['run'], entry['id']): entry for entry in json.loads((STEP / 'census' / 'packet.json').read_text())}
SCHEMA = json.loads((HERE / 'candidate-schema.json').read_text())


def example(draw, thesis_id):
    return next(entry for entry in EXAMPLES if entry['thesis'] == [draw, thesis_id])


def inputs_of(entry):
    """The thesis, article, company and research list a fixture runs on: a stored thesis, or the fixture's own made-up input."""
    if entry.get('fixture_input'):
        given = entry['fixture_input']
        made_up_list = universe.Universe({'version': 'fixture', 'themes': [],
                                          'companies': [{'id': given['company'], 'name': 'Retailer', 'categories': [], 'fiscal_year_end_month': 1, 'aliases': []}]})
        return given['thesis'], given['item'], given['company'], made_up_list
    stored = STORED[tuple(entry['thesis'])]
    return {'id': entry['thesis'][1], **stored['thesis']}, stored['article'], 'NVDA', RESEARCH_LIST


def exact(answer):
    """A fixture's answer as the step reads it: the exact parse of its JSON text."""
    return ladder_step.parse_exactly(json.dumps(answer))


def check(answer, entry, thesis_changes=None, article_changes=None):
    thesis, article, company, research_list = inputs_of(entry)
    thesis, article = {**thesis, **(thesis_changes or {})}, {**article, **(article_changes or {})}
    return ladder_step.check_answer(answer if isinstance(answer, dict) and not _has_floats(answer) else exact(answer), thesis=thesis,
                                    article=article, company=company, research_list=research_list, repair_quote=extraction.repair_quote,
                                    normalise=extraction.normalise, quote_tokens=extraction._quote_tokens,
                                    beyond_next_year=extraction.beyond_next_year,
                                    binding_horizon_days=extraction.BINDING_HORIZON_DAYS)


def _has_floats(node):
    if isinstance(node, float):
        return True
    if isinstance(node, dict):
        return any(_has_floats(value) for value in node.values())
    if isinstance(node, list):
        return any(_has_floats(value) for value in node)
    return False


def reasons_for(answer, entry, **changes):
    return check(answer, entry, **changes)[0]


COMPANY_FIGURE = example('u1', 'clean-7')        # a company's figure, lower favourable, no reference
THEME_FIGURE = example('u1', 'clean-4')          # a theme's figure with a reference value
EVENT_TWO = example('u1', 'clean-3')            # an event with nothing to rule it out: two rungs
OBLIGATION = example('u1', 'clean-2')            # an event on a binding obligation, due on day 548
EVENT_THREE = example('u2', 'clean-9')           # a company's event in three outcomes (D409)
THEME_EVENT = example('u3', 'clean-12')          # a theme's event in three outcomes
DECLINED = example('u2', 'clean-10')
HIGHER_FAVOURABLE = example('made-up', 'clean-99')


def changed(entry, change):
    answer = copy.deepcopy(entry['answer'])
    change(answer['ladder'] if answer['ladder'] is not None else answer)
    return answer


# ---- checks 1 to 7 on the fixtures --------------------------------------------------------------------------------------------

@pytest.mark.parametrize('entry', EXAMPLES, ids=lambda entry: '/'.join(entry['thesis']))
def test_a_fixture_passes_checks_1_to_6_and_is_written_as_its_projection(entry):
    """Checks 1 to 7: every check fixture is accepted, and the view written for it is the projection the fixture shows."""
    thesis, article, company, research_list = inputs_of(entry)
    answer = exact(entry['answer'])
    reasons, passage = check(answer, entry)
    assert reasons == []
    if answer['ladder'] is None:
        assert entry['written']['view'] is None
        return
    view = ladder_step.write_view(answer['ladder'], passage, thesis=thesis, article_day=article['publication_date'], company=company, research_list=research_list)
    written = entry['written']
    assert (view['object_id'], view['object_kind'], view['kind'], view['year'], view['due_day']) == \
        (written['object_id'], written['object_kind'], written['kind'], written['year'], written['due_day'])
    assert [(rung['label'], rung['condition'], rung.get('lo'), rung.get('hi')) for rung in view['rungs']] == \
        [(rung['label'], rung['condition'], rung.get('lo'), rung.get('hi')) for rung in written['rungs']]
    assert view['looks_at'] == thesis['outcome']


# ---- check 1: shape -----------------------------------------------------------------------------------------------------------

def test_check_1_exactly_one_of_no_ladder_and_ladder_is_null():
    both = copy.deepcopy(EVENT_TWO['answer']); both['no_ladder'] = 'a reason'
    neither = {'no_ladder': None, 'ladder': None}
    assert reasons_for(both, EVENT_TWO) == ['exactly one of no_ladder and ladder must be null']
    assert reasons_for(neither, EVENT_TWO) == ['exactly one of no_ladder and ladder must be null']


def test_check_1_exactly_one_answer_shape_is_filled():
    two_shapes = changed(EVENT_TWO, lambda ladder: ladder.update(figure=copy.deepcopy(COMPANY_FIGURE['answer']['ladder']['figure'])))
    no_shape = changed(EVENT_TWO, lambda ladder: ladder.update(event=None))
    assert reasons_for(two_shapes, EVENT_TWO) == ['exactly one of event and figure must be filled; 2 are']
    assert reasons_for(no_shape, EVENT_TWO) == ['exactly one of event and figure must be filled; 0 are']


@pytest.mark.parametrize('count', [4, 6])
def test_check_1_a_figure_has_exactly_five_ranges(count):
    """Production's validator enforces no maximum length, so the count is this check's."""
    def resize(ladder):
        ranges = ladder['figure']['ranges']
        if count == 4:
            ranges[3]['hi'] = None; ranges.pop()
        else:
            ranges[4] = {'lo': 180000000000.0, 'hi': 200000000000.0}; ranges.append({'lo': 200000000000.0, 'hi': None})
    answer = changed(COMPANY_FIGURE, resize)
    assert model.check_schema(answer, SCHEMA) == []                                      # the schema lets both through
    assert f'a figure has exactly five ranges; this one has {count}' in reasons_for(answer, COMPANY_FIGURE)


@pytest.mark.parametrize('addition', [' Compared with the figure cited in this item.', ' Compared with the $119 billion cited in the item.',
                                      " Against the article's forecast."])
def test_d407_a_question_that_points_at_the_item_is_refused(addition):
    answer = changed(COMPANY_FIGURE, lambda ladder: ladder.update(question=ladder['question'] + addition))
    assert any('refers to the item or the article' in reason for reason in reasons_for(answer, COMPANY_FIGURE))


def test_d407_a_condition_that_points_at_the_item_is_refused_and_an_article_of_law_is_not():
    in_happened = changed(EVENT_TWO, lambda ladder: ladder['event'].update(happened=ladder['event']['happened'] + ' As this article describes.'))
    in_ruled_out = changed(EVENT_THREE, lambda ladder: ladder['event']['ruled_out'].update(decision=ladder['event']['ruled_out']['decision'] + ' As stated in the item.'))
    an_article_of_law = changed(EVENT_TWO, lambda ladder: ladder.update(question=ladder['question'] + ' (under the Article 232 tariffs)'))
    assert any('refers to the item or the article' in reason for reason in reasons_for(in_happened, EVENT_TWO))
    assert any('refers to the item or the article' in reason for reason in reasons_for(in_ruled_out, EVENT_THREE))
    assert reasons_for(an_article_of_law, EVENT_TWO) == []


# ---- check 2: the object ------------------------------------------------------------------------------------------------------

@pytest.mark.parametrize('object_name', ['AMD', 'memory-chip-prices', ''])
def test_check_2_another_company_or_an_unlisted_theme_is_refused(object_name):
    answer = changed(EVENT_TWO, lambda ladder: ladder.update(object=object_name))
    reasons = reasons_for(answer, EVENT_TWO)
    assert any('is not the company NVDA or a listed theme' in reason and 'Choose the correct listed object if one applies' in reason for reason in reasons)


# ---- check 4: a figure --------------------------------------------------------------------------------------------------------

def figure_text(entry, old_number, new_token):
    """A figure fixture's answer as JSON text with one number token replaced, to carry tokens a float cannot."""
    text = json.dumps(entry['answer'])
    assert text.count(old_number) >= 1
    return ladder_step.parse_exactly(text.replace(old_number, new_token))


@pytest.mark.parametrize('token', ['NaN', 'Infinity', '1e400', '1e999999999999999999999999'])
def test_check_4_a_bound_that_is_not_a_finite_number_is_refused(token):
    answer = figure_text(COMPANY_FIGURE, '180000000000.0', token)
    assert 'every bound that is not null is a finite number' in reasons_for(answer, COMPANY_FIGURE)


@pytest.mark.parametrize('token, text', [('73.50', '73.5'), ('9007199254740993', '9,007,199,254,740,993'), ('2.5e18', '2,500,000,000,000,000,000'),
                                         ('17234567891234567.89', '17234567891234567.89'), ('1e+0000', '1'), ('-250', '-250'), ('0', '0'), ('-0', '0')])
def test_check_4_and_7_any_finite_number_is_accepted_and_written_as_the_number_it_is(token, text):
    number = ladder_step.read_number_token(token)
    assert ladder_step.is_finite_number(number)
    assert ladder_step.written_number(number) == text


def test_check_4_and_7_a_figure_with_long_and_large_bounds_is_accepted_and_written_as_those_numbers():
    """Through the check and the view writer: no limit on size or digits; the text is the number the model wrote."""
    thesis, _, company, research_list = inputs_of(COMPANY_FIGURE)
    text = json.dumps(COMPANY_FIGURE['answer']).replace('140000000000.0', '17234567891234567.89').replace('180000000000.0', '2.5e18')
    answer = ladder_step.parse_exactly(text)
    reasons, passage = check(answer, COMPANY_FIGURE)
    assert reasons == []
    conditions = [rung['condition'] for rung in ladder_step.write_view(answer['ladder'], passage, thesis=thesis, article_day='2026-07-01', company=company, research_list=research_list)['rungs']]
    assert 'from 17234567891234567.89 USD to below 2,500,000,000,000,000,000 USD' in conditions
    assert '2,500,000,000,000,000,000 USD or more' in conditions


def test_check_4_the_ranges_meet_end_to_end():
    gap = changed(COMPANY_FIGURE, lambda ladder: ladder['figure']['ranges'][2].update(lo=115000000000.0))
    assert any('must meet end to end' in reason for reason in reasons_for(gap, COMPANY_FIGURE))


def test_check_4_no_range_is_empty():
    def empty(ladder):
        ranges = ladder['figure']['ranges']
        ranges[1]['hi'] = ranges[1]['lo']; ranges[2]['lo'] = ranges[1]['lo']
    assert any('holds no value' in reason for reason in reasons_for(changed(COMPANY_FIGURE, empty), COMPANY_FIGURE))


def test_check_4_the_ranges_are_open_below_and_above():
    closed_below = changed(COMPANY_FIGURE, lambda ladder: ladder['figure']['ranges'][0].update(lo=0.0))
    closed_above = changed(COMPANY_FIGURE, lambda ladder: ladder['figure']['ranges'][4].update(hi=500000000000.0))
    assert 'exactly one range, the lowest, has lo null' in reasons_for(closed_below, COMPANY_FIGURE)
    assert 'exactly one range, the highest, has hi null' in reasons_for(closed_above, COMPANY_FIGURE)


def test_check_4_the_order_the_ranges_are_listed_in_does_not_matter():
    shuffled = changed(COMPANY_FIGURE, lambda ladder: ladder['figure']['ranges'].reverse())
    assert reasons_for(shuffled, COMPANY_FIGURE) == []


@pytest.mark.parametrize('favourable_end, why', [('n/a', 'A reason.'), ('lower', '  ')])
def test_check_4_a_companys_figure_names_its_favourable_end_with_a_reason(favourable_end, why):
    answer = changed(COMPANY_FIGURE, lambda ladder: ladder['figure'].update(favourable_end=favourable_end, favourable_why=why))
    assert any("names its favourable end" in reason for reason in reasons_for(answer, COMPANY_FIGURE))


def test_check_4_a_themes_figure_has_no_favourable_end():
    answer = changed(THEME_FIGURE, lambda ladder: ladder['figure'].update(favourable_end='higher', favourable_why='More spending.'))
    assert any("favourable_end n/a" in reason for reason in reasons_for(answer, THEME_FIGURE))


def test_check_4_the_year_has_the_form_of_its_objects_kind():
    company_with_calendar_year = changed(COMPANY_FIGURE, lambda ladder: ladder['figure'].update(year='2027'))
    theme_with_fiscal_year = changed(THEME_FIGURE, lambda ladder: ladder['figure'].update(year='FY2027'))
    trailing_line_break = changed(COMPANY_FIGURE, lambda ladder: ladder['figure'].update(year='FY2027\n'))
    assert any('FY and four digits' in reason for reason in reasons_for(company_with_calendar_year, COMPANY_FIGURE))
    assert any('calendar year as four digits' in reason for reason in reasons_for(theme_with_fiscal_year, THEME_FIGURE))
    assert any('FY and four digits' in reason for reason in reasons_for(trailing_line_break, COMPANY_FIGURE))


# ---- check 5: dates -----------------------------------------------------------------------------------------------------------

def test_check_5_the_due_day_is_a_real_date_after_the_items_day():
    not_a_date = changed(EVENT_TWO, lambda ladder: ladder.update(due_day='2026-13-45'))
    same_day = changed(EVENT_TWO, lambda ladder: ladder.update(due_day='2026-07-02'))
    assert any('not a real date' in reason for reason in reasons_for(not_a_date, EVENT_TWO))
    assert any("not after the item's day" in reason for reason in reasons_for(same_day, EVENT_TWO))


def test_check_5_a_binding_obligation_is_due_within_548_days_not_549():
    """D185, as production computes it: the fixture's due day is day 548 exactly and is accepted; the next day is refused."""
    assert reasons_for(OBLIGATION['answer'], OBLIGATION) == []
    one_day_later = changed(OBLIGATION, lambda ladder: ladder.update(due_day='2028-01-01'))
    assert any('at most 548 days' in reason for reason in reasons_for(one_day_later, OBLIGATION))


def test_check_5_a_figure_beyond_next_year_is_refused_unless_the_topic_is_a_binding_obligation():
    beyond = changed(COMPANY_FIGURE, lambda ladder: (ladder['figure'].update(year='FY2029'), ladder.update(due_day='2027-12-01', due_day_basis='stated')))
    assert reasons_for(beyond, COMPANY_FIGURE) == []                                   # the fixture's thesis is a binding obligation
    assert any('beyond next year' in reason for reason in reasons_for(beyond, COMPANY_FIGURE, thesis_changes={'opens_as': 'product_node'}))


def test_check_5_a_figure_for_a_year_already_ended_is_refused_with_no_exception():
    ended = changed(COMPANY_FIGURE, lambda ladder: ladder['figure'].update(year='FY2026'))
    assert any('had ended' in reason for reason in reasons_for(ended, COMPANY_FIGURE))


def test_check_5_the_due_days_basis_fits_the_shape():
    figure_with_period_end = changed(COMPANY_FIGURE, lambda ladder: ladder.update(due_day_basis='period_end'))
    event_with_expected_publication = changed(EVENT_TWO, lambda ladder: ladder.update(due_day_basis='expected_publication'))
    assert any('does not fit a figure' in reason for reason in reasons_for(figure_with_period_end, COMPANY_FIGURE))
    assert any('does not fit an event' in reason for reason in reasons_for(event_with_expected_publication, EVENT_TWO))


# ---- check 6: the reference (D405) --------------------------------------------------------------------------------------------

ARTICLE = ('Shares fell on Tuesday. The company does not expect sales to increase this year, its finance chief said. '
           'Analysts had forecast revenue of $12 billion [5] . Rivals plan to shift 46% of budgets, up from roughly 30% today [6] . '
           'Orders grew ≥10%, and the backlog [7] rose again.')


@pytest.mark.parametrize('words, written', [
    ('The company does not expect sales to increase this year', 'The company does not expect sales to increase this year'),      # exact
    ('the company does not expect sales to increase this year', 'The company does not expect sales to increase this year'),      # letter case aside
    ('Rivals plan to shift 46% of budgets, up from roughly 30% today.', 'Rivals plan to shift 46% of budgets, up from roughly 30% today'),   # a footnote marker before the full stop, as Stage A met it
    ('Analysts had forecast revenue of $12 billion.', 'Analysts had forecast revenue of $12 billion'),                           # the same
    ('and the backlog rose again', 'and the backlog [7] rose again.'),          # a footnote marker between words; production's repair takes the closing stop into the passage
    ('The company does expect sales to increase this year', None),                                                               # a left-out "not"
    ('Analysts had forecast revenue this year of $12 billion', None),                                                            # moved words
    ('Analysts had confidently forecast revenue of $12 billion', None),                                                          # an added word
    ('The company does not expect sales to increase this year, its finance chief said. Analysts agreed', None),                 # runs on past the article
    ('Rivals plan to shift 46% of budgets up from roughly 30% today', None),                                                     # a dropped comma
    ('The company does not expect sales to increase this year.', None),                                                          # a full stop where the article has a comma
    ('Orders grew 10%, and the backlog rose again', None),                                                                       # a dropped sign
])
def test_d405_a_references_words_are_one_unbroken_passage_of_the_article(words, written):
    assert ladder_step.article_passage(words, ARTICLE, extraction.repair_quote, extraction.normalise, extraction._quote_tokens) == written


def test_d405_a_repaired_passage_that_holds_words_the_quote_does_not_is_refused():
    """The quote is not exact (its first letter is a capital). Its text, case aside, can be found in the article cut out of
    "million", and production's repair answers with a passage holding five words the quote does not. What is written must hold
    the quote's words and no others, so this is a refusal."""
    article = 'The ion in 2026 was 5 million in 2026 overall and beyond.'
    words = 'Ion in 2026 overall and beyond'
    assert words not in article
    assert extraction.repair_quote(words, article) == 'ion in 2026 was 5 million in 2026 overall and beyond.'
    assert ladder_step.article_passage(words, article, extraction.repair_quote, extraction.normalise, extraction._quote_tokens) is None


def test_d405_a_quote_of_fewer_than_eight_characters_is_accepted_only_when_exact():
    """Production's repair looks at no quote that short; the boundary is kept and stated."""
    assert ladder_step.article_passage('Shares', ARTICLE, extraction.repair_quote, extraction.normalise, extraction._quote_tokens) == 'Shares'
    assert ladder_step.article_passage('shares', ARTICLE, extraction.repair_quote, extraction.normalise, extraction._quote_tokens) is None


def test_check_6_words_that_are_not_the_articles_refuse_the_answer():
    answer = changed(THEME_FIGURE, lambda ladder: ladder['reference'].update(words='Nvidia projects that this figure could reach $1 trillion next year.'))
    assert any("the reference's words are not in the item" in reason for reason in reasons_for(answer, THEME_FIGURE))


def test_check_6_a_figures_reference_value_lies_in_the_middle_range():
    at_the_upper_bound = changed(THEME_FIGURE, lambda ladder: ladder['reference'].update(value=ladder['figure']['ranges'][2]['hi']))
    at_the_lower_bound = changed(THEME_FIGURE, lambda ladder: ladder['reference'].update(value=ladder['figure']['ranges'][2]['lo']))
    assert any('must lie in the middle range' in reason for reason in reasons_for(at_the_upper_bound, THEME_FIGURE))
    assert reasons_for(at_the_lower_bound, THEME_FIGURE) == []


def view_of(answer, entry):
    thesis, article, company, research_list = inputs_of(entry)
    exact_answer = exact(answer)
    reasons, passage = check(exact_answer, entry)
    assert reasons == []
    return ladder_step.write_view(exact_answer['ladder'], passage, thesis=thesis, article_day=article['publication_date'], company=company,
                                  research_list=research_list)


@pytest.mark.parametrize('entry, the_day_code_sets', [(COMPANY_FIGURE, '2027-04-01'), (THEME_FIGURE, '2028-03-30')])
def test_d414_a_years_figure_with_an_estimated_day_is_due_a_fixed_time_after_its_year_ends_whatever_day_the_model_wrote(entry, the_day_code_sets):
    """A company's fiscal year 2027 ends on 2027-01-31: 60 days later is 2027-04-01. Calendar 2027 ends on 2027-12-31: 90 days
    later is 2028-03-30. Two answers that differ only in the day the model expects are due on the same day."""
    year_end = {'2027-04-01': '2027-01-31', '2028-03-30': '2027-12-31'}[the_day_code_sets]
    days = set()
    for the_day_the_model_expects in (year_end, '2028-06-30' if entry is THEME_FIGURE else '2027-03-05'):
        answer = changed(entry, lambda ladder: ladder.update(due_day=the_day_the_model_expects, due_day_basis='expected_publication'))
        days.add(view_of(answer, entry)['due_day'])
    assert days == {the_day_code_sets}


def test_d414_a_day_the_topic_or_the_item_states_is_kept_and_an_events_day_is_kept():
    stated = changed(COMPANY_FIGURE, lambda ladder: ladder.update(due_day='2027-03-05', due_day_basis='stated'))
    assert view_of(stated, COMPANY_FIGURE)['due_day'] == '2027-03-05'
    assert view_of(EVENT_TWO['answer'], EVENT_TWO)['due_day'] == EVENT_TWO['answer']['ladder']['due_day']


def test_d414_a_figure_expected_before_its_year_ends_is_not_that_years_figure_and_is_refused():
    """A quarter's figure filed under fiscal 2027 is expected in November 2026, before the year ends on 2027-01-31."""
    a_quarter = changed(COMPANY_FIGURE, lambda ladder: ladder.update(due_day='2026-11-18', due_day_basis='expected_publication'))
    on_the_last_day = changed(COMPANY_FIGURE, lambda ladder: ladder.update(due_day='2027-01-31', due_day_basis='expected_publication'))
    assert any('which ends on 2027-01-31, and you expect it published on 2026-11-18, before that' in reason for reason in reasons_for(a_quarter, COMPANY_FIGURE))
    assert reasons_for(on_the_last_day, COMPANY_FIGURE) == []


def test_d414_the_rules_on_the_due_day_read_the_day_code_sets():
    """The fixture's thesis is a binding obligation opened on 2026-07-06: 548 days later is 2028-01-05. A figure for fiscal 2028
    (which the research list's fiscal calendar ends on 2028-01-31) with an estimated day is due on 2028-03-31 by code, beyond
    that, though the day the model wrote is inside."""
    beyond = changed(COMPANY_FIGURE, lambda ladder: (ladder['figure'].update(year='FY2028'), ladder.update(due_day='2028-01-31', due_day_basis='expected_publication')))
    stated = changed(COMPANY_FIGURE, lambda ladder: (ladder['figure'].update(year='FY2028'), ladder.update(due_day='2027-12-31', due_day_basis='stated')))
    assert any('a binding obligation is due at most 548 days after the item; 2028-03-31 is later' in reason for reason in reasons_for(beyond, COMPANY_FIGURE))
    assert reasons_for(stated, COMPANY_FIGURE) == []


TYPED_RULING_OUT = {'by_whom': 'The company', 'decision': 'The company formally cancels the launch, or states that it will not ship by the due day.'}


def test_d416_a_typed_ruling_out_is_shown_to_the_judge_as_its_decision_sentence_under_codes_scope():
    """The typed shape (who decides, what they decide) gives the same three rungs as one sentence does: the decision is the
    second rung's first sentence, and code's sentence on the scope follows it."""
    typed = changed(EVENT_TWO, lambda ladder: ladder['event'].update(ruled_out=dict(TYPED_RULING_OUT)))
    as_a_sentence = changed(EVENT_TWO, lambda ladder: ladder['event'].update(ruled_out=TYPED_RULING_OUT['decision']))
    typed_view, sentence_view = view_of(typed, EVENT_TWO), view_of(as_a_sentence, EVENT_TWO)
    assert [rung['label'] for rung in typed_view['rungs']] == ['Yes', 'Ruled out', 'Still open']
    assert typed_view['rungs'][1]['condition'].startswith(TYPED_RULING_OUT['decision'] + ' This rung holds when that, or any other decision against')
    assert typed_view['rungs'] == sentence_view['rungs']


@pytest.mark.parametrize('part', ['by_whom', 'decision'])
def test_d416_a_typed_ruling_out_names_both_who_decides_and_what_they_decide(part):
    empty = changed(EVENT_TWO, lambda ladder: ladder['event'].update(ruled_out=dict(TYPED_RULING_OUT, **{part: '  '})))
    assert 'ruled_out names who decides and what they decide: neither by_whom nor decision may be empty' in reasons_for(empty, EVENT_TWO)


def test_d416_a_typed_ruling_out_is_read_for_a_reference_to_the_item_like_any_condition():
    pointing = changed(EVENT_TWO, lambda ladder: ladder['event'].update(ruled_out=dict(TYPED_RULING_OUT, decision='The company cancels the launch described in this item.')))
    assert any('refers to the item or the article' in reason for reason in reasons_for(pointing, EVENT_TWO))


def test_d411_a_reported_amount_is_named_as_that_to_the_judge_and_never_as_the_reference():
    thesis, article, company, research_list = inputs_of(THEME_FIGURE)
    expected = exact(THEME_FIGURE['answer'])
    reported = exact(changed(THEME_FIGURE, lambda ladder: ladder['reference'].update(kind='last_reported')))
    views = {}
    for name, answer in (('expected', expected), ('last_reported', reported)):
        reasons, passage = check(answer, THEME_FIGURE)
        assert reasons == []
        views[name] = ladder_step.write_view(answer['ladder'], passage, thesis=thesis, article_day='2026-07-01', company=company, research_list=research_list)
    assert views['expected']['reference_status'] == 'reference figure' and '(the reference when the question opened: "' in views['expected']['rungs'][2]['condition']
    assert views['last_reported']['reference_status'] == 'last reported figure'
    assert '(the amount last reported when the question opened: "' in views['last_reported']['rungs'][2]['condition']
    assert 'the reference when the question opened' not in views['last_reported']['rungs'][2]['condition']


def test_d411_an_events_reference_is_never_a_reported_amount():
    with_a_plan = changed(EVENT_TWO, lambda ladder: ladder.update(reference={'words': 'could begin shipping later this year', 'kind': 'expected', 'value': None, 'value_to': None}))
    as_reported = changed(EVENT_TWO, lambda ladder: ladder.update(reference={'words': 'could begin shipping later this year', 'kind': 'last_reported', 'value': None, 'value_to': None}))
    assert not any('last_reported' in reason for reason in reasons_for(with_a_plan, EVENT_TWO))
    assert any('a reference of kind last_reported belongs to a figure' in reason for reason in reasons_for(as_reported, EVENT_TWO))


@pytest.mark.parametrize('value, value_to, accepted', [
    (900000000000.0, 1100000000000.0, True),        # the stated range is the middle range itself, end to end
    (950000000000.0, 1050000000000.0, True),        # well inside
    (850000000000.0, 1050000000000.0, False),       # starts below the middle range
    (1000000000000.0, 1200000000000.0, False),      # its middle and its lower end lie inside, its upper end beyond: a part of what is expected would fall in the next rung
])
def test_d411_the_middle_range_spans_a_stated_range_from_end_to_end(value, value_to, accepted):
    """The fixture's middle range runs from 900 billion to below 1.1 trillion. The rule is on the two ends, as the request words
    it: the middle range starts at or below the stated range's lower end and ends at or above its upper end."""
    answer = changed(THEME_FIGURE, lambda ladder: ladder['reference'].update(value=value, value_to=value_to))
    refused = any('must run from at or below the lower end' in reason for reason in reasons_for(answer, THEME_FIGURE))
    assert refused is not accepted
    assert accepted is (reasons_for(answer, THEME_FIGURE) == [])


@pytest.mark.parametrize('value, value_to', [(1000000000000.0, 1000000000000.0), (1000000000000.0, 900000000000.0), (None, 1000000000000.0)])
def test_d411_the_upper_end_of_a_range_is_greater_than_its_lower_end_and_never_stands_alone(value, value_to):
    answer = changed(THEME_FIGURE, lambda ladder: ladder['reference'].update(value=value, value_to=value_to))
    assert 'value_to is the upper end of a range the item states: it is null, or greater than value' in reasons_for(answer, THEME_FIGURE)


def test_d411_the_schema_asks_every_reference_for_its_kind():
    without_kind = changed(THEME_FIGURE, lambda ladder: ladder['reference'].pop('kind'))
    another_kind = changed(THEME_FIGURE, lambda ladder: ladder['reference'].update(kind='guidance'))
    assert model.check_schema(THEME_FIGURE['answer'], SCHEMA) == []
    assert model.check_schema(without_kind, SCHEMA) != [] and model.check_schema(another_kind, SCHEMA) != []


def test_check_6_and_7_a_reference_in_words_alone_is_kept_and_the_ladder_marked_as_having_no_reference_figure():
    thesis, _, company, research_list = inputs_of(THEME_FIGURE)
    answer = exact(changed(THEME_FIGURE, lambda ladder: ladder['reference'].update(value=None)))
    reasons, passage = check(answer, THEME_FIGURE)
    view = ladder_step.write_view(answer['ladder'], passage, thesis=thesis, article_day='2026-07-01', company=company, research_list=research_list)
    assert reasons == [] and passage
    assert view['reference_status'] == 'no reference figure'
    assert view['rungs'][2]['condition'].endswith(' (no reference figure when the question opened)')


# ---- check 7: what is written -------------------------------------------------------------------------------------------------

def test_check_7_position_1_is_strongly_bullish_at_the_favourable_end():
    thesis, _, company, research_list = inputs_of(HIGHER_FAVOURABLE)
    higher = exact(HIGHER_FAVOURABLE['answer'])
    lower = exact(changed(HIGHER_FAVOURABLE, lambda ladder: ladder['figure'].update(favourable_end='lower')))
    rungs_higher = ladder_step.write_view(higher['ladder'], 'x', thesis=thesis, article_day='2026-07-01', company=company, research_list=research_list)['rungs']
    rungs_lower = ladder_step.write_view(lower['ladder'], 'x', thesis=thesis, article_day='2026-07-01', company=company, research_list=research_list)['rungs']
    assert [rung['label'] for rung in rungs_higher] == ladder_step.COMPANY_LABELS == [rung['label'] for rung in rungs_lower]
    assert rungs_higher[0]['hi'] is None and rungs_higher[4]['lo'] is None            # the highest range is Strongly bullish
    assert rungs_lower[0]['lo'] is None and rungs_lower[4]['hi'] is None              # the lowest range is Strongly bullish
    assert rungs_higher[2]['lo'] == rungs_lower[2]['lo']                              # the middle range is Neutral either way


def test_check_7_an_events_year_is_the_year_of_its_due_day():
    thesis, _, company, research_list = inputs_of(EVENT_TWO)
    view = ladder_step.write_view(exact(EVENT_TWO['answer'])['ladder'], None, thesis=thesis, article_day='2026-07-01', company=company, research_list=research_list)
    assert view['year'] == EVENT_TWO['answer']['ladder']['due_day'][:4]


def test_d409_an_event_with_nothing_to_rule_it_out_has_two_rungs_the_second_written_by_code():
    """Exactly one rung holds for every outcome: the second rung is the complement of the first, whatever the first says."""
    rungs = ladder_step.event_rungs({'happened': 'The regulator has cleared the merger.', 'ruled_out': None}, '2027-06-30', '2026-07-01')
    assert rungs == [{'label': 'Yes', 'condition': 'The regulator has cleared the merger.'},
                     {'label': 'No', 'condition': 'Rung 1 does not hold on 2027-06-30.'}]


@pytest.mark.parametrize('ruled_out', ['The regulator has blocked the merger or the filing is withdrawn.', 'The regulator has blocked the merger or the filing is withdrawn  '])
def test_d409_an_event_that_can_be_ruled_out_has_three_rungs_and_code_makes_them_exclude_one_another(ruled_out):
    """The second rung takes the way named and every other decision against the event as a whole that was taken after the
    article's day and stands on the due day, and holds only when the first does not; the third is the complement of both; a
    condition with no full stop is given one before the code's sentence."""
    rungs = ladder_step.event_rungs({'happened': 'The regulator has cleared the merger.', 'ruled_out': ruled_out}, '2027-06-30', '2026-07-01')
    assert rungs == [{'label': 'Yes', 'condition': 'The regulator has cleared the merger.'},
                     {'label': 'Ruled out', 'condition': 'The regulator has blocked the merger or the filing is withdrawn. This rung holds when that, or any other '
                                                         'decision against the event of rung 1 as a whole, or a formal abandonment or withdrawal of it as a '
                                                         'whole, was made after 2026-07-01 and stands on 2027-06-30, and only when rung 1 does not.'},
                     {'label': 'Still open', 'condition': 'Neither rung 1 nor rung 2 holds on 2027-06-30.'}]


def test_d409_the_schema_takes_an_event_and_refuses_the_retired_shapes():
    assert model.check_schema(EVENT_THREE['answer'], SCHEMA) == [] and model.check_schema(EVENT_TWO['answer'], SCHEMA) == []
    one_sentence = changed(EVENT_THREE, lambda ladder: ladder['event'].update(ruled_out=ladder['event']['ruled_out']['decision']))
    assert model.check_schema(one_sentence, SCHEMA) != []                              # D416: the ruling out is who decides and what they decide
    five_states = changed(EVENT_TWO, lambda ladder: ladder.update(states=[{'label': 'Neutral', 'condition': 'Nothing yet.'}]))
    yes_no = changed(EVENT_TWO, lambda ladder: ladder.update(yes_no={'yes': 'It happened.', 'no': 'It did not.'}))
    assert model.check_schema(five_states, SCHEMA) != [] and model.check_schema(yes_no, SCHEMA) != []


# ---- check 8: one thesis, one or two requests, through the real model call, archive and spending limit -----------------------

SETTING = config.Setting(name='clean_ladder', model='gpt-6-luna', prompt_version='test', reasoning_effort='medium', max_output_tokens=16000)


def payload_of(entry):
    thesis, article, company, _ = inputs_of(entry)
    return {'company': company, 'fiscal_year_note': 'a note', 'themes': [], 'thesis': thesis,
            'item': {field: article[field] for field in ('publication_date', 'publisher', 'title', 'text')}}


def run_step(tmp_path, entry, answer_texts, usage=(1000, 200)):
    """Run the step for one fixture's thesis against a fake transport that returns the given texts in turn."""
    sent_requests = []
    texts = iter(answer_texts)

    def fake_transport(provider, request):
        sent_requests.append(request)
        return {'choices': [{'message': {'content': next(texts)}}], 'usage': {'prompt_tokens': usage[0], 'completion_tokens': usage[1]}}

    limit = budget.Budget(1.00, attempt=fake_transport)
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    call_model = model_calls.model_caller(model, archive, SimpleNamespace(provider='openai', version='test', checksum='test'), SETTING, limit)
    outcome = ladder_step.ladder_for_thesis(payload_of(entry), system_text='system', closing_text='closing', schema=SCHEMA,
                                            call_model=call_model, check=lambda answer: check(answer, entry))
    return outcome, sent_requests, limit


def test_check_8_an_accepted_answer_is_one_request(tmp_path):
    outcome, sent, _ = run_step(tmp_path, COMPANY_FIGURE, [json.dumps(COMPANY_FIGURE['answer'])])
    assert outcome['status'] == 'ladder' and len(sent) == 1
    assert [request['result'] for request in outcome['requests']] == ['ladder']
    assert sent[0]['messages'][1]['content'].endswith('\n\nclosing')


def test_check_8_a_refused_answer_is_sent_back_once_with_its_reasons(tmp_path):
    refused = json.dumps(changed(COMPANY_FIGURE, lambda ladder: ladder.update(question=ladder['question'] + ' As cited in this item.')))
    outcome, sent, limit = run_step(tmp_path, COMPANY_FIGURE, [refused, json.dumps(COMPANY_FIGURE['answer'])])
    assert outcome['status'] == 'ladder' and len(sent) == 2
    assert [request['result'] for request in outcome['requests']] == ['refused', 'ladder']
    resent = sent[1]['messages'][1]['content']
    assert resent.startswith(sent[0]['messages'][1]['content'])                         # the first request, then the note
    assert 'Your previous answer was:\n' + refused in resent                            # the model is shown what it wrote
    assert 'It was refused for the reasons below.' in resent and '- The question or a condition refers to the item or the article' in resent
    assert outcome['requests'][0]['answer_text'] == refused                              # the refused answer's own text is kept in full
    assert limit.spent_usd == pytest.approx(2 * (1000 * 0.10 + 200 * 0.50) / 1e6)        # both requests are charged from their tokens


def test_checks_1_and_8_six_ranges_are_refused_and_sent_back_through_the_steps_entry_point(tmp_path):
    def six(ladder):
        ladder['figure']['ranges'][4] = {'lo': 180000000000.0, 'hi': 200000000000.0}
        ladder['figure']['ranges'].append({'lo': 200000000000.0, 'hi': None})
    outcome, sent, _ = run_step(tmp_path, COMPANY_FIGURE, [json.dumps(changed(COMPANY_FIGURE, six)), json.dumps(COMPANY_FIGURE['answer'])])
    assert [request['result'] for request in outcome['requests']] == ['refused', 'ladder']
    assert outcome['requests'][0]['reasons'] == ['a figure has exactly five ranges; this one has 6'] and len(sent) == 2


def test_check_8_refused_twice_ends_with_no_ladder_and_both_sets_of_reasons(tmp_path):
    refused = json.dumps(changed(EVENT_TWO, lambda ladder: ladder.update(object='AMD')))
    outcome, sent, _ = run_step(tmp_path, EVENT_TWO, [refused, refused])
    assert outcome['status'] == 'no ladder: refused' and len(sent) == 2 and outcome['answer'] is None
    assert all(request['result'] == 'refused' and request['reasons'] for request in outcome['requests'])


def test_check_8_a_declined_topic_is_recorded_with_the_models_reason(tmp_path):
    outcome, sent, _ = run_step(tmp_path, DECLINED, [json.dumps(DECLINED['answer'])])
    assert outcome['status'] == 'no ladder' and outcome['reason'] == DECLINED['answer']['no_ladder'] and len(sent) == 1


@pytest.mark.parametrize('unreadable', [
    'not json at all',                                                                    # not JSON
    json.dumps({'no_ladder': None}),                                                      # does not fit the schema
    '{"no_ladder": null, "ladder": ' + '1' * 4301 + '}',                                  # an integer beyond Python's 4,300 digits
    '{"no_ladder": "\\ud800", "ladder": null}',                                           # a string the archive cannot store
    '[' * 100000 + ']' * 100000,                                                          # brackets nested too deep
])
def test_check_8_an_answer_that_cannot_be_read_is_refused_and_sent_back_and_its_text_and_cost_are_kept(tmp_path, unreadable):
    outcome, sent, limit = run_step(tmp_path, EVENT_TWO, [unreadable, json.dumps(EVENT_TWO['answer'])])
    assert outcome['status'] == 'ladder' and len(sent) == 2
    assert outcome['requests'][0]['result'] == 'refused' and outcome['requests'][0]['answer_text'] == unreadable
    assert outcome['requests'][0]['input_tokens'] == 1000 and limit.spent_usd == pytest.approx(2 * (1000 * 0.10 + 200 * 0.50) / 1e6)
    resent = sent[1]['messages'][1]['content']
    assert 'Your previous answer could not be used:' in resent and 'Your previous answer was:' not in resent
    json.loads(ladder_step.as_json(outcome))                                             # the record can be stored whatever the text held


def test_check_8_an_answer_from_the_cache_stops_the_step(tmp_path):
    answer_text = json.dumps(EVENT_TWO['answer'])
    run_step(tmp_path, EVENT_TWO, [answer_text])
    with pytest.raises(ladder_step.CachedAnswer):
        run_step(tmp_path, EVENT_TWO, [answer_text])                                         # the same request, the same archive
