# Round 137: slice 4b built and proven (D598); next, proof 10 (serving while the real writer runs)

## Slice 4b (D598)

- **Built:**
  - `src/hivemind/live_lock.py`;
  - the writer's lock life in `ladder_adapter` (`open_wal_store`, the check before each day, `LadderAdapter.close`, the `finally`
    around `replay`);
  - preflight's `locked_copy` and `store_copies`;
  - `scripts/snapshot_store.py`;
  - the conftests' temporary lock folder.
- **Tests:** `tests/test_live_lock.py` (12) and `stage_b/test_writer_lock.py` (14), including a real `SIGKILL` of a writer process
  on its third day and a snapshot taken beside the writer holding uncheckpointed commits. The suite passes (339), the new system's
  folders (186), and the frozen checks. Mutants: 17 of 17 caught (`live-service/lock-mutants.txt`).
- **The filesystem-full proof** ran separately, each variant on its own 2 MB image, both detached
  (`live-service/filesystem-full-proof.output.txt`):
  - **A, the stop switched off:** the disk filled on the tenth day and the writer crashed with "database or disk is full". Nine days
    were kept and served by readers and by preflight's copy, and the lock was free.
  - **B, the stop as built:** it stopped before the first day with its reason recorded.
- **Found and fixed in the slice** (contract, "Found while building 4b"):
  1. **A WAL-mode store without side files cannot be opened read-only**, and the product's own readers open `mode=ro`.
     - Reproduced on scratch stores. The writer now leaves WAL on every exit, not only its normal end.
     - Tested: the mode is `delete` after every exit.
     - I did not see the state left by the writer itself in two direct checks; the side files remained after a stop in both. So
       this is a guard on a reachable state (the last closer read-write in WAL mode), not an observed failure of the writer. Say
       whether it is warranted.
  2. **Preflight's part E reread each store unlocked.** One locked copy now feeds both parts, tested through `main`.
  3. **`verify` now names a missing store or a new hard link** as `PathChanged`.
- **My errors:** a fixture that built the unreadable state itself; an after-open test that failed inside `acquire`'s own `verify`;
  the first filesystem-full run sharing one disk.

**Asked of you:** anything in 4b that departs from row 7 or rounds 134 to 136, and whether fix 1 is a warranted guard or a mechanism
for a case no one named.

## Next: proof 10

Re-run `page-contract/serving_while_writing.py` on the built code. Today it pauses a writer and serves the page. Proposed change: the
writer is the real `replay` (WAL, lock), and the API and MCP serve from its store while it writes. Each request is checked to answer
as one completed day, never the half-processed day, and never a mixed state within one request. I will read the harness before
proposing its exact steps.

End with `CONSENSUS: yes` (4b accepted; proof 10 next) or `CONSENSUS: no, because …`.
