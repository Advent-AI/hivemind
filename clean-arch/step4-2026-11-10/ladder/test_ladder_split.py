"""The period split's step (splitting/DESIGN.md v4, D616) on a real stored topic and article (the five largest hyperscalers' capex in
calendar 2026 and 2027, c1/clean-4 of the week of 2026-10-06), with the frozen step's own checks and a fake model; nothing is sent."""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / 'src'), str(ROOT / 'clean-arch' / 'e2e-2026-11-09'), str(HERE.parent / 'stage_a')]
import ladder_split  # noqa: E402
import ladder_step  # noqa: E402
from hivemind import extraction, model, universe  # noqa: E402

RESEARCH_LIST = universe.load(str(ROOT / 'poc' / 'universe.json'))
CASE = next(c for c in json.loads((ROOT / 'poc/data/clean-second-week-2026-11-15/week-continued/c1/cases/cases.json').read_text())
            if c['case'] == 'c1/clean-4')
FROZEN_SCHEMA = json.loads((HERE / 'candidate-schema.json').read_text())
SCHEMA = ladder_split.split_schema(FROZEN_SCHEMA)
SYSTEM, CLOSING = 'the system text', 'the closing check'
DAY = CASE['item']['publication_date']
B = 10 ** 9
WORDS = {'2026': ('plan to spend approximately $800 billion in capital expenditures (capex) in 2026 alone', 800 * B, [600 * B, 700 * B, 900 * B, 1000 * B]),
         '2027': ('roughly $1.3 trillion in 2027', 1300 * B, [900 * B, 1100 * B, 1500 * B, 1700 * B])}


def frozen_check(answer):
    return ladder_step.check_answer(answer, thesis=CASE['thesis'], article=CASE['item'], company='NVDA', research_list=RESEARCH_LIST,
                                    repair_quote=extraction.repair_quote, normalise=extraction.normalise, quote_tokens=extraction._quote_tokens,
                                    beyond_next_year=extraction.beyond_next_year, binding_horizon_days=extraction.BINDING_HORIZON_DAYS)


def check_for(year):
    return ladder_split.checker(frozen_check, article_day=DAY, company='NVDA', research_list=RESEARCH_LIST, year=year)


def ladder_text(year):
    words, value, bounds = WORDS[year]
    ranges = [{'lo': None, 'hi': bounds[0]}] + [{'lo': a, 'hi': b} for a, b in zip(bounds, bounds[1:])] + [{'lo': bounds[-1], 'hi': None}]
    return json.dumps({'no_ladder': None, 'ladder': {
        'question': f'How much combined capital expenditure will Amazon, Alphabet, Microsoft, Meta Platforms and Oracle report for calendar {year}?',
        'object': 'ai-capex', 'not_judged': [], 'event': None,
        'figure': {'unit': 'USD', 'year': year, 'ranges': ranges, 'favourable_end': 'n/a', 'favourable_why': ''},
        'reference': {'words': words, 'kind': 'expected', 'value': value, 'value_to': None},
        'due_day': f'{int(year) + 1}-02-28', 'due_day_basis': 'expected_publication'}})


def decline(case, reason, periods=None):
    return json.dumps({'no_ladder': {'case': case, 'reason': reason, 'periods': periods}, 'ladder': None})


SPLIT = decline('one_quantity_two_periods', 'The topic asks the big five capex for calendar 2026 and for calendar 2027.', ['2026', '2027'])


class FakeModel:
    """Answers by which question it is asked: the topic, or one year (the restriction line); records every request."""

    def __init__(self, topic, years):
        self.topic, self.years, self.sent = list(topic), {y: list(a) for y, a in years.items()}, []

    def __call__(self, system_text, user_text, schema):
        self.sent.append((system_text, user_text, schema))
        year = next((y for y in self.years if ladder_split.RESTRICTION.format(year=y, other='2027' if y == '2026' else '2026') in user_text), None)
        queue = self.years[year] if year else self.topic
        assert queue, 'a request beyond the topic\'s answers carries no yearly line'
        return {'answer_text': queue.pop(0), 'input_tokens': 10, 'output_tokens': 10, 'request_sha256': str(len(self.sent)), 'cached': False,
                'error': None}


def run(model):
    payload = {'company': 'NVDA', 'thesis': CASE['thesis'], 'item': CASE['item']}
    return ladder_split.ladder_for_thesis_split(payload, system_text=SYSTEM, closing_text=CLOSING, schema=SCHEMA, call_model=model,
                                                check_for=check_for), payload


@pytest.mark.parametrize('text', [ladder_text('2026'), ladder_text('2027'), SPLIT, decline('no_main', 'none main')])
def test_every_made_up_answer_fits_the_schema_production_validates_against(text):
    """`model.call` validates each answer against the schema before the step's checks; a made-up answer that does not fit it would
    pass the fake model and never pass production."""
    assert model.check_schema(json.loads(text), SCHEMA) == []


