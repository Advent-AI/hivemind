"""D150: test source-to-scope explanations inside the existing extraction call."""
import argparse
import copy
import fcntl
import json
from pathlib import Path

import grouping_consistency as context_study
import ingestion_groups as base
import ingestion_threads as threads
import retained_membership as retained
import study
from hivemind import dispatch, universe

MAX_REQUESTS = 24
MAX_USD = 1
GOOGLE_ID = 'nvblog:google-cloud-vera-rubin-infrastructure'
LABELS = [f'{sample}-{arm}' for sample in (1, 2, 3) for arm in ('control', 'basis')]
MEMBERSHIP_PROMPT = """ Group each thesis by its continuing business process: product rollout, investment program,
demand cycle or policy process. For each membership, state how this thesis's source fits the subject scope,
then give its ID. Reuse shown subjects or declare a new one; retain all justified memberships. Different
milestones and customers can share a process; a shared company alone is insufficient. Grouping neither
merges theses nor creates causal dependencies."""


def extraction_schema(offered):
    """Keep the old candidate contract, replacing IDs with ordered basis/ID pairs."""
    schema = retained.extraction_schema(offered)
    candidate = schema['properties']['candidates']['items']
    references = candidate['properties'].pop('thread_ids')
    candidate['required'] = ['memberships' if key == 'thread_ids' else key for key in candidate['required']]
    candidate['properties']['memberships'] = {
        'type': 'array', 'minItems': 1,
        'items': study.obj({'basis': study.STRING, 'thread_id': references['items']})}
    return schema


def project(raw, offered):
    """Validate the complete new answer before discarding explanation text for old readers."""
    errors = study.model.check_schema(raw, extraction_schema(offered))
    if errors:
        raise ValueError('Membership basis shape: ' + '; '.join(errors))
    projected = copy.deepcopy(raw)
    for candidate in projected['candidates']:
        memberships = candidate.pop('memberships')
        if any(not member['basis'].strip() for member in memberships):
            raise ValueError('Membership basis must not be empty')
        candidate['thread_ids'] = [member['thread_id'] for member in memberships]
    retained.validate_extraction(projected, offered)
    return projected


class BudgetReached(RuntimeError):
    pass


class Calls(retained.Calls):
    def __init__(self, out, label, source):
        super().__init__(out, label)
        self.source = source
        self.with_basis = label.endswith('-basis')

    def stage(self, name, prompt, payload, schema, setting):
        if name.startswith(('item1-', 'item2-')):
            record = json.loads((self.source / f'{name}.json').read_text())
            expected = study.model.build_request(setting, prompt, json.dumps(payload, ensure_ascii=False),
                                                schema, 'hierarchy_result', self.cfg.provider)
            if record['status'] != 'complete' or record['request'] != expected:
                raise ValueError('Prefix request differs; no prefix HTTP calls are allowed')
            return record['answer']
        if self.with_basis and name.endswith('-extract'):
            if prompt != base.EXTRACT_PROMPT + retained.EXTRACT_MEMBERSHIP:
                raise ValueError('Unexpected extraction prompt')
            offered = payload['existing_subjects']
            raw = super().stage(name, base.EXTRACT_PROMPT + MEMBERSHIP_PROMPT,
                                payload, extraction_schema(offered), setting)
            return project(raw, offered)
        return super().stage(name, prompt, payload, schema, setting)

    def call(self, step, prompt, payload, schema):
        if not (self.out / f'sample-{self.sample}' / f'{step}.json').exists():
            request = study.model.build_request(self.setting, prompt, json.dumps(payload, ensure_ascii=False),
                                                schema, 'hierarchy_result', self.cfg.provider)
            reserve = (len(json.dumps(request, ensure_ascii=False).encode()) * 1.25
                       + self.setting.max_output_tokens * 10) / 1e6
            budget = json.loads((self.out / 'budget.json').read_text())
            if False:
                raise BudgetReached('D150 budget reached; no request sent')
        return super().call(step, prompt, payload, schema)


def fingerprints():
    paths = [Path(__file__), Path(context_study.__file__), study.ROOT / 'poc/config/poc-v7.json',
             study.ROOT / 'src/hivemind/universe.py']
    return retained.fingerprints() | {str(p.relative_to(study.ROOT)): study.digest(p) for p in paths}


