**The design and decision rule are not ready for the test. Two serious findings remain.**

1. **The tie rule still leaves part of finding 1 unresolved.**  
   Call **370** is now covered: Broadcom’s sales go to custom-chip spending (`v16`), rather than NVIDIA’s share (`v6`). But call **204**, evidence `e2`, states both **$55,000 per Rubin GPU** and **$5,000 per Vera CPU**. These support separate product-revenue questions, `v20` and `v19`; neither is uniquely “most direct.” The [design explicitly leaves this case unresolved](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/design-links.md:39). Referring back to “narrowest” supplies no choice between those two questions.

2. **Finding 3 is only partly resolved: the new rule can pass substantial harm to one question.**  
   “No statistically significant loss” is being treated as “no harmful loss” in the [proposed guards](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/prd-amendment-proposal.md:18).

   I tested this entirely in memory using stored answers and the same 4,000-reassignment procedure:
   - A diagnostic correction passed the development checks.
   - A deliberately damaged copy **also passed every development check**, although deliveries to the financing-backstop question (`v9`) fell **17 → 9**, summed across three answers.
   - Its harm probability was **4.625%**, so the **1%** guard did not reject it. Overall delivery improved **183 → 213**, parking fell **139 → 18**, and core/noise guards passed.

   The sparse cases are worse: the stored `v9` deliveries are **5 / 6 / 6**, all from one article. Diverting all of them gives an exact reassignment probability of **5%**—still insufficient to trigger the 1% guard. This is a diagnostic counterexample, not a model result.

The other round-3 findings are resolved: [delivery credit requires the actual question’s link](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/measure_filing.py:149), and [combined v1/v22 parking plus per-question noise counts exist](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/measure_filing.py:155). Comparing stored answers against themselves triggered no harm guards; correctly, it did not establish improvement.

No files were edited and no model calls were sent.