"""Code requirements from the two-scope evidence-basis experiment plan."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest
import basis_replay as basis
import replay
import study


def snapshot(name='rubin', cutoff=532):
    data = json.loads((basis.FROZEN / 'input.json').read_text())
    return next(s for s in data[name] if s['cutoff_seq'] == cutoff)


def review_answer(snap):
    return {'assessments': {r['source_ref']: {'role': 'context',
                           'reason': 'Stored source retained for evaluation.'} for r in basis.catalog(snap)}}


def summary(ref='source_e748'):
    return {'status': 'supported', 'conclusion': 'System validation is a readiness signal.',
            'arguments': [{'statement': 'The system was validated.', 'role': 'supports', 'sources': [ref]}],
            'limitations': [], 'watch_questions': []}


def test_one_source_keeps_all_real_origins_without_duplicating_evidence():
    """Plan source identity: shared e55 is one record, with two separate origin paths."""
    records = basis.catalog(snapshot(cutoff=379))
    source = next(r for r in records if r['source_ref'] == 'source_e55')
    assert source['origin_paths'] == [{'view_id': 'v7', 'judgement_id': 350}, {'view_id': 'v15', 'judgement_id': 355}]
    assert len(records) == 46


def test_all_six_current_sets_require_one_row_each_and_reject_missing_or_unknown():
    """Plan completeness: every real current source is judged exactly once."""
    data = json.loads((basis.FROZEN / 'input.json').read_text())
    count = 0
    for name, snapshots in data.items():
        for snap in snapshots:
            answer = review_answer(snap)
            value = basis.compile_basis(answer, snap, name)
            count += len(value['rows'])
            missing = copy.deepcopy(answer)
            missing['assessments'].pop(next(iter(missing['assessments'])))
            with pytest.raises(ValueError, match='required'):
                basis.compile_basis(missing, snap, name)
            repeated = copy.deepcopy(answer)
            repeated['assessments']['invented'] = {'role': 'context', 'reason': 'Unknown source.'}
            with pytest.raises(ValueError, match='not allowed'):
                basis.compile_basis(repeated, snap, name)
    assert count == 274


def test_new_risk_is_not_removed_when_the_summary_only_cites_positive_progress():
    """Plan separate basis: rendering selection cannot delete a retained risk."""
    snap = snapshot()
    answer = review_answer(snap)
    answer['assessments']['source_e724']['role'] = 'challenges'
    state = basis.compile_basis(answer, snap, 'rubin')
    card = basis.compile_card(summary(), state['rows'], snap, 'rubin', state)
    assert [r['source_ref'] for r in card['basis']['challenges']] == ['source_e724']
    assert 'source_e724' not in card['summary']['arguments'][0]['sources']


def test_new_refs_remove_all_32_previously_observed_wrong_pair_assemblies():
    """Plan provenance owner: resolve source handles using stored origins, never model pairs."""
    audit = json.loads((basis.FROZEN / 'reference-audit.json').read_text())
    assert len(audit['citation_errors']) == 32
    for error in audit['citation_errors']:
        name, _, cutoff = error['step'].split('-')
        snap = snapshot(name, int(cutoff))
        ref = 'source_' + error['evidence_id']
        card = basis.compile_card(summary(ref), basis.catalog(snap), snap, name)
        source = basis.visible_sources(card)[0]
        assert error['view_id'] not in {o['view_id'] for o in source['origin_paths']}
        assert {o['view_id'] for o in source['origin_paths']} == set(error['actual_views'])


def test_delta_exposes_risk_and_validation_arrivals_and_keeps_prior_sources():
    """Plan temporal path: source changes remain explicit even when the leaf rung is unchanged."""
    before, after = snapshot(cutoff=379), snapshot(cutoff=532)
    changes = basis.change_set(before, after)
    assert {'source_e724', 'source_e748'} <= set(changes['added'])
    assert 'source_e55' in changes['retained']
    assert 'v7' in changes['changed_views']
    assert next(t for t in before['theses'] if t['id'] == 'v7')['assessment']['position'] == next(t for t in after['theses'] if t['id'] == 'v7')['assessment']['position']


def test_probe_is_limited_to_card_sources_and_future_sources_fail():
    """Plan visibility: a real but hidden source is not valid for this reader."""
    snap = snapshot()
    card = basis.compile_card(summary(), basis.catalog(snap), snap, 'rubin')
    answer = {'facets': [{'facet': f, 'answer': 'A readiness signal, not completed shipments.',
                         'sources': ['source_e748']} for f in replay.SCOPES['rubin']['facets']]}
    assert basis.validate_probe(answer, card, replay.SCOPES['rubin']) is answer
    answer['facets'][0]['sources'] = ['source_e724']
    with pytest.raises(ValueError):
        basis.validate_probe(answer, card, replay.SCOPES['rubin'])
    with pytest.raises(ValueError):
        basis.compile_card(summary('source_e748'), basis.catalog(snapshot(cutoff=379)), snapshot(cutoff=379), 'rubin')


def test_prepare_cli_preserves_frozen_input_and_budget(tmp_path):
    """Plan entry point: preparation copies the frozen six-snapshot input and makes no model call."""
    out = tmp_path / 'basis-study'
    result = subprocess.run([sys.executable, str(Path(basis.__file__)), 'prepare', '--out', str(out)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads((out / 'input.json').read_text()) == json.loads((basis.FROZEN / 'input.json').read_text())
    assert json.loads((out / 'budget.json').read_text())['attempts'] == []
    assert json.loads((out / 'manifest.json').read_text())['max_attempts'] == 42
