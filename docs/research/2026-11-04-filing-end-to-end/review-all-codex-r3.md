**No serious issues remain in the reviewed scope. I found no new minor findings.**

1. **Resolved — exact threshold calculations.**  
   [baseline_all_measure.py:45](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_all_measure.py:45) keeps probabilities as exact fractions through the rejection decision. An independent integer-count calculation matched all **4,096 success-count combinations**. All **36 cases with p exactly 0.05** correctly remained nonsignificant.

2. **Resolved — dependence between questions.**  
   [baseline_all_measure.py:128](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_all_measure.py:128) reports the union bound separately and explicitly labels the product calculation as assuming independence. With 17 perfectly correlated tests, the actual probability was **3.725%**, the reported upper bound **63.325%**, and the independence-only estimate **47.552%**. These now have the correct meanings.

3. **Resolved — reader decisions cannot be overridden silently.**  
   [baseline_all_measure.py:73](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_all_measure.py:73) enforces the allowed decisions and agreement rules. Both round-2 counterexamples were refused. Disagreement without a resolution reason was also refused; an unreviewed decline remained **pending**.

The broader re-check found no additional serious defect in the named files or design rounds 8–10. All **32 controls** passed; **44 reading requests** rebuilt; **54 synthetic judging requests** passed their checks. The constructed comparisons changed only the added evidence and its count, and scoring matched the frozen scorer on **19 questions in each of three stored draws**. The earlier unit-loss case remains fixed.

No files were edited and no model requests were sent.