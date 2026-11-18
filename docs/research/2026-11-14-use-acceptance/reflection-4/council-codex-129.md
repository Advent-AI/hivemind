**Not yet.** The single view-vector read addresses my concern about a build changing that set mid-search, but the current dimension check still lets an invisible view affect the answer.

`fresh_vectors` iterates **all** views and takes the first usable vector’s length as the dimension for the rest. An unfinished or otherwise invisible view encountered first can therefore cause a visible view’s vector to be rejected, changing `missing_vectors` and the search mode. Restrict dimension selection and validation to the request’s visible candidates, and add a control with an invisible view carrying a different-length cached vector. [Current `fresh_vectors`](/Users/lchingen/hivemind/src/hivemind/search.py:122).

Two statements also need narrowing before the proof:

- A first-day-started service does not build an index, but it may use a **pre-existing matching vector in a shared index** when the day completes. It is lexical until restart only when at least one visible view lacks a match. Test both cases through API and MCP. [Contract](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md:110).
- A query cache key identifies the input and model; it does not by itself prove that a fresh provider response would be byte-identical to a cached vector. Say that a cache hit reuses the stored matching vector, and test the concurrency behavior without claiming identical provider outputs. [Query cache](/Users/lchingen/hivemind/src/hivemind/search.py:136).

CONSENSUS: no, because invisible views can still influence vector validation, and the first-day shared-cache behavior is stated too broadly.