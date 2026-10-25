"""The subject-names projection (docs/research/2026-10-25-subject-names/plan.md): names become IDs by code; the shapes
the model got wrong before cannot be expressed."""
import copy
import json
from pathlib import Path

import pytest

import subject_names as names

SOURCE = Path(__file__).resolve().parents[2] / 'poc/reports/2026-10-25-direct-subjects-01/sample-2-retained/item3-extract.json'
OFFERED = [{'thread_id': 'g2', 'name': 'SK Telecom AI factory rollout', 'scope': 'The planned Korea AI Cloud and AI factory build.'},
           {'thread_id': 'g1', 'name': 'Vera Rubin platform rollout', 'scope': 'NVIDIA’s Vera Rubin platform rollout.'}]


def stored_answer():
    """A real D147 answer (three candidates: v1 Rubin shipments, c1 PC SoC, c2 OpenAI deployment) rewritten in the new shape."""
    raw = copy.deepcopy(json.loads(SOURCE.read_text())['answer'])
    raw.pop('threads')
    for candidate in raw['candidates']:
        candidate.pop('thread_ids')
    by_id = {c['id']: c for c in raw['candidates']}
    by_id['v1']['subjects'] = [{'existing': 'Vera Rubin platform rollout', 'new_name': '', 'new_scope': ''}]
    by_id['c1']['subjects'] = [{'existing': 'none', 'new_name': 'Windows PC SoC rollout', 'new_scope': 'NVIDIA’s Windows PC SoC and the OEM devices built on it.'}]
    by_id['c2']['subjects'] = [{'existing': 'Vera Rubin platform rollout', 'new_name': '', 'new_scope': ''},
                               {'existing': 'none', 'new_name': 'OpenAI–NVIDIA AI infrastructure deployment', 'new_scope': 'The planned deployment of NVIDIA systems for OpenAI.'}]
    return raw


def test_names_become_ids_and_declarations():
    projected, counts = names.project(stored_answer(), OFFERED)
    refs = {c['id']: c['thread_ids'] for c in projected['candidates']}
    assert refs == {'v1': ['g1'], 'c1': ['t1'], 'c2': ['g1', 't2']}
    assert [(t['id'], t['name']) for t in projected['threads']] == [('t1', 'Windows PC SoC rollout'), ('t2', 'OpenAI–NVIDIA AI infrastructure deployment')]
    assert counts == {'existing_refs': 2, 'new_subjects': 2, 'redeclared_existing': 0}
    assert 'subjects' not in json.dumps(projected)


def test_a_redeclared_shown_subject_resolves_to_the_stored_one_and_is_counted():
    raw = stored_answer()
    raw['candidates'][0]['subjects'] = [{'existing': 'none', 'new_name': 'vera  rubin platform rollout', 'new_scope': 'again'}]
    projected, counts = names.project(raw, OFFERED)
    assert projected['candidates'][0]['thread_ids'] == ['g1'] and counts['redeclared_existing'] == 1 and len(projected['threads']) == 2


def test_two_candidates_naming_the_same_new_subject_share_one_declaration():
    raw = stored_answer()
    raw['candidates'][0]['subjects'] = [{'existing': 'none', 'new_name': 'Windows PC SoC rollout', 'new_scope': 'same subject, other thesis'}]
    projected, counts = names.project(raw, OFFERED)
    assert projected['candidates'][0]['thread_ids'] == ['t1'] and projected['candidates'][1]['thread_ids'] == ['t1'] and counts['new_subjects'] == 2


def test_the_old_failure_shapes_cannot_be_written():
    raw = stored_answer()
    raw['candidates'][1]['subjects'] = [{'existing': 'g1', 'new_name': '', 'new_scope': ''}]          # an ID instead of a name
    with pytest.raises(ValueError, match='shape'):
        names.project(raw, OFFERED)
    raw = stored_answer()
    raw['candidates'][1]['subjects'] = [{'existing': 'none', 'new_name': 'Windows PC SoC rollout', 'new_scope': ''}]   # a new subject without a scope
    with pytest.raises(ValueError, match='name and a scope'):
        names.project(raw, OFFERED)
    raw = stored_answer()
    raw['candidates'][0]['subjects'] = [{'existing': 'Vera Rubin platform rollout', 'new_name': 'x', 'new_scope': ''}]   # both at once
    with pytest.raises(ValueError, match='no new name'):
        names.project(raw, OFFERED)
    with pytest.raises(ValueError, match='collide'):
        names.project(stored_answer(), OFFERED + [{'thread_id': 'g3', 'name': 'VERA RUBIN PLATFORM ROLLOUT', 'scope': 'dup'}])


def test_the_schema_offers_exactly_the_shown_names():
    schema = names.extraction_schema(OFFERED)
    candidate = schema['properties']['candidates']['items']
    assert candidate['properties']['subjects']['items']['properties']['existing']['enum'] == ['SK Telecom AI factory rollout', 'Vera Rubin platform rollout', 'none']
    assert 'thread_ids' not in candidate['properties'] and 'threads' not in schema['properties'] and 'subjects' in candidate['required']
