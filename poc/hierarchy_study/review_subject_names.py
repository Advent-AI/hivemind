"""Audit saved grouping transitions, never infer semantic correctness from names.

D156 contract: docs/research/2026-10-25-grouping-acceptance.md.
Exit zero means the selected records are complete and structurally consistent,
not that extraction coverage or business grouping has passed acceptance.
"""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


class RecordError(ValueError):
    """Saved records cannot support the requested audit."""


class Snapshot:
    """Read files once and detect changes or newly appearing completion records."""

    def __init__(self):
        self.files = {}

    def read(self, path, optional=False):
        path = Path(path).resolve()
        if path not in self.files:
            self.files[path] = path.read_bytes() if path.exists() else None
        data = self.files[path]
        if data is None:
            if optional:
                return None
            raise RecordError(f'Missing record: {path}')
        return json.loads(data)

    def verify(self):
        for path, data in self.files.items():
            current = path.read_bytes() if path.exists() else None
            if current != data:
                raise RecordError(f'Record changed during audit: {path}')


def indexed(rows, key):
    result = {row[key]: row for row in rows}
    if len(result) != len(rows):
        raise RecordError(f'Duplicate {key} in saved records')
    return result


def call_payload(record):
    if record['status'] != 'complete':
        raise RecordError('Model call is not complete')
    request = record['request']
    digest = hashlib.sha256(json.dumps(request, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    if digest != record['request_sha256']:
        raise RecordError('Saved request digest differs')
    users = [m['content'] for m in request['messages'] if m['role'] == 'user']
    if len(users) != 1:
        raise RecordError('Expected one saved user payload')
    return json.loads(users[0])


def projected_answer(answer, offered, projection):
    """Independently check every selected target against its archived projection."""
    candidates = answer['candidates']
    indexed(candidates, 'id')
    old = indexed(offered, 'thread_id')
    if projection is None:
        if any('subjects' in c for c in candidates):
            raise RecordError('Names answer is missing its projection')
        projected = answer
    else:
        if projection['subjects'] != [c['subjects'] for c in candidates]:
            raise RecordError('Projection selections differ from the raw answer')
        if len(projection['thread_ids']) != len(candidates):
            raise RecordError('Projection candidate row count differs')
        declarations = indexed(projection['threads'], 'id')
        names = indexed(offered, 'name')
        rewritten = []
        for candidate, refs in zip(candidates, projection['thread_ids']):
            selected = candidate['subjects']
            if len(refs) != len(selected):
                raise RecordError(f"Projection target count differs: {candidate['id']}")
            for choice, ref in zip(selected, refs):
                if choice['existing'] != 'none':
                    target = names.get(choice['existing'])
                    if (target is None or ref != target['thread_id'] or
                            choice['new_name'] or choice['new_scope']):
                        raise RecordError(f"Projection changed existing target: {candidate['id']}")
                else:
                    target = declarations.get(ref)
                    if (target is None or not choice['new_name'].strip() or not choice['new_scope'].strip() or
                            (target['name'], target['scope']) != (choice['new_name'], choice['new_scope'])):
                        raise RecordError(f"Projection changed new target: {candidate['id']}")
            rewritten.append(dict(candidate, thread_ids=refs))
        projected = dict(answer, candidates=rewritten, threads=projection['threads'])
    declarations = indexed(projected['threads'], 'id')
    if old.keys() & declarations.keys():
        raise RecordError('Local and existing group IDs overlap')
    known = old.keys() | declarations.keys()
    for candidate in projected['candidates']:
        refs = candidate['thread_ids']
        if not refs or len(set(refs)) != len(refs) or set(refs) - known:
            raise RecordError(f"Invalid membership references: {candidate['id']}")
    return projected


def audit_memberships(answer, decisions, before, result):
    """Check this write against chosen references; keep old membership separate."""
    seq, input_id = result['seq'], result['input_id']
    if type(seq) is not int or seq != before['seq'] + 1:
        raise RecordError('Result is not the next transition after the saved prefix')
    old_groups = indexed(before['threads'], 'thread_id')
    groups = indexed(result['threads'], 'thread_id')
    views = indexed(result['views'], 'view_id')
    old_members = {(m['thread_id'], m['view_id']): m for m in before['memberships']}
    members = {(m['thread_id'], m['view_id']): m for m in result['memberships']}
    if len(members) != len(result['memberships']) or len(old_members) != len(before['memberships']):
        raise RecordError('Duplicate stored membership')
    if any(groups.get(gid) != row for gid, row in old_groups.items()):
        raise RecordError('An existing group changed')
    if any(members.get(key) != row for key, row in old_members.items()):
        raise RecordError('An existing membership changed')
    for key, member in members.items():
        if key[0] not in groups or key[1] not in views:
            raise RecordError('Membership has a missing group or view')
        if key not in old_members and (member['seq'], member['input_id']) != (seq, input_id):
            raise RecordError('New membership has wrong input or sequence')

    candidates = indexed(answer['candidates'], 'id')
    outcomes = indexed(decisions['candidates'], 'id')
    if outcomes.keys() - candidates.keys() or result['new_views'].keys() - candidates.keys():
        raise RecordError('Write or decision contains an unknown candidate')
    dropped = {entry[0] for entry in result['dropped']}
    declarations = indexed(answer['threads'], 'id')
    offered = indexed(result['offered_threads'], 'thread_id')
    expected, resolved, rows = set(), {}, []
    for cid, candidate in candidates.items():
        decision = outcomes.get(cid)
        targets = []
        if cid in dropped:
            if decision or cid in result['new_views']:
                raise RecordError(f'Rejected candidate also written or matched: {cid}')
            disposition, vid = 'rejected', None
        elif decision is None:
            raise RecordError(f'Candidate has no decision or rejection: {cid}')
        else:
            disposition = decision['outcome']
            if disposition in ('new', 'successor'):
                vid = result['new_views'].get(cid)
                if vid not in views or views[vid]['question'] != candidate['question']:
                    raise RecordError(f'New candidate has wrong final view: {cid}')
            elif disposition == 'existing':
                vid = decision['target_view_id']
                if vid not in views or cid in result['new_views']:
                    raise RecordError(f'Existing target is inconsistent: {cid}')
            elif disposition == 'discard':
                vid = None
                if cid in result['new_views']:
                    raise RecordError(f'Discarded candidate was written: {cid}')
            else:
                raise RecordError(f'Unknown candidate decision: {disposition}')
        if vid is not None:
            for ref in candidate['thread_ids']:
                if ref in offered:
                    gid = ref
                    if ref not in old_groups or any(groups[ref][k] != offered[ref][k] for k in ('name', 'scope')):
                        raise RecordError(f'Offered group differs from stored group: {ref}')
                else:
                    declaration = declarations[ref]
                    matches = [gid for gid, group in groups.items() if gid not in old_groups and
                               (group['seq'], group['input_id'], group['name'], group['scope']) ==
                               (seq, input_id, declaration['name'], declaration['scope'])]
                    if len(matches) != 1:
                        raise RecordError(f'New group mapping is missing or ambiguous: {ref}')
                    gid = matches[0]
                    if gid in resolved.values() and resolved.get(ref) != gid:
                        raise RecordError('Distinct local declarations were merged')
                    resolved[ref] = gid
                expected.add((cid, vid, gid))
                targets.append({'thread_id': gid, 'name': groups[gid]['name'], 'scope': groups[gid]['scope']})
        rows.append({'candidate_id': cid, 'question': candidate['question'], 'disposition': disposition,
                     'view_id': vid, 'groups': targets, 'semantic_status': 'pending'})

    actual = {(b['candidate_id'], b['view_id'], b['thread_id']) for b in result['bindings']}
    if actual != expected or len(actual) != len(result['bindings']):
        raise RecordError('Final bindings differ from selected targets')
    expected_pairs = {(gid, vid) for _, vid, gid in expected}
    if set(members) != set(old_members) | expected_pairs:
        raise RecordError('Stored memberships differ from this transition')
    seen = set(old_members)
    for binding in result['bindings']:
        key = (binding['thread_id'], binding['view_id'])
        if binding['new_membership'] is not (key not in seen):
            raise RecordError('Binding new-membership flag differs')
        seen.add(key)
    if set(groups) - set(old_groups) != set(resolved.values()):
        raise RecordError('Unused or unexplained new group')
    return {'candidates': rows, 'bindings_checked': len(expected),
            'prior_memberships_preserved': len(old_members),
            'new_memberships': len(set(members) - set(old_members))}


def audit_sample(snapshot, folder, item, before):
    row = {'sample': folder.name.removeprefix('sample-'), 'state': 'incomplete',
           'grouping': 'unexercised', 'semantic_status': 'pending', 'errors': []}
    failed = snapshot.read(folder / 'failed.json', optional=True)
    if failed is not None:
        return dict(row, state='failed', errors=[failed['error']])
    records = {name: snapshot.read(folder / name, optional=True) for name in
               ('item3-extract.json', 'item3-extract-projection.json', 'item3-match.json',
                'item3-result.json', 'checks.json')}
    if not any(value is not None for value in records.values()):
        started = folder.exists() and any(folder.iterdir())
        return dict(row, state='incomplete' if started else 'not_started')
    required = ('item3-extract.json', 'item3-match.json', 'item3-result.json', 'checks.json')
    missing = [name for name in required if records[name] is None]
    if missing:
        return dict(row, errors=[f'Missing records: {missing}'])
    checks = records['checks.json']
    if checks.get('history_unchanged') is not True or checks.get('resend') != 'skipped':
        return dict(row, state='failed', errors=['Saved history/resend checks failed'])
    extract = records['item3-extract.json']
    payload = call_payload(extract)
    match = records['item3-match.json']
    match_payload = call_payload(match)
    result = records['item3-result.json']
    for key in ('input_id', 'title', 'publication_day', 'category', 'text'):
        if payload['article'][key] != item[key]:
            raise RecordError(f'Saved input differs from registered item: {key}')
    if any(match_payload['item'][k] != item[k] for k in ('input_id', 'publication_day', 'category')):
        raise RecordError('Matching input differs from registered item')
    if result['input_id'] != item['input_id'] or result['route'] != 'written':
        raise RecordError('Result input or route differs')
    if payload['existing_subjects'] != result['offered_threads']:
        raise RecordError('Offered groups differ between request and result')
    answer = projected_answer(extract['answer'], payload['existing_subjects'], records['item3-extract-projection.json'])
    row.update(audit_memberships(answer, match['answer'], before, result))
    dropped = {entry[0]: entry[1] for entry in result['dropped']}
    row.update(state='complete', references_checked=sum(len(c['thread_ids']) for c in answer['candidates']),
               input_id=item['input_id'], evidence=[dict(e, rejection=dropped.get(e['id'])) for e in answer['evidence']],
               rejections=result['dropped'], evidence_retention_status='not_checked',
               call={'input_tokens': extract['input_tokens'], 'output_tokens': extract['output_tokens'],
                     'seconds': extract['seconds'], 'cached': extract['cached']})
    row['grouping'] = 'pending_semantic_review' if row['bindings_checked'] else 'unexercised'
    return row


def review(out, case='dev'):
    snapshot = Snapshot()
    manifest = snapshot.read(out / 'manifest.json')
    if manifest['version'] != 'subject-names-v1':
        raise RecordError('Unsupported experiment format')
    items = snapshot.read(out / 'items.json')
    before = snapshot.read(Path(manifest['source']) / 'item2-result.json')
    cases = list(manifest['plan']) if case == 'all' else [case]
    rows = []
    for selected in cases:
        labels = manifest['plan'][selected]
        if not labels or len(set(labels)) != len(labels):
            raise RecordError('Empty or duplicate registered sample list')
        for label in labels:
            if Path(label).name != label:
                raise RecordError('Invalid sample label')
            try:
                row = audit_sample(snapshot, out / f'sample-{label}', items[selected], before)
            except (RecordError, KeyError, TypeError, ValueError) as error:
                row = {'sample': label, 'state': 'invalid', 'semantic_status': 'pending', 'errors': [str(error)]}
            rows.append(dict(row, case=selected))
    snapshot.verify()
    counts = Counter(row['state'] for row in rows)
    return {'mode': 'stored_record_audit', 'acceptance': 'not_established',
            'samples_registered': len(rows), 'states': dict(counts), 'samples': rows,
            'references_checked': sum(r.get('references_checked', 0) for r in rows),
            'bindings_checked': sum(r.get('bindings_checked', 0) for r in rows),
            'semantic_cases_judged': 0,
            'exit_code': 0 if counts.get('complete', 0) == len(rows) else 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--case', choices=['dev', 'google', 'amd', 'all'], default='dev')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        report = review(args.out.resolve(), args.case)
    except (OSError, RecordError, KeyError, TypeError, ValueError) as error:
        report = {'mode': 'stored_record_audit', 'acceptance': 'not_established', 'errors': [str(error)], 'exit_code': 1}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print('Stored-record audit only; semantic acceptance is NOT established.')
        for row in report.get('samples', []):
            print(f"{row['sample']}: {row['state']}; grouping={row.get('grouping', 'not_checked')}; "
                  f"references={row.get('references_checked', 0)}; new memberships={row.get('new_memberships', 0)}")
            for error in row['errors']:
                print(f'  {error}')
        print(json.dumps({k: v for k, v in report.items() if k != 'samples'}, ensure_ascii=False))
    return report['exit_code']


if __name__ == '__main__':
    raise SystemExit(main())
