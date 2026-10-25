"""Execute D172 on a complete stored day with recorded providers and real storage.

This proves scheduling and record equivalence, not fresh API latency or model quality.
Unknown speculative extraction requests get an empty synthetic response; every
accepted handover must still bind to an original recorded request and answer.
"""
import argparse
import copy
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'poc'))
sys.path.insert(0, str(ROOT / 'docs/research/2026-10-25-day-batch-review'))
from snapshot_proof import snapshot
from hivemind import config, model, replay, testdb, universe
from hivemind.views import store
from hivemind.parallel_day import ParallelDay, digest
from concurrency_study.proof import accepted_requests, handover_errors

SOURCE = ROOT / 'poc/data/english-v23-jev-2026-10-25'
ITEMS = ROOT / 'poc/data/items-window-tags2-2026-10-24.sqlite'
TABLES = ('views', 'rungs', 'evidence', 'evidence_sources', 'evidence_links',
          'dependencies', 'successions', 'thesis_groups', 'thesis_group_members', 'judgements')


def readonly(path):
    conn = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def logical_rows(path):
    ignored = {'created_at', 'call_id', 'id', 'judgement_id'}
    with readonly(path) as db:
        return {table: [{k: r[k] for k in r.keys() if k not in ignored}
                        for r in db.execute(f'select * from {table} order by rowid')]
                for table in TABLES}


class RecordedProvider:
    def __init__(self, calls, delay_scale, limit):
        self.calls, self.scale = calls, delay_scale
        self.lock = threading.Lock()
        self.slots = threading.BoundedSemaphore(limit)
        self.active = self.peak = 0
        self.events = []

    def __call__(self, *args):
        with self.slots:
            return self._call(*args)

    def _call(self, *args):
        request = args[-1]
        sha = model.request_identity(request)[1]
        recorded = self.calls.get(sha)
        exact = recorded is not None
        if recorded:
            response = json.loads(recorded['response_json'])
            duration = recorded['seconds']
            kind = recorded['purpose']
        elif len(args) == 2 and request['response_format']['json_schema']['name'] == 'extraction':
            # Only a prepared request that is never accepted may use this response.
            response = {'choices': [{'message': {'content': json.dumps(
                {'evidence': [], 'candidates': [], 'new_groups': []})}}],
                'usage': {'prompt_tokens': 0, 'completion_tokens': 0}}
            duration, kind = 5.0, 'unrecorded_speculation'
        else:
            raise ValueError('unrecorded authoritative request: ' + sha)
        with self.lock:
            self.active += 1
            self.peak = max(self.peak, self.active)
            event = {'request_sha256': sha, 'kind': kind, 'start': time.perf_counter(),
                     'recorded_seconds': duration, 'synthetic': recorded is None,
                     'exact_recorded_request': exact}
            self.events.append(event)
        try:
            threading.Event().wait(duration * self.scale)
            return copy.deepcopy(response)
        finally:
            with self.lock:
                event['end'] = time.perf_counter()
                self.active -= 1


def validate_handovers(conn, items, cfg, uni, calls, first, events=None):
    """Bind every accepted handover to its exact current-prefix request and answer."""
    hit = lambda key: calls[key]['answer_json'] if key in calls else None
    errors, keys = handover_errors(conn, items, cfg, uni, first, hit, accepted_requests(events) if events is not None else None)
    assert not errors, errors[:5]
    return list(keys.values())


