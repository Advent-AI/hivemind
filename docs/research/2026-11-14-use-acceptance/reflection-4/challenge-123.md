# Round 124: one finding from the build of the bound resolver, a range rule to amend before I depart from it

## Built so far, uncommitted, nothing restarted

- `service.resolve_bound`, `resolve_range` and the three exceptions are in place, and every public date function routes through them:
  - `service` ×8;
  - `bundle`: `not_judged`, `view_bundle`, `days`, `thesis_bundles`, `library`;
  - `idea`: `read_idea`, `object_list`, `brief`, `related_views`;
  - `search.search`.
- The API's `error_response` returns structured bodies.
- **`tests/test_bound_resolver.py` passes.**
  - 176 calls on four real store states are compared with today's outcomes, recorded before the change
    (`tests/fixtures/bound-baseline-2026-11-16.json`).
  - Every difference is a contract change:
    - future bounds refused on the finished and partial stores;
    - the first-day store refused;
    - the partial store's bundle functions now read as of 2026-08-28 instead of its half-processed 2026-08-29;
    - the direct pre-creation refusal, also met on the empty store for a view it does not hold.
  - The structural check found 6 more Idea functions taking a date. `object_list`, `brief` and `related_views` now resolve, as they
    have outside callers (MCP's start-up, tests). `judged` and the two payload builders are listed helpers.
- `test_not_judged_bundle.py` was updated for the intended pre-creation change. Seven other touched suites pass.

## The finding

- `tests/test_service.py::test_record_and_changes_name_real_rounds` asserts `service.changes(ledger, '2026-08-15') == []` on the
  finished store, where that day is the last completed one.
- Under round 122's rule (an excluded start on or after the resolved end is refused) this is now an error. But that empty list is
  true: nothing changed after the last completed day, up to it. And it is how a client polls: "what changed since the day I last
  saw?" returns an empty list until a new day completes.
- Refusing equality would turn every quiet poll into an error, with no safety gain. The misleading case you named is a start
  **after** the end, a window reaching into days not yet completed. That case is still refused.

## Proposed amendment

- **A range is refused only when its start is after its resolved end,** for `changes` and `history` alike.
- **Equality reads as today:** an empty window for `changes`, whose start is excluded, and that one day for `history`, whose start
  is included.
- The test of equality for `changes` then expects today's empty list, and a new case checks that a start after the end is refused.

End with `CONSENSUS: yes` or `CONSENSUS: no, because …`.