def prepare(out, source):
    if out.exists():
        raise ValueError('Use a new dated experiment directory')
    prefix = source / 'sample-2-retained'
    sources = [source / 'items.json', prefix / 'item2-result.json', prefix / 'item3-extract.json']
    sources += [prefix / f'item{i}-{step}.json' for i in (1, 2) for step in ('extract', 'match')]
    hashes = {str(p): study.digest(p) for p in sources}
    items = json.loads((source / 'items.json').read_text())
    if [item['input_id'] for item in items] != base.ITEM_IDS or any(not item['text'] for item in items):
        raise ValueError('Expected the three registered full source articles')
    corpus = study.read_only(base.CORPUS)
    try:
        row = corpus.execute('select * from items where input_id=?', (GOOGLE_ID,)).fetchone()
        if row is None or not row['text']:
            raise ValueError('Missing predefined Google article')
        google = dict(row)
        google['object_identifiers'] = json.loads(google['object_identifiers'])
    finally:
        corpus.close()
    out.mkdir(parents=True)
    for case in ('dev', 'google'):
        for label in LABELS:
            (out / f'sample-{case}-{label}').mkdir()
    study.write_json(out / 'items.json', {'prefix': items[:2], 'dev': items[2], 'google': google})
    study.write_json(out / 'budget.json', {'attempts': [], 'estimated_spent': 0})
    study.write_json(out / 'manifest.json', {
        'version': 'membership-basis-v1', 'source': str(prefix), 'sources': hashes,
        'dependencies': fingerprints(), 'items_sha256': study.digest(out / 'items.json'),
        'labels': LABELS, 'max_requests': MAX_REQUESTS, 'max_estimated_usd': MAX_USD})


def verify(out):
    manifest = json.loads((out / 'manifest.json').read_text())
    if (manifest['dependencies'] != fingerprints()
            or manifest['items_sha256'] != study.digest(out / 'items.json')
            or any(study.digest(path) != sha for path, sha in manifest['sources'].items())):
        raise ValueError('Frozen experiment inputs or code changed')
    return manifest


def run(out, case='dev'):
    with (out / 'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        manifest = verify(out)
        if case == 'google':
            approval = json.loads((out / 'dev-review.json').read_text())
            if approval.get('reviewed_by') != 'assistant' or approval.get('google_conditions_met') is not True:
                raise ValueError('Google requires the registered development review')
        items = json.loads((out / 'items.json').read_text())
        uni = universe.load(str(study.ROOT / 'poc/universe.json'))
        expected = json.loads((Path(manifest['source']) / 'item2-result.json').read_text())['details']
        for label in LABELS:
            verify(out)
            full_label = f'{case}-{label}'
            folder = out / f'sample-{full_label}'
            if (folder / 'failed.json').exists():
                continue
            conn = threads.open_db(folder / 'views.sqlite')
            calls = Calls(out, full_label, Path(manifest['source']))
            try:
                for index, item in enumerate(items['prefix'], 1):
                    retained.process(conn, calls, uni, item, index)
                if context_study.history(conn, 2) != expected:
                    raise ValueError('Fixed prefix differs from stored history')
                result = retained.process(conn, calls, uni, items[case], 3)
                if result['route'] == 'skipped':
                    row = conn.execute('select result_json from ingestion_events where input_id=?',
                                       (items[case]['input_id'],)).fetchone()
                    if row is None:
                        raise ValueError('Completed article is missing its result')
                    result = json.loads(row[0])
                study.write_json(folder / 'item3-result.json', result)
                checks = {'history_unchanged': context_study.history(conn, 2) == expected,
                          'resend': dispatch.route(conn, items[case], uni).kind}
                study.write_json(folder / 'checks.json', checks)
                if not checks['history_unchanged'] or checks['resend'] != 'skipped':
                    raise ValueError('History or resend contract failed')
                print(f'COMPLETE {full_label} new_views={len(result["new_views"])}', flush=True)
            except Exception as error:
                conn.rollback()
                study.write_json(folder / 'failed.json', {'error': type(error).__name__ + ': ' + str(error)[:500]})
                print(f'FAILED {full_label}: {type(error).__name__}: {str(error)[:500]}', flush=True)
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
    parser.add_argument('--case', choices=['dev', 'google'], default='dev')
    args = parser.parse_args()
    if args.command == 'prepare':
        if args.source is None:
            parser.error('prepare requires --source')
        prepare(args.out.resolve(), args.source.resolve())
    else:
        run(args.out.resolve(), args.case)
