"""Report every smoke sample, separating API validation from semantic acceptance."""
import argparse
import json
from pathlib import Path
import statistics


def summarize(directory):
    result = json.loads((directory / 'result.json').read_text())
    if result['failure'] or result['changed_protected_files']:
        return {'passed': False, 'failure': result['failure'], 'changed_protected_files': result['changed_protected_files']}
    rows = result['results']
    if len(rows) != 18 or len(result['accounting']['attempts']) != 36:
        raise ValueError('incomplete study; cannot report a passing smoke')
    report = {'passed': True, 'protected_files_unchanged': result['protected_files'], 'timing': {}, 'comparisons': [],
              'extraction_counts': [{'sample': r['sample'], 'arm': r['arm'], 'original_call_id': a['original_call_id'],
                                     'candidates': len(a['data'].get('candidates', [])), 'evidence': len(a['data'].get('evidence', [])),
                                     'groups': len(a['data'].get('new_groups', []))}
                                    for r in rows if r['purpose'] == 'extract' for a in r['answers']]}
    for purpose in ('extract', 'match'):
        samples = []
        for sample in (1, 2, 3):
            arms = {r['arm']: r for r in rows if r['purpose'] == purpose and r['sample'] == sample}
            a, b, c = [arms[k] for k in ('control-a', 'control-b', 'concurrent')]
            samples.append({'sample': sample, 'control_a_seconds': a['seconds'], 'control_b_seconds': b['seconds'],
                            'concurrent_seconds': c['seconds'], 'ratio_to_mean_control': ((a['seconds'] + b['seconds']) / 2) / c['seconds']})
            for name, left, right in [('control-a/control-b', a, b), ('control-a/concurrent', a, c), ('control-b/concurrent', b, c)]:
                compared = {'sample': sample, 'purpose': purpose, 'pair': name, 'equal_full_answers': 0, 'choice_questions': 0, 'changed_choices': [], 'noul_deltas': []}
                for x, y in zip(left['answers'], right['answers']):
                    if x['request_sha256'] != y['request_sha256']:
                        raise ValueError('compared different requests')
                    compared['equal_full_answers'] += int(x['data'] == y['data'])
                    if purpose == 'match':
                        for key, value in x['data'].items():
                            other = y['data'][key]
                            if value['type'] == 'choice':
                                compared['choice_questions'] += 1
                                if value['choice'] != other['choice']:
                                    compared['changed_choices'].append({'call': x['original_call_id'], 'question': key, 'left': value['choice'], 'right': other['choice']})
                            elif value['type'] == 'noul':
                                compared['noul_deltas'].append({'call': x['original_call_id'], 'question': key, 'absolute_delta': abs(value['noul'] - other['noul'])})
                report['comparisons'].append(compared)
        report['timing'][purpose] = {'samples': samples, 'median_ratio_to_mean_control': statistics.median(r['ratio_to_mean_control'] for r in samples)}
    attempts = result['accounting']['attempts']
    report['attempts'] = len(attempts)
    report['unknown_attempts'] = sum(a['state'] != 'complete' for a in attempts)
    report['conservative_charge_usd'] = result['accounting']['held_microdollars'] / 1e6
    report['standard_list_charge_usd'] = sum(a['standard_list_cost_usd'] for r in rows for a in r['answers'])
    report['interpretation'] = 'API smoke only. Fresh answer variation and request timing do not establish end-to-end correctness, gold acceptance, or production speedup.'
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(summarize(args.directory), indent=2))
