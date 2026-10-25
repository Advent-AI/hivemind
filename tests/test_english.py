"""D163, the English library (docs/research/2026-10-25-english/plan.md and build-log.md): the canonical vocabulary at every
boundary that reads an answer or a stored record, the English prompt versions (schema, request text, retry), the year
forms, the half-year filter in both languages, successor orientation from bounds, bounds in bundles, and preflight's
parsers for both request languages. Real ledgers on temporary paths; the universe file the pipeline reads; no model."""
import importlib.util
import os
import sys
import types

from test_keyed_views import EVIDENCE, ITEM, RUNGS, TEXT, UNIVERSE, candidate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import bundle, config, extraction, service, universe, vocabulary  # noqa: E402
from hivemind.views import judging, matching, store, writing  # noqa: E402

LEGACY_RUNGS = [dict(r, label=vocabulary.legacy('label', r['label'])) for r in RUNGS]


def legacy_answer():
    """An answer as extraction v5 wrote it: Chinese kind, tiers and rung labels."""
    c = candidate('c1', kind='对象观点', rungs=LEGACY_RUNGS)
    return {'candidates': [c], 'evidence': [dict(EVIDENCE[0], tier='当事人说的')]}


def test_legacy_values_read_as_canonical_and_unknown_values_pass_through():
    for field, mapping in vocabulary.LEGACY.items():
        for old, new in mapping.items():
            assert vocabulary.canonical(field, old) == new
            assert vocabulary.canonical(field, new) == new          # idempotent
            assert vocabulary.legacy(field, new) == old
        assert vocabulary.canonical(field, 'something else') == 'something else'
    assert set(vocabulary.LEGACY['candidate_outcome'].values()) == set(vocabulary.CANDIDATE_OUTCOMES)
    assert set(vocabulary.LEGACY['tier'].values()) == set(vocabulary.TIERS)


def test_legacy_and_english_extraction_answers_sift_to_the_same_canonical_handover():
    evidence_zh, kept_zh, dropped_zh = extraction.sift(legacy_answer(), ITEM, TEXT, set(), UNIVERSE)
    english = {'candidates': [candidate('c1')], 'evidence': [EVIDENCE[0]]}
    evidence_en, kept_en, dropped_en = extraction.sift(english, ITEM, TEXT, set(), UNIVERSE)
    assert dropped_zh == dropped_en == []
    assert kept_zh[0]['kind'] == kept_en[0]['kind'] == 'asset'
    assert [r['label'] for r in kept_zh[0]['rungs']] == [r['label'] for r in kept_en[0]['rungs']] == vocabulary.ASSET_LABELS
    assert evidence_zh[0]['tier'] == evidence_en[0]['tier'] == 'party_statement'
    # a reversed asset ladder in either spelling is the same ladder, turned round
    reversed_zh = candidate('c1', kind='对象观点', rungs=LEGACY_RUNGS[::-1])
    _, kept, _ = extraction.sift({'candidates': [reversed_zh], 'evidence': [EVIDENCE[0]]}, ITEM, TEXT, set(), UNIVERSE)
    assert [r['label'] for r in kept[0]['rungs']] == vocabulary.ASSET_LABELS