def run(directory, day, workers, delay_scale, source_directory=SOURCE):
    directory = directory.resolve()
    if (directory / 'manifest.json').exists():
        raise ValueError('output already used; preserve it')
    directory.mkdir(parents=True, exist_ok=True)
    protected = {str(p): digest(p) for p in (source_directory / 'views.sqlite', source_directory / 'archive.sqlite', ITEMS)}
    cfg, uni = config.load(ROOT / 'poc/config/poc-v23.json'), universe.load(ROOT / 'poc/universe.json')
    with readonly(source_directory / 'views.sqlite') as source:
        rows = list(source.execute("select distinct input_id,sequence_no from processing_steps "
            "where publication_day=? and sequence_no>0 and input_id not like 'day:%' order by sequence_no", (day,)))
        assert rows and len({r['input_id'] for r in rows}) == len(rows)
        first, last = rows[0]['sequence_no'], rows[-1]['sequence_no']
        baseline = snapshot(source, first, exclude_unordered=True)
        baseline.commit()
        with sqlite3.connect(directory / 'baseline.sqlite') as dest:
            baseline.backup(dest)
        baseline.close()
    selected = {r['input_id'] for r in rows}
    with readonly(ITEMS) as source, sqlite3.connect(directory / 'items.sqlite') as dest:
        schema = source.execute("select sql from sqlite_master where type='table' and name='items'").fetchone()[0]
        dest.execute(schema)
        fields = [r[1] for r in source.execute('pragma table_info(items)')]
        for row in source.execute('select rowid as source_rowid,* from items order by rowid'):
            if row['input_id'] in selected:
                dest.execute(f'insert into items(rowid,{",".join(fields)}) values ({",".join("?" for _ in range(len(fields)+1))})',
                             [row['source_rowid']] + [row[f] for f in fields])
    with readonly(directory / 'items.sqlite') as db:
        ordered = list(testdb.feed(db, day, day))
    assert [i['input_id'] for i in ordered] == [r['input_id'] for r in rows]
    with readonly(source_directory / 'archive.sqlite') as db:
        calls = {r['request_sha256']: dict(r) for r in db.execute(
            "select * from model_calls where config_version='poc-v23' and answer_json is not null")}
    (directory / 'manifest.json').write_text(json.dumps({'day': day, 'inputs': sorted(selected),
        'sequence': [first, last], 'config': cfg.version, 'workers': workers,
        'delay_scale': delay_scale, 'mode': 'recorded provider; not live latency', 'protected': protected}, indent=2))
    results = {}
    for name, count in [('serial', 1), ('parallel', workers)]:
        folder = directory / name
        folder.mkdir()
        shutil.copyfile(directory / 'baseline.sqlite', folder / 'views.sqlite')
        provider = RecordedProvider(calls, delay_scale, workers)
        archive = model.Archive(folder / 'archive.sqlite')
        runner = ParallelDay(directory / 'items.sqlite', folder / 'manifests',
                           extraction_workers=count, jev_workers=count) if count > 1 else None
        started = time.perf_counter()
        result = replay.run(testdb_path=str(directory / 'items.sqlite'), views_path=str(folder / 'views.sqlite'),
            archive=archive, cfg=cfg, universe=uni, from_day=day, until_day=day,
            transport=provider, day_runner=runner, log=lambda s: print(name, s, flush=True))
        elapsed = time.perf_counter() - started
        with readonly(folder / 'views.sqlite') as db:
            accepted = validate_handovers(db, ordered, cfg, uni, calls, first, runner.events if runner else None)
            assert len(accepted) == len(rows)
            assert store.last_completed_day(db) == day
        info = {'result': result, 'synthetic_elapsed_seconds': elapsed, 'provider_peak_inflight': provider.peak,
                'accepted_original_requests': len(accepted), 'events': runner.events if runner else [],
                'provider_events': provider.events}
        (folder / 'result.json').write_text(json.dumps(info, indent=2))
        results[name] = info
        assert provider.peak <= workers
        archive.conn.close()
    a, b = logical_rows(directory / 'serial/views.sqlite'), logical_rows(directory / 'parallel/views.sqlite')
    differences = [table for table in TABLES if a[table] != b[table]]
    changed = [p for p, sha in protected.items() if digest(Path(p)) != sha]
    summary = {'day': day, 'items': len(rows), 'logical_tables_compared': len(TABLES),
        'different_tables': differences, 'changed_protected': changed,
        'serial': {k: v for k, v in results['serial'].items() if 'events' not in k},
        'parallel': {k: v for k, v in results['parallel'].items() if 'events' not in k},
        'stale_preparations': sum(e['event'] == 'stale' for e in results['parallel']['events'])}
    (directory / 'summary.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    assert not differences and not changed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--day', default='2026-07-27')
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--delay-scale', type=float, default=0.01)
    parser.add_argument('--source-directory', type=Path, default=SOURCE)
    args = parser.parse_args()
    run(args.directory, args.day, args.workers, args.delay_scale, args.source_directory.resolve())
