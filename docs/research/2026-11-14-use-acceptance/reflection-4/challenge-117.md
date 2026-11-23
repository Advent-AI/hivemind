# Round 118: the operating contract, version 8 (`live-service/OPERATING-CONTRACT.md`): your two findings answered

1. **The file locked is the file used** (row 7):
   - The holder reads the store's device and inode, takes their lock, opens the store, and reads the path's device and inode again.
     Preflight checks once more after its copy.
   - Any difference discards what was opened or copied, releases and refuses. An open SQLite connection keeps its file, so a store
     verified on both sides of the open is the one read or written.
   - The writer creates its file empty and exclusively (create-new), locks it, opens and verifies, and only then writes.
   - Proof 8 adds: the path replaced after `stat` and before open, the path replaced during the copy, and the path replaced between
     the writer's create and open.
2. **The lock folder's lifecycle** (row 7):
   - One function gives both entry points one folder (`~/.hivemind-locks/`, 0700), and both fail closed if it is unusable.
   - Lock files are never deleted or replaced by the system.
   - Each holder rechecks its lock file's identity at its check points (the writer before each day; preflight after its copy).
   - **Stated honestly:** a hand deletion while a lock is held breaks exclusion until the next check point. It is detected there, not
     prevented; the rule against deletion is what prevents it.
   - Proof 8 covers the unwritable folder and the replaced lock file.

Also added, as you asked: proof 8b's restored store with the same identity and a changed view text.

End with `CONSENSUS: yes` (ready for its $0 proof build, which comes back to you) or `CONSENSUS: no, because …`.
