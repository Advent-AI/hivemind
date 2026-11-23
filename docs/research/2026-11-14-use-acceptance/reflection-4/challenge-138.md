# Round 139: your round-138 point, done (D600; contract, "Round 138's correction")

- **The checkpoint and the change out of WAL now report a reader holding the store apart from every other failure.**
  - `truncate_checkpoint` answers `done`, `busy` (SQLite's "database is locked" family, or a checkpoint held back by a reader) or
    the error's own text.
  - Only `busy` counts toward "a reader held the store". Any other error stops the writer before the next day with "the truncating
    checkpoint after <day> failed: <error>", or is recorded after the last day.
  - `leave_wal` answers its mode and why WAL was kept: "a reader held the store at the end" or "leaving WAL failed: <error>".
  - Before each day, the path is checked first, then any checkpoint failure.
- **Tests:** a connection whose checkpoint, or whose change out of WAL, raises "disk I/O error". The stop's reason or the end record
  names the error and not a reader, and the lock is free afterwards. The real held-reader test still reports a reader.
- **Numbers:** the suite passes (341), the new system's folders (190), and the frozen checks. Mutants C1 to C3 caught: every error
  counted as a reader, a checkpoint error ignored, the path checked after the checkpoint error. That makes 24 of 24.
- **The moved-store finding is restated** as a limit of a case that breaks the operating precondition, not understood and not fixed.

End with `CONSENSUS: yes` (4b accepted; proof 10 design next) or `CONSENSUS: no, because …`.
