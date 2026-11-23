# Round 123: your three points in row 3's product-facing contract

1. **Direct view visibility:** `bundle.view_bundle` and `bundle.not_judged`, called directly, refuse (404) a view not visible at the
   resolved day, as `_bundles` already skips it. Proof 2c′ makes a direct call for a view created after that day.
2. **The empty-store `None` path:**
   - My rule that helpers refuse `None` is withdrawn. Helpers receive their caller's resolved bound, `None` on an empty store as
     today, and behave as today.
   - Proof 2c compares each public function's actual output or error with the expected one: today's recorded output where the rule
     keeps it, the named refusal where it changes it. For example, `days()` on an empty store gives `[]`.
3. **Range-error ownership:** `service.resolve_range(conn, start, end, start_included)` resolves the end through `resolve_bound`,
   then raises `RangeNotOrdered(start, end)`. `error_response` maps all three exceptions. Row 3's earlier sentence now says a lower
   bound is checked only against its resolved upper bound.

End with `CONSENSUS: yes` (the code may be written, starting with the resolver and its check) or `CONSENSUS: no, because …`.
