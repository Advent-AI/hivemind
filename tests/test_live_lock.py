"""Who writes a store, and how it is copied (docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md, row 7 and "Who
writes, and copies: slice 4b"): the lock's aliases, the path checks, the lock folder, preflight's locked copy and the snapshot entry
point (`scripts/snapshot_store.py`), on a copy of the sealed run's real store put in WAL mode. The writer's side is proven in
`clean-arch/step4-2026-11-10/stage_b/test_writer_lock.py`."""
import fcntl
import importlib.util
import os
import sqlite3
import subprocess
import sys

import pytest

from hivemind import live_lock, service

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FINISHED = os.path.join(ROOT, 'poc', 'data', 'sealed-2026-10-24-run3-through-0815', 'views.sqlite')
SNAPSHOT = os.path.join(ROOT, 'scripts', 'snapshot_store.py')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


preflight = load('preflight', os.path.join(ROOT, 'scripts', 'preflight.py'))
snapshot_store = load('snapshot_store', SNAPSHOT)


WRITERS = []


@pytest.fixture(autouse=True)
def close_writers():
    yield
    while WRITERS:
        WRITERS.pop().close()


def wal_store(folder, name='views.sqlite'):
    """The sealed run's store, copied by the backup API and put in WAL mode, with a connection left open on it as a running writer
    keeps one (its side files exist, as they do while a writer runs or after it crashed)."""
    path = os.path.join(folder, name)
    source, target = service.open_ledger(FINISHED), sqlite3.connect(path)
    source.backup(target)
    assert target.execute('pragma journal_mode=wal').fetchone()[0] == 'wal'
    target.execute('select count(*) from views').fetchone()                  # the side files exist once the connection reads
    source.close()
    WRITERS.append(target)
    return path


def last_day(path):
    with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as conn:
        return conn.execute('select max(day) from days_completed').fetchone()[0]


def lock_is_free(lock_path):
    descriptor = os.open(lock_path, os.O_RDWR)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except BlockingIOError:
        return False
    finally:
        os.close(descriptor)


def test_the_store_and_a_symlink_to_it_meet_one_lock_and_a_hard_linked_store_is_refused_by_the_lock_preflight_and_the_snapshot(tmp_path):
    path = wal_store(tmp_path)
    os.symlink(path, tmp_path / 'alias.sqlite')
    held = live_lock.acquire(path)
    with pytest.raises(live_lock.LockRefused, match='being written'):
        live_lock.acquire(tmp_path / 'alias.sqlite')
    live_lock.release(held)
    os.link(path, tmp_path / 'second-name.sqlite')
    with pytest.raises(live_lock.LockRefused, match='2 hard links'):
        live_lock.acquire(path)
    with pytest.raises(live_lock.LockRefused, match='2 hard links'):
        preflight.store_copies([path])
    assert snapshot_store.main([path, str(tmp_path / 'snap.sqlite')]) == 1 and not (tmp_path / 'snap.sqlite').exists()


def test_preflight_refuses_a_store_being_written_and_names_the_snapshot_route(tmp_path):
    path = wal_store(tmp_path)
    writer = live_lock.acquire(path)
    with pytest.raises(live_lock.LockRefused, match='snapshot_store.py'):
        preflight.store_copies([path])
    live_lock.release(writer)


def test_preflight_copies_a_wal_store_under_the_lock_into_a_copy_a_read_only_reader_opens_and_releases_the_lock(tmp_path):
    path = wal_store(tmp_path)
    [copy] = preflight.store_copies([path])
    with sqlite3.connect(f'file:{copy}?mode=ro', uri=True) as conn:
        assert conn.execute('pragma journal_mode').fetchone()[0] == 'delete'
    assert last_day(copy) == last_day(path) == '2026-08-15'
    live_lock.release(live_lock.acquire(path))                               # free at once


def test_a_store_path_replaced_after_its_stat_is_refused_and_the_lock_released(tmp_path, monkeypatch):
    path, other = wal_store(tmp_path), wal_store(tmp_path, 'other.sqlite')
    real_folder = live_lock.lock_folder
    seen = {}

    def replace_then_folder():
        seen['identity'] = live_lock.own_path(path)[1]
        os.replace(other, path)                                               # after acquire's stat, before its lock
        return real_folder()
    monkeypatch.setattr(live_lock, 'lock_folder', replace_then_folder)
    with pytest.raises(live_lock.PathChanged, match='no longer names the locked store'):
        live_lock.acquire(path)
    device, inode = seen['identity']
    assert lock_is_free(os.path.join(real_folder(), f'{device}-{inode}.writer.lock'))


