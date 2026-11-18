# Round 132: slice 4a's stop path and WAL start, specified (`live-service/OPERATING-CONTRACT.md`, the new section "The writer's start, stops and end")

1. **WAL before anything is written:**
   - The writer creates the file empty and exclusively, opens it with `sqlite3`, sets `journal_mode=wal` and checks the pragma answers
     `wal` (refusing otherwise), sets `journal_size_limit`, and closes.
   - Only then does it call `store.open_db`, whose schema writes are in WAL mode, the mode being kept in the file.
   - A test reads the mode back after `open_db` and after the first day.
2. **The stop path through the real launcher:**
   - `ladder_adapter.WriterStopped(reason, last_completed_day)` is an `Exception` that `run_stage_b.resendable` does not accept.
   - Before raising it, `replay` writes `adapter-counts.json` with the reason and the last completed day.
   - The launcher's existing branch for a stop no resend can change then applies: `limit.stop(reason)`, the attempt recorded, the
     draw `incomplete`, no redo, every later launch stopped. It is never recorded as complete.
   - The store keeps every completed day, because the stop comes before a day or after a day's checkpoint.
   - A stop before the first day leaves an empty store, recorded incomplete.
   - Tests through `run_stage_b.send` with the existing fake judge: low space before the first day, low space before the third day
     (last completed day the second), and three failed checkpoints. Each checks the record, the state, no redo, the store's last
     completed day and the counts file.
3. **Its end:** `journal_mode=delete` tried with a short busy timeout. With readers it keeps WAL and records it. Tested both ways.
4. **The limit is stated:** no writer lock until 4b. 4a's proofs are on isolated test stores and do not make a live run, or preflight
   beside one, safe. P1 stays unresolved.

End with `CONSENSUS: yes` (build 4a) or `CONSENSUS: no, because …`.
