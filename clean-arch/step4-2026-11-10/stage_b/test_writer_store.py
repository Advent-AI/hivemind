"""The writer's store mode, stops and end (docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md, "The writer's start,
stops and end"; rows 1, 5 and 6; proofs 1, 5, 6 and 8d), on isolated test stores through `replay` and the real launcher
(`run_stage_b.send`) with the stored draw u1 and a fake judge. No writer lock yet (slice 4b): nothing here makes a live run safe."""
import sqlite3
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(HERE.parents[1] / 'e2e-2026-11-09'), str(ROOT / 'src')]
import ladder_adapter  # noqa: E402
import run_stage_b  # noqa: E402
from test_ladder_adapter import fake_judge, no_credentials  # noqa: E402,F401
from hivemind import bundle, search, service  # noqa: E402
from hivemind.views import store  # noqa: E402


def completed_days(path):
    return [r[0] for r in sqlite3.connect(f'file:{path}?mode=ro', uri=True).execute('select day from days_completed order by id')]


def test_the_store_is_in_wal_mode_with_its_size_limit_on_the_writers_connection_from_its_first_write(tmp_path, monkeypatch):
    seen = []
    real = ladder_adapter.LadderAdapter.close_and_complete

    def after_first_day(self, day):
        closed = real(self, day)
        if not seen:
            seen.append((self.conn.execute('pragma journal_mode').fetchone()[0], self.conn.execute('pragma journal_size_limit').fetchone()[0]))
        return closed
    monkeypatch.setattr(ladder_adapter.LadderAdapter, 'close_and_complete', after_first_day)
    conn, held = ladder_adapter.open_wal_store(tmp_path / 'fresh.sqlite')
    assert (conn.execute('pragma journal_mode').fetchone()[0], conn.execute('pragma journal_size_limit').fetchone()[0]) == ('wal', ladder_adapter.STORE_SIZE_LIMIT)
    with pytest.raises(FileExistsError):                                      # created exclusively: never an existing store
        ladder_adapter.open_wal_store(tmp_path / 'fresh.sqlite')
    conn.close()
    ladder_adapter.live_lock.release(held)
    ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    assert seen == [('wal', ladder_adapter.STORE_SIZE_LIMIT)]


def test_production_stores_keep_the_rollback_journal(tmp_path):
    """Proof 1's other half: production's stores are opened by `store.open_db`, untouched, and a new one keeps the rollback journal."""
    assert store.open_db(str(tmp_path / 'prod.sqlite')).execute('pragma journal_mode').fetchone()[0] == 'delete'


def low_space_from(monkeypatch, nth_day):
    """Free space reported below the need from the `nth_day`-th day the writer checks (1 = before the first day)."""
    checked = []

    def free(folder):
        checked.append(folder)
        return 0 if len(checked) >= nth_day else 10 ** 15
    monkeypatch.setattr(ladder_adapter, 'free_bytes', free)


@pytest.mark.parametrize('nth_day, expected_last', [(1, None), (3, 'second')])
def test_low_space_stops_the_writer_before_a_day_and_the_launcher_records_it_incomplete_without_a_redo(tmp_path, monkeypatch, nth_day, expected_last):
    low_space_from(monkeypatch, nth_day)
    record = run_stage_b.send(tmp_path, transport=fake_judge, sleep=lambda seconds: None)
    days = completed_days(tmp_path / 'draw-u1' / 'views.sqlite')
    assert record['u1']['state'] == 'incomplete' and [a['folder'] for a in record['u1']['attempts']] == ['draw-u1']
    assert not (tmp_path / 'draw-u1-redo').exists() and 'u2' not in record
    attempt_reason = record['u1']['attempts'][0]['stopped']
    assert attempt_reason.startswith('WriterStopped: free space below 20 times the store')
    assert record['stopped'] == f"u1 incomplete: {attempt_reason.split(': ', 1)[1]}"
    counts = __import__('json').loads((tmp_path / 'draw-u1' / 'adapter-counts.json').read_text())
    if expected_last is None:
        assert days == [] and counts['last completed day'] is None
    else:
        assert len(days) == 2 and counts['last completed day'] == days[-1]
    assert counts['stopped'] == attempt_reason.split(': ', 1)[1]


def test_three_failed_checkpoints_stop_the_writer_before_the_next_day(tmp_path, monkeypatch):
    monkeypatch.setattr(ladder_adapter, 'truncate_checkpoint', lambda conn: 'busy')
    record = run_stage_b.send(tmp_path, transport=fake_judge, sleep=lambda seconds: None)
    assert record['u1']['state'] == 'incomplete' and not (tmp_path / 'draw-u1-redo').exists()
    assert record['stopped'] == 'u1 incomplete: the truncating checkpoint failed after 3 consecutive completed days (another connection held the store)'
    assert len(completed_days(tmp_path / 'draw-u1' / 'views.sqlite')) == 3


