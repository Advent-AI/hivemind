"""06-views ladder rule 5 (only this year and next year open), counted in the company's own fiscal years (D243, the
extraction standard's known defect B17): NVIDIA's FY2028 is next year in July 2026, a calendar 2028 total is not."""
import json
from pathlib import Path

from hivemind import extraction, universe

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / 'tests/fixtures/fiscal-year-horizon-2026-07.json').read_text())['cases']


def year_refusals(case):
    answer = {'evidence': [], 'candidates': [case['candidate']], 'new_groups': []}
    item = {'input_id': case['input_id'], 'publication_day': case['publication_day']}
    _, _, dropped = extraction.sift(answer, item, '', set(), universe.load(ROOT / 'poc/universe.json'), english=True)
    return [reason for _, reason in dropped if 'beyond next year' in reason]


def test_next_fiscal_year_is_not_refused_as_the_year_after_next():
    nvidia_fy2028 = CASES[0]
    assert nvidia_fy2028['candidate']['year'] == 'FY2028'
    assert year_refusals(nvidia_fy2028) == []


def test_a_calendar_year_after_next_is_still_refused():
    capex_2028 = CASES[1]
    assert capex_2028['candidate']['year'] == '2028'
    assert len(year_refusals(capex_2028)) == 1


def test_a_two_digit_fiscal_year_counts_like_the_four_digit_one():
    """The year forms are the universe's (parse_year): FY29 is FY2029, two fiscal years out for NVIDIA in July 2026 (2026-10-30 review)."""
    uni = universe.load(ROOT / 'poc/universe.json')
    assert extraction.beyond_next_year('FY29', '2026-07-02', 'NVDA', uni) is True
    assert extraction.beyond_next_year('FY28', '2026-07-02', 'NVDA', uni) is False

