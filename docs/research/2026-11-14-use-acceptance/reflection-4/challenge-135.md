# Round 136: your three points

1. **No-replace publication:** the snapshot is published by a hard link from the temporary file to the destination, which fails
   if the destination exists, and the temporary file is then removed. A new test creates the destination just before publication:
   it stays untouched, and the helper refuses and removes its temporary copy.
2. **The D597 index line** now says "a partial-day exception inside the writer's process (not a killed process; that proof is 4b's)".
3. **Cleanup inside the opening path:** `open_wal_store` closes any connection it opened and releases the lock before raising, if
   anything fails after the lock is taken. So `replay` only ever owns a fully opened store. Tested by making `store.open_db` fail
   after the lock is taken: the lock is free at once and no connection is open.

End with `CONSENSUS: yes` (build 4b) or `CONSENSUS: no, because …`.
