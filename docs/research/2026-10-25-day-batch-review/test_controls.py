"""Controls for the D170 snapshot and visibility measurements, using real records."""
import json
from pathlib import Path
import sys

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from audit import ROOT, connect, wave  # noqa: E402
from snapshot_proof import snapshot  # noqa: E402
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import extraction, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

CASE = 'edgar:NVDA:0001045810-26-000019:q4fy26cfocommentary.htm'
FOLDER = ROOT / 'poc/data/english-v23-jev-2026-10-25'


@pytest.fixture
def recorded_case():
    with connect(FOLDER / 'views.sqlite') as ledger, connect(ROOT / 'poc/data/items-window-tags2-2026-10-24.sqlite') as source:
        item = dict(source.execute('select * from items where input_id=?', (CASE,)).fetchone())
        item['object_identifiers'] = json.loads(item['object_identifiers'])
        seq = ledger.execute('select seq from handovers where input_id=?', (CASE,)).fetchone()[0]
        first = ledger.execute('select min(sequence_no) from processing_steps where publication_day=? and sequence_no>0', (item['publication_day'],)).fetchone()[0]
        yield ledger, item, seq, first


def test_historical_snapshot_preserves_predecessor_and_excludes_future(recorded_case):
    """A day-start snapshot cannot contain v2, but the recorded second item can."""
    ledger, item, seq, first = recorded_case
    prior, start = snapshot(ledger, seq), snapshot(ledger, first)
    try:
        assert store.view(prior, 'v2') is not None
        assert store.view(start, 'v2') is None
        assert prior.execute('select count(*) from views where created_seq>=?', (seq,)).fetchone()[0] == 0
        assert [r[0] for r in prior.execute('select view_id from views_fts order by rowid')] == [r[0] for r in prior.execute('select view_id from views order by rowid')]
    finally:
        prior.close(); start.close()


def test_complete_request_is_reproduced_before_comparing_day_start(recorded_case):
    """Measurement control: reproduce the actual request, including source and context."""
    ledger, item, seq, first = recorded_case
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    db = snapshot(ledger, seq)
    try:
        objects = [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
        built = extraction.build_prompt(item, item['text'], store.views_for_prompt(db, objects), uni, 'v10', store.groups_for_prompt(db, objects, item['title']))
        with connect(FOLDER / 'archive.sqlite') as archive:
            saved = next(json.loads(row[0]) for row in archive.execute("select request_json from model_calls where config_version='poc-v23' and purpose='extract'")
                         if f'[Item] id {CASE}, category ' in json.loads(row[0])['messages'][1]['content'])
        assert built == tuple(m['content'] for m in saved['messages'])
    finally:
        db.close()


def test_a_stored_answer_loses_evidence_when_the_prior_thesis_is_hidden(recorded_case):
    """Decisive real failure: narrowing to day-start IDs drops existing evidence."""
    ledger, item, seq, first = recorded_case
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    with connect(FOLDER / 'archive.sqlite') as archive:
        row = next(r for r in archive.execute("select request_json,answer_json from model_calls where config_version='poc-v23' and purpose='extract'")
                   if f'[Item] id {CASE}, category ' in json.loads(r[0])['messages'][1]['content'])
        raw = json.loads(row['answer_json'])
    prior, start = snapshot(ledger, seq), snapshot(ledger, first)
    try:
        ids = {r[0] for r in prior.execute('select view_id from views')}
        day_ids = {r[0] for r in start.execute('select view_id from views')}
        control = extraction.sift_with_groups(raw, item, item['text'], ids, uni, english=True)
        changed = extraction.sift_with_groups(raw, item, item['text'], day_ids, uni, english=True)
        assert len(control[0]) > len(changed[0])
        assert any('links to nothing shown' in reason for _, reason in changed[2])
    finally:
        prior.close(); start.close()


def test_scheduler_accounts_for_worker_limit_and_slowest_call():
    """Timing control: extra workers cannot shorten a single slow call."""
    assert wave([10, 10, 10], 1) == 30
    assert wave([10, 10, 10], 2) == 20
    assert wave([100, 1, 1], 3) == 100
    assert wave([], 3) == 0


def test_missing_measurement_input_is_not_created(tmp_path):
    """Missing-input precondition: never let SQLite invent an empty source."""
    path = tmp_path / 'missing.sqlite'
    with pytest.raises(ValueError, match='missing input'):
        with connect(path):
            pass
    assert not path.exists()
