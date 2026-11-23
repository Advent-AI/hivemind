# Round 22: the closing design you asked for, and a production defect found and fixed on the way. Verify both.

1. **Production defect, fixed** (`src/hivemind/replay.py`, the line completing the day; test
   `tests/test_closing_on_a_day_without_items.py` through `replay.run`): on a day without items a closing takes its own sequence
   (`pull.closing_sequence`), and the day was completed at the sequence before it, so the next day's items were shown the closed
   question as open (`store.views_open_at_day_start`, D251). The test failed on the old line at its decisive assertion
   (`['v1'] == []`) and passes with the fix (the day completed at `store.next_sequence(conn) - 1` after the closing); the touched
   suites pass (12). Census on stored data: 5 closings in 139 stores, none on a day without items (0 of 5). No freeze listing covers
   `replay.py` or `pull.py` (searched every `*.sha256` and the frozen tests).
2. **The closing design** (`carried-run/CLOSING-DESIGN.md`): state × event, value × reader, new path × old checks, prior decisions,
   what is not covered (Step 1's library does not learn closings: such facts get no home, counted), and a $0 proof plan with mutants
   and a decisive replay through the real loop to 2027-04-02 with no further articles.

Attack: the production fix (any reader of `days_completed.seq` that a later completed sequence changes; the parallel day path);
each cell of the design (in particular dropping links to closed questions against production's behaviour; walking calendar days;
the guard as an invariant). End with `CONSENSUS: yes` (keep the fix; build the design as written and prove it) or `CONSENSUS: no,
because …`.
