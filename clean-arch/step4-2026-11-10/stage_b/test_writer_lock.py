"""The writer's lock (docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md, row 7 and "Who writes, and copies:
slice 4b"): taken before the first write, checked before each day, released after its connection is closed on every exit, released
by the operating system when the writer's process is killed; and a snapshot taken beside the running writer. Through `replay`, the
real launcher (`run_stage_b.send`), preflight and `scripts/snapshot_store.py`, on the stored draw u1 with a fake judge."""
import importlib.util
import os
import signal
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(HERE.parents[1] / 'e2e-2026-11-09'), str(ROOT / 'src')]
import budget  # noqa: E402
import ladder_adapter  # noqa: E402
import run_stage_b  # noqa: E402
from test_ladder_adapter import fake_judge, no_credentials, refusing_judge  # noqa: E402,F401
from hivemind import live_lock, service  # noqa: E402
from hivemind.views import judging, store  # noqa: E402

spec = importlib.util.spec_from_file_location('preflight', ROOT / 'scripts' / 'preflight.py')
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)
SNAPSHOT = ROOT / 'scripts' / 'snapshot_store.py'


def watch_the_writer(monkeypatch):
    """What the writer opened, and whether its connection was closed when its lock was released."""
    seen = {'connections': [], 'closed at release': []}
    real_open, real_release = store.open_db, live_lock.release

    def open_db(path):
        conn = real_open(path)
        seen['connections'].append(conn)
        return conn

    def release(held):
        seen['closed at release'].append(all(closed(conn) for conn in seen['connections']))
        return real_release(held)
    monkeypatch.setattr(store, 'open_db', open_db)
    monkeypatch.setattr(live_lock, 'release', release)
    return seen


def closed(conn):
    try:
        conn.execute('select 1')
        return False
    except sqlite3.ProgrammingError:
        return True


def lock_free(path):
    live_lock.release(live_lock.acquire(path))
    return True


def interrupt_on_the_second_day(monkeypatch):
    real, days = ladder_adapter.LadderAdapter.close_and_complete, []

    def close(self, day):
        if len(days) == 1:
            raise KeyboardInterrupt('interrupted')
        days.append(day)
        return real(self, day)
    monkeypatch.setattr(ladder_adapter.LadderAdapter, 'close_and_complete', close)


def low_space_on_the_third_day(monkeypatch):
    checked = []
    monkeypatch.setattr(ladder_adapter, 'free_bytes', lambda folder: checked.append(1) or (0 if len(checked) >= 3 else 10 ** 15))


EXITS = {
    'the end': (None, {}, lambda monkeypatch: None),
    'a stop before a day': (ladder_adapter.WriterStopped, {}, low_space_on_the_third_day),
    'a refused judgement': (judging.JudgementRefused, {'transport': refusing_judge}, lambda monkeypatch: None),
    'the spending cap': (budget.OverBudget, {'cap_usd': 0.0001}, lambda monkeypatch: None),
    'an interrupt': (KeyboardInterrupt, {}, interrupt_on_the_second_day),
}


@pytest.mark.parametrize('exit_kind', list(EXITS))
def test_every_exit_closes_the_writers_connection_before_releasing_its_lock(tmp_path, monkeypatch, exit_kind):
    raised, arguments, arrange = EXITS[exit_kind]
    arrange(monkeypatch)
    seen = watch_the_writer(monkeypatch)
    arguments = {'transport': fake_judge, 'cap_usd': 5.0, **arguments}
    if raised is None:
        ladder_adapter.replay('u1', tmp_path / 'out', **arguments)
    else:
        with pytest.raises(raised):
            ladder_adapter.replay('u1', tmp_path / 'out', **arguments)
    assert seen['closed at release'] == [True] and len(seen['connections']) == 1
    assert lock_free(tmp_path / 'out' / 'views.sqlite')
    with sqlite3.connect(f'file:{tmp_path / "out" / "views.sqlite"}?mode=ro', uri=True) as conn:
        assert conn.execute('pragma journal_mode').fetchone()[0] == 'delete'       # no WAL-mode store left behind on any exit


@pytest.mark.parametrize('failing', ['the schema', 'the check after the open'])
def test_a_failure_while_opening_closes_what_was_opened_and_releases_the_lock(tmp_path, monkeypatch, failing):
    seen = watch_the_writer(monkeypatch)
    if failing == 'the schema':
        monkeypatch.setattr(store, 'open_db', lambda path: (_ for _ in ()).throw(sqlite3.OperationalError('disk I/O error (test)')))
        expected = sqlite3.OperationalError
    else:
        real_verify, calls = live_lock.verify, []

        def verify(held):                     # the first call is acquire's own; the second is the check after `store.open_db`
            calls.append(1)
            if len(calls) == 2:
                raise live_lock.PathChanged('moved (test)')
            return real_verify(held)
        monkeypatch.setattr(live_lock, 'verify', verify)
        expected = live_lock.PathChanged
    with pytest.raises(expected):
        ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    assert seen['closed at release'] == [True]
    assert all(closed(conn) for conn in seen['connections'])
    assert len(seen['connections']) == (0 if failing == 'the schema' else 1)
    monkeypatch.undo()
    assert lock_free(tmp_path / 'out' / 'views.sqlite')