def test_the_schema_changes_only_the_refusal_field_into_the_closed_set_of_the_frozen_cases_plus_the_split():
    assert {k: v for k, v in SCHEMA['properties'].items() if k != 'no_ladder'} == {k: v for k, v in FROZEN_SCHEMA['properties'].items() if k != 'no_ladder'}
    assert {k: v for k, v in SCHEMA.items() if k != 'properties'} == {k: v for k, v in FROZEN_SCHEMA.items() if k != 'properties'}
    frozen = FROZEN_SCHEMA['properties']['no_ladder']['description']
    for name, meaning in ladder_split.CASES.items():
        assert name == ladder_split.SPLIT_CASE or meaning in frozen, name                    # every old case transcribed as it stands
    assert SCHEMA['properties']['no_ladder']['anyOf'][1]['properties']['case']['enum'] == list(ladder_split.CASES)


def test_the_split_system_text_is_the_frozen_one_with_the_decline_list_extended_by_the_eighth_case_only():
    frozen = (HERE / 'candidate-system.txt').read_text()
    split = ladder_split.split_system(frozen)
    for before, after in ladder_split.SYSTEM_REPLACEMENTS:
        assert frozen.count(before) == 1 and split.count(after) == 1
    restored = split
    for before, after in reversed(ladder_split.SYSTEM_REPLACEMENTS):
        restored = restored.replace(after, before)
    assert restored == frozen and 'in eight cases' in split and ladder_split.SPLIT_CASE not in split
    assert 'List every other part as before' in ladder_split.RESTRICTION and 'prevails' in ladder_split.RESTRICTION


@pytest.mark.parametrize('periods, accepted', [
    (['2026', '2027'], True), (['2027', '2026'], True), (['FY2027', 'FY2028'], True),
    (['2025', '2026'], False), (['2027', '2028'], False), (['2026', '2026'], False), (['2026', 'FY2027'], False),
    (['2026', '2027', '2028'], False), (None, False)])
def test_the_two_periods_must_be_this_year_and_next_written_alike(periods, accepted):
    assert (ladder_split.period_reasons(periods, DAY, 'NVDA', RESEARCH_LIST) == []) is accepted


def test_a_valid_split_re_asks_once_per_year_with_one_added_line_and_writes_both_years():
    model = FakeModel([SPLIT], {'2026': [ladder_text('2026')], '2027': [ladder_text('2027')]})
    outcome, payload = run(model)
    assert outcome['status'] == 'split' and outcome['periods'] == ['2026', '2027']
    assert {y: c['status'] for y, c in outcome['children'].items()} == {'2026': 'ladder', '2027': 'ladder'}
    assert [o['answer']['ladder']['figure']['year'] for o in outcome['children'].values()] == ['2026', '2027']
    topic_user = ladder_step.user_text(payload, CLOSING)
    assert model.sent[0] == (SYSTEM, topic_user, SCHEMA)
    for (system, user, schema), (year, other) in zip(model.sent[1:], (('2026', '2027'), ('2027', '2026'))):
        assert (system, schema) == (SYSTEM, SCHEMA)
        assert user == ladder_step.user_text(payload, CLOSING + '\n\n' + ladder_split.RESTRICTION.format(year=year, other=other))
    assert len(model.sent) == 3


def test_one_year_declining_and_one_failing_twice_are_recorded_truthfully():
    wrong_year = ladder_text('2027')
    model = FakeModel([SPLIT], {'2026': [wrong_year, wrong_year], '2027': [decline('no_main', 'The 2027 plan names no single total.')]})
    outcome, _ = run(model)
    assert outcome['children']['2026']['status'] == 'no ladder: refused'
    assert ladder_split.shown_reason(outcome['children']['2026']) == ladder_split.FAILED_TWICE
    assert outcome['children']['2027']['status'] == 'no ladder'
    assert ladder_split.shown_reason(outcome['children']['2027']) == 'The 2027 plan names no single total.'
    assert 'this question is for 2026 only' in json.dumps(outcome['children']['2026']['requests'][0]['reasons'])


def test_a_year_naming_the_split_again_is_refused_with_no_recursion():
    model = FakeModel([SPLIT], {'2026': [SPLIT, SPLIT], '2027': [ladder_text('2027')]})
    outcome, _ = run(model)
    assert outcome['children']['2026']['status'] == 'no ladder: refused' and len(model.sent) == 4


def test_a_split_naming_an_ended_year_is_malformed_and_nothing_is_split():
    ended = decline('one_quantity_two_periods', 'base year and target year', ['2025', '2026'])
    model = FakeModel([ended, ended], {})
    outcome, _ = run(model)
    assert outcome['status'] == 'no ladder: refused' and 'children' not in outcome and len(model.sent) == 2


@pytest.mark.parametrize('answer, status', [(decline('no_main', 'Several figures, none the main one.'), 'no ladder'), ('LADDER', 'ladder')])
def test_any_other_answer_passes_through_as_the_frozen_step_gives_it(answer, status):
    model = FakeModel([ladder_text('2026') if answer == 'LADDER' else answer], {})
    outcome, _ = run(model)
    assert outcome['status'] == status and 'children' not in outcome and len(model.sent) == 1


def test_a_decline_without_a_case_of_the_closed_set_or_with_stray_periods_is_refused():
    check = check_for(None)
    assert check(ladder_step.parse_exactly(json.dumps({'no_ladder': 'free text', 'ladder': None})))[0]
    assert check(ladder_step.parse_exactly(decline('made_up', 'x')))[0]
    assert check(ladder_step.parse_exactly(decline('no_main', 'x', ['2026', '2027'])))[0]
    assert check(ladder_step.parse_exactly(decline('no_main', 'x')))[0] == []
