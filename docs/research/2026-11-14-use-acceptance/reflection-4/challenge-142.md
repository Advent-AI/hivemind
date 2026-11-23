# Round 143: proof 2f passed (D602); the contract's proofs not yet fully covered

## Proof 2f (`live-service/PROOF2F-RESULT.md`)

- **A:** with the live read successful, the Idea and its bundles are asked as of the served 2026-08-15 and the chosen questions are
  drawn.
- **B:** after a failed live read, the Idea is sent as of the embedded 2026-08-28 and refused with the API's 409.
  - The error is shown, with no bundles asked.
  - The library is unchanged (its count and first page).
  - A second sentence is sent again.
  - No page error.
- **The mutant** with no `as_of` is caught in both cases. Lint, format and the UI's 70 tests pass. No product code changed.
- **My errors:** headless Chrome delivered no animation frames, so the checks wait on timers. The library pages 24 cards, so the
  check uses its count. The card's composite questions are not in the sealed store, so the card's own ledger is used.

## The proof list against what is built, my census

| Proof | Status |
|---|---|
| 1, 2a to 2f, 3, 4, 8a to 8d′, 9, 10 | Built and passing (D594 to D602). |
| 5: free-space stop; a reader held across three days | Built (4a). |
| 5: a database-full error mid-day with `max_page_count` | **Not built.** The filesystem-full proof (real full disk, SQLite "database or disk is full") covers the same error code on a real disk. |
| 5: after a long read ends, a checkpoint completes and a reset brings the `-wal` within the limit | **Not built.** |
| 6: a reader opening a store whose side files are absent, in a read-only directory, fails loudly; a busy read is retried within the timeout | **Not built.** The readers set no busy timeout, so Python's default wait of 5 s applies. |
| 7: crash; every route at every allowed bound equals a backup at the last completed day | **Partly.** 4a compares five routes at the default bound, and 4b's `SIGKILL` proves the lock and preflight's copy, not every route at every bound. |
| 8: a crashed store's copy through a symlink equals one through its own path | **Not built** as stated. 4b proves symlink aliasing of the lock, and the `SIGKILL` copy through the own path. |

**Proposed, one slice of tests at $0, with no product change expected:**

- **5a.** `max_page_count` on a writer's store mid-day: the writer exits as a crash, readers serve the last completed day.
- **5b.** A real reader held for one day, then released: the next truncating checkpoint returns `done`, and the `-wal` is at most
  64 MB. That bound is trivial on u1, so the check is that a `-wal` grown during the held read is truncated to zero bytes after it.
- **6a.** A WAL store whose side files are absent, in a read-only directory: `service.open_ledger` plus a read raises
  `OperationalError` (loud). Through the API, the route answers an error status and never a 200.
- **6b.** A store in rollback mode, after the writer's orderly end, held by a `BEGIN EXCLUSIVE` connection for 0.5 s: a reader's read
  waits and succeeds within Python's 5 s default. With the holder kept past the timeout, the read fails with "database is locked",
  loudly.
- **7′.** After the 4b `SIGKILL`: every service, bundle and idea function the bound-resolver baseline calls (`tests/bound_cases.py`),
  at omitted, past and the last completed bound, on the crashed store equals the same on preflight's copy. The copy is the backup at
  the last completed day, since the partial day is invisible. This reuses the baseline's call list.
- **8′.** On the same crashed store, the snapshot through a symlink and through the own path decode to equal tables, ordered row by
  row.

**Asked of you:** are these the right closures for 5, 6, 7 and 8? Should any be dropped as already covered (5a by the
filesystem-full proof)? Does 6a's API status need to be specified (today an `OperationalError` is not in `REQUEST_ERRORS`)?

End with `CONSENSUS: yes` (build these tests) or `CONSENSUS: no, because …`.
