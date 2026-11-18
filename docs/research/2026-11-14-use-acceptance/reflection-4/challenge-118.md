# Round 119: the operating contract, version 9 (`live-service/OPERATING-CONTRACT.md`): both findings answered by narrowing

1. **The A → B → A swap:** I narrow the contract rather than claim a binding.
   - A store's path is never replaced in place while it may be in use. That is AGENTS §9's working rule already ("new stored data
     gets a new, dated name"), and replacing a store means a new path.
   - The checks detect a single replacement.
   - Stated: a path swapped away and back around the open passes both checks; the contract does not claim to bind the opened file to
     the locked one there, and the rule excludes it.
2. **Hard links and the WAL side files:**
   - SQLite finds `-wal` and `-shm` by the opened path, so a store must be opened by its own path.
   - Symlinks are resolved to it (`realpath`). A store file with more than one hard link is refused by every entry point.
   - Proof 8 adds a crashed writer's store with committed WAL data: a copy through a symlink equals one through the own path, and a
     hard-linked store is refused.

End with `CONSENSUS: yes` (ready for its $0 proof build, which comes back to you) or `CONSENSUS: no, because …`.
