"""Row 1's reader rules (docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md, "Slice 5"; council rounds 143 and
144): a reader that cannot open the store, or cannot begin and pin its read, fails loudly with the store's path (`service.open_pinned`,
`StoreUnreadable`) through the API, its streamed route and MCP; and a busy read waits within the reader's explicit busy timeout
(SQLite's busy handler; no application-level retry). The busy case is held by a connection in exclusive locking mode, a stand-in for
SQLite's rare WAL busy cases, which cannot be timed in a test."""
import json
import os
import sqlite3
import sys
import threading
import time
import urllib.error
import urllib.request

import pytest

from hivemind import service
from hivemind.views import store

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from test_live_reads import a_wal_store, load_mcp, post_idea, serve  # noqa: E402


@pytest.fixture
def api(tmp_path, monkeypatch):
    import hivemind_api
    for name, file in (('views', 'views.sqlite'), ('index', 'index.sqlite'), ('items', 'no-items.sqlite'), ('archive', 'archive.sqlite')):
        monkeypatch.setitem(hivemind_api.PATHS, name, str(tmp_path / file))
    return hivemind_api


def make_unreadable(folder):
    """A WAL store whose side files are absent, in a directory its reader cannot write: a read-only reader cannot create the `-shm`."""
    path = folder / 'views.sqlite'
    with open(path, 'rb') as header:
        assert header.read(20)[18:20] == b'\x02\x02'                          # the file is in WAL mode
    for side in ('-wal', '-shm'):
        if os.path.exists(f'{path}{side}'):
            os.remove(f'{path}{side}')
    folder.chmod(0o500)
    return path


@pytest.fixture
def unreadable(tmp_path):
    folder = tmp_path / 'store'
    folder.mkdir()
    writer = a_wal_store(folder / 'views.sqlite')
    writer.execute('pragma wal_checkpoint(TRUNCATE)')
    writer.close()
    yield folder
    folder.chmod(0o700)


def test_a_store_that_cannot_be_opened_is_refused_loudly_with_its_path(unreadable):
    path = make_unreadable(unreadable)
    with pytest.raises(service.StoreUnreadable) as refused:
        service.open_pinned(str(path))
    assert str(refused.value).startswith(f'{path}: ') and 'unable to open database file' in str(refused.value)


def test_the_api_answers_500_with_the_path_on_its_plain_and_streamed_routes(tmp_path, unreadable, api, monkeypatch):
    path = make_unreadable(unreadable)
    monkeypatch.setitem(api.PATHS, 'views', str(path))
    server = serve(api)
    try:
        with pytest.raises(urllib.error.HTTPError) as plain:
            urllib.request.urlopen(f'http://127.0.0.1:{server.server_address[1]}/days', timeout=10)
        status, content_type, text = post_idea(server, {'text': 'an idea'})
    finally:
        server.shutdown()
    assert plain.value.code == 500 and json.loads(plain.value.read())['error'].startswith(f'{path}: ')
    assert (status, content_type.split(';')[0]) == (500, 'application/json') and json.loads(text)['error'].startswith(f'{path}: ')


def test_mcp_refuses_at_start_and_per_tool_with_the_path(tmp_path, monkeypatch):
    writer = a_wal_store(tmp_path / 'views.sqlite')
    mcp = load_mcp(tmp_path, monkeypatch)                                     # started while the store is readable
    writer.execute('pragma wal_checkpoint(TRUNCATE)')
    writer.close()
    real = tmp_path / 'views.sqlite'
    try:
        make_unreadable(tmp_path)
        with pytest.raises(service.StoreUnreadable, match=str(real)):
            mcp.views()
        with pytest.raises(service.StoreUnreadable, match=str(real)):
            load_mcp(tmp_path, monkeypatch)
    finally:
        tmp_path.chmod(0o700)


def held_exclusively(path, seconds):
    """A connection in exclusive locking mode that has written, so no other connection can read, closed after `seconds`."""
    holder = sqlite3.connect(str(path), isolation_level=None, check_same_thread=False)
    assert holder.execute('pragma locking_mode=exclusive').fetchone()[0] == 'exclusive'
    holder.execute('begin immediate')
    holder.execute("insert into days_completed(day, seq, at) values ('2026-10-02', 2, '2026-10-02T00:00:00Z')")
    holder.execute('commit')
    release = threading.Timer(seconds, holder.close)
    release.start()
    return release


def test_a_busy_read_waits_within_the_timeout_and_then_reads(tmp_path):
    a_wal_store(tmp_path / 'views.sqlite').close()
    held_exclusively(tmp_path / 'views.sqlite', 0.5)
    started = time.monotonic()
    conn = service.open_pinned(str(tmp_path / 'views.sqlite'))
    waited = time.monotonic() - started
    assert 0.4 <= waited < store.READ_BUSY_TIMEOUT_SECONDS                   # it waited for the holder, then read
    assert service.resolve_bound(conn, None) == '2026-10-02'
    conn.close()


def test_a_read_held_past_the_timeout_fails_loudly_with_the_path(tmp_path, monkeypatch):
    a_wal_store(tmp_path / 'views.sqlite').close()
    monkeypatch.setattr(store, 'READ_BUSY_TIMEOUT_SECONDS', 0.3)
    release = held_exclusively(tmp_path / 'views.sqlite', 1.5)
    started = time.monotonic()
    with pytest.raises(service.StoreUnreadable) as refused:
        service.open_pinned(str(tmp_path / 'views.sqlite'))
    waited = time.monotonic() - started
    release.join()
    assert 0.25 <= waited < 1.4 and str(refused.value) == f"{tmp_path / 'views.sqlite'}: database is locked"
