# Council hh: review of the Step 4 design, version 25: the ladder step and Stage A (fresh reviewer; read-only: do not edit files, run model calls or start runs)

You have not seen this work before. Review `clean-arch/step4-2026-11-10/DESIGN.md` (version 25) with its request
`clean-arch/step4-2026-11-10/ladder/candidate-system.txt`, schema `candidate-schema.json`, check fixtures `examples.json` and the
Stage A reading form `stage-a-reader-brief.md`, as a design that must be READY before any code is written. Read `AGENTS.md` first
(§1, §2, §6 and §7 govern a design, a prompt and a test). Open the code and the data behind every claim you rely on.

## Scope

- **In scope:** the ladder step (§5 to §7 of the design), the request, the schema, the fixtures, and Stage A of the test (§8 up to
  "Stage B"), with the $0 readings it rests on (`dryrun/`, `dryrun2/` packet A, `dryrun3/` to `dryrun8/`, `reference/`).
- **Out of scope:** Stage B. The design says it is an outline that gets its own review and Alex's word before any Stage B send. Do
  not report findings on Stage B, its form or its lines.
- Also out of scope: the frozen ruler, the frozen production prompts and judge, c8, Step 2 and Step 3,
  `clean-arch/step2-validation-2026-11-07/LOG.md`, `reports/step2-*`, the frontend.

## What is settled, do not reopen (Alex's decisions of 2026-11-10, `docs/DECISIONS-log.md`)

- D397: one judged question per thesis; every other part of its wording shown as not judged.
- D398: the ladder step carries D186 in full (the reference; the favourable end; labels by code).
- D399: the request teaches how to build an event's five states (the construction and the merger example).
- D400: Stage A sends the candidate only and is read against six fixed lines, with no paid control arm; an exception he made to
  AGENTS §7.3. Every report says Stage A does not compare the step with production.
- D401: after a review that finds nothing serious, the step is built and Stage A sent, capped at $3.
- The items under "Behaviour this design takes from production" in §4 were reported to him.

Twenty earlier reviews and two blind request audits are in `clean-arch/step1-unfiled-2026-11-08/council/` (`gg-codex.md`,
`gl-codex.md` … `hg-codex.md`; `gw-audit-codex.md`, `gy-audit-codex.md`). Version 25 claims to answer every finding of the last
(`hg-codex.md`: the count of five, the text and cost of each answer, the duplicate claim). Version 24 restated two parts as one
rule each, because four reviews in a row had found new corners in them: the number rule (§5.3 check 4, with
`ladder/number_rule_check.py`) and Stage A's accounting (the table under "The accounting"); `hg` found nothing in either.
A stance settled in version 19 and accepted by the last four reviewers: the fixtures of `examples.json` are now stated to be check fixtures for the code (valid shapes, with the rows written), not answers claimed sound; the design says why (§5.2, §8).

## Angles (answer each, in scope only)

1. **hg's findings.** Is each answered? Quote what is still missing.
2. **The contract.** Walk every fixture of `examples.json` through the schema, checks 1 to 8 and the label and number rules. Say
   where a written row differs from what the rules produce, and whether treating them as check fixtures leaves the build without a test it needs. Give any answer that
   passes every check and is wrong in a way no reader mark of §5.3 would catch.
3. **The request against its sources (AGENTS §6),** sentence by sentence against the table in §5.2: consistent, wider, narrower,
   contradicts, or no source. Does the request ask for anything a check refuses, or a check refuse what the request allows? Does
   the closing check repeat only rules stated above it? Is any sentence or in-text example fitted to the covered company or a test
   article?
4. **State × event (§7.1), value × reader (§5.4), new path × old checks (§7.3).** Name anything missing or wrong.
5. **Stage A.** Can it fail each of its six lines? Can it pass for a wrong reason? Are the outcomes of a send, the denominators,
   the "right" measure and the NOT MEASURED rules complete and consistent with the form on disk? Are the claims made from the $0
   readings supported by their score files and reader answers?
6. **Could two engineers build different things from §5 to §7 and Stage A?** Name each place.

## Deliver

First line: READY, READY WITH CHANGES (name them; none may be a design decision), or NOT READY. A finding is serious when, left
as it is, the build or Stage A could produce a wrong ladder that goes unseen, a result that misstates what happened, or two
different builds. Then the findings, most serious first, each with its file and line and what a complete fix must contain;
wording-level points in a short list at the end. Under 1,300 words.
