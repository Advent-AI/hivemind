**Not ready for the test.** The three round-5 findings are resolved, but three serious issues remain.

Sparse noise now reaches the reading list without a significance filter; reader classes decide nothing; and the single-home exemption excludes ancestor questions. The reported **6.9% and 9.1%** rates reproduce exactly. With 4,000 reassignments, I obtained **7.8% and 9.825%**.

1. **The lookup can hide facts that actually reached the question.**  
   [`send_facts`](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/decide.py:95) selects one matching statement before checking its links. For `i130`, the gold passage contains both $91 billion revenue guidance and 75% gross-margin guidance. Every stored control answer puts the margin statement under `v3`, but the lookup selects the revenue statement under `v1` and reports `v3` delivery as **0/3**.

   In an in-memory check, deleting the margin statement left that result unchanged: the loss was invisible. Across the stored answers, there are **52 send/item/question cases** where another matching statement reaches the question; those are candidates for inspection, not 52 independently verified errors. The `i130` case is verified. This affects both the counts and their calibration.

2. **“Two lost facts cannot be distinguished from luck” is too broad; a stricter check is available at the same cost.**  
   The [proposed limitation](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/prd-amendment-proposal.md:45) treats all two-fact losses alike. They are not equally uncertain.

   Using copies of the stored answers, I moved `i227` and `i183`—from two different articles—from `v17` to an unrelated question. Both fell from **3/3 deliveries to 0/3**. The current guard reported two drops and **passed**. Under the script’s article-by-article reassignment, that particular directional loss occurs with probability **1/20 × 1/20 = 0.25%**.

   A general extension that also rejects **two net losses of 3/3 → 0/3** catches this case. On the same 4,000 reassignments, adding it to the existing guards produced combined failure rates of **8.475% and 9.825%**, still below the stated 10% target. Thus three/five are defensible fixed count thresholds, but they are not the strictest protection available from these same answers. The blanket exemption leaves avoidable losses unprotected against PRD §1’s goal.

3. **The promised adjustment above 10% is absent from the code.**  
   The [proposal](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/prd-amendment-proposal.md:43) says the limits rise when the test’s reassignment failure rate exceeds 10%, before comparing observed counts. The [implementation](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/decide.py:196) instead calculates the observed verdict using fixed limits, calculates and prints the reassignment rate, and retains that verdict regardless of the rate.

   Consequently, the full test—including the held-out articles—will not execute the written decision rule if its chance-failure rate exceeds 10%. That adjustment must either be implemented and specified unambiguously or removed from the proposal before freezing the test.

No files were edited and no model calls were made.