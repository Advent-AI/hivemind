"""Count every citation error and publish descriptive replay measurements, without judging prose."""
import argparse
import collections
import json
from pathlib import Path
import statistics

import study


def audit(out):
    data = json.loads((out / 'input.json').read_text())
    records, errors = [], []
    for path in sorted(out.glob('sample-*/*-result.json')):
        outcome = json.loads(path.read_text())
        step = path.name.removesuffix('-result.json')
        scope, arm, phase = step.split('-')
        raw = json.loads((path.parent / f'{step}.json').read_text())
        record = {'sample': int(path.parent.name.split('-')[1]), 'scope': scope,
                  'arm': arm, 'phase': phase, 'status': outcome['status'],
                  'seconds': raw['seconds'], 'input_tokens': raw['input_tokens'],
                  'output_tokens': raw['output_tokens'], 'estimated_usd': raw['estimated_usd']}
        if phase != 'probe':
            snap = next(s for s in data[scope] if s['cutoff_seq'] == int(phase))
            known = {t['id']: {e['evidence_id'] for e in t['evidence']} for t in snap['theses']}
            all_evidence = set().union(*known.values())
            refs = []
            for index, argument in enumerate(raw['answer']['arguments']):
                seen = set()
                for reference in argument['references']:
                    for eid in reference['evidence_ids']:
                        pair = (reference['view_id'], eid)
                        refs.append(pair)
                        reason = ('duplicate' if pair in seen else
                                  'wrong_view' if eid in all_evidence and eid not in known.get(pair[0], set()) else
                                  'not_current_evidence' if eid not in all_evidence else None)
                        if reason:
                            actual = [view for view, ids in known.items() if eid in ids]
                            errors.append(dict(sample=record['sample'], step=step, argument=index,
                                               view_id=pair[0], evidence_id=eid, reason=reason, actual_views=actual))
                        seen.add(pair)
            record.update(reference_occurrences=len(refs), evidence_ids=sorted({e for _, e in refs}),
                          conclusion=raw['answer']['conclusion'])
        records.append(record)
    grouped = []
    for scope in data:
        for arm in ['fresh', 'update']:
            group = [r for r in records if r['scope'] == scope and r['arm'] == arm and r['phase'] != 'probe']
            grouped.append({'scope': scope, 'arm': arm, 'attempted': len(group),
                            'valid': sum(r['status'] == 'valid' for r in group),
                            'rejected': sum(r['status'] == 'rejected' for r in group),
                            'median_seconds': statistics.median(r['seconds'] for r in group)})
    result = {'grouped': grouped, 'calls': records, 'citation_errors': errors,
              'error_occurrences': len(errors), 'error_kinds': dict(collections.Counter(e['reason'] for e in errors)),
              'reference_occurrences': sum(r.get('reference_occurrences', 0) for r in records),
              'rejected_outputs': sum(r['status'] == 'rejected' for r in records),
              'attempted_calls': len(records), 'estimated_usd': sum(r['estimated_usd'] for r in records)}
    study.write_json(out / 'reference-audit.json', result)
    text = ['# Replay measurements', '', 'Citation validity only; these are not semantic accuracy rates.', '',
            '| Scope | Arm | Attempted synthesis | Valid | Rejected | Median seconds |',
            '|---|---|---:|---:|---:|---:|']
    for row in grouped:
        text.append(f'| {row["scope"]} | {row["arm"]} | {row["attempted"]} | {row["valid"]} | {row["rejected"]} | {row["median_seconds"]:.2f} |')
    text.extend(['', f'Total calls: {len(records)}. Estimated cost: ${result["estimated_usd"]:.6f}.',
                 f'Citation errors: {len(errors)} of {result["reference_occurrences"]} reference occurrences across {result["rejected_outputs"]} rejected outputs.', '',
                 '| Sample | Step | Argument | Selected view | Evidence | Actual visible views |',
                 '|---:|---|---:|---|---|---|'])
    for error in errors:
        text.append(f'| {error["sample"]} | {error["step"]} | {error["argument"]} | {error["view_id"]} | {error["evidence_id"]} | {", ".join(error["actual_views"])} |')
    (out / 'measurements.md').write_text('\n'.join(text) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in {'calls', 'citation_errors'}}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    audit(parser.parse_args().out.resolve())
