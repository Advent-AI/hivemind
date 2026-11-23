"""One committed state per request while a writer commits (docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md,
row 2; proofs 3, 4 and 2e): the API's `Connections` and MCP's per-call `connections()` pin the ledger's state by BEGIN and a first read;
a writer's commits during a request are invisible to it and never blocked by it; a failure while opening leaves nothing open; the streamed
Idea route refuses a first-day store or a future date before any header; MCP's instructions name their start day while its tools read the
current one. Real stores in WAL mode on temporary paths, written through the store's own functions; no model call."""
import importlib.util
import json
import os
import sqlite3
import sys
import threading
import urllib.error
import urllib.request

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [os.path.join(ROOT, 'src'), os.path.join(ROOT, 'scripts')]
from hivemind import dispatch, search, service  # noqa: E402
from hivemind.views import store  # noqa: E402

RUNGS = [{'label': 'Yes', 'condition': 'It ships by 2027-01-31.'}, {'label': 'Ruled out', 'condition': 'It is cancelled.'},
         {'label': 'Still open', 'condition': 'Neither holds on 2027-01-31.'}]


def add_day(writer, day, seq, view_id):
    """One article's processing, one view opened under it, and the day completed, committed: what the loop writes for a day."""
    dispatch.mark(writer, {'input_id': f'gnews:{view_id}', 'publication_day': day}, seq, 'handed_over')
    store.create_view(writer, view_id=view_id, object_id='NVDA', object_kind='asset', kind='asset', looks_at=f'shipments {view_id}',
                      question=f'Will product {view_id} ship by 2027-01-31?', due_day='2027-01-31', year='2027', rungs=RUNGS, seq=seq,
                      input_id=f'gnews:{view_id}', created_at=f'{day}T00:00:00Z')
    store.complete_day(writer, day, seq, day)
    writer.commit()


def a_wal_store(path, *, first_day=False):
    writer = store.open_db(str(path))
    writer.execute('pragma journal_mode=wal')
    if first_day:
        dispatch.mark(writer, {'input_id': 'gnews:first', 'publication_day': '2026-10-01'}, 1, 'handed_over')
        writer.commit()
    else:
        add_day(writer, '2026-10-01', 1, 'v1')
    return writer


def view_ids(conn):
    return [v['view_id'] for v in service.views(conn, None, None, include_closed=True)]


@pytest.fixture
def api(tmp_path, monkeypatch):
    import hivemind_api
    monkeypatch.setitem(hivemind_api.PATHS, 'views', str(tmp_path / 'views.sqlite'))
    monkeypatch.setitem(hivemind_api.PATHS, 'index', str(tmp_path / 'index.sqlite'))
    monkeypatch.setitem(hivemind_api.PATHS, 'items', str(tmp_path / 'no-items.sqlite'))
    monkeypatch.setitem(hivemind_api.PATHS, 'archive', str(tmp_path / 'archive.sqlite'))
    return hivemind_api


def test_an_api_request_keeps_its_state_while_the_writer_commits_a_day(tmp_path, api):
    writer = a_wal_store(tmp_path / 'views.sqlite')
    with api.Connections(read_only=True) as db:
        assert view_ids(db.ledger) == ['v1'] and service.resolve_bound(db.ledger, None) == '2026-10-01'
        add_day(writer, '2026-10-02', 2, 'v2')                                     # commits while the request is open: not blocked
        assert view_ids(db.ledger) == ['v1'] and service.resolve_bound(db.ledger, None) == '2026-10-01'
    with api.Connections(read_only=True) as db:
        assert view_ids(db.ledger) == ['v1', 'v2'] and service.resolve_bound(db.ledger, None) == '2026-10-02'


def test_a_failure_while_opening_leaves_no_connection_open(tmp_path, api, monkeypatch):
    a_wal_store(tmp_path / 'views.sqlite')
    opened = []
    real_open = service.open_ledger
    monkeypatch.setattr(service, 'open_ledger', lambda path: opened.append(real_open(path)) or opened[-1])
    monkeypatch.setattr(api.search, 'open_index', lambda path: (_ for _ in ()).throw(OSError('index unavailable')))
    with pytest.raises(OSError, match='index unavailable'):
        with api.Connections():
            pass
    with pytest.raises(sqlite3.ProgrammingError):                                   # closed
        opened[0].execute('select 1')


