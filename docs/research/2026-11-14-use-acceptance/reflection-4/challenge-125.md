# Round 126: your four points answered (contract row 2 and row 3's legacy sentence; one new test)

1. **The legacy ledger:**
   - Today's default (`default_as_of`, unchanged) already queries `days_completed`, so a ledger without the table fails today with
     "no such table: days_completed".
   - The new test `test_a_ledger_without_the_completed_day_table_fails_exactly_as_it_did_before` shows four public calls, omitted and
     explicit bounds, failing with exactly that error. The census of 143 stored ledgers found none without the table.
   - The contract's sentence now says this instead of "reads as today". The resolver suite passes (10 tests).
2. **MCP's object list stays in its instructions, labelled with its day:**
   - It is computed once at start through `idea.object_list`, which resolves its bound. The direct `service.default_as_of` call in
     `scripts/hivemind_mcp.py` goes.
   - The text names the start day and says every tool reads the current last completed day.
   - On a first-day store it says no day has completed, and the tools refuse.
   - No tool is added. Proof 4 tests, at the actual entry point, that after a later day completes a tool sees that day's views while
     the instructions keep their start day.
3. **Concurrent search:** MCP opens its ledger, items and index connections per tool call. The index is written during a search (the
   query-embedding cache), so overlapping searches never share one. Proof 4 includes two overlapping search calls.
4. **The API's snapshot pinned:**
   - `BEGIN`, then a first read (the bound resolution), fixes the committed state in WAL mode before any writer is released in the
     test.
   - A failure while opening closes what was already opened inside `__enter__`. Proof 4 includes an opening error leaving no
     connection open.

End with `CONSENSUS: yes` (build slice 2) or `CONSENSUS: no, because …`.
