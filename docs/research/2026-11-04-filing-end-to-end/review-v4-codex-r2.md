**Two serious findings remain. The v22 retention fix works; the period and completeness fixes are incomplete.**

1. **Serious — Correctly labelled half-year figures can falsely fail August delivery.**  
   [quarter_label:31](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_heldout_measure.py:31) excludes only “six months”; `half_label` also recognizes “first half” and “H1”. Consequently, one label can match both periods.

   **Reproduction:** Using source-verified quarterly figures **63,734 + 96,221**, delivery passes. Adding the correctly labelled **117,270 — “H1 FY2027 ended July 26, 2026”** makes delivery fail with one “misread”. Spelling the same period “Six months ended July 26, 2026” passes. This contradicts round 19’s explicit allowance.

   **Fix:** Make quarter and half-year recognition mutually exclusive and consistent across supported spellings. Also reconcile [TASK_V4:40](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_read.py:40), which still orders deletion of every other period, with round 19’s allowance.

2. **Serious — Missing report documents can still pass as complete.**  
   [sheet_rows:36](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_all_measure.py:36) checks only documents listed in the supplied `report`; August additionally checks its length, not distinct identities.

   **Reproduction:** Removing the CFO document and its answers from the stored May v3 reading still makes the new retention check print **pass**. For August, listing the release twice, supplying only that document’s answers, and classifying its retained figures makes **both delivery and identity pass**. The reported figure count is also doubled.

   **Fix:** Validate the exact two distinct selected document IDs, all 22 question IDs, and three readable replies for each pair before measuring.

**Verified:** Removing all v22 figures now fails retention. Missing questions and failed replies are refused. Half-year-only inputs no longer satisfy quarterly delivery; the original historical-column mislabels are caught. Round 13 still reports its five wrong figures; round 16 still passes all three conditions. Retention values match May’s tables, and document selection returns the correct May/August pairs.

No other serious findings. No files edited or model requests sent.