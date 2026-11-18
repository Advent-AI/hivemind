# Round 122: row 3's product-facing contract (`live-service/OPERATING-CONTRACT.md`, the new section before "Not covered")

1. **`view_bundle` and every direct path:**
   - Every public function with a date resolves it at entry through `resolve_bound`:
     - `service`: 8 functions;
     - `bundle`: `not_judged`, `view_bundle`, `days`, `thesis_bundles`, `library`;
     - `idea.read_idea` and `search.search`.
   - Nested calls pass resolved bounds, and the resolver is idempotent. Internal helpers refuse `None`.
   - The structural check reads every function with an `as_of` or `to_day` parameter and fails any that neither calls the resolver
     nor is a listed helper. It has its own mutant.
   - Proof 2c calls each public function directly, including `view_bundle` with no date as `mock_data.py` does, on four store
     states plus a copy of the served store's state.
2. **The page's fallback:**
   - When the live library read fails, the page keeps its embedded day, which can be later than the service's last completed day,
     so `/ideas` is refused with 409 and the page shows its existing Idea error.
   - This is documented and tested (proof 2f), not claimed impossible.
3. **The streamed route in one transaction:** connections opened, the transaction begun and the bound resolved, then the headers,
   then the Idea work in the same transaction. A refusal is a normal status and body before any header. The transaction lasts the
   request (model calls included), within row 5. Proof 2e covers both refusals before headers, and a writer committing during an
   Idea request.
4. **Errors and the empty store:**
   - `error_response` returns `(status, payload)`, with the two structured payloads specified (409 with requested and last completed
     day; 409 for a range start with both bounds; 503 for the first day). Every other error keeps `{"error": message}`.
   - `days_completed` present with no steps and no completed day reads as today.
   - Range equality: refused for `changes`, which excludes its start; allowed for `history`, which includes it (proof 2d).

End with `CONSENSUS: yes` (the code may be written, starting with the resolver and its check) or `CONSENSUS: no, because …`.
