# Round 133: your two points in slice 4a's design

1. **The run-level stop reason:** a small launcher change. For a `WriterStopped`, `limit.stop` and the run record's `stopped` carry
   `"<run> incomplete: <the stop's reason>"`, not only the exception's name. The tests assert the exact reason in both the attempt and
   the run-level record.
2. **The size limit:** it belongs to a connection, so it is set on the writer's own connection returned by `store.open_db`. The test
   reads both `journal_mode` and `journal_size_limit` back on that connection, after `open_db` and after the first day.

End with `CONSENSUS: yes` (build 4a) or `CONSENSUS: no, because …`.
