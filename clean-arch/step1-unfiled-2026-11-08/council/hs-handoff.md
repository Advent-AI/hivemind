# Council hs: review of the Step 4 design, version 27, one angle: state × event, and new path × old checks, against the code (fresh reviewer; read-only: do not edit files, run model calls or start runs)

You have not seen this work before. Review `clean-arch/step4-2026-11-10/DESIGN.md` (version 27) with its request
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

Twenty-one single reviews, four blind request audits and two rounds by angle are in
`clean-arch/step1-unfiled-2026-11-08/council/` (`gg-codex.md`, `gl-codex.md` … `hh-codex.md`; the audits `gw`, `gy`, `hi`, `hm`; the
rounds by angle `hj`/`hk`/`hl` on version 25 and `hn`/`ho`/`hp` on version 26). Version 27 claims to answer every finding of the
second round; the round log's last table (`clean-arch/step1-unfiled-2026-11-08/LOG.md`, the end of §69) lists each finding
and its change. This is the third round, with six reviewers new to the work, one angle each.
**You have one angle. Finish it.** Begin by checking that the findings of this angle's last review (`ho-codex.md`) are answered, then walk the angle again in full. If a part remains unread when you stop, list exactly which rows or sentences.
A stance settled in version 19 and accepted by the last four reviewers: the fixtures of `examples.json` are now stated to be check fixtures for the code (valid shapes, with the rows written), not answers claimed sound; the design says why (§5.2, §8).

## Your angle: two tables (design §7.1 state × event; §7.3 new path × old checks), against the code

Leave to the other five reviewers: the fixtures and checks, the request's sentences against their sources, the table of who
reads each written value (§5.4), Stage A's lines, and the counts stated from the practice readings.

Open the code each row names: `src/hivemind/views/judging.py`, `views/store.py`, `extraction.py` (`sift` and the checks it
calls), `model.py`, `clean-arch/e2e-2026-11-09/adapter.py` and `budget.py`.

1. **State × event (AGENTS §2, table 1).** For every state, walk every event it can meet: success, refusal, a refused resend, an
   external failure, a crash midway, work in flight when a run ends, a later day, a changed configuration, a corrected input,
   another writer, two scopes at once, the spending cap, a cached answer. Name every missing or wrong cell, and every cell whose
   "what is written" or date does not match the code it names.
2. **The spend ledger and the restart of Stage A's runner** (§8, "The cap" and "Across a stop"): is the total bounded by the cap
   in every interleaving of reserve, send, charge and process death you can construct? Give the interleaving if not.
3. **New path × old checks.** For every check `extraction.sift` applies to a production candidate: is it kept, replaced or
   dropped, and is the reason given true of the code? Name any old check with no row.
4. Could two engineers build different things from §7 and the ledger rules? Name each place.

## Deliver

First line: READY FOR THIS ANGLE, or NOT READY. A finding is serious when, left as it is, the build or Stage A could produce a
wrong ladder that goes unseen, a result that misstates what happened, or two different builds. Then the findings, most serious
first, each with its file and line and what a complete fix must contain; wording-level points in a short list at the end; then
one line saying what you walked in full and what, if anything, you did not reach. Under 1,000 words.
