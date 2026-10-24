"""Targeted three-sample diagnostic for orphaned theses, after the main comparisons."""
import argparse
import copy
import json
from pathlib import Path

import study

PROMPT = """Revisit atomic research theses that were left unassigned earlier in a stream.
You now see existing themes and the complete supplied immutable thesis texts. Reconsider only the unassigned_ids.
Assign one to an existing theme if that theme's scope fits; otherwise create a bounded reusable theme if the now-visible
context supports one. A theme can span companies. Do not use shared company name or generic financial vocabulary alone.
Do not change old assignments, merge themes, or force housekeeping into a business theme. Some IDs can remain unassigned.
Return assignments only for those unassigned IDs, plus any new_groups. Each unassigned ID must appear exactly once in
assignments or unassigned. New groups need unique IDs distinct from existing IDs. Existing groups are immutable and must
not be returned or rewritten. Use only supplied texts; write new titles/scopes in English. Return the requested JSON."""


def check(value, old, ids):
    study.check_partition(value, ids)
    updated = {group['id']: group for group in value['groups']}
    for group in old['groups']:
        if group['id'] not in updated:
            raise ValueError('Revisit removed an existing theme')
        next_group = updated[group['id']]
        if next_group['title'] != group['title'] or next_group['scope'] != group['scope']:
            raise ValueError('Revisit changed an existing theme boundary')
        if not set(group['members']) <= set(next_group['members']):
            raise ValueError('Revisit moved a previously assigned member')
    return value


def apply_update(old, update, ids):
    import collections
    actual = update['unassigned'] + [assignment['view_id'] for assignment in update['assignments']]
    if collections.Counter(actual) != collections.Counter(old['unassigned']):
        raise ValueError('Revisit may place only the previously unassigned IDs')
    result = copy.deepcopy(old)
    result['unassigned'] = update['unassigned']
    groups = {group['id']: group for group in result['groups']}
    for group in update['new_groups']:
        if group['id'] in groups:
            raise ValueError('New group collides with an existing ID')
        created = dict(group, members=[])
        result['groups'].append(created)
        groups[group['id']] = created
    for assignment in update['assignments']:
        if assignment['group_id'] not in groups:
            raise ValueError('Unknown target group')
        groups[assignment['group_id']]['members'].append(assignment['view_id'])
    return check(result, old, ids)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    out = Path(args.out)
    if not (out / 'argument_first_metrics.json').exists():
        raise ValueError('Complete A-E first')
    data = json.loads((out / 'input.json').read_text())
    snapshot = data['snapshots'][-1]
    ids = [thesis['id'] for thesis in snapshot['theses']]
    results = []
    for sample in [1, 2, 3]:
        old = json.loads((out / f'sample-{sample}/D_incremental_llm-partition.json').read_text())
        calls = study.Calls(out, sample)
        update = calls.call('F_orphan-revisit', PROMPT, {'existing_groups': old['groups'], 'unassigned_ids': old['unassigned'], 'theses': study.grouping_nodes(snapshot)}, study.UPDATE_SCHEMA)
        value = apply_update(old, update, ids)
        study.write_json(out / f'sample-{sample}/F_partition.json', value)
        results.append({'sample': sample, 'before_unassigned': old['unassigned'], 'after_unassigned': value['unassigned'], 'recovered': sorted(set(old['unassigned'])-set(value['unassigned'])), 'v7_group': next((group['title'] for group in value['groups'] if 'v7' in group['members']), None)})
    study.write_json(out / 'revisit_metrics.json', results)
    print(json.dumps(results), flush=True)


if __name__ == '__main__':
    main()
