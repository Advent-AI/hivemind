# D371: first diagnostic for financial information linked to a same-answer question

Alex: “收入和财务这边对于当下，未来应该都是需要track 的，你应该要修改”. D369 requires capturing both core and supporting material; D370 removes presets and extra earnings-report import. D371 directs tracking current and forward-looking financial information; it does not direct a separate question for every number. The frozen version-5 ruler and every historical gold remain immutable.

## Evidence and scope

The 2026-08-29 smoke contains 40 raw extractions, 163 raw evidence entries, 64 handover `no home` drops in 15 articles and one quote failure. These counts are not all financial misses. Five articles produced six candidate questions. In the Microsoft article, e11 is current FY2027 Q1 revenue guidance and c1 is its own FY2027 annual revenue candidate: the raw answer omitted the link, so the stored handover discarded it. An exact copy with only e11's `links` changed to c1 survives schema, source checks and handover; changing only the candidate evidence list does not. The earlier FY2026 Q4 actual is a potentially useful earlier actual; old standard §5.3 permits a restated past actual as optional, and the extent D371 changes that old boundary is not settled by silently changing old gold. The model's post-hoc account says it confused a restriction on opening quarterly questions with connecting quarterly evidence; this is self-report, not proof of internal reasoning. An exact independent repeat returned a different, much shorter answer and no annual candidate. Its only evidence concerned cloud capex, so the same linking omission did not repeat in the same form.

A separate mechanism is proven for three NVIDIA next-year growth reports: the day-start snapshot excludes v70, though it was opened earlier that day. The quoted 70% forecast is present in the article that opened v70; another dropped record also carries a 44% consensus and a >100% unconstrained scenario. This experiment does not alter day-start visibility. The model can propose a candidate that matching merges into a later actual question, but the changed line does not guarantee that; so this is one class of loss, not a complete D371 solution. The source corpus and article dates are not all validated as of the claimed day; this is a request/answer diagnostic only.

## Small before/after hypothesis

**Hypothesis:** the role text's opening rules mention annual figures and forbid standalone quarterly questions, but do not explicitly distinguish supporting quarterly evidence from opening a quarterly question. Replacing one sentence should make the model connect related quarterly figures and guidance to annual questions or candidates, without opening quarterly questions or altering every other decision. This is a proposed mechanism supported by the model's account and a stored-answer counterfactual, not yet established causal proof. It does not hard-code any company, financial field, topic or article.

One in-place replacement keeps the other role instructions unchanged. The original 250-character sentence:

> A number, a financial line, a target or a named customer project does not by itself open a thesis; a customer's purchase or rollout plan is evidence to the supplier's demand and product theses unless it changes the supplier's own cash or credit risk.

Proposed 259-character replacement:

> Financial lines, numbers, targets or customer projects alone open no thesis. Quarterly data can support related annual questions or candidates. Customer purchase or rollout plans support supplier demand and product unless supplier cash or credit risk changes.

This compresses the same sentence to add the quarterly clarification without removing the separate materiality instruction. The net growth is nine characters; the reason is preserving the existing customer-plan and financial-line boundaries while clarifying the missing link. Check semantics and token counts independently before any send. The new text does not direct a link unless it is relevant.
Potential regression: the model might attach unrelated quarters to annual questions, propose an annual question from an unimportant line, or change nonfinancial evidence. We will read paired traces, including unaffected controls. The original source v74i, its schema and old configs remain unchanged.

## Four fixed requests before any send

The exact archived request for each input is rebuilt from the same item and original day-start snapshot, verified by the original archive identity and unsorted wire-order. One fresh control and one candidate on the same four real articles, each in a separate new archive; six or fewer concurrent requests, no resume or silent retries beyond production transport. These are mechanism-finding single draws, never proof of a total or general quality:

