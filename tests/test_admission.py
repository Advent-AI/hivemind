"""D184: a candidate thesis opens only for one of four stated reasons, with the public material that settles it and what
would be lost if it were only evidence; the schema requires the fields from extraction version 12 and code checks their
shape. D185: a binding obligation is due within 18 months, exempt from the next-year rule on quantities."""
import json
import os
import sys

from test_keyed_views import EVIDENCE, ITEM, TEXT, UNIVERSE, candidate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, dispatch, extraction, model  # noqa: E402
from hivemind.views import store  # noqa: E402
from hivemind.views import round as rounds  # noqa: E402

ADMITTED = {'opens_as': 'main_driver', 'folds_into': '', 'lost_if_folded': 'the segment that carries the value would be read only through total revenue',
            'settled_by': 'NVIDIA FY2027 annual earnings release', 'group_refs': []}


def admitted(cid, **over):
    return candidate(cid, **{**ADMITTED, **over})


def test_v12_schema_requires_the_admission_fields_and_v10_does_not():
    schema = extraction.schema_for('v12', [], ['v1', 'v7'])
    fields = schema['properties']['candidates']['items']['properties']
    required = schema['properties']['candidates']['items']['required']
    assert {'opens_as', 'folds_into', 'lost_if_folded', 'settled_by'} <= set(required)
    assert fields['opens_as']['enum'] == extraction.ADMISSION_REASONS == ['main_driver', 'industry_aggregate', 'policy_stage', 'binding_obligation']
    assert fields['folds_into']['pattern'] == '^(?:|v1|v7)$'
    assert 'opens_as' not in extraction.schema_for('v10', [])['properties']['candidates']['items']['properties']


def test_sift_drops_blank_lost_if_folded_and_unshown_folds_into():
    data = {'new_groups': [], 'evidence': [EVIDENCE[0], dict(EVIDENCE[0], id='e2', links=['c2']), dict(EVIDENCE[0], id='e3', links=['c3'])],
            'candidates': [admitted('c1'), admitted('c2', folds_into='v1', lost_if_folded='  ', evidence_ids=['e2']), admitted('c3', folds_into='v9', evidence_ids=['e3'])]}
    _, kept, dropped, _ = extraction.sift_with_groups(data, ITEM, TEXT, {'v1'}, UNIVERSE, english=True)
    assert [c['id'] for c in kept] == ['c1']
    reasons = dict(dropped)
    assert 'lost_if_folded is empty although folds_into names a thesis' in reasons['c2']
    assert 'folds_into names a thesis not shown' in reasons['c3']


def test_binding_obligation_horizon():
    def one(**over):
        data = {'new_groups': [], 'evidence': [EVIDENCE[0]], 'candidates': [admitted('c1', **over)]}
        _, kept, dropped, _ = extraction.sift_with_groups(data, ITEM, TEXT, set(), UNIVERSE, english=True)
        return [c['id'] for c in kept], dict(dropped).get('c1', '')
    binding = dict(opens_as='binding_obligation', measure='financing_amount', scope='Ohio guarantee', year='2028', unit='USD')
    assert one(**binding, due_day='2027-06-30') == (['c1'], '')                      # within 548 days of 2026-05-20, year rule waived (D185)
    kept, reason = one(**binding, due_day='2028-06-30')
    assert kept == [] and 'binding obligation due beyond 18 months' in reason
    kept, reason = one(opens_as='industry_aggregate', measure='spend_total', scope='five hyperscalers', year='2028', due_day='2027-06-30')
    assert kept == [] and 'beyond next year' in reason


def test_candidates_without_opens_as_follow_the_old_path():
    data = {'new_groups': [], 'evidence': [EVIDENCE[0]], 'candidates': [candidate('c1', group_refs=[])]}      # a version-10 shape: no admission fields
    _, kept, dropped, _ = extraction.sift_with_groups(data, ITEM, TEXT, set(), UNIVERSE, english=True)
    assert [c['id'] for c in kept] == ['c1'] and dropped == []


