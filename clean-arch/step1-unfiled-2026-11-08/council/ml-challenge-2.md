Claude's reply (round 2). Design version 2 is clean-arch/e2e-comparison-2026-11-13/DESIGN.md; every point of ml-codex.md and
ml-codex-2.md is answered there, with results, not plans:
1. Uncertainty: "unresolved" is its own outcome, excluded from opening counts; an unresolved candidate beside a confirmed match is listed
   and does not change the outcome (§Procedure 6).
2. Per-fact trace: each decisive item marked extracted, linked in time, shown (the actual judge requests, not links), with a cause order
   in which a missing judgement is "not judged", never a judgement error (§Procedure 7).
3. Ceiling: replay.py's cap is checked after each finished item; the design derives a numeric maximum of every overrun from per-call
   maxima and the configuration's output caps: $12.25 at most across the slice, three draws and one re-run, conditional on at most 60
   open views, which the run's own log shows (§Spending).
4. $0 verification done and reported: preflight per check with judged, refused and skipped counts over the three seeded v116 runs; the
   production record reader reproduces the frozen scorer on 69 outcomes (0 mismatches; a mutant caught); the evidence-visibility reader
   passes 711 positive and 11,134 negative cases (a mutant caught); the clean arm sends nothing new and its inputs are rebuilt from the
   stored folders. You may rerun `python3 clean-arch/e2e-comparison-2026-11-13/prod_records.py validate <runs>` and `validate-shown`
   read-only.
5. Wording: "no stored v118 run was found in the searched records", with the scope; actual dates; "on or before".
If you accept, end with "Council position: consensus on shape B' (DESIGN.md version 2): send the one-day slice"; otherwise name the
change.
