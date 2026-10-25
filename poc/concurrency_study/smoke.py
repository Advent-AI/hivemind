"""Two stored requests per provider; fresh serial controls and two-worker samples."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import contextlib
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'poc'))
sys.path.insert(0, str(ROOT / 'docs/research/2026-10-25-day-batch-review'))
from snapshot_proof import snapshot
from hivemind import config, extraction, jev, model, universe
from hivemind.views import store
from concurrency_study.budget import GuardedTransport, single_attempt_http

CALLS = (574, 575, 577, 578)


def fingerprint(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def readonly(path):
    return contextlib.closing(sqlite3.connect(Path(path).as_uri() + '?mode=ro', uri=True))


def jobs_for(directory):
    """Rebuild all four full requests with current builders before using credentials."""
    cfg = config.load(ROOT / 'poc/config/poc-v23.json')
    uni = universe.load(ROOT / 'poc/universe.json')
    jobs = []
    with readonly(directory / 'inputs/archive.sqlite') as archive, readonly(directory / 'inputs/items.sqlite') as items, readonly(directory / 'inputs/views.sqlite') as views:
        for conn in (archive, items, views):
            conn.row_factory = sqlite3.Row
        for ident in CALLS:
            row = dict(archive.execute('select * from model_calls where call_id=?', (ident,)).fetchone())
            req = json.loads(row['request_json'])
            job = {'original_call_id': ident, 'purpose': row['purpose'], 'request': req}
            if row['purpose'] == 'extract':
                item_id = re.search(r'^\[Item\] id (.+?), category ', req['messages'][1]['content'], re.M).group(1)
                item = dict(items.execute('select * from items where input_id=?', (item_id,)).fetchone())
                item['object_identifiers'] = json.loads(item['object_identifiers'])
                seq = views.execute('select min(sequence_no) from processing_steps where input_id=? and sequence_no>0', (item_id,)).fetchone()[0]
                db = snapshot(views, seq)
                try:
                    objects = [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
                    setting, system, user, schema = extraction.request_for(cfg, item, item['text'], store.views_for_prompt(db, objects), uni, store.groups_for_prompt(db, objects, item['title'] or ''))
                    rebuilt = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
                finally:
                    db.close()
                job.update(setting=setting, system=system, user=user, schema=schema)
            else:
                rebuilt = jev.request_for(cfg.matching, req['state'], req['questions'])
                problems = jev.validate(json.loads(row['answer_json']), req['questions'])
                if problems:
                    raise ValueError('stored Jev control does not validate')
            _, sha = model.request_identity(rebuilt)
            if sha != row['request_sha256'] or rebuilt != req:
                raise ValueError(f'current full request differs from stored call {ident}')
            job['request_sha256'] = sha
            jobs.append(job)
    return cfg, jobs


def call_job(job, archive, cfg, transport):
    """A refusal closes admission in its own worker, before any ordered wait."""
    try:
        return _call_job(job, archive, cfg, transport)
    except BaseException:
        transport.stop('request validation failed or cancelled')
        raise


def _call_job(job, archive, cfg, transport):
    if job['purpose'] == 'extract':
        answer = model.call(archive, cfg, job['setting'], job['system'], job['user'], job['schema'], 'extraction', 'extract', transport=transport)
    else:
        req = job['request']
        answer = jev.ask(archive, cfg, cfg.matching, req['state'], req['questions'], 'match', transport=transport)
    if answer.cached or answer.request_sha256 != job['request_sha256']:
        raise ValueError('smoke response is cached or has a different request identity')
    return {'original_call_id': job['original_call_id'], 'request_sha256': answer.request_sha256,
            'data': answer.data, 'input_tokens': answer.input_tokens, 'output_tokens': answer.output_tokens,
            'standard_list_cost_usd': answer.cost_usd}


def run(directory, *, live=False):
    directory = Path(directory).resolve()
    protected = json.loads((directory / 'protected-before.json').read_text())
    changed = [p for p, expected in protected.items() if not Path(p).is_file() or fingerprint(p) != expected]
    if changed:
        raise ValueError('protected database changed before smoke: ' + ', '.join(changed))
    cfg, jobs = jobs_for(directory)
    manifest = {'calls': [{k: j[k] for k in ('original_call_id', 'purpose', 'request_sha256')} for j in jobs],
                'max_calls': 36, 'cap_usd': 1.5, 'workers': 2, 'samples': 3, 'mode': 'ordinary API concurrency',
                'inputs': {p.name: fingerprint(p) for p in (directory / 'inputs').glob('*.sqlite')},
                'config_sha256': fingerprint(ROOT / 'poc/config/poc-v23.json')}
    manifest_path = directory / 'manifest.json'
    if manifest_path.exists() and json.loads(manifest_path.read_text()) != manifest:
        raise ValueError('smoke manifest changed')
    if not manifest_path.exists():
        with manifest_path.open('x') as handle:
            json.dump(manifest, handle, indent=2)
    if not live:
        print(json.dumps({'prepared': True, **manifest}, indent=2))
        return
    if (directory / 'budget.sqlite').exists():
        raise ValueError('live smoke already attempted; do not silently restart or retry')
    transport = GuardedTransport(directory / 'budget.sqlite', single_attempt_http())
    results, failure = [], None
    try:
        for sample in range(3):
            # Rotate the schedule; the concurrent arm is not always last.
            order = ('control-a', 'control-b', 'concurrent')
            order = order[sample:] + order[:sample]
            for arm in order:
                folder = directory / f'sample-{sample + 1}-{arm}'
                folder.mkdir()
                archive = model.Archive(folder / 'archive.sqlite')
                try:
                    for purpose in ('extract', 'match'):
                        selected = [j for j in jobs if j['purpose'] == purpose]
                        start = time.perf_counter()
                        if arm == 'concurrent':
                            pool = ThreadPoolExecutor(max_workers=2)
                            futures = []
                            try:
                                futures = [pool.submit(call_job, j, archive, cfg, transport) for j in selected]
                                replies = [f.result() for f in futures]
                            except BaseException:
                                transport.stop('study failed or cancelled')
                                for future in futures:
                                    future.cancel()
                                raise
                            finally:
                                pool.shutdown(wait=True, cancel_futures=True)
                        else:
                            replies = [call_job(j, archive, cfg, transport) for j in selected]
                        result = {'sample': sample + 1, 'arm': arm, 'purpose': purpose,
                                  'seconds': round(time.perf_counter() - start, 3), 'answers': replies}
                        results.append(result)
                        (directory / 'progress.json').write_text(json.dumps(results, indent=2, ensure_ascii=False))
                        print(json.dumps({k: result[k] for k in ('sample', 'arm', 'purpose', 'seconds')}), flush=True)
                finally:
                    archive.conn.close()
    except BaseException as exc:
        transport.stop('study failed or cancelled')
        failure = type(exc).__name__
        raise
    finally:
        changed = [p for p, expected in protected.items() if not Path(p).is_file() or fingerprint(p) != expected]
        report = {'failure': failure, 'protected_files': len(protected), 'changed_protected_files': changed,
                  'results': results, 'accounting': transport.summary()}
        (directory / 'result.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
        print(json.dumps({'failure': failure, 'changed_protected_files': changed,
                          'attempts': len(report['accounting']['attempts']),
                          'conservative_cost_usd': report['accounting']['held_microdollars'] / 1e6}), flush=True)
        if changed and failure is None:
            raise ValueError('protected database changed during smoke')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    run(args.directory, live=args.live)
