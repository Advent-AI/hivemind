**No-go on the send yet.** The preparation has three issues that could make its verdict or spending report misleading.

1. **The probe includes topics from the 44 on which D426 stopped tuning.** C2 explicitly contains the two official-gate failure topics, and the changed request would be sent on them. Calling them guards does not by itself resolve that conflict. Replace them with suitable non-44 controls or establish a decision that specifically permits this use before sending. [Population](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/splitting/PROBE-PREP.md), [D426](/Users/lchingen/hivemind/docs/DECISIONS.md:770)

2. **The call maximum omits transport retries.** The stated 78 and 234 are the maxima for logical requests including the answer-check resend. The budget transport can attempt each request up to three times, so the corresponding maximum is **234 and 702 transport attempts**, absent an earlier stop. [Retry setting](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/budget.py:21) Recalculate the reservation report for retries and the actual longer yearly and repair requests. The caps can stop the run first; an incomplete run must remain not measured, and the $0.40 bound remains conditional on charges within reserves.

3. **The scorer needs an exact population check.** [Its count](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/splitting/score_split.py:49) builds dictionaries keyed by topic and pass, so a duplicate can overwrite another row while the expected key set still matches. The reading collector similarly builds dictionaries from outcomes. Refuse duplicate, missing or extra sends and verify that the reading and key contain exactly the items derived from those sends. Test those breaches.

One reading limitation should be stated: yearly items carry a `split` field and are only produced by the changed arm, so readers can infer the arm for those items. The arm labels are hidden, but that is not full arm blindness. Also settle whether a missed plant voids the reading even when the count has already failed; the scorer currently returns negative before checking the plants.

Bring the corrected population, accounting tests and reservation calculation back before sending.

CONSENSUS: no, because the 44-topic boundary, retry accounting and exact reading population need to be resolved first.