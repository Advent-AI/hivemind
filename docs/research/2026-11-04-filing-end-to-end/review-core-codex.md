The claim survives as a real mismatch between the seed arrows and D208. It does not survive as the single explanation for the filing failures, and the proposed fix is not ready for acceptance.

Database references below are under poc/data/e2e-r9-frozen-v108-2026-11-03/. I opened all six databases read-only. No files changed and no model calls were sent.

1. The inversion is real, but “the root reads no driver conclusions” is false.

D208 says drivers declare the root they feed, and roots read driver and theme conclusions. Seeding writes those declarations as ordinary dependencies. Judging interprets an ordinary dependency as “this question reads that question.”

All three frozen ledgers contain the same 17 seed dependencies and no later dependencies. The stored requests confirm the result: on July 14, Data Center reads total revenue; custom silicon reads NVIDIA’s accelerator share; memory prices read NVIDIA’s gross margin.

However, the total-revenue question already receives driver conclusions through the theme block. Its July 14 request includes hyperscaler spending, custom silicon, memory prices and H200 permission. Several are yesterday’s conclusions because the explicit arrows make them wait for company questions.

Sources: docs/DECISIONS.md:2640–2641; src/hivemind/seeding.py:1–4,32–33; src/hivemind/views/judging.py:137–155,166–173; d1/views.sqlite dependencies rows 1–17; d1/archive.sqlite model_calls 999,1005,1008,1018.

I found no later decision explicitly replacing D208 with “judge roots first, then let drivers read roots.” There is nevertheless later, deliberate support for checking a component against its whole: D260 added that check after Blackwell/Rubin exceeded Data Center revenue. D354 subsequently froze the implementation. Those decisions cannot simply be treated as nonexistent.

Sources: docs/DECISIONS.md:3052–3053,3684–3697.

2. The numerical evidence overstates how mechanically the drivers follow the root.

The claim’s Data Center counts—13/14, 14/14 and 11/14 “computed from” total revenue—do not match that description.

In d1, the first five judgements explicitly decline to calculate a segment estimate from total revenue. July 3 calls total revenue an upper bound, not a segment estimate. July 5 says the necessary segment share is missing. The explicit total-times-share calculation starts July 6.

The Blackwell/Rubin count also needs correction or a stated counting rule. In d2, six judgements, July 9–14, calculate its estimate from Data Center using approximately 90%. That is more than the claimed 2/13.

Sources: core-problem.md:33–35; d1/views.sqlite judgements 2,7,16,31,40,57; d2/views.sqlite judgements 108,133,149,165,190,205.

The dependence is substantial. The stated counts are not reliable evidence for its extent.

3. The frozen reference itself uses the supposedly defective top-down calculation.

Reader B builds total revenue from quarterly results, guidance and product information. But Reader B then estimates Data Center using its total-revenue forecast times a 92–93% share. It estimates Blackwell/Rubin using that total, Data Center’s share and compute’s share, with further product adjustments.

Therefore, “total × share” is not itself a failure under the frozen reference. The question is whether the calculation respects the available evidence and uncertainty.

Sources: docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json:68,98,117,918.

This also limits the proposed interpretation of a successful test. Better agreement would support the changed information flow. It would not prove that bottom-up calculation is universally right and top-down calculation wrong.

4. The inversion explains a route for error propagation. It does not explain why facts were filed incorrectly.

There is a concrete cascade. In d1 on July 11, total revenue changes to approximately $385bn. Data Center multiplies that by its reported share and falls below $360bn. On July 12, the total estimate rises and Data Center crosses back. Total revenue’s rung remains unchanged during those two movements; its estimated amount changes.

Sources: d1/views.sqlite judgements 140,142,159,163.

But judging happens after filing. Reversing judging arrows does not move Broadcom’s revenue into the custom-silicon question:

- d1 e219/e220 are linked to total revenue.
- d2 e236/e237 are linked to total revenue.
- d3 e242 is linked to Data Center.
- None is linked to custom silicon.

The frozen custom-silicon judgements therefore lack the Broadcom figures Reader B uses. Removing the accelerator-share conclusion cannot supply those missing figures.

Sources: each draw’s evidence and evidence_links rows named above; gold-v1.json, q16 entry; docs/DECISIONS.md:3702–3706.

The other examples also resist one universal explanation. Morgan Stanley’s rack price reaches the product-revenue question in d1 and d3, but total revenue in d2. NVL72x2 cancellation reaches the intended launch question in several records, but Data Center or product revenue in others. Google backlog reaches the capex question in d2, but revenue questions in d1/d3.

Sources: d1 evidence e104,e113,e186,e222; d2 e119,e129,e182,e202,e239; d3 e130,e185,e205,e244, with their evidence_links.

These are filing differences under identical seed arrows.

5. The revenue pile has independently documented causes that the proposed fix leaves in place.

D207 reported a pile before the driver layer was built. D259 deliberately widened what revenue questions accept and explicitly accepted more noise as its cost. D264 traced renewed concentration to that broad wording. D265 removed duplicate parent links but expressly left wrong sole links untouched. D273 added the fallback to retain indirect evidence.

