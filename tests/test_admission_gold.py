"""D188: the extraction gold scorer reads a ledger and the gold's typed keys; fail when a must-open thesis or an evidence
target is missing, partial when a must-not-open thesis was created, full otherwise, "not processed" when the run never
saw the item. Real ledger on a temporary path."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from hivemind import universe  # noqa: E402
from hivemind.views import store  # noqa: E402
import score_admission_gold as scorer  # noqa: E402

UNIVERSE = universe.load(os.path.join(ROOT, 'poc', 'universe.json'))
ITEM = 'truenorth:transcript:NVDA:2026-02-25'
RUNGS = [{'label': 'Strongly bullish', 'condition': '>=80', 'lo': 80, 'hi': None}, {'label': 'Bullish', 'condition': '77-80', 'lo': 77, 'hi': 80},
         {'label': 'Neutral', 'condition': '73-77', 'lo': 73, 'hi': 77}, {'label': 'Bearish', 'condition': '70-73', 'lo': 70, 'hi': 73},
         {'label': 'Strongly bearish', 'condition': '<70', 'lo': None, 'hi': 70}]
CASE = {'id': 'T01', 'title': 'gross margin guidance', 'items': [ITEM], 'window': 'seed', 'passage': 'mid-70s', 'source': 'test',
        'must_open': [{'gist': 'FY2027 non-GAAP gross margin', 'object': 'NVDA', 'measure': 'gross_margin', 'year': 'FY2027', 'event_type': 'n/a', 'scope_regex': '',
                       'opens_as': 'main_driver', 'alternatives': []}],
        'must_not_open': [{'gist': 'FY2027 tax rate', 'object': 'NVDA', 'measure': 'tax_rate', 'year': 'FY2027', 'event_type': 'n/a', 'scope_regex': ''}],
        'evidence_targets': [{'quote_regex': 'mid-70s', 'target': 'self:FY2027 non-GAAP gross margin'}],
        'must_not_link': [], 'system_v23': {'views': [], 'score': 'partial', 'why': 'test'}}


def ledger(tmp_path, *, with_tax=True, with_link=True, processed=True):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    seq = 5
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='company', kind='asset', looks_at='FY2027 gross margin',
                      question='Where will NVIDIA FY2027 non-GAAP gross margin land?', due_day='2027-02-24', year='FY2027', rungs=RUNGS, seq=seq, input_id=ITEM, created_at='2026-02-25T22:00:00Z')
    store.add_key(conn, 'v1', {'measure': 'gross_margin', 'scope': '', 'period_start': '2026-02-01', 'period_end': '2027-01-31', 'basis': 'non_GAAP', 'unit': 'percent', 'event_type': 'n/a'}, seq)
    if with_tax:
        store.create_view(conn, view_id='v2', object_id='NVDA', object_kind='company', kind='asset', looks_at='FY2027 tax rate', question='tax?', due_day='2027-02-24', year='FY2027',
                          rungs=RUNGS, seq=seq, input_id=ITEM, created_at='2026-02-25T22:00:00Z')
        store.add_key(conn, 'v2', {'measure': 'tax_rate', 'scope': '', 'period_start': '2026-02-01', 'period_end': '2027-01-31', 'basis': 'non_GAAP', 'unit': 'percent', 'event_type': 'n/a'}, seq)
    store.add_evidence(conn, evidence_id='e1', quote='For the full year, we continue to see gross margins in the mid-70s.', one_line='FY27 GM mid-70s', speaker='CFO',
                       original_who='NVIDIA', original_day='2026-02-25', tier='party_statement', event_time='', seq=seq, input_id=ITEM)
    store.add_source(conn, 'e1', ITEM, 'T4', '2026-02-25', 'p1', seq)
    if with_link:
        store.link(conn, 'e1', 'v1', seq)
    if processed:
        handover = {'evidence': [], 'candidates': [{'id': 'c1', 'object': 'NVDA', 'measure': 'gross_margin', 'year': 'FY2027', 'opens_as': 'main_driver', 'folds_into': ''}], 'dropped': [], 'new_groups': []}
        store.insert(conn, 'handovers', input_id=ITEM, seq=seq, handover_json=json.dumps(handover))
    conn.commit()
    return conn


def test_partial_when_the_must_open_exists_and_a_must_not_open_was_created(tmp_path):
    result = scorer.score_case(ledger(tmp_path), CASE, UNIVERSE)
    assert result['score'] == 'partial' and result['extra_opened'] == ['FY2027 tax rate'] and result['missing_must_open'] == [] and result['missing_links'] == []


def test_full_when_only_the_must_open_exists(tmp_path):
    assert scorer.score_case(ledger(tmp_path, with_tax=False), CASE, UNIVERSE)['score'] == 'full'


def test_fail_when_the_evidence_target_is_not_linked(tmp_path):
    result = scorer.score_case(ledger(tmp_path, with_tax=False, with_link=False), CASE, UNIVERSE)
    assert result['score'] == 'fail' and result['missing_links'] == ['mid-70s'] and result['missing_must_open'] == ['FY2027 non-GAAP gross margin']


def test_not_processed_when_the_item_never_reached_a_handover(tmp_path):
    assert scorer.score_case(ledger(tmp_path, processed=False), CASE, UNIVERSE)['score'] == 'not processed'


def test_census_counts_theses_by_object_measure_and_admission_reason(tmp_path):
    census = scorer.census(ledger(tmp_path))
    assert census['theses'] == 2 and census['by_object'] == {'NVDA': 2} and census['by_measure'] == {'gross_margin': 1, 'tax_rate': 1}
    assert census['by_opens_as'] == {'main_driver': 1} and census['folds_into_named'] == 0


def test_census_counts_duplicate_keys(tmp_path):
    conn = ledger(tmp_path, with_tax=False)
    store.create_view(conn, view_id='v9', object_id='NVDA', object_kind='company', kind='asset', looks_at='FY2027 gross margin again', question='again?', due_day='2027-02-24', year='FY2027',
                      rungs=RUNGS, seq=9, input_id='other', created_at='2026-03-01T00:00:00Z')
    store.add_key(conn, 'v9', {'measure': 'gross_margin', 'scope': 'company', 'period_start': '2026-02-01', 'period_end': '2027-01-31', 'basis': 'non_GAAP', 'unit': 'percent', 'event_type': 'n/a'}, 9)
    conn.commit()
    assert scorer.census(conn)['duplicate_keys'] == {'NVDA gross_margin FY2027': 2}       # the same object, quantity and year twice, whatever the scope wording (log row 43: scope is wording)


def test_an_event_thesis_matches_its_key_whatever_year_its_check_day_falls_in(tmp_path):
    """D185: an obligation's check day is the model's own (up to 18 months), so the gold names the event, not its year."""
    conn = ledger(tmp_path, with_tax=False)
    store.create_view(conn, view_id='v7', object_id='NVDA', object_kind='company', kind='asset', looks_at='Ohio guarantee',
                      question='Will NVIDIA document a binding guarantee for the Ohio campus by July 27, 2027?', due_day='2027-07-27', year='2027',
                      rungs=[{'label': 'Yes', 'condition': 'documented', 'lo': None, 'hi': None}, {'label': 'No', 'condition': 'not documented', 'lo': None, 'hi': None}], seq=7, input_id='ohio', created_at='2026-07-27T00:00:00Z')
    store.add_key(conn, 'v7', {'measure': 'event', 'scope': 'Ohio guarantee', 'period_start': '2026-01-01', 'period_end': '2027-07-27', 'basis': 'n/a', 'unit': 'n/a', 'event_type': 'deal_close'}, 7)
    conn.commit()
    key = {'gist': 'Ohio guarantee', 'object': 'NVDA', 'measure': 'event', 'year': '2026', 'event_type': 'deal_close', 'scope_regex': 'ohio', 'opens_as': 'binding_obligation', 'alternatives': []}
    assert scorer.views_with_key(conn, key, UNIVERSE) == ['v7']
    assert scorer.views_with_key(conn, dict(key, event_type='licence'), UNIVERSE) == []


def test_a_forbidden_link_costs_the_full_score(tmp_path):
    conn = ledger(tmp_path, with_tax=False)
    case = dict(CASE, must_not_link=[{'quote_regex': 'mid-70s', 'target': 'self:FY2027 non-GAAP gross margin'}])      # the one link present is also the forbidden one
    result = scorer.score_case(conn, case, UNIVERSE)
    assert result['forbidden_links'] == ['mid-70s'] and result['score'] == 'partial'


def test_a_missing_required_quote_fails_even_when_the_thesis_has_another_link(tmp_path):
    conn = ledger(tmp_path, with_tax=False)
    case = dict(CASE, evidence_targets=CASE['evidence_targets'] + [{'quote_regex': 'low-40s', 'target': 'self:FY2027 non-GAAP gross margin'}])
    result = scorer.score_case(conn, case, UNIVERSE)
    assert result['missing_must_open'] == [] and result['missing_links'] == ['low-40s'] and result['score'] == 'fail'


def test_census_counts_a_named_fold_target(tmp_path):
    conn = ledger(tmp_path, with_tax=False)
    handover = {'evidence': [], 'candidates': [{'id': 'c1', 'object': 'NVDA', 'measure': 'segment_revenue', 'year': 'FY2027', 'opens_as': 'main_driver', 'folds_into': 'v1'}], 'dropped': [], 'new_groups': []}
    store.insert(conn, 'handovers', input_id='other', seq=8, handover_json=json.dumps(handover))
    conn.commit()
    assert scorer.census(conn)['folds_into_named'] == 1


def test_the_report_counts_only_processed_cases_as_judged(tmp_path):
    conn = ledger(tmp_path, with_tax=False)
    results = [scorer.score_case(conn, CASE, UNIVERSE), scorer.score_case(conn, dict(CASE, id='T02', items=['never:seen']), UNIVERSE)]
    text = scorer.render({'version': 'test', 'cases': [CASE, dict(CASE, id='T02')]}, results, scorer.census(conn), 'ledger')
    assert 'Cases judged: 1' in text and 'not processed 1' in text
