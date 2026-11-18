# Round 51: the live-service design. Attack before any code.

`live-service/DESIGN.md`: the stores are in rollback-journal mode (checked: `delete`), where pinning a request to one snapshot can hold the
writer; the design puts the new loop's store in WAL mode (production's stores unchanged), checks readiness inside one read transaction
per request in the API (`Connections`) and around each MCP tool, computes MCP's object list per call, checks the streamed Idea route
before its headers, and records (not builds) a page notice for a collected snapshot as Alex's presentation choice; a state × event table;
a proof that holds a request between its check and its read while the writer commits.

Attack: WAL with read-only (`mode=ro`) connections (the -wal/-shm files, the directory's permissions); checkpointing; anything WAL
changes for the writer (the extension proof's byte-equality of stores, if any check compares files); every reader that opens the store
outside `Connections`; whether the page notice should wait for Alex. End with `CONSENSUS: yes` (build as designed) or `CONSENSUS: no, because …`.
