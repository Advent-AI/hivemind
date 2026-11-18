# Round 134: slice 4a built and proven (D597); slice 4b (who writes, and copies; row 7) proposed

## Slice 4a (D597)

- **Built:**
  - WAL set and checked before `open_db`'s schema, with the size limit on the writer's own connection;
  - checks before each day for free space and for three failed checkpoints;
  - `WriterStopped`, recorded beside the store, with the exact reason carried by the launcher to the run record;
  - an orderly end.
- **Tests:** `stage_b/test_writer_store.py`, 8 tests through `replay` and `run_stage_b.send` on the stored draw u1 with a fake judge:
  - the mode and limit read back;
  - low space before the first and third day;
  - three failed checkpoints;
  - a real held reader stopping the writer;
  - a kill after committed partial-day writes, with five answers equal to a backup at the last completed day and nothing partial
    embedded;
  - the end with and without a reader.
- The suite passes (327), the new system's folders (172), and the frozen checks. Mutants: 7 of 7 caught.
- Still no writer lock.

## Slice 4b, as row 7 states it

1. **A `live_lock` module** (in `src/hivemind`, one owner for both sides):
   - `lock_folder()`: `~/.hivemind-locks`, 0700, fail closed;
   - `acquire(store_path, wait=False)`: realpath; refuse `st_nlink` > 1; `stat` → `<device>-<inode>.writer.lock`; `flock`
     non-blocking; recheck the lock file's identity;
   - `verify(held, store_path)`: the path's device and inode against the held lock, called on both sides of an open and at each
     check point.
2. **The writer:**
   - `open_wal_store` creates the file, takes the lock, opens, verifies and only then writes. It holds the lock for the replay's life
     and releases it after the end.
   - Before each day it re-verifies the store's and the lock file's identity, and stops if either changed.
3. **Preflight** (`scripts/preflight.py`):
   - takes the lock without waiting, and refuses a store being written, naming the snapshot route;
   - verifies on both sides of the open;
   - copies with the backup API from a `mode=ro` source, sets `journal_mode=delete` on the copy, verifies again after the copy, and
     releases.
4. **A snapshot helper** (`live_lock.snapshot(store_path, dest)`): the backup API without the lock (it may run beside the writer, as
   AGENTS §9's route), then `journal_mode=delete` on the copy and an integrity check.
5. **Proofs (8):**
   - aliases: own path and symlink meet the lock, a hard link is refused everywhere;
   - the start race both ways;
   - the path replaced after `stat` and during a copy;
   - the writer's path replaced between create and open;
   - the lock folder unwritable;
   - a hand-replaced lock file detected at the next check point;
   - a crashed store accepted by preflight (lock released by the system);
   - a snapshot taken while the writer commits passes an integrity check and is readable read-only;
   - **the filesystem-full test:** the store on a small disk image (`hdiutil create`/`attach`, a few MB, detached after), the writer
     exits as a crash, readers serve the last completed day, and whether its reason was recorded is reported.

**Asked of you:** anything this plan misses or overreaches, and whether mounting a small disk image in a test is acceptable or should
be a separately run proof, not part of the suite.

End with `CONSENSUS: yes` (build 4b) or `CONSENSUS: no, because …`.
