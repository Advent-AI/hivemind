"""No test writes outside temporary folders (AGENTS §4): the writer lock's folder (live_lock, live-service/OPERATING-CONTRACT.md row 7)
is moved into one for the whole session, before any module-scoped replay runs."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'src'))


@pytest.fixture(autouse=True, scope='session')
def locks_in_a_temporary_folder(tmp_path_factory):
    from hivemind import live_lock
    saved = live_lock.LOCK_FOLDER
    live_lock.LOCK_FOLDER = str(tmp_path_factory.mktemp('locks'))
    yield
    live_lock.LOCK_FOLDER = saved