def test_english_extraction_version_has_english_schema_and_request():
    schema = extraction.schema_for('v6')
    candidate_schema = schema['properties']['candidates']['items']['properties']
    assert candidate_schema['kind']['enum'] == vocabulary.KINDS
    assert schema['properties']['evidence']['items']['properties']['tier']['enum'] == vocabulary.TIERS
    assert 'measure' in candidate_schema and 'lo' in candidate_schema['rungs']['items']['properties']
    assert extraction.schema_for('v5')['properties']['candidates']['items']['properties']['kind']['enum'] == ['对象观点', '主题观点']
    shown = [{'view_id': 'v1', 'object_id': 'NVDA', 'looks_at': 'FY2027 total revenue', 'due_day': '2027-02-25', 'question': 'Can demand lift FY2027 revenue above $300 billion?',
              'depends_on': ['v2', '（等 v3 这条链上 FY2027 年的那条）'], 'dependencies': [{'view_id': 'v2'}, {'view_id': None, 'wait_chain_view_id': 'v3', 'wait_year': 'FY2027'}]}]
    system, user = extraction.build_prompt(ITEM, 'Data center revenue guidance is above $300 billion.', shown, UNIVERSE, 'v6')
    assert system.startswith('You are a senior hedge-fund analyst')
    before_item = user.split('[Item]')[0]
    assert not extraction.re.search('[一-龥]', before_item), before_item
    assert 'depends on: v2, (waiting for the FY2027 thesis on chain v3)' in user
    assert "NVDA's fiscal year ends in month 1" in user and 'this year is FY2027' in user
    assert 'ai-capex: AI capital spending' in user
    # the Chinese builder of version 5 prints the stored dependency text unchanged
    _, user_zh = extraction.build_prompt(ITEM, 'x', shown, UNIVERSE, 'v5')
    assert '依赖：v2、（等 v3 这条链上 FY2027 年的那条）' in user_zh


def test_half_year_figures_are_evidence_in_both_languages_and_a_half_year_event_is_not():
    def kept(looks_at, question):
        c = candidate('c1', looks_at=looks_at, question=question)
        _, kept, dropped = extraction.sift({'candidates': [c], 'evidence': [EVIDENCE[0]]}, ITEM, TEXT, set(), UNIVERSE)
        return bool(kept)
    for zh, en in [(('H1 收入', 'H1 收入多少？'), ('H1 revenue', 'What is H1 revenue?')),
                   (('上半年收入', '上半年收入多少？'), ('first-half revenue', 'Can first-half revenue top $100 billion?')),
                   (('1H FY2027 收入', '多少？'), ('1H FY2027 revenue', 'How much?'))]:
        assert kept(*zh) is False and kept(*en) is False, (zh, en)
    assert kept('Rubin 下半年量产出货', 'Rubin 是否在下半年量产？') is True
    assert kept('Rubin volume shipments in H2 2026', 'Does Rubin ship in volume in the second half of 2026?') is True


def test_matching_english_version_schema_and_checks_in_both_vocabularies(tmp_path):
    schema = matching.schema_for('matching-v2')
    assert schema['properties']['candidates']['items']['properties']['outcome']['enum'] == vocabulary.CANDIDATE_OUTCOMES
    assert schema['properties']['evidence']['items']['properties']['outcome']['enum'] == vocabulary.EVIDENCE_OUTCOMES
    assert schema['properties']['candidates']['items']['properties']['dependencies']['items']['properties']['direction']['enum'] == vocabulary.DIRECTIONS
    assert matching.schema_for('matching-v1')['properties']['candidates']['items']['properties']['outcome']['enum'] == ['归入已有的', '接续', '新观点', '不开']
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    first = extraction.Handover([EVIDENCE[0]], [candidate('c1')], [], 0, '', False, 0.0)
    vid = writing.write(conn, UNIVERSE, 1, ITEM, first, matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {}).new_views['c1']
    later = candidate('c2', question='Can demand lift FY2027 data center revenue above $300 billion?')
    lists = matching.Lists({'c2': [vid]}, {})
    for spelling in ('归入已有的', 'merge'):
        decision = {'candidates': [{'id': 'c2', 'outcome': spelling, 'target_view_id': vid, 'reason': 'same quantity', 'dependencies': []}], 'evidence': []}
        checked = matching.check(conn, UNIVERSE, decision, [later], [EVIDENCE[0]], lists, [])
        assert checked.refusals == [] and checked.outcomes['c2'] == ('merge', vid, [])
    # a legacy direction on a new theme view's dependency is stored canonical
    theme = candidate('c3', object='ai-capex', kind='主题观点', measure='spend_total', scope='five hyperscalers', looks_at='2026 hyperscaler capex', question='How much?',
                      rungs=[dict(r, label=f'band {i}') for i, r in enumerate(RUNGS)], year='2026', period_start='2026-01-01', period_end='2026-12-31')
    decision = {'candidates': [{'id': 'c3', 'outcome': '新观点', 'target_view_id': '', 'reason': 'new', 'dependencies': [{'view_id': vid, 'wait_chain_view_id': '', 'wait_year': '', 'direction': '同向'}]}], 'evidence': []}
    checked = matching.check(conn, UNIVERSE, decision, [theme], [EVIDENCE[0]], matching.Lists({'c3': [vid]}, {}), [])
    assert checked.refusals == [] and checked.outcomes['c3'][2][0]['direction'] == 'same'


