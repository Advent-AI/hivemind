"""D197: a shared quantity (an aggregate opened as industry_aggregate / shared_quantity) is one thesis per theme, measure and period;
its scope is wording, so code decides identity (D155) and neither Jev nor the collision judge is asked whether two wordings of
one aggregate are one question. Real ledgers on temporary paths; scripted transports."""
import json
import os
import sys

from test_keyed_views import ITEM, RUNGS, UNIVERSE, candidate
from test_jev_matching import scripted

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction, model  # noqa: E402
from hivemind.views import identity, jev_matching, matching, store, writing  # noqa: E402

CFG = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v29.json'))
USD = [dict(r, label=l) for r, l in zip(RUNGS, ['$800bn or more', '$700–800bn', '$600–700bn', '$500–600bn', 'below $500bn'])]


def aggregate(cid, scope, year='2026', **over):
    return candidate(cid, object='ai-capex', kind='theme', measure='spend_total', scope=scope, scope_source='model', opens_as='industry_aggregate',
                     settled_by='the five companies\' reported capital expenditures', folds_into='', lost_if_folded='',
                     period_start=f'{year}-01-01', period_end=f'{year}-12-31', year=year, due_day=f'{int(year) + 1}-04-30', unit='USD', basis='n/a', event_type='n/a',
                     looks_at=f'{scope}, calendar {year}', question=f'How much will {scope} spend in calendar {year}?', rungs=USD, **over)


def never_judge(provider, request):
    raise AssertionError('the collision judge was asked about a shared quantity')


def test_a_shared_quantity_is_keyed_without_its_scope():
    five = aggregate('c1', 'Alphabet, Amazon, Meta, Microsoft and Oracle combined')
    industry = aggregate('c2', 'industrywide AI infrastructure spending')
    assert identity.automatic_key(five) is not None and identity.automatic_key(five) == identity.automatic_key(industry)
    assert identity.automatic_key(five)[2] == ''                                           # the scope is not in the key
    assert identity.automatic_key(aggregate('c3', 'the same five', year='2027')) != identity.automatic_key(five)
    assert identity.automatic_key(candidate('c4', scope='Data Center', scope_source='model')) is None   # a company line with a model-written scope stays the model's
    assert identity.automatic_key(candidate('c5', object='chip-export-controls', kind='theme', measure='policy_event', event_type='other',
                                            scope='H200 imports', scope_source='model', opens_as='policy_stage')) is None   # a policy stage is not a quantity


def test_the_writer_records_the_shared_scope_source_and_the_exact_identity_is_found_under_any_wording(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    first = extraction.Handover([], [aggregate('c1', 'the top five cloud providers')], [], 0, '', False, 0.0)
    v = writing.write(conn, UNIVERSE, 1, ITEM, first, matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {}).new_views['c1']
    assert store.view_key(conn, v)['scope_source'] == 'shared'
    other = aggregate('c2', 'Big Tech companies\' combined AI outlays')
    assert store.exact_key_views(conn, other) == [v]
    assert store.exact_key_views(conn, aggregate('c3', 'the top five cloud providers', year='2027')) == []
    lists = matching.build_lists(conn, extraction.Handover([], [other], [], 0, '', False, 0.0), [], 10)
    assert lists.candidate_lists['c2'] == [v]


def test_matching_merges_another_wording_of_the_aggregate_by_code_and_succeeds_it_for_the_next_year(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    first = extraction.Handover([], [aggregate('c1', 'the top five cloud providers')], [], 0, '', False, 0.0)
    v = writing.write(conn, UNIVERSE, 1, ITEM, first, matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {}).new_views['c1']
    other = aggregate('c2', 'Big Tech companies\' combined AI outlays')
    next_year = aggregate('c3', 'AI hyperscaler data-center capital expenditures worldwide', year='2027')
    lists = matching.Lists({'c2': [v], 'c3': [v]}, {})
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    jev_says_different = scripted({})
    answer = jev_matching.decide(archive, CFG, conn, ITEM, [other, next_year], [], lists, [], transport=jev_says_different, llm_transport=never_judge)
    raw = {d['id']: (d['outcome'], d['target_view_id']) for d in answer.data['candidates']}
    assert raw == {'c2': ('merge', v), 'c3': ('succession', v)}
    assert 'shared quantity' in next(d['reason'] for d in answer.data['candidates'] if d['id'] == 'c2')
    checked = matching.check(conn, UNIVERSE, answer.data, [other, next_year], [], lists, [])
    assert checked.refusals == [] and checked.outcomes['c2'] == ('merge', v, []) and checked.outcomes['c3'] == ('succession', v, [])
    written = writing.write(conn, UNIVERSE, 2, ITEM, extraction.Handover([], [other, next_year], [], 0, '', False, 0.0), checked, {})
    assert 'c2' not in written.new_views and written.new_views['c3'] != v
    assert store.view_key(conn, written.new_views['c3'])['scope_source'] == 'shared'
    # a company's own capital spending is not the aggregate: a different object, never the same thesis
    own = candidate('c4', object='MSFT', measure='capex', scope='', scope_source='none', opens_as='main_driver', period_start='2026-01-01', period_end='2026-12-31', year='2026',
                    looks_at='calendar-2026 capex', question='MSFT capex 2026?', unit='USD', basis='n/a', event_type='n/a')
    assert store.exact_key_views(conn, own) == []