None says the fallback was added because judging ran root-first. That causal history is an inference in core-problem.md, not a recorded finding.

Sources: docs/DECISIONS.md:2632–2635,3042–3047,3080,3087–3088,3143–3146.

I confirmed that the root cites other-company and market news. I could not certify the exact 24–44% claim without a classification rule and numerator list. Across the stored root judgements, the citation-occurrence totals are 151, 159 and 153. “Another company’s news” also does not automatically mean irrelevant evidence.

Sources: core-problem.md:12–14; d1–d3/views.sqlite judgements.cited_evidence_json for v1.

Keeping filing frozen means keeping this pile frozen. The experiment can test how judging uses it; it cannot demonstrate that filing was repaired.

6. Typed edges are a plausible direction, but several contracts remain unresolved.

Separating “feeds this question” from “reads this conclusion” fits D208’s intent and preserves PRD 06’s ordinary dependency meaning. A blanket reversal of every seed arrow is not yet a complete design.

The concrete problems are:

- Filing: direct_parents supplies the narrowest-question filter. Reversing that relation globally would make the filter discard the driver instead of the root.
- Cycles: validation must inspect the resulting reading direction across both edge types. Otherwise a feeds edge and a reads edge can form a cycle that neither local check sees.
- Article-opened questions: their matching-chosen dependencies must retain their present meaning, including awaited years and successors.
- Direction: an edge’s bullish/bearish meaning refers to particular endpoints. It cannot automatically survive reversing those endpoints.
- Citations: the answer checker currently permits cites_views only from dependencies_of. A new driver block must have matching citation rules.
- Information carried: current_state omits the stored implied_outcome, and dependency reasons are truncated to 600 characters. A root might receive a rung while losing the numerical calculation it needs.

Sources: src/hivemind/views/store.py:223–268; src/hivemind/extraction.py:48–67; src/hivemind/views/judging.py:148,210–219; src/hivemind/views/writing.py:49–65,175–204; docs/prd/06-views.md:114–131.

The three frozen graphs remain acyclic when their seed reading directions are reversed. That establishes only this population: they contain zero article-created dependency edges.

7. The theme block and closing rules must remain explicit parts of the design.

D195 requires every open, judged theme to reach every asset question. Several proposed feeding drivers are already themes. A new driver block could therefore present the same conclusion twice, or present different-aged versions of it.

The current ordering already exposes stale theme conclusions: d1’s July 14 root request reads July 13 conclusions for several themes. Fixing that ordering is meaningful, but it is a more precise claim than “roots cannot read drivers.”

Sources: docs/DECISIONS.md:2541–2542; src/hivemind/views/judging.py:76–91,306–336; d1/archive.sqlite model_calls 999.

Closing must retain numeric dependencies’ frozen conclusions and event dependencies’ successor rules. Closed questions must not restart merely because their drivers change. Also, current judging requires a question’s own evidence before judging it; driver conclusions alone do not make it eligible.

Sources: docs/prd/06-views.md:115–129; src/hivemind/views/judging.py:300–301; src/hivemind/pull.py:30–37.

None of the three frozen draws contains a closure, so this window cannot validate that behavior.

8. Leaving frozen files unchanged preserves the reference, but does not authorize the change.

The same questions, ladders and gold can measure a changed implementation. There is no need to edit the frozen reference.

However, changing the text supplied to judging changes the judging request even when judging-v7.txt remains byte-identical. Passing the hash tests would not establish compliance with D354’s freeze. A new version needs Alex’s decision.

Sources: docs/DECISIONS.md:3694–3697,3829; tests/test_frozen_questions_and_judgement.py:14–35.

Preflight is also insufficient for this change. Its current checks cover extraction, matching and vocabulary. They do not replay the proposed judging order or validate driver-conclusion citations. D354’s old extraction-preflight defect was subsequently addressed by D359; that repair does not add judging coverage.

Sources: scripts/preflight.py:8–16,300–305; docs/DECISIONS.md:3820–3823.

9. The proposed run is a useful bounded experiment, not sufficient acceptance.

Fourteen days, frozen upstream results and three judging draws are appropriate for asking whether changed reading directions improve these forecasts. They cannot establish that the filing symptoms are solved.

Its result would be misleading if:

- New judging is compared only with old stored judging, conflating the change with model variation over time.
- A completed ledger supplies future evidence or previous conclusions to earlier days.
- Old judgements remain and affect evidence selection or suppress new calls.
- Cached control answers substitute for changed judging requests.
- Only final agreement is reported. The scorer excludes unjudged questions from its agreement denominator and accepts overlapping ranges.
- Improvement in the four selected questions hides regressions elsewhere.
- The result is presented as covering article-created dependencies, cycles or closing, which this population does not exercise.

Sources: src/hivemind/views/judging.py:41–50,275–301; judgement-gold/score_judgement.py:63–94; judgement-gold/ruler-v1.md:63; d1–d3 dependencies and view_switches tables.

The defensible conclusion is: repair the disagreement between seed meaning and judging meaning as a separately justified change. Do not claim that it explains or repairs all filing failures. The missing Broadcom facts, inconsistent narrow-question filing, broad revenue fallback and duplicate evidence remain separate, demonstrated problems.