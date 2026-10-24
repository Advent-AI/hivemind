"""D147 representation diagnostic; business decisions and local checks remain unchanged."""
import copy
import json
import re

import pytest

import flat_membership as flat
import extraction_membership as membership
import ingestion_threads as legacy
import study
from hivemind import universe


def test_d147_flat_schema_keeps_the_accepted_reference_set():
    """Closed-set row: one pattern accepts the same local IDs and displayed old IDs as the union."""
    for old_ids in [[], ['g1'], ['g1', 'g12']]:
        offered = [{'thread_id': x} for x in old_ids]
        original = membership.extraction_schema(offered)
        before = copy.deepcopy(original)
        new = flat.wire_schema(original, offered)
        pattern = new['properties']['candidates']['items']['properties']['thread_ids']['items']['pattern']
        for value in ['t1', 't999', 't0', 't-1', 'g1', 'g12', 'g99', '', ' t1', 't1\n']:
            assert bool(re.fullmatch(pattern, value)) == (bool(re.fullmatch(r't[1-9][0-9]*', value)) or value in old_ids)
        assert original == before
        before['properties']['candidates']['items']['properties']['thread_ids']['items'] = {'type': 'string', 'pattern': pattern}
        assert new == before


@pytest.mark.parametrize('sample', [1, 2, 3])
def test_d147_duplicate_raw_outputs_still_refused_and_complete_references_write(tmp_path, sample):
    """Failure-class proof: new schema spelling never deduplicates or repairs saved model output."""
    source = study.ROOT / f'poc/reports/2026-10-25-direct-subjects-01/sample-{sample}-membership'
    record = json.loads((source / 'item2-extract.json').read_text())
    offered = json.loads(record['request']['messages'][1]['content'])['existing_subjects']
    with pytest.raises(ValueError):
        membership.validate_extraction(record['answer'], offered)
    original = study.read_only(source / 'views.sqlite')
    conn = legacy.open_db(tmp_path / 'views.sqlite')
    original.backup(conn)
    original.close()
    class Saved:
        cfg = study.config.load(str(study.ROOT / 'poc/config/poc-v7.json'))
        def stage(self, name, prompt, payload, schema, setting):
            if name.endswith('extract'):
                answer = copy.deepcopy(record['answer'])
                answer['candidates'][0]['thread_ids'] = ['g1', 't1']
                return answer
            return {'candidates': [{'id': 'c1', 'outcome': 'new', 'target_view_id': '',
                     'reason': 'A distinct customer deployment.', 'dependencies': []}],
                    'evidence': [{'id': pair['evidence_id'], 'view_id': pair['view_id'], 'outcome': 'new',
                                  'target_evidence_id': '', 'said_day': '', 'reason': 'New deployment evidence.'}
                                 for pair in payload['evidence_pairs']]}
    items = json.loads((source.parent / 'items.json').read_text())
    result = membership.process(conn, Saved(), universe.load(str(study.ROOT / 'poc/universe.json')), items[1], 2)
    assert {m['view_id'] for m in result['memberships'] if m['thread_id'] == 'g1'} == {'v1', 'v2'}
    conn.close()
