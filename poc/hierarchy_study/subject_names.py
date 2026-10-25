"""D152 slice: the model names the business subject of each proposed thesis (a shown subject's name, or a new name
and scope) and writes no IDs; code binds names to stored IDs and projects to the D147 shape, so every downstream
check and the writer stay as they are. Plan and tables: docs/research/2026-10-25-subject-names/plan.md."""
import argparse
import copy
import fcntl
import json
import re
from pathlib import Path

import grouping_consistency as context_study
import ingestion_groups as base
import ingestion_threads as threads
import retained_membership as retained
import study
from hivemind import dispatch, universe

MAX_REQUESTS = 24
MAX_USD = 1.5
GOOGLE_ID = 'nvblog:google-cloud-vera-rubin-infrastructure'
AMD_ID = 'gnews:7ce0b7c3361fc5060098941f'
ARMS = ('names', 'control')
SUBJECT_PROMPT = """ For each proposed thesis name the continuing business subject it belongs to: a product rollout, an
investment program, a demand cycle or a policy process, with its milestones, customers and dates. If it is one of the
shown subjects, pick that subject's name under existing; otherwise set existing to none and give the new subject a
name and a scope. A company alone is too broad; a customer-specific subject takes only that customer's theses, while
a deployment that uses the product also belongs to the product's subject. A thesis may belong to several subjects.
Membership neither merges theses nor implies causation."""


def normalize(name):
    return re.sub(r'\s+', ' ', name.replace('–', '-').replace('—', '-').replace('’', "'").replace('‘', "'")).strip().casefold()


def extraction_schema(offered):
    """The D147 candidate contract with `subjects` in place of `thread_ids`, and no separate definitions list."""
    schema = retained.extraction_schema(offered)
    candidate = schema['properties']['candidates']['items']
    candidate['properties'].pop('thread_ids')
    candidate['required'] = ['subjects' if key == 'thread_ids' else key for key in candidate['required']]
    names = [row['name'] for row in offered]
    candidate['properties']['subjects'] = {
        'type': 'array', 'minItems': 1,
        'items': study.obj({'existing': {'type': 'string', 'enum': names + ['none']}, 'new_name': study.STRING, 'new_scope': study.STRING})}
    schema['properties'].pop('threads')
    schema['required'] = [key for key in schema['required'] if key != 'threads']
    return schema


def project(raw, offered):
    """Names → IDs: a shown name to its stored ID, each distinct new name to a local t ID with a declaration; a new name
    that equals a shown one resolves to the stored subject and is counted. Returns the D147-shaped answer and the counts."""
    errors = study.model.check_schema(raw, extraction_schema(offered))
    if errors:
        raise ValueError('Subject names shape: ' + '; '.join(errors))
    by_name = {normalize(row['name']): row['thread_id'] for row in offered}
    if len(by_name) != len(offered):
        raise ValueError('Shown subject names collide after normalisation')
    projected = copy.deepcopy(raw)
    new_ids, declarations, counts = {}, [], {'existing_refs': 0, 'new_subjects': 0, 'redeclared_existing': 0}
    for candidate in projected['candidates']:
        refs = []
        for subject in candidate.pop('subjects'):
            if subject['existing'] != 'none':
                if subject['new_name'].strip() or subject['new_scope'].strip():
                    raise ValueError('An existing subject carries no new name or scope')
                refs.append(by_name[normalize(subject['existing'])])
                counts['existing_refs'] += 1
                continue
            name, scope = subject['new_name'].strip(), subject['new_scope'].strip()
            if not name or not scope:
                raise ValueError('A new subject needs a name and a scope')
            key = normalize(name)
            if key in by_name:
                counts['redeclared_existing'] += 1
                refs.append(by_name[key])
                continue
            if key not in new_ids:
                new_ids[key] = f't{len(new_ids) + 1}'
                declarations.append({'id': new_ids[key], 'name': name, 'scope': scope})
                counts['new_subjects'] += 1
            refs.append(new_ids[key])
        candidate['thread_ids'] = list(dict.fromkeys(refs))
    projected['threads'] = declarations
    retained.validate_extraction(projected, offered)
    return projected, counts