def test_repeat_target_shown_in_another_list_of_the_same_request_is_accepted_when_under_the_view(tmp_path):
    """06-views step 5: evidence is compared with the evidence under its destination thesis. The request shows each piece
    the top-N of that thesis's evidence; a target the model names from another list of the same request is accepted when
    it is linked to that thesis (the 2026-07-27 OpenAI financing item: Huang's clarification replaced the WSJ report that
    was in e1's list, not e5's), and refused when it is not linked there."""
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    first = extraction.Handover([EVIDENCE[0]], [candidate('c1')], [], 0, '', False, 0.0)
    v_dc = writing.write(conn, UNIVERSE, 1, ITEM, first, matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {}).new_views['c1']
    total = candidate('c2', measure='total_revenue', scope='', looks_at='FY2027 total revenue', question='Can demand lift FY2027 total revenue above $400 billion?')
    v_total = writing.write(conn, UNIVERSE, 2, ITEM, extraction.Handover([dict(EVIDENCE[0], id='e9', links=['c2'])], [total], [], 0, '', False, 0.0),
                            matching.Checked({'c2': ('new', None, [])}, {}, [], {}), {}).new_views['c2']
    under_dc = store.evidence_ids_under(conn, v_dc)[0]
    under_total = store.evidence_ids_under(conn, v_total)[0]
    store.link(conn, under_dc, v_total, 2)                      # the WSJ piece sits under both theses
    fresh = [dict(EVIDENCE[0], id='e1', quote=EVIDENCE[0]['quote'], links=[v_total, v_dc]), dict(EVIDENCE[0], id='e5', quote=EVIDENCE[0]['quote'], one_line='Huang says the reports overstated the talks', links=[v_total, v_dc])]
    lists = matching.Lists({}, {('e1', v_total): [under_dc, under_total], ('e1', v_dc): [under_dc], ('e5', v_total): [under_total], ('e5', v_dc): []})
    decisions = {'candidates': [], 'evidence': [
        {'id': 'e1', 'view_id': v_total, 'outcome': 'repeat', 'target_evidence_id': under_dc, 'said_day': '', 'reason': 'same report'},
        {'id': 'e1', 'view_id': v_dc, 'outcome': 'repeat', 'target_evidence_id': under_dc, 'said_day': '', 'reason': 'same report'},
        {'id': 'e5', 'view_id': v_total, 'outcome': 'replace', 'target_evidence_id': under_dc, 'said_day': '2026-07-27', 'reason': 'clarification supersedes the report'},
        {'id': 'e5', 'view_id': v_dc, 'outcome': 'replace', 'target_evidence_id': under_dc, 'said_day': '2026-07-27', 'reason': 'clarification supersedes the report'}]}
    checked = matching.check(conn, UNIVERSE, decisions, [], fresh, lists, [])
    assert checked.refusals == []
    assert checked.evidence[('e5', v_dc)] == ('replace', under_dc, '2026-07-27')
    # the same target named under a thesis it is not linked to is still refused
    store_only_total = dict(decisions, evidence=[{'id': 'e5', 'view_id': v_dc, 'outcome': 'replace', 'target_evidence_id': under_total, 'said_day': '', 'reason': 'x'}])
    refused = matching.check(conn, UNIVERSE, store_only_total, [], [fresh[1]], matching.Lists({}, {('e5', v_dc): [], ('e5', v_total): [under_total]}), [])
    assert any("not among" in r for r in refused.refusals)


