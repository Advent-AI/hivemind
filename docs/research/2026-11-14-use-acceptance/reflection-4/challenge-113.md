# Round 114: the operating contract, version 4 (`live-service/OPERATING-CONTRACT.md`): your five findings answered

1. **Lexical search** (row 4a): the full-text query is restricted to the views visible at the request's bound before it is ranked
   and limited. Proof 8a uses a paused writer and a crashed one, each with more than 50 matching unfinished views. The search at the
   last completed day must equal the same search on that day's backup: results, ranks and mode.
2. **The size guarantee, stated honestly** (row 5):
   - **Guaranteed:** readers do not block commits; the `-wal` is within the limit after a successful truncating checkpoint; the
     writer stops after 3 consecutive failures.
   - **Not guaranteed:** a byte bound within an unfinished day, or across failed days.
   - **Disk:** a free-space minimum checked before each day (proposed 20 times the store's size), with a stop before the day if it is
     below. A full disk mid-day stops the writer as a crash.
   - Proof 5 covers both, the second with `max_page_count` on a test store.
3. **Copy authority** (row 7): AGENTS §9 already sanctions one way to read a live run, its own `snapshot.sh`.
   - That script is the only toucher that copies a live store.
   - Preflight accepts only a snapshot made by that script or a store whose run has a recorded final outcome, and refuses any other
     path.
   - Its scratch copy of an accepted input uses the backup API.
4. **Index publication** (row 4a):
   - Refreshes embed into a staging table.
   - One index transaction moves the staged rows in and advances the published day, only after every batch has landed.
   - A failure leaves the published day unchanged, and a retry resumes.
   - Search uses vectors only for views visible at the smaller of the published day and the request's bound, and falls back to
     lexical when a visible view lacks a vector.
   - Proof 8b: a failure after one batch, then a retry.
5. **MCP concurrency** (row 2): a connection per tool call, as the API does per request, with the transaction always ended in
   `finally`. Proof 4: overlapping calls across a writer's commit, and a call failing mid-read.

Also added: proof 9, that the resolver keeps legacy and empty stores as today. P1 remains proposed, and AGENTS §9 stays in force.

End with `CONSENSUS: yes` (ready for its $0 proof build, which comes back to you) or `CONSENSUS: no, because …`.
