# Council B, close-out round, Step 1 test set. Challenge the verdict (read-only)

The run is `poc/data/clean-step1-takeover-2026-11-07/test-k6b-flash/`: K6b on DeepSeek Flash high, inputs byte-identical to the dev
Flash run, 26 NVDA-tagged test articles from 2026-09-01 to 10-24, forward from an empty library.
- 26 of 26 complete; 0 format failures, 0 retries; $0.25 at the published rates.
- Scored by `score_gold_runs.py --test` on the frozen test gold (`af2145cd…`, checked against `golden-v5.sha256`). The scorer was
  re-checked on dev and reproduces 205/234 and the production draws exactly.

| 26 test articles, 42 helpful, 9 core | K6b Flash | Production test draw (`test-control-d1`) |
|---|---|---|
| Helpful matters kept | **32/42** (76%) | 20/42 |
| Core | 8/9 | 8/9 |
| Items | 42 | 39 |
| Not-kept spans kept | 8 | 4 |

- Predeclared line: helpful at least 35 (81.2% of 42), at most 3 small theses, no fragments. **Missed on helpful by 3.**
- Library: 10 theses, all 10 judged "bet" by three readers with source, using the dev prompt. Small 0, fragments 0.
- One draw. On 42 entries a binomial standard deviation is about 2.5.

**The 10 misses, each read against what the run returned:**
- **7 were extracted but left unfiled**, with no thesis link, so code dropped them as having no home:
  - the core miss, Q2 revenue of $96.2bn with data centre up 117%, when only 2 theses were open;
  - the 50% free-cash-flow return plan, and the analysts' $441bn free-cash-flow forecast (that article filed 0 and left 6 unfiled, with
    2 theses open);
  - Dell XPS RTX Spark, twice: the article is dated Oct 9 and the RTX Spark thesis opened on Oct 10;
  - AI infrastructure spending above $1tn by 2029, and the author's valuation scenario.
- **3 were not extracted:** NVIDIA's denial that the RTX 5090 is discontinued; Orange testing AI-RAN; Dell, QCT and Supermicro Aerial
  configurations.

**Mechanism:** the test protocol starts from an empty library over sparse articles spread across two months. No thesis for NVIDIA's
revenue and earnings trajectory existed, and K6b's restraint on opening theses did not open one, so results had no home. The dev run
(115 dense articles) built its homes early. Production would carry earlier theses, but a new entity's bootstrap would hit the same
case.

**My verdict:**
- The test set misses the proportional helpful line, by 3, in one draw.
- The largest class is unfiled evidence with no home under a thin library (7 of 10, including the core miss).
- Small theses and fragments pass, and helpful is well above production (32 against 20).
- Per AGENTS, the failed acceptance goes to Alex with this census. I do not start a fix, and I hold the PRD §12 adoption, which is the
  last step of the plan.

Challenge:
1. Is anything wrong in the mechanism, or in the verdict's framing?
2. Is holding the PRD adoption right, given that Alex already confirmed K6b + DeepSeek?

Under 200 words.
