# Round 112: the operating contract, version 2 (`live-service/OPERATING-CONTRACT.md`): your six findings answered

1. **Every date bound** (row 3): `to_day` in `history` and `changes` joins `as_of` in every route and tool.
   - A future upper bound is refused, and an omitted one is the last completed day.
   - It is enforced once, in the service's date resolution (today `default_as_of` and its callers).
   - Proof 2 lists the routes from the code, so a new route without a test fails.
2. **WAL size** (row 5): `journal_size_limit` (proposed 64 MB), automatic passive checkpoints, and a truncating checkpoint asked
   for after each completed day with a short busy timeout, retried the next day.
   - The bound is the `-wal` size after a successful reset.
   - Proof 5 checks checkpoint progress, not file shrinkage.
3. **Read-only precondition and busy reads** (row 1):
   - same user and a writable directory;
   - a loud failure when the store cannot be opened or read;
   - a busy timeout with retry.
   - The guarantee is now "readers do not block the writer's commits", not "the writer never waits". Proof 6 covers it.
4. **A crash** (row 6): the day's committed writes stay.
   - Readers stay bounded by the date rule, because those rows are dated after the last completed day.
   - The writer does not resume (today's loop), and the store is served as of its last completed day until replaced.
   - Resuming is a separate design. Proof 7 compares every route against a backup taken at the last completed day.
5. **AGENTS §9 stays in force.** The live-reader exception is a proposed decision (P1), to be resolved before any live operation and
   not assumed by any proof. The proofs run on test stores.
6. **Inventory:**
   - the API's start-up `ensure_index` and MCP's start-up index and object list, which now wait for a completed day and run in one
     transaction;
   - preflight's `shutil.copy`: never on a live store, refused by a check to build with the contract (row 7);
   - `snapshot.sh` named as a per-run file. The contract's copy is SQLite's backup API.

End with `CONSENSUS: yes` (ready for its $0 proof build, which comes back to you before anything runs live) or `CONSENSUS: no,
because …`.
