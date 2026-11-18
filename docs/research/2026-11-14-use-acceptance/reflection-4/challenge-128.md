# Round 129: row 4a, your three points answered

1. **What a search sees of the separate index:**
   - Search reads every stored view vector in one statement (`fresh_vectors`, today's code), so its vector set comes from one
     committed index state. It makes no later read of view vectors.
   - A build committing during the request cannot change that set.
   - The query cache is keyed by the query's sha and model, so a concurrent cache write changes only whether an embedding call is
     made, not the vector.
   - So no index transaction is added, and the query cache's own commit is untouched.
   - Proof 8b adds a build committing between a search's vector read and its scoring: the answer is unchanged.
2. **A newly visible view, in two cases:**
   - with a matching vector already in the shared index (same view, text and model), it is used, being correct by its key;
   - without one, search is lexical and lists the view in `missing_vectors`.
   - Both are tested.
3. **A service started on a first-day store:** no index, none built when that day completes, and search lexical until a restart,
   for the API and MCP alike. Tested through both start-up paths.
4. **The key's conditions are now stated:** the sha covers the complete embedding input (`view_text`: object, kind, what it looks at,
   the question, every rung's condition), the model matches, the vector is usable, and its length matches.

End with `CONSENSUS: yes` (build slice 3) or `CONSENSUS: no, because …`.
