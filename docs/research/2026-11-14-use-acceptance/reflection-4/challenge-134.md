# Round 135: slice 4b's lock life, snapshot helper and filesystem-full proof, specified (`live-service/OPERATING-CONTRACT.md`, "Who writes, and copies: slice 4b")

1. **The lock's owner:**
   - `replay` owns the connection and the lock in one `try`/`finally`. On every exit (normal end, `WriterStopped`, judge or schema
     error, spending stop, interrupt, opening failure) it closes the connection first, then releases the lock.
   - No caller uses the runner's connection after it returns (searched).
   - Tested on each exit: connection closed, lock free at once.
2. **A real kill:** a subprocess running `replay`, `SIGKILL`ed after committed partial-day writes. The operating system releases the
   lock, preflight takes it and copies, and the copy answers as the last completed day. It replaces 4a's in-process interrupt as the
   crash proof (D597's wording is corrected).
3. **The snapshot helper:**
   - It applies the same path rules (`realpath`, hard links refused) and takes no lock, as §9's route.
   - Its destination must be a new path that is not the source. It writes a temporary file beside the destination, converts it out
     of WAL (checked), checks integrity, then renames atomically. On any failure nothing is left.
   - It is tested through its entry point `scripts/snapshot_store.py`, including a failing conversion.
4. **The filesystem-full proof** is a separate script with a unique image and mount point, always detached and deleted. An image
   that cannot be mounted is reported unexercised.

End with `CONSENSUS: yes` (build 4b) or `CONSENSUS: no, because …`.