def test_a_store_path_replaced_during_preflights_copy_discards_the_copy_and_releases_the_lock(tmp_path, monkeypatch):
    path, other = wal_store(tmp_path), wal_store(tmp_path, 'other.sqlite')
    real = live_lock.leave_wal_mode

    def replace_during_the_copy(connection):
        os.replace(other, path)
        return real(connection)
    monkeypatch.setattr(live_lock, 'leave_wal_mode', replace_during_the_copy)
    scratch = tmp_path / 'scratch.sqlite'
    with pytest.raises(live_lock.PathChanged):
        preflight.locked_copy(path, str(scratch))
    assert not scratch.exists()
    live_lock.release(live_lock.acquire(path))                               # the new file's lock is free too


@pytest.mark.parametrize('unusable', ['cannot be created', 'cannot be written'])
def test_an_unusable_lock_folder_refuses_the_lock_and_preflight(tmp_path, monkeypatch, unusable):
    path = wal_store(tmp_path)
    parent = tmp_path / 'locked-parent'
    parent.mkdir()
    folder = parent / 'locks'
    if unusable == 'cannot be written':
        folder.mkdir()
        folder.chmod(0o500)
    else:
        parent.chmod(0o500)
    monkeypatch.setattr(live_lock, 'LOCK_FOLDER', str(folder))
    try:
        with pytest.raises(live_lock.LockRefused, match=unusable):
            live_lock.acquire(path)
        with pytest.raises(live_lock.LockRefused, match=unusable):
            preflight.store_copies([path])
    finally:
        parent.chmod(0o700)
        if folder.exists():
            folder.chmod(0o700)


def test_the_snapshot_entry_point_writes_a_new_read_only_readable_copy_out_of_wal_mode(tmp_path):
    path = wal_store(tmp_path)
    finished = subprocess.run([sys.executable, SNAPSHOT, path, str(tmp_path / 'snap.sqlite')], capture_output=True, text=True)
    assert finished.returncode == 0, finished.stderr
    with sqlite3.connect(f'file:{tmp_path / "snap.sqlite"}?mode=ro', uri=True) as conn:
        assert conn.execute('pragma journal_mode').fetchone()[0] == 'delete'
        assert conn.execute('pragma integrity_check').fetchone()[0] == 'ok'
    assert last_day(tmp_path / 'snap.sqlite') == '2026-08-15'


def leftovers(folder):
    return sorted(name for name in os.listdir(folder) if name.startswith('.snapshot-'))


def test_the_snapshot_never_writes_over_an_existing_path_or_the_store_itself(tmp_path):
    path = wal_store(tmp_path)
    (tmp_path / 'taken.sqlite').write_text('someone else')
    before = open(path, 'rb').read()
    assert snapshot_store.main([path, str(tmp_path / 'taken.sqlite')]) == 1
    assert snapshot_store.main([path, path]) == 1
    assert (tmp_path / 'taken.sqlite').read_text() == 'someone else' and open(path, 'rb').read() == before
    assert leftovers(tmp_path) == []


def test_a_failed_conversion_leaves_nothing_at_the_destination(tmp_path, monkeypatch):
    path = wal_store(tmp_path)

    def fail(connection):
        raise RuntimeError('the snapshot could not leave WAL mode (test)')
    monkeypatch.setattr(live_lock, 'leave_wal_mode', fail)
    assert snapshot_store.main([path, str(tmp_path / 'snap.sqlite')]) == 1
    assert not (tmp_path / 'snap.sqlite').exists() and leftovers(tmp_path) == []


def test_a_destination_created_just_before_publication_stays_untouched_and_the_temporary_copy_is_removed(tmp_path, monkeypatch):
    path = wal_store(tmp_path)
    real = live_lock.leave_wal_mode

    def someone_takes_the_destination(connection):
        real(connection)
        (tmp_path / 'snap.sqlite').write_text('someone else')
    monkeypatch.setattr(live_lock, 'leave_wal_mode', someone_takes_the_destination)
    assert snapshot_store.main([path, str(tmp_path / 'snap.sqlite')]) == 1
    assert (tmp_path / 'snap.sqlite').read_text() == 'someone else' and leftovers(tmp_path) == []


