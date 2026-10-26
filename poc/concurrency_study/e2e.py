"""Live end-to-end comparison on one complete day: the serial product path against the ordered concurrent runner.

Both modes start from the same start-of-day ledger, read the same items with the same configuration, and send fresh
requests to the live providers (a fresh archive per trial). A trial's wall time runs from the day's first item to
day completion, daily judging included. Each trial is audited (every accepted handover is rebuilt from its committed
prefix and bound to the exact archived answer), then replayed through the other mode on its own answers with no
network: the same answers must give the same ledger. Fresh model answers are samples, so the trials are compared
with the recorded sequential golden as a drift census, never as an identity check.
"""
import argparse
import dataclasses
import json
from pathlib import Path
import shutil
import signal
import sqlite3
import statistics
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'poc'))
from hivemind import config, model, replay, testdb, universe
from hivemind.views import round as rounds, store
from concurrency_study.budget import GuardedTransport, RetryableError, request_envelope, single_attempt_http
from hivemind.parallel_day import ParallelDay, digest, runtime_key
from concurrency_study.proof import accepted_requests, handover_errors, ledger_rows

DAY = '2026-07-27'
FIXTURE = ROOT / 'poc/reports/2026-10-25-full-day-parallel-r4'   # start-of-day ledger, the day's items, recorded golden
CONFIG = ROOT / 'poc/config/poc-v23.json'
UNIVERSE = ROOT / 'poc/universe.json'
ORDER = ('serial-1', 'parallel-1', 'parallel-2', 'serial-2', 'serial-3', 'parallel-3')
LIMITS = {'cap_microdollars': 4000000, 'max_calls': 2000, 'outbound': 32, 'extraction_workers': 16, 'jev_workers': 8,
          'attempts_per_call': 3}


def readonly(path):
    conn = sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def configuration():
    return config.load(CONFIG), universe.load(UNIVERSE)


def contract(directory):
    cfg, uni = configuration()
    inputs = {name: digest(directory / 'inputs' / name) for name in ('baseline.sqlite', 'items.sqlite', 'gold.sqlite')}
    return {'day': DAY, 'trial_order': list(ORDER), 'config': dataclasses.asdict(cfg), 'universe': vars(uni),
            'runtime': runtime_key(), 'study_code': digest(Path(__file__)), 'inputs': inputs, 'limits': LIMITS}


def prepare(directory):
    """Copy the fixed workload once; later trials refuse a changed contract."""
    if (directory / 'study.json').exists():
        raise ValueError('study already prepared; preserve it')
    (directory / 'inputs').mkdir(parents=True)
    for name, source in (('baseline.sqlite', FIXTURE / 'baseline.sqlite'), ('items.sqlite', FIXTURE / 'items.sqlite'),
                         ('gold.sqlite', FIXTURE / 'serial/views.sqlite')):
        shutil.copyfile(source, directory / 'inputs' / name)
    with readonly(directory / 'inputs/gold.sqlite') as gold:
        assert store.last_completed_day(gold) == DAY, 'golden did not complete the day'
    (directory / 'study.json').write_text(json.dumps(contract(directory), indent=2, ensure_ascii=False))


def day_items(directory):
    with readonly(directory / 'inputs/items.sqlite') as db:
        return list(testdb.feed(db, DAY, DAY))


def first_sequence(directory):
    with readonly(directory / 'inputs/baseline.sqlite') as db:
        return store.next_sequence(db)


class LiveTransport:
    """Bounded outbound slots and bounded retries over one budget journal; one timing event per attempt."""

    def __init__(self, guard, *, outbound, attempts):
        self.guard, self.attempts = guard, attempts
        self.slots = threading.BoundedSemaphore(outbound)
        self.lock = threading.Lock()
        self.active = self.peak = 0
        self.events = []

    def __call__(self, *args):
        request = args[-1]
        kind = request['response_format']['json_schema']['name'] if len(args) == 2 else 'jev'
        for attempt in range(1, self.attempts + 1):
            with self.slots:
                with self.lock:
                    self.active += 1
                    self.peak = max(self.peak, self.active)
                event = {'kind': kind, 'attempt': attempt, 'start': time.perf_counter(), 'request_sha256': model.request_identity(request)[1]}
                try:
                    response = self.guard(*args)
                    event['outcome'] = 'ok'
                    return response
                except RetryableError as error:
                    event['outcome'] = str(error)
                    if attempt == self.attempts:
                        raise
                except BaseException as error:
                    event['outcome'] = type(error).__name__
                    raise
                finally:
                    event['end'] = time.perf_counter()
                    with self.lock:
                        self.active -= 1
                        self.events.append(event)
            threading.Event().wait(2 * attempt)


