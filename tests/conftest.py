"""Tests that read a stored ledger or archive under poc/data (not in Git) are skipped, with the missing path named, when that
data is absent: a fresh clone runs the suite without 40 errors that say nothing about the code (2026-10-28 cleanup). The tests
themselves are unchanged; on a machine with the data they run as before.

No test reads a credential (AGENTS §9): every test runs with the model and Jev key readers refusing, so a call that escapes its
fake transport fails the test instead of reaching a provider."""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
STORED_DATA = {
    'test_event_horizon': ['poc/data/keyed-2026-10-25/archive-T2.sqlite', 'poc/data/items-window-tags2-2026-10-24.sqlite'],
    'test_idea': ['poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite', 'poc/data/items-window.sqlite'],
    'test_search': ['poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite'],
    'test_service': ['poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite'],
    'test_ui_bundles': ['poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite', 'poc/data/items-window.sqlite'],
    'test_sequential_replay': ['poc/data/views-2026-10-25-v15-T2b-aborted-fresh-archive.sqlite'],
}


def pytest_collection_modifyitems(config, items):
    for item in items:
        needed = STORED_DATA.get(item.module.__name__, [])
        missing = [p for p in needed if not os.path.exists(os.path.join(ROOT, p))]
        if missing:
            item.add_marker(pytest.mark.skip(reason=f'stored data not present: {missing[0]}'))


@pytest.fixture(autouse=True)
def no_credentials(monkeypatch):
    from hivemind import jev, model

    def refuse(*arguments):          # pytest.fail raises a BaseException, which the pipeline's `except Exception` cannot record as an item failure
        pytest.fail('a test read a credential: a model or Jev call escaped its fake transport')
    monkeypatch.setattr(model, '_key', refuse)
    monkeypatch.setattr(jev, '_key', refuse)
