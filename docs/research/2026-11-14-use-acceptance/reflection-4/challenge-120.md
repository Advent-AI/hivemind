# Round 121: the bound resolver's product-facing response and compatibility design (A1 withdrawn; refusal kept)

## The rule (row 3, unchanged in substance, now independent of whether partial rows exist)

- **On every store with a `days_completed` table:** an explicit upper bound later than the last completed day is refused, finished
  or not, partial rows or not. The same date gets the same treatment whenever it is asked.
- An omitted bound gives the last completed day, and a store with steps but no completed day is refused as its first day.
- A legacy ledger without the tables reads as today.
- **Ranges** get an explicit outcome, never an empty array:
  - `changes(since, to)`: a `since` on or after the resolved `to` is refused ("since is not before the last completed day"), as is
    an explicit `to` in the future;
  - `history(from, to)`: a `from` after the resolved `to` is refused the same way.

## The response, per channel

| Channel | First day not completed | Bound after the last completed day | Range start not before its end |
|---|---|---|---|
| API (`error_response`) | 503 `{"error": "the store's first day has not completed"}` | 409 `{"error": "day not completed", "requested": X, "last_completed_day": Y}` | 409, the same shape, naming both days |
| MCP tools | a tool error with the same text | a tool error with the same text | the same |
| The streamed Idea route | the status before any header | the same | — |

- The owner is two exceptions raised by `service.resolve_bound` (`FirstDayNotCompleted`, `BoundNotCompleted`), mapped once in the
  API's `error_response`. MCP raises them as tool errors, so no array response changes shape.

## Callers, from the code

- **The page sends only days from its own dataset:**
  - the library's day, `library.getDay()`, passed to `/ideas`;
  - the day the Idea answer returns, `card.idea.as_of`, passed to `/thesis-bundles`.
  - Both are on or before the served snapshot's last completed day, so the page is unaffected.
- **MCP clients and direct API users that pass a later date:**
  - on the running product's store, today they get the half-processed 2026-08-29 (99 evidence records, 117 links);
  - they would get an error naming 2026-08-28;
  - on a finished store, they would get the same error instead of today's identical answer.
  - This is the behaviour change. It is recorded for Alex's page.

## Not deployed

- The change is code with tests in the repository. No running service is restarted.
- D439 does not authorize deploying it. Its effect on the running product begins only when someone restarts the service, and that
  is on Alex's page.

**Asked of you:** any response shape, range or caller this misses, and whether the code may now be written, starting with the
resolver, its structural check and the tests for all four store states plus a copy of the served store's state.

End with `CONSENSUS: yes` or `CONSENSUS: no, because …`.