def test_merge_into_a_candidate_of_the_same_answer_opens_a_new_view_instead_of_refusing(tmp_path):
    """06-views step 4: a merge inherits an existing thesis's ladder and due day; another candidate has neither. The
    2026-07-29 META transcript merged Family of Apps revenue into the total-revenue candidate and the refusal cost the item."""
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    total = candidate('c1', measure='total_revenue', scope='', looks_at='FY2026 total revenue', question='Can ads lift FY2026 total revenue above $200 billion?',
                      object='META', period_start='2026-01-01', period_end='2026-12-31', year='2026')
    segment = candidate('c2', measure='segment_revenue', scope='Family of Apps', looks_at='FY2026 Family of Apps revenue', question='How much?',
                        object='META', period_start='2026-01-01', period_end='2026-12-31', year='2026', evidence_ids=['e1'])
    decisions = {'candidates': [{'id': 'c1', 'outcome': 'new', 'target_view_id': '', 'reason': 'no thesis', 'dependencies': []},
                                {'id': 'c2', 'outcome': 'merge', 'target_view_id': 'c1', 'reason': 'part of total revenue', 'dependencies': []}], 'evidence': []}
    checked = matching.check(conn, UNIVERSE, decisions, [total, segment], [EVIDENCE[0]], matching.Lists({'c1': [], 'c2': []}, {}), [])
    assert checked.refusals == []
    assert checked.outcomes['c1'][0] == 'new' and checked.outcomes['c2'][0] == 'new'
    assert any('into candidate c1 is not a destination' in n for n in checked.notes)


def test_judging_english_version_schema_and_pushes_stored_canonical(tmp_path):
    assert judging.schema_for('judging-v3')['properties']['pushes']['items']['properties']['push']['enum'] == vocabulary.PUSHES
    assert judging.schema_for('judging-v2')['properties']['pushes']['items']['properties']['push']['enum'] == ['推向第一格', '推向最后一格', '不推']
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    first = extraction.Handover([EVIDENCE[0]], [candidate('c1')], [], 0, '', False, 0.0)
    vid = writing.write(conn, UNIVERSE, 1, ITEM, first, matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {}).new_views['c1']
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v17.json'))
    answer = types.SimpleNamespace(data={'rung': 2, 'reasons': 'guidance', 'cites': ['e1'], 'cites_views': [], 'pushes': [{'evidence_id': 'e1', 'push': '推向第一格'}],
                                         'changed': True, 'why_changed': 'first'}, call_id=0, request_sha256='x', cached=False, cost_usd=0.0)
    system, user = judging.build_prompt(conn, vid, 'judging-v3')
    assert '[Evidence in force under this thesis, 1 items]' in user and 'this is the first judgement, so changed must be true' in user
    assert 'Thesis ' + vid + ' (NVDA, asset, focus' in user and '[Previous conclusion' in user
    judging._record(conn, cfg, vid, 1, ITEM, answer)
    stored = conn.execute('select pushes_json from judgements where view_id=?', (vid,)).fetchone()[0]
    assert '"toward_first"' in stored and '推向' not in stored
    _, user = judging.build_prompt(conn, vid, 'judging-v3')
    assert '[Previous conclusion, for comparison only] rung 2; reasons: guidance' in user
    assert judging.retry_note('judging-v3', ['x']).startswith('\n\nThe code returned the previous answer because: x')


