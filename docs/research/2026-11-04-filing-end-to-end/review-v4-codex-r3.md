**Round 2’s two findings are fixed in the full May/August measurements. One serious completeness gap remains in the trial.**

1. **Serious — The trial still accepts a duplicated document and omits the other.**  
   [baseline_v4_trial.py:29](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_v4_trial.py:29) builds its expected replies from the supplied document list without validating that list. Line 37 then counts duplicated answers twice.

   **Reproduction:** In memory, I copied round 16’s reading, marked it version 4, and removed its labelled next-quarter guidance to make a passing control. Replacing the document list with the May release twice and removing all CFO answers still produced **pass**, including “capex kept in 6 of 6 reads.” The CFO document was never evaluated.

   **Fix:** Apply the shared document-selection check to the trial too. Require the two distinct selected May documents and exactly three readable replies for each of its seven questions.

**Verified fixes and regressions:** The quarterly pair plus correctly labelled H1, first-half, six-month or year-to-date figures now passes. Half-year-only delivery fails; historical-column mislabels remain caught. Full May/August measurements reject missing or duplicated documents, and August rejects missing questions or replies.

Round 13 still reports **53 figures, five wrong quantities**. Round 16 still reports **46 figures and all three conditions passing**. Retention passes the stored round-16 control and fails when v22’s figures are removed.

No other serious findings in rounds 18–20 or `TASK_V4`. No files edited or model requests sent.