class BudgetReached(RuntimeError):
    pass


class Calls(retained.Calls):
    def __init__(self, out, label, source):
        super().__init__(out, label)
        self.source = source
        self.names_arm = label.endswith('-names')

    def stage(self, name, prompt, payload, schema, setting):
        if name.startswith(('item1-', 'item2-')):
            record = json.loads((self.source / f'{name}.json').read_text())
            expected = study.model.build_request(setting, prompt, json.dumps(payload, ensure_ascii=False), schema, 'hierarchy_result', self.cfg.provider)
            if record['status'] != 'complete' or record['request'] != expected:
                raise ValueError('Prefix request differs; no prefix HTTP calls are allowed')
            return record['answer']
        if self.names_arm and name.endswith('-extract'):
            if prompt != base.EXTRACT_PROMPT + retained.EXTRACT_MEMBERSHIP:
                raise ValueError('Unexpected extraction prompt')
            offered = payload['existing_subjects']
            raw = super().stage(name, base.EXTRACT_PROMPT + SUBJECT_PROMPT, payload, extraction_schema(offered), setting)
            projected, counts = project(raw, offered)
            study.write_json(self.out / f'sample-{self.sample}' / f'{name}-projection.json', {'counts': counts, 'subjects': [c['subjects'] for c in raw['candidates']], 'thread_ids': [c['thread_ids'] for c in projected['candidates']], 'threads': projected['threads']})
            return projected
        return super().stage(name, prompt, payload, schema, setting)

    def call(self, step, prompt, payload, schema):
        if not (self.out / f'sample-{self.sample}' / f'{step}.json').exists():
            request = study.model.build_request(self.setting, prompt, json.dumps(payload, ensure_ascii=False), schema, 'hierarchy_result', self.cfg.provider)
            reserve = (len(json.dumps(request, ensure_ascii=False).encode()) * 1.25 + self.setting.max_output_tokens * 10) / 1e6
            budget = json.loads((self.out / 'budget.json').read_text())
            if len(budget['attempts']) >= MAX_REQUESTS or budget['estimated_spent'] + reserve > MAX_USD:
                raise BudgetReached('subject-names budget reached; no request sent')
        return super().call(step, prompt, payload, schema)


def fingerprints():
    paths = [Path(__file__), Path(context_study.__file__), study.ROOT / 'poc/config/poc-v7.json', study.ROOT / 'src/hivemind/universe.py']
    return retained.fingerprints() | {str(p.relative_to(study.ROOT)): study.digest(p) for p in paths}


def labels(case, samples):
    return [f'{case}-{k}-{arm}' for k in range(1, samples + 1) for arm in ARMS]


def prepare(out, source, samples=3, controls=1):
    if out.exists():
        raise ValueError('Use a new dated experiment directory')
    prefix = source / 'sample-2-retained'
    sources = [source / 'items.json', prefix / 'item2-result.json'] + [prefix / f'item{i}-{step}.json' for i in (1, 2) for step in ('extract', 'match')]
    hashes = {str(p): study.digest(p) for p in sources}
    items = json.loads((source / 'items.json').read_text())
    if [item['input_id'] for item in items] != base.ITEM_IDS or any(not item['text'] for item in items):
        raise ValueError('Expected the three registered full source articles')
    corpus = study.read_only(base.CORPUS)
    try:
        held = {}
        for case, input_id in (('google', GOOGLE_ID), ('amd', AMD_ID)):
            row = corpus.execute('select * from items where input_id=?', (input_id,)).fetchone()
            if row is None or not row['text']:
                raise ValueError(f'Missing held-out article {input_id}')
            held[case] = dict(row)
            held[case]['object_identifiers'] = json.loads(held[case]['object_identifiers'])
    finally:
        corpus.close()
    out.mkdir(parents=True)
    plan = {'dev': [f'dev-{k}-names' for k in range(1, samples + 1)] + [f'dev-{k}-control' for k in range(1, controls + 1)],
            'google': [f'google-{k}-names' for k in range(1, samples + 1)], 'amd': [f'amd-{k}-names' for k in range(1, samples + 1)]}
    for case in plan:
        for label in plan[case]:
            (out / f'sample-{label}').mkdir()
    study.write_json(out / 'items.json', {'prefix': items[:2], 'dev': items[2], **held})
    study.write_json(out / 'budget.json', {'attempts': [], 'estimated_spent': 0})
    study.write_json(out / 'manifest.json', {'version': 'subject-names-v1', 'source': str(prefix), 'sources': hashes, 'dependencies': fingerprints(),
                                              'items_sha256': study.digest(out / 'items.json'), 'plan': plan, 'max_requests': MAX_REQUESTS, 'max_estimated_usd': MAX_USD})