def test_config_v25_loads_and_builds_a_v12_request():
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v25.json'))
    assert cfg.version == 'poc-v25' and all(s.prompt_version.endswith('-v12') for s in cfg.extraction.values())
    shown = [{'view_id': 'v3', 'object_id': 'NVDA', 'looks_at': 'FY2027 data center revenue', 'question': 'q', 'due_day': '2027-02-24', 'dependencies': []},
             {'view_id': 'v4', 'object_id': 'NVDA', 'looks_at': 'FY2027 gross margin', 'question': 'q', 'due_day': '2027-02-24', 'dependencies': []}]
    setting, system, user, schema = extraction.request_for(cfg, dict(ITEM, text=TEXT), TEXT, shown, UNIVERSE)
    assert setting.prompt_version == 'T1-v12' and system.startswith(open(config.prompt_path('role-v12.txt'), encoding='utf-8').read()[:80])
    fields = schema['properties']['candidates']['items']['properties']
    assert fields['folds_into']['pattern'] == '^(?:|v3|v4)$' and 'opens_as' in fields


def test_round_writes_a_v12_candidate_end_to_end(tmp_path):
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v25.json'))
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    item = dict(ITEM, text=TEXT, publisher='NVIDIA', published_at='2026-05-20T12:00:00Z', source_uri='https://example.test/call')
    raw = {k: v for k, v in admitted('c1').items() if k not in ('key_version', 'scope_source')}
    seen = {}

    def transport(provider, request):
        name = request['response_format']['json_schema']['name']
        seen[name] = request
        if name == 'extraction':
            data = {'candidates': [raw], 'evidence': EVIDENCE[:1], 'new_groups': []}
        else:
            data = {'candidates': [{'id': 'c1', 'outcome': 'new', 'target_view_id': '', 'reason': 'new', 'dependencies': []}], 'evidence': []}
        return {'choices': [{'message': {'content': json.dumps(data)}}]}

    route = dispatch.route(conn, item, UNIVERSE)
    result = rounds.run(conn, archive, cfg, UNIVERSE, item, route.sequence_no, transport=transport)
    assert result.failed == '' and result.new_views == 1
    assert seen['extraction']['response_format']['json_schema']['schema']['properties']['candidates']['items']['properties']['opens_as']['enum'] == extraction.ADMISSION_REASONS
    saved = json.loads(conn.execute('select handover_json from handovers').fetchone()[0])
    assert saved['candidates'][0]['opens_as'] == 'main_driver' and saved['candidates'][0]['settled_by'] == ADMITTED['settled_by']


def test_an_impossible_calendar_date_on_a_binding_obligation_is_refused_not_a_crash():
    data = {'new_groups': [], 'evidence': [EVIDENCE[0]], 'candidates': [admitted('c1', opens_as='binding_obligation', measure='event', scope='Ohio guarantee', event_type='deal_close', due_day='2026-06-31')]}
    _, kept, dropped, _ = extraction.sift_with_groups(data, ITEM, TEXT, set(), UNIVERSE, english=True)
    assert kept == [] and 'due_day is not a real date' in dict(dropped)['c1']


def test_binding_obligation_horizon_applies_to_events_too():
    data = {'new_groups': [], 'evidence': [EVIDENCE[0]], 'candidates': [admitted('c1', opens_as='binding_obligation', measure='event', scope='Ohio guarantee', event_type='deal_close', year='2028', due_day='2028-06-30')]}
    _, kept, dropped, _ = extraction.sift_with_groups(data, ITEM, TEXT, set(), UNIVERSE, english=True)
    assert kept == [] and 'binding obligation due beyond 18 months' in dict(dropped)['c1']


def test_v13_names_shared_quantity_and_v12_keeps_industry_aggregate():
    v13 = extraction.schema_for('v13', [], ['v1'])['properties']['candidates']['items']['properties']['opens_as']['enum']
    v12 = extraction.schema_for('v12', [], ['v1'])['properties']['candidates']['items']['properties']['opens_as']['enum']
    assert v13 == ['main_driver', 'shared_quantity', 'policy_stage', 'binding_obligation'] and v12 == extraction.ADMISSION_REASONS
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v27.json'))
    assert all(s.prompt_version.endswith('-v13') for s in cfg.extraction.values()) and cfg.collision is not None


