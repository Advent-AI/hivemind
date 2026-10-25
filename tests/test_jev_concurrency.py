"""D172: parallel Jev jobs retain serial decisions and exact archive identities."""
import copy
import concurrent.futures
import json
import threading

import pytest

from test_jev_matching import CFG, ITEM, ledger_with_view, piece
from hivemind import model
from hivemind.views import jev_matching, matching, store


def response(request, choice='different'):
    answers = {}
    for key, question in request['questions'].items():
        labels = list(question['criteria'])
        probabilities = {label: 0.05 for label in labels}
        probabilities[choice] = 0.9
        answers[key] = {'type': 'choice', 'choice': choice, 'confidence': 0.9, 'probabilities': probabilities}
    return {'answers': answers, 'usage': {'input_tokens': 1000, 'output_tokens': 0}}


def jobs(conn):
    first = piece('x1', 'First independent statement.', ['v1'])
    second = piece('x2', 'Second independent statement.', ['v1'])
    return [first, second], matching.Lists({}, {('x1', 'v1'): ['e1'], ('x2', 'v1'): ['e1']})


def test_independent_jobs_overlap_but_decisions_and_hashes_keep_input_order(tmp_path):
    """D172 ordered collection: completion order must not reorder the matching answer."""
    conn, _ = ledger_with_view(tmp_path)
    evidence, lists = jobs(conn)
    def answer(request):
        return response(request, 'same_statement' if 'First independent' in request['state'] else 'different')
    serial = jev_matching.decide(model.Archive(str(tmp_path / 'serial.sqlite')), CFG, conn, ITEM, [], copy.deepcopy(evidence), lists, [], transport=answer)
    barrier = threading.Barrier(2)
    def concurrent(request):
        barrier.wait(5)
        return answer(request)
    archive = model.Archive(str(tmp_path / 'parallel.sqlite'))
    parallel = jev_matching.decide(archive, CFG, conn, ITEM, [], copy.deepcopy(evidence), lists, [], transport=concurrent, workers=2)
    assert parallel.data == serial.data
    assert parallel.request_sha256 == serial.request_sha256
    assert [x['id'] for x in parallel.data['evidence']] == ['x1', 'x2']
    assert len(parallel.request_records) == 2
    for record in parallel.request_records:
        row = archive.conn.execute('select request_sha256,answer_json from model_calls where call_id=?', (record['call_id'],)).fetchone()
        assert row[0] == record['request_sha256']
        assert json.loads(row[1])


def test_identical_jobs_share_one_response_and_cost(tmp_path):
    """D172 duplicate-request row: two logical requests cannot disagree under one archive ID."""
    conn, _ = ledger_with_view(tmp_path)
    evidence, lists = jobs(conn)
    evidence[1] = dict(evidence[0], id='x2')  # IDs are not in Jev's state; these are byte-identical calls.
    calls = []
    lock = threading.Lock()
    second_started = threading.Event()
    def changing_provider(request):
        with lock:
            calls.append(request)
            index = len(calls)
        if index == 1:
            second_started.wait(0.5)  # Force overlapping cache misses if the shared-future rule is removed.
        else:
            second_started.set()
        return response(request, 'same_statement' if index == 1 else 'different')
    archive = model.Archive(str(tmp_path / 'shared.sqlite'))
    answer = jev_matching.decide(archive, CFG, conn, ITEM, [], evidence, lists, [], transport=changing_provider, workers=2)
    assert len(calls) == 1
    assert [d['outcome'] for d in answer.data['evidence']] == ['repeat', 'repeat']
    assert answer.request_records[0] == answer.request_records[1]
    assert answer.calls == 2  # Logical requests retain their original order and aggregate hash.
    assert answer.cost_usd == pytest.approx(0.000042)
    cached = jev_matching.decide(archive, CFG, conn, ITEM, [], evidence, lists, [], transport=changing_provider, workers=2)
    assert cached.data == answer.data and cached.cached and cached.cost_usd == 0
    assert len(calls) == 1


def test_partial_failure_drains_and_reuses_the_successful_request_on_retry(tmp_path):
    """D172 failed wave: successful calls stay archived but no partial decision is returned."""
    conn, _ = ledger_with_view(tmp_path)
    evidence, lists = jobs(conn)
    archive = model.Archive(str(tmp_path / 'partial.sqlite'))
    barrier = threading.Barrier(2)
    def failing(request):
        barrier.wait(5)
        if 'First independent' in request['state']:
            raise model.TransportError('one question failed')
        return response(request)
    with pytest.raises(model.TransportError, match='one question failed'):
        jev_matching.decide(archive, CFG, conn, ITEM, [], evidence, lists, [], transport=failing, workers=2)
    assert archive.totals()[0] == 1
    called = []
    def retry(request):
        assert 'First independent' in request['state']
        called.append(request)
        return response(request)
    answer = jev_matching.decide(archive, CFG, conn, ITEM, [], evidence, lists, [], transport=retry, workers=2)
    assert len(called) == 1 and len(answer.data['evidence']) == 2
    assert archive.totals()[0] == 2


def test_failure_stops_unsent_jobs_and_drains_only_running_work(tmp_path):
    """D172 queued-work row: a failure among two running jobs must not launch jobs 3–10."""
    conn, _ = ledger_with_view(tmp_path)
    evidence = [piece(f'x{i}', f'Independent part {i}.', ['v1']) for i in range(10)]
    lists = matching.Lists({}, {(e['id'], 'v1'): ['e1'] for e in evidence})
    archive = model.Archive(str(tmp_path / 'bounded.sqlite'))
    failed, release, unwanted = threading.Event(), threading.Event(), threading.Event()
    calls, lock = [], threading.Lock()
    def transport(request):
        with lock:
            calls.append(request['state'])
        if 'part 0.' in request['state']:
            assert release.wait(5)
            return response(request)
        if 'part 1.' in request['state']:
            failed.set()
            raise model.TransportError('stop the wave')
        unwanted.set()
        return response(request)
    def run():
        owned = store.open_read_only(str(tmp_path / 'views.sqlite'))
        try:
            return jev_matching.decide(archive, CFG, owned, ITEM, [], evidence, lists, [], transport=transport, workers=2)
        finally:
            owned.close()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as caller:
        future = caller.submit(run)
        try:
            assert failed.wait(5)
            assert not unwanted.wait(0.1)
        finally:
            release.set()
        with pytest.raises(model.TransportError, match='stop the wave'):
            future.result()
    assert len(calls) == 2