def serve(api):
    server = api.http.server.ThreadingHTTPServer(('127.0.0.1', 0), api.Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def post_idea(server, body):
    request = urllib.request.Request(f'http://127.0.0.1:{server.server_address[1]}/ideas', data=json.dumps(body).encode(),
                                     headers={'Content-Type': 'application/json', 'Accept': 'application/x-ndjson'}, method='POST')
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, response.headers.get('Content-Type'), response.read().decode()
    except urllib.error.HTTPError as error:
        return error.code, error.headers.get('Content-Type'), error.read().decode()


@pytest.mark.parametrize('first_day, body, status, payload', [
    (True, {'text': 'an idea'}, 503, {'error': "the store's first day has not completed"}),
    (False, {'text': 'an idea', 'as_of': '2026-10-05'}, 409, {'error': 'day not completed', 'requested': '2026-10-05', 'last_completed_day': '2026-10-01'}),
])
def test_the_streamed_idea_route_refuses_before_any_header(tmp_path, api, first_day, body, status, payload):
    a_wal_store(tmp_path / 'views.sqlite', first_day=first_day)
    server = serve(api)
    try:
        got_status, content_type, text = post_idea(server, body)
    finally:
        server.shutdown()
    assert (got_status, content_type.split(';')[0], json.loads(text)) == (status, 'application/json', payload)


def load_mcp(tmp_path, monkeypatch):
    """The MCP server's module as its entry point builds it, on the test store, lexical (no network)."""
    monkeypatch.setattr(sys, 'argv', ['hivemind_mcp.py', '--views', str(tmp_path / 'views.sqlite'), '--index', str(tmp_path / 'index.sqlite'),
                                      '--items', str(tmp_path / 'no-items.sqlite'), '--lexical'])
    spec = importlib.util.spec_from_file_location(f'hivemind_mcp_{tmp_path.name}', os.path.join(ROOT, 'scripts', 'hivemind_mcp.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_mcp_tools_read_the_current_day_while_its_instructions_keep_their_start_day(tmp_path, monkeypatch):
    writer = a_wal_store(tmp_path / 'views.sqlite')
    mcp = load_mcp(tmp_path, monkeypatch)
    assert mcp.OBJECTS.startswith('Objects as of 2026-10-01, when this server started')
    assert [v['view_id'] for v in mcp.views()] == ['v1']
    add_day(writer, '2026-10-02', 2, 'v2')
    assert [v['view_id'] for v in mcp.views()] == ['v1', 'v2']
    assert mcp.OBJECTS.startswith('Objects as of 2026-10-01')


def test_overlapping_mcp_calls_each_keep_their_own_state_and_index_connection(tmp_path, monkeypatch):
    writer = a_wal_store(tmp_path / 'views.sqlite')
    mcp = load_mcp(tmp_path, monkeypatch)
    with mcp.connections() as (first, _, first_index):
        assert view_ids(first) == ['v1']
        add_day(writer, '2026-10-02', 2, 'v2')
        with mcp.connections() as (second, _, second_index):
            assert view_ids(second) == ['v1', 'v2'] and view_ids(first) == ['v1']
            assert first_index is not second_index
    with pytest.raises(sqlite3.ProgrammingError):                                   # both closed when their calls ended
        first.execute('select 1')

    fake = lambda texts, model: ([[1.0, 0.0] for _ in texts], 1)
    errors, start = [], threading.Barrier(2)

    def a_search_call(text):
        """What a search tool call does with its own connections, in its own thread: read the ledger, write the query cache."""
        try:
            with mcp.connections() as (ledger, _, index):
                start.wait(timeout=5)
                view_ids(ledger)
                search.query_vector(index, text, fake)
        except Exception as error:                                               # noqa: BLE001 - any error is the finding
            errors.append(repr(error))
    threads = [threading.Thread(target=a_search_call, args=(text,)) for text in ('one', 'two')]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert errors == []
    cached = sqlite3.connect(str(tmp_path / 'index.sqlite')).execute('select count(*) from query_vectors').fetchone()[0]
    assert cached == 2


def test_mcp_on_a_first_day_store_says_so_and_every_tool_refuses(tmp_path, monkeypatch):
    a_wal_store(tmp_path / 'views.sqlite', first_day=True)
    mcp = load_mcp(tmp_path, monkeypatch)
    assert mcp.OBJECTS == 'No day of this ledger has completed yet; every tool refuses until one has.'
    for tool in (lambda: mcp.views(), lambda: mcp.thesis_library(), lambda: mcp.changes('2026-09-01'), lambda: mcp.search('ship')):
        with pytest.raises(service.FirstDayNotCompleted):
            tool()


def test_an_mcp_opening_failure_leaves_no_connection_open(tmp_path, monkeypatch):
    a_wal_store(tmp_path / 'views.sqlite')
    mcp = load_mcp(tmp_path, monkeypatch)
    opened = []
    real_open = service.open_ledger
    monkeypatch.setattr(mcp.service, 'open_ledger', lambda path: opened.append(real_open(path)) or opened[-1])
    monkeypatch.setattr(mcp.search_module, 'open_index', lambda path: (_ for _ in ()).throw(OSError('index unavailable')))
    with pytest.raises(OSError, match='index unavailable'):
        mcp.views()
    with pytest.raises(sqlite3.ProgrammingError):
        opened[0].execute('select 1')
