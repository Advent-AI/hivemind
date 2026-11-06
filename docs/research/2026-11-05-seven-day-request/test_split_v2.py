"""Split POC version 2 (2026-11-05): source quotes as production's sift reads them, subjects chosen from the listed ids, the D197 key on
a shared quantity, the year limit, the version-2 new-question schema and the first-N manifest. Run with an explicit path:
PYTHONPATH=src python3 -m pytest -c /dev/null docs/research/2026-11-05-seven-day-request/test_split_v2.py"""
import json, sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / 'docs/research/2026-11-05-parallel-refinement'), str(ROOT / 'src')]
import split_seven_day_poc as p  # noqa: E402
from hivemind import universe  # noqa: E402

UNI = universe.load(str(ROOT / 'poc/universe.json'))
SOURCE = ("The company's supply and capacity commitments increased from $119 billion at the end of the first quarter to $279 billion at "
          "the end of the second quarter of fiscal 2027. Shipments fell 21% year‑over‑year on low‑end models.")


def test_the_subject_company_written_for_the_company_is_the_source_passage_only_with_its_name():
    # stopped run, seq 1246: B wrote "Nvidia's" for "The company's"; production's sift passes the subject names (D266), the split did not
    quote = "Nvidia's supply and capacity commitments increased from $119 billion at the end of the first quarter to $279 billion at the end of the second quarter of fiscal 2027."
    assert p.source_quote(quote, SOURCE) is None
    kept = p.source_quote(quote, SOURCE, ['NVIDIA'])
    assert kept and kept in SOURCE and kept.startswith('supply and capacity commitments')
    assert p.source_quote(quote.replace('$279', '$297'), SOURCE, ['NVIDIA']) is None


def test_a_hyphen_glyph_compares_as_a_hyphen_and_the_stored_passage_keeps_the_source_glyph():
    kept = p.source_quote('Shipments fell 21% year-over-year on low-end models.', SOURCE)
    assert kept == 'Shipments fell 21% year‑over‑year on low‑end models.'


def test_the_subject_is_a_listed_id_and_its_kind_follows_it():
    q = {'question': 'q'}
    assert p.chosen_subject({'object': 'fed-policy-rate'}, q, UNI) == ('fed-policy-rate', 'theme')
    assert p.chosen_subject({'object': 'NVDA'}, q, UNI) == ('NVDA', 'asset')
    assert p.chosen_subject({'object': 'new', 'new_subject': 'OpenAI', 'new_subject_kind': 'company'}, q, UNI) == ('OpenAI', 'asset')
    assert p.chosen_subject({'object': 'Federal Reserve benchmark interest rate', 'kind': 'asset'}, q, UNI)[1] == 'asset'   # an earlier run's answer


def test_only_a_theme_quantity_summed_over_a_calendar_year_carries_the_code_owned_key():
    key = p.shared_key({'shared_measure': 'spend_total', 'unit': 'USD', 'year': '2027'}, 'theme')
    assert (key['measure'], key['period_start'], key['period_end'], key['opens_as']) == ('spend_total', '2027-01-01', '2027-12-31', 'shared_quantity')
    assert p.shared_key({'shared_measure': 'spend_total', 'unit': 'USD', 'year': '2027'}, 'asset') == {}
    assert p.shared_key({'shared_measure': 'none', 'unit': 'percent', 'year': '2026'}, 'theme') == {}
    assert p.shared_key({'shared_measure': 'spend_total', 'unit': 'USD', 'year': 'FY2027'}, 'theme') == {}


def handover(question, year, quote, rungs):
    item = {'input_id': 'gnews:test', 'publication_day': '2026-08-30', 'text': SOURCE, 'object_identifiers': [{'value': 'NVDA'}]}
    a = {'questions': [{'question': question, 'why_it_matters': 'w', 'closest_existing_question': 'none', 'what_separates_it': 's',
                        'how_and_when_to_check': 'annual report', 'evidence': [{'quote': quote, 'what_it_shows': 'x', 'original_speaker': 'y'}]}]}
    meta = {'candidates': {'c1': {'object': 'NVDA', 'new_subject': '', 'new_subject_kind': 'none', 'shared_measure': 'none', 'unit': 'percent', 'year': year,
                                  'due_day': '', 'date_basis': 'unknown', 'date_provenance': '', 'rungs': rungs}},
            'evidence': {'e1': {'speaker': 's', 'original_who': 'o', 'original_day': '', 'tier': 'fact', 'event_time': ''}}}
    return p.build_handover(item, [], UNI, a, {'evidence': []}, meta)


NUMERIC = [{'label': l, 'condition': l, 'lo': lo, 'hi': hi} for l, lo, hi in
           [('Strongly bullish', 90, None), ('Bullish', 85, 90), ('Neutral', 80, 85), ('Bearish', 75, 80), ('Strongly bearish', None, 75)]]


