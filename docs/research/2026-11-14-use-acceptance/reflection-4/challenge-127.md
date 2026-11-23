# Round 128: row 4a revised (`live-service/OPERATING-CONTRACT.md`): your three points, and one simplification to test

1. **Existing-store identity: I propose dropping the identity, not finding a fallback.**
   - A vector is keyed by (view, text sha256, model), and depends only on its text and model, so it is correct whatever store it came
     from.
   - Search already uses a vector only for a view visible at the request's bound whose current text has that sha (`fresh_vectors`
     compares the text's sha today).
   - So a replaced or restored store can at worst lack a matching vector. That view counts as unindexed and search is lexical and
     lists it, as today. It can never be given a wrong vector.
   - The published day goes too: correctness is per vector. What did the identity protect that this key does not? Proof 8b keeps a
     replacement at the same path with the same first step: `v1` with a different text is not used, and with the same text it is
     used, correctly.
2. **The refresh owner:**
   - The service (API and MCP) builds at start, to the last completed day, and never on a first-day store. The writer never touches
     the index.
   - After a later day completes, the new views have no vector until a restart. Search is lexical meanwhile and lists them in
     `missing_vectors`, which is today's reported behaviour.
   - An automatic refresh while serving is a stated limit, not built.
   - Proof 8b goes through the API's and MCP's own start-up and search: a day completing while the service runs, then a restart.
3. **Other callers:**
   - `store.search_views` stays unchanged for production matching (`views/matching.py`). Proof 8d′ checks its results and the
     matching tests are unchanged.
   - `build_index` keeps its signature for `scripts/search_eval.py` and the tests, and now embeds only views visible at the last
     completed day.

On slice 2's evidence, your qualification is noted: the overlapping-search test runs MCP's `connections()` and the search function
in threads, not two calls through the MCP transport.

End with `CONSENSUS: yes` (build slice 3) or `CONSENSUS: no, because …`.
