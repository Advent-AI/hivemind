"""D147: extraction-owned memberships; only referenced subjects reach the writer."""
import argparse
import dataclasses
import fcntl
import json
import re
from pathlib import Path

import flat_membership as previous
import ingestion_groups as base
import ingestion_threads as legacy
import study
from hivemind import dispatch, universe
from hivemind.views import matching, store, writing

EXTRACT_MEMBERSHIP = """ Assign each proposed thesis to the continuing business subject it concerns.
Reuse an existing_subjects ID, or declare a new subject in threads. Describe an ongoing product rollout,
investment program, demand cycle or policy process, including its separate milestones, customers and dates.
A company alone is too broad. Related theses share IDs; a thesis may belong to several subjects.
This is research membership, not a claim that the events are identical or causal."""


def extraction_schema(offered):
    schema = legacy.extraction_schema()
    old_ids = [row['thread_id'] for row in offered]
    ref = {'type': 'string', 'pattern': r'^(?:t[1-9][0-9]*' + ''.join('|' + re.escape(x) for x in old_ids) + ')$'} if old_ids else legacy.LOCAL_ID
    schema['properties']['candidates']['items']['properties']['thread_ids']['items'] = ref
    return schema


def validate_extraction(raw, offered):
    """Only displayed stored IDs and this answer's declared local IDs can own a candidate."""
    errors = study.model.check_schema(raw, extraction_schema(offered))
    if errors:
        raise ValueError('Membership extraction shape: ' + '; '.join(errors))
    ids = [t['id'] for t in raw['threads']]
    if any(re.fullmatch(legacy.LOCAL_ID['pattern'], ident) is None for ident in ids):
        raise ValueError('New subject IDs must use t followed by a positive integer')
    if len(ids) != len(set(ids)) or any(not t['name'].strip() or not t['scope'].strip() for t in raw['threads']):
        raise ValueError('Subjects need unique local IDs, names and scope')
    offered_ids = {row['thread_id'] for row in offered}
    for candidate in raw['candidates']:
        refs = candidate['thread_ids']
        if not refs or len(refs) != len(set(refs)) or set(refs) - set(ids) - offered_ids:
            raise ValueError('Each candidate needs nonempty unique declared or offered subject references')


def process(conn, calls, uni, item, index):
    route = dispatch.route(conn, item, uni)
    if route.kind != 'extract':
        return {'input_id': item['input_id'], 'route': route.kind}
    seq = route.sequence_no
    shown = store.views_for_prompt(conn, [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])])
    offered = legacy.search_threads(conn, {'name': item['title'], 'scope': item['text']}, calls.cfg.search_top_n)
    payload = {'article': {k: item[k] for k in ['input_id', 'title', 'publication_day', 'category', 'text']},
               'objects': [dict(id=k, kind=uni.kind(k)) for k in list(uni.companies) + list(uni.themes)],
               'fiscal_context': [uni.fiscal_note(o['value'], item['publication_day']) for o in item['object_identifiers']],
               'existing_theses': [{k: v[k] for k in ['view_id', 'object_id', 'question', 'looks_at', 'due_day']} for v in shown],
               'existing_subjects': offered}
    raw = calls.stage(f'item{index}-extract', base.EXTRACT_PROMPT + EXTRACT_MEMBERSHIP, payload,
                      extraction_schema(offered), calls.cfg.extraction_setting(item['category']))
    validate_extraction(raw, offered)
    handover = base.sift(raw, item, shown)
    used = {tid for c in handover.candidates for tid in c['thread_ids']}
    threads = [t for t in raw['threads'] if t['id'] in used]
    roots = {ident: ident for ident in used}
    lists = matching.build_lists(conn, handover, shown, calls.cfg.search_top_n)
    payload = base.match_payload(conn, item, handover, lists, shown, None, [])
    payload['candidates'] = [{k: v for k, v in c.items() if k != 'thread_ids'} for c in payload['candidates']]
    answer = calls.stage(f'item{index}-match', base.MATCH_PROMPT, payload,
                         base.matching_schema(False), calls.cfg.matching)
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
              'offered_threads': offered,
              'threads': [dict(r) for r in conn.execute('select * from threads')],
              'memberships': [dict(r) for r in conn.execute('select * from thread_members')],
              'views': [base.view_record(conn, r[0]) for r in conn.execute('select view_id from views')],
              'details': [legacy.thread_detail(conn, r[0], seq) for r in conn.execute('select thread_id from threads')]}
    conn.execute('insert into ingestion_events values (?,?,?)', (seq, item['input_id'], json.dumps(result)))
    dispatch.mark(conn, item, seq, 'written', 'ok', json.dumps({'changed': result['changed_views'], 'threads': affected}))
    dispatch.mark(conn, item, seq, 'handed_over', 'ok', '')
    conn.commit()
    return result

