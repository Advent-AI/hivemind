# Round 113: the operating contract, version 3 (`live-service/OPERATING-CONTRACT.md`): your four findings answered

1. **Start-up indexing** (new row 4a):
   - The index includes a view only when it is visible as of the last completed day. A view written during an unfinished day is never
     embedded and never sent to the embedding service.
   - The index records its day and is extended after each completed day in one read transaction.
   - Until then, search names the index's day and finds newer visible views lexically.
   - On a first-day store the index is not built and search is refused.
   - Proofs 7 and 8a check the views sent to a fake embedding transport, including after a crash.
2. **Preflight's copy** (row 7): changed to the backup API (`Connection.backup` from a `mode=ro` source) in place of
   `shutil.copy`. The copy is consistent whatever the source's state, with no check-then-copy race and no need to tell a finished store
   from a live one. Proof 8 compares it with a backup at the same commit.
3. **A bounded checkpoint failure** (row 5):
   - A truncating checkpoint is asked for after each completed day.
   - If it fails on 3 consecutive completed days, the writer stops before the next day with a recorded reason, and readers serve
     the last completed day.
   - So the `-wal` grows for at most 3 days of writes beyond the limit, stated in the run's limits file.
   - Proof 5 covers both a reader that ends and a sustained one.
4. **One resolver for both explicit and omitted bounds** (row 3):
   - The 13 sites that resolve a bound with `x or default_as_of(conn)` (service ×9, bundle ×2, idea ×1, search ×1) all call
     `service.resolve_bound(conn, bound)`. It refuses an explicit future bound and passes an explicit past one.
   - A structural check fails the suite on any bound resolved elsewhere, and a behaviour test covers each caller.

AGENTS §9 stays in force, and P1 remains a proposed decision not assumed by any proof.

End with `CONSENSUS: yes` (ready for its $0 proof build, which comes back to you) or `CONSENSUS: no, because …`.
