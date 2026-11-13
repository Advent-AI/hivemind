# Council ia: review of the Step 4 design, version 28, one angle: Stage A: the lines, the accounting and the form (fresh reviewer; read-only: do not edit files, run model calls or start runs)

You have not seen this work before. Review `clean-arch/step4-2026-11-10/DESIGN.md` (version 28) with its request
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

Twenty-one single reviews, five blind request audits and three rounds by angle are in
`clean-arch/step1-unfiled-2026-11-08/council/` (`gg-codex.md`, `gl-codex.md` … `hh-codex.md`; the audits `gw`, `gy`, `hi`, `hm`, `hq`;
the rounds by angle `hj`/`hk`/`hl` on version 25, `hn`/`ho`/`hp` on version 26 and `hr`/`hs`/`ht`/`hu`/`hv` on version 27).
Version 28 claims to answer every finding of the third round; the round log's last table
(`clean-arch/step1-unfiled-2026-11-08/LOG.md`, the end of §69) lists each finding and its change. This is the fourth round, with
seven reviewers new to the work, one angle each.
**You have one angle. Finish it.** Begin by checking that the findings of this angle's last review (`hu-codex.md`) are answered, then walk the angle again in full. If a part remains unread when you stop, list exactly which rows or sentences.
A stance settled in version 19 and accepted by the last four reviewers: the fixtures of `examples.json` are now stated to be check fixtures for the code (valid shapes, with the rows written), not answers claimed sound; the design says why (§5.2, §8).

## Your angle: Stage A (design §8 from "Stage A" up to "Stage B"; `ladder/stage-a-reader-brief.md`)

Leave to the other six reviewers: the fixtures and checks, the request's sentences against their sources, the tables of §5.4
and §7, and the counts the design states from the practice readings (a sixth reviewer checks those against the stored answers).

1. **The six lines.** For each: can it fail? Can it pass for a wrong reason? Is the population it is read on defined, and what
   does it read when that population is empty or too small?
2. **The accounting table** and the rules under it (a mark's value, asking again, NOT MEASURED, a line measured only on
   something, a case and its files, the cap, three sends as three samples, the shares): is every outcome of a send, every
   reader field and every denominator defined, and consistent with the form on disk, field by field? Give any set of reader
   rows for which two people would compute different results.
3. **The form against the request.** For each thing the request tells the model to do or not to do, which mark fails when the
   model does not? Name any instruction no mark covers (W aside) and any mark the form defines differently from the design.
4. Does every statement of what Stage A shows keep to D400's limit (it does not compare the step with production)?

## Deliver

First line: READY FOR THIS ANGLE, or NOT READY. A finding is serious when, left as it is, the build or Stage A could produce a
wrong ladder that goes unseen, a result that misstates what happened, or two different builds. Then the findings, most serious
first, each with its file and line and what a complete fix must contain; wording-level points in a short list at the end; then
one line saying what you walked in full and what, if anything, you did not reach. Under 1,000 words.
