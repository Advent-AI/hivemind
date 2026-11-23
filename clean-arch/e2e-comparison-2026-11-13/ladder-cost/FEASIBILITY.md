# Can the clean ladder step's own cost be measured on the same questions and facts? (D466's $0 feasibility check, 2026-11-13; version 2 after council round 3)

**Answer: possibly, but not as first written; council round 3 (`council/mu-codex-3.md`) found errors and missing proofs, corrected below. It
needs Alex's word in any case (it reuses the key's questions, D392).** The
control arm is already stored: the seeded Stage 2 draws judged the key's 22 questions on the key's own ladders and agreed with reader B on all
six graded questions they carry, in all three draws (18 of 18; q23 was not a seed), and on 18, 18 and 17 questions in all
(`clean-arch/unseeded-2026-11-10/result.txt`). So any loss the clean ladders cause on these questions shows directly.

## What exists (read)

- Seeded traces: `poc/data/clean-e2e-2026-11-09/stage2-clean-d{1,2,3}/trace.sqlite` plus `…-segment-2/trace.sqlite`, the 22 seeds as the
  initial library (`initial.json`: v1–v22, each with description, outcome, period).
- Step 2 libraries: `…-segment-2/step2/library.json`, stamped over both trace parts (`inputs.sha256`).
- The control judgements on the key's ladders: d1 and d2 `…/judged/`, **d3 `…/judged-2/`** (the first d3 judging stopped midway); 229, 253
  and 233 judgements ($0.48 from tokens in d1).

## What is missing (the builds)

1. **Seed cases for the ladder step.** The ladder step reads a thesis (description, outcome, period, opens_as, settled_by) and the article
   it came from. A seed has no opening article and no opens_as. Proposal: the seed's article is the first article in the seeded trace whose
   kept evidence links to it (written by code, its day recorded); opens_as follows the standard's class where clean's four reasons hold it.
   That covers the six graded seeds (q04, q05, q13 shared quantity; q18 product node; q08 policy stage; q09 binding obligation), q07, and the
   theme figures q06, q16, q17: **ten questions** (q14 and q15 have no reference answer in the frozen gold, `no_view`, and are left out). The company's own lines (q01–q03, q10–q12, q19, q20, q22: the standard's main-driver class)
   and q21 are left out: clean Step 1 has no main-driver reason, so its ladder step was never built for them.
2. **A seed mode in the ladder adapter.** `ladders_for` takes only theses the trace opened, with the case's article on the opening day, and
   names views from `clean-N` ids. A seed mode takes the seed ids, opens each view on its case article's day, and keeps everything else of
   the ladder mode. It needs tests (a seed with no linked article refused; view names; the control path unchanged) and a council read.

## How it would be counted

Per seed question and draw: the judge's last judgement on the clean ladder, by the frozen scorer's rule (`control_theses.agrees`) against
reader B; eligibility as in Stage B (the same question; the same due day by D430's reading), so a reworded question or a moved due day is
counted as the ladder step's loss, said so; the council's extras (round 2): the width of the clean rung that holds reader B's answer against
the key's rung, whether the rungs cover every outcome, refusals and rewordings, each listed. Sample: 6 graded questions × 3 draws = 18
question-draws (control 18 of 18 on an earlier day), ten questions × 3 = 30 in all. **Disclosed scoring detail:** the frozen comparison counts
any yes/no label other than "Yes" as "No" (`control_theses.py`), so a "still open" rung can agree with reader B's "No"; the real labels are
listed beside every yes/no agreement.

## Cost (estimated from stored runs, not a budget)

Ladder step: 10 seeds × 3 draws, first pass only, about 30 sends (the fourth Stage A: 132 answers for $0.109) → a few cents. Judging: the ten
questions drew 127, 125 and 120 judgements in the three stored control runs; a **same-day control on the key's ladders is required** (an
earlier day's 18 of 18 cannot separate the ladder from the judge's sampling). **An early rough figure of about $1–3, not a budget**; the
budget is computed from the stored requests' tokens once the question list, the wiring and the sample are fixed.

## The proofs still owed at $0 (council round 3), before this goes to Alex as a test

- **The same facts day by day:** the seeded control has every seed open from the first day; a seed mode that opens a seed on its first linked
  article's day could lose earlier links, judgement history or other questions' conclusions. Either open every seed on the first day in both
  arms, or prove on the stored data that both arms receive the same facts, links and revisions on every judging day.
- **Dependencies stay:** stored dependencies (for example v4 on v1, v5 on v3) mean the company's own lines stay in the run with their
  original questions, ladders and judging, even though the ladder step does not write their ladders.
- **The control path rebuilds:** the key's-ladder arm, run through the same wiring, reproduces the stored judgements' inputs, or each
  difference is explained, on stored data.
- **The case article** for each seed is listed with its day and whether it carries the context the question needs; opens_as and settled_by
  are written with their source.

## What it can decide

If the clean ladders keep the graded agreements against a same-day control (with rungs that are reasonable, cover every outcome and are
not merely wider), no loss was **observed on these six questions in these runs**; it does not show the ladder step is not a bottleneck and
does not pass Stage A (D400, D426). If they lose answers,
the loss is the ladder step's, measured on the same questions and facts, and its fix is Step 4's (frozen by D426; Alex reopens it).
