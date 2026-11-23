# Council round 53: check the round-52 revision of the v13s small format, before code

You are an independent read-only reviewer. **The scope is binding (Alex, D737):** report a finding only when it does one of these:
- (a) lets one of the five defects through the rules as written: a number misread, wrong arithmetic, a part above its whole or
  added into it, two forecasts of one quarter, an own estimate passed off as the market's;
- (b) breaks structure;
- (c) refuses a right answer;
- (d) states a rule differently from how code is to enforce it;
- (e) makes the blind test unable to decide.

A wrong answer outside the five defects is a reader's matter, not a finding. Code cannot see inside an estimate's judgement. Under
D737, an estimate is recorded and shown to readers, and the readers mark the five defects on every reply.

**The design:** `docs/research/2026-11-22-number-answers/SMALL-DESIGN.md`. Its §2 and §3 carry "[52]" revisions answering round 52
(`codex-r52.md`, same folder). Read the revision against round 52's findings and against the harness code (`paid_gate.py`,
`render_v13.py`, `calc_check.py`, `paid_rehearsal.py`).

## Questions

1. **Round 52's findings.** For each, does the [52] revision close it within scope? Quote the revised sentence. Name any finding left
   open.
2. **New defects from the revision.** Does the revision create a new (a)–(e) issue? Look especially at:
   - S4's "same figure" rule against legitimate range and scenario-free calculations in the six registered cases;
   - S8's "uses" lineage against the remainder and the share operation;
   - S6's requirement that the outcome be own (computed or estimate, basis forecast);
   - S3's lowest-versus-highest comparison on recomputed values.
3. **Consistency.** Do §2 [52], the [52] descriptions in §3, the operation units and the header text say the same thing?
4. **Ready?** Can implementation start, with the end-to-end rehearsal (A4) as the decisive $0 check? Answer "ready" or list the
   blocking items.

Report findings ranked by severity, tagged (a)–(e), with file and line. Out of scope: the frozen ruler, `poc-v118`, D725's lines,
D731's harness rules.
