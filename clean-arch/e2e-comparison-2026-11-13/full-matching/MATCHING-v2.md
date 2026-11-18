# Unseeded measurement: matching rule, graded subset and predictions, version 2 (2026-11-10, D394)

This replaces MATCHING.md, which is kept. The council (`council/ga-codex.md`) asked for three changes, all made here: the seven are a
subset, not the product's set; dev-d1 clean-1 is NOT SAME; and every outcome has a defined verdict.

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
- **Limit:** boundary 2 (another deadline) applies to an event's date, not to an amount held at a date. dev-d1 clean-1 asks for credit
  support at end-2027, while q09 asks for a broader total at FY2027 year-end. The amounts can differ, so it is NOT SAME, as both readers
  had it. dev-d2 and dev-d3 clean-1 are checked in the same FY2027 10-K and stay SAME.

**Mapping of the stored dev runs** (SAME only):

| run | ruler questions opened as SAME |
|---|---|
| dev-d1 | q07, q08, q13, q18 |
| dev-d2 | q07, q08, q09, q13, q18 |
| dev-d3 | q05, q07, q08, q09, q18 (its hyperscaler question bundles 2026 and 2027: broader than q04 and q13) |

## 2. The graded subset, and every other question reported

`questions-v1.json` records, per question, the frozen gold's must-open entries it covers. Seven questions cover at least one: q04, q05,
q08, q09, q13, q18 and q23.
- **The graded subset.** These seven are the graded subset of this exploratory comparison: questions the frozen question gold says the
  product must open.
- **What the subset is not.** It is not the product's whole question set. An empty field means no must-open entry was written for that
  question, not that the product must not open it. q07 is opened in every c8 run and has gold may-open entries.
- **The other 16 are reported question by question.** For each: opened as SAME or not, and if judged, agree or disagree. None is called
  "by design" except the company-figure questions (q01, q02, q03, q10, q11, q12, q19, q20, q22), which Alex's 2026-11-08 "我觉得财务类型不应该是
  thesis，而更多的是条件…" and D370 keep out of opening. The rest (q06, q07, q14, q15, q16, q17, q21) are reported plainly.

## 3. Predictions for an unseeded clean run (243 items, three draws), frozen

| question | opened as SAME | agrees when opened |
|---|---|---|
| q08, q09, q13, q18 | in at least 2 of 3 draws each | in at least 2 of 3 draws each |
| q05 | at most 2 of 3 | yes |
| q04 | at most 1 of 3 (bundled with 2027) | yes |
| q23 | at most 1 of 3 (opened in 1 of 3 seeded Stage 2 draws) | yes |

- **Outcomes**, per question and draw: agree; disagree; not opened; opened but never judged; or run failed. Only "agree" counts.
- **Stops**, each reported with its cost:
  - a network cut in Step 1 is continued from the last completed article (`continue_clean_draw.py`);
  - a judging stopped by the frozen judge's refusal is redone from its start;
  - any other stop ends that draw;
  - if three complete draws cannot be had, the measurement stops and goes to Alex.
- **What a mapped view answers.** A mapped view carries the ruler question's text and ladder. Where the opened question has another
  deadline, the report says that the judge answered the ruler's question, by its deadline, not the product's own question.
- **Predicted subset agreements:** 4–5 of 7 per draw.
- **The seeded clean arm of Stage 2 on the same seven:** 19 of 21, about 6.3 of 7 per draw.
- **The observed gap** is the seeded subset agreements per draw on average, less the unseeded subset agreements per draw on average.
  It is reported with the questions it falls on and their outcomes (not opened, or opened and disagreeing). The gap describes what the
  unseeded system loses; it does not on its own say why. The gap mixes opening, evidence delivery and judging.
- **Labels:**
  - exploratory, from three dev runs;
  - the seeded comparison was sent on another day, so the loss mixes opening with day-to-day sampling (a same-day seeded control would
    cost about $7 more);
  - three draws.

## 4. What a paid run needs first (none of it built yet)

- **The adapter extension.** All 22 seed views plus q23 are created with their ruler text and ladder, so the frozen scorer accepts the
  run. Each clean thesis mapped SAME by the rule above, as applied by an independent reader to the run's opened questions before any
  judging, feeds its links to that view. Unmapped ruler questions have no evidence and are not judged.
- **A council read and tests with mutants.**
- **Cost:** about $7–8 (three clean draws at about $2.3; no new control, since the seeded Stage 2 is the comparison).