def refuse_network(*args):
    raise AssertionError('cross-replay request missing from the trial archive')


def audit(directory, folder, cfg, uni, events=None):
    """Rebuild every accepted request from its committed prefix and check the ledger's day records; no model call."""
    items = day_items(directory)
    first = first_sequence(directory)
    errors = []
    with readonly(directory / 'inputs/baseline.sqlite') as baseline, readonly(folder / 'views.sqlite') as conn, \
            readonly(folder / 'archive.sqlite') as archive:
        for table in store.TABLES:
            old = [tuple(r) for r in baseline.execute(f'select * from {table} order by rowid')]
            if old != [tuple(r) for r in conn.execute(f'select * from {table} order by rowid limit ?', (len(old),))]:
                errors.append(f'start-of-day records changed: {table}')
        hands = list(conn.execute('select * from handovers where seq>=? order by seq', (first,)))
        if [(r['input_id'], r['seq']) for r in hands] != [(i['input_id'], first + n) for n, i in enumerate(items)]:
            errors.append('handover order or count differs from dispatch order')

        def answer_for(key):
            row = archive.execute("select request_json,answer_json from model_calls where request_sha256=? and purpose='extract'", (key,)).fetchone()
            if row and model.request_identity(json.loads(row['request_json']))[1] != key:
                errors.append('archived request body differs from its hash')
            return row['answer_json'] if row else None
        errors += handover_errors(conn, items, cfg, uni, first, answer_for, accepted_requests(events) if events is not None else None)[0]
        for record in conn.execute('select * from match_records where seq>=?', (first,)):
            for call in json.loads(record['shown_json']).get('requests', []):
                if not archive.execute('select 1 from model_calls where call_id=? and request_sha256=?', (call['call_id'], call['request_sha256'])).fetchone():
                    errors.append('matching request trace missing')
        changed = rounds.changed_views_of_day(conn, DAY)
        expected_judged = {v for v in changed if store.is_open(conn, v) and store.evidence_in_force(conn, v)}
        judged = list(conn.execute('select * from judgements where seq>=?', (first,)))
        if sorted(r['view_id'] for r in judged) != sorted(expected_judged):
            errors.append('daily judgement population differs')
        if any(r['input_id'] != 'day:' + DAY or r['publication_day'] != DAY for r in judged):
            errors.append('daily judgement record differs')
        if store.last_completed_day(conn) != DAY:
            errors.append('day not completed')
        if conn.execute('select count(*) from thesis_group_members m left join views v using(view_id) left join thesis_groups g using(group_id) '
                        'where v.view_id is null or g.group_id is null').fetchone()[0]:
            errors.append('dangling group membership')
    return {'errors': errors, 'handovers': len(hands), 'judged': len(judged)}


class ArchiveProvider:
    """Serves a trial's own answers to the concurrent runner; an unknown request may only be a speculation that the
    runner then discards (the cross-replay comparison and audit fail if one is accepted)."""

    def __init__(self, archive_path):
        with readonly(archive_path) as db:
            self.calls = {r['request_sha256']: json.loads(r['response_json']) for r in db.execute(
                'select request_sha256,response_json from model_calls where answer_json is not null')}
        self.lock, self.unknown = threading.Lock(), 0

    def __call__(self, *args):
        request = args[-1]
        sha = model.request_identity(request)[1]
        if sha in self.calls:
            return json.loads(json.dumps(self.calls[sha]))
        if len(args) == 2 and request['response_format']['json_schema']['name'] == 'extraction':
            with self.lock:
                self.unknown += 1
            return {'choices': [{'message': {'content': json.dumps({'evidence': [], 'candidates': [], 'new_groups': []})}}],
                    'usage': {'prompt_tokens': 0, 'completion_tokens': 0}}
        raise AssertionError('authoritative request missing from the trial archive: ' + sha)


