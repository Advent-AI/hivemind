"""Summarize every sample and the explicit human-readable source assessment; no API calls."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--result', type=Path, required=True)
parser.add_argument('--assessment', type=Path, default=Path(__file__).with_name('assessments.json'))
args = parser.parse_args()
data = json.loads(args.result.read_text())
assessment = json.loads(args.assessment.read_text())
assert data['failure'] is None and data['changed_protected'] == []
assert len(data['samples']) == 6
rows = []
for sample in data['samples']:
    rows.append({'name': sample['name'], 'covered': assessment['samples'][sample['name']]['covered'],
                 'new_views': len(sample['new_views']), 'evidence_kept': len(sample['handover']['evidence']),
                 'candidates_proposed': len(sample['raw_answer']['candidates']), 'drops': len(sample['handover']['dropped']),
                 'input_tokens': sample['input_tokens'], 'output_tokens': sample['output_tokens'],
                 'seconds': sample['seconds'], 'request_sha256': sample['request_sha256']})
arms = {}
for arm in ('control', 'treatment'):
    selected = [r for r in rows if r['name'].startswith(arm)]
    assert len(selected) == 3
    arms[arm] = {'covered': sum(r['covered'] for r in selected), 'samples': 3,
                 'input_tokens_per_request': sorted({r['input_tokens'] for r in selected}),
                 'output_tokens_total': sum(r['output_tokens'] for r in selected)}
print(json.dumps({'scope': data['scope'], 'samples': rows, 'arms': arms,
                  'physical_requests': len(data['budget']['attempts']),
                  'conservative_cost_usd': data['budget']['held_microdollars'] / 1e6,
                  'standard_list_price_estimate_usd': sum(s['archive_totals'][1] for s in data['samples']),
                  'changed_protected': data['changed_protected'],
                  'assessment_source': assessment['reviewer']}, indent=2))
