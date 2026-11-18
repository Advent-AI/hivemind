"""A pytest plugin for one exercise ($0; council round 32): the package's own test suite run with the separated reading installed
(`separated_edges.install`), so that every test that writes or reads a dependency goes through it. No package or test file changes.

  PYTHONPATH=<this folder> python3 -m pytest -q -p seam_plugin
"""
import separated_edges


def pytest_configure(config):
    separated_edges.install()


def pytest_unconfigure(config):
    separated_edges.restore()


# SEAM_RESTATE_FIXTURES=1: a fixture row written by hand with the seed label at an article's sequence on a question that no seed file
# created is restated as what the matching writer writes (a direction label of its vocabulary), so that the test's path (a resumed
# round recovering its queue through a dependency) can be exercised for a `reads` edge. Only the label of such a row is changed.
import os

from hivemind.views import store as _store

if os.environ.get('SEAM_RESTATE_FIXTURES') == '1':
    _insert = _store.insert

    def insert(conn, table, **values):
        if table == 'dependencies' and values.get('direction') == 'last_end' and values.get('seq', 0) > 0:
            seeded = conn.execute("select 1 from views where view_id = ? and lower(substr(created_from_input, 1, 5)) = 'seed:'", (values['view_id'],)).fetchone()
            if not seeded:
                values['direction'] = 'first_is_bullish'
        return _insert(conn, table, **values)

    _store.insert = insert
