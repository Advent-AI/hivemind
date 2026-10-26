"""Replay the test database through the pipeline day by day with no look-ahead.

For every calendar day from from_day to until_day: route each item published that day (dispatch), run its round
(extraction → matching → writing), then the day's one re-judging round over the views whose reading changed (D63),
then pull mode for that day. A guard refuses an item whose
publication day is after the replay day. The views database refuses to run a day at or before the last day it
completed (no backdating). After day0's pull the views database is copied to <views>.day0.sqlite for the agent
layer. Every day prints one line and the archive's cumulative cost."""
import datetime
import shutil
import time

from . import dispatch, pull, testdb
from .views import round as round_module, store


class StaleHandoverError(RuntimeError):
    """A saved parallel extraction cannot establish that it read its predecessors."""


def refuse_unfinished_parallel(conn):
    """D159: preserve old handovers, but never resume a day-start read as a sequential read."""
    pending = conn.execute("""select p.input_id, p.reason from processing_steps p
        where p.step='extracted' and p.result='ok'
        and p.id=(select max(q.id) from processing_steps q
                  where q.input_id=p.input_id and q.step='extracted' and q.result='ok')
        and not exists (select 1 from processing_steps q
                        where q.input_id=p.input_id and q.step='handed_over' and q.result='ok')
        order by p.sequence_no""")
    ids = [row['input_id'] for row in pending if row['reason'].endswith(' (parallel)')]
    if ids:
        raise StaleHandoverError('unfinished day-start extractions; keep this ledger and replay into a new one: ' + ', '.join(ids))


class LookAheadError(RuntimeError):
    pass


class BackdatingError(RuntimeError):
    pass


def calendar_days(from_day, until_day):
    day = datetime.date.fromisoformat(from_day)
    last = datetime.date.fromisoformat(until_day)
    while day <= last:
        yield day.isoformat()
        day += datetime.timedelta(days=1)


def run(*, testdb_path, views_path, archive, cfg, universe, from_day, until_day, day0=None, spend_cap_usd=None,
        transport=None, log=print, only_objects=None, max_items_per_day=None, day_runner=None):
    items_db = testdb.open_db(testdb_path)
    conn = store.open_db(views_path)
    refuse_unfinished_parallel(conn)
    last_done = store.last_completed_day(conn)
    start = from_day
    if last_done and from_day <= last_done:
        next_day = (datetime.date.fromisoformat(last_done) + datetime.timedelta(days=1)).isoformat()
        if next_day > until_day:
            raise BackdatingError(f'views database already completed {last_done}; nothing to run before it')
        log(f'resuming after the last completed day {last_done}')
        start = next_day
    last_written = conn.execute('select max(publication_day) from processing_steps where sequence_no > 0').fetchone()[0]
    if last_written and start < last_written:
        raise BackdatingError(f'views database already holds rounds of {last_written}; a replay cannot start before it (D31)')
    totals = {'items': 0, 'extracted': 0, 'skipped': 0, 'merged': 0, 'not_processed': 0, 'returned': 0, 'failed': 0,
              'evidence': 0, 'new_views': 0, 'judged': 0, 'changed': 0, 'closed': 0}
    calls_before, cost_before, *_ = archive.totals()
    for day in calendar_days(start, until_day):
        day_stats = {k: 0 for k in totals}
        day_cost_before = archive.totals()[1]
        processed = 0
        to_run = []
        for item in testdb.feed(items_db, day, day):
            if item['publication_day'] > day:
                raise LookAheadError(f'{item["input_id"]} is dated {item["publication_day"]}, after replay day {day}')
            if only_objects and not any(o['value'] in only_objects for o in item['object_identifiers']):
                continue
            if max_items_per_day and processed >= max_items_per_day:
                break
            day_stats['items'] += 1
            route = dispatch.route(conn, item, universe)
            if route.kind != 'extract':
                day_stats[route.kind] += 1
                if route.kind == 'skipped':
                    processed += 1      # written by an earlier run of this day: a restart keeps the day's item limit
                if route.kind == 'merged':
                    dispatch.mark(conn, item, 0, 'merged', 'ok', route.reason)
                    conn.commit()
                continue
            processed += 1
            to_run.append((item, route))
        results = (day_runner(conn, archive, cfg, universe, to_run, day=day, transport=transport, log=log) if day_runner else
                   (round_module.run(conn, archive, cfg, universe, item, route.sequence_no, resume_from=route.resume_from, transport=transport, log=log)
                    for item, route in to_run))
        finished = 0
        try:
            for index, result in enumerate(results):
                if index >= len(to_run) or result.input_id != to_run[index][0]['input_id']:
                    raise RuntimeError('day runner returned results out of input order')
                finished += 1
                day_stats['extracted'] += 1
                day_stats['evidence'] += result.evidence
                day_stats['new_views'] += result.new_views
                day_stats['judged'] += result.judged
                day_stats['changed'] += result.changed
                if result.failed:
                    day_stats['failed'] += 1
                    log(f'  ! {result.input_id[:60]}: {result.failed}')
                    raise RuntimeError(f'item failed; day {day} remains resumable: {result.failed}')
                if spend_cap_usd is not None and archive.totals()[1] - cost_before > spend_cap_usd:
                    raise RuntimeError(f'spend cap {spend_cap_usd} reached on {day}')
        finally:
            if hasattr(results, 'close'):
                results.close()
        if finished != len(to_run):
            raise RuntimeError('day runner did not complete every routed item')
        seq = store.next_sequence(conn) - 1
        judged = round_module.judge_day(conn, archive, cfg, day, seq, transport=transport, log=log)
        day_stats['judged'] += judged.judged
        day_stats['changed'] += judged.changed
        if judged.failed:
            day_stats['failed'] += 1
            log(f'  ! day judging: {judged.failed}')
            raise RuntimeError(f'judging failed; day {day} remains resumable: {judged.failed}')
        closed = pull.end_of_day(conn, day, seq)
        day_stats['closed'] = len(closed)
        store.complete_day(conn, day, seq, time.strftime('%Y-%m-%dT%H:%M:%S'))
        conn.commit()
        for key in totals:
            totals[key] += day_stats[key]
        calls, cost, _, _ = archive.totals()
        day_cost = cost - day_cost_before  # Includes discarded speculative calls and repaired refusals.
        open_count = len(store.open_views(conn))
        log(f'{day} | items {day_stats["items"]:3d} extracted {day_stats["extracted"]:3d} merged {day_stats["merged"]:2d} skipped {day_stats["not_processed"]:2d} '
            f'failed {day_stats["failed"]:2d} | evidence {day_stats["evidence"]:3d} new views {day_stats["new_views"]:2d} judged {day_stats["judged"]:3d} '
            f'changed {day_stats["changed"]:3d} closed {len(closed)} | open views {open_count} | day ${day_cost:.2f} total ${cost - cost_before:.2f} calls {calls - calls_before}')
        if day0 and day == day0:
            conn.commit()
            shutil.copy(views_path, views_path + '.day0.sqlite')
            log(f'day 0 snapshot written: {views_path}.day0.sqlite')
    return totals
