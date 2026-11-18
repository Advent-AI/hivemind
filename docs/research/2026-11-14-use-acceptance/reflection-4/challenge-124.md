# Round 125: slice 1 (the bound resolver) built and proven; go for slice 2 (row 2: one read transaction per request, MCP per call, the streamed route)?

## Slice 1 (D594)

- The resolver, the range function and the three exceptions are built. Every public date function routes through them, and the API
  returns structured 503/409 bodies.
- `tests/test_bound_resolver.py`:
  - 176 calls on four real store states compared with today's recorded outcomes. Every difference is a contract change.
  - The structural check, the range rule on three stores, and the API mapping.
- The suite passes (308), and so do the new system's folders (164).
- Mutants (`live-service/resolver-mutants.txt`): 8 caught. M7 is equivalent, because `view_bundle` ends in `not_judged`'s identical
  refusal; M8 and M9 show that refusal is guarded.
- The contract's range text is aligned with round 124. Nothing is deployed or restarted.

## Slice 2, as the contract states it

1. **API `Connections`:** `BEGIN` on the ledger on entry, after opening, and the transaction ended in `__exit__` on every path.
2. **MCP:** a connection opened per tool call (a context manager like the API's), in place of the process-wide `LEDGER`. `OBJECTS`
   is computed per call. The index connection stays process-wide for now, since the index is row 4a's slice.
3. **The streamed Idea route:**
   - connections opened, the transaction begun and `resolve_bound` run on the request's `as_of` (with the first-day check);
   - then the 200 headers, then the Idea work in the same transaction;
   - a refusal is a normal status and body before any header.
4. **Proofs:**
   - 3: an API request held between its first and last read by a hook, while a writer commits a judgement and completes a day,
     returns its start state, and the writer commits;
   - 4: two overlapping MCP calls across a commit, a call failing mid-read leaving no open transaction or connection, and no
     transaction open between calls;
   - 2e: the streamed route refused before headers on a first-day store and on a future date.
   - All on test stores in WAL mode, set by the test.

End with `CONSENSUS: yes` or `CONSENSUS: no, because …`.
