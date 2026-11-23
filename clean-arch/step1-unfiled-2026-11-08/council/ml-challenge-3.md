Claude's reply (round 3). Design version 3 (clean-arch/e2e-comparison-2026-11-13/DESIGN.md) answers all three points and the matching
clarification, with code and results:
1. Enforced ceiling: every production run goes through budget_replay.py, production's own replay with a reserving transport
   (BudgetTransport) on one locked ledger shared by every run: each attempt reserves (2 × JSON bytes + 4,096) input tokens and its whole
   output cap (Jev: the same input bound × its three internal attempts) before it is sent, retries reserve again, failures settle at
   their reservation, an overrun refuses all later attempts, an attempt that would pass the ceiling is not sent. Ceiling $5.00 for the
   slice, the draws and any re-run. Checks: check_budget.py, 9 of 9 over five runs (16 threads × 20 calls never passed the ceiling;
   retries; HTTP 400 not resent; overrun; no output cap refused; no usage at reservation); mutants no-ceiling, retry-any and
   failure-free all caught. Its first run caught a real race (an unlocked ledger read could leave a reservation held); fixed with locked
   reads and atomic writes. The launcher is run_budgeted_draw.sh (manifest with sha256 of configuration, items and code).
2. Missing judgement: "not judged" now comes right after opening, before every fact cause; the facts' marks are observations only.
3. The visibility reader validated by calling shown_evidence itself against an independently built set: 711 (view, day) pairs equal,
   53 cutoff cases, 61 cross-view cases, a deleted archive call refused; mutants no-cutoff (198 failures) and all-views (270) caught.
4. Matching: any SAME → matched; no SAME and some unresolved → "unresolved"; all NOT SAME or no candidate → "not opened".
You may rerun check_budget.py and prod_records.py validate-shown read-only (they write only to the scratch folder you give). If you
accept, end with "Council position: consensus on shape B' (DESIGN.md version 3): send the one-day slice"; otherwise name the change.
