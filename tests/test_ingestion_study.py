"""The ingestion study's baseline, shared dispatch limit and failure boundaries."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sqlite3
import sys
import threading

import pytest

from hivemind import config, model, replay
from hivemind.views import judging, store
from test_concurrency import responses
from test_sequential_replay import setup_run
from test_keyed_views import candidate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'poc'))
sys.path.insert(0, str(ROOT / 'docs/research/2026-10-25-day-batch-review'))
from snapshot_proof import snapshot
from concurrency_study.budget import BudgetError, GuardedTransport
from concurrency_study.ingestion import StudyTransport, study_day
from concurrency_study.runner import DayRunner


def openai_request(name):
    return {'model': 'gpt-6-luna', 'messages': [{'role': 'user', 'content': name}],
            'response_format': {'json_schema': {'schema': {'type': 'object'}}}, 'max_completion_tokens': 8000}


def response():
    return {'choices': [{'message': {'content': '{}'}}], 'usage': {'prompt_tokens': 1000, 'completion_tokens': 10}}


def test_projected_baseline_excludes_unordered_future_records(tmp_path):
    """Baseline table: sequence-zero future audit data is not historical knowledge."""
    source = store.open_db(tmp_path / 'source.sqlite')
    for ident, seq, day in [('past', 1, '2026-07-23'), ('future', 0, '2026-07-24')]:
        store.mark_step(source, ident, seq, 'merged', 'ok', '', day, day + 'T12:00:00')
    store.pool(source, 'suggested_theme', 'unplaced', {'input_id': None}, 0)
    control = snapshot(source, 21)
    assert control.execute('select count(*) from processing_steps').fetchone()[0] == 2
    projected = snapshot(source, 21, exclude_unordered=True)
    assert projected.execute('select input_id from processing_steps').fetchall()[0][0] == 'past'
    assert projected.execute('select count(*) from processing_steps').fetchone()[0] == 1
    assert projected.execute('select count(*) from review_pool_entries').fetchone()[0] == 0


def test_shared_transport_bounds_requests_across_stages(tmp_path):
    """Shared limit: three callers across providers cannot dispatch more than two together."""
    entered, release = threading.Event(), threading.Event()
    lock = threading.Lock()
    active = maximum = count = 0
    def prepare(provider, request):
        def send():
            nonlocal active, maximum, count
            with lock:
                active += 1; count += 1; maximum = max(maximum, active)
                if count == 2:
                    entered.set()
            try:
                assert release.wait(5)
                if provider == 'jev':
                    return {'answers': {'q': {'type': 'noul', 'noul': 0.5}}, 'usage': {'input_tokens': 1000, 'output_tokens': 10}}
                return response()
            finally:
                with lock:
                    active -= 1
        return send
    transport = StudyTransport(GuardedTransport(tmp_path / 'budget.sqlite', prepare))
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(transport, 'openai', openai_request('extract')),
                   pool.submit(transport, 'openai', openai_request('judge')),
                   pool.submit(transport, {'model': 'jev-1.14.0', 'state': '', 'questions': {'q': {'type': 'noul'}}})]
        try:
            assert entered.wait(5)
            assert active == 2
        finally:
            release.set()
        for future in futures:
            future.result()
    assert maximum == 2 and count == 3


def test_judging_schema_failure_stops_waiting_requests_before_drain(tmp_path):
    """Judging failure row: malformed answer closes admission within the actual day judge pool."""
    second_started = threading.Event()
    first_reply_ready = threading.Event()
    lock = threading.Lock()
    calls = []
    transport = None
    def prepare(provider, request):
        def send():
            with lock:
                number = len(calls); calls.append(number)
                if number == 1:
                    second_started.set()
            if number == 0:
                assert second_started.wait(5)
                first_reply_ready.set()
            elif number == 1:
                assert first_reply_ready.wait(5)
            return response()  # JSON is valid; required judgement fields are absent.
        return send
    transport = StudyTransport(GuardedTransport(tmp_path / 'budget.sqlite', prepare))
    conn = store.open_db(tmp_path / 'views.sqlite')
    c = candidate('c1')
    for n in range(4):
        vid, eid = f'v{n+1}', f'e{n+1}'
        store.create_view(conn, view_id=vid, object_id='NVDA', object_kind='asset', kind='asset', looks_at=c['looks_at'],
                          question=f'Will scenario {n+1} occur?', due_day='2027-12-31', year='2027', rungs=c['rungs'],
                          seq=1, input_id='seed', created_at='2026-07-23T12:00:00')
        store.add_evidence(conn, evidence_id=eid, quote='The company expects production shipments in 2027.', one_line='Production expected in 2027.',
                           speaker='NVIDIA', original_who='NVIDIA', original_day='2026-07-23', tier='party_statement', event_time='', seq=1, input_id='seed')
        store.add_source(conn, eid, 'seed', 'T6', '2026-07-23', '', 1)
        store.link(conn, eid, vid, 1)
    conn.commit()
    cfg = config.load(ROOT / 'poc/config/poc-v23.json')
    with pytest.raises((BudgetError, model.SchemaError)):
        judging.round_of_judgements(model.Archive(tmp_path / 'archive.sqlite'), cfg, conn,
                                    ['v1', 'v2', 'v3', 'v4'], 2, {'input_id': 'day:2026-07-24', 'publication_day': '2026-07-24'}, transport=transport)
    assert transport.stopped.is_set()
    assert len(calls) == 2
    assert conn.execute('select count(*) from judgements').fetchone()[0] == 0


def test_failed_item_closes_study_before_later_handover(tmp_path):
    """Item failure row: the wrapper closes admission before normal generator cleanup."""
    args = setup_run(tmp_path)
    conn = store.open_db(args['views_path'])
    conn.execute("create trigger fail_write before insert on views begin select raise(abort,'test storage failure'); end")
    conn.commit(); conn.close()
    send, _ = responses(reverse=True)
    def prepare(provider, request):
        def complete():
            result = send(provider, request)
            result['usage'] = {'prompt_tokens': 1000, 'completion_tokens': 100}
            return result
        return complete
    transport = StudyTransport(GuardedTransport(tmp_path / 'budget.sqlite', prepare))
    runner = DayRunner(Path(args['testdb_path']), tmp_path / 'manifests', jev_workers=1)
    stopped_at_failed_yield = []
    wrapped = study_day(runner, transport)
    def observe(*a, **kw):
        for result in wrapped(*a, **kw):
            if result.failed:
                stopped_at_failed_yield.append(transport.stopped.is_set())
            yield result
    with pytest.raises(RuntimeError, match='test storage failure'):
        replay.run(**args, transport=transport, day_runner=observe)
    assert transport.stopped.is_set()
    assert stopped_at_failed_yield == [True]
    with sqlite3.connect(args['views_path']) as db:
        assert db.execute('select count(*) from handovers').fetchone()[0] == 1
        assert db.execute('select count(*) from days_completed').fetchone()[0] == 0
