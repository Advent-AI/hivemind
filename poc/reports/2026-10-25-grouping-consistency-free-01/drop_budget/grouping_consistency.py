"""D148: compare existing-membership context on one fixed ingestion prefix."""
import argparse
import fcntl
import json
from pathlib import Path

import ingestion_groups as base
import ingestion_threads as threads
import retained_membership as retained
import study
from hivemind import dispatch, universe

MAX_REQUESTS = 18
MAX_USD = 2
LABELS = [f'{sample}-{arm}' for sample in (1, 2, 3) for arm in ('control', 'context')]


def membership_context(conn, payload):
    """Expose only already-written memberships in the displayed subject set."""
    offered = {row['thread_id'] for row in payload['existing_subjects']}
    shown = []
    for thesis in payload['existing_theses']:
        members = {row[0] for row in conn.execute(
            'select thread_id from thread_members where view_id=?', (thesis['view_id'],))}
        shown.append(thesis | {'thread_ids': sorted(members & offered)})
    return payload | {'existing_theses': shown}


def fingerprints():
    paths = [Path(__file__), study.ROOT / 'poc/config/poc-v7.json',
             study.ROOT / 'src/hivemind/universe.py']
    return retained.fingerprints() | {str(p.relative_to(study.ROOT)): study.digest(p) for p in paths}


class BudgetReached(RuntimeError):
    pass


class Calls(retained.Calls):
    def __init__(self, out, label, conn, source):
        super().__init__(out, label)
        self.conn, self.source = conn, source
        self.context = label.endswith('-context')

    def stage(self, name, prompt, payload, schema, setting):
        if name.startswith(('item1-', 'item2-')):
            record = json.loads((self.source / f'{name}.json').read_text())
            expected = study.model.build_request(setting, prompt, json.dumps(payload, ensure_ascii=False),
                                                  schema, 'hierarchy_result', self.cfg.provider)
            if record['status'] != 'complete' or record['request'] != expected:
                raise ValueError('Prefix request differs; no prefix model calls are allowed')
            return record['answer']
        if self.context and name.endswith('-extract'):
            payload = membership_context(self.conn, payload)
        return super().stage(name, prompt, payload, schema, setting)

    def call(self, step, prompt, payload, schema):
        if not (self.out / f'sample-{self.sample}' / f'{step}.json').exists():
            request = study.model.build_request(self.setting, prompt, json.dumps(payload, ensure_ascii=False),
                                                schema, 'hierarchy_result', self.cfg.provider)
            reserve = (len(json.dumps(request, ensure_ascii=False).encode()) * 1.25
                       + self.setting.max_output_tokens * 10) / 1e6
            budget = json.loads((self.out / 'budget.json').read_text())
            if False:
                raise BudgetReached('D148 budget reached; no request sent')
        return super().call(step, prompt, payload, schema)


def prepare(out, source):
    if out.exists():
        raise ValueError('Use a new dated experiment directory')
    prefix = source / 'sample-2-retained'
    sources = [source / 'items.json', prefix / 'item2-result.json']
    sources += [prefix / f'item{i}-{step}.json' for i in (1, 2) for step in ('extract', 'match')]
    hashes = {str(p): study.digest(p) for p in sources}
    items = json.loads((source / 'items.json').read_text())
    if [item['input_id'] for item in items] != base.ITEM_IDS or any(not item['text'] for item in items):
        raise ValueError('Expected the three complete registered source articles')
    out.mkdir(parents=True)
    for label in LABELS:
        (out / f'sample-{label}').mkdir()
    study.write_json(out / 'items.json', items)
    study.write_json(out / 'budget.json', {'attempts': [], 'estimated_spent': 0})
    study.write_json(out / 'manifest.json', {
        'version': 'grouping-context-diagnostic-v1', 'source': str(prefix), 'sources': hashes,
        'dependencies': fingerprints(), 'items_sha256': study.digest(out / 'items.json'),
        'labels': LABELS, 'max_requests': MAX_REQUESTS, 'max_estimated_usd': MAX_USD})


def verify(out):
    manifest = json.loads((out / 'manifest.json').read_text())
    if (manifest['dependencies'] != fingerprints()
            or manifest['items_sha256'] != study.digest(out / 'items.json')
            or any(study.digest(path) != sha for path, sha in manifest['sources'].items())):
        raise ValueError('Frozen experiment inputs or code changed')
    return manifest


def history(conn, seq):
    return [threads.thread_detail(conn, row[0], seq)
            for row in conn.execute('select thread_id from threads where seq<=? order by rowid', (seq,))]


def run(out):
    with (out / 'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        manifest = verify(out)
        items = json.loads((out / 'items.json').read_text())
        uni = universe.load(str(study.ROOT / 'poc/universe.json'))
        expected = json.loads((Path(manifest['source']) / 'item2-result.json').read_text())['details']
        for label in LABELS:
            verify(out)
            folder = out / f'sample-{label}'
            if (folder / 'failed.json').exists():
                continue
            conn = threads.open_db(folder / 'views.sqlite')
            calls = Calls(out, label, conn, Path(manifest['source']))
            try:
                for index, item in enumerate(items[:2], 1):
                    retained.process(conn, calls, uni, item, index)
                if history(conn, 2) != expected:
                    raise ValueError('Fixed prefix differs from stored history')
                result = retained.process(conn, calls, uni, items[2], 3)
                if result['route'] == 'skipped':
                    row = conn.execute('select result_json from ingestion_events where input_id=?',
                                       (items[2]['input_id'],)).fetchone()
                    if row is None:
                        raise ValueError('Completed article is missing its result')
                    result = json.loads(row[0])
                study.write_json(folder / 'item3-result.json', result)
                checks = {'history_unchanged': history(conn, 2) == expected,
                          'resend': dispatch.route(conn, items[2], uni).kind}
                study.write_json(folder / 'checks.json', checks)
                if not checks['history_unchanged'] or checks['resend'] != 'skipped':
                    raise ValueError('History or resend contract failed')
                print(f'COMPLETE {label} new_views={len(result["new_views"])}', flush=True)
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
        print(f'FINISHED requests={len(budget["attempts"])} estimated_usd={budget["estimated_spent"]:.6f}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'run'])
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--source', type=Path)
    args = parser.parse_args()
    if args.command == 'prepare':
        if args.source is None:
            parser.error('prepare requires --source')
        prepare(args.out.resolve(), args.source.resolve())
    else:
        run(args.out.resolve())
