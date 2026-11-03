"""D149 research groups in the default pipeline (docs/poc/grouping-improvement-plan.md Steps C/D as built, D164, D211): the extraction
request shows no stored group, so a candidate declares its matter's group with local ids and aliases; the code checks the references;
the writer creates a group when the first written thesis cites it, folds a declaration whose names hit a stored group into that group
(D166) and records memberships in the same transaction; matching only shows groups. Real ledgers on temporary paths; the universe file
the pipeline reads; a scripted model."""
import json
import os
import sys

from test_keyed_views import EVIDENCE, ITEM, TEXT, UNIVERSE, candidate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import extraction, model, placement, replay  # noqa: E402
from hivemind.views import matching, store, writing  # noqa: E402
from test_sequential_replay import setup_run, v108_send  # noqa: E402

NEW_GROUPS = [{'id': 'n1', 'name': 'Rubin platform ramp', 'scope': 'Vera Rubin production, shipments and first customer deployments in 2026–2027'},
              {'id': 'n2', 'name': 'Unused subject', 'scope': 'declared but cited by no candidate'}]
KEPT_GROUPS = [dict(NEW_GROUPS[0], aliases=[])]          # what the sift hands over: the cited declaration, aliases normalised


def grouped(cid, refs, **over):
    return candidate(cid, group_refs=refs, **over)


def test_the_schema_admits_only_local_group_ids_with_their_aliases():
    schema = extraction.schema_for('v74i')
    def raw(c):
        return {k: v for k, v in c.items() if k not in ('key_version', 'scope_source')}      # fields the sift adds, not the model
    ok = {'evidence': [], 'new_groups': [dict(NEW_GROUPS[0], aliases=['Rubin'])], 'candidates': [raw(grouped('c1', ['n1'], opens_as='main_driver', settled_by='the annual report'))]}
    assert model.check_schema(ok, schema) == []
    bad = {'evidence': [], 'new_groups': [], 'candidates': [raw(grouped('c1', ['g2'], opens_as='main_driver', settled_by='the annual report'))]}
    assert any('group_refs' in e for e in model.check_schema(bad, schema))
    assert 'aliases' in schema['properties']['new_groups']['items']['required']


def test_sift_keeps_well_referenced_candidates_and_only_cited_declarations():
    data = {'new_groups': NEW_GROUPS, 'evidence': [EVIDENCE[0], dict(EVIDENCE[0], id='e2', links=['c2']), dict(EVIDENCE[0], id='e3', links=['c3']), dict(EVIDENCE[0], id='e4', links=['c4'])],
            'candidates': [grouped('c1', ['n1']), grouped('c2', [], measure='total_revenue', scope='', evidence_ids=['e2']),
                           grouped('c3', ['g9'], measure='capex', scope='', evidence_ids=['e3']), grouped('c4', ['n1', 'n1'], measure='gross_margin', scope='', evidence_ids=['e4'])]}
    evidence, kept, dropped, new_groups = extraction.sift_with_groups(data, ITEM, TEXT, set(), UNIVERSE)
    assert [c['id'] for c in kept] == ['c1', 'c2']            # empty group_refs is allowed: a company's own financial line carries no group
    reasons = dict(dropped)
    assert "cites a group not declared in this answer: ['g9']" in reasons['c3'] and 'repeats a group' in reasons['c4']
    assert new_groups == KEPT_GROUPS                         # n2 was declared and never cited


