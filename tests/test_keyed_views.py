"""Keyed views (docs/poc/keyed-views-plan.md, D153): the reference list and the bounds check in the sift (2.4, 2.2), the key
stored with the view, key-first matching that never merges two quantities (2.5), and claims judged on numeric bounds.
Real ledger on a temporary path; the universe file the pipeline reads; no model."""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import extraction, service, universe  # noqa: E402
from hivemind.views import matching, store, writing  # noqa: E402

UNIVERSE = universe.load(os.path.join(ROOT, 'poc', 'universe.json'))
ITEM = {'input_id': 'test:nvda-call', 'publication_day': '2026-05-20', 'category': 'T1', 'publisher_type': 'issuer', 'title': 'call',
        'object_identifiers': [{'value': 'NVDA'}]}
TEXT = '数据中心收入指引为全年三千亿美元以上。GeForce NOW 八月上新二十六款游戏。毛利率指引为七十三到七十五。'
RUNGS = [{'label': 'Strongly bullish', 'condition': '3500亿美元及以上', 'lo': 350e9, 'hi': None}, {'label': 'Bullish', 'condition': '3000亿至3500亿', 'lo': 300e9, 'hi': 350e9},
         {'label': 'Neutral', 'condition': '2500亿至3000亿', 'lo': 250e9, 'hi': 300e9}, {'label': 'Bearish', 'condition': '2000亿至2500亿', 'lo': 200e9, 'hi': 250e9},
         {'label': 'Strongly bearish', 'condition': '低于2000亿', 'lo': None, 'hi': 200e9}]
KEY = {'measure': 'segment_revenue', 'scope': 'Data Center', 'period_start': '2026-02-01', 'period_end': '2027-01-31', 'basis': 'n/a', 'unit': 'USD', 'event_type': 'n/a'}


def candidate(cid, **over):
    base = {'id': cid, 'object': 'NVDA', 'kind': 'asset', 'looks_at': 'FY2027 数据中心收入', 'question': 'FY2027 数据中心收入多少？', 'rungs': RUNGS,
            'due_day': '2027-02-25', 'year': 'FY2027', 'evidence_ids': ['e1'], 'key_version': 2, **KEY}
    base.update(over)
    return base


EVIDENCE = [{'id': 'e1', 'quote': '数据中心收入指引为全年三千亿美元以上', 'one_line': '数据中心收入指引三千亿以上', 'speaker': 'CFO', 'original_who': 'NVIDIA', 'original_day': '2026-05-20', 'tier': 'party_statement', 'event_time': '', 'links': ['c1']},
            {'id': 'e2', 'quote': 'GeForce NOW 八月上新二十六款游戏', 'one_line': 'GeForce NOW 新游戏', 'speaker': '', 'original_who': 'NVIDIA', 'original_day': '2026-05-20', 'tier': 'fact', 'event_time': '', 'links': ['c2']}]


def test_reference_list_does_not_veto_model_candidates():
    trivia = candidate('c2', measure='event', scope='GeForce NOW', event_type='launch', looks_at='GeForce NOW 八月新游戏', question='八月是否上新 26 款？', evidence_ids=['e2'],
                       rungs=[{'label': 'Yes', 'condition': '是', 'lo': None, 'hi': None}, {'label': 'No', 'condition': '否', 'lo': None, 'hi': None}], due_day='2026-08-31', year='2026')
    other = candidate('c3', measure='other', scope='', evidence_ids=['e1'])
    evidence, kept, dropped = extraction.sift({'candidates': [candidate('c1'), trivia, other], 'evidence': EVIDENCE}, ITEM, TEXT, set(), UNIVERSE)
    assert [c['id'] for c in kept] == ['c1', 'c2', 'c3']
    assert not any(reason.startswith('watch:') for _, reason in dropped)
    # a candidate written before keys (no measure) is not gated
    legacy = {k: v for k, v in candidate('c4').items() if k not in KEY}
    legacy['rungs'] = [{'label': r['label'], 'condition': r['condition']} for r in RUNGS]
    legacy_evidence = [dict(EVIDENCE[0], links=['c4'])]
    assert [c['id'] for c in extraction.sift({'candidates': [legacy], 'evidence': legacy_evidence}, ITEM, TEXT, set(), UNIVERSE)[1]] == ['c4']


