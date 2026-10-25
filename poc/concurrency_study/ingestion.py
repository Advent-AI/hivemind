"""Selected whole-document ingestion through the product's ordered replay path."""
import argparse
import contextlib
import dataclasses
import json
from pathlib import Path
import shutil
import signal
import sqlite3
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'poc'))
sys.path.insert(0, str(ROOT / 'docs/research/2026-10-25-day-batch-review'))
from snapshot_proof import snapshot
from hivemind import config, extraction, jev, model, replay, testdb, universe
from hivemind.views import round as rounds, store
from concurrency_study.budget import GuardedTransport, single_attempt_http
from concurrency_study.runner import DayRunner, digest, extraction_key

DAY = '2026-07-24'
FIRST = 21
INPUTS = (
    'nvidianews:sk-group-and-nvidia-expand-strategic-partnership-across-ai-factories-and-next-generation-memory',
    'nvidianews:naver-nvidia-and-brookfield-to-expand-koreas-national-ai-factory-infrastructure-buildout',
    'nvblog:ai-summit-korea-partners-and-nvidia',
)
ORDER = ('control-1', 'concurrent-1', 'concurrent-2', 'control-2', 'control-3', 'concurrent-3')
DEFAULT_CONFIG = ROOT / 'poc/config/poc-v23.json'


def readonly(path):
    conn = sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return contextlib.closing(conn)


def protected_changes(directory):
    expected = json.loads((directory / 'protected-before.json').read_text())
    return [name for name, sha in expected.items() if not Path(name).is_file() or digest(Path(name)) != sha]


def baseline_problems(conn):
    problems = []
    for table in store.TABLES:
        fields = [r[1] for r in conn.execute(f'pragma table_info({table})')]
        seq = next((f for f in ('created_seq', 'after_seq', 'seq', 'sequence_no') if f in fields), None)
        if seq and conn.execute(f'select count(*) from {table} where {seq}=0 or {seq}>=?', (FIRST,)).fetchone()[0]:
            problems.append(f'{table}: unordered or future sequence')
        for date in ('publication_day', 'day'):
            if date in fields and conn.execute(f'select count(*) from {table} where {date}>=?', (DAY,)).fetchone()[0]:
                problems.append(f'{table}: future date')
    return problems


def configuration(config_path=DEFAULT_CONFIG):
    return config.load(config_path), universe.load(ROOT / 'poc/universe.json')


def contract(directory, config_path=DEFAULT_CONFIG):
    directory = Path(directory).resolve()
    config_path = Path(config_path).resolve()
    cfg, uni = configuration(config_path)
    paths = [directory / 'items.sqlite', directory / 'ordered-baseline.sqlite',
             config_path, ROOT / 'poc/universe.json', Path(__file__),
             ROOT / 'poc/concurrency_study/budget.py', ROOT / 'poc/concurrency_study/runner.py',
             ROOT / 'docs/research/2026-10-25-day-batch-review/snapshot_proof.py']
    paths += sorted((ROOT / 'src/hivemind').rglob('*.py')) + sorted((ROOT / 'src/hivemind/prompts').glob('*'))
    return {'day': DAY, 'first_sequence': FIRST, 'inputs': list(INPUTS), 'trial_order': list(ORDER),
            'config_path': str(config_path), 'config': dataclasses.asdict(cfg), 'universe': vars(uni),
            'sha256': {str(p): digest(p) for p in paths if p.is_file()},
            'max_calls': 144, 'cap_microdollars': 1500000, 'outbound_workers': 2}


def prepare(directory, *, config_path=DEFAULT_CONFIG):
    directory = Path(directory).resolve()
    path = directory / 'ordered-baseline.sqlite'
    if path.exists() or (directory / 'study.json').exists():
        raise ValueError('study already prepared; preserve it')
    if protected_changes(directory):
        raise ValueError('protected inputs changed')
    with readonly(directory / 'inputs/views.sqlite') as source:
        projected = snapshot(source, FIRST, exclude_unordered=True)
        try:
            problems = baseline_problems(projected)
            if problems:
                raise ValueError('; '.join(problems))
            projected.commit()
            with sqlite3.connect(path) as dest:
                projected.backup(dest)
        finally:
            projected.close()
    with readonly(directory / 'items.sqlite') as conn:
        items = list(testdb.feed(conn, DAY, DAY))
    if [i['input_id'] for i in items] != list(INPUTS):
        raise ValueError('selected input order differs')
    with readonly(directory / 'inputs/items.sqlite') as original:
        for item in items:
            row = dict(original.execute('select * from items where input_id=?', (item['input_id'],)).fetchone())
            row['object_identifiers'] = json.loads(row['object_identifiers'])
            if row != item:
                raise ValueError('selected input changed')
    with (directory / 'study.json').open('x') as handle:
        json.dump(contract(directory, config_path), handle, indent=2, ensure_ascii=False)