def test_preflights_entry_point_hands_its_store_checks_only_its_locked_copies(tmp_path, monkeypatch):
    """Parts C and E read preflight's locked copy, never the store (a writer could start between them); the parts' own checks are
    covered by tests/test_preflight_replay.py, so here they only record what they were given."""
    path = wal_store(tmp_path)
    given = {}
    for name in ('part_a', 'part_b', 'part_d'):
        monkeypatch.setattr(preflight, name, lambda *arguments: 1)
    monkeypatch.setattr(preflight, 'part_c', lambda archive, paths, uni: given.setdefault('c', list(paths)) and 1)
    monkeypatch.setattr(preflight, 'part_e', lambda paths: given.setdefault('e', list(paths)))
    from hivemind import model
    model.Archive(str(tmp_path / 'archive.sqlite'))
    monkeypatch.setattr(sys, 'argv', ['preflight.py', '--archive', str(tmp_path / 'archive.sqlite'), '--items', str(tmp_path / 'items.sqlite'),
                                      '--views', path])
    preflight.main()
    assert given['c'] == given['e'] and path not in given['c'] and len(given['c']) == 1
    with sqlite3.connect(f'file:{given["c"][0]}?mode=ro', uri=True) as conn:
        assert conn.execute('pragma journal_mode').fetchone()[0] == 'delete'


def test_the_api_and_mcp_refuse_a_hard_linked_store_at_start_and_on_each_request_naming_the_reason(tmp_path, monkeypatch):
    """Row 7: every entry point opens a store by its own path; a store with another hard link is refused, by the API at start and per
    request (500, the reason named) and by MCP at start and per tool call."""
    import json as json_module
    import urllib.error
    import urllib.request
    sys.path.insert(0, os.path.join(ROOT, 'scripts'))
    import hivemind_api
    from test_live_reads import a_wal_store, load_mcp, serve
    for name, file in (('views', 'views.sqlite'), ('index', 'index.sqlite'), ('items', 'no-items.sqlite'), ('archive', 'archive.sqlite')):
        monkeypatch.setitem(hivemind_api.PATHS, name, str(tmp_path / file))
    WRITERS.append(a_wal_store(tmp_path / 'views.sqlite'))
    mcp = load_mcp(tmp_path, monkeypatch)                                     # started before the second name exists
    os.link(tmp_path / 'views.sqlite', tmp_path / 'second-name.sqlite')
    with pytest.raises(live_lock.LockRefused, match='2 hard links'):
        hivemind_api.index_at_start()
    server = serve(hivemind_api)
    try:
        with pytest.raises(urllib.error.HTTPError) as refused:
            urllib.request.urlopen(f'http://127.0.0.1:{server.server_address[1]}/days', timeout=10)
    finally:
        server.shutdown()
    assert refused.value.code == 500 and '2 hard links' in json_module.loads(refused.value.read())['error']
    with pytest.raises(live_lock.LockRefused, match='2 hard links'):
        mcp.views()
    with pytest.raises(live_lock.LockRefused, match='2 hard links'):
        load_mcp(tmp_path, monkeypatch)


def test_a_snapshot_whose_target_fails_to_open_closes_its_source_and_leaves_nothing(tmp_path, monkeypatch):
    path = wal_store(tmp_path)
    real_connect, opened = sqlite3.connect, []

    def connect(*arguments, **keywords):
        if opened:
            raise sqlite3.OperationalError('the target cannot be opened (test)')
        opened.append(real_connect(*arguments, **keywords))
        return opened[-1]
    monkeypatch.setattr(live_lock.sqlite3, 'connect', connect)
    assert snapshot_store.main([path, str(tmp_path / 'snap.sqlite')]) == 1
    monkeypatch.undo()
    with pytest.raises(sqlite3.ProgrammingError):
        opened[0].execute('select 1')
    assert not (tmp_path / 'snap.sqlite').exists() and leftovers(tmp_path) == []
