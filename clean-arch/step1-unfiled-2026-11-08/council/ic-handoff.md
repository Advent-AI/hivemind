# Council ic: review of the Step 4 design, version 28, one angle: the evidence of §2: counts from the stored runs and archives (fresh reviewer; read-only: do not edit files, run model calls or start runs)

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
`clean-arch/step1-unfiled-2026-11-08/council/`; the last review of the evidence is `hv-codex.md`, on version 27. Version 28 claims
to answer its findings (the round log's last table, `clean-arch/step1-unfiled-2026-11-08/LOG.md`, the end of §69). This is the
fourth round, with seven reviewers new to the work, one angle each. **You have one angle. Finish it.** If a part remains unread
when you stop, list exactly which rows or sentences.
A stance settled in version 19 and accepted by the last four reviewers: the fixtures of `examples.json` are now stated to be check fixtures for the code (valid shapes, with the rows written), not answers claimed sound; the design says why (§5.2, §8).

## Your angle: the stored-data findings of §2 (design §2.1 to §2.4), against the files and archives they come from

Leave to the other six reviewers: the fixtures and checks, the request's sentences, the tables, Stage A's lines, and the
practice readings of §8 (a sixth reviewer has those).

No earlier reviewer finished these: the counts attributed to the council's independent investigation (`gi-codex.md`) in §2.1,
every archive claim of §2.3 (the judge's refusals) and §2.4 (the mapping facts), and the zero counts of the production tally in
§2.2. Read-only: you may run the scripts under `clean-arch/step4-2026-11-10/census/` and read the stored runs they name
(`sqlite3` in read-only mode on stored, finished runs; never a live run), and you may write nothing.

1. §2.1: recompute every count from `census/packet.json`, `census/reader-codex.jsonl`, `census/reader-claude.jsonl` and
   `census/tally.py`; for the counts attributed to `gi-codex.md`, say whether that file states them and whether the packet
   supports them.
2. §2.2: recompute the counts from `census/production_ladders.py` and its output, the zero counts included.
3. §2.3 and §2.4: for each number and each fact about the code, open the archive, run folder or source line it rests on and say
   whether it holds. Cite the file and the query or line.
4. List each count you checked and its result, so the walk can be seen to be whole; name any you could not reach and why.

## Deliver

First line: READY FOR THIS ANGLE, or NOT READY. A finding is serious when, left as it is, the build or Stage A could produce a
wrong ladder that goes unseen, a result that misstates what happened, or two different builds. Then the findings, most serious
first, each with its file and line and what a complete fix must contain; wording-level points in a short list at the end; then
one line saying what you walked in full and what, if anything, you did not reach. Under 1,000 words.