def test_a_reader_held_across_three_completed_days_stops_the_writer_and_readers_keep_the_last_completed_day(tmp_path, monkeypatch):
    """The real checkpoint, held back by a real reader transaction opened after the first day."""
    out = tmp_path / 'out'
    holder = {}
    real = ladder_adapter.LadderAdapter.close_and_complete

    def open_a_long_reader_after_the_first_day(self, day):
        closed = real(self, day)
        if 'conn' not in holder:
            reader = service.open_ledger(str(out / 'views.sqlite'))
            reader.execute('begin')
            reader.execute('select count(*) from views').fetchone()
            holder['conn'], holder['day'] = reader, day
        return closed
    monkeypatch.setattr(ladder_adapter.LadderAdapter, 'close_and_complete', open_a_long_reader_after_the_first_day)
    with pytest.raises(ladder_adapter.WriterStopped) as stopped:
        ladder_adapter.replay('u1', out, transport=fake_judge, cap_usd=5.0)
    assert stopped.value.reason.startswith('the truncating checkpoint failed after 3')
    assert service.resolve_bound(holder['conn'], None) == holder['day']          # the held reader still sees its own state
    holder['conn'].rollback()
    days = completed_days(out / 'views.sqlite')
    assert len(days) == 3 and stopped.value.last_completed_day == days[-1]
    with service.open_ledger(str(out / 'views.sqlite')) as fresh:
        assert service.resolve_bound(fresh, None) == days[-1]


def test_a_writer_killed_after_committed_partial_day_writes_leaves_every_answer_equal_to_its_last_completed_day(tmp_path, monkeypatch):
    out = tmp_path / 'out'
    taken = {}
    real = ladder_adapter.LadderAdapter.close_and_complete

    def complete_two_days_then_die_in_the_third(self, day):
        done = len(taken.get('days', []))
        if done == 2:
            raise KeyboardInterrupt('killed mid-day, after the day\'s articles were committed')
        closed = real(self, day)
        taken.setdefault('days', []).append(day)
        if len(taken['days']) == 2:
            target = sqlite3.connect(str(tmp_path / 'backup.sqlite'))
            self.conn.backup(target)
            target.execute('pragma journal_mode=delete')
            target.close()
        return closed
    monkeypatch.setattr(ladder_adapter.LadderAdapter, 'close_and_complete', complete_two_days_then_die_in_the_third)
    with pytest.raises(KeyboardInterrupt):
        ladder_adapter.replay('u1', out, transport=fake_judge, cap_usd=5.0)
    live, kept = service.open_ledger(str(out / 'views.sqlite')), service.open_ledger(str(tmp_path / 'backup.sqlite'))
    partial = live.execute('select count(*) from processing_steps where publication_day > ?', (taken['days'][-1],)).fetchone()[0]
    assert partial > 0                                                        # the third day's articles are in the file
    item_of = bundle.item_lookup(None)
    for name, call in (('views', lambda c: service.views(c, None, None, include_closed=True)),
                       ('library', lambda c: bundle.library(c, None)),
                       ('changes', lambda c: service.changes(c, '2000-01-01')),
                       ('search', lambda c: search.search(c, None, 'revenue data center', 10, semantic=False)),
                       ('days', lambda c: bundle.days(c))):
        assert call(live) == call(kept), name
    sent = []
    index = search.open_index(str(tmp_path / 'index.sqlite'))
    search.build_index(live, index, embed=lambda texts, model: (sent.extend(texts) or search.fake_embed(texts, model, dims=8)))
    visible = {r['view_id'] for r in service.summaries(kept, None, include_closed=True)}
    assert len(sent) == len(visible)                                          # nothing of the partial day is embedded


def test_the_writers_end_leaves_wal_mode_without_a_reader_and_keeps_it_with_one(tmp_path, monkeypatch):
    runner = ladder_adapter.replay('u1', tmp_path / 'alone', transport=fake_judge, cap_usd=5.0)
    assert runner.counts['store journal mode at the end'] == 'delete' and 'stopped in order' not in runner.counts
    held = {}
    real = ladder_adapter.leave_wal

    def with_a_reader(conn):
        reader = sqlite3.connect(str(tmp_path / 'held' / 'views.sqlite'))
        reader.execute('begin')
        reader.execute('select count(*) from views').fetchone()
        held['reader'] = reader
        return real(conn)
    monkeypatch.setattr(ladder_adapter, 'leave_wal', with_a_reader)
    runner = ladder_adapter.replay('u1', tmp_path / 'held', transport=fake_judge, cap_usd=5.0)
    assert runner.counts['store journal mode at the end'] == 'wal'
    assert runner.counts['stopped in order'] == 'WAL kept: another connection held the store at the end'
    held['reader'].rollback()