def test_v16_states_the_decidable_gate_rule_keeps_v12s_admission_reasons_and_asks_for_empty_arrays_only_without_business_content():
    """D199: one call still reads and extracts; the two rules that contradicted each other (every statement is evidence by
    default / link only what a thesis directly concerns, omit the rest) become one decidable rule, and the closing line no
    longer invites an empty answer. v12 is unchanged, so the paused run's requests still replay from the archive."""
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v32.json'))
    assert all(s.prompt_version.endswith('-v16') for s in cfg.extraction.values())
    shown = [{'view_id': 'v3', 'object_id': 'NVDA', 'looks_at': 'FY2027 data center revenue', 'question': 'q', 'due_day': '2027-02-24', 'dependencies': []}]
    setting, system, user, schema = extraction.request_for(cfg, dict(ITEM, text=TEXT), TEXT, shown, UNIVERSE)
    assert "makes that thesis's answer more or less likely" in system and 'by default, evidence' not in system and 'directly concerns' not in system
    assert user.endswith('Return empty arrays only for a page with no business content.')
    assert schema['properties']['candidates']['items']['properties']['opens_as']['enum'] == extraction.ADMISSION_REASONS   # v12's set, as the text names it
    old = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v30.json'))
    _, old_system, old_user, old_schema = extraction.request_for(old, dict(ITEM, text=TEXT), TEXT, shown, UNIVERSE)
    assert 'by default, evidence' in old_system and old_user.endswith('Return empty arrays when there is nothing to extract.')


MANDATORY_TEXT = ('CoreWeave proves old GPUs pay\n'
                  'Skip to main content\n'
                  'CoreWeave signed contracts for its A100 GPUs that run into 2029, chief executive Michael Intrator said on the call, and power constraints keep that capacity rented.\n'
                  'The company reported quarterly revenue of $2.58 billion, up 112% from a year earlier.\n'
                  'Analysts were unmoved by the news on the day.')


def test_v17_numbers_the_page_and_requires_an_account_per_mandatory_paragraph():
    """D199: one call, but the answer accounts for every paragraph that carries a digit, a month name or 120+ characters
    (statements or a skip reason); statements from other paragraphs go in extra; pieces keep their nine fields."""
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v33.json'))
    shown = [{'view_id': 'v3', 'object_id': 'NVDA', 'looks_at': 'FY2027 data center revenue', 'question': 'q', 'due_day': '2027-02-24', 'dependencies': []}]
    setting, system, user, schema = extraction.request_for(cfg, dict(ITEM, text=MANDATORY_TEXT), MANDATORY_TEXT, shown, UNIVERSE)
    assert setting.prompt_version == 'T1-v17' and "makes that thesis's answer more or less likely" in system
    assert '\np0001 CoreWeave proves old GPUs pay\np0002 Skip to main content\np0003 CoreWeave signed' in user
    assert '[Paragraphs to account for]' in user and user.split('[Paragraphs to account for]')[1].split('\n\n')[0].endswith('p0003, p0004')   # the two paragraphs with a digit or 120+ characters
    assert list(schema['properties']) == ['paragraphs', 'extra', 'candidates', 'new_groups'] and schema['properties']['paragraphs']['required'] == ['p0003', 'p0004']
    entry = schema['properties']['paragraphs']['properties']['p0003']
    assert [list(option['properties']) for option in entry['anyOf']] == [['statements'], ['skip']] and entry['anyOf'][1]['properties']['skip']['enum'] == extraction.SKIP_REASONS
    assert list(schema['$defs']['piece']['properties']) == ['id', 'quote', 'one_line', 'speaker', 'original_who', 'original_day', 'tier', 'event_time', 'links']


