# Council hx: review of the Step 4 design, version 28, one angle: the contract: fixtures, checks and the complete writes (fresh reviewer; read-only: do not edit files, run model calls or start runs)

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
**You have one angle. Finish it.** Begin by checking that the findings of this angle's last review (`hr-codex.md`) are answered, then walk the angle again in full. If a part remains unread when you stop, list exactly which rows or sentences.
A stance settled in version 19 and accepted by the last four reviewers: the fixtures of `examples.json` are now stated to be check fixtures for the code (valid shapes, with the rows written), not answers claimed sound; the design says why (§5.2, §8).

## Your angle: the contract (design §5.3; the field-by-field writes at the head of §5.4; `ladder/examples.json`; `ladder/candidate-schema.json`; `ladder/number_rule_check.py`)

Leave to the other six reviewers: the request's sentences against their sources, the state table and the old-checks table, the
table of who reads each written value, Stage A's lines, and the counts stated from the practice readings.

1. Walk **each of the eight fixtures** of `examples.json` through the schema (with production's validator, `model.check_schema`
   in `src/hivemind/model.py`), checks 1 to 8 and the label and number rules of check 7. For each: passes or is refused, by which
   check, and whether its `written` projection is what the rules and the field-by-field tables of §5.4 produce.
2. For each of checks 1 to 8: is what it relies on really enforced where the design says (the validator, the production code it
   names, or the check itself)? Open the code it names. Name any rule enforced nowhere, and any answer that would stop the run
   where the design says it is refused and resent.
3. Give any answer that passes every check and is wrong in a way none of the reader marks listed at the end of §5.3 would catch.
4. Could two engineers build different things from §5.3 and the write tables? Name each place.

## Deliver

First line: READY FOR THIS ANGLE, or NOT READY. A finding is serious when, left as it is, the build or Stage A could produce a
wrong ladder that goes unseen, a result that misstates what happened, or two different builds. Then the findings, most serious
first, each with its file and line and what a complete fix must contain; wording-level points in a short list at the end; then
one line saying what you walked in full and what, if anything, you did not reach. Under 1,000 words.
