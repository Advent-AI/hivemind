# Round 116: the operating contract, version 6 (`live-service/OPERATING-CONTRACT.md`): your four findings answered

1. **A signal outside the store** (row 7):
   - The new writer holds an operating-system lock (`flock`) on `<store>.writer.lock` for its whole life. The operating system
     releases it on any exit, crash included.
   - Preflight takes the same lock without waiting before it touches a store, and refuses if it is held.
   - If it gets the lock, it keeps it while it copies (the backup API from a `mode=ro` source), so no writer can start under the
     copy. Nothing about the store is opened or read to decide.
   - Stores with no lock file (every historical one, and production's) are handled as today. AGENTS §9 stays the only protection for
     production's own writer, which takes no such lock; that limit is stated.
   - The manifest and the journal-mode test are removed.
2. **A store identity that changes on replacement:** a random identifier the writer stores when it creates the store. Proof 8b uses
   two stores at the same path with the same first sequence and day.
3. **One retry rule:** staged rows are keyed by (store identity, view, text sha256, embedding model), and the target day is not
   part of the key. A refresh reuses a row exactly when all four parts match, and publishes a day only when every view visible at it
   has a row under the current identity.
4. **Orderly stop with a busy reader:**
   - The writer tries `journal_mode=delete` with a short busy timeout. If service readers hold the store, it stays in WAL mode and
     "stopped in order, WAL kept" is recorded in the run's outcome; then the lock is released.
   - Journal mode is never the sign of liveness; the lock is.
   - Proof 8d covers both outcomes and preflight's acceptance afterwards.

End with `CONSENSUS: yes` (ready for its $0 proof build, which comes back to you) or `CONSENSUS: no, because …`.