def test_rung_bounds_must_partition_the_line():
    assert extraction.check_bounds(RUNGS) is None
    gap = [dict(r) for r in RUNGS]
    gap[1]['lo'] = 310e9                                   # 300–310 belongs to no rung
    assert extraction.check_bounds(gap) == 'rung bounds overlap or leave a gap'
    closed_top = [dict(r) for r in RUNGS]
    closed_top[0]['hi'] = 500e9
    assert extraction.check_bounds(closed_top) == 'the top rung must be open above'
    _, kept, dropped = extraction.sift({'candidates': [candidate('c1', rungs=gap)], 'evidence': EVIDENCE}, ITEM, TEXT, set(), UNIVERSE)
    assert kept == [] and dropped[0][1].startswith('candidate ladder bounds')


def test_the_key_and_the_bounds_are_written_with_the_view_and_judge_a_claim(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    handover = extraction.Handover(EVIDENCE[:1], [candidate('c1')], [], 0, '', False, 0.0)
    checked = matching.Checked({'c1': ('new', None, [])}, {}, [], {})
    written = writing.write(conn, UNIVERSE, 1, ITEM, handover, checked, {})
    view_id = written.new_views['c1']
    assert store.view_key(conn, view_id)['measure'] == 'segment_revenue' and store.view_key(conn, view_id)['scope_key'] == 'data center'
    assert [(r['lo'], r['hi']) for r in store.rungs_of(conn, view_id)][:2] == [(350e9, None), (300e9, 350e9)]
    bands, problem = service.ladder_bands(store.rungs_of(conn, view_id))
    assert problem is None and bands[2] == (300e9, True, 350e9, False)       # from the numbers, not from the prose
    assert store.open_views_with_key(conn, 'NVDA', 'segment_revenue', 'data center', '2026-02-01', '2027-01-31') == [view_id]
    assert store.open_views_with_key(conn, 'NVDA', 'segment_revenue', 'data center', '2027-02-01', '2028-01-31') == []   # the next year does not overlap


def test_matching_compares_a_keyed_candidate_only_with_views_of_its_key_and_never_merges_two_quantities(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    # an open data-center view (same key as c1) and an open total-revenue view
    first = extraction.Handover(EVIDENCE[:1], [candidate('c1')], [], 0, '', False, 0.0)
    written = writing.write(conn, UNIVERSE, 1, ITEM, first, matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {})
    dc = written.new_views['c1']
    total = candidate('c9', measure='total_revenue', scope='', looks_at='FY2027 总收入', question='FY2027 总收入多少？')
    written2 = writing.write(conn, UNIVERSE, 2, ITEM, extraction.Handover(EVIDENCE[:1], [total], [], 0, '', False, 0.0), matching.Checked({'c9': ('new', None, [])}, {}, [], {}), {})
    tot = written2.new_views['c9']
    # a new data-center candidate: its list is the data-center view alone
    later = extraction.Handover(EVIDENCE[:1], [candidate('c1', looks_at='FY2027 数据中心全年收入（美元）')], [], 0, '', False, 0.0)
    lists = matching.build_lists(conn, later, store.views_for_prompt(conn, ['NVDA']), 10)
    assert lists.candidate_lists['c1'] == [dc]
    # the model tries to merge it into total revenue: the key refuses, it opens as a new view, the note says so
    decision = {'candidates': [{'id': 'c1', 'outcome': 'merge', 'target_view_id': tot, 'reason': 'same company', 'dependencies': []}], 'evidence': []}
    checked = matching.check(conn, UNIVERSE, decision, later.candidates, later.evidence, lists, store.views_for_prompt(conn, ['NVDA']))
    assert checked.refusals == [] and checked.outcomes['c1'][0] == 'new' and 'refused by key' in checked.notes[0]
    # merging into the view of the same key is accepted as before
    same = {'candidates': [{'id': 'c1', 'outcome': 'merge', 'target_view_id': dc, 'reason': 'same quantity', 'dependencies': []}], 'evidence': []}
    assert matching.check(conn, UNIVERSE, same, later.candidates, later.evidence, lists, store.views_for_prompt(conn, ['NVDA'])).outcomes['c1'] == ('merge', dc, [])


def test_code_owns_the_scope_spelling_and_the_fiscal_period():
    # T2 (2026-10-25): the tax rate opened four times with scopes 'GAAP', 'GAAP tax rate', 'non-GAAP tax rate'; Compute & Networking
    # FY2027 was written as 2027-02..2028-01. A scope-less measure carries no scope; a watched scope takes the list's spelling;
    # a company's yearly number takes its fiscal span from the universe, whatever dates the model wrote.
    sloppy = candidate('c1', measure='tax_rate', scope='GAAP tax rate', basis='GAAP', period_start='2027-02-01', period_end='2028-01-31', looks_at='FY2027 GAAP 税率', question='FY2027 GAAP 税率多少？',
                       rungs=[dict(r, lo=(None if r['lo'] is None else r['lo'] / 1e10), hi=(None if r['hi'] is None else r['hi'] / 1e10)) for r in RUNGS])
    _, kept, _ = extraction.sift({'candidates': [sloppy], 'evidence': EVIDENCE}, ITEM, TEXT, set(), UNIVERSE)
    assert kept[0]['scope'] == '' and kept[0]['basis'] == 'GAAP' and (kept[0]['period_start'], kept[0]['period_end']) == ('2026-02-01', '2027-01-31')
    rubin = candidate('c2', measure='event', scope='rubin', event_type='shipment', year='2026', period_start='2026-01-01', period_end='2026-12-31',
                      rungs=[{'label': 'Yes', 'condition': '是', 'lo': None, 'hi': None}, {'label': 'No', 'condition': '否', 'lo': None, 'hi': None}], due_day='2026-12-31')
    _, kept, _ = extraction.sift({'candidates': [rubin], 'evidence': [dict(EVIDENCE[0], links=['c2'])]}, ITEM, TEXT, set(), UNIVERSE)
    assert kept[0]['scope'] == 'Rubin'                                       # the watch list's spelling, not the model's
    assert UNIVERSE.fiscal_period('NVDA', 'FY2027') == ('2026-02-01', '2027-01-31') and UNIVERSE.fiscal_period('MSFT', '2027') == ('2026-07-01', '2027-06-30')
    assert UNIVERSE.fiscal_period('ai-capex', '2026') == ('2026-01-01', '2026-12-31') and UNIVERSE.fiscal_period('NVDA', '') is None


def test_a_basis_of_n_a_matches_either_basis_and_gaap_never_matches_non_gaap(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    tax = candidate('c1', measure='tax_rate', scope='', basis='n/a', looks_at='FY2027 全年税率', question='FY2027 税率？')
    written = writing.write(conn, UNIVERSE, 1, ITEM, extraction.Handover(EVIDENCE[:1], [tax], [], 0, '', False, 0.0), matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {})
    v = written.new_views['c1']
    assert store.open_views_with_key(conn, 'NVDA', 'tax_rate', '', '2026-02-01', '2027-01-31', 'GAAP') == [v]
    gaap = candidate('c2', measure='tax_rate', scope='', basis='GAAP', looks_at='FY2027 GAAP 税率', question='GAAP 税率？')
    written2 = writing.write(conn, UNIVERSE, 2, ITEM, extraction.Handover(EVIDENCE[:1], [gaap], [], 0, '', False, 0.0), matching.Checked({'c2': ('new', None, [])}, {}, [], {}), {})
    g = written2.new_views['c2']
    assert store.open_views_with_key(conn, 'NVDA', 'tax_rate', '', '2026-02-01', '2027-01-31', 'non_GAAP') == [v]      # the GAAP view is another quantity
    later = extraction.Handover(EVIDENCE[:1], [candidate('c3', measure='tax_rate', scope='', basis='non_GAAP')], [], 0, '', False, 0.0)
    lists = matching.build_lists(conn, later, [], 10)
    decision = {'candidates': [{'id': 'c3', 'outcome': 'merge', 'target_view_id': g, 'reason': 'tax', 'dependencies': []}], 'evidence': []}
    assert matching.check(conn, UNIVERSE, decision, later.candidates, later.evidence, matching.Lists({'c3': [g, v]}, {}), []).outcomes['c3'][0] == 'new'


def test_reference_aliases_do_not_authorize_scope_replacement():
    # D155: an alias is a search hint, not authority to replace a narrower or broader scope.
    assert UNIVERSE.canonical_scope('ai-capex', 'spend_total', 'top 5 cloud providers and hyperscalers CapEx') == 'top 5 cloud providers and hyperscalers CapEx'
    assert UNIVERSE.canonical_scope('NVDA', 'event', 'H200 China', 'licence') == 'H200 China'


def test_a_level_and_a_growth_rate_of_the_same_measure_are_two_quantities(tmp_path):
    # T0 keying (2026-10-25): Microsoft's FY2027 revenue (USD) and its growth rate (percent) collided on the key without the unit
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    level = candidate('c1', measure='total_revenue', scope='', unit='USD', looks_at='FY2027 总收入', question='总收入？')
    written = writing.write(conn, UNIVERSE, 1, ITEM, extraction.Handover(EVIDENCE[:1], [level], [], 0, '', False, 0.0), matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {})
    v = written.new_views['c1']
    assert store.open_views_with_key(conn, 'NVDA', 'total_revenue', '', '2026-02-01', '2027-01-31', 'n/a', 'percent') == []
    assert store.open_views_with_key(conn, 'NVDA', 'total_revenue', '', '2026-02-01', '2027-01-31', 'n/a', 'USD') == [v]
    growth = extraction.Handover(EVIDENCE[:1], [candidate('c2', measure='total_revenue', scope='', unit='percent', looks_at='FY2027 总收入增速', question='增速？')], [], 0, '', False, 0.0)
    decision = {'candidates': [{'id': 'c2', 'outcome': 'merge', 'target_view_id': v, 'reason': 'revenue', 'dependencies': []}], 'evidence': []}
    assert matching.check(conn, UNIVERSE, decision, growth.candidates, growth.evidence, matching.Lists({'c2': [v]}, {}), []).outcomes['c2'][0] == 'new'


def test_a_code_owned_key_decides_identity_and_another_period_never_merges(tmp_path):
    # T2c (2026-10-25): the model merged a same-key candidate in one sample and opened it anew in the next; with a scope the
    # watch list spelled (or none), the key is code's and one open twin is the same view. A candidate of another period is never 归入.
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    first = extraction.Handover(EVIDENCE[:1], [candidate('c1', scope_source='watch')], [], 0, '', False, 0.0)
    dc = writing.write(conn, UNIVERSE, 1, ITEM, first, matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {}).new_views['c1']
    again = extraction.Handover(EVIDENCE[:1], [candidate('c1', scope_source='watch', looks_at='FY2027 数据中心分部全年收入')], [], 0, '', False, 0.0)
    lists = matching.build_lists(conn, again, [], 10)
    says_new = {'candidates': [{'id': 'c1', 'outcome': 'new', 'target_view_id': '', 'reason': 'different wording', 'dependencies': []}], 'evidence': []}
    checked = matching.check(conn, UNIVERSE, says_new, again.candidates, again.evidence, lists, [])
    assert checked.outcomes['c1'] == ('merge', dc, []) and 'merged into' in checked.notes[0]
    # a model-written scope keeps the model's decision
    free = extraction.Handover(EVIDENCE[:1], [candidate('c1', scope_source='model', scope='Data Center')], [], 0, '', False, 0.0)
    assert matching.check(conn, UNIVERSE, says_new, free.candidates, free.evidence, matching.build_lists(conn, free, [], 10), []).outcomes['c1'][0] == 'new'
    # next fiscal year into this year's view: refused, opened as new
    next_year = extraction.Handover(EVIDENCE[:1], [candidate('c1', scope_source='watch', period_start='2027-02-01', period_end='2028-01-31', year='FY2028', due_day='2028-02-25')], [], 0, '', False, 0.0)
    merge = {'candidates': [{'id': 'c1', 'outcome': 'merge', 'target_view_id': dc, 'reason': 'same segment', 'dependencies': []}], 'evidence': []}
    checked = matching.check(conn, UNIVERSE, merge, next_year.candidates, next_year.evidence, matching.Lists({'c1': [dc]}, {}), [])
    assert checked.outcomes['c1'][0] == 'new' and 'refused by key' in checked.notes[0]


def test_a_model_written_scope_is_wording_not_identity(tmp_path):
    # T4 (2026-10-25): thirteen financing views on one story, because the key refused the model's merges on scope wording
    # ('OpenAI data center guarantee' vs 'OpenAI Ohio data center backstop'); only a code-owned scope binds identity
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    fin = lambda cid, scope: candidate(cid, object='ai-capex', kind='theme', measure='financing_amount', scope=scope, scope_source='model', period_start='2026-01-01', period_end='2026-12-31',
                                       year='2026', looks_at=f'{scope} 金额', question=f'{scope}？', rungs=[dict(r, label=l) for r, l in zip(RUNGS, ['1000亿及以上', '500亿至1000亿', '200亿至500亿', '100亿至200亿', '低于100亿'])])
    first = extraction.Handover(EVIDENCE[:1], [fin('c1', 'OpenAI data center guarantee')], [], 0, '', False, 0.0)
    v = writing.write(conn, UNIVERSE, 1, ITEM, first, matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {}).new_views['c1']
    assert store.view_key(conn, v)['scope_source'] == 'model'
    later = extraction.Handover(EVIDENCE[:1], [fin('c1', 'OpenAI Ohio data center backstop')], [], 0, '', False, 0.0)
    lists = matching.build_lists(conn, later, [], 10)
    assert lists.candidate_lists['c1'] == [v]                                            # the family is shown whatever the wording
    merge = {'candidates': [{'id': 'c1', 'outcome': 'merge', 'target_view_id': v, 'reason': 'same guarantee', 'dependencies': []}], 'evidence': []}
    checked = matching.check(conn, UNIVERSE, merge, later.candidates, later.evidence, lists, [])
    assert checked.outcomes['c1'] == ('merge', v, []) and checked.notes == []       # the model's merge stands
    says_new = {'candidates': [{'id': 'c1', 'outcome': 'new', 'target_view_id': '', 'reason': 'another amount', 'dependencies': []}], 'evidence': []}
    assert matching.check(conn, UNIVERSE, says_new, later.candidates, later.evidence, lists, []).outcomes['c1'][0] == 'new'   # and so does its "new"


def test_legacy_key_read_does_not_mutate_schema_and_distinct_event_is_refused(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    conn.execute('drop table view_keys')
    conn.execute('create table view_keys (view_id text primary key, measure text, scope text, scope_key text, period_start text, period_end text, basis text, unit text, event_type text, seq integer)')
    rubin = candidate('c1', measure='event', scope='Rubin', event_type='shipment', year='2026', period_start='2026-01-01', period_end='2026-12-31', due_day='2026-12-31',
                      rungs=[{'label': 'Yes', 'condition': '是', 'lo': None, 'hi': None}, {'label': 'No', 'condition': '否', 'lo': None, 'hi': None}])
    conn.execute("insert into view_keys (view_id, measure, scope, scope_key, period_start, period_end, basis, unit, event_type, seq) values ('v1','event','Rubin','rubin','2026-01-01','2026-12-31','n/a','n/a','shipment',1)")
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='company', kind='asset', looks_at='Rubin 出货', question='?', due_day='2026-12-31', year='2026', rungs=rubin['rungs'], seq=1, input_id='x', created_at='2026-10-25T00:00:00')
    assert store.view_key(conn, 'v1')['scope_source'] == 'model'                       # the store alone cannot tell
    other = extraction.Handover(EVIDENCE[:1], [candidate('c2', measure='event', scope='Blackwell+Rubin', scope_source='watch', event_type='launch', year='2026', period_start='2026-01-01', period_end='2026-12-31', due_day='2026-12-31', rungs=rubin['rungs'])], [], 0, '', False, 0.0)
    merge = {'candidates': [{'id': 'c2', 'outcome': 'merge', 'target_view_id': 'v1', 'reason': 'rubin', 'dependencies': []}], 'evidence': []}
    checked = matching.check(conn, UNIVERSE, merge, other.candidates, other.evidence, matching.Lists({'c2': ['v1']}, {}), [])
    assert checked.outcomes['c2'][0] == 'new' and 'refused by key' in checked.notes[0]   # the universe knows 'Rubin' is the list's spelling: the scope binds


def test_another_objects_view_is_never_the_same_view(tmp_path):
    # T4b (2026-10-25): Amazon's FY2026 capex and revenue were merged into Meta's by a key match that ignored the object
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    meta_item = dict(ITEM, object_identifiers=[{'value': 'META'}])
    meta = candidate('c1', object='META', measure='capex', scope='', unit='USD', year='2026', period_start='2026-01-01', period_end='2026-12-31', scope_source='none', looks_at='Meta FY2026 capex', question='capex?', due_day='2027-01-31')
    m = writing.write(conn, UNIVERSE, 1, meta_item, extraction.Handover(EVIDENCE[:1], [meta], [], 0, '', False, 0.0), matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {}).new_views['c1']
    amzn = extraction.Handover(EVIDENCE[:1], [candidate('c1', object='AMZN', measure='capex', scope='', unit='USD', year='2026', period_start='2026-01-01', period_end='2026-12-31', scope_source='none', looks_at='Amazon FY2026 capex', question='capex?', due_day='2027-01-31')], [], 0, '', False, 0.0)
    lists = matching.Lists({'c1': [m]}, {})
    says_new = {'candidates': [{'id': 'c1', 'outcome': 'new', 'target_view_id': '', 'reason': 'amazon', 'dependencies': []}], 'evidence': []}
    assert matching.check(conn, UNIVERSE, says_new, amzn.candidates, amzn.evidence, lists, []).outcomes['c1'][0] == 'new'            # no auto-merge across objects
    merge = {'candidates': [{'id': 'c1', 'outcome': 'merge', 'target_view_id': m, 'reason': 'same capex', 'dependencies': []}], 'evidence': []}
    checked = matching.check(conn, UNIVERSE, merge, amzn.candidates, amzn.evidence, lists, [])
    assert checked.outcomes['c1'][0] == 'new' and 'another object' in checked.notes[0]                                               # nor by the model's hand