def test_a_figure_for_the_year_after_next_is_not_opened_and_its_passages_leave_with_it():
    h = handover('What share will NVIDIA hold in 2028?', '2028', 'Shipments fell 21% year-over-year on low-end models.', NUMERIC)
    assert h.candidates == [] and h.evidence == [] and 'beyond next year' in h.dropped[0][1]
    kept = handover('What share will NVIDIA hold in FY2028?', 'FY2028', 'Shipments fell 21% year-over-year on low-end models.', NUMERIC)
    assert len(kept.candidates) == 1 and len(kept.candidates[0]['rungs']) == 5


def test_a_question_whose_only_passage_is_not_in_the_article_is_dropped_with_its_reason():
    h = handover('What share will NVIDIA hold in FY2028?', 'FY2028', 'A sentence the article does not contain at all.', [])
    assert h.candidates == [] and ('c1', 'candidate without surviving evidence') in h.dropped


def test_the_new_question_schema_names_the_closest_shown_question_and_leaves_the_quote_undescribed():
    schema = p.a_question_schema(['v5', 'v85'])
    q = schema['properties']['questions']['items']
    assert q['properties']['closest_existing_question']['enum'] == ['none', 'v5', 'v85'] and 'why_not_already_covered' not in q['properties']
    assert q['properties']['evidence']['minItems'] == 1
    # the "copied character for character" description made the model copy article text into the question field (4 of 6 sends)
    assert 'description' not in q['properties']['evidence']['items']['properties']['quote']


def test_record_preparation_lists_every_subject_and_accepts_only_those_ids_or_new():
    a = {'questions': [{'question': 'q?', 'why_it_matters': 'w', 'how_and_when_to_check': 'c', 'evidence': [{'quote': 'x', 'what_it_shows': 'y', 'original_speaker': 'z'}]}]}
    system, user, schema, _ = p.metadata_request({'text': SOURCE}, a, UNI)
    assert '  - ai-capex: AI capital spending (theme)' in user and '  - TSM: Taiwan Semiconductor Manufacturing (company)' in user
    enum = schema['$defs']['candidate']['properties']['object']['enum']
    assert enum[-1] == 'new' and set(enum[:-1]) == set(UNI.companies) | set(UNI.themes)
    assert 'kind' not in schema['$defs']['candidate']['properties']


def test_the_first_hundred_manifest_is_the_stopped_runs_first_hundred_rows_over_three_days():
    stopped = json.loads((ROOT / 'poc/data/split-fresh-seven-day-matching-v4-2026-11-05/manifest.json').read_text())
    m = p.select_manifest(None, 100)
    assert [r['id'] for r in m['input_rows']] == [r['id'] for r in stopped['input_rows'][:100]]
    assert m['days'] == ['2026-08-29', '2026-08-30', '2026-08-31'] and m['limit'] == 100 and m['config'] == 'poc/config/poc-split-v2.json'


def test_a_quote_that_differs_only_by_punctuation_is_the_source_passage_whatever_its_length():
    # first split-v2 run, seq 1223: a seven-word fragment with an added full stop was refused although its words are the article's
    text = "Nvidia's latest quarterly report—$96.2 billion in revenue, up 106% year-over-year—looks like a triumph."
    assert p.source_quote('$96.2 billion in revenue, up 106% year-over-year.', text) == '$96.2 billion in revenue, up 106% year-over-year'
    assert p.source_quote('$96.2 billion in revenue, up 160% year-over-year.', text) is None


def test_a_space_between_a_number_and_its_percent_sign_is_the_same_text_and_the_source_spacing_is_stored():
    # final split-v2 run, seq 1280: the filing writes "28.1 %"; the model wrote "28.1%"
    text = 'For the fiscal year ended June 30, 2026, sales to one customer represented 28.1 % of total net sales. Other text.'
    kept = p.source_quote('For the fiscal year ended June 30, 2026, sales to one customer represented 28.1% of total net sales.', text)
    assert kept == 'For the fiscal year ended June 30, 2026, sales to one customer represented 28.1 % of total net sales.'
    assert p.source_quote('For the fiscal year ended June 30, 2026, sales to one customer represented 21.8% of total net sales.', text) is None


def test_a_quote_that_copies_a_passage_and_runs_on_keeps_only_the_copied_passage():
    # final split-v2 run, seq 1243; production's sift keeps the copied passage (D266)
    text = 'Now, according to reports, Nvidia is slated to buy the platform for $12.9 billion. More sports news follows here.'
    kept = p.source_quote('Now, according to reports, Nvidia is slated to buy the platform for $12.9 billion. He also owns a stake worth more.', text)
    assert kept == 'Now, according to reports, Nvidia is slated to buy the platform for $12.9 billion.'


def test_a_fiscal_year_named_in_the_question_sets_the_year_limit_when_preparation_gives_a_bare_year():
    # confirmation run, seq 1207: "FY2028 total revenue growth" prepared with year "2028" was dropped as calendar 2028
    kept = handover('What year-over-year total revenue growth will NVIDIA report for FY2028?', '2028', 'Shipments fell 21% year-over-year on low-end models.', NUMERIC)
    assert len(kept.candidates) == 1
    assert p.question_year('What share will NVIDIA hold in calendar 2028?', '2028') == '2028'
