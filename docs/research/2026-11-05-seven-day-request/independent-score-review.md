**The truth table follows Alex’s rule for the four cases it represents, but it cannot measure opening precision or establish seven-day quality.** For example, if the library shown to the model already contains a worthy topic, the table correctly marks no new opening as correct. It cannot tell whether the system also opened five unrelated or duplicate topics.

The requested `topic_decision_table.py` is not present in this checkout. I reviewed the neighboring [topic_score_table.py](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-seven-day-request/topic_score_table.py:6), which implements the described decision.

| Gold says topic is worthy | Already in shown library | Same topic opened | Result |
|---|---|---|---|
| Yes | Yes | No | Correct |
| Yes | Yes | Yes | Wrong |
| Yes | No | Yes | Correct |
| Yes | No | No | Wrong |

Optional topics and unknown inputs are unscored, as requested. The included seven self-checks pass. They check the function’s answers for examples; they do not verify any article, library, or opening.

The main limits are:

- **The table trusts its inputs.** It does not retrieve or verify the exact library shown with each request, decide whether a library question is the same topic, or establish whether a candidate actually became a new opening. Those judgments need the saved request and the corresponding run outcome. A starting snapshot or final library cannot substitute for the library shown on a later request.
- **It does not estimate precision.** It starts with gold-worthy topics, so openings that match no such topic are outside its view. Its yes/no opening input also cannot count two openings of the same absent topic. A correct-result percentage would combine successful restraint with successful opening; it is neither opening precision nor opening recall.
- **Unknowns can hide gaps.** Optional, missing, and even unrecognized worth labels all return `unscored`. They should remain neutral, but the reasons and counts need to be visible before anyone interprets a score.

The table itself does not read or write gold. I also checked the frozen dev and test gold hashes in this checkout and in the checkout used by the census: both copies match the recorded hashes. That verifies those two gold files currently match their frozen values.

For seven-day use, the [preparation census](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-seven-day-request/inspect_inputs.py:33) reports **486 feed items, with only two matching gold articles and one required topic in each**. Thus even perfect results on both would speak only to two topic decisions, not the quality of all seven days. The census calls itself preparation only; it does not report a completed seven-day model test. Its initial count of 68 questions is a database count, not proof of each exact model-visible library.

The same census flags 14 items whose recorded timestamps fall after their assigned day and one known later update. These are unresolved source-timing concerns, not proof that all 14 are wrong; they do prevent treating the feed as a verified reconstruction of what was available each day. The earlier one-day smoke also explicitly did not establish semantic acceptance. [One-day report](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/one-day-v117-smoke-2026-11-05.zh.md:31)

My recommendation is to use this table only for the two known worthy-topic decisions, with a reader checking each against the **actual shown library and final opening outcome**, and report unscored cases separately. Do not call that result seven-day precision. No files were changed and no paid calls were made.