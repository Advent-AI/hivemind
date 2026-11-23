"""Who writes a store, and how it is copied (docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md, row 7 and "Who
writes, and copies: slice 4b").

The writer and preflight take one operating-system lock (`flock`) named by the store file's device and inode, in one folder; the
operating system releases it when its process ends, a crash included. A store is opened only by its own path (a symlink is resolved;
a store with another hard link is refused, since SQLite finds a WAL store's side files by the opened path). The holder checks that the
path still names the locked file on both sides of an open and at each later check point; a path swapped away and back around an open
is not detected (the contract's operating precondition excludes it).

`snapshot` is AGENTS §9's route to read a store being written: SQLite's backup API, taken out of WAL mode, integrity checked, and
published without replacing anything.
"""
import fcntl
import os
import sqlite3
import tempfile

LOCK_FOLDER = os.path.expanduser('~/.hivemind-locks')


class LockRefused(RuntimeError):
    """The store is being written (its lock is held), its lock folder cannot be used, or its path is not its own."""


class PathChanged(RuntimeError):
    """The store's path, or its lock file's path, no longer names the file that was locked."""


def lock_folder():
    """The one lock folder, owner-only; refused (never skipped) when it cannot be created or written."""
    try:
        os.makedirs(LOCK_FOLDER, mode=0o700, exist_ok=True)
    except OSError as error:
        raise LockRefused(f'the lock folder {LOCK_FOLDER} cannot be created: {error}') from error
    if not os.access(LOCK_FOLDER, os.W_OK | os.X_OK):
        raise LockRefused(f'the lock folder {LOCK_FOLDER} cannot be written')
    return LOCK_FOLDER


def own_path(store_path):
    """(the store's real path, (device, inode)); a store with another hard link is refused."""
    real = os.path.realpath(store_path)
    status = os.stat(real)
    if status.st_nlink > 1:
        raise LockRefused(f'{real} has {status.st_nlink} hard links: a store is opened only by its own path')
    return real, (status.st_dev, status.st_ino)


class Held:
    """A held lock: the store's real path and identity, the lock file's path, descriptor and inode."""

    def __init__(self, real_path, identity, lock_path, descriptor):
        self.real_path, self.identity, self.lock_path, self.descriptor = real_path, identity, lock_path, descriptor
        self.lock_inode = os.fstat(descriptor).st_ino


def acquire(store_path):
    """The store's lock, without waiting: refused when another process holds it."""
    real, identity = own_path(store_path)
    lock_path = os.path.join(lock_folder(), f'{identity[0]}-{identity[1]}.writer.lock')
    descriptor = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        os.close(descriptor)
        raise LockRefused(f'{real} is being written (its lock is held): read a snapshot of it instead (scripts/snapshot_store.py)') from None
    held = Held(real, identity, lock_path, descriptor)
    try:
        verify(held)
    except BaseException:
        release(held)
        raise
    return held


def verify(held):
    """The store's path still names the locked file with no other hard link, and the lock file's path still names the locked lock
    file; otherwise `PathChanged`."""
    try:
        status = os.stat(held.real_path)
    except FileNotFoundError:
        raise PathChanged(f'{held.real_path} no longer exists') from None
    if os.path.realpath(held.real_path) != held.real_path or (status.st_dev, status.st_ino) != held.identity:
        raise PathChanged(f'{held.real_path} no longer names the locked store')
    if status.st_nlink > 1:
        raise PathChanged(f'{held.real_path} now has {status.st_nlink} hard links')
    try:
        lock_inode = os.stat(held.lock_path).st_ino
    except FileNotFoundError:
        lock_inode = None
    if lock_inode != held.lock_inode:
        raise PathChanged(f'the lock file {held.lock_path} was replaced')


def release(held):
    try:
        fcntl.flock(held.descriptor, fcntl.LOCK_UN)
    finally:
        os.close(held.descriptor)


def leave_wal_mode(connection):
    """The copy out of WAL mode, so a read-only reader can open it; refused unless the mode becomes rollback."""
    mode = connection.execute('pragma journal_mode=delete').fetchone()[0]
    if mode != 'delete':
        raise RuntimeError(f'the snapshot could not leave WAL mode (it is {mode!r})')


def snapshot(store_path, destination):
    """A consistent copy of a store, even while it is written: only to a new path (so never onto the store itself); made in a temporary
    file beside the destination, taken out of WAL mode, integrity checked, then published by a hard link that fails if the destination
    has appeared meanwhile. On any failure nothing created by this call is left. Returns the destination."""
    real, _ = own_path(store_path)
    destination = os.path.abspath(destination)
    if os.path.lexists(destination):
        raise FileExistsError(f'{destination} exists: a snapshot is written only to a new path')
    descriptor, temporary = tempfile.mkstemp(prefix='.snapshot-', suffix='.sqlite', dir=os.path.dirname(destination) or '.')
    os.close(descriptor)
    source = target = None
    try:
        try:
            source = sqlite3.connect(f'file:{real}?mode=ro', uri=True)
            target = sqlite3.connect(temporary)
            source.backup(target)
            leave_wal_mode(target)
            check = target.execute('pragma integrity_check').fetchone()[0]
            if check != 'ok':
                raise RuntimeError(f'the snapshot failed its integrity check: {check}')
        finally:
            for connection in (target, source):
                if connection is not None:
                    connection.close()
        os.link(temporary, destination)                      # fails if the destination appeared during the copy: nothing is replaced
        return destination
    finally:
        for leftover in (temporary, temporary + '-journal', temporary + '-wal', temporary + '-shm'):
            if os.path.exists(leftover):
                os.remove(leftover)
