"""D146: direct subject identity groups inside the existing ingestion pipeline."""
import argparse
import dataclasses
import fcntl
import json
from pathlib import Path

import ingestion_groups as base
import ingestion_threads as legacy
import study
from hivemind import dispatch, universe
from hivemind.views import matching, store, writing

MATCH_SUBJECTS = """ Also group descriptions of the same continuing business subject in subject_identity.
Reuse a displayed stored subject when it is the same development; otherwise create a new one. Separate metrics,
customer deployments and dates within a product rollout or program retain its identity. A shared company alone
is insufficient. Thesis memberships are already assigned; decide only which subject descriptions are identical."""


def matching_schema(subjects, candidates):
    local_ids = [subject['id'] for subject in subjects]
    destinations = sorted({value['thread_id'] for hits in candidates.values() for value in hits})
    schema = base.matching_schema(False)
    schema['required'].append('subject_groups')
    groups = {'type': 'array', 'items': study.obj({
        'local_ids': {'type': 'array', 'items': {'type': 'string', 'enum': local_ids} if local_ids else study.STRING,
                      'minItems': 1},
        'destination': {'type': 'string', 'enum': ['new', *destinations]},
        'reason': study.STRING})}
    if not local_ids:
        groups['maxItems'] = 0
    schema['properties']['subject_groups'] = groups
    return schema


def identity_payload(payload, subjects, candidates):
    """Separate subject identity from already assigned thesis membership in the matching request."""
    payload = dict(payload)
    payload['candidates'] = [{key: value for key, value in candidate.items() if key != 'thread_ids'}
                             for candidate in payload['candidates']]
    stored = {value['thread_id']: value for hits in candidates.values() for value in hits}
    payload['subject_identity'] = {'local_descriptions': subjects,
        'stored_subjects': list(stored.values()),
        'eligible_stored_ids': {key: [value['thread_id'] for value in hits] for key, hits in candidates.items()}}
    return payload


def resolve_groups(answer, subjects, candidates):
    """Every local description occurs once; destinations are new or actually offered stored subjects."""
    errors = study.model.check_schema(answer, matching_schema(subjects, candidates))
    if errors:
        raise ValueError('Subject identity shape: ' + '; '.join(errors))
    ids = [subject['id'] for subject in subjects]
    groups = answer['subject_groups']
    flattened = [ident for group in groups for ident in group['local_ids']]
    if sorted(flattened) != sorted(ids):
        raise ValueError('Subject groups must cover every local ID exactly once')
    resolved = {}
    for group in groups:
        members, destination = group['local_ids'], group['destination']
        if not members or not group['reason'].strip():
            raise ValueError('Subject group needs members and a reason')
        if destination == 'new':
            root = next(ident for ident in ids if ident in members)
        else:
            if any(destination not in {value['thread_id'] for value in candidates[ident]} for ident in members):
                raise ValueError('Stored subject must be offered for every local member')
            root = destination
        resolved.update((ident, root) for ident in members)
    return resolved


def process(conn, calls, uni, item, index):
    route = dispatch.route(conn, item, uni)
    if route.kind != 'extract':
        return {'input_id': item['input_id'], 'route': route.kind}
    seq = route.sequence_no
    shown = store.views_for_prompt(conn, [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])])
    payload = {'article': {k: item[k] for k in ['input_id', 'title', 'publication_day', 'category', 'text']},
               'objects': [dict(id=k, kind=uni.kind(k)) for k in list(uni.companies) + list(uni.themes)],
               'fiscal_context': [uni.fiscal_note(o['value'], item['publication_day']) for o in item['object_identifiers']],
               'existing_theses': [{k: v[k] for k in ['view_id', 'object_id', 'question', 'looks_at', 'due_day']} |
                                    {'threads': legacy.thread_context(conn, v['view_id'])} for v in shown]}
    raw = calls.stage(f'item{index}-extract', base.EXTRACT_PROMPT + legacy.EXTRACT_THREADS, payload,
                      legacy.extraction_schema(), calls.cfg.extraction_setting(item['category']))
    legacy.validate_extraction(raw)
    handover = base.sift(raw, item, shown)
    used = {tid for c in handover.candidates for tid in c['thread_ids']}
    threads = [t for t in raw['threads'] if t['id'] in used]
    candidates = {t['id']: legacy.search_threads(conn, t, calls.cfg.search_top_n) for t in threads}
    lists = matching.build_lists(conn, handover, shown, calls.cfg.search_top_n)
    payload = base.match_payload(conn, item, handover, lists, shown, None, [])
    payload = identity_payload(payload, threads, candidates)
    answer = calls.stage(f'item{index}-match', base.MATCH_PROMPT + MATCH_SUBJECTS, payload,
                         matching_schema(threads, candidates), calls.cfg.matching)
    roots = resolve_groups(answer, threads, candidates)
    checked = base.check_matching(conn, uni, answer, handover, lists, shown)
    if checked.refusals:
        raise ValueError('Original matching checks: ' + '; '.join(checked.refusals))
    pending = [(e, checked.outcomes[link][1]) for e in handover.evidence for link in e['links']
               if link in checked.outcomes and checked.outcomes[link][0] == matching.OUTCOMES[0]]
    second = {}
    if pending:
        unique = {e['id']: e for e, _ in pending}
        second_handover = dataclasses.replace(handover, candidates=[], evidence=list(unique.values()))
        lists2 = matching.Lists({}, {(e['id'], vid): matching.rank_evidence(conn, vid, e['one_line'], calls.cfg.search_top_n) for e, vid in pending})
        payload = base.match_payload(conn, item, second_handover, lists2, [], None, [])
        raw2 = calls.stage(f'item{index}-match-evidence', base.MATCH_PROMPT, payload,
                           base.matching_schema(False), calls.cfg.matching)
        check2 = base.check_matching(conn, uni, raw2, second_handover, lists2, [])
        if check2.refusals:
            raise ValueError('Second matching checks: ' + '; '.join(check2.refusals))
        second = check2.evidence
    handover.candidates.sort(key=lambda c: c['kind'] != 'theme')
    written = writing.write(conn, uni, seq, item, handover, checked, second)
    bindings, affected = legacy.write_threads(conn, threads, roots, handover, checked, written, seq, item)
    result = {'input_id': item['input_id'], 'seq': seq, 'route': 'written', 'new_views': written.new_views,
              'changed_views': sorted(written.changed_views), 'affected_threads': affected,
              'bindings': bindings, 'dropped': handover.dropped, 'thread_roots': roots,
              'subject_groups': answer['subject_groups'],
              'thread_candidates': candidates,
              'threads': [dict(r) for r in conn.execute('select * from threads')],
              'memberships': [dict(r) for r in conn.execute('select * from thread_members')],
              'views': [base.view_record(conn, r[0]) for r in conn.execute('select view_id from views')],
              'details': [legacy.thread_detail(conn, r[0], seq) for r in conn.execute('select thread_id from threads')]}
    conn.execute('insert into ingestion_events values (?,?,?)', (seq, item['input_id'], json.dumps(result)))
    dispatch.mark(conn, item, seq, 'written', 'ok', json.dumps({'changed': result['changed_views'], 'threads': affected}))
    dispatch.mark(conn, item, seq, 'handed_over', 'ok', '')
    conn.commit()
    return result

