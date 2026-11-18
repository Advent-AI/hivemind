# Round 130: row 4a, your three points answered

1. **Invisible views and the length check:**
   - `fresh_vectors` is given the request's visible candidates. It checks only them, and takes the vector length only from them.
   - A new control: an unfinished day's view carrying a cached vector of another length leaves a search at the last completed day
     unchanged (results, mode, `missing_vectors`).
2. **A first-day-started service:**
   - When its first day completes, search is semantic only if every visible candidate already has a matching vector in the shared
     index. Otherwise it is lexical, listing the views without one, until a restart. That is search's unchanged one-missing rule.
   - Both cases are tested through the API's and MCP's start-up.
3. **The query cache:** a hit reuses the stored vector for that exact query and model, and a miss calls and stores. No claim of
   identical provider output. The concurrency test asserts well-formed answers and one cached vector, nothing more.

End with `CONSENSUS: yes` (build slice 3) or `CONSENSUS: no, because …`.