def cross_replay(directory, trial, cfg, uni):
    """Run the trial's answers through the other mode with no network; the ledger must be identical."""
    folder = directory / trial
    target = folder / 'cross-replay'
    if target.exists():
        shutil.rmtree(target)       # derived data: rebuilt from the trial's own archive
    target.mkdir()
    shutil.copyfile(directory / 'inputs/baseline.sqlite', target / 'views.sqlite')
    if trial.startswith('parallel'):
        shutil.copyfile(folder / 'archive.sqlite', target / 'archive.sqlite')
        transport, runner, unknown = refuse_network, None, None
    else:
        provider = ArchiveProvider(folder / 'archive.sqlite')
        transport, unknown = provider, provider
        runner = ParallelDay(directory / 'inputs/items.sqlite', target / 'manifests',
                           extraction_workers=LIMITS['extraction_workers'], jev_workers=LIMITS['jev_workers'])
    archive = model.Archive(target / 'archive.sqlite')
    try:
        replay.run(testdb_path=str(directory / 'inputs/items.sqlite'), views_path=str(target / 'views.sqlite'), archive=archive,
                   cfg=cfg, universe=uni, from_day=DAY, until_day=DAY, transport=transport, day_runner=runner, log=lambda s: None)
    finally:
        archive.conn.close()
    expected, actual = ledger_rows(folder / 'views.sqlite'), ledger_rows(target / 'views.sqlite')
    different = [table for table in expected if expected[table] != actual[table]]
    checked = audit(directory, target, cfg, uni, runner.events) if runner else None
    return {'mode': 'serial' if runner is None else 'parallel', 'different_tables': different,
            'tables_compared': len(expected), 'rows_compared': sum(len(v) for v in expected.values()),
            'discarded_unknown_speculations': unknown.unknown if unknown else 0,
            'audit_errors': checked['errors'] if checked else []}


def signatures(path, first):
    """One comparable line per item: evidence and candidate counts, existing theses linked, links to new theses, new theses."""
    with readonly(path) as db:
        existing = {r[0] for r in db.execute('select view_id from views where created_seq<?', (first,))}
        result = {}
        for hand in db.execute('select input_id,seq,handover_json from handovers where seq>=? order by seq', (first,)):
            data = json.loads(hand['handover_json'])
            links = [r[0] for r in db.execute('select view_id from evidence_links where seq=?', (hand['seq'],))]
            result[hand['input_id']] = {'evidence': len(data['evidence']), 'candidates': len(data['candidates']),
                                        'existing_linked': sorted({v for v in links if v in existing}),
                                        'new_links': sum(v not in existing for v in links),
                                        'new_views': db.execute('select count(*) from views where created_seq=?', (hand['seq'],)).fetchone()[0]}
        totals = {'evidence_links': db.execute('select count(*) from evidence_links where seq>=?', (first,)).fetchone()[0],
                  'new_evidence': db.execute('select count(*) from evidence where created_seq>=?', (first,)).fetchone()[0],
                  'new_views': db.execute('select count(*) from views where created_seq>=?', (first,)).fetchone()[0],
                  'judged': db.execute('select count(*) from judgements where seq>=?', (first,)).fetchone()[0],
                  'judged_views': sorted(r[0] for r in db.execute('select view_id from judgements where seq>=?', (first,)))}
    return result, totals


def drift(directory, names):
    """Item agreement between every pair of ledgers (the golden included); sampler noise sets the floor."""
    first = first_sequence(directory)
    ledgers = {'gold': directory / 'inputs/gold.sqlite'}
    ledgers.update({n: directory / n / 'views.sqlite' for n in names})
    sig = {n: signatures(p, first) for n, p in ledgers.items()}
    pairs = {}
    keys = list(sig)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            items = sig[a][0]
            same = sum(sig[a][0][k] == sig[b][0].get(k) for k in items)
            linked = sum(sig[a][0][k]['existing_linked'] == sig[b][0].get(k, {}).get('existing_linked') for k in items)
            pairs[f'{a}~{b}'] = {'items_identical': same, 'existing_links_identical': linked, 'items': len(items)}
    return {'totals': {n: s[1] for n, s in sig.items()}, 'pairs': pairs}


