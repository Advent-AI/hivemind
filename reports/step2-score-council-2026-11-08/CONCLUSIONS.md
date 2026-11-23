# Step 2: should Jev see retrieval scores?

Research council, 2026-11-08. Scope: the isolated clean Step 2 evidence-comparison path. No production change, model test, or change to the concurrent Step 1 experiment.

## Conclusion

Neither a benefit nor harm has been established. Keep the present request until a controlled comparison shows an advantage. Similarity is calculated between a search query and a stored group's original text; it is not a probability of same statement. The query may contain a thesis and a candidate may have several scores from different queries. Jev does not receive these scores; it receives the incoming piece as state and one candidate per typed question. It returns a choice and probabilities. Jev's choice probability, not cosine, selects among multiple same-statement results.

## Concrete observation

In saved c6 X4, incoming 12:e1 was grouped into 1:E1 although the two revenue-sharing arrangements were judged different. Recomputed from the cached exact-text vectors, cosine of the one thesis query against 1:E1's document is 0.8574. Its own document-vector cosine is 0.8654, but the record had one thesis query and that value was not its retrieval query. The saved Jev answer called same_statement at 0.89. This is one error; it neither establishes that score information will harm Jev nor measures a score distribution. Source: `poc/data/clean-step2-forward-c6-2026-11-08/{decisions.json,library.json,embeddings.json,merge-key.json,merge-third-answer.json}`. Query/doc text and cosine are reconstructed as `clean-arch/step2/compare.py` defines them.

## Council

Claude Code session 4c06c24f-8f77-4add-9443-7081a27b7903; original handoff, streams, stderr and challenge are saved alongside this record. Claude initially recommended an offline score-separation gate. Codex challenged it: overlapping marginal scores cannot rule out conditional help, and separation cannot establish Jev uses them. Claude agreed and withdrew that gate, its extrapolation of score ranges from another task, and claims about Jev's internal reasoning. Offline profiling can inform a test but cannot establish efficacy. Vendor describes Jev as a typed, non-text-generating decision model with independently evaluated questions (https://docs.typesafe.ai/introduction); evidence on LLM anchoring is only a hypothesis for Jev, not a finding (https://arxiv.org/abs/2405.01724).

## Proposed discriminating test, not yet registered or run

Reconstruct identical saved candidate requests; interleave fresh no-score controls with true-score requests and a score-shuffled control, with fixed score representation and randomization, repeated draws, cache misses, and identical model, candidates and question content except score lines. Make each score's query origin explicit: multiple search queries may yield different scores. A shuffled control tests sensitivity to a number but needs care with singleton/equal-score cases and preserving query origin. A source-blind independent reader judges differing pairs and controls without seeing arm, score, or prior decision. Report wrong merges, missed repeats, incorrect revision classifications and group choices separately, all cases, with same-arm variability, cost and limitations; fixed-candidate comparisons do not prove forward-run performance. The fresh set has few or no revisions; use separately identified stored revision cases without presenting isolated pair results as product-path evidence. Freeze design, audit and preflight under repository rules before any paid send. A score can also encode context Jev did not directly receive (e.g. thesis wording or period), so improvement would not itself establish the mechanism.

No evidence supports a universal score threshold. This proposal does not alter the accepted configuration or authorize deployment.
