"""A snapshot of a store, even while it is written (AGENTS §9's route; live-service/OPERATING-CONTRACT.md, row 7): SQLite's backup API,
taken out of WAL mode, integrity checked, published at a new path without replacing anything. Nothing is left on failure.

  python3 scripts/snapshot_store.py <store> <new destination>
"""
import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
from hivemind import live_lock  # noqa: E402


def main(arguments):
    if len(arguments) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        destination = live_lock.snapshot(arguments[0], arguments[1])
    except (OSError, RuntimeError, sqlite3.Error) as error:          # LockRefused is a RuntimeError
        print(f'snapshot refused: {error}', file=sys.stderr)
        return 1
    print(f'snapshot: {destination}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
