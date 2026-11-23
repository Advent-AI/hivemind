# Council A: why the clean system misses two questions end to end (independent investigation; read-only)

You are Codex, the second member of a council with Claude Code. Read-only: do not edit files, run model calls or start runs.
Investigate independently; Claude is investigating the same material and you will challenge each other afterwards. Read the record
cold and do not assume earlier conclusions are right.

## Objective
Alex, 2026-11-11: "好考试下一步然后跑council review 结果找问题根因" (start the next step, review the results with the council, find the root
causes). In the seeded end-to-end test of the clean system (D392; `clean-arch/e2e-2026-11-09/stage2-result.txt`, reasons in
`stage2-reasons.txt`), scored on the frozen judgement ruler, two misses have no traced cause: the China share question (q17, view
v17) in clean draw 3, and the FY2028 total revenue question (q22, view v22) in clean draw 2. Find each one's mechanism and the step
that owns it (Step 1 extraction and filing, Step 2 comparison, Step 3 saving, the frozen judge, or the measurement itself).

## Constraints
- /Users/lchingen/hivemind, branch clean-arch. AGENTS.md §1 governs (count the class, trace one case end to end, step back: the
  product's problem or the measurement's; the cheapest proof).
- Frozen: production, the judge (`src/hivemind/views/judging.py`), the ruler (`docs/research/2026-11-01-e2e-loop/judgement-gold/`: gold-v1.json,
  questions-v1.json, packet-v1.json, score_judgement.py). A gold disagreement is a gap in the system, never a case for the ruler (D263).
- Out of scope: Step 4's ladder step (`clean-arch/step4-2026-11-10/`, another session's work), any redesign or new mechanism.

## Primary materials
- Saved clean runs: `poc/data/clean-e2e-2026-11-09/stage2-clean-d{1,2,3}/judged*/` (views.sqlite, archive.sqlite with every judge
  request and answer, judge-requests.json; draw 3's completed run is `judged-2`); Step 1 traces `stage2-clean-d{N}/trace.sqlite` and
  `stage2-clean-d{N}-segment-2/trace.sqlite`; Step 2/3 library `stage2-clean-d{N}-segment-2/step2/library.json`.
- Production's control draws of the same test: `poc/data/clean-e2e-2026-11-09/stage2-control-d{1,3,4}/` (views.sqlite, archive.sqlite).
- Exact judge requests per day, reproduced offline from the saved archives: `poc/data/clean-e2e-misses-2026-11-11/control-d{1,2,3}/`
  (`control-requests.json` keyed by request sha256, `control-rounds.json` by day).
- The articles: `poc/data/items-nvda-2026-07-01-10-27.sqlite`.
- Prior diagnosis of the other clean misses: docs/CURRENT_STATE.md (capital spending, D394; Ohio guarantee, open defect 1).

## Deliver
1. For each of the two misses: the mechanism, traced on the record with evidence ids, days and request text; the step that owns
   it; whether the agreeing draws differ in input or only in the judge's choice. Facts and hypotheses kept apart.
2. The class each belongs to, counted over all questions and draws (clean and production), with what each instance costs on the ruler.
3. The cheapest decisive proof for each (stored data first; then re-sending saved requests, with the number of sends and what
   result would mean what).
Under 700 words.