def test_v17_answers_are_flattened_before_the_checks_and_a_ref_schema_is_checked_locally():
    piece = dict(EVIDENCE[0], quote='CoreWeave signed contracts for its A100 GPUs that run into 2029, chief executive Michael Intrator said on the call, and power constraints keep that capacity rented.', links=['v3'])
    answer = {'paragraphs': {'p0003': {'statements': [piece]}, 'p0004': {'skip': 'no_claim'}}, 'extra': [dict(piece, id='e2', quote='Analysts were unmoved by the news on the day.', links=['v3'])], 'candidates': [], 'new_groups': []}
    evidence, candidates, dropped, groups = extraction.sift_with_groups(answer, dict(ITEM, text=MANDATORY_TEXT), MANDATORY_TEXT, {'v3'}, UNIVERSE, english=True, shown_group_ids=[], version='v17')
    assert [e['id'] for e in evidence] == ['e1', 'e2'] and dropped == []
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v33.json'))
    schema = extraction.request_for(cfg, dict(ITEM, text=MANDATORY_TEXT), MANDATORY_TEXT, [{'view_id': 'v3', 'object_id': 'NVDA', 'looks_at': 'x', 'question': 'q', 'due_day': '2027-02-24', 'dependencies': []}], UNIVERSE)[3]
    assert model.check_schema(answer, schema) == []
    bad = {'paragraphs': {'p0003': {'statements': [dict(piece, tier='gossip')]}, 'p0004': {'skip': 'no_claim'}}, 'extra': [], 'candidates': [], 'new_groups': []}
    assert model.check_schema(bad, schema) != []                        # the $ref'd piece is checked, not waved through
    missing = {'paragraphs': {'p0003': {'skip': 'no_claim'}}, 'extra': [], 'candidates': [], 'new_groups': []}
    assert any('p0004' in e for e in model.check_schema(missing, schema))


def test_the_account_is_capped_at_the_limit_so_a_long_page_cannot_spend_the_output_cap_on_reasoning_alone():
    long_page = '\n'.join(f'Line {i} reports a figure of {i} million dollars for the quarter.' for i in range(1, 101))
    ids = extraction.mandatory_ids(long_page)
    assert len(ids) == extraction.ACCOUNT_LIMIT == 30 and ids[0] == 'p0001' and ids[-1] == 'p0030'


def test_v18_puts_evidence_first_with_the_four_kinds_and_examples_and_narrows_the_opinion_reading_block():
    """D199, arms B3–B6: the role the model reads opens with the evidence job, defines the four kinds of material statement with
    examples, walks the whole page, rejects by example and decides links statement by statement; T8's reading block asks for
    forecasts, ratings, targets and cited figures."""
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v34.json'))
    shown = [{'view_id': 'v3', 'object_id': 'NVDA', 'looks_at': 'FY2027 data center revenue', 'question': 'q', 'due_day': '2027-02-24', 'dependencies': []}]
    item = dict(ITEM, text=TEXT, category='T8')
    setting, system, user, schema = extraction.request_for(cfg, item, TEXT, shown, UNIVERSE)
    assert setting.prompt_version == 'T8-v18' and system.startswith('You are a senior hedge-fund analyst reading one item. Your first job is evidence')
    assert system.index('Evidence: what to keep') < system.index('Which questions to propose')
    assert 'A material statement is one of four kinds' in system and 'a page with eight such statements yields eight evidence items' in system
    assert 'Decide links statement by statement' in system and 'A rumour or an unconfirmed report bears on a thesis exactly as a confirmed statement does' in system
    assert "[What to read out] The author's forecasts, ratings and price targets with their figures" in user and user.endswith('Return empty arrays only for a page with no business content.')
    assert schema['properties']['candidates']['items']['properties']['opens_as']['enum'] == extraction.ADMISSION_REASONS


def test_v18_sends_the_flat_answer_shape_the_arms_were_measured_with_not_v17s_account_per_paragraph():
    """D200: arms B3–B6 and the scale tests sent v18 with the flat shape (evidence, candidates, new_groups) and the page as
    text; the per-paragraph account is v17's shape alone (refuted, D199). Production sends what was measured."""
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v34.json'))
    shown = [{'view_id': 'v3', 'object_id': 'NVDA', 'looks_at': 'FY2027 data center revenue', 'question': 'q', 'due_day': '2027-02-24', 'dependencies': []}]
    setting, system, user, schema = extraction.request_for(cfg, dict(ITEM, text=MANDATORY_TEXT), MANDATORY_TEXT, shown, UNIVERSE)
    assert setting.prompt_version == 'T1-v18'
    assert list(schema['properties']) == ['evidence', 'candidates', 'new_groups']
    assert '[Paragraphs to account for]' not in user and '\np0001 ' not in user
    assert user.split('[Item] id ')[1].split('\n\n', 1)[1].startswith(MANDATORY_TEXT[:40])
    flat = {'evidence': [dict(EVIDENCE[0], quote='CoreWeave signed contracts for its A100 GPUs that run into 2029, chief executive Michael Intrator said on the call, and power constraints keep that capacity rented.', links=['v3'])], 'candidates': [], 'new_groups': []}
    assert model.check_schema(flat, schema) == []
    v17 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v33.json'))
    assert list(extraction.request_for(v17, dict(ITEM, text=MANDATORY_TEXT), MANDATORY_TEXT, shown, UNIVERSE)[3]['properties']) == ['paragraphs', 'extra', 'candidates', 'new_groups']