def test_the_writers_path_replaced_between_its_creation_and_its_lock_is_refused(tmp_path, monkeypatch):
    real_acquire = live_lock.acquire

    def replaced_first(path):
        (tmp_path / 'other.sqlite').write_bytes(b'')
        os.replace(tmp_path / 'other.sqlite', path)
        return real_acquire(path)
    monkeypatch.setattr(live_lock, 'acquire', replaced_first)
    with pytest.raises(live_lock.PathChanged, match='between its creation and its lock'):
        ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    monkeypatch.setattr(live_lock, 'acquire', real_acquire)
    assert lock_free(tmp_path / 'out' / 'views.sqlite')


def test_a_start_race_lost_to_preflight_refuses_the_writer_before_it_writes(tmp_path, monkeypatch):
    real_acquire, holder = live_lock.acquire, {}

    def preflight_first(path):
        holder['held'] = real_acquire(path)
        return real_acquire(path)
    monkeypatch.setattr(live_lock, 'acquire', preflight_first)
    with pytest.raises(live_lock.LockRefused, match='being written'):
        ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    assert os.path.getsize(tmp_path / 'out' / 'views.sqlite') == 0             # nothing written
    live_lock.release(holder['held'])


def test_an_unusable_lock_folder_refuses_the_writer_before_it_writes(tmp_path, monkeypatch):
    parent = tmp_path / 'locked-parent'
    parent.mkdir()
    parent.chmod(0o500)
    monkeypatch.setattr(live_lock, 'LOCK_FOLDER', str(parent / 'locks'))
    try:
        with pytest.raises(live_lock.LockRefused, match='cannot be created'):
            ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    finally:
        parent.chmod(0o700)
    assert os.path.getsize(tmp_path / 'out' / 'views.sqlite') == 0


@pytest.mark.parametrize('replaced, reason', [('the lock file', 'was replaced'), ('the store', 'no longer exists')])
def test_a_path_changed_during_the_run_stops_the_writer_at_the_next_day_through_the_launcher(tmp_path, monkeypatch, replaced, reason):
    real, days = ladder_adapter.LadderAdapter.close_and_complete, []

    def change_after_the_first_day(self, day):
        closed_today = real(self, day)
        days.append(day)
        if len(days) == 1:
            if replaced == 'the lock file':
                os.remove(self.lock.lock_path)
                Path(self.lock.lock_path).write_text('')
            else:
                os.rename(self.lock.real_path, self.lock.real_path + '.moved')
        return closed_today
    monkeypatch.setattr(ladder_adapter.LadderAdapter, 'close_and_complete', change_after_the_first_day)
    record = run_stage_b.send(tmp_path, transport=fake_judge, sleep=lambda seconds: None)
    assert record['u1']['state'] == 'incomplete' and not (tmp_path / 'draw-u1-redo').exists()
    assert record['stopped'].startswith('u1 incomplete: ') and reason in record['stopped'] and f'before {days[0]}' not in record['stopped'], record['u1']['attempts'][0].get('traceback')
    assert len(days) == 1


KILLED_WRITER = '''
import sqlite3, sys, time
from pathlib import Path
here, out, marker, locks, reference = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], sys.argv[5]
sys.path[:0] = [str(here), str(here.parents[0] / 'e2e-2026-11-09'), str(here.parents[2] / 'src')]
import ladder_adapter
from hivemind import jev, live_lock, model
live_lock.LOCK_FOLDER = locks
def refuse(*arguments):
    raise SystemExit('a credential was read')
model._key = jev._key = refuse
from test_ladder_adapter import fake_judge
real, done = ladder_adapter.LadderAdapter.close_and_complete, []
def close(self, day):
    if len(done) == 2:                       # the third day's articles are committed; its completion never comes
        marker.write_text(day)
        time.sleep(600)
    result = real(self, day)
    done.append(day)
    if len(done) == 2:                       # the reference: the store right after its second day, before any write of the third
        target = sqlite3.connect(reference)
        self.conn.backup(target)
        target.execute('pragma journal_mode=delete')
        target.close()
    return result
ladder_adapter.LadderAdapter.close_and_complete = close
ladder_adapter.replay('u1', out, transport=fake_judge, cap_usd=5.0)
'''