class Calls(legacy.Calls):
    def __init__(self, out, label):
        super().__init__(out, label)
        self.cfg = dataclasses.replace(self.cfg, version='direct-subjects-v1')


def fingerprints():
    paths = [Path(__file__), Path(legacy.__file__), Path(base.__file__), Path(study.__file__),
             *[study.ROOT / 'src/hivemind' / name for name in ['extraction.py', 'dispatch.py', 'model.py', 'config.py',
                 'views/store.py', 'views/matching.py', 'views/writing.py']], study.ROOT / 'poc/universe.json']
    return {str(path.relative_to(study.ROOT)): study.digest(path) for path in paths}


def prepare(out):
    legacy.prepare(out)
    path = out / 'manifest.json'
    manifest = json.loads(path.read_text())
    manifest.update(code_sha256=study.digest(__file__), dependencies=fingerprints(),
                    version='direct-subjects-v1', control='D144')
    study.write_json(path, manifest)


def verify(out):
    manifest = json.loads((out / 'manifest.json').read_text())
    if (manifest['dependencies'] != fingerprints() or manifest['sealed_sha256'] != study.digest(base.SEALED)
            or manifest['corpus_sha256'] != study.digest(base.CORPUS)
            or manifest['items_sha256'] != study.digest(out / 'items.json')
            or manifest['extra_sha256'] != study.digest(out / 'extra-item.json')
            or manifest['config_checksum'] != study.config.load(str(study.ROOT / 'poc/config/poc-v7.json')).checksum):
        raise ValueError('Frozen experiment changed')


def run(out, extra=False):
    verify(out)
    if extra:
        review = json.loads((out / 'core-review.json').read_text())
        if review.get('reviewed_by') != 'assistant' or review.get('core_semantics_passed') is not True:
            raise ValueError('Extra article requires the predefined successful core review')
        events = [(4, json.loads((out / 'extra-item.json').read_text()))]
    else:
        events = list(enumerate(json.loads((out / 'items.json').read_text()), 1))
    uni = universe.load(str(study.ROOT / 'poc/universe.json'))
    with (out / 'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        streams = []
        for sample in [1, 2, 3]:
            arms = ['threads'] if extra else ['control', 'threads'] if sample != 2 else ['threads', 'control']
            for arm in arms:
                label = f'{sample}-{arm}'
                calls = Calls(out, label)
                conn = legacy.open_db(out / f'sample-{label}' / 'views.sqlite')
                streams.append((label, arm, calls, conn))
        stop = False
        for index, item in events:
            for label, arm, calls, conn in streams:
                failed = out / f'sample-{label}' / ('extra-failed.json' if extra else 'failed.json')
                if failed.exists() or store.is_processed(conn, item['input_id']):
                    continue
                try:
                    result = (process if arm == 'threads' else legacy.process)(conn, calls, uni, item, index)
                    study.write_json(out / f'sample-{label}' / f'item{index}-result.json', result)
                    print(f'WRITTEN {label} item={index} new_views={len(result.get("new_views", {}))}', flush=True)
                except Exception as error:
                    conn.rollback()
                    study.write_json(failed, {'item_index': index, 'error': type(error).__name__ + ': ' + str(error)[:1000]})
                    print(f'FAILED {label} item={index}: {error}', flush=True)
                    if 'budget' in str(error).lower():
                        stop = True
                        break
            if stop:
                break
        last_item = events[-1][1]
        for label, arm, calls, conn in streams:
            if store.is_processed(conn, last_item['input_id']):
                route = dispatch.route(conn, last_item, uni)
                study.write_json(out / f'sample-{label}' / ('extra-resend.json' if extra else 'resend.json'),
                                 {'route': route.kind, 'reason': route.reason})
            conn.close()
            calls.archive.conn.close()
    base.report(out)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'core', 'extra', 'report'])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    if args.command == 'prepare':
        prepare(out)
    elif args.command == 'report':
        base.report(out)
    else:
        run(out, args.command == 'extra')
