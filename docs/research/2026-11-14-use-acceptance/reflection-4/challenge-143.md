# Round 144: slice 5, row 1 made true in code, and the open proofs (contract, "Slice 5")

Your three points:

1. **7′ now has an independent reference.** The killed writer backs up its own store right after its second day completes, before any
   third-day write. The crashed store and preflight's post-crash copy are each compared with that reference.
   - The calls are exactly `bound_cases.calls`' 14: 8 service, 5 bundle and lexical search.
   - Each runs at the omitted bound, the first completed day, the last completed day and a future day.
   - Idea functions are not in the list, and the report says so.
2. **6a is specified as a product change.**
   - A new `service.open_pinned(path)` opens, begins and pins. It is the one opener for the API's `Connections` and MCP's
     `connections()`, replacing their two copies.
   - On a SQLite failure it closes what it opened and raises `StoreUnreadable("<path>: <message>")`, a `LedgerError`.
   - The API answers 500 with the path, before headers on the streamed route. MCP raises it.
3. **Busy reads.**
   - `store.open_read_only` sets `timeout=READ_BUSY_TIMEOUT_SECONDS` (5 s) explicitly. SQLite's busy handler retries within it,
     with no application-level retry, and row 1's wording is narrowed to that.
   - The test holds a WAL store with a connection in exclusive locking mode, as a stand-in for SQLite's rare WAL busy cases (such as
     index recovery), which cannot be timed.
   - Released after 0.5 s, the read waits and succeeds. Held past a 0.3 s timeout, it fails loudly with the path.

**Kept:** 5a (`max_page_count`) beside the real-disk proof, which it does not replace. Also 5b (a busy checkpoint during a held read,
then `done` with the `-wal` at 0 bytes) and 8′ (snapshot through a symlink equals one through the own path, row by row).

End with `CONSENSUS: yes` (build slice 5) or `CONSENSUS: no, because …`.
