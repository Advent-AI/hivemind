One serious blocker remains: **an evidence ID does not uniquely identify the underlying view and judgment.**

For example, at cutoff **379**, `e55` belongs to both:

- `v7 / judgment 350`: whether Rubin starts shipping in 2026.
- `v15 / judgment 355`: whether SK Telecom’s AI factory opens by the end of 2027.

These are different questions supported by the same source.

The [plan, line 26](/Users/lchingen/hivemind/docs/research/2026-10-24-main-thesis-replay/plan.md:26) asks the model to cite only `evidence_id`, then has code attach the corresponding `view_id` and `judgement_id`. Neither that paragraph nor the [value/readers table](/Users/lchingen/hivemind/docs/research/2026-10-24-main-thesis-replay/plan.md:61) defines what happens when several pairs correspond.

This occurs in **all six planned snapshots**. At the final cutoffs, **7 Rubin evidence IDs** and **10 Capex evidence IDs** have multiple view/judgment associations. The existing [snapshot exporter](/Users/lchingen/hivemind/poc/hierarchy_study/study.py:129) preserves those associations per view; [synthesis_context](/Users/lchingen/hivemind/poc/hierarchy_study/study.py:370) deduplicates evidence separately.

**Why this blocks the core question:** choosing one association can send the agent to the wrong view. Attaching every association preserves provenance, but does not establish that the answer actually used every linked view—so `unused` and successful drill-down need a defined meaning.

**Required before code:** specify the complete citation-to-association rule, including how multiple associations affect `unused` and the probe. Preserve the actual snapshot associations; do not infer a unique pair from `evidence_id`.

I found no other serious blocker in the fresh-versus-update comparison, time cutoffs, or stated budget/recovery policy. No files changed; no model calls made.