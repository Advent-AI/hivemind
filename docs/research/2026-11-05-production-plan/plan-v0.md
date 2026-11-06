# From the split prototype to production: draft plan v0 (Claude, for joint review with Codex)

Alex, 2026-11-05, after the first-100 results: "重跑之前你和codex subagent 需要一起我多轮的讨论和看trace，错误来达到一致下一步应该怎么改进。我需要能把这个推上线变成production，所以按照生产标准来做工作，深度的讨论直到你们彼此盲点都解决统一改动策略和计划".

This draft is the starting point of the review rounds, not a decision. Every claim cites a file; every proposal names its source in the
standard, a decision or a PRD, or is marked as a proposal for Alex. Nothing is re-run until the plan is agreed.

## 0. Where we are (evidence)

- Prototype: `docs/research/2026-11-05-seven-day-request/split_seven_day_poc.py` with `split-v2-design.md` (classes, mechanisms, changes,
  proofs) and `split-v2-predictions.md` (predictions written before each run). Configuration `poc/config/poc-split-v2.json`.
- Runs on the same first 100 rows (76 article items): baseline `poc/data/split-fresh-seven-day-matching-v4-2026-11-05/` (rows 1–100), then
  `split-v2-first100-…`, `split-v2-final-first100-…`, `split-v2-confirm-first100-…`. Readable per-item traces: `traces/<run>/<seq>.json`
  (article, A answer, record preparation, B answer, handover, matching decisions with reasons, questions written with rungs and judgements);
  `traces/<run>/_index.json`, `_ledger.json`.
- Blind reading (Codex, keys withheld): `docs/research/2026-11-05-seven-day-request/blind-*-2026-11-05/` (packets and verdicts); summary in
  `split-v2-design.md` §4 and §6. Headline: questions the standard would not open 24 of 35 → 3 of 22 (confirmation run); opening passages
  helpful 8–10 of 30 → 18 of 30; existing-question passages 21–23 of 30 → 16–22 of 30 (B unchanged).
- Known residuals (`split-v2-design.md` §6): a derived share no public material reports opens each run; one shared quantity filed under a new
  subject; B's fallback (D273, kept by D361) parks weak links under company-wide revenue questions, more of them as more total-revenue
  questions open.

## 1. What "production" requires (AGENTS §2–§5, §7.1, §11; D274, D354, D359, D375)

1. **One code path.** The split lives in `src/hivemind` (not in a research script importing research modules: `existing_path`,
   `simple_new_question_poc`, `run_structure_v2`, `b_arm`), chosen by configuration, run by `scripts/replay.py` and the service; the
   research runner retires or becomes a thin caller.
2. **Versioned prompts and schemas** in `src/hivemind/prompts` (A, B, record preparation, collision), named by the configuration; once
   accepted, frozen by tests like `tests/test_frozen_extraction_prompt.py`. D359: the code builds only frozen versions; a new version exists
   only when Alex opens it, measured against the frozen production version.
3. **Per-item latest library (D375) inside the production day runner.** `parallel_day` (D183) prepares up to 16 extraction requests ahead
   and validates them at each item's turn. With every open question shown to A and B, any question written by an earlier item changes the
   next item's request. Options to decide: sequential items (A and B in parallel per item; about 20 s an item measured), or speculative
   preparation with re-preparation when the snapshot changed (cost and wall-clock measured on the stored runs).
4. **Identity and subjects as data.** Research subjects created by the split (`research:<hash>` in the experiment's `poc_subjects` table)
   become ledger data with the same identity rules, restored on restart; D187 (private companies, to be built) and D155 (the list is a start,
   not a limit) govern.
5. **State × event table** for an item through A, B, record preparation, matching, writing and the day's judging: refusal, retry, crash
   midway, a stopped run, restart on a later date, configuration change, a corrected input, two writers.
6. **Preflight** (`scripts/preflight.py`) replays split requests and answers through the code checks ($0) before any paid run.
7. **Acceptance on the frozen ruler (AGENTS §5, §7.1).** The ruler is golden-v5 (July articles), the questions standard with the 22 seeds,
   and reader B's judgement gold at 2026-07-14. D370 retired the seeded starting library for runs. Open question: how the split is accepted
   on the frozen ruler without reviving the retired seeding as product behaviour (for instance: the frozen seeds as the measurement's
   starting library only, labelled as such; extraction scored with D372's helpful / not-helpful counting; questions against
   must_open/may_open; judgement against reader B). This needs Alex's word.
8. **Decisions and documents.** Record what the split changes (A/B split, record preparation, all-open context, the one-deal rule in A, the
   part-period ladder reference, the D197 key for split candidates, collision-v4) in `docs/DECISIONS-log.md`/`DECISIONS.md`, and in PRDs
   05, 06, 03 (and 04 for the day runner). The worktrees' decision numbers have diverged (main D374–D377; this worktree lacks them and holds
   unnumbered records): renumber before merge. Two different files are named `poc-v118.json` (main: collision-v2; here: collision-v3).

## 2. Improvements still open on the traces (to confirm or refute in review)

- A: a derived share with no public figure opens every run; one question without source support for its quantity; whether A misses
  important new questions (recall) — not yet measured by anyone on these 100 items.
- Record preparation: subject choice misses (Hormuz oil under a new subject); a pace reference that reads the wrong base (server CPU:
  Grace's trailing $5 billion doubled instead of the guided $20 billion doubled).
- B: misses on existing questions not measured; weak links through the fallback (D273/D361); a retold announcement not written (1285,
  outside the first 100).
- Matching: the review's coin flips on deal milestones and population variants (pair probe: Hugging Face 2/3, Fed 2/3); the A first line
  now stops the Hugging Face repeat (0 of 4), and code (D197) owns capex aggregates.
- Judging: judgements of the new numeric questions with pace references not read yet; themes now filed correctly reach every asset
  judgement (D191) — effect not read.
- Cross-lane: the same passage written by A (for its new question) and by B (for an existing question) is stored as two pieces.

## 3. Questions for the review rounds

1. Which error classes in the traces did Claude miss, with counts and the request sentence or code that produces each?
2. Which of Claude's claims, fixes or measurements are wrong, case-fitted, contradict the standard or a decision, or would not survive a
   larger sample?
3. What is the minimal production architecture (code path, day runner under D375, identity, resume, preflight), and its state × event
   table?
4. How is the split accepted for production on the frozen ruler given D370, and what does Alex need to decide?
5. In what order should the work go, each step with its cheapest proof and the one test that accepts it?
