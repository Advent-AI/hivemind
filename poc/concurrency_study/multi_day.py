"""Fifteen days of items through the serial product path and the parallel day, with no network (D182).

Both modes start from the July 31 ledger of the recorded run poc/data/english-v23-jev-2026-10-25 (poc-v23) and replay
August 1–15 from the same items with the current code. The recorded run's own answers cannot serve them: it predates
D168, whose matching and writing rules make the current ledger, and so every later request, differ from the
recording. Every call is answered instead by one deterministic oracle, a function of the request bytes only, so the
same request gets the same answer in every mode:

- extraction: the recorded answer for the same item, each evidence line tagged with the request's digest, so a ledger
  built from an answer to any other request differs;
- Jev: each question's choice drawn from the request digest and question id, mostly 'different' or 'false';
- judging: rung 1, nothing cited, changed (valid for every view).

Answers arrive after a scaled duration: the item's recorded extraction time, the recorded median Jev and judging time.
The parallel ledger must equal the serial ledger in every product table plus handovers and match decisions, and the
requests its turns accepted must be exactly the serial run's extraction requests. A mutant runner that accepts a
prepared answer without re-preparing or checking its request must produce a different ledger, which shows the comparison can see the
defect it guards against. Times are an estimate of the per-day speed-up, not a live measurement.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import statistics
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'poc'))
from hivemind import config, model, replay, testdb, universe  # noqa: E402
from hivemind import parallel_day  # noqa: E402
from hivemind.views import round as rounds  # noqa: E402
from concurrency_study.e2e import logical_rows, readonly  # noqa: E402
from concurrency_study.proof import accepted_requests  # noqa: E402

SOURCE = ROOT / 'poc/data/english-v23-jev-2026-10-25'
ITEMS = ROOT / 'poc/data/items-window-tags2-2026-10-24.sqlite'
START_LEDGER, RECORDED_ARCHIVE = SOURCE / 'views.week.sqlite', SOURCE / 'archive.sqlite'
FIRST_DAY, LAST_DAY = '2026-08-01', '2026-08-15'
WORKERS = {'extraction_workers': 16, 'jev_workers': 8}
OUTBOUND = 32
EMPTY_EXTRACTION = {'evidence': [], 'candidates': [], 'new_groups': []}
RELATION_WEIGHTS = {'different': 0.5, 'same_matter_different_quantity': 0.2, 'part_of': 0.12, 'same_quantity_or_event': 0.12,
                    'same_quantity_other_period': 0.03, 'cannot_tell': 0.03}
PIECE_WEIGHTS = {'different': 0.85, 'same_statement': 0.1, 'supersedes': 0.05}


def fraction(*parts):
    return int(hashlib.sha256('|'.join(parts).encode()).hexdigest()[:8], 16) / 0xFFFFFFFF


def weighted(options, weights, draw):
    total = 0.0
    for option, weight in zip(options, weights):
        total += weight
        if draw < total:
            return option
    return options[-1]


class Oracle:
    """One deterministic answer per request; at most OUTBOUND calls in flight, each after its scaled duration."""

    def __init__(self, delay_scale):
        with readonly(RECORDED_ARCHIVE) as db:
            rows = [dict(r) for r in db.execute("select purpose,request_json,answer_json,seconds from model_calls "
                                                "where config_version='poc-v23' and answer_json is not null")]
        with readonly(ITEMS) as db:
            items = list(testdb.feed(db, FIRST_DAY, LAST_DAY))
        self.snippets = {}
        for item in items:
            snippet = json.dumps(item['text'], ensure_ascii=False)[1:301]
            recorded = [r for r in rows if r['purpose'] == 'extract' and snippet in r['request_json']]
            if recorded:
                self.snippets[snippet] = (json.loads(recorded[0]['answer_json']), recorded[0]['seconds'] or 0.0)
        self.jev_seconds = statistics.median(r['seconds'] for r in rows if r['purpose'] == 'match')
        self.judge_seconds = statistics.median(r['seconds'] for r in rows if r['purpose'] == 'judge')
        self.delay_scale = delay_scale
        self.slots, self.lock = threading.BoundedSemaphore(OUTBOUND), threading.Lock()
        self.counts = {'extraction': 0, 'extraction_without_recorded_answer': 0, 'jev': 0, 'judgement': 0}
        self.inflight = self.peak_inflight = 0

    def _extraction(self, request, request_sha):
        request_json = json.dumps(request, ensure_ascii=False)
        found = next((value for snippet, value in self.snippets.items() if snippet in request_json), None)
        answer, seconds = copy.deepcopy(found) if found else (copy.deepcopy(EMPTY_EXTRACTION), 7.0)
        for evidence in answer['evidence']:
            evidence['one_line'] = f"{evidence['one_line']} [r:{request_sha[:8]}]"
        return answer, seconds, found is not None

    def _jev(self, request, request_sha):
        answers = {}
        for question_id, question in request['questions'].items():
            draw = fraction(request_sha, question_id)
            if question['type'] == 'noul':
                answers[question_id] = {'type': 'noul', 'noul': 0.9 if draw < 0.08 else 0.03}
                continue
            weights = PIECE_WEIGHTS if 'supersedes' in question['criteria'] else RELATION_WEIGHTS
            options = [option for option in weights if option in question['criteria']]
            choice = weighted(options, [weights[o] for o in options], draw * sum(weights[o] for o in options))
            rest = round(0.1 / (len(question['criteria']) - 1), 4)
            probabilities = {option: (round(1 - rest * (len(question['criteria']) - 1), 4) if option == choice else rest)
                             for option in question['criteria']}
            answers[question_id] = {'type': 'choice', 'choice': choice, 'confidence': probabilities[choice], 'probabilities': probabilities}
        return {'model': request['model'], 'answers': answers}

    def __call__(self, *args):
        request = args[-1]
        request_sha = model.request_identity(request)[1]
        if len(args) == 1:
            response, seconds, kind = self._jev(request, request_sha), self.jev_seconds, 'jev'
        elif request['response_format']['json_schema']['name'] == 'extraction':
            answer, seconds, recorded = self._extraction(request, request_sha)
            kind = 'extraction' if recorded else 'extraction_without_recorded_answer'
            response = {'choices': [{'message': {'content': json.dumps(answer, ensure_ascii=False)}}],
                        'usage': {'prompt_tokens': 0, 'completion_tokens': 0}}
        elif request['response_format']['json_schema']['name'] == 'judgement':
            answer = {'rung': 1, 'reasons': f'oracle [r:{request_sha[:8]}]', 'cites': [], 'cites_views': [], 'pushes': [],
                      'changed': True, 'why_changed': 'oracle'}
            response, seconds, kind = ({'choices': [{'message': {'content': json.dumps(answer)}}],
                                        'usage': {'prompt_tokens': 0, 'completion_tokens': 0}}, self.judge_seconds, 'judgement')
        else:
            raise AssertionError('unexpected request kind')
        with self.slots:
            with self.lock:
                self.counts[kind] += 1
                self.inflight += 1
                self.peak_inflight = max(self.peak_inflight, self.inflight)
            try:
                threading.Event().wait(seconds * self.delay_scale)
            finally:
                with self.lock:
                    self.inflight -= 1
        return response


def mutant_runner_class():
    """ParallelDay without its two guards, the re-preparation after each commit and the turn check: a prepared answer is
    accepted whatever request it answered."""
    source = Path(parallel_day.__file__).read_text()
    for old, new in (('            for input_id, (key, _, future, item) in list(pending.items()):\n',
                      '            return\n            for input_id, (key, _, future, item) in list(pending.items()):\n'),
                     ('            if current_key == prior_key:\n', '            if True:\n'),
                     ('                if answer.request_sha256 != current_key:\n', '                if False:\n')):
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    spec = importlib.util.spec_from_loader('hivemind.parallel_day_mutant', loader=None)
    module = importlib.util.module_from_spec(spec)
    module.__package__ = 'hivemind'
    module.__file__ = parallel_day.__file__
    exec(compile(source, 'parallel_day_mutant', 'exec'), module.__dict__)
    return module.ParallelDay


def extraction_requests(archive_path):
    with readonly(archive_path) as db:
        return sorted(row[0] for row in db.execute("select request_sha256 from model_calls where purpose='extract'"))


def run_mode(output, mode, cfg, uni, delay_scale):
    folder = output / mode
    folder.mkdir()
    shutil.copyfile(START_LEDGER, folder / 'views.sqlite')
    archive = model.Archive(folder / 'archive.sqlite')
    runner_class = {'serial': None, 'parallel-16': parallel_day.ParallelDay, 'parallel-16-mutant': mutant_runner_class()}[mode]
    runner = runner_class(ITEMS, folder / 'manifests', **WORKERS) if runner_class else None
    oracle = Oracle(delay_scale)
    judging, day_lines = {}, []
    original_judge_day = rounds.judge_day

    def timed_judge_day(conn, archive, cfg, day, *args, **kwargs):
        judging_started = time.perf_counter()
        try:
            return original_judge_day(conn, archive, cfg, day, *args, **kwargs)
        finally:
            judging[day] = (judging_started, time.perf_counter())

    def log(message):
        if message[:5] == '2026-':
            day_lines.append((message[:10], time.perf_counter(), message))

    rounds.judge_day = timed_judge_day
    failure = totals = None
    started = time.perf_counter()
    try:
        totals = replay.run(testdb_path=str(ITEMS), views_path=str(folder / 'views.sqlite'), archive=archive, cfg=cfg,
                            universe=uni, from_day=FIRST_DAY, until_day=LAST_DAY, transport=oracle, day_runner=runner, log=log)
    except Exception as error:      # recorded and judged by the checks, never a pass by itself
        failure = f'{type(error).__name__}: {str(error)[:300]}'
    finally:
        rounds.judge_day = original_judge_day
        archive.conn.close()
    finished = time.perf_counter()
    days, day_started = [], started
    for day, day_finished, line in day_lines:
        judging_started, judging_finished = judging[day]
        days.append({'day': day, 'extracted': int(line.split(' extracted ')[1].split()[0]), 'seconds': round(day_finished - day_started, 3),
                     'item_work_seconds': round(judging_started - day_started, 3),
                     'judging_seconds': round(judging_finished - judging_started, 3)})
        day_started = day_finished
    report = {'mode': mode, 'delay_scale': delay_scale, 'failure': failure, 'seconds': round(finished - started, 3),
              'totals': totals, 'days': days, 'oracle_calls': oracle.counts, 'peak_inflight': oracle.peak_inflight}
    if runner:
        counts = {}
        for event in runner.events:
            counts[event['event']] = counts.get(event['event'], 0) + 1
        report['runner_events'] = counts
        report['accepted_requests'] = sorted(accepted_requests(runner.events).values())
    (folder / 'result.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k not in ('days', 'accepted_requests', 'totals')}), flush=True)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--delay-scale', type=float, required=True, help='0 answers at once; 1 at recorded durations')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit('output exists; preserve it and name a new folder')
    output.mkdir(parents=True)
    protected = {path: parallel_day.digest(path) for path in (START_LEDGER, RECORDED_ARCHIVE, ITEMS)}
    cfg, uni = config.load(ROOT / 'poc/config/poc-v23.json'), universe.load(ROOT / 'poc/universe.json')
    reports = {mode: run_mode(output, mode, cfg, uni, args.delay_scale) for mode in ('serial', 'parallel-16', 'parallel-16-mutant')}
    serial_rows = logical_rows(output / 'serial' / 'views.sqlite')
    compared = {mode: [table for table, rows in logical_rows(output / mode / 'views.sqlite').items() if rows != serial_rows[table]]
                for mode in ('parallel-16', 'parallel-16-mutant')}
    serial_requests = extraction_requests(output / 'serial' / 'archive.sqlite')
    serial, parallel = reports['serial'], reports['parallel-16']
    checks = {
        'inputs_unchanged': {path: parallel_day.digest(path) for path in protected} == protected,
        'serial_and_parallel_completed': serial['failure'] is None and parallel['failure'] is None and len(serial['days']) == 15,
        'parallel_equals_serial': compared['parallel-16'] == [],
        'accepted_equals_serial_requests': parallel['accepted_requests'] == serial_requests,
        'mutant_detected': reports['parallel-16-mutant']['failure'] is not None or compared['parallel-16-mutant'] != [],
        'early_requests_changed_by_a_commit': parallel['runner_events'].get('stale', 0) > 0,
    }
    days = [{'day': s['day'], 'extracted': s['extracted'], 'serial_seconds': s['seconds'], 'parallel_seconds': p['seconds'],
             'speedup': round(s['seconds'] / p['seconds'], 2) if p['seconds'] else None,
             'item_work_speedup': round(s['item_work_seconds'] / p['item_work_seconds'], 2) if p['item_work_seconds'] else None}
            for s, p in zip(serial['days'], parallel['days'])]
    summary = {'delay_scale': args.delay_scale, 'passed': all(checks.values()), 'checks': checks,
               'rows_compared': sum(len(rows) for rows in serial_rows.values()), 'tables_compared': len(serial_rows),
               'mutant_tables_different': compared['parallel-16-mutant'], 'mutant_failure': reports['parallel-16-mutant']['failure'],
               'accepted_requests': len(parallel['accepted_requests']), 'runner_events': parallel['runner_events'],
               'total_seconds': {mode: report['seconds'] for mode, report in reports.items()},
               'total_speedup': round(serial['seconds'] / parallel['seconds'], 2) if parallel['seconds'] else None, 'days': days,
               'mode': 'deterministic oracle at scaled recorded durations; an estimate, not live latency'}
    (output / 'summary.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: v for k, v in summary.items() if k != 'days'}, indent=2))
    if not summary['passed']:
        raise SystemExit('multi-day check failed')


if __name__ == '__main__':
    main()
