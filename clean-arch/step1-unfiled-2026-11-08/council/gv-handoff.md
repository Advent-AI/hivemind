# Council gv: review of the Step 4 design, version 13 (fresh reviewer; read-only: do not edit files, run model calls or start runs)

You have not seen this work before. Review `clean-arch/step4-2026-11-10/DESIGN.md` (version 13) with its request
`clean-arch/step4-2026-11-10/ladder/candidate-system.txt`, schema `candidate-schema.json` and worked examples `examples.json`, as a
design that must be READY before any code is written. Read `AGENTS.md` first (§1, §2, §6 and §7 govern a design, a prompt and a
test). Open the code and the data behind every claim you rely on.

## What is settled, do not reopen

- Alex decided the two product choices on 2026-11-10: D397 (one judged question per thesis; other parts shown as not judged) and
  D398 (the ladder step carries D186 in full), `docs/DECISIONS-log.md`. The items under "Behaviour this design takes from production"
  in §4 are marked there as reported to him or still to report.
- Eleven earlier reviews are in `clean-arch/step1-unfiled-2026-11-08/council/` (`gg-codex.md`, `gl-codex.md` … `gu-codex.md`).
  Version 13 claims to answer every finding of the last (`gu-codex.md`), in part by a change of the test: Stage A sends no control
  arm; its reference is a $0 reading of the 36 ladders production wrote (`clean-arch/step4-2026-11-10/reference/`). Three $0 readings
  with their forms, packets, keys and scores are in `dryrun/`, `dryrun2/` and `reference/`.

## Angles (answer each)

1. **gu's six findings.** Is each answered in version 13? Quote what is still missing.
2. **Dropping the control arm.** Is the reasoning sound under AGENTS §7.1 to §7.3 (a control, the reference system, what a send
   must decide)? What can Stage A no longer conclude, and does the design claim it anyway?
3. **The contract (§5, the schema, the examples).** Walk the examples through the schema, checks 1 to 8 and the label and number
   rules; say where the written rows in `examples.json` differ from what the rules produce. Give any answer that passes every
   check and is wrong in a way no reader mark of §5.3 would catch.
4. **The request against its sources (AGENTS §6),** sentence by sentence against the table in §5.2: consistent, wider, narrower,
   contradicts, or no source. Does the request ask for anything a check refuses, or a check refuse what the request allows?
5. **State × event (§7.1), value × reader (§5.4), new path × old checks (§7.3).** Name anything still missing or wrong.
6. **The test (§8).** Can Stage A and Stage B each fail, and can each be passed for the wrong reason? Are the outcomes, the
   denominators and the "right" measure complete and consistent with the forms on disk (`dryrun/reader-brief.md`,
   `dryrun2/reader-brief-a.md`, `dryrun2/reader-brief-b4.md`)? Are the claims made from the three $0 readings supported by their
   score files and reader answers?
7. **Could two engineers build different things from §5 and §6?** Name each place.

Out of scope: the frozen ruler, the frozen production prompts and judge (a defect in them is a finding, never an edit), c8, Step 2
and Step 3, `clean-arch/step2-validation-2026-11-07/LOG.md`, `reports/step2-*`, the frontend.

## Deliver

First line: READY, READY WITH CHANGES (name them; none may be a design decision), or NOT READY. Then the findings, most serious
first, each with its file and line and what a complete fix must contain; wording-level points in a short list at the end. Under
1,300 words.