class RecordedPrepare:
    """Offline rehearsal of the live path: the golden run's recorded answers at a scaled recorded duration."""

    def __init__(self, archive_path, scale):
        with readonly(archive_path) as db:
            self.calls = {r['request_sha256']: (json.loads(r['response_json']), r['seconds'] or 0.0) for r in db.execute(
                'select request_sha256,response_json,seconds from model_calls where answer_json is not null')}
        self.scale = scale

    def __call__(self, provider, request):
        sha = model.request_identity(request)[1]
        if sha in self.calls:
            response, seconds = self.calls[sha]
        elif provider == 'openai' and request['response_format']['json_schema']['name'] == 'extraction':
            response, seconds = {'choices': [{'message': {'content': json.dumps({'evidence': [], 'candidates': [], 'new_groups': []})}}],
                                 'usage': {'prompt_tokens': 0, 'completion_tokens': 0}}, 7.0
        else:
            raise AssertionError('rehearsal request not recorded: ' + sha)

        def send():
            threading.Event().wait(seconds * self.scale)
            return json.loads(json.dumps(response))
        return send


def passed(report):
    """A trial counts only if it ran, its audit is clean, and the other mode rebuilt the same ledger with a clean audit."""
    crossed = report.get('cross_replay') or {}
    return (not report.get('failure') and not (report.get('audit') or {}).get('errors', ['not audited'])
            and crossed.get('different_tables') == [] and not crossed.get('audit_errors'))


def interrupt(signum, frame):
    """Signal handler: unwind only; the trial closes the budget journal after the interrupted call releases its lock."""
    raise KeyboardInterrupt


def run_trial(directory, trial, *, prepare=None):
    directory = directory.resolve()
    if trial not in ORDER or json.loads((directory / 'study.json').read_text()) != contract(directory):
        raise ValueError('unknown trial or changed study contract')
    for name in ORDER[:ORDER.index(trial)]:
        if not passed(json.loads((directory / name / 'result.json').read_text())):
            raise ValueError(f'prior trial {name} failed; the study stops')
    folder = directory / trial
    if folder.exists():
        raise ValueError('trial already started; preserve it')
    cfg, uni = configuration()
    guard = GuardedTransport(directory / 'budget.sqlite', prepare or single_attempt_http(), cap_microdollars=LIMITS['cap_microdollars'],
                             max_calls=LIMITS['max_calls'], envelope_for=request_envelope, halt_on_failure=False)
    transport = LiveTransport(guard, outbound=LIMITS['outbound'], attempts=LIMITS['attempts_per_call'])
    folder.mkdir()
    shutil.copyfile(directory / 'inputs/baseline.sqlite', folder / 'views.sqlite')
    archive = model.Archive(folder / 'archive.sqlite')
    runner = (ParallelDay(directory / 'inputs/items.sqlite', folder / 'manifests', extraction_workers=LIMITS['extraction_workers'],
                        jev_workers=LIMITS['jev_workers']) if trial.startswith('parallel') else None)
    marks = {}
    original_judge_day = rounds.judge_day

    def timed_judge_day(*args, **kwargs):
        marks['judging_started'] = time.perf_counter()
        try:
            return original_judge_day(*args, **kwargs)
        finally:
            marks['judging_finished'] = time.perf_counter()

    handlers = {sig: signal.signal(sig, interrupt) for sig in (signal.SIGINT, signal.SIGTERM)}
    before = guard.summary()
    failure = result = checked = crossed = None
    rounds.judge_day = timed_judge_day
    started = time.perf_counter()
    try:
        result = replay.run(testdb_path=str(directory / 'inputs/items.sqlite'), views_path=str(folder / 'views.sqlite'), archive=archive,
                            cfg=cfg, universe=uni, from_day=DAY, until_day=DAY, transport=transport, day_runner=runner,
                            log=lambda message: print(trial, message, flush=True))
        finished = time.perf_counter()
    except BaseException as error:
        finished = time.perf_counter()
        guard.stop('trial failed')
        failure = {'type': type(error).__name__, 'message': str(error)[:500]}
    finally:
        rounds.judge_day = original_judge_day
        for sig, handler in handlers.items():
            signal.signal(sig, handler)
        archive.conn.close()
    if failure is None:
        try:
            checked = audit(directory, folder, cfg, uni, runner.events if runner else None)
            crossed = cross_replay(directory, trial, cfg, uni)
        except Exception as error:      # recorded as a failed check, never as a pass
            crossed = {'different_tables': [f'cross-replay failed: {type(error).__name__}: {str(error)[:300]}']}
    after = guard.summary()
    attempts = after['attempts'][len(before['attempts']):]
    with readonly(folder / 'archive.sqlite') as db:
        priced = [dict(r) for r in db.execute('select purpose,model,count(*) n,sum(input_tokens) i,sum(output_tokens) o from model_calls '
                                              'where answer_json is not null group by purpose,model')]
    published = sum(r['i'] / 1e6 * model.PRICES[r['model']][0] + r['o'] / 1e6 * model.PRICES[r['model']][1] for r in priced)
    report = {'trial': trial, 'failure': failure, 'seconds': finished - started,
              'ingestion_seconds': marks.get('judging_started', finished) - started,
              'judging_seconds': marks.get('judging_finished', finished) - marks.get('judging_started', finished),
              'result': result, 'audit': checked or {'errors': ['not audited']}, 'cross_replay': crossed or {'different_tables': ['not run']},
              'provider_peak_inflight': transport.peak, 'attempts': len(attempts),
              'retried_attempts': sum(e['attempt'] > 1 for e in transport.events),
              'conservative_microdollars': after['held_microdollars'] - before['held_microdollars'],
              'published_rate_usd': round(published, 6), 'calls_by_purpose': priced,
              'runner_events': [dict(e, t=e['t'] - started) for e in runner.events] if runner else [],
              'transport_events': [dict(e, start=e['start'] - started, end=e['end'] - started) for e in transport.events]}
    (folder / 'result.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps({k: report[k] for k in ('trial', 'failure', 'seconds', 'ingestion_seconds', 'judging_seconds', 'provider_peak_inflight',
                                             'retried_attempts', 'published_rate_usd')}
                     | {'audit_errors': report['audit']['errors'], 'cross_replay_different': report['cross_replay']['different_tables']}), flush=True)
    if not passed(report):
        raise RuntimeError(f'{trial} failed: {failure or "audit or cross-replay"}')