def test_year_forms_full_match_and_one_canonical_spelling():
    nvda_fy2027 = ('2026-02-01', '2027-01-31')
    for text in ('FY2027', 'FY 2027', 'fiscal 2027', 'fiscal year 2027', '2027财年', 'FY27', '2027', '2027年'):
        assert UNIVERSE.fiscal_period('NVDA', text) == nvda_fy2027, text          # a company's bare year is its fiscal year for the period (06-views)
    for text in ('FY2027', 'FY 2027', 'fiscal 2027', 'fiscal year 2027', '2027财年', 'FY27'):
        assert UNIVERSE.canonical_year('NVDA', text) == 'FY2027', text
    for text in ('2027', '2027年', ' 2027 '):
        assert UNIVERSE.canonical_year('NVDA', text) == '2027', text              # a bare year is never respelled: an event dated 2026 is calendar 2026
    # the English request defines "2026" as a calendar year: the sift of an English answer reads it so (MSFT's
    # "calendar-year 2026 capex" and NVDA's "2026 market share" had been moved to fiscal years in the week build)
    assert UNIVERSE.fiscal_period('MSFT', '2026', bare_is_calendar=True) == ('2026-01-01', '2026-12-31')
    assert UNIVERSE.fiscal_period('MSFT', '2026') == ('2025-07-01', '2026-06-30')
    msft = candidate('c1', object='MSFT', measure='capex', scope='', year='2026', period_start='2026-01-01', period_end='2026-12-31',
                     looks_at='Calendar-year 2026 capital expenditures', question='How much?', evidence_ids=['e1'])
    _, kept_en, _ = extraction.sift({'candidates': [msft], 'evidence': [EVIDENCE[0]]}, dict(ITEM, object_identifiers=[{'value': 'MSFT'}]), TEXT, set(), UNIVERSE, english=True)
    _, kept_zh, _ = extraction.sift({'candidates': [msft], 'evidence': [EVIDENCE[0]]}, dict(ITEM, object_identifiers=[{'value': 'MSFT'}]), TEXT, set(), UNIVERSE)
    assert (kept_en[0]['period_start'], kept_en[0]['period_end']) == ('2026-01-01', '2026-12-31')
    assert (kept_zh[0]['period_start'], kept_zh[0]['period_end']) == ('2025-07-01', '2026-06-30')
    for text in ('calendar year 2026', 'calendar 2026', 'CY2026', '2026自然年', '2026 calendar year'):
        assert UNIVERSE.fiscal_period('NVDA', text) == ('2026-01-01', '2026-12-31'), text
        assert UNIVERSE.canonical_year('NVDA', text) == '2026', text
    assert UNIVERSE.fiscal_period('ai-capex', '2026') == ('2026-01-01', '2026-12-31')
    assert UNIVERSE.canonical_year('ai-capex', 'FY2026') == '2026'            # a theme has no fiscal year of its own
    assert UNIVERSE.canonical_year('AMZN', 'FY2026') == '2026'                # a December year-end is the calendar year
    assert UNIVERSE.canonical_year('MSFT', 'fiscal 2027') == 'FY2027'
    for text in ('2025-2027', 'FY2026-FY2027', '2025–2027自然年', 'next year', '', 'H2 2026'):
        assert universe.parse_year(text) is None, text
        assert UNIVERSE.fiscal_period('NVDA', text) is None, text
        assert UNIVERSE.canonical_year('NVDA', text) == text.strip(), text


def test_waiting_dependency_resolves_across_year_spellings(tmp_path):
    """A theme view waits for NVDA's FY2027 revenue written as 'fiscal year 2027'; the successor arrives with year '2027'."""
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    first = extraction.Handover([EVIDENCE[0]], [candidate('c1', measure='total_revenue', scope='', year='FY2026', period_start='2025-02-01', period_end='2026-01-31', looks_at='FY2026 total revenue')], [], 0, '', False, 0.0)
    v1 = writing.write(conn, UNIVERSE, 1, ITEM, first, matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {}).new_views['c1']
    theme = candidate('c2', object='ai-capex', kind='theme', measure='spend_total', scope='five hyperscalers', looks_at='2026 hyperscaler capex', question='How much?',
                      rungs=[dict(r, label=f'band {i}') for i, r in enumerate(RUNGS)], year='2026', period_start='2026-01-01', period_end='2026-12-31')
    waiting = [{'view_id': None, 'wait_chain_view_id': v1, 'wait_year': 'fiscal year 2027', 'direction': 'same'}]
    x = writing.write(conn, UNIVERSE, 2, ITEM, extraction.Handover([EVIDENCE[0]], [theme], [], 0, '', False, 0.0),
                      matching.Checked({'c2': ('new', None, waiting)}, {}, [], {}), {}).new_views['c2']
    assert conn.execute('select wait_year from dependencies where view_id=?', (x,)).fetchone()[0] == 'FY2027'
    successor = candidate('c3', measure='total_revenue', scope='', year='fiscal 2027', looks_at='FY2027 total revenue')
    v2 = writing.write(conn, UNIVERSE, 3, ITEM, extraction.Handover([EVIDENCE[0]], [successor], [], 0, '', False, 0.0),
                       matching.Checked({'c3': ('succession', v1, [])}, {}, [], {}), {}).new_views['c3']
    assert store.view(conn, v2)['year'] == 'FY2027'
    assert [d['resolved_to'] for d in store.dependencies_of(conn, x)] == [v2]


