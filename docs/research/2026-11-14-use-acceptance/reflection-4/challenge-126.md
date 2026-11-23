# Round 127: slice 2 built and proven (D595); go for slice 3, search (row 4a)?

## Slice 2

- **API:** a request's ledger state is pinned by `BEGIN` and a first read, the transaction ends on every path, and an opening failure
  closes what was opened.
- **MCP:** connections per tool call, and a labelled start-up object list through the resolving `idea.object_list`.
- **The streamed route:** refuses a first-day store or future date before headers. `/days` refuses a first-day store.
- **Tests:** `tests/test_live_reads.py`, 8 tests on WAL test stores written through the store's own functions. The suite passes
  (317), and so do the new system's folders (164). Mutants: 6 of 6 caught.
- **One build finding, corrected:** my pre-header check first validated the whole body, which broke D281's existing test (a malformed
  body answered in the stream with status 400). It now checks only the contract's date refusals, and the malformed body stays in the
  stream.
- The page reads a non-200 JSON answer as an Idea error (`readIdea`), so a 409 or 503 before headers is shown.

## Slice 3, as the contract's row 4a states it

1. **Lexical search over the visible corpus:**
   - `search.search` ranks the visible candidates' texts in an in-memory full-text table (the same trigram tokenizer), in place of
     `store.search_views`' ranking over the whole `views_fts`.
   - `store.search_views` stays for its other callers, which a census will list.
2. **The index publishes a day:**
   - `build_index` takes the store's identity (a new one-row table the writer creates; for an existing store without it, the
     identity is its path and first step, and the store is then never treated as replaced) and the target day.
   - It embeds only views visible at that day, into a staging table keyed by (store identity, view, text sha256, model), and moves
     them in and advances the published day in one index transaction when every visible view has a row.
   - A failure leaves the published day as it was.
   - `fresh_vectors` uses a published vector only when the identity matches, the published day is on or before the store's last
     completed day, and the text sha matches.
3. **Start-up** (API and MCP): the index is refreshed to the last completed day, not built from every view. On a first-day store
   it is not built.
4. **Proofs:**
   - 8a: lexical search at the last completed day, with more than 50 matching unfinished views, equals the same search on the
     backup;
   - 8b: a refresh failing after one batch, then a retry; another day completing before the retry; a replaced store; a restored store
     with a later published day or a changed text;
   - 8c: the views sent to a fake embedding transport are exactly those visible at the last completed day.

**Asked of you:** anything in this slice's plan that departs from row 4a or misses a caller.

End with `CONSENSUS: yes` or `CONSENSUS: no, because …`.
