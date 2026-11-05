**Three serious issues remain.** The original missing-question, incomplete-classification and pending-review cases now fail or remain pending correctly, but the statistical and review-record fixes are incomplete.

1. **Serious — Floating-point rounding changes the registered rejection threshold.**  
   **Evidence:** [baseline_all_measure.py:49](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_all_measure.py:49), [line 64](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_all_measure.py:64), [line 107](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_all_measure.py:107).  
   In-memory counterexample: control successes by draw **1, 1, 2**, arm **0, 0, 0**. The exact upper-tail probability is **0.05**, which must not satisfy the registered **p < 0.05** rule. The code calculates `0.04999999999999999`, declares a significant drop, and bypasses human adjudication. `false_failure` likewise reports approximately 5% instead of zero for these margins. Exhaustively checking all 343 possible margin combinations reproduced this boundary defect.  
   **Fix:** Keep integer permutation counts or exact fractions through rejection and false-failure calculations. The convolution and one-sided direction themselves are correct.

2. **Serious — The reported chance that “some question fails” assumes independence that the design has not established.**  
   **Evidence:** [baseline_all_measure.py:115](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_all_measure.py:115) calculates `1 − product(1 − chance)`. [baseline-design.md:215](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline-design.md:215) still acknowledges dependence from sharing each reading across three draws.  
   Counterexample: 17 perfectly correlated question tests, each with the same margins and individual false-failure probability **3.725%**. Their actual probability of at least one failure is **3.725%**; this code reports **47.552%**. Identical margins can support different joint probabilities, so margins alone cannot determine this number. Restricting permutations within draws also does not preserve the acknowledged cross-draw dependence.  
   **Fix:** Establish and calibrate a joint null that preserves the relevant dependence. Until then, report the independence calculation explicitly as conditional on that assumption, with a valid bound rather than an asserted exact family probability.

3. **Serious — Both review formats can override unanimous adverse reader decisions and report every condition passed.**  
   **Evidence:** [baseline_all_measure.py:121](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_all_measure.py:121), [line 139](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_all_measure.py:139). Reader entries need only be truthy; their decisions are not checked against the final decision.  
   In-memory reproductions:
   - Both readers classify a figure as `"another quantity"`, but final `"class": "own"` makes condition 3 pass—even without a resolution reason.
   - Both readers say `"the records drove the wrong answers"`, but final `"verdict": "not the records"` makes condition 2 pass for a 9/9 versus 7/9 drop.

   With v10/v12 successful, both examples printed **all three conditions passed**.  
   **Fix:** Define typed reader decisions and an explicit resolution format. Unanimous decisions must match the final decision; disagreements must remain pending until a reasoned resolution is recorded.

The unit-loss counterexample is fixed: the real cash-flow row now reaches judging with `USD millions`. Missing v10/v12 answers count as failures; omitted classification keys are refused; unadjudicated drops remain pending. The current 44 reading requests rebuild successfully, and scoring matches all 19 questions in each stored draw. I found no additional serious issue in labelled alternate accounting bases or gold leakage. No files were edited or model requests sent.