def test_a_numeric_successor_is_stored_in_the_predecessor_direction(tmp_path):
    """06-views: a successor keeps the predecessor's direction. The first real succession (2027 hyperscaler capex after 2026,
    poc-v21 seed) came low-to-high where its predecessor ran high-to-low; the writer reverses it, matching no longer refuses."""
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    high_first = [{'label': 'At least $750 billion', 'condition': '≥ 750', 'lo': 750e9, 'hi': None}, {'label': '$700–750 billion', 'condition': '700–750', 'lo': 700e9, 'hi': 750e9},
                  {'label': '$650–700 billion', 'condition': '650–700', 'lo': 650e9, 'hi': 700e9}, {'label': '$600–650 billion', 'condition': '600–650', 'lo': 600e9, 'hi': 650e9},
                  {'label': 'Below $600 billion', 'condition': '< 600', 'lo': None, 'hi': 600e9}]
    capex26 = candidate('c1', object='ai-capex', kind='theme', measure='spend_total', scope='five hyperscalers', looks_at='2026 hyperscaler capex', question='How much?',
                        rungs=high_first, year='2026', period_start='2026-01-01', period_end='2026-12-31')
    v26 = writing.write(conn, UNIVERSE, 1, ITEM, extraction.Handover([EVIDENCE[0]], [capex26], [], 0, '', False, 0.0), matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {}).new_views['c1']
    low_first = [{'label': 'Below $750 billion', 'condition': '< 750', 'lo': None, 'hi': 750e9}, {'label': '$750–900 billion', 'condition': '750–900', 'lo': 750e9, 'hi': 900e9},
                 {'label': '$900 billion–1 trillion', 'condition': '900–1000', 'lo': 900e9, 'hi': 1e12}, {'label': '$1–1.1 trillion', 'condition': '1000–1100', 'lo': 1e12, 'hi': 1.1e12},
                 {'label': '$1.1 trillion or more', 'condition': '≥ 1100', 'lo': 1.1e12, 'hi': None}]
    capex27 = candidate('c2', object='ai-capex', kind='theme', measure='spend_total', scope='five hyperscalers', looks_at='2027 hyperscaler capex', question='How much?',
                        rungs=low_first, year='2027', period_start='2027-01-01', period_end='2027-12-31', evidence_ids=['e1'])
    decision = {'candidates': [{'id': 'c2', 'outcome': 'succession', 'target_view_id': v26, 'reason': 'next year', 'dependencies': []}], 'evidence': []}
    checked = matching.check(conn, UNIVERSE, decision, [capex27], [EVIDENCE[0]], matching.Lists({'c2': [v26]}, {}), [])
    assert checked.refusals == [] and checked.outcomes['c2'][:2] == ('succession', v26)
    written = writing.write(conn, UNIVERSE, 2, ITEM, extraction.Handover([EVIDENCE[0]], [capex27], [], 0, '', False, 0.0), checked, {})
    stored = store.rungs_of(conn, written.new_views['c2'])
    assert [r['label'] for r in stored] == [r['label'] for r in reversed(low_first)] and stored[0]['lo'] == 1.1e12
    assert any('reversed to the predecessor' in n for n in written.notes)
    assert conn.execute('select succeeds from successions where view_id=?', (written.new_views['c2'],)).fetchone()[0] == v26


