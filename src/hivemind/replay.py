"""Replay the test database through the pipeline day by day with no look-ahead.

For every calendar day from from_day to until_day: route each item published that day (dispatch), run its round
(extraction → matching → writing), then the day's one re-judging round over the views whose reading changed (D63),
then pull mode for that day. A guard refuses an item whose
publication day is after the replay day. The views database refuses to run a day at or before the last day it
completed (no backdating). After day0's pull the views database is copied to <views>.day0.sqlite for the agent
layer. Every day prints one line and the archive's cumulative cost."""
import concurrent.futures
import datetime
import json
import os
import shutil
import time

from . import dispatch, extraction, pull, testdb
from .views import round as round_module, store

EXTRACTION_WORKERS = 8


def pre_extract(conn, archive, cfg, universe, items_and_routes, transport, log):
    """Run the day's extractions concurrently (model calls that read only the item and the views open at the start
    of the day) and store each handover; the rounds then run in sequence order and resume from 'matched'. A candidate
    that an earlier item of the same day just opened is caught by matching (归入), so the end state is the one
    sequential processing gives (D31: a parallel read that changed is judged again by the matcher)."""
    # the views database connection stays in this thread: the shown views are read here, once per object set
    snapshot = {}
    shown_for = {}
    for item, route in items_and_routes:
        objects = [o['value'] for o in item.get('object_identifiers') or [] if universe.has(o['value'])]
        key = tuple(sorted(objects))
        if key not in snapshot:
            snapshot[key] = store.views_for_prompt(conn, objects)
        shown_for[item['input_id']] = snapshot[key]

    def work(item, route):
        return item, route, extraction.extract(archive, cfg, item, item['text'], shown_for[item['input_id']], universe, transport=transport)

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=EXTRACTION_WORKERS) as pool_:
        futures = [pool_.submit(work, item, route) for item, route in items_and_routes]
        for future in concurrent.futures.as_completed(futures):
            try:
                item, route, handover = future.result()
                results[item['input_id']] = handover
            except Exception as error:
                log('  ! pre-extraction failed:', repr(error)[:200])
    for item, route in items_and_routes:
        handover = results.get(item['input_id'])
        if handover is None:
            continue
        store.insert(conn, 'handovers', input_id=item['input_id'], seq=route.sequence_no,
                     handover_json=json.dumps({'evidence': handover.evidence, 'candidates': handover.candidates, 'dropped': handover.dropped}, ensure_ascii=False))
        dispatch.mark(conn, item, route.sequence_no, 'extracted', 'ok', f'{len(handover.evidence)} evidence, {len(handover.candidates)} candidates, {len(handover.dropped)} dropped (parallel)')
    conn.commit()
    return results


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
        transport=None, log=print, only_objects=None, max_items_per_day=None):
    items_db = testdb.open_db(testdb_path)
    conn = store.open_db(views_path)
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
        day_cost = 0.0
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
                if route.kind == 'merged':
                    dispatch.mark(conn, item, 0, 'merged', 'ok', route.reason)
                    conn.commit()
                continue
            processed += 1
            to_run.append((item, route))
        fresh = [(item, route) for item, route in to_run if not route.resume_from]
        if len(fresh) > 1:
            extracted = pre_extract(conn, archive, cfg, universe, fresh, transport, log)
            to_run = [(item, dispatch.Route('extract', route.sequence_no, 'matched' if item['input_id'] in extracted else None, route.reason))
                      for item, route in to_run]
        for item, route in to_run:
            result = round_module.run(conn, archive, cfg, universe, item, route.sequence_no, resume_from=route.resume_from, transport=transport, log=log)
            day_stats['extracted'] += 1
            day_stats['evidence'] += result.evidence
            day_stats['new_views'] += result.new_views
            day_stats['judged'] += result.judged
            day_stats['changed'] += result.changed
            day_cost += result.cost
            if result.failed:
                day_stats['failed'] += 1
                log(f'  ! {item["input_id"][:60]}: {result.failed}')
            if spend_cap_usd is not None and archive.totals()[1] - cost_before > spend_cap_usd:
                raise RuntimeError(f'spend cap {spend_cap_usd} reached on {day}')
        seq = store.next_sequence(conn) - 1
        judged = round_module.judge_day(conn, archive, cfg, day, seq, transport=transport, log=log)
        day_stats['judged'] += judged.judged
        day_stats['changed'] += judged.changed
        day_cost += judged.cost
        if judged.failed:
            day_stats['failed'] += 1
            log(f'  ! day judging: {judged.failed}')
        closed = pull.end_of_day(conn, day, seq)
        day_stats['closed'] = len(closed)
        store.complete_day(conn, day, seq, time.strftime('%Y-%m-%dT%H:%M:%S'))
        conn.commit()
        for key in totals:
            totals[key] += day_stats[key]
        calls, cost, _, _ = archive.totals()
        open_count = len(store.open_views(conn))
        log(f'{day} | items {day_stats["items"]:3d} extracted {day_stats["extracted"]:3d} merged {day_stats["merged"]:2d} skipped {day_stats["not_processed"]:2d} '
            f'failed {day_stats["failed"]:2d} | evidence {day_stats["evidence"]:3d} new views {day_stats["new_views"]:2d} judged {day_stats["judged"]:3d} '
            f'changed {day_stats["changed"]:3d} closed {len(closed)} | open views {open_count} | day ${day_cost:.2f} total ${cost - cost_before:.2f} calls {calls - calls_before}')
        if day0 and day == day0:
            conn.commit()
            shutil.copy(views_path, views_path + '.day0.sqlite')
            log(f'day 0 snapshot written: {views_path}.day0.sqlite')
    return totals