def verify(out):
    manifest = json.loads((out / 'manifest.json').read_text())
    if manifest['dependencies'] != fingerprints() or manifest['items_sha256'] != study.digest(out / 'items.json') or any(study.digest(path) != sha for path, sha in manifest['sources'].items()):
        raise ValueError('Frozen experiment inputs or code changed')
    return manifest


def run(out, case='dev'):
    with (out / 'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        manifest = verify(out)
        if case != 'dev':
            review = json.loads((out / 'dev-review.json').read_text())
            if review.get('reviewed_by') != 'assistant' or review.get('wiring_errors') != 0:
                raise ValueError('A held-out case needs the recorded development review with zero wiring errors')
        items = json.loads((out / 'items.json').read_text())
        uni = universe.load(str(study.ROOT / 'poc/universe.json'))
        expected = json.loads((Path(manifest['source']) / 'item2-result.json').read_text())['details']
        for label in manifest['plan'][case]:
            verify(out)
            folder = out / f'sample-{label}'
            if (folder / 'failed.json').exists() or (folder / 'item3-result.json').exists():
                continue
            conn = threads.open_db(folder / 'views.sqlite')
            calls = Calls(out, label, Path(manifest['source']))
            try:
                for index, item in enumerate(items['prefix'], 1):
                    retained.process(conn, calls, uni, item, index)
                if context_study.history(conn, 2) != expected:
                    raise ValueError('Fixed prefix differs from stored history')
                result = retained.process(conn, calls, uni, items[case], 3)
                if result['route'] == 'skipped':
                    row = conn.execute('select result_json from ingestion_events where input_id=?', (items[case]['input_id'],)).fetchone()
                    if row is None:
                        raise ValueError('Completed article is missing its result')
                    result = json.loads(row[0])
                study.write_json(folder / 'item3-result.json', result)
                checks = {'history_unchanged': context_study.history(conn, 2) == expected, 'resend': dispatch.route(conn, items[case], uni).kind}
                study.write_json(folder / 'checks.json', checks)
                if not checks['history_unchanged'] or checks['resend'] != 'skipped':
                    raise ValueError('History or resend contract failed')
                print(f'COMPLETE {label} new_views={len(result["new_views"])} memberships={[(m["thread_id"], m["view_id"]) for m in result["memberships"]]}', flush=True)
            except Exception as error:
                conn.rollback()
                study.write_json(folder / 'failed.json', {'error': type(error).__name__ + ': ' + str(error)[:500]})
                print(f'FAILED {label}: {type(error).__name__}: {str(error)[:500]}', flush=True)
                if isinstance(error, BudgetReached):
                    break
            finally:
                calls.archive.conn.close()
                conn.close()
        verify(out)
        budget = json.loads((out / 'budget.json').read_text())
        print(f'FINISHED {case} requests={len(budget["attempts"])} estimated_usd={budget["estimated_spent"]:.6f}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'run'])
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--case', choices=['dev', 'google', 'amd'], default='dev')
    args = parser.parse_args()
    if args.command == 'prepare':
        if args.source is None:
            parser.error('prepare requires --source')
        prepare(args.out.resolve(), args.source.resolve())
    else:
        run(args.out.resolve(), args.case)