def test_successor_orientation_reads_bounds_first_then_english_prose():
    # conditions without a number: only the bounds can orient these ladders (prose alone leaves them to the model)
    rising = [{'label': 'a', 'condition': 'the low band', 'lo': None, 'hi': 300e9}, {'label': 'b', 'condition': 'the middle band', 'lo': 300e9, 'hi': 500e9},
              {'label': 'c', 'condition': 'the high band', 'lo': 500e9, 'hi': None}]
    falling = list(reversed(rising))
    assert matching.ladder_direction(rising) == 1 and matching.ladder_direction(falling) == -1
    assert matching.ladder_direction([{'label': r['label'], 'condition': r['condition']} for r in rising]) is None
    prose = [{'label': 'a', 'condition': 'below $300 billion'}, {'label': 'b', 'condition': 'from $300 billion to $500 billion'}, {'label': 'c', 'condition': 'at least $500 billion'}]
    assert matching.ladder_direction(prose) == 1
    assert matching.first_value('above 1.2 trillion dollars') == 1200.0 and matching.first_value('above 500 million') == 0.5


def test_bundle_carries_bounds_and_service_counts_facts_in_both_spellings(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    first = extraction.Handover([EVIDENCE[0]], [candidate('c1')], [], 0, '', False, 0.0)
    vid = writing.write(conn, UNIVERSE, 1, ITEM, first, matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {}).new_views['c1']
    store.add_evidence(conn, evidence_id='e9', quote='q', one_line='legacy fact', speaker='', original_who='', original_day='2026-05-20', tier='发生的事', event_time='', seq=1, input_id=ITEM['input_id'])
    store.link(conn, 'e9', vid, 1)
    store.add_evidence(conn, evidence_id='e10', quote='q2', one_line='canonical fact', speaker='', original_who='', original_day='2026-05-20', tier='fact', event_time='', seq=1, input_id=ITEM['input_id'])
    store.link(conn, 'e10', vid, 1)
    store.mark_step(conn, ITEM['input_id'], 1, 'handed_over', 'ok', '', ITEM['publication_day'], '2026-05-20T12:00:00')      # the service dates every row by its sequence number
    store.complete_day(conn, ITEM['publication_day'], 1, '2026-05-20T23:59:00')
    conn.commit()
    assert service.view(conn, vid, ITEM['publication_day'])['counts']['facts'] == 2
    item_of = lambda input_id: {'title': 'call', 'publisher': 'NVIDIA', 'publisher_type': 'issuer', 'category': 'T1', 'source_uri': '', 'publication_day': ITEM['publication_day']}
    rungs = bundle.view_bundle(conn, item_of, vid)['rungs']
    assert [r['lo'] for r in rungs] == [350e9, 300e9, 250e9, 200e9, None] and rungs[-1]['hi'] == 200e9


def test_preflight_parsers_read_both_request_languages():
    spec = importlib.util.spec_from_file_location('preflight', os.path.join(ROOT, 'scripts', 'preflight.py'))
    preflight = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(preflight)
    zh = preflight.ITEM_ID.search('【信息】编号 gnews:abc，类别 T7，作者 Reuters')
    en = preflight.ITEM_ID.search('[Item] id gnews:abc, category T7, author Reuters')
    assert (zh.group(1) or zh.group(2)) == (en.group(1) or en.group(2)) == 'gnews:abc'
    assert preflight.BLOCK5_VIEW.findall('  - v1（NVDA，看的是「x」）：q\n  - v2 (NVDA, focus "x", due 2027-02-25): q') == ['v1', 'v2']
    assert preflight.MATCH_SHOWN.findall('· v3（开着，NVDA）：q\n· v4 (open, NVDA): q') == ['v3', 'v4']


def test_poc_v17_names_english_prompts_that_carry_every_schema_value():
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v17.json'))
    assert extraction.is_english(cfg.extraction['T7'].prompt_version.rpartition('-')[2]) and matching.is_english(cfg.matching.prompt_version)
    assert judging.is_english(cfg.rejudging.prompt_version) and cfg.idea.prompt_version == 'idea-v11'
    role = open(config.prompt_path('role-v6.txt'), encoding='utf-8').read()
    assert all(value in role for value in vocabulary.TIERS + vocabulary.KINDS + vocabulary.ASSET_LABELS)
    for name in ('matching-v2.txt', 'matching-v3.txt'):
        match = open(config.prompt_path(name), encoding='utf-8').read()
        assert all(value in match for value in vocabulary.CANDIDATE_OUTCOMES + vocabulary.EVIDENCE_OUTCOMES + vocabulary.DIRECTIONS), name
    v18 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v18.json'))
    assert v18.matching.prompt_version == 'matching-v3' and matching.is_english(v18.matching.prompt_version)
    assert 'one decision per listed pair' in open(config.prompt_path('matching-v3.txt'), encoding='utf-8').read()
    judge = open(config.prompt_path('judging-v3.txt'), encoding='utf-8').read()
    assert all(value in judge for value in vocabulary.PUSHES)
    for name in ('role-v6.txt', 'categories-v6.json', 'matching-v2.txt', 'judging-v3.txt', 'idea-v11.txt'):
        assert not extraction.re.search('[一-龥]', open(config.prompt_path(name), encoding='utf-8').read()), name


def test_a_repeat_may_name_the_piece_shown_for_the_same_evidence_under_another_thesis(tmp_path):
    """06-views step 6: a repeat adds a source and any new thesis link. The 2026-08-08 item (gnews:0214359f…) restated NVIDIA's
    $91bn Q2 guidance, linked to total revenue and Data Center revenue; the guidance piece sat only under total revenue, and
    the check refused the model's repeat under Data Center twice, failing the item (9 of 17 such refusals over four ledgers).
    A replacement naming a piece of another thesis is still refused (test above)."""
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    first = extraction.Handover([EVIDENCE[0]], [candidate('c1')], [], 0, '', False, 0.0)
    v_dc = writing.write(conn, UNIVERSE, 1, ITEM, first, matching.Checked({'c1': ('new', None, [])}, {}, [], {}), {}).new_views['c1']
    total = candidate('c2', measure='total_revenue', scope='', looks_at='FY2027 total revenue', question='Can demand lift FY2027 total revenue above $400 billion?')
    v_total = writing.write(conn, UNIVERSE, 2, ITEM, extraction.Handover([dict(EVIDENCE[0], id='e9', links=['c2'], quote='NVIDIA guided Q2 revenue to $91 billion.')], [total], [], 0, '', False, 0.0),
                            matching.Checked({'c2': ('new', None, [])}, {}, [], {}), {}).new_views['c2']
    guidance = store.evidence_ids_under(conn, v_total)[0]
    other_dc = store.evidence_ids_under(conn, v_dc)[0]
    assert guidance not in store.evidence_ids_under(conn, v_dc)
    restated = dict(EVIDENCE[0], id='e3', quote='NVIDIA still guides $91 billion in Q2 revenue.', links=[v_total, v_dc])
    lists = matching.Lists({}, {('e3', v_total): [guidance], ('e3', v_dc): [other_dc]})
    decisions = {'candidates': [], 'evidence': [
        {'id': 'e3', 'view_id': v_total, 'outcome': 'repeat', 'target_evidence_id': guidance, 'said_day': '', 'reason': 'same guidance'},
        {'id': 'e3', 'view_id': v_dc, 'outcome': 'repeat', 'target_evidence_id': guidance, 'said_day': '', 'reason': 'same guidance'}]}
    checked = matching.check(conn, UNIVERSE, decisions, [], [restated], lists, [])
    assert checked.refusals == [] and checked.evidence[('e3', v_dc)] == ('repeat', guidance, '')
    handover = extraction.Handover([restated], [], [], 0, '', False, 0.0)
    writing.write(conn, UNIVERSE, 3, dict(ITEM, input_id='later'), handover, checked, {})
    assert guidance in store.evidence_ids_under(conn, v_dc)                  # the writer adds the new thesis link
    # a target shown to no list of this piece is still refused
    stray = dict(decisions, evidence=[decisions['evidence'][0], dict(decisions['evidence'][1], target_evidence_id='e999')])
    assert any("not among" in r for r in matching.check(conn, UNIVERSE, stray, [], [restated], lists, []).refusals)
