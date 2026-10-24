"""The in-pipeline grouping contract, using real stored article text and real SQLite writes."""
import copy
import json

import pytest
import ingestion_groups as ingest
import study
from hivemind import dispatch, extraction, universe
from hivemind.views import matching, store, writing


def fixture():
    corpus = study.read_only(ingest.CORPUS)
    item = dict(corpus.execute('select * from items where input_id=?', (ingest.ITEM_IDS[0],)).fetchone())
    corpus.close()
    item['object_identifiers'] = json.loads(item['object_identifiers'])
    old = study.read_only(ingest.SEALED)
    quote = old.execute("select quote from evidence where evidence_id='e7'").fetchone()[0]
    old.close()
    return item, {'candidates': [{'id': 'c1', 'object': 'NVDA', 'kind': 'company',
        'looks_at': 'Vera Rubin production shipment timing',
        'question': 'Will NVIDIA begin Vera Rubin production shipments by December 31, 2026?',
        'rungs': [{'label': 'yes', 'condition': 'Production shipments start by 2026-12-31.'},
                  {'label': 'no', 'condition': 'Production shipments do not start by 2026-12-31.'}],
        'due_day': '2026-12-31', 'year': '2026', 'evidence_ids': ['e1']}],
        'evidence': [{'id': 'e1', 'quote': quote,
        'one_line': 'NVIDIA expects Vera Rubin production shipments in the second half of 2026.',
        'speaker': 'NVIDIA management', 'original_who': 'NVIDIA', 'original_day': '2026-02-25',
        'tier': 'party_statement', 'event_time': '2026 H2', 'links': ['c1']}]}


def new_answer():
    return {'candidates': [{'id': 'c1', 'outcome': 'new', 'target_view_id': '', 'reason': 'Distinct dated question.', 'dependencies': []}],
            'evidence': [], 'new_groups': [{'id': 'new_g1', 'title': 'Product commercialization',
            'question': 'Can product readiness become customer deliveries?', 'scope': 'Delivery and deployment.'}],
            'memberships': [{'thesis_id': 'c1', 'group_id': 'new_g1', 'reason': 'Shipment timing is part of commercialization.'}]}


def test_english_handover_passes_original_sift_and_roundtrips_control_enums():
    """Plan adapter: real quote and original checks, without translating prose."""
    item, raw = fixture()
    assert ingest.translate_controls(ingest.translate_controls(raw), reverse=True) == raw
    handover = ingest.sift(raw, item, [])
    assert len(handover.candidates) == len(handover.evidence) == 1
    assert handover.candidates[0]['kind'] == 'company'
    assert handover.evidence[0]['quote'] == raw['evidence'][0]['quote']
    invalid = copy.deepcopy(raw)
    invalid['evidence'][0]['quote'] = 'A sentence absent from the real article.'
    assert ingest.sift(invalid, item, []).candidates == []


def test_original_write_and_group_write_are_one_transaction(tmp_path):
    """Plan atomicity and ID resolution: failure after creating a thesis leaves neither thesis nor group."""
    conn = ingest.open_experiment_db(tmp_path / 'views.sqlite')
    item, raw = fixture()
    handover = ingest.sift(raw, item, [])
    uni = universe.load(str(study.ROOT / 'poc/universe.json'))
    answer = new_answer()
    checked = ingest.check_matching(conn, uni, answer, handover, matching.Lists({'c1': []}, {}), [])
    assert checked.refusals == []
    ingest.check_groups(answer, checked, set(), [])
    written = writing.write(conn, uni, 1, item, handover, checked, {})
    affected = ingest.write_groups(conn, answer, checked, written, 1, item)
    assert affected == ['g1']
    assert tuple(conn.execute('select group_id,view_id from group_members').fetchone()) == ('g1', written.new_views['c1'])
    assert store.view(conn, written.new_views['c1'])['kind'] == 'company'
    assert conn.execute('select count(*) from dependencies').fetchone()[0] == 0
    conn.rollback()
    assert conn.execute('select count(*) from views').fetchone()[0] == 0
    assert conn.execute('select count(*) from research_groups').fetchone()[0] == 0
    assert conn.execute('select count(*) from group_members').fetchone()[0] == 0


def test_group_cannot_reference_unseen_discarded_or_duplicate_members():
    """Plan closed membership set is checked separately from the original matcher."""
    checked = matching.Checked({'c1': (matching.OUTCOMES[2], None, [])}, {}, [], {})
    for transform in ['unseen', 'discarded', 'duplicate', 'empty_group']:
        answer = new_answer()
        if transform == 'unseen': answer['memberships'][0]['thesis_id'] = 'v999'
        if transform == 'discarded': answer['memberships'][0]['thesis_id'] = 'c2'
        if transform == 'duplicate': answer['memberships'].append(answer['memberships'][0])
        if transform == 'empty_group': answer['memberships'] = []
        with pytest.raises(ValueError):
            ingest.check_groups(answer, checked, set(), [])