def test_a_killed_writer_process_leaves_its_lock_released_and_preflights_copy_answers_as_its_last_completed_day(tmp_path, monkeypatch):
    """Row 7 and proofs 7′ and 8′ (OPERATING-CONTRACT.md, "Slice 5"): the operating system releases the lock; the crashed store and
    preflight's copy each give the same outcome as an independent reference taken right after the second day, before any third-day
    write, on `tests/bound_cases.calls` (8 service functions, 5 bundle functions and lexical search; no Idea function, no route) at
    the omitted bound, the first and the last completed day, and a future day; and snapshots of the crashed store through a symlink
    and through its own path are equal table by table, row by row."""
    (tmp_path / 'writer.py').write_text(KILLED_WRITER)
    out, marker, reference = tmp_path / 'out', tmp_path / 'third-day', tmp_path / 'reference.sqlite'
    writer = subprocess.Popen([sys.executable, str(tmp_path / 'writer.py'), str(HERE), str(out), str(marker), live_lock.LOCK_FOLDER,
                               str(reference)])
    deadline = time.monotonic() + 120
    while not marker.exists() and writer.poll() is None and time.monotonic() < deadline:
        time.sleep(0.1)
    assert marker.exists(), 'the writer never reached its third day'
    with pytest.raises(live_lock.LockRefused):                                 # held while it runs
        live_lock.acquire(out / 'views.sqlite')
    os.kill(writer.pid, signal.SIGKILL)
    writer.wait()
    [copy] = preflight.store_copies([str(out / 'views.sqlite')])
    with service.open_ledger(copy) as conn:
        days = [r[0] for r in conn.execute('select day from days_completed order by id')]
        assert len(days) == 2 and service.resolve_bound(conn, None) == days[-1]
        assert conn.execute('select count(*) from processing_steps where publication_day = ?', (marker.read_text(),)).fetchone()[0] > 0
    with service.open_ledger(str(reference)) as conn:                         # the reference holds nothing of the third day
        assert conn.execute('select count(*) from processing_steps where publication_day = ?', (marker.read_text(),)).fetchone()[0] == 0
    sys.path.insert(0, str(HERE.parents[2] / 'tests'))
    import bound_cases
    judged = 0
    for state, past in (('crash: the first completed day', days[0]), ('crash: the last completed day', days[-1])):
        monkeypatch.setitem(bound_cases.STATES, state, {'past': past, 'future': '2099-01-01', 'since': days[0]})
        outcomes = {}
        for label, path in (('reference', reference), ('crashed store', out / 'views.sqlite'), ('preflight copy', copy)):
            with service.open_ledger(str(path)) as conn:
                outcomes[label] = [(name, kind, bound_cases.outcome(call)) for name, kind, call in bound_cases.calls(conn, state)]
        assert outcomes['crashed store'] == outcomes['reference'] and outcomes['preflight copy'] == outcomes['reference'], state
        assert sum(1 for _, _, result in outcomes['reference'] if result[0] == 'ok') >= 20  # mostly answers, not only refusals
        judged += len(outcomes['reference'])
    assert judged == 2 * (14 * 3 + 2)
    os.symlink(out / 'views.sqlite', tmp_path / 'alias.sqlite')
    snapshots = {}
    for label, source in (('own path', out / 'views.sqlite'), ('symlink', tmp_path / 'alias.sqlite')):
        destination = tmp_path / f"snapshot-{label.replace(' ', '-')}.sqlite"
        finished = subprocess.run([sys.executable, str(SNAPSHOT), str(source), str(destination)], capture_output=True, text=True)
        assert finished.returncode == 0, finished.stderr
        with sqlite3.connect(f'file:{destination}?mode=ro', uri=True) as conn:
            tables = [r[0] for r in conn.execute("select name from sqlite_master where type = 'table' order by name")]
            snapshots[label] = {table: sorted(conn.execute(f'select * from "{table}"').fetchall(), key=repr) for table in tables}  # some tables have no rowid
    assert len(snapshots['own path']) > 10 and snapshots['symlink'] == snapshots['own path']
    assert any(rows for rows in snapshots['own path'].values())