class Calls(base.Calls):
    def __init__(self, out, label):
        super().__init__(out, label)
        self.cfg = dataclasses.replace(self.cfg, version='retained-membership-v1')


def fingerprints():
    return previous.fingerprints() | {str(Path(__file__).relative_to(study.ROOT)): study.digest(__file__)}


def prepare(out):
    previous.verify(out)
    path = out / 'retained-manifest.json'
    if path.exists() or list(out.glob('sample-*-retained')):
        raise ValueError('Use a fresh retained-membership experiment')
    sources = {}
    for sample in [1, 2, 3]:
        source = out / f'sample-{sample}-flat'
        target = out / f'sample-{sample}-retained'
        target.mkdir()
        for file in sorted(source.glob('item*.json')):
            record = json.loads(file.read_text())
            if 'request' not in record:
                continue
            if record['status'] != 'complete':
                raise ValueError('Do not retry an unknown model call')
            record['reused_from'] = str(file)
            study.write_json(target / file.name, record)
            sources[str(file)] = study.digest(file)
    budget = json.loads((out / 'budget.json').read_text())
    study.write_json(path, {'version': 'retained-membership-v1', 'dependencies': fingerprints(),
        'reused_sources': sources, 'shared_attempts_before': len(budget['attempts']),
        'shared_budget_before': budget['estimated_spent']})


def verify(out):
    previous.verify(out)
    manifest = json.loads((out / 'retained-manifest.json').read_text())
    if manifest['dependencies'] != fingerprints() or any(study.digest(path) != sha for path, sha in manifest['reused_sources'].items()):
        raise ValueError('Frozen retained-membership experiment changed')


def run(out, extra=False):
    verify(out)
    if extra:
        review = json.loads((out / 'retained-core-review.json').read_text())
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
            label = f'{sample}-retained'
            calls = Calls(out, label)
            conn = legacy.open_db(out / f'sample-{label}' / 'views.sqlite')
            streams.append((label, calls, conn))
        stop = False
        for index, item in events:
            for label, calls, conn in streams:
                failed = out / f'sample-{label}' / ('extra-failed.json' if extra else 'failed.json')
                if failed.exists() or store.is_processed(conn, item['input_id']):
                    continue
                try:
                    result = process(conn, calls, uni, item, index)
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
        for label, calls, conn in streams:
            if store.is_processed(conn, last_item['input_id']):
                route = dispatch.route(conn, last_item, uni)
                study.write_json(out / f'sample-{label}' / ('extra-resend.json' if extra else 'resend.json'),
                                 {'route': route.kind, 'reason': route.reason})
            conn.close()
            calls.archive.conn.close()
    budget = json.loads((out / 'budget.json').read_text())
    print(f'FINISHED shared_attempts={len(budget["attempts"])} estimated_usd={budget["estimated_spent"]:.6f}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'core', 'extra'])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    if args.command == 'prepare':
        prepare(out)
    else:
        run(out, args.command == 'extra')
