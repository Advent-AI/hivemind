"""B-only offline identity prototype; actual repeated-claim matching is still required."""
import copy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = ROOT / 'docs/research/2026-11-05-parallel-thesis-evidence-poc'
sys.path[:0] = [str(HERE), str(OLD), str(ROOT / 'src')]
import run_poc
from hivemind import model


def handover_by_record(data, request, universe, answer):
    """Check each B record with the existing sift; retain evidence identity by response position.

    This intentionally does not deduplicate semantic repeats and is not a writer or production path.
    """
    errors = model.check_schema(data, request['schema'])
    if errors:
        raise ValueError('invalid raw schema: ' + '; '.join(errors[:5]))
    evidence, dropped, identity = [], [], []
    for index, raw in enumerate(data['evidence'], 1):
        record = copy.deepcopy(raw)
        record_id = 'e' + str(index)
        identity.append({'position': index, 'raw_id': record['id'], 'record_id': record_id})
        record['id'] = record_id
        result = run_poc.handover({'evidence': [record]}, request, universe, answer)
        evidence.extend(result['evidence'])
        dropped.extend(result['dropped'])
    return {'evidence': evidence, 'dropped': dropped, 'identity': identity}
