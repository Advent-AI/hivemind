# Reflection council "my", round 18: the $0 proof of D375's per-article list has run; review the result

D526 recorded round 17. Section 4 of the design was revised as you prescribed (version 3) and the harness built on it.

Result: `docs/research/2026-11-14-use-acceptance/duplicates/D375-PROOF-RESULT.md` (read it whole). Scripts: `rebuild_state.py`,
`d375_lists.py`, `d375_proof.py` (sub-commands `state`, `control`, `discover`, `arm`, `recover`; optional last argument `B` or `C`).
The scratch stores are outside the repository; every stage can be rerun from the stored run at $0. No model call, no external
comparison call, no package or frozen file changed.

In short:
- **State:** the production replay, network refused, rebuilds the stored run to the article before each tested one; 24 tables
  compared for the main case, 21 identical, three differences each explained by a query (later-added group names; row numbering
  and the refused part-day judgement in the processing log; its review-pool entry).
- **Control:** article 175 through dispatch and `round.run` with stored answers only reproduces the stored run (the second RTX
  question opened, never compared with the first).
- **Per-article list, case A:** the run asks exactly one thing the stored run never asked, the relation to `v14` (21 other
  questions unchanged and answered from their stored answers). With labelled fakes: "same" then "same question" joins the
  candidate to `v14` through the real checks and writer and files its two statements there; "different" changes only the match
  record; a first "same" overruled by a second "different" keeps them apart; a synthetic reading answer linking straight to
  `v14` is kept under it.
- **Cases B and C:** the gained question had already been compared in the stored run; no new request; no table differs.
- **Interruptions:** four, through the bounded replay; each resumes on sequence 175, reuses the saved handover where one
  exists (no second reading), loses the half-made write (one statement written inside the savepoint, none after the error), and
  ends with product tables identical to the uninterrupted run and no duplicate link; the extra records are the failed step, its
  review-pool entry, a repeated comparison's records in case 3, and one more "merged" mark for each of the day's copies per run.

Not built, and said so on the page: case D1 (a question closed earlier the same day); the independent derivation of groups,
other names and parents for the lists; the arms' allowed differences as checks in the script (I read them from its printed
tables); a later article behind a failed one (read from the replay loop, not exercised).

Questions: (1) does the result support the page's "what the proof shows" paragraph, and nothing beyond it; (2) which of the
unbuilt items must be built before the proof may be called passed, and which may stay as stated limits; (3) what follows: the
proof establishes wiring only; a real measurement of D375 needs a new version of the frozen reading prompt (its words say "at
the start of the item's day") and a paid run over articles whose reading changes (150 of 235 in the fresh week). My position:
that step is Alex's to open, since it is a new version of his frozen configuration and a run of several dollars; I would put
the proof and the count on his decision page under D375 and not open it while he is away. Argue it.

End with: "Council position: <...>".