def summarize(directory):
    directory = directory.resolve()
    done = [n for n in ORDER if (directory / n / 'result.json').exists()]
    reports = {n: json.loads((directory / n / 'result.json').read_text()) for n in done}
    by_mode = {}
    for name, report in reports.items():
        by_mode.setdefault(name.split('-')[0], []).append(report)
    timing = {}
    for mode, rows in by_mode.items():
        timing[mode] = {key: {'samples': [round(r[key], 2) for r in rows], 'median': round(statistics.median(r[key] for r in rows), 2)}
                        for key in ('seconds', 'ingestion_seconds', 'judging_seconds')}
        timing[mode]['published_rate_usd'] = round(sum(r['published_rate_usd'] for r in rows), 6)
    if {'serial', 'parallel'} <= set(timing):
        timing['speedup'] = {key: round(timing['serial'][key]['median'] / timing['parallel'][key]['median'], 3)
                             for key in ('seconds', 'ingestion_seconds', 'judging_seconds')}
    summary = {'trials': done, 'timing': timing,
               'correctness': {n: {'audit_errors': r['audit']['errors'], 'cross_replay': r['cross_replay']} for n, r in reports.items()},
               'drift': drift(directory, done)}
    (directory / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps(summary['timing'], indent=2))
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--trial', choices=ORDER)
    parser.add_argument('--all', action='store_true', help='run every remaining trial in the registered order')
    parser.add_argument('--summarize', action='store_true')
    parser.add_argument('--rehearse', type=float, metavar='SCALE',
                        help='offline: serve the golden run\'s recorded answers at SCALE times their recorded duration')
    args = parser.parse_args()
    directory = args.directory.resolve()
    rehearsal = RecordedPrepare(ROOT / 'poc/reports/2026-10-25-full-day-canonical/archive.sqlite', args.rehearse) if args.rehearse is not None else None
    if args.prepare:
        prepare(directory)
    if args.trial:
        run_trial(directory, args.trial, prepare=rehearsal)
    if args.all:
        for name in ORDER:
            if not (directory / name).exists():
                run_trial(directory, name, prepare=rehearsal)
    if args.summarize or args.all:
        summarize(directory)
