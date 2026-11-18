# Round 138: your three points from round 137, done (D599; contract, "Round 137's corrections")

1. **Readers open a store by its own path.**
   - `store.open_read_only`, used by the API, MCP, `service` and reports, resolves a symlink and refuses a store with another hard
     link (`LockRefused`, naming the reason).
   - Census first: none of the 702 stored `.sqlite` files has a second link.
   - The API refuses at start (`index_at_start`) and per request (500, reason in the body). MCP refuses at start and per tool.
   - Tested through `hivemind_api.index_at_start`, a real HTTP `GET /days`, an MCP tool on a store linked after start, and an MCP
     load on a linked store.
2. **The finding is narrowed** to its tested conditions: SQLite 3.51.0, scratch stores, and a read-only reader that cannot create the
   `-shm`. It is labelled a guard on a reachable state, not an observed writer failure. A failed change out of WAL is kept distinct
   from a reader holding the store.
3. **Cleanup when cleanup fails:**
   - **`LadderAdapter.close`** releases the lock only once the connection is closed. If leaving WAL fails, it closes and then
     releases (tested). If closing fails, it keeps the lock until the process ends (tested with a connection whose close fails: the
     lock is still held afterwards).
   - **`snapshot`** closes its source if the target cannot be opened, leaving nothing (tested). Its entry point now reports SQLite
     errors as a refusal.

**Found while testing, and fixed:**

- On a store renamed mid-run, SQLite raised "disk I/O error" on the writer's next statement, before its own path check. This
  happened only after the hard-link test had run in the same process, so the launcher recorded `OperationalError` and not the path
  reason. I did not identify which SQLite state in that process makes the difference.
- The writer no longer depends on it:
  - its stop takes the last completed day from its loop, not from the store;
  - the checkpoint and the change out of WAL keep every statement inside their error handling.
- The moved-store test now passes alone, after the hard-link test, and with all three files together (twice).

**Numbers:** the suite passes (341), the new system's folders (188), and the frozen checks. Mutants: 4 more, all caught (R1 to R4;
21 of 21 in `live-service/lock-mutants.txt`).

**Asked of you:** whether 4b is now accepted. Is leaving the SQLite trigger unidentified acceptable, given that the writer no longer
depends on it?

**Next, if yes:** proof 10. I will read `page-contract/serving_while_writing.py` and propose its exact steps, naming the real API and
MCP calls and the pause points, before running it.

End with `CONSENSUS: yes` (4b accepted; proof 10 design next) or `CONSENSUS: no, because …`.
