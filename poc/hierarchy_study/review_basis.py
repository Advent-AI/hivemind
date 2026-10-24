"""Reproduce structural counts, costs and source traces from the frozen basis experiment."""
import argparse
import collections
import json
from pathlib import Path
import statistics

import basis_replay as basis
import study


def review(out):
    snapshots = json.loads((out / 'input.json').read_text())
    results, traces, judged_sources = [], [], 0
    for path in sorted(out.glob('sample-*/*-result.json')):
        result = json.loads(path.read_text())
        step = path.name.removesuffix('-result.json')
        scope, stage, ending = step.split('-')
        raw = json.loads((path.parent / (step + '.json')).read_text())
        phase = 'review' if stage == 'review' else stage + '_' + ending
        item = {'sample': int(path.parent.name.split('-')[1]), 'scope': scope, 'phase': phase,
                'step': step, 'status': result['status'], 'input_tokens': raw.get('input_tokens'),
                'output_tokens': raw.get('output_tokens'), 'seconds': raw.get('seconds'),
                'estimated_usd': raw.get('estimated_usd')}
        results.append(item)
        if result['status'] != 'valid':
            continue
        value = result['value']
        if stage == 'review':
            snap = next(s for s in snapshots[scope] if s['cutoff_seq'] == int(ending))
            catalog = {r['source_ref']: r for r in basis.catalog(snap)}
            assert {r['source_ref'] for r in value['rows']} == set(catalog)
            for row in value['rows']:
                assert row['origin_paths'] == catalog[row['source_ref']]['origin_paths']
            judged_sources += len(value['rows'])
            item['source_count'] = len(value['rows'])
            item['roles'] = dict(collections.Counter(r['role'] for r in value['rows']))
        if ending == 'final':
            item['visible_sources'] = len(basis.visible_sources(value))
        targets = ['source_e724', 'source_e748'] if scope == 'rubin' else ['source_e816', 'source_e814', 'source_e826']
        trace = {'sample': item['sample'], 'scope': scope, 'step': step}
        if stage == 'review':
            trace['targets'] = [{k: r[k] for k in ['source_ref', 'role', 'reason']} for r in value['rows'] if r['source_ref'] in targets]
        elif ending == 'final':
            trace['conclusion'] = value['summary']['conclusion']
            trace['target_arguments'] = [a for a in value['summary']['arguments'] if set(a['sources']) & set(targets)]
            trace['target_visible'] = [r['source_ref'] for r in basis.visible_sources(value) if r['source_ref'] in targets]
            trace['limitations'] = value['summary']['limitations']
        else:
            trace['facets'] = value['facets']
        traces.append(trace)
    if not results:
        raise ValueError('No experiment outputs to measure')
    budget = json.loads((out / 'budget.json').read_text())
    assert len(results) == len(budget['attempts']), 'Missing attempt outcomes'
    grouped = []
    for phase in ['review', 'basis_final', 'direct_final', 'basis_probe', 'direct_probe']:
        rows = [r for r in results if r['phase'] == phase]
        measured = [r for r in rows if r['input_tokens'] is not None]
        grouped.append({'phase': phase, 'attempted': len(rows), 'valid': sum(r['status'] == 'valid' for r in rows),
                        'mean_input_tokens': statistics.mean(r['input_tokens'] for r in measured) if measured else None,
                        'estimated_usd': sum(r['estimated_usd'] for r in measured)})
    round_costs = []
    for sample in [1, 2, 3]:
        for scope, snaps in snapshots.items():
            latest = snaps[-1]['cutoff_seq']
            current = [r for r in results if r['sample'] == sample and r['scope'] == scope]
            for arm in ['basis', 'direct']:
                selected = [r for r in current if r['phase'] in {arm + '_final', arm + '_probe'} or
                            (arm == 'basis' and r['step'] == f'{scope}-review-{latest}')]
                expected = 3 if arm == 'basis' else 2
                if len(selected) == expected and all(r['estimated_usd'] is not None for r in selected):
                    round_costs.append({'sample': sample, 'scope': scope, 'arm': arm,
                                        'estimated_usd': sum(r['estimated_usd'] for r in selected)})
    report = {'attempts': len(results), 'valid': sum(r['status'] == 'valid' for r in results),
              'judged_sources': judged_sources, 'estimated_usd': budget['estimated_spent'],
              'source_unchanged': study.digest(basis.replay.SOURCE) == json.loads((out / 'manifest.json').read_text())['source_sha256'],
              'groups': grouped, 'final_round_costs': round_costs, 'results': results, 'traces': traces}
    means = {arm: statistics.mean(r['estimated_usd'] for r in round_costs if r['arm'] == arm)
             for arm in ['basis', 'direct'] if any(r['arm'] == arm for r in round_costs)}
    if len(means) == 2:
        report['comparison'] = {'mean_final_round_usd': means, 'basis_to_direct_cost_ratio': means['basis'] / means['direct'],
                                'basis_to_direct_reader_input_ratio': next(r['mean_input_tokens'] for r in grouped if r['phase'] == 'basis_probe') / next(r['mean_input_tokens'] for r in grouped if r['phase'] == 'direct_probe')}
    study.write_json(out / 'measurements.json', report)
    text = ['# Basis experiment measurements', '', 'Structural validity and observed usage; not semantic accuracy.', '',
            '| Phase | Attempted | Valid | Mean input tokens | Estimated USD |', '|---|---:|---:|---:|---:|']
    for row in grouped:
        text.append(f'| {row["phase"]} | {row["attempted"]} | {row["valid"]} | {row["mean_input_tokens"]} | {row["estimated_usd"]:.6f} |')
    text += ['', f'Judged source instances: {judged_sources}. Total estimated USD: {report["estimated_usd"]:.6f}.', '',
             'The final-round comparison includes latest-source review + summary + reader for basis, and summary + reader for direct. Earlier historical source reviews are excluded from that comparison.', '',
             '```json', json.dumps(round_costs, indent=2), '```']
    (out / 'measurements.md').write_text('\n'.join(text) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in {'results', 'traces'}}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    review(parser.parse_args().out.resolve())
