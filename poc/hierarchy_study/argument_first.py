"""Exploratory main-thesis-first baseline, run after the four frozen grouping POCs."""
import argparse
import json
from pathlib import Path

import study

SCHEMA = study.obj({'heads': {'type': 'array', 'items': study.HEAD}})
PROMPT = """Build an agent-facing argument map from the supplied atomic financial-research theses.
Start with a small number of substantive, bounded overarching business judgements, then link the atomic theses that
support, challenge, or contextualize each judgement. Do NOT begin by partitioning all inputs into topic buckets.
An atomic thesis may support more than one overarching thesis. Housekeeping and isolated events may be left unused.
A main thesis must say what the research currently supports, through what business mechanism, with what limitations.
It must not merely rename a category such as Revenue, Products, or Tax. If the data cannot support an overarching
judgement, omit it. Emitted heads use status main_thesis. Use only supplied point-in-time research, no outside knowledge or stock-price inference.
Keep actual results distinct from guidance, forecasts and future events. Preserve conflicting or contrary evidence.
Every substantive explanatory claim needs supplied atomic view_ids, with supports/challenges/context role. The main
thesis statement must be supported by its cited claims. Give each head a unique group_id, concise title, limitations,
and concrete watch questions. All prose is English. No new independent numerical score or fabricated outcome.
Return only the requested JSON."""


def validate(value, snapshot):
    errors = study.model.check_schema(value, SCHEMA)
    if errors:
        raise ValueError('; '.join(errors))
    gids = [head['group_id'] for head in value['heads']]
    if len(set(gids)) != len(gids):
        raise ValueError('Main thesis IDs must be unique')
    known = {thesis['id'] for thesis in snapshot['theses']}
    used = set()
    for head in value['heads']:
        if head['status'] != 'main_thesis' or not head['thesis'].strip() or not head['claims']:
            raise ValueError('Emit only substantive main theses')
        for claim in head['claims']:
            if not claim['text'].strip() or not claim['view_ids'] or not set(claim['view_ids']) <= known:
                raise ValueError('A claim needs true snapshot references')
            used.update(claim['view_ids'])
    return dict(value, unused_ids=sorted(known-used))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    out = Path(args.out)
    if not (out / 'metrics.json').exists():
        raise ValueError('Complete A-D before running the exploratory E baseline')
    data = json.loads((out / 'input.json').read_text())
    snapshot = data['snapshots'][-1]
    records = []
    for sample in [1, 2, 3]:
        calls = study.Calls(out, sample)
        value = validate(calls.call('E_argument-first', PROMPT, {'as_of': '2026-08-15', **study.synthesis_context(snapshot)}, SCHEMA), snapshot)
        study.write_json(out / f'sample-{sample}' / 'E_result.json', value)
        probe = calls.call('E_argument-first-agent', study.PROBE_PROMPT, {'main_theses': value['heads'], 'questions': study.QUESTIONS}, study.PROBE_SCHEMA)
        known = {thesis['id'] for thesis in snapshot['theses']}
        errors = study.probe_errors(probe, value['heads'], snapshot)
        study.write_json(out / f'sample-{sample}' / 'E_argument-first-agent-checks.json', {'valid': not errors, 'errors': errors})
        references = [set(ident for claim in head['claims'] for ident in claim['view_ids']) for head in value['heads']]
        reused = {ident for ident in known if sum(ident in group for group in references) > 1}
        records.append({'sample': sample, 'main_theses': len(value['heads']), 'used_atomic_theses': len(known) - len(value['unused_ids']), 'unused_ids': value['unused_ids'], 'reused_atomic_theses': sorted(reused), 'cross_object_heads': sum(len({thesis['object'] for thesis in snapshot['theses'] if thesis['id'] in group}) > 1 for group in references), 'agent_references_valid': not errors})
    study.write_json(out / 'argument_first_metrics.json', records)
    print(json.dumps(records), flush=True)


if __name__ == '__main__':
    main()
