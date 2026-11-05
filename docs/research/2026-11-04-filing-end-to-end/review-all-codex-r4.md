**No serious issues found in the three changes. Two minor findings:**

1. **Minor — `SCALE` misses plausible abbreviations.** At [baseline_all_judge.py:43](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_all_judge.py:43), `$81.6 bln`, `$81.6 bil.` and `$81.6 MM` are treated as having no scale. For example, `$81.6 bln` paired with `unit="USD millions"` still produces a contradictory suffix—the problem this change addresses. **Fix:** recognize these financial abbreviations too. Ordinary table values, full scale words, `bn`, `mn`, single-letter scales and `%` behaved correctly.

2. **Minor — the reading list excludes v10/v12 even when they cite starting records.** At [baseline_all_measure.py:112](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/baseline_all_measure.py:112), `view_id not in NEVER_JUDGED` guards both selection reasons. A constructed case with 27 record-citing answers listed only nine, omitting all 18 v10/v12 answers. Their rungs still print elsewhere. **Fix:** apply that exclusion only to the comparison with control rungs; include record-citing answers for every question.

The three condition calculations remain intact. Independent integer enumeration matched all **4,096** success-count combinations; significant declines failed, unresolved smaller declines remained pending, and missing sends counted as unsuccessful. The renamed `misread` category consistently covers mislabeled accounting bases and triggers condition 3 failure.

No files were edited and no model requests were sent.