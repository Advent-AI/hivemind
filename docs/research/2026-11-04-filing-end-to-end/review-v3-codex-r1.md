**One serious issue found: the trial can pass without valid answers to the questions it is meant to fix.**

1. **Serious — Failed requests count as successful exclusions.**  
   **Evidence:** [baseline_all.py:114](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_all.py:114) records exhausted transport failures as `figures: []`; malformed JSON receives the same treatment. [baseline_v3_pilot.py:26](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_v3_pilot.py:26) checks the figures but ignores `failure`.

   **Reproduction:** In memory, I replaced all 12 v19/v20 replies with transport failures and retained the stored successful v10/v12 replies. The evaluator printed all four conditions satisfied and **`pass`**. That cannot establish that the changed sentence stopped the unwanted figures.

   **Fix:** Require all 24 expected replies to be present and successfully completed before evaluating the four conditions. A failed reply must leave the trial incomplete, not satisfy “keeps nothing.”

**No other serious findings within scope.**

- **Sentence:** `LINES_V3` expresses Alex’s approved meaning. Calculation inputs remain allowed for v10; the same quantity under the report’s name remains allowed for v12. It contains no company, product, number or benchmark example. The 99-character growth has a written reason.
- **Whole request:** I found no new contradiction or requirement that `kept_figures` refuses. The possible effects on share questions, yes/no questions and other-party themes remain correctly assigned to the full test; the pilot alone cannot establish those outcomes.
- **Version plumbing:** All **44 second-version request identities matched the stored run**. All 44 third-version requests became identical ordered JSON after replacing the task text back. `SYSTEM`, original `TASK`, `SCHEMA` and `kept_figures` are unchanged. The four downstream files match their registered hashes.
- **Trial calculations:** Apart from failed replies counting as empty answers, the four calculations match the written conditions. Replaying the stored unwanted figures correctly produced **FAIL**.
- **Registered test:** The trial-first, stop-on-failure sequence is sound once the completion check is fixed. The subsequent plan preserves round 8’s conditions, classification and fresh control comparisons, and rebuilds judgments from the new reading results.

No files were edited and no model requests were sent.