# Council mx: a deep review of the traces, then one next step to try (independent investigation; read-only)

You are Codex, the second member of a council with Claude Code. Read-only: do not edit files, run model calls or start runs.
Investigate independently; Claude is reading the same material in parallel and you will challenge each other afterwards. Read the record
cold and do not assume earlier conclusions are right, Claude's included.

## Objective
Alex, 2026-11-14 (D492 in `docs/DECISIONS-log.md`): "跑council run review of the traces deeply then determine next step to try improving, don’t go in
circles or make same mistake learn from it". The product goal is `clean-arch/PRD.md` §1: a research brain that follows an investment
analyst's process: questions worth tracking, the evidence filed under them, and judgements a reader can trace to that evidence. The
standing goal of this path is to move toward production with small steps that each decide something.

## Where things stand (check every line against the record)
- Two systems: production as it runs (frozen, `poc/config/poc-v118.json`) and the clean path (Step 1 request c8, `clean-arch/PRD.md` §12;
  Step 2 and grouping frozen; the answer-options step and the frozen judge).
- The fresh week 2026-09-22..28, one draw a system (D489): `docs/research/2026-11-14-use-acceptance/week/WEEK-RESULT.md`. Stored runs:
  `poc/data/clean-lean-week-2026-11-14/week-r2/c1` (clean: `step1/trace.sqlite` holds each article's request, raw answer with its reasoning,
  result and library state before and after; `step2/library.json`; `judge/draw-c1/archive.sqlite` and `views.sqlite`) and
  `poc/data/clean-lean-week-2026-11-14/week/p1/prod` (production: `views.sqlite` with views, evidence, links, handovers and their drops,
  judgements; `archive.sqlite` with every model call).
- Alex then opened a test of revenue and margin questions on the clean path (D490); its arm c20 failed its probe on a line written
  beforehand and was stopped (D491): `docs/research/2026-11-14-use-acceptance/main-numbers/PROBE-DESIGN.md`, `RESULT.md`,
  `answers-listing-stage1.txt`; raw sends in `poc/data/clean-main-numbers-probe-2026-11-14/stage1/`.
- The round logs: `docs/research/2026-11-14-use-acceptance/LEAN-LOG.md` (this path, with its lessons); the long history of Step 1 changes in
  `clean-arch/step1-unfiled-2026-11-08/LOG.md` (sections 85 to 92 for the last stretch; D439 to D482 in `docs/DECISIONS-log.md`: about ten
  measured changes to the Step 1 request, none adopted); the earlier reflection D483; the choices of D477
  (`clean-arch/e2e-comparison-2026-11-13/CHOICES-FOR-ALEX-2026-11-13.md`).

## Constraints
- The frozen ruler never changes (AGENTS.md §7.1). Production's pieces and the clean path's frozen pieces change only as a new version;
  Alex's decisions stand (D382 and D384 among them) unless he changes them; a choice that changes what the product does is his.
- Nothing is pushed or committed; no spending cap is raised; spend so far on this path $5.71.
- Out of scope: the network fix (D488), wording of documents, anything in modules this path has not touched.

## Deliver (read the traces themselves, not only the result pages; cite files, steps and ids)
1. **Where a reader loses value in each system on this week,** at the level of what the reader ends with (questions, the evidence under
   them, the judgements): rank the losses by product impact, with counts from the stored runs and at least three traced examples each
   (an article, what each system did with it, what a reader needed). Include what happens to statements that end with no question
   (the clean path keeps them unread; production throws them away or files them under a revenue question): read a sample and say what
   they are.
2. **The pattern in what was tried,** across D439 to D491: what kind of change was tried each time, why each failed, and what the failures
   share. Name the mistakes in method that were repeated (Claude's, the council's), with the instance of each.
3. **Conclusions weaker than they look** in WEEK-RESULT.md, RESULT.md and LEAN-LOG.md.
4. **Next step candidates, ranked by expected effect on the reader's loss in (1),** at least two that are not another sentence in the
   Step 1 request (structure, payload, pipeline, the judge's inputs, what the product shows, or stopping a line). For each: the
   mechanism, what it could break, its fit with the constraints and with Alex's decisions, and the cheapest decisive check on stored data.
5. **One recommendation and one test,** with the result that would refute it written out.
Facts and hypotheses kept apart. Under 1,500 words.