class StudyTransport:
    """Shared across extraction, matching and judging; validate before freeing a slot."""

    def __init__(self, guard, workers=2):
        self.guard = guard
        self.slots = threading.BoundedSemaphore(workers)
        self.stopped = threading.Event()

    def stop(self, reason):
        self.guard.stop(reason)
        self.stopped.set()

    def __call__(self, *args):
        with self.slots:
            try:
                response = self.guard(*args)
                request = args[-1]
                if len(args) == 2:
                    value = json.loads(response['choices'][0]['message']['content'])
                    errors = model.check_schema(value, request['response_format']['json_schema']['schema'])
                else:
                    errors = jev.validate(response.get('answers'), request['questions'])
                if errors:
                    raise model.SchemaError('; '.join(errors[:5]))
                return response
            except BaseException:
                self.stop('terminal worker failure or cancellation')
                raise


def study_day(runner, transport):
    def run(*args, **kwargs):
        iterator = runner(*args, **kwargs)
        try:
            for result in iterator:
                if result.failed:
                    transport.stop('authoritative item failed')
                yield result
        except BaseException:
            transport.stop('day cancelled or failed')
            raise
        finally:
            iterator.close()
    return run


def audit(directory, trial, cfg, uni):
    """Read actual product records and rebuild the accepted requests; never call a model."""
    folder = directory / trial
    errors, requests = [], []
    with readonly(directory / 'ordered-baseline.sqlite') as baseline, readonly(folder / 'views.sqlite') as conn, readonly(folder / 'archive.sqlite') as archive, readonly(directory / 'items.sqlite') as source:
        items = {i['input_id']: i for i in testdb.feed(source, DAY, DAY)}
        for table in store.TABLES:
            old = [tuple(r) for r in baseline.execute(f'select * from {table} order by rowid')]
            prefix = [tuple(r) for r in conn.execute(f'select * from {table} order by rowid limit ?', (len(old),))]
            if old != prefix:
                errors.append(f'baseline changed: {table}')
        hands = list(conn.execute('select * from handovers where seq>=? order by seq', (FIRST,)))
        if [(r['input_id'], r['seq']) for r in hands] != [(i, FIRST + n) for n, i in enumerate(INPUTS)]:
            errors.append('handover order/count differs')
        for hand in hands:
            item = items[hand['input_id']]
            before = snapshot(conn, hand['seq'], exclude_unordered=True)
            try:
                objects = [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
                shown = store.views_for_prompt(before, objects)
                groups = store.groups_for_prompt(before, objects, item.get('title') or '')
                key = extraction_key(cfg, item, item['text'], shown, uni, groups)
            finally:
                before.close()
            accepted = archive.execute("select call_id,request_json,answer_json from model_calls where request_sha256=? and purpose='extract'", (key,)).fetchone()
            if not accepted:
                errors.append('accepted request not rebuilt: ' + item['input_id'])
            else:
                if model.request_identity(json.loads(accepted['request_json']))[1] != key:
                    errors.append('archived request hash differs from body')
                version = cfg.extraction_setting(item['category']).prompt_version.rpartition('-')[2]
                evidence, candidates, dropped, new_groups = extraction.sift_with_groups(
                    json.loads(accepted['answer_json']), item, item['text'], {v['view_id'] for v in shown}, uni,
                    english=extraction.is_english(version), shown_group_ids=[g['group_id'] for g in groups])
                expected_hand = {'evidence': evidence, 'candidates': candidates, 'dropped': dropped, 'new_groups': new_groups}
                if json.loads(json.dumps(expected_hand)) != json.loads(hand['handover_json']):
                    errors.append('accepted handover differs from the bound request answer: ' + item['input_id'])
            requests.append({'input_id': item['input_id'], 'seq': hand['seq'], 'request_sha256': key,
                             'call_id': accepted['call_id'] if accepted else None})
            for evidence in json.loads(hand['handover_json'])['evidence']:
                if extraction.normalise(evidence['quote']) not in extraction.normalise(item['text']):
                    errors.append('quote missing from selected whole item')
        for record in conn.execute('select * from match_records where seq>=?', (FIRST,)):
            if json.loads(record['checks_json'])['refusals']:
                errors.append('matching refusal')
            for call in json.loads(record['shown_json']).get('requests', []):
                if not archive.execute('select 1 from model_calls where call_id=? and request_sha256=?', (call['call_id'], call['request_sha256'])).fetchone():
                    errors.append('matching request trace missing')
        changed = rounds.changed_views_of_day(conn, DAY)
        expected = {v for v in changed if store.is_open(conn, v) and store.evidence_in_force(conn, v)}
        judgments = list(conn.execute('select * from judgements where seq>=?', (FIRST,)))
        if sorted(r['view_id'] for r in judgments) != sorted(expected):
            errors.append('daily judgement population differs')
        if any(r['seq'] != FIRST + len(INPUTS) - 1 or r['input_id'] != 'day:' + DAY or r['publication_day'] != DAY for r in judgments):
            errors.append('daily judgement ordering differs')
        if store.last_completed_day(conn) != DAY:
            errors.append('day not completed')
        missing = conn.execute('select count(*) from thesis_group_members m left join views v using(view_id) left join thesis_groups g using(group_id) where v.view_id is null or g.group_id is null').fetchone()[0]
        if missing:
            errors.append('dangling group membership')
        views = [dict(r) for r in conn.execute('select * from views order by rowid')]
        groups = [dict(r) for r in conn.execute('select * from thesis_groups order by rowid')]
        members = [dict(r) for r in conn.execute('select * from thesis_group_members order by rowid')]
        evidence = [dict(r) for r in conn.execute('select * from evidence order by rowid')]
        links = [dict(r) for r in conn.execute('select * from evidence_links order by rowid')]
        sources = [dict(r) for r in conn.execute('select * from evidence_sources order by rowid')]
        return {'errors': errors, 'accepted_requests': requests, 'views': views, 'groups': groups, 'members': members,
                'evidence': evidence, 'links': links, 'sources': sources, 'judgements': [dict(r) for r in judgments],
                'baseline_dependencies': baseline.execute('select count(*) from dependencies').fetchone()[0]}


def run_trial(directory, trial, *, live=False, transport=None, config_path=DEFAULT_CONFIG):
    directory = Path(directory).resolve()
    if trial not in ORDER or contract(directory, config_path) != json.loads((directory / 'study.json').read_text()):
        raise ValueError('unknown trial or changed study contract')
    previous = ORDER[:ORDER.index(trial)]
    for name in previous:
        saved = json.loads((directory / name / 'result.json').read_text())
        if saved['failure'] or saved['audit']['errors']:
            raise ValueError('prior trial failed')
    if protected_changes(directory):
        raise ValueError('protected database changed')
    folder = directory / trial
    if folder.exists():
        raise ValueError('trial already started; preserve it')
    cfg, uni = configuration(config_path)
    if transport is None:
        if not live:
            raise ValueError('explicit offline transport or --live required')
        transport = StudyTransport(GuardedTransport(directory / 'budget.sqlite', single_attempt_http(), max_calls=144))
    folder.mkdir()
    shutil.copyfile(directory / 'ordered-baseline.sqlite', folder / 'views.sqlite')
    archive = model.Archive(folder / 'archive.sqlite')
    runner = DayRunner(directory / 'items.sqlite', folder / 'manifests') if trial.startswith('concurrent') else None
    before = transport.guard.summary()
    old_handlers = {}
    if live:
        def cancel(signum, frame):
            transport.stop('cancelled')
            raise KeyboardInterrupt
        for sig in (signal.SIGINT, signal.SIGTERM):
            old_handlers[sig] = signal.signal(sig, cancel)
    failed, result, inspected = None, None, None
    started = time.perf_counter()
    try:
        result = replay.run(testdb_path=str(directory / 'items.sqlite'), views_path=str(folder / 'views.sqlite'), archive=archive,
                            cfg=cfg, universe=uni, from_day=DAY, until_day=DAY, transport=transport,
                            day_runner=study_day(runner, transport) if runner else None, log=lambda msg: print(msg, flush=True))
        inspected = audit(directory, trial, cfg, uni)
        if inspected['errors']:
            raise ValueError('structural audit failed: ' + '; '.join(inspected['errors']))
    except BaseException as exc:
        transport.stop('trial failed')
        failed = {'type': type(exc).__name__, 'message': str(exc)[:500]}
        raise
    finally:
        elapsed = time.perf_counter() - started
        for sig, handler in old_handlers.items():
            signal.signal(sig, handler)
        archive.conn.close()
        after = transport.guard.summary()
        report = {'trial': trial, 'seconds': elapsed, 'failure': failed, 'result': result, 'audit': inspected,
                  'events': runner.events if runner else [], 'changed_protected': protected_changes(directory),
                  'new_attempts': after['attempts'][len(before['attempts']):],
                  'conservative_cost_microdollars': after['held_microdollars'] - before['held_microdollars']}
        (folder / 'result.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
        print(json.dumps({k: report[k] for k in ('trial', 'seconds', 'failure', 'changed_protected', 'conservative_cost_microdollars')}), flush=True)
        if report['changed_protected'] and not failed:
            raise ValueError('protected database changed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--config', type=Path, default=DEFAULT_CONFIG)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--trial', choices=ORDER)
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    if args.prepare:
        prepare(args.directory.resolve(), config_path=args.config.resolve())
    elif args.trial:
        run_trial(args.directory, args.trial, live=args.live, config_path=args.config.resolve())
    else:
        parser.error('choose --prepare or --trial')
