# Council R, round 6: version 3 of the design and the revised test plan

Your round 5 (`codex-r5.md`, NOT READY) is answered in `DESIGN.md` (version 3; §10 maps each finding) and `TEST-PLAN.md`. In short:
sign questions keep the candidate as the shared state, two builders name who reads whom; the graph check runs on the whole proposed
set plus every stored row, and a store holding an unbound waiting row is refused under `jev-links`; the archive is one writable copy
per sequence with the v9 and v14 judge rows retired through `Archive.retire`, proved at $0; the selection is a new table
`link_selections`, not a `match_records` row; `proposed_links=None` keyword-only; reversed stored successors, event measures and
typed intervals defined; restart, second-writer, version-switch and judging-eligibility rows added; the dry run checks queueing both
ways and that the control invents no 07-11 Data Center judgement; extra links registered (a reader outside v9/v14 stops the sequence,
not comparable); the budget transport used as it behaves, the shared ledger read after a stop.

Check each answer against the code it names. End with READY TO BUILD, or NOT READY with the exact changes. Findings that do not block
the build (wording, tests to add) are listed as such.