def test_visible_groups_follow_actual_shown_members_and_existing_target_resolves(tmp_path):
    """Plan natural retrieval and merge: groups arrive via visible members; merged candidates keep old identity."""
    conn = ingest.open_experiment_db(tmp_path / 'views.sqlite')
    item, raw = fixture(); handover = ingest.sift(raw, item, [])
    uni = universe.load(str(study.ROOT / 'poc/universe.json')); answer = new_answer()
    checked = ingest.check_matching(conn, uni, answer, handover, matching.Lists({'c1': []}, {}), [])
    written = writing.write(conn, uni, 1, item, handover, checked, {})
    ingest.write_groups(conn, answer, checked, written, 1, item); conn.commit()
    assert ingest.visible_groups(conn, set()) == []
    assert ingest.visible_groups(conn, {'v999'}) == []
    assert [g['group_id'] for g in ingest.visible_groups(conn, {'v1'})] == ['g1']
    merged = matching.Checked({'c1': (matching.OUTCOMES[0], 'v1', [])}, {}, [], {})
    answer['new_groups'] = []; answer['memberships'][0]['group_id'] = 'g1'
    ingest.check_groups(answer, merged, {'v1'}, ingest.visible_groups(conn, {'v1'}))
    result = ingest.write_groups(conn, answer, merged, writing.Written({'v1'}, {}, {}, []), 2, item)
    assert result == ['g1']
    assert conn.execute('select count(*) from group_members').fetchone()[0] == 1
    unchanged = ingest.write_groups(conn, answer, merged, writing.Written(set(), {}, {}, []), 3, item)
    assert unchanged == []


def test_resending_processed_article_never_calls_model(tmp_path):
    """Plan resend path uses the real dispatch skip decision."""
    conn = ingest.open_experiment_db(tmp_path / 'views.sqlite'); item, _ = fixture()
    uni = universe.load(str(study.ROOT / 'poc/universe.json'))
    dispatch.mark(conn, item, 1, 'handed_over'); conn.commit()
    class NoCalls:
        def stage(self, *args, **kwargs):
            raise AssertionError('Model must not be called for a processed item')
    assert ingest.process(conn, NoCalls(), uni, item, 3, True)['route'] == 'skipped'


def test_complete_ingestion_uses_original_pipeline_functions_and_commits_groups(tmp_path):
    """Plan user path: a full item enters dispatch, extraction checks, matching, writer and group commit."""
    conn = ingest.open_experiment_db(tmp_path / 'views.sqlite'); item, raw = fixture()
    uni = universe.load(str(study.ROOT / 'poc/universe.json'))
    class Calls:
        cfg = study.config.load(str(study.ROOT / 'poc/config/poc-v7.json'))
        names = []
        def stage(self, name, prompt, payload, schema, setting):
            self.names.append(name)
            value = dict(raw, relationship_hints=[]) if name.endswith('extract') else new_answer()
            assert study.model.check_schema(value, schema) == []
            return value
    calls = Calls()
    result = ingest.process(conn, calls, uni, item, 1, True)
    assert result['affected_groups'] == ['g1']
    assert result['new_views'] == {'c1': 'v1'}
    assert result['views'][0]['question'] == raw['candidates'][0]['question']
    assert result['members'][0]['view_id'] == 'v1'
    assert calls.names == ['item1-extract', 'item1-match']
    before = len(calls.names)
    assert ingest.process(conn, calls, uni, item, 1, True)['route'] == 'skipped'
    assert len(calls.names) == before


def test_existing_extraction_hint_resolves_new_identity_without_another_model_decision():
    """Diagnostic: a retained extraction relation survives candidate-ID resolution; unknown targets fail."""
    checked = matching.Checked({'c1': (matching.OUTCOMES[2], None, [])}, {}, [], {})
    written = writing.Written({'v2'}, {'c1': 'v2'}, {}, [])
    hint = {'candidate_id': 'c1', 'related_view_ids': ['v1'], 'broader_question': 'How is the platform commercialized?', 'reason': 'The deployment uses the platform.'}
    assert ingest.resolve_hints([hint], checked, written, {'v1'})[0]['source'] == 'v2'
    with pytest.raises(ValueError, match='not visible'):
        ingest.resolve_hints([hint], checked, written, set())
