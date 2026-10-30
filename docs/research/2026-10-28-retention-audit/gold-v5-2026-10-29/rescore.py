"""Validate the recorded human-readable reassessment; do not infer semantic labels."""
import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / 'gold-v4-reassessment-2026-10-29'


def run():
    spec = importlib.util.spec_from_file_location('previous_measure', PREVIOUS / 'measure.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    old = module.read(PREVIOUS / 'assessments.json')
    new = module.read(HERE / 'reassessment.json')
    module.need(new['derived_from']['sha256'] == module.digest(PREVIOUS / 'assessments.json'),
                'previous reassessment changed')
    old_summary = module.measure(PREVIOUS, old)
    new_summary = module.measure(HERE, new)
    expected = copy.deepcopy(old['runs'])
    row = next(a for r in expected if r['run_id'] == 'revenue-clean-gpt-3'
               for a in r['assessments'] if a['reference_id'] == 'G09')
    changed = next(a for r in new['runs'] if r['run_id'] == 'revenue-clean-gpt-3'
                  for a in r['assessments'] if a['reference_id'] == 'G09')
    module.need(row['meaning'] == 'partial' and changed['meaning'] == 'correct',
                'recorded semantic correction differs')
    row['meaning'] = changed['meaning']
    row['reason'] = changed['reason']
    module.need(expected == new['runs'], 'unexplained historical observation change')
    return {'before': old_summary, 'after': new_summary,
            'changed_observations': [{'run_id': 'revenue-clean-gpt-3', 'reference_id': 'G09',
                                      'before': 'partial', 'after': 'correct',
                                      'reason': changed['reason']}],
            'unchanged_observations': new_summary['reference_observations'] - 1,
            'new_product_calls': 0}


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
