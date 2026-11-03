"""D184: a candidate question opens only for one of four stated reasons, with the public material that settles it; the schema
requires both fields and code checks their shape. D185: a binding obligation is due within 18 months, exempt from the next-year rule
on quantities."""
import json
import os
import sys

from test_keyed_views import EVIDENCE, ITEM, TEXT, UNIVERSE, candidate
from test_sequential_replay import setup_run, v108_send

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction, replay  # noqa: E402

ADMITTED = {'opens_as': 'main_driver', 'settled_by': 'NVIDIA FY2027 annual earnings release', 'group_refs': []}


def admitted(cid, **over):
    return candidate(cid, **{**ADMITTED, **over})


def test_the_schema_requires_the_reason_and_the_settling_material():
    schema = extraction.schema_for('v74i')
    fields = schema['properties']['candidates']['items']['properties']
    assert {'opens_as', 'settled_by'} <= set(schema['properties']['candidates']['items']['required'])
    assert fields['opens_as']['enum'] == extraction.ADMISSION_REASONS == ['main_driver', 'industry_aggregate', 'policy_stage', 'binding_obligation']


def test_a_candidate_without_its_settling_material_is_dropped():
    data = {'new_groups': [], 'evidence': [EVIDENCE[0], dict(EVIDENCE[0], id='e2', links=['c2'])],
            'candidates': [admitted('c1'), admitted('c2', settled_by='  ', evidence_ids=['e2'])]}
    _, kept, dropped, _ = extraction.sift_with_groups(data, ITEM, TEXT, {'v1'}, UNIVERSE)
    assert [c['id'] for c in kept] == ['c1'] and 'settled_by is empty' in dict(dropped)['c2']


def test_binding_obligation_horizon():
    def one(**over):
        data = {'new_groups': [], 'evidence': [EVIDENCE[0]], 'candidates': [admitted('c1', **over)]}
        _, kept, dropped, _ = extraction.sift_with_groups(data, ITEM, TEXT, set(), UNIVERSE)
        return [c['id'] for c in kept], dict(dropped).get('c1', '')
    binding = dict(opens_as='binding_obligation', measure='financing_amount', scope='Ohio guarantee', year='2028', unit='USD')
    assert one(**binding, due_day='2027-06-30') == (['c1'], '')                      # within 548 days of 2026-05-20, year rule waived (D185)
    kept, reason = one(**binding, due_day='2028-06-30')
    assert kept == [] and 'binding obligation due beyond 18 months' in reason
    kept, reason = one(opens_as='industry_aggregate', measure='spend_total', scope='five hyperscalers', year='2028', due_day='2027-06-30')
    assert kept == [] and 'beyond next year' in reason


def test_an_impossible_calendar_date_on_a_binding_obligation_is_refused_not_a_crash():
    data = {'new_groups': [], 'evidence': [EVIDENCE[0]], 'candidates': [admitted('c1', opens_as='binding_obligation', measure='event', scope='Ohio guarantee', event_type='deal_close', due_day='2026-06-31')]}
    _, kept, dropped, _ = extraction.sift_with_groups(data, ITEM, TEXT, set(), UNIVERSE)
    assert kept == [] and 'due_day is not a real date' in dict(dropped)['c1']


def test_binding_obligation_horizon_applies_to_events_too():
    data = {'new_groups': [], 'evidence': [EVIDENCE[0]], 'candidates': [admitted('c1', opens_as='binding_obligation', measure='event', scope='Ohio guarantee', event_type='deal_close', year='2028', due_day='2028-06-30')]}
    _, kept, dropped, _ = extraction.sift_with_groups(data, ITEM, TEXT, set(), UNIVERSE)
    assert kept == [] and 'binding obligation due beyond 18 months' in dict(dropped)['c1']


def test_a_statement_day_is_an_iso_day_or_unknown_never_a_month_a_range_or_the_publication_day():
    """D203: the writer and every reader take original_day as the day the statement was made. The model wrote 54 of 2,369 raw
    pieces of the three-month run with a month ("2026-03"), a range ("2026-07-05 to 2026-07-06") or text, and the writer filled 1,445
    unknown days with the publication day (D245: unknown stays unknown). The sift keeps the piece and blanks a non-day; the writer
    stores the blank."""
    piece = dict(EVIDENCE[0], quote=TEXT.split('。')[0] + '。', links=['v1'])
    for bad in ('2026-07-05 to 2026-07-06', '2026-03', '2025 (fall; exact day not stated)', 'Not stated'):
        kept, _, dropped = extraction.sift({'evidence': [dict(piece, original_day=bad)], 'candidates': []}, ITEM, TEXT, {'v1'}, UNIVERSE)
        assert len(kept) == 1 and kept[0]['original_day'] == '' and dropped == []
    kept, _, _ = extraction.sift({'evidence': [dict(piece, original_day='2026-05-20')], 'candidates': []}, ITEM, TEXT, {'v1'}, UNIVERSE)
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
    _, kept, dropped, _ = extraction.sift_with_groups(data, ITEM, TEXT, set(), UNIVERSE)
    assert [c['id'] for c in kept] == ['c1'], dropped
    assert 'quarterly number' in dict(dropped)['c2']


def test_the_replay_writes_an_admitted_candidate_with_its_reason_and_settling_material(tmp_path):
    """The production path end to end: the request asks for the four reasons and the stored handover keeps both fields."""
    args, sent = setup_run(tmp_path), []
    send = v108_send()

    def recording(*parameters):
        if len(parameters) == 2:
            sent.append(parameters[1])
        return send(*parameters)
    result = replay.run(**args, transport=recording)
    assert result['failed'] == 0 and result['new_views'] == 2
    extraction_request = next(r for r in sent if r['response_format']['json_schema']['name'] == 'extraction')
    assert extraction_request['response_format']['json_schema']['schema']['properties']['candidates']['items']['properties']['opens_as']['enum'] == extraction.ADMISSION_REASONS
    import sqlite3
    with sqlite3.connect(args['views_path']) as db:
        saved = json.loads(db.execute('select handover_json from handovers order by id limit 1').fetchone()[0])
    assert saved['candidates'][0]['opens_as'] == 'main_driver' and saved['candidates'][0]['settled_by'] == 'the FY2027 annual report'


def test_the_request_ends_with_the_review_check_and_names_no_empty_answer_condition():
    """AGENTS §6 (2026-10-30, loop log rows 35–39): a test the model must apply to each statement is a check at the very end of the
    same prompt; the user message ends with the review file after the closing line, which says nothing about empty arrays."""
    item = dict(ITEM, text=TEXT, category='T7')
    _, _, user, _ = extraction.request_for(config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v108.json')), item, TEXT, [], UNIVERSE)
    review = open(os.path.join(ROOT, 'src', 'hivemind', 'prompts', 'review-v74i.txt'), encoding='utf-8').read().strip()
    assert user.endswith('(FY2027, or 2026 for a calendar year).\n\n' + review) and 'empty arrays' not in user