def test_writer_creates_a_group_once_and_records_memberships_in_the_same_write(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    first = extraction.Handover([EVIDENCE[0], dict(EVIDENCE[0], id='e2', links=['c2'])],
                                [grouped('c1', ['n1']), grouped('c2', ['n1'], measure='product_revenue', scope='Vera standalone CPUs', looks_at='FY2027 Vera CPU revenue', evidence_ids=['e2'])],
                                [], 0, '', False, 0.0, KEPT_GROUPS)
    written = writing.write(conn, UNIVERSE, 1, ITEM, first, matching.Checked({'c1': ('new', None, []), 'c2': ('new', None, [])}, {}, [], {}), {})
    groups = [dict(r) for r in conn.execute('select * from thesis_groups')]
    assert [(g['group_id'], g['name']) for g in groups] == [('g1', 'Rubin platform ramp')]
    assert sorted(store.members_of_group(conn, 'g1')) == sorted(written.new_views.values())
    # a later item: one candidate joins the stored group, one is merged into an existing thesis and adds no membership
    later = extraction.Handover([dict(EVIDENCE[0], id='e5', links=['c3']), dict(EVIDENCE[0], id='e6', links=['c4'])],
                                [grouped('c3', ['g1'], measure='event', scope='SK Telecom AI factory', event_type='deployment', looks_at='SK Telecom AI factory deployment',
                                         rungs=[{'label': 'Yes', 'condition': 'deployed', 'lo': None, 'hi': None}, {'label': 'No', 'condition': 'not deployed', 'lo': None, 'hi': None}], due_day='2027-12-31', year='2027', evidence_ids=['e5']),
                                 grouped('c4', ['n1'], evidence_ids=['e6'])], [], 0, '', False, 0.0, [{'id': 'n1', 'name': 'Another name', 'scope': 'would duplicate g1 if written'}])
    dc = written.new_views['c1']
    written2 = writing.write(conn, UNIVERSE, 2, ITEM, later, matching.Checked({'c3': ('new', None, []), 'c4': ('merge', dc, [])}, {}, [], {}), {})
    assert [g['group_id'] for g in store.groups_of_view(conn, written2.new_views['c3'])] == ['g1']
    assert conn.execute('select count(*) from thesis_groups').fetchone()[0] == 1          # the merged candidate's declaration created nothing
    assert len(store.members_of_group(conn, 'g1')) == 3
    shown = store.groups_for_prompt(conn, ['NVDA'], 'Rubin shipments start')
    assert [g['group_id'] for g in shown] == ['g1'] and len(shown[0]['members']) == 3 and shown[0]['members'][0]['object_id'] == 'NVDA'
    assert 'research group: g1 "Rubin platform ramp"' in matching.describe_view(conn, dc, english=True)
    _, user = extraction.build_prompt(ITEM, TEXT, [], UNIVERSE, 'v74i')      # D211: the stored group is not shown; the standing instruction is
    assert extraction.GROUPS_INSTRUCTION in user and 'Rubin platform ramp' not in user


def test_the_replay_runs_the_grouped_contract_end_to_end(tmp_path):
    """The production path: the request shows the standing instruction and admits local ids only; the first declaration creates the
    group, the second item's declaration of the same names folds into it, and the handover keeps the cited declaration."""
    args, sent = setup_run(tmp_path), []
    send = v108_send()

    def recording(*parameters):
        if len(parameters) == 2:
            sent.append(parameters[1])
        return send(*parameters)
    result = replay.run(**args, transport=recording)
    assert result['failed'] == 0 and result['new_views'] == 2
    request = next(r for r in sent if r['response_format']['json_schema']['name'] == 'extraction')
    assert '[Research groups] None yet' in request['messages'][1]['content']
    assert request['response_format']['json_schema']['schema']['properties']['candidates']['items']['properties']['group_refs']['items']['pattern'] == '^(?:n[1-9][0-9]*)$'
    conn = store.open_db(args['views_path'])
    assert [dict(r) for r in conn.execute('select group_id, name from thesis_groups')] == [{'group_id': 'g1', 'name': 'Rubin rollout'}]
    assert sorted(store.members_of_group(conn, 'g1')) == ['v1', 'v2']
    saved = json.loads(conn.execute('select handover_json from handovers order by id limit 1').fetchone()[0])
    assert saved['new_groups'][0]['name'] == 'Rubin rollout' and saved['candidates'][0]['group_refs'] == ['n1']


def test_a_company_financial_line_cannot_found_a_group_but_may_join_one(tmp_path):
    """D164 (Alex, 2026-10-25): a group is an ongoing matter; a company's own lines belong to the company. A declaration cited
    only by financial lines creates nothing; the same declaration cited by an event creates the group, and the lines join it."""
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    lines_only = extraction.Handover([EVIDENCE[0], dict(EVIDENCE[0], id='e2', links=['c2'])],
                                     [grouped('c1', ['n1']), grouped('c2', ['n1'], measure='gross_margin', scope='', looks_at='FY2027 gross margin', evidence_ids=['e2'])],
                                     [], 0, '', False, 0.0, [{'id': 'n1', 'name': 'AI infrastructure demand', 'scope': 'a company folder in disguise'}])
    written = writing.write(conn, UNIVERSE, 1, ITEM, lines_only, matching.Checked({'c1': ('new', None, []), 'c2': ('new', None, [])}, {}, [], {}), {})
    assert conn.execute('select count(*) from thesis_groups').fetchone()[0] == 0
    assert any('cited by no written thesis that tracks a matter; not created' in n for n in written.notes)
    event = grouped('c3', ['n1'], measure='event', scope='Vera Rubin', event_type='shipment', looks_at='Vera Rubin production shipments', question='Will Rubin ship in 2026?',
                    rungs=[{'label': 'Yes', 'condition': 'shipped', 'lo': None, 'hi': None}, {'label': 'No', 'condition': 'not shipped', 'lo': None, 'hi': None}], due_day='2026-12-31', year='2026', evidence_ids=['e3'])
    cpu = grouped('c4', ['n1'], measure='product_revenue', scope='Vera standalone CPUs', looks_at='FY2027 Vera CPU revenue', question='How much?', evidence_ids=['e4'])
    margin = grouped('c5', ['n1'], measure='gross_margin', scope='', looks_at='FY2027 gross margin', question='Margin?', evidence_ids=['e5'])
    second = extraction.Handover([dict(EVIDENCE[0], id=f'e{i}', links=[c]) for i, c in ((3, 'c3'), (4, 'c4'), (5, 'c5'))], [event, cpu, margin], [], 0, '', False, 0.0,
                                 [{'id': 'n1', 'name': 'Vera Rubin rollout', 'scope': 'production shipments, customer deployments and the Vera CPU'}])
    written2 = writing.write(conn, UNIVERSE, 2, ITEM, second, matching.Checked({'c3': ('new', None, []), 'c4': ('new', None, []), 'c5': ('new', None, [])}, {}, [], {}), {})
    assert [dict(r)['name'] for r in conn.execute('select name from thesis_groups')] == ['Vera Rubin rollout']
    assert sorted(store.members_of_group(conn, 'g1')) == sorted(written2.new_views.values())      # the margin line joins the group an event founded


RUBIN_DECLARATION = {'id': 'n1', 'name': 'NVIDIA Blackwell and Rubin rollout', 'scope': 'Blackwell and Vera Rubin production shipments and customer deployments',
                     'aliases': ['Vera Rubin', 'Rubin', 'Blackwell', 'Vera', 'NVIDIA', 'VR']}


def shipment(cid, refs, **over):
    return grouped(cid, refs, measure='event', scope='Vera Rubin', event_type='shipment', looks_at='Vera Rubin production shipments', question='Will Vera Rubin ship in volume by 2026-12-31?',
                   rungs=[{'label': 'Yes', 'condition': 'shipped', 'lo': None, 'hi': None}, {'label': 'No', 'condition': 'not shipped', 'lo': None, 'hi': None}], due_day='2026-12-31', year='2026', **over)


def test_aliases_decide_group_identity_and_membership(tmp_path):
    """D166: a group is a matter with names. Company names are never aliases; a thesis whose own text carries a group's name
    joins it; a declaration whose names hit a stored group is that group and creates nothing (the SK Telecom case)."""
    from hivemind.views import groups
    assert groups.clean_aliases(RUBIN_DECLARATION['aliases'], RUBIN_DECLARATION['name'], UNIVERSE) == ['NVIDIA Blackwell and Rubin rollout', 'Vera Rubin', 'Rubin', 'Blackwell', 'Vera']
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    first = extraction.Handover([EVIDENCE[0], dict(EVIDENCE[0], id='e2', links=['c2'])],
                                [shipment('c1', ['n1']), grouped('c2', [], measure='product_revenue', scope='Vera standalone CPUs', looks_at='FY2027 standalone Vera CPU revenue',
                                                                   question='Can demand for Vera standalone CPUs lift FY2027 CPU revenue above $20 billion?', evidence_ids=['e2'])],
                                [], 0, '', False, 0.0, [RUBIN_DECLARATION])
    written = writing.write(conn, UNIVERSE, 1, ITEM, first, matching.Checked({'c1': ('new', None, []), 'c2': ('new', None, [])}, {}, [], {}), {})
    rows = [dict(r) for r in conn.execute('select view_id, basis from thesis_group_members order by id')]
    assert rows == [{'view_id': written.new_views['c1'], 'basis': 'model'}, {'view_id': written.new_views['c2'], 'basis': 'alias:Vera'}]
    assert groups.stored_groups(conn)[0]['aliases'] == ['NVIDIA Blackwell and Rubin rollout', 'Vera Rubin', 'Rubin', 'Blackwell', 'Vera']
    # the SK Telecom item: the model declares its own group, whose names hit the stored Rubin group → the deployment joins g1, nothing new is created
    sk = grouped('c3', ['n1'], measure='event', scope='SK Telecom AI factory', event_type='deployment', looks_at='SK Telecom AI factory deployment',
                 question='Will SK Telecom bring its first 2-gigawatt-scale NVIDIA Vera Rubin DSX AI factory online in 2027?',
                 rungs=[{'label': 'Yes', 'condition': 'online', 'lo': None, 'hi': None}, {'label': 'No', 'condition': 'not online', 'lo': None, 'hi': None}], due_day='2027-12-31', year='2027', evidence_ids=['e3'])
    second = extraction.Handover([dict(EVIDENCE[0], id='e3', links=['c3'])], [sk], [], 0, '', False, 0.0,
                                 [{'id': 'n1', 'name': 'SK Telecom AI factory deployment', 'scope': "SK Telecom's Korean Vera Rubin AI factory", 'aliases': ['SK Telecom', 'Vera Rubin']}])
    written2 = writing.write(conn, UNIVERSE, 2, ITEM, second, matching.Checked({'c3': ('new', None, [])}, {}, [], {}), {})
    assert conn.execute('select count(*) from thesis_groups').fetchone()[0] == 1
    assert [dict(r) for r in conn.execute('select group_id, basis from thesis_group_members where view_id=?', (written2.new_views['c3'],))] == [{'group_id': 'g1', 'basis': 'model'}]
    assert any('is stored group g1 by its names; not created' in n for n in written2.notes)
    # a company's own financial line does not join by alias even when its question carries the group's name (the discarded v21 seed put
    # NVIDIA's total revenue into the Rubin group through a generic alias); the model may still cite a group for it
    line = grouped('c9', [], measure='total_revenue', scope='', looks_at='FY2027 total revenue', question='Can Rubin demand lift FY2027 total revenue above $400 billion?', evidence_ids=['e9'])
    written_line = writing.write(conn, UNIVERSE, 5, ITEM, extraction.Handover([dict(EVIDENCE[0], id='e9', links=['c9'])], [line], [], 0, '', False, 0.0, []),
                                 matching.Checked({'c9': ('new', None, [])}, {}, [], {}), {})
    assert conn.execute('select count(*) from thesis_group_members where view_id=?', (written_line.new_views['c9'],)).fetchone()[0] == 0
    # a thesis that names nothing of the matter stays out; one that names a party of a different matter joins only that one
    other = grouped('c4', [], measure='event', scope='Amazon Leo', event_type='launch', looks_at='Amazon Leo initial satellite service', question='Does Amazon Leo start service in 2026?', object='AMZN',
                    rungs=[{'label': 'Yes', 'condition': 'y', 'lo': None, 'hi': None}, {'label': 'No', 'condition': 'n', 'lo': None, 'hi': None}], due_day='2026-12-31', year='2026', period_start='2026-01-01', period_end='2026-12-31', evidence_ids=['e4'])
    third = extraction.Handover([dict(EVIDENCE[0], id='e4', links=['c4'])], [other], [], 0, '', False, 0.0, [])
    written3 = writing.write(conn, UNIVERSE, 3, dict(ITEM, object_identifiers=[{'value': 'AMZN'}]), third, matching.Checked({'c4': ('new', None, [])}, {}, [], {}), {})
    assert conn.execute('select count(*) from thesis_group_members where view_id=?', (written3.new_views['c4'],)).fetchone()[0] == 0
    # the request names a question's group with its aliases in the question's takes line
    shown = store.groups_for_prompt(conn, ['NVDA'], 'Rubin')
    assert isinstance(shown[0]['aliases'], list) and store.group(conn, 'g1')['aliases'][1] == 'Vera Rubin'      # aliases read back as a list, never as JSON text
    view_id = written.new_views['c1']
    view = dict(store.view(conn, view_id), key=store.view_key(conn, view_id) or {}, groups=store.groups_of_view(conn, view_id))
    assert '(also called Vera Rubin, Rubin, Blackwell, Vera, SK Telecom AI factory deployment, SK Telecom)' in placement.takes(view)   # D166 (2026-11-01, D257): the SK Telecom declaration's other names joined g1
