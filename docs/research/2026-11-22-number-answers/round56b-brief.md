# Council round 56b (challenge round on the narrowed S4 change): independent read, read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite what you read.

**Context.** Round 56 (`docs/research/2026-11-22-number-answers/codex-r56.md`, read it first) rejected a blanket rule that stopped
S4's walk below any % or x figure. It gave two counterexamples and recommended narrowing the exemption to the demonstrated use: a
guidance growth rate applied with `apply_growth` to the shared quarter's forecast as the dollar base. It also asked for the request
and reader wording to be aligned.

**What was built, on a scratch copy only.** The diffs against the current files are in
`docs/research/2026-11-22-number-answers/r56b/*.diff`:
- `calc_small.py`: in `_shared`, at an `apply_growth` figure whose base input is the adopted forecast of the wanted quarter, or is
  computed from it along inputs, the walk skips the rate input. It still walks the base. Everything else is unchanged.
- `render_v13.py`: the schema's figures description and the header's shared-quantities line.
- `blind_test.py` (reader brief) and `blind_adjudicate.py` (adjudication header): the D741 ruling-1 sentence.
- `small_cases.py`:
  - two new A1 cases: the rate applied to the company Q3 forecast for Q4; the Data Center Q3 forecast grown at the guided company
    rate;
  - three new A2 cases: a Q3 value rebuilt from Q2 at the guided rate; your round-56 counterexample, the guided multiple applied
    twice to Q2; Q4 grown from a run-rate rebuilt from Q2.
- `small_mutants.py`: two new mutants: the exemption disabled; the exemption without its base condition.

**Results on the scratch copy, $0:**
- 109 of 109 cases. On the current checker the two new A1 cases fail. On the round-56 blanket copy
  (`s4-ratestop-calc_small.py.txt`) your two counterexample shapes pass, so the blanket copy is wrong.
- 43 of 43 (control + 42 mutants).
- 19 of 19 rehearsal checks; the old v13 run reproduces byte for byte.
- Census over the 24 stored v13s replies of both blind tests: 1 changes (the refused P-v4/Claude reply now publishes), 23 unchanged.
- Your counterexample on the saved P-v4 reply (Q4 = Q2 × (108/96.2)², Q3 = 112.5 in the sum): current refuses, blanket publishes,
  narrowed refuses.

## Questions
1. Find a realistic answer that passes the narrowed rule yet uses a second value of a listed shared quarter in an outcome. Look in
   particular at:
   - a base that is computed from the forecast but also from the guidance;
   - an `apply_growth` whose rate is itself built from another shared quarter;
   - range inputs;
   - `rests_on` routes, which S4 never walked (D738 records them for readers).
2. Is the narrowed rule wider than D741 ruling 1 as Alex answered it? `docs/DECISIONS-log.md`, D741, holds the question text: "参考它定
   四季度增速 13%，再套在自己预测的三季度 1136 亿上。进入收入计算的三季度数只有 1136 亿这一个". Is it narrower in a way that refuses a right
   answer an analyst would write?
3. The wording. Does each changed sentence agree with the code's closed set? Is anything left contradictory across the system text's
   "run-rate that carries the guided growth forward", the schema, the header and the reader brief?
4. Are the new cases and mutants decisive? Does each fail without the code it tests? Does any duplicate an existing one?

Return a numbered report: findings marked serious / minor / wording, with citations, then a one-line verdict: build as is, build with
the listed changes, or do not build.
