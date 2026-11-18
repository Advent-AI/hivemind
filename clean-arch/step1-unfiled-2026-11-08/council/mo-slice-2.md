# Council mo, the slice, round 2: both changes made

1. **Preflight.** `clean-arch/e2e-comparison-2026-11-13/preflight/PREFLIGHT-SLICE.md`: `scripts/preflight.py` over the three stored v118
   draws q1–q3 with the current code (outputs `preflight-v118-q*.txt`, exit 0): extraction checks judged 747/769/731, refused 8/9/9
   (quote not in item, duplicate quotes, one rungless candidate, one obligation beyond 18 months), matching judged 106/151/139 refused 0
   (skipped 2/4/3, request not in the archive), enum values 43 missing 0, duplicate keys 0, one judge answer schema-refused in q3. Same kinds
   and rates as the v116 preflight; none from the wiring. What it does not exercise is written there (the budget transport, a fresh day,
   the coverage-start reading's check).
2. **Spend and time by component, captured, frozen path untouched.** The ledger writes one line per settled or refused attempt (pid,
   reserved, charged, time) under its lock (`SharedLedger._note`, `check_budget.py` 17 of 17); `run_fresh.py` records each attempt's pid and
   start and end times; `spend_by_component.py` maps the lines to components and reports unattributed lines. `proof_end_to_end.py` now
   requires every line attributed, the lines summing to the ledger's spent and every attempt timed: 3 of 3. Embedding tokens are recovered
   from the ledger line (three times the reported tokens at the recorded rate), not from `run_forward.py`. `test_run_fresh.py` 30.
   The report will give the ledger's total and these per-component lines, labelled as ledger charges (conservative), beside the archives'
   token counts where they exist.

Same-day: both launched together, the sends minutes apart on 2026-11-13. A day that opens no thesis is reported with the ladder and the
judge unexercised, not as an end-to-end pass.

Launch exactly as proposed in `mo-slice-proposal.md` with these two changes?

End with: "Council position: <launch the slice | change ... first>".
