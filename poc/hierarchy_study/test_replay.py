"""Requirements in the two-scope replay plan, exercised on sealed records without credentials."""
import copy
import json
import subprocess
import sys

import pytest
import replay
import study


def snapshot(name='rubin', cutoff=379):
    conn = study.read_only(replay.SOURCE)
    result = study.snapshot(conn, set(replay.SCOPES[name]['ids']), cutoff)
    conn.close()
    result['as_of'] = {66: '2026-07-24', 67: '2026-07-24', 379: '2026-08-05', 532: '2026-08-12'}[cutoff]
    return result


def positive(snap, vid='v7', eid='e55'):
    thesis = next(t for t in snap['theses'] if t['id'] == vid)
    source = next(e for e in thesis['evidence'] if e['evidence_id'] == eid)
    return {'status': 'supported', 'conclusion': 'Customer deployment is planned, not completed.',
            'arguments': [{'statement': source['quote'], 'role': 'context',
                           'reason': 'A planned deployment is not confirmation of production shipments.',
                           'references': [{'view_id': vid, 'evidence_ids': [eid]}]}],
            'limitations': ['A future plan does not confirm delivery.'], 'watch_questions': []}


def test_selected_shared_evidence_binds_only_selected_view_and_version():
    """Plan citation association: shared e55 must not turn v7 into v15."""
    snap = snapshot()
    card = replay.make_card(positive(snap), snap, 'rubin')
    ref = card['arguments'][0]['references'][0]
    assert ref == {'view_id': 'v7', 'evidence_ids': ['e55'], 'judgement_id': 350}
    assert 'v15' in card['unused_ids']
    assert card['as_of_seq'] == 379


def test_current_pairs_refuse_unknown_cross_view_and_future_evidence():
    """Plan closed references: an existing global ID is not enough."""
    snap = snapshot()
    for vid, eid in [('v7', 'e724'), ('v7', 'e471'), ('invented', 'e55')]:
        answer = positive(snap)
        answer['arguments'][0]['references'] = [{'view_id': vid, 'evidence_ids': [eid]}]
        with pytest.raises(ValueError):
            replay.validate(answer, snap)


def test_probe_cannot_recover_a_view_hidden_by_main_card():
    """Plan probe visibility: v15/e55 exists in data but is not on this card."""
    snap = snapshot()
    card = replay.make_card(positive(snap), snap, 'rubin')
    answer = {'facets': [{'facet': facet, 'answer': 'Only this source is supplied.',
                         'references': [{'view_id': 'v7', 'evidence_ids': ['e55']}]}
                        for facet in replay.SCOPES['rubin']['facets']]}
    assert replay.validate_probe(answer, card, snap, replay.SCOPES['rubin']) is answer
    hidden = copy.deepcopy(answer)
    hidden['facets'][0]['references'][0]['view_id'] = 'v15'
    with pytest.raises(ValueError, match='absent from its card'):
        replay.validate_probe(hidden, card, snap, replay.SCOPES['rubin'])


def test_material_gate_ignores_unrelated_sequence_but_detects_changed_research():
    """Plan no-op: a new global sequence alone must not rewrite a main thesis."""
    snap = snapshot(cutoff=66)
    card = replay.make_card(positive(snap), snap, 'rubin')
    assert not replay.update_required(card, snapshot(cutoff=67))
    assert replay.update_required(card, snapshot(cutoff=532))


def test_started_request_is_not_resent_and_changed_request_is_refused(tmp_path, monkeypatch):
    """Plan restart/config table: no uncertain retry and no mismatched cache."""
    calls = replay.Calls(tmp_path, 1)
    response_schema = study.obj({'result': study.STRING})
    payload = {'question': 'Pinned request'}
    request = study.model.build_request(calls.setting, 'Pinned prompt', json.dumps(payload, ensure_ascii=False), response_schema, 'hierarchy_result', calls.cfg.provider)
    path = tmp_path / 'sample-1/uncertain.json'
    study.write_json(path, {'status': 'started', 'request': request})
    sent = []
    monkeypatch.setattr(study.model, 'call', lambda *a, **k: sent.append(True))
    with pytest.raises(RuntimeError, match='no automatic resend'):
        calls.call('uncertain', 'Pinned prompt', payload, response_schema)
    with pytest.raises(ValueError, match='Stored request differs'):
        calls.call('uncertain', 'Changed prompt', payload, response_schema)
    assert not sent
    calls.archive.conn.close()


def test_prepare_entrypoint_preserves_six_nonempty_historical_snapshots(tmp_path):
    """Plan input bounds through the real CLI default source; no model calls."""
    out = tmp_path / 'experiment'
    result = subprocess.run([sys.executable, str(study.ROOT / 'poc/hierarchy_study/replay.py'), 'prepare', '--out', str(out)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    data = json.loads((out / 'input.json').read_text())
    judged = 0
    for snaps in data.values():
        for snap in snaps:
            assert snap['theses']
            for thesis in snap['theses']:
                assert thesis['created_seq'] <= snap['cutoff_seq']
                assert thesis['assessment']['seq'] <= snap['cutoff_seq']
                assert all(e['created_seq'] <= snap['cutoff_seq'] for e in thesis['evidence'])
                judged += 1
    assert judged == 40
