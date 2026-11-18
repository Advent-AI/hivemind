"""Proofs 5a and 5b (docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md, "Slice 5"; council rounds 143 and 144),
through `replay` and the real launcher on the stored draw u1 with a fake judge: a database-full error during a day stops the writer as
a crash while readers keep the last completed day; and a checkpoint held back by a real reader completes once the reader has gone."""
import os
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / 'e2e-2026-11-09'), str(HERE.parents[2] / 'src')]
import ladder_adapter  # noqa: E402
import run_stage_b  # noqa: E402
from test_ladder_adapter import fake_judge, no_credentials  # noqa: E402,F401
from hivemind import live_lock, service  # noqa: E402


def test_a_database_full_error_during_a_day_stops_the_writer_as_a_crash_and_readers_keep_the_last_completed_day(tmp_path, monkeypatch):
    real, days = ladder_adapter.LadderAdapter.close_and_complete, []

    def cap_the_store_after_the_second_day(self, day):
        closed = real(self, day)
        days.append(day)
        if len(days) == 2:                       # no page may be added from here: the third day's first growth fails
            pages = self.conn.execute('pragma page_count').fetchone()[0]
            assert self.conn.execute(f'pragma max_page_count={pages}').fetchone()[0] == pages
        return closed
    monkeypatch.setattr(ladder_adapter.LadderAdapter, 'close_and_complete', cap_the_store_after_the_second_day)
    record = run_stage_b.send(tmp_path, transport=fake_judge, sleep=lambda seconds: None)
    attempt = record['u1']['attempts'][0]
    assert attempt['stopped'] == 'OperationalError: database or disk is full', attempt.get('traceback')
    assert record['u1']['state'] == 'incomplete' and not (tmp_path / 'draw-u1-redo').exists() and len(days) == 2
    store_path = tmp_path / 'draw-u1' / 'views.sqlite'
    live_lock.release(live_lock.acquire(store_path))                          # free once the writer's connection closed
    with service.open_ledger(str(store_path)) as reader:
        assert service.resolve_bound(reader, None) == days[-1]


def test_a_checkpoint_held_back_by_a_reader_completes_after_it_and_truncates_the_wal(tmp_path, monkeypatch):
    real_close, real_checkpoint = ladder_adapter.LadderAdapter.close_and_complete, ladder_adapter.truncate_checkpoint
    held, outcomes = {}, []
    out = tmp_path / 'out'

    def hold_over_the_first_day(self, day):
        if len(outcomes) == 1:                   # the second day: the reader goes before its completion and checkpoint
            held['reader'].rollback()
            held['reader'].close()
        closed = real_close(self, day)
        if not held:
            reader = sqlite3.connect(str(out / 'views.sqlite'))
            reader.execute('begin')
            reader.execute('select count(*) from views').fetchone()
            held['reader'] = reader
        return closed

    def record_checkpoint(conn):
        outcome = real_checkpoint(conn)
        wal = out / 'views.sqlite-wal'
        outcomes.append((outcome, wal.stat().st_size if wal.exists() else 0))
        return outcome
    monkeypatch.setattr(ladder_adapter.LadderAdapter, 'close_and_complete', hold_over_the_first_day)
    monkeypatch.setattr(ladder_adapter, 'truncate_checkpoint', record_checkpoint)
    ladder_adapter.replay('u1', out, transport=fake_judge, cap_usd=5.0)
    assert outcomes[0][0] == 'busy' and outcomes[0][1] > 0                    # held back: the -wal keeps its frames
    assert outcomes[1] == ('done', 0)                                         # the reader gone: done, and the -wal truncated
