# Council ig: review of the Step 4 design, version 29, one angle: value × reader: who reads each value the step writes (fresh reviewer; read-only: do not edit files, run model calls or start runs)

You have not seen this work before. Review `clean-arch/step4-2026-11-10/DESIGN.md` (version 29) with its request
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

Twenty-one single reviews, six blind request audits and four rounds by angle are in
`clean-arch/step1-unfiled-2026-11-08/council/` (`gg-codex.md`, `gl-codex.md` … `hh-codex.md`; the audits `gw`, `gy`, `hi`, `hm`, `hq`, `hw`;
the rounds by angle on versions 25 to 28, the last being `hx` contract, `hy` state table and old checks, `hz` value × reader,
`ia` Stage A, `ib` practice readings, `ic` the stored-data counts of §2). Version 29 claims to answer every finding of that
round; the round log's last table (`clean-arch/step1-unfiled-2026-11-08/LOG.md`, the end of §69) lists each finding and its
change. This is the fifth round, with seven reviewers new to the work, one angle each.
**You have one angle. Finish it.** Begin by checking that the findings of this angle's last review (`hz-codex.md`) are answered, then
walk the angle again in full. If a part of your own angle remains unread when you stop, list exactly which rows or sentences.
Your verdict is for your angle alone. Material the other reviewers hold is not something you failed to reach: do not withhold
READY FOR THIS ANGLE because of it. Withhold it only for a finding in your angle, or for a part of your own angle you did not read.
A stance settled in version 19 and accepted by the last four reviewers: the fixtures of `examples.json` are now stated to be check fixtures for the code (valid shapes, with the rows written), not answers claimed sound; the design says why (§5.2, §8).

## Your angle: value × reader (design §5.4, the table "value | written to | readers on this path | readers elsewhere" and the field-by-field write tables above it), against the code

Leave to the other six reviewers: the fixtures and checks, the request's sentences against their sources, the state table and
the old-checks table, Stage A's lines, and the counts stated from the practice readings.

For **every** value the step writes (each argument of `store.create_view`, each rung field, the open switch, the search text,
each column of `clean_ladders`), search the field's name across `src/hivemind/` and `clean-arch/e2e-2026-11-09/adapter.py`:

1. Is every reader on this path (the replay: the adapter and production's judge, `views/judging.py`, `views/store.py`,
   `views/writing.py`) listed, and is what the table says each does with the value true of the code? Cite file and line.
2. Does any reader on this path need a value the step does not write, or a form of it the step does not produce (a type, a
   null, an id format, an order of rungs)? In particular: view ids, `object_kind`, `kind`, `year` for an event, rung `lo`/`hi`
   for a ladder that is not a figure, `created_from_input`, the open switch.
3. For the readers the table lists as "elsewhere, not run on this path": is each truly not run on the replay path the design
   describes?
4. Name any value with no row, and any row whose reader does not exist.

The last reviewer of this angle finished the readers on the replay path and did not finish the column "readers elsewhere, not
run on this path". Start with that column: for each row, search `src/hivemind/` for the field and say whether each reader it
names exists, reads that field, and is truly not run by the replay the design describes. Then the path's own readers.

List every field you searched, so the walk can be seen to be whole.

## Deliver

First line: READY FOR THIS ANGLE, or NOT READY. A finding is serious when, left as it is, the build or Stage A could produce a
wrong ladder that goes unseen, a result that misstates what happened, or two different builds. Then the findings, most serious
first, each with its file and line and what a complete fix must contain; wording-level points in a short list at the end; then
one line saying what you walked in full and what, if anything, you did not reach. Under 1,000 words.