def test_a_statement_day_is_an_iso_day_or_unknown_never_a_month_a_range_or_the_publication_day():
    """D203: the writer and every reader take original_day as the day the statement was made. The model wrote 54 of 2,369 raw
    pieces of the three-month run with a month ("2026-03"), a range ("2026-07-05 to 2026-07-06") or text, and the writer filled 1,445
    unknown days with the publication day (D245: unknown stays unknown). The sift keeps the piece and blanks a non-day; the writer
    stores the blank."""
    piece = dict(EVIDENCE[0], quote=TEXT.split('。')[0] + '。', links=['v1'])
    for bad in ('2026-07-05 to 2026-07-06', '2026-03', '2025 (fall; exact day not stated)', 'Not stated'):
        kept, _, dropped = extraction.sift({'evidence': [dict(piece, original_day=bad)], 'candidates': []}, ITEM, TEXT, {'v1'}, UNIVERSE, english=True)
        assert len(kept) == 1 and kept[0]['original_day'] == '' and dropped == []
    kept, _, _ = extraction.sift({'evidence': [dict(piece, original_day='2026-05-20')], 'candidates': []}, ITEM, TEXT, {'v1'}, UNIVERSE, english=True)
    assert kept[0]['original_day'] == '2026-05-20'



# D236: the date by which the product that carries the value ships is a main driver; an event question that names its quarter
# ("by the end of Q3 2026") is an event, not a quarterly number (06-views ladder rule 6 is about figures). Case: the Morgan Stanley
# rack-cost page of 2026-07-06 (gnews:f66e1689ec2e27e7eab2a2dd), whose shipping question three of three v23 sends lost to the quarter rule.
def test_an_event_question_naming_a_quarter_is_not_a_quarterly_number():
    yes_no = [{'label': 'Yes', 'condition': 'First shipments by 2026-09-30', 'lo': None, 'hi': None},
              {'label': 'No', 'condition': 'No shipment by 2026-09-30', 'lo': None, 'hi': None}]
    ship = admitted('c1', measure='event', scope='Vera Rubin', event_type='shipment', looks_at='Whether first Vera Rubin shipments occur by the end of Q3 2026',
                    question='Will Nvidia begin shipping Vera Rubin by 2026-09-30?', rungs=yes_no, due_day='2026-09-30', year='2026')
    quarterly = admitted('c2', looks_at='Q3 FY2027 data center revenue', question='What will data center revenue be in Q3 FY2027?')
    data = {'new_groups': [], 'evidence': [dict(EVIDENCE[0], links=['c1', 'c2'])], 'candidates': [ship, quarterly]}
    _, kept, dropped, _ = extraction.sift_with_groups(data, ITEM, TEXT, set(), UNIVERSE, english=True)
    assert [c['id'] for c in kept] == ['c1'], dropped
    assert 'quarterly number' in dict(dropped)['c2']


# D191/D246: the schemas of role-v13..v15 alone name shared_quantity; every later version names the four reasons of
# ADMISSION_REASONS, so a new prompt version (role-v52) needs no code change to keep industry_aggregate open.
def test_a_new_prompt_version_names_the_current_four_reasons_without_a_code_change():
    def reasons(version):
        return extraction.schema_for(version)['properties']['candidates']['items']['properties']['opens_as']['enum']
    assert reasons('v51') == reasons('v52') == extraction.ADMISSION_REASONS
    assert reasons('v14') == extraction.ADMISSION_REASONS_V13
