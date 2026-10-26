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