| Input | Archive call | Body SHA256 | Original request identity | Original wire SHA256 |
|---|---:|---|---|---|
| `gnews:d144b91986c520ea36e718cf` | 116 | `5d9de2121d8a247b06549f866cf8c213835b86b85e3af07d8d2c649576af956f` | `117cae5377ed5e903e16682eb82c2d08afd786c50693beafaa5d55490822498e` | `bd0106ae2cd0b26e874f96627e15d7f2188ae517968c9064bcde5fd3b64061a2` |
| `gnews:8f8a2d115ab834c7026aefd1` | 99 | `8bb09eaa4ac7991286720cef36851cbd0bcbd3213f52be721a42fec28749d563` | `767ab434772478e66b53541952f49a2abd7473bde67990eaa53ad39ae64d173d` | `9ac1714be15e779627389a991e2e2f356f6998eee553197468e408dff077ca63` |
| `gnews:6dcaad557a1b21d7b867fe34` | 11 | `858839f2ff9fe7d9ecd016834517a6dab00398febe36aad24862a2b7f30c4f8c` | `497768d4b5be85f8e6bf926c751af1a3e2316ca808c78830fd9c4cbb32bd541e` | `879411e6039acf5b9582e8ea5ecfa3154c631241f5eee768abd111f7b5df515a` |
| `gnews:71114e6d410b3ece8ed7f321` | 15 | `c5da1de40639ee59640d927f9c9d03e9a18b3745849638640c48fa65120b488b` | `787bd24d41c40a7ef6ba2e7a6a0da7d607084b3648ee013447ab299ac85dd35d` | `260cd22ec9eba382f53a6e1abb20ec6f9e75a237d1fd33e5cf94c99afa7b9d54` |

The snapshot is `poc/data/pilot-d369-existing-library-v2/views.sqlite`, as of sequence 1204; the first request sees 23 questions, the others 68. Identity was checked against the actual one-day archive; wire hashes come from reconstructing the production dict in its original order, not from the canonical archived JSON. Fix both candidate request hashes and the complete manifest before sending.

**Predeclared decision:** Microsoft supports the hypothesis only if the answer both opens a valid relevant annual candidate and explicitly links the source-correct Q1 guidance to it, and it survives handover. If the candidate or guidance is absent, the linkage hypothesis is untested, not a pass. Any unrelated link, incorrect amount/speaker/time, or meaningful loss in the four paired traces stops promotion and is diagnosed. A missing/mismatched input, identity, schema or transport failure stops the experiment without resending. A single draw is a lead, never an efficacy claim. NVIDIA's same-day case assesses whether a viable candidate is made; it cannot establish the original snapshot limitation has been resolved.
Assess each raw answer against its complete article, check source span, speaker, uncertainty, the actual `links`, candidate, dropped evidence and final handover. Check whether the case actually addresses the hypothesis: if it does not write or open an annual question, do not score it as a link success. Read all four paired outcomes and every new dropped or extra record. Source recency remains unverified. The diagnostic is not scored against a new or edited golden set, is not an acceptance measurement, and does not establish effectiveness on unseen articles or other industries. A successful small diagnostic only decides whether a separately reviewed whole-bench regression is worth proposing.

## State, readers and checks

| State/event | Reader or action | Requirement |
|---|---|---|
| No output yet | CLI and caller | Four immutable source rows and exact day-start state, matching original request identity; any mismatch refuses. |
| Fresh control/candidate | Existing `extraction.request_for`, `model.build_request`, `model.call`, JSON schema | Same source, config, shown questions, schema and ordered request except the one in-place system-role clarification; fresh archive for every call. |
| Fake transport | Existing schema, source and `sift_with_groups`/`file_reading` | Validate candidate-link source-backed example and reject report-only quote; count 8 checked arms; refuse any missing or altered case. No credential. |
| Failed/unknown request | Archive and experiment log | Record terminal failure; no silent rerun; earlier transport retries and cost may be unknown. |
| Valid answer | Existing sift/handover then human and independent read | Keep source and output together; do not confuse finding, drop, new question and delivery. No matching/reader claim without those paths. |
| Later or interrupted work | Fresh stores, dated log | No shared state or live code edits; immutable input hashes; no automatic resume. |
| New prompt | Frozen old version and all existing callers | Prototype only until reviewed; no edits to old files, no default change, no new prompt accepted without full appropriate tests and regression. |

Before a paid send, compare archived stored requests with production reconstruction, rerun stored-answer preflight (already reproduced 243/243 extract, 161 matching checked and 3 skipped; the seven quote refusals were previously read) and run the fake controls on all eight cases. This single-sentence pilot asks a distinct question from the live run: whether the clarification increases correctly connected quarterly information, while the independent controls reveal obvious changes elsewhere. It does not test day-start visibility or end-to-end quality.
