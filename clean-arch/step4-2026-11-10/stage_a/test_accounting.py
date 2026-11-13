"""Tests of Stage A's accounting on made-up outcomes and rows (DESIGN.md §8: "The calculation is code, tested before the send on
made-up rows"). Each names the rule it proves. Run: python3 -m pytest clean-arch/step4-2026-11-10/stage_a/test_accounting.py
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import accounting  # noqa: E402

LABELS = ['Strongly bullish', 'Bullish', 'Neutral', 'Bearish', 'Strongly bearish']


def outcome(case, pass_number, kind='yes/no', favourable_end='lower', due_day='2027-01-31', not_judged=0):
    """A made-up send of the given kind, shaped as the runner writes it."""
    if kind == 'refused twice':
        return {'case': case, 'pass': pass_number, 'status': 'no ladder: refused', 'answer': None, 'view': None}
    if kind == 'refusal':
        return {'case': case, 'pass': pass_number, 'status': 'no ladder', 'answer': None, 'view': None}
    ladder = {'yes_no': None, 'states': None, 'figure': None, 'due_day': due_day,
              'not_judged': [{'part': f'part {number}', 'why': 'a reason'} for number in range(not_judged)]}
    if kind == 'yes/no':
        ladder['yes_no'] = {'yes': 'It happened.', 'no': 'It did not.'}
    elif kind in ('company states', 'theme states'):
        ladder['states'] = [{'label': label, 'condition': 'A state.'} for label in LABELS]
    else:
        ladder['figure'] = {'favourable_end': favourable_end if kind == 'company figure' else 'n/a'}
    company = kind in ('yes/no', 'company states', 'company figure')
    return {'case': case, 'pass': pass_number, 'status': 'ladder', 'answer': {'ladder': ladder},
            'view': {'kind': 'asset' if company else 'theme', 'due_day': due_day}}


def row(one_outcome, **changes):
    """A valid row that holds every mark that applies to the outcome, then changed as asked."""
    kind = accounting.kind_of(one_outcome)
    applicable = accounting.marks_that_apply(kind)
    made = {mark: ('holds' if mark in applicable else 'n/a') for mark in accounting.ALL_MARKS}
    made['G'] = 'holds' if kind in ('company figure', 'theme figure') else 'n/a'
    made['B'] = [] if kind == 'refusal' else ['not_a_bet'] * len(one_outcome['answer']['ladder']['not_judged'])
    made['W'], made['why'] = '', ''
    made.update(changes)
    if any(made[mark] == 'fails' for mark in applicable) or made['W']:
        made.setdefault('why', '')
        made['why'] = made['why'] or 'a reason'
    return made


def rows_for(outcomes, changes=None):
    changes = changes or {}
    return {(o['case'], o['pass']): row(o, **changes.get((o['case'], o['pass']), {})) for o in outcomes if accounting.kind_of(o) != 'refused twice'}


def forty_four(kind_of_case=lambda number: 'yes/no'):
    return [outcome(f'case-{number}', pass_number, kind_of_case(number)) for number in range(1, 45) for pass_number in (1, 2, 3)]


def test_all_sound_ladders_meet_lines_1_to_3_and_5_and_line_4_reads_no_refusal_occurred():
    outcomes = forty_four()
    report = accounting.account(outcomes, rows_for(outcomes), rows_for(outcomes), {})
    assert report['reading'] == 'complete'
    assert [report['lines'][number][0] for number in (1, 2, 3)] == ['met', 'met', 'met']
    assert report['lines'][4] == 'no refusal occurred'                                 # reported as that, never as a pass
    assert report['lines'][5] == ('met', {'right': 44, 'right by a ladder': 44, 'of': 44})


def test_a_missing_row_for_one_answer_makes_lines_1_to_5_not_measured():
    """A fault could sit in the answer nobody marked."""
    outcomes = forty_four()
    rows = rows_for(outcomes)
    missing = dict(rows); del missing[('case-7', 2)]
    report = accounting.account(outcomes, rows, missing, {})
    assert report['invalid rows'] == [(('case-7', 2), 'reader 2', 'no row')]
    assert all(report['lines'][number] == accounting.NOT_MEASURED for number in (1, 2, 3, 5))


@pytest.mark.parametrize('change, problem', [
    ({'Q': 'n/a'}, 'Q is'),                           # n/a on a mark that applies
    ({'W': None}, 'W is missing'),                    # no W
    ({'B': ['bet']}, 'B must hold'),                  # B of the wrong length
    ({'Q': 'fails', 'why': ' '}, 'why is empty'),     # a failed mark with no reason
])
def test_a_row_that_is_not_valid_is_not_a_reading(change, problem):
    outcomes = forty_four()
    made = row(outcomes[0])
    made.update(change)
    assert problem in accounting.row_problem(made, outcomes[0])


def test_a_figure_marked_g_n_a_is_not_a_valid_row_and_a_yes_no_marked_g_holds_is_not_either():
    figure, yes_no = outcome('a', 1, 'company figure'), outcome('b', 1, 'yes/no')
    assert 'G is' in accounting.row_problem(row(figure, G='n/a'), figure)
    assert accounting.row_problem(row(figure, G='not_assessable'), figure) is None
    assert 'G is' in accounting.row_problem(row(yes_no, G='holds'), yes_no)


def test_a_differing_mark_takes_the_third_readers_ruling_and_without_a_ruling_nothing_is_measured():
    outcomes = forty_four()
    key = ('case-3', 1)
    reader_1, reader_2 = rows_for(outcomes, {key: {'Q': 'fails'}}), rows_for(outcomes)
    without = accounting.account(outcomes, reader_1, reader_2, {})
    assert without['missing rulings'] == [(key, 'Q')] and without['lines'][1] == accounting.NOT_MEASURED
    upheld = accounting.account(outcomes, reader_1, reader_2, {key: {'marks': {'Q': 'fails'}}})
    cleared = accounting.account(outcomes, reader_1, reader_2, {key: {'marks': {'Q': 'holds'}}})
    assert upheld['lines'][1] == ('missed', [key]) and cleared['lines'][1] == ('met', [])


def test_a_w_upheld_on_an_otherwise_sound_ladder_makes_it_not_right_and_one_not_upheld_does_not():
    outcomes = forty_four()
    keys = [(f'case-{number}', pass_number) for number in range(1, 11) for pass_number in (1, 2)]     # ten cases, two sends each
    reader_1 = rows_for(outcomes, {key: {'W': 'A fault no mark names.'} for key in keys})
    upheld = accounting.account(outcomes, reader_1, rows_for(outcomes), {key: {'W': {'reader 1': True}} for key in keys})
    dismissed = accounting.account(outcomes, reader_1, rows_for(outcomes), {key: {'W': {'reader 1': False}} for key in keys})
    assert upheld['lines'][5] == ('missed', {'right': 34, 'right by a ladder': 34, 'of': 44}) and len(upheld['upheld W']) == 20
    assert dismissed['lines'][5][0] == 'met'
    assert accounting.account(outcomes, reader_1, rows_for(outcomes), {})['lines'][5] == accounting.NOT_MEASURED     # a W with no ruling


def test_a_twice_refused_answer_needs_no_row_stays_in_the_count_and_is_not_right():
    outcomes = forty_four()
    outcomes[0] = outcome('case-1', 1, 'refused twice')
    outcomes[1] = outcome('case-1', 2, 'refused twice')
    report = accounting.account(outcomes, rows_for(outcomes), rows_for(outcomes), {})
    assert report['reading'] == 'complete' and report['lines'][5] == ('met', {'right': 43, 'right by a ladder': 43, 'of': 44})


def test_line_5_refusals_alone_cannot_meet_it():
    """Two sound ladders and an unjustified refusal: right, and by a ladder. One sound ladder and two justified refusals: right, not by a ladder."""
    def kinds(number):
        return 'yes/no'
    outcomes = forty_four(kinds)
    for number in range(1, 21):                       # twenty cases: one ladder, two justified refusals
        outcomes[(number - 1) * 3 + 1] = outcome(f'case-{number}', 2, 'refusal')
        outcomes[(number - 1) * 3 + 2] = outcome(f'case-{number}', 3, 'refusal')
    outcomes[20 * 3 + 2] = outcome('case-21', 3, 'refusal')                               # one case: two ladders, an unjustified refusal
    reader = rows_for(outcomes, {('case-21', 3): {'N': 'fails'}})
    report = accounting.account(outcomes, reader, reader, {})
    assert report['lines'][5] == ('missed', {'right': 44, 'right by a ladder': 24, 'of': 44})
    assert report['lines'][4] == ('missed', [('case-21', 3)])


def test_no_ladder_at_all_leaves_lines_1_to_3_not_measured():
    outcomes = [outcome(f'case-{number}', pass_number, 'refusal') for number in range(1, 45) for pass_number in (1, 2, 3)]
    report = accounting.account(outcomes, rows_for(outcomes), rows_for(outcomes), {})
    assert all(report['lines'][number] == accounting.NOT_MEASURED for number in (1, 2, 3))
    assert report['lines'][4] == ('met', []) and report['lines'][5][1]['right by a ladder'] == 0


def test_every_send_refused_twice_is_no_reading():
    outcomes = [outcome(f'case-{number}', pass_number, 'refused twice') for number in range(1, 45) for pass_number in (1, 2, 3)]
    report = accounting.account(outcomes, {}, {}, {})
    assert report['dispute share'] == 'no reading' and report['reading'].startswith('no reading')
    assert all(report['lines'][number] == accounting.NOT_MEASURED for number in (1, 2, 3))
    assert report['lines'][4] == 'no refusal occurred'
    assert report['lines'][5] == ('missed', {'right': 0, 'right by a ladder': 0, 'of': 44})
    assert report['lines'][6]['direction'][0] == accounting.NOT_MEASURED and report['lines'][6]['due day'][0] == accounting.NOT_MEASURED


def test_the_dispute_share_is_counted_over_the_whole_reading_not_answer_by_answer():
    outcomes = forty_four()
    key = ('case-1', 1)
    disputed = {'Q': 'fails', 'O': 'fails', 'R': 'fails', 'D': 'fails'}                    # four of one answer's seven marks
    ruling = {key: {'marks': {mark: 'holds' for mark in disputed}}}
    report = accounting.account(outcomes, rows_for(outcomes, {key: disputed}), rows_for(outcomes), ruling)
    assert report['dispute share'] == (4, 132 * 7) and report['reading'] == 'complete'
    many = {(f'case-{number}', pass_number): disputed for number in range(1, 45) for pass_number in (1, 2, 3)}       # four of seven, everywhere
    rulings = {key: {'marks': {mark: 'holds' for mark in disputed}} for key in many}
    assert accounting.account(outcomes, rows_for(outcomes, many), rows_for(outcomes), rulings)['reading'].startswith('too disputed')


def test_line_6_direction_is_read_on_theses_whose_three_sends_are_company_figures_and_needs_three():
    def kinds(number):
        return 'company figure' if number <= 4 else 'yes/no'
    outcomes = forty_four(kinds)
    report = accounting.account(outcomes, rows_for(outcomes), rows_for(outcomes), {})
    assert report['lines'][6]['direction'] == ('met', {'theses': 4, 'direction differs': []})
    outcomes[2] = outcome('case-1', 3, 'company figure', favourable_end='higher')          # one thesis flips its favourable end
    assert accounting.account(outcomes, rows_for(outcomes), rows_for(outcomes), {})['lines'][6]['direction'] == ('missed', {'theses': 4, 'direction differs': ['case-1']})
    two = forty_four(lambda number: 'company figure' if number <= 2 else 'yes/no')
    assert accounting.account(two, rows_for(two), rows_for(two), {})['lines'][6]['direction'][0] == accounting.NOT_MEASURED


def test_line_6_two_company_figures_and_an_event_count_for_the_due_day_and_not_for_direction():
    outcomes = forty_four(lambda number: 'company figure' if number <= 4 else 'yes/no')
    outcomes[2] = outcome('case-1', 3, 'yes/no')
    line = accounting.account(outcomes, rows_for(outcomes), rows_for(outcomes), {})['lines'][6]
    assert line['direction'][1]['theses'] == 3 and line['due day'][1]['theses'] == 44 and line['shape differs across sends'] == ['case-1']


def test_line_6_the_due_day_is_the_same_in_nine_theses_of_ten_and_needs_twenty_theses():
    outcomes = forty_four()
    for number in range(1, 5):                        # four of 44 theses change their due day in one send: 40 of 44 the same, above nine in ten
        outcomes[(number - 1) * 3] = outcome(f'case-{number}', 1, 'yes/no', due_day='2027-06-30')
    assert accounting.account(outcomes, rows_for(outcomes), rows_for(outcomes), {})['lines'][6]['due day'] == ('met', {'theses': 44, 'same due day': 40})
    outcomes[4 * 3] = outcome('case-5', 1, 'yes/no', due_day='2027-06-30')                  # a fifth: 39 of 44, below nine in ten
    assert accounting.account(outcomes, rows_for(outcomes), rows_for(outcomes), {})['lines'][6]['due day'][0] == 'missed'
    few = [outcome(f'case-{number}', pass_number) for number in range(1, 20) for pass_number in (1, 2, 3)]
    assert accounting.account(few, rows_for(few), rows_for(few), {})['lines'][6]['due day'][0] == accounting.NOT_MEASURED


def test_the_shares_have_one_population_a_mark_and_g_and_b_are_counted_by_reader_with_no_single_value():
    outcomes = forty_four(lambda number: 'company figure' if number <= 2 else 'yes/no')
    outcomes[0] = outcome('case-1', 1, 'company figure', not_judged=2)
    reader_1 = rows_for(outcomes, {('case-1', 1): {'G': 'fails', 'why': 'unfair ranges', 'B': ['bet', 'not_a_bet']}, ('case-1', 2): {'G': 'not_assessable'}})
    report = accounting.account(outcomes, reader_1, rows_for(outcomes), {})
    assert report['shares']['Q'] == (132, 132) and report['shares']['Y'] == (6, 6) and report['shares']['F'] == (6, 6)
    assert report['shares']['N'] == 'none to count'
    assert report['shares']['G, reader 1'] == {'fails': 1, 'not_assessable': 1, 'holds': 4} and report['shares']['G, reader 2'] == {'holds': 6}
    assert report['shares']['B, reader 1'] == {'bet': 1, 'not_a_bet': 1}


def test_d409_an_event_takes_the_seven_ladder_marks_and_no_direction_mark():
    event = {'case': 'a', 'pass': 1, 'status': 'ladder', 'view': {'kind': 'asset'},
             'answer': {'ladder': {'event': {'happened': 'It happened.', 'ruled_out': None}, 'figure': None, 'due_day': '2027-01-31', 'not_judged': []}}}
    assert accounting.kind_of(event) == 'event' and accounting.marks_that_apply('event') == accounting.LADDER_MARKS
    assert accounting.row_problem(row(event), event) is None
    assert 'F is' in accounting.row_problem(row(event, F='holds'), event)


def test_two_third_readers_agree_on_a_mark_or_leave_it_unresolved_and_counted_both_ways():
    of_one = {'marks': {'Q': 'fails', 'R': 'fails', 'L': 'holds'}, 'W': {'reader 1': True, 'reader 2': True}}
    of_other = {'marks': {'Q': 'fails', 'R': 'holds', 'L': 'holds'}, 'W': {'reader 1': True, 'reader 2': False}}
    for_the_answer, unresolved = accounting.rulings_of_two(of_one, of_other, 'holds')
    against_it, unresolved_again = accounting.rulings_of_two(of_one, of_other, 'fails')
    assert unresolved == unresolved_again == ['R', 'W of reader 2']
    assert for_the_answer == {'marks': {'L': 'holds', 'Q': 'fails', 'R': 'holds'}, 'W': {'reader 1': True, 'reader 2': False}}
    assert against_it == {'marks': {'L': 'holds', 'Q': 'fails', 'R': 'fails'}, 'W': {'reader 1': True, 'reader 2': True}}


def test_a_point_only_one_third_reader_ruled_on_is_a_missing_ruling_not_a_value():
    outcomes = forty_four()
    key = ('case-3', 1)
    reader_1, reader_2 = rows_for(outcomes, {key: {'Q': 'fails'}}), rows_for(outcomes)
    resolved, unresolved = accounting.rulings_of_two({'marks': {'Q': 'fails'}}, {'marks': {}}, 'holds')
    assert resolved == {'marks': {}, 'W': {}} and unresolved == []
    report = accounting.account(outcomes, reader_1, reader_2, {key: resolved})
    assert report['missing rulings'] == [(key, 'Q')] and report['lines'][1] == accounting.NOT_MEASURED

