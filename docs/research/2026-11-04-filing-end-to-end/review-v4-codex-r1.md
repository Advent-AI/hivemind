**Three serious findings remain. I would fix these before sending v4.**

1. **Serious — The period rules and August delivery check disagree.**  
   Round 18 requires quarterly operating income and revenue for v10; only capex explicitly allows the half-year alternative ([design:432](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline-design.md:432)). But [baseline_heldout_measure.py:49](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_heldout_measure.py:49) accepts either complete quarterly or half-year inputs for v10. In memory, **117,270 operating income + 177,837 revenue**, correctly labelled six months, returned `delivered=True` without either required quarterly figure.

   Additionally, line 46 checks historical-column values only when labelled as the quarter: **50,078**, wrongly labelled as the latest half-year, was not flagged. The prompt’s “any other period” exclusion also leaves unclear why correctly labelled year-to-date figures are allowed.

   **Fix:** Align the prompt, registered conditions and checker on quarter versus year-to-date treatment. Require v10’s registered quarterly pair; reject historical values mislabeled as either current period.

2. **Serious — Losing every v22 starting figure can still pass all May conditions.**  
   Round 18 explicitly claims to determine whether the new check drops v22’s quarterly revenue ([design:437](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline-design.md:437)). However, questions with no retained figures are excluded from judging ([baseline_all_judge.py:78](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_all_judge.py:78)); classification assesses only retained figures.

   **Reproduction:** I removed every v22 figure from a copy of the stored v3 results and removed its downstream judgments/classifications. **All three conditions still printed `pass`.**

   **Fix:** Before sending, register an explicit retention condition for v22’s latest reported total revenue. Treat missing required starting figures as failures independently of downstream judgment accuracy.

3. **Serious — The held-out checker can pass an incomplete question set.**  
   [baseline_heldout_measure.py:56](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_heldout_measure.py:56) relies on `sheet_rows`, which checks failures among supplied entries without requiring all 22 questions.

   **Reproduction:** A synthetic reading containing only v10 and v12, with the other **20 questions absent**, printed both delivery and identity `pass`.

   **Fix:** Require exactly the 22 expected questions, both selected report documents, and three completed replies per question/document before evaluating either condition.

The filed-copy rule correctly selects May’s two documents and August’s two EDGAR documents, excluding both August website copies. The printed value sets match the stored tables. Failed sends are refused; empty required answers fail delivery; six-month figures mislabeled as quarterly are caught. May’s Q2/outlook exclusion works as registered, but a correctly labelled Q4 figure passes that deliberately narrower check.

The trial → May judging → August blind-classification sequence is otherwise sound. No files were edited and no model requests were sent.