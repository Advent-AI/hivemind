# Split prompts: two-article diagnostic on existing gold

Authorization: D373 (Alex: remove gold-inconsistency stop, reuse old scores, run a few new cases). No production change, no gold edit, no recreated artificial seed set.

## What this test can decide

One send per lane for two saved real articles in golden-v5 dev: `gnews:085b1e1a1543437edb9756d6` (financing guarantee, eight prior questions), `gnews:4d1b1ca014068fb532f116b3` (customer-made chips, ten prior questions). The question lists come from the same saved historical snapshots used in the ten-article B diagnostic. The articles are seen dev cases and a single draw; this test finds prompt, linkage and output problems, not stable superiority or held-out performance. Both lanes get identical articles and question lists, model and generation settings. B receives its existing-question schema and treatment field; A receives the candidate schema with c+digits identity guard and the restructured system prompt. A does not receive B's prior generated answer, or conversely.

## State × event

| State | Success | Provider/refusal/schema failure | Partial or crash |
|---|---|---|---|
| Before either call | one new isolated result directory and immutable offline source/request manifest; gold readonly | preflight and fake tests fail closed before sending | no paid call |
| A and B in flight | each response persisted independently before validation | record response/error; no retry; pair incomplete | preserve successful lane, never claim joined score |
| Both complete | raw answer and checked handover for each; report both raw and kept, drops, questions | one invalid lane means pair incomplete | no production database write |
| Scoring | existing frozen gold with helpful=core+supporting, not_kept noise, optional neutral | missing sample or bad hash refuses score | source-backed matching aid reviewed against raw text; unresolved matches remain explicitly uncertain |

No moving snapshot is read during the call. Identity and output rules remain experimental and scoped to these calls. Any invented date, bad link or lost statement is reported even if a string matcher says hit. Same article and same source in both lanes is one source, not independent corroboration. Cross-lane exact duplicates are reported; semantic duplicates are read by hand. Incomplete pair receives no combined score.

## Inputs and comparisons

- Gold: extraction-quality worktree `golden-v5-dev.json`, SHA-256 `6f9476bb6a81ea590af273a71565e7c3c0f49908d26274b8482d52cfdee31a21`, standard page version 5. No item is rewritten. The disputed Micron article is not selected in this first diagnostic; D373 requires the unresolved concern to be disclosed if it is later scored.
- Old source results already exist for these articles in `poc/data/e2e-r9-frozen-v108-2026-11-03/d1..d3` in extraction-quality worktree. Reuse the stored answers without model reruns. **Their questions came from the 22-seed configuration; the new test uses reconstructed no-preseed snapshots.** Report old and new as historical context, not an apples-to-apples experiment. The archived B1 3-draw answers used the same eight/ten-question snapshots but test only B, not the whole old system.
- Evaluate raw extraction as well as checked handover: the full gold includes evidence that may not fit an existing/new question. Record the no-home coverage explicitly; do not mistake a dropped but written matter for unextracted. The expected gain is an open hypothesis, not a promised result.
- The old generated fiscal note supplies only a month while requiring a day; preserve this known input as a diagnostic limitation and inspect all candidate due dates; do not claim they are source-supported. The schema shape permits a date but cannot establish its truth.
- Stop and report a refusal, malformed answer, identity violation or cost/transport failure; do not automatically retry a malformed provider response. Save source, exact wire requests, original provider responses, outputs and costs in a new run directory.

## Before sending

Run stored-data preflight, verify frozen gold hash and selected snapshots against source-only packet, and run the paired fake transport: one valid response passes the actual checked handover; bad quote, wrong IDs, repeated candidate IDs and a failed arm are refused or recorded. Request byte equality is checked from the object that `model.call` sends, not its sorted archival representation. Assess preflight's known historical refusals rather than presenting its exit code as a clean pass.

## Result: 2026-11-05, one draw per new lane

Four calls completed. All original provider responses and request manifests are in `poc/data/parallel-restructure-small-2026-11-05-v1/`. This is one diagnostic draw, not a claim that the split is better or stable. An independent model reader checked every gold matter against the original source, raw answer and handover; its complete reasoning is in `small-scored-independent-20261105.zh.md`. Human review of every detail is not claimed.

Frozen v5 counts: two articles contain **19 helpful matters** (16 + 3); core and supporting were combined. The new split kept **7 complete** (4 + 3), another **2 partial**, wrote **2** that the check then dropped, and missed **8**. Among the gold's not-kept matters it retained **1**; optional entries were neutral. Partial describes whether the original meaning was fully preserved, not a new core/supporting tier. Other output not listed in gold requires source review and is not automatically classified.

The old archived v108 results were **not rerun**. The independent reader found, across the same two articles and three old draws, **7/19, 9/19, 12/19 complete helpful matters at handover**; **0, 3, 2** not-kept gold matters reached handover. It classified additional old items as partial or written and then dropped; see its per-article table. These numbers are historical context only: old v108 had 22 seeded questions and the new experiment had eight or ten historical questions. System, schema and dates also differ. This is not an apples-to-apples paired measurement.

For the first article, A proposed no gold-required question about the amount of the GPU revenue-backstop programme; it instead proposed questions on 2028 AI capex and 2029 AI debt, both listed in `must_not` and refused by existing year checks. The associated two evidence records had no home and were dropped. B retained seven records; the independent read found four complete useful gold matters and two partial. In particular, the programme record preserved the minimum guarantee but not the revenue-share-above-backstop term, and the record on negotiations did not preserve the separate claim about accelerating announcements. B linked the Firmus revenue forecast to `v1` and filled 2026-07-06 as Firmus's original statement date although the source does not establish that date. It also linked several backstop programme details to a specific AI Compute Partnership question where the article does not establish the programme identity.

For the second article B retained all three useful gold matters, plus one gold not-kept generic claim about custom silicon negotiation leverage. Five of its seven records carry two existing-question links. In one, a non-GAAP quarterly margin guidance was linked to a GAAP annual-margin question. The author says China revenue is effectively zero, while the CFO comments on the future size and impact of that market; one combined record attributes the original speaker to the CFO, risking transfer of the author's first claim to her.

The counting aid gave false positives, including treating a Sharon $4.88B case as the gold's 18% take-rate scenario, and missed the partial negotiations matter. The reported table therefore follows the independent reader's source/answer inspection, not the automatic counts. A score does not by itself establish correct source, attribution, or question placement.

Preflight before the send replayed 40 archived extractions, with one quote refusal; it also recorded one matching refusal and skipped 31 unavailable matching requests. Existing frozen-ruler test passed 3/3; fake checks exercised the four request shapes and a failed pair. The real calls used 34,726 input tokens (4,756 cached) and 6,017 output tokens. At `model.PRICES` of $0.10 / million input and $0.50 / million output, with cached input at 10%, the successful-response cost was approximately **$0.00605**, excluding any provider transport retries.

Fake-check correction after the run: the initial invalid candidate fixture had missing required fields, so its refusal did not prove the ID pattern itself was checked. The fake fixture was corrected to use a complete valid saved candidate, then mutate only its ID and separately duplicate it; the positive control and both negative cases passed offline. The stored real requests and responses were not changed or re-sent. The separate existing A identity test had already exercised valid candidates and mutated identities before this paid run.