def test_a_snapshot_taken_beside_the_writer_holding_uncheckpointed_commits_is_whole_and_read_only_readable(tmp_path, monkeypatch):
    real, days, taken = ladder_adapter.LadderAdapter.close_and_complete, [], {}

    def snapshot_before_completing_the_second_day(self, day):
        if len(days) == 1:
            taken['run'] = subprocess.run([sys.executable, str(SNAPSHOT), self.lock.real_path, str(tmp_path / 'snap.sqlite')],
                                          capture_output=True, text=True)
            taken['day'] = day
        days.append(day)
        return real(self, day)
    monkeypatch.setattr(ladder_adapter.LadderAdapter, 'close_and_complete', snapshot_before_completing_the_second_day)
    monkeypatch.setattr(ladder_adapter, 'truncate_checkpoint', lambda conn: 'done')   # the second day's commits stay in the -wal
    ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    assert taken['run'].returncode == 0, taken['run'].stderr
    with sqlite3.connect(f'file:{tmp_path / "snap.sqlite"}?mode=ro', uri=True) as conn:
        assert conn.execute('pragma journal_mode').fetchone()[0] == 'delete'
        assert conn.execute('pragma integrity_check').fetchone()[0] == 'ok'
        assert [r[0] for r in conn.execute('select day from days_completed')] == days[:1]
        assert conn.execute('select count(*) from processing_steps where publication_day = ?', (taken['day'],)).fetchone()[0] > 0


def test_a_failure_while_leaving_wal_mode_still_closes_the_connection_then_releases_the_lock(tmp_path, monkeypatch):
    seen = watch_the_writer(monkeypatch)
    monkeypatch.setattr(ladder_adapter, 'leave_wal', lambda conn: (_ for _ in ()).throw(RuntimeError('leaving WAL failed (test)')))
    with pytest.raises(RuntimeError, match='leaving WAL failed'):
        ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    assert seen['closed at release'] == [True]
    monkeypatch.undo()
    assert lock_free(tmp_path / 'out' / 'views.sqlite')


class FailsToClose:
    """The writer's connection, except that closing it fails."""

    def __init__(self, real):
        self.real = real

    def __getattr__(self, name):
        return getattr(self.real, name)

    def close(self):
        raise sqlite3.OperationalError('closing failed (test)')


def test_a_connection_that_fails_to_close_keeps_its_lock_until_the_process_ends(tmp_path, monkeypatch):
    real, runner = ladder_adapter.LadderAdapter.close_and_complete, {}

    def wrap_the_connection(self, day):
        closed_today = real(self, day)
        if not isinstance(self.conn, FailsToClose):
            self.conn, runner['self'] = FailsToClose(self.conn), self
        return closed_today
    monkeypatch.setattr(ladder_adapter.LadderAdapter, 'close_and_complete', wrap_the_connection)
    with pytest.raises(sqlite3.OperationalError, match='closing failed'):
        ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    writer = runner['self']
    assert writer.lock is not None and not closed(writer.conn.real)            # the connection is open, so its lock is kept
    with pytest.raises(live_lock.LockRefused, match='being written'):
        live_lock.acquire(tmp_path / 'out' / 'views.sqlite')
    writer.conn.real.close()
    live_lock.release(writer.lock)


class FailsOn:
    """The writer's connection, except that a statement containing `fragment` fails with SQLite's disk I/O error."""

    def __init__(self, real, fragment):
        self.real, self.fragment = real, fragment

    def __getattr__(self, name):
        return getattr(self.real, name)

    def execute(self, sql, *arguments):
        if self.fragment in sql:
            raise sqlite3.OperationalError('disk I/O error')
        return self.real.execute(sql, *arguments)


def fail_from_the_first_day_on(monkeypatch, fragment):
    real, days = ladder_adapter.LadderAdapter.close_and_complete, []

    def wrap(self, day):
        closed_today = real(self, day)
        days.append(day)
        if not isinstance(self.conn, FailsOn):
            self.conn = FailsOn(self.conn, fragment)
        return closed_today
    monkeypatch.setattr(ladder_adapter.LadderAdapter, 'close_and_complete', wrap)
    return days


def test_a_checkpoint_failing_for_another_reason_than_a_reader_stops_the_writer_with_that_reason(tmp_path, monkeypatch):
    days = fail_from_the_first_day_on(monkeypatch, 'wal_checkpoint')
    record = run_stage_b.send(tmp_path, transport=fake_judge, sleep=lambda seconds: None)
    assert record['stopped'] == f'u1 incomplete: the truncating checkpoint after {days[0]} failed: disk I/O error'
    assert record['u1']['state'] == 'incomplete' and len(days) == 1 and 'reader' not in record['stopped']
    assert lock_free(tmp_path / 'draw-u1' / 'views.sqlite')


def test_leaving_wal_failing_for_another_reason_than_a_reader_is_recorded_as_that_failure(tmp_path, monkeypatch):
    fail_from_the_first_day_on(monkeypatch, 'journal_mode=delete')
    runner = ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    assert runner.counts['store journal mode at the end'] == 'wal'
    assert runner.counts['stopped in order'] == 'WAL kept: leaving WAL failed: disk I/O error'
    assert lock_free(tmp_path / 'out' / 'views.sqlite')
