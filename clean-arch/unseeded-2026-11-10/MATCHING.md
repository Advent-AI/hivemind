# Unseeded measurement: matching rule, product question set and predictions, frozen before any paid draw (2026-11-10, D394)

## 1. The matching rule (an addition to the measurement; no frozen file changes)

An opened question is the same as a ruler question when the same reported figure or event settles both (D248 and its boundaries).
**Extra wording that does not separate them:**
- a part, programme or single deal of a reference total (D248 boundary 1; R2-e);
- the same event under another deadline, in either direction (boundary 2);
- a later milestone, variant or parenthetical widening that the question's own check does not rest on (boundary 3; R2-f for steps of
  one approval process).

**It stays apart only when:**
- it is a yes/no signing question beside an amount question (the Ohio exception, D248); or
- its extra scope is its own check and could resolve on its own, as a separately watched bet.

**How the rule was set** (`reader-brief.md`):
- Two blind readers, Codex and Claude, read the 28 questions opened by the three stored unseeded c8 dev runs.
- They agreed on SAME or not SAME for 24 of 28.
- A third reader decided the 4 disagreements against the full texts and the decisions: all SAME (`adjudication.md`). The rule above is
  that reader's general statement.
- Applying it also turns dev-d1 clean-1 into SAME for q09, though both readers had it as not same. It is the same credit-support
  programme with a later check date (boundary 2).

**Mapping of the stored dev runs** (SAME only):

| run | ruler questions opened as SAME |
|---|---|
| dev-d1 | q07, q08, q09, q13, q18 |
| dev-d2 | q07, q08, q09, q13, q18 |
| dev-d3 | q05, q07, q08, q09, q18 (its hyperscaler question bundles 2026 and 2027: broader than q04 and q13) |

## 2. The product question set: the frozen ruler's own field

`questions-v1.json` records, per question, the frozen gold's must-open entries it covers. Seven questions cover any: q04, q05, q08, q09,
q13, q18 and q23. These are the questions the product is meant to open (questions standard v3).
- The other 15 cover none. Most are company-figure questions: revenue, data-center revenue, margins, EPS, capex, product revenue.
  Under D370 (no preset questions) and Alex's 2026-11-08 "我觉得财务类型不应该是thesis，而更多的是条件…", the product does not open
  them.
- They are reported as "not opened by design". They are never scored against the product and never edited.
- q07 (Vera Rubin shipping) covers no must-open entry, but c8 opens it in every run. It is reported apart.

## 3. Predictions for an unseeded clean run (243 items, three draws), frozen

| question | opened as SAME | agrees when opened |
|---|---|---|
| q08, q09, q13, q18 | in at least 2 of 3 draws each | in at least 2 of 3 draws each |
| q05 | at most 2 of 3 | yes |
| q04 | at most 1 of 3 (bundled with 2027) | yes |
| q23 | at most 1 of 3 (opened in 1 of 3 seeded Stage 2 draws) | yes |

- **Predicted product-set agreements:** 4–5 of 7 per draw.
- **The seeded clean arm of Stage 2 on the same seven:** q04, q05, q08, q09, q13 and q18 each 3/3, q23 1/3, so 19 of 21, about 6.3 of 7
  per draw.
- **The question the run answers:** how much of the product's own judgement is lost when it opens its own questions, and which
  questions the loss falls on.
- **The verdict.** A loss of at least 2 per draw on average says opening is the next bottleneck. A loss of 1 or less says it is not.
  These lines are labelled exploratory, from three dev runs and two seeded comparisons.

## 4. What a paid run needs first (none of it built yet)

- **The adapter extension.** All 22 seed views plus q23 are created with their ruler text and ladder, so the frozen scorer accepts the
  run. Each clean thesis mapped SAME by the rule above, as applied by an independent reader to the run's opened questions before any
  judging, feeds its links to that view. Unmapped ruler questions have no evidence and are not judged.
- **A council read and tests with mutants.**
- **Cost:** about $7–8 (three clean draws at about $2.3; no new control, since the seeded Stage 2 is the comparison).
