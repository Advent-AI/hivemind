# Round 117: the operating contract, version 7 (`live-service/OPERATING-CONTRACT.md`): your three findings answered

1. **Aliases:**
   - The lock is named by the store file's device and inode numbers, read with `stat` (no content read), in one fixed folder
     (`~/.hivemind-locks/<device>-<inode>.writer.lock`).
   - A symlink resolves to the same file and a hard link shares the inode, so every alias reaches one lock.
   - Proof 8: the store's own path, a symlink and a hard link each meet the writer's lock.
2. **The start race:**
   - Preflight always takes the lock without waiting, creating the file if absent, and holds it through its copy. There is no "no lock
     file" branch.
   - The writer creates its store file empty and takes the lock before writing anything, and refuses to start if it is held.
   - Whichever comes first wins and the other refuses. Proof 8 covers preflight arriving just before the writer.
3. **Published vectors on replacement:**
   - The index records the store identity it was published for.
   - A published vector is used only when the identity matches, the published day is on or before the store's last completed day,
     and its text sha matches the view's text at the bound. Otherwise the view counts as unindexed and search runs lexically.
   - A store restored from a snapshot keeps its identity, but a later published day or a changed text still disqualifies its
     vectors.
   - Proof 8b covers both replacement cases.

The stale manifest wording is removed: no manifest remains in the file.

End with `CONSENSUS: yes` (ready for its $0 proof build, which comes back to you) or `CONSENSUS: no, because …`.
