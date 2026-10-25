1. **Alex’s idea is sound:** retrieve candidates first, then use Jev to judge their fit; TypeSafe publishes this pattern itself. [Vendor reranking example](https://docs.typesafe.ai/cookbooks/rerank_typesafe)
2. **Grouping and identity need different answers:** Vera CPU revenue can belong to the Rubin story without being the same quantity as total Rubin revenue. [Plan:39](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:39)
3. **The example request is structurally valid**, but its membership wording conflicts with its own examples. [Plan:35–39](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:35), [Choice API](https://docs.typesafe.ai/primitives/choice)
4. **Jev 1.14.0 is now newest; 1.13.0 remains available.** The plan should distinguish an intentional pin from the current release. [Current models](https://docs.typesafe.ai/models)
5. **The 64-question and 120,000-byte restrictions come from the old client**, not today’s API limits. [Old client:24–43](/Users/lchingen/tn-hivemind/src/tn_hivemind/models/jev.py:24), [Current limits](https://docs.typesafe.ai/models)
6. **The evidence test was 56/69 correct for Jev, 60/69 for Luna, and 61/69 for the reconstructed cascade**—one extra correct answer over Luna. [Jev results:127](/Users/lchingen/tn-hivemind/evals/bench-v1/results/relations-jev-r1.json:127), [Luna results:127](/Users/lchingen/tn-hivemind/evals/bench-v1/results/relations-v4-r1.json:127)
7. **The tagging result supports Jev as a check:** role accuracy was 74.2% for Jev, 89.1% for extraction, and 91.0% for the cascade. [Benchmark:190–199](/Users/lchingen/tn-hivemind/docs/BENCHMARK.md:190)
8. **Neither old test measured group membership or identity**, so neither establishes that Jev succeeds at one and fails at the other. [Evidence specification:59–89](/Users/lchingen/tn-hivemind/evals/bench-v1/SPEC.md:59), [Tagging questions:568–577](/Users/lchingen/tn-hivemind/src/tn_hivemind/data/relations.py:568)
9. **The largest mistake is turning one score into “same,” “same matter,” or “different.”** Certainty and relationship type are separate things. [Plan:62](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:62), [Score semantics](https://docs.typesafe.ai/primitives/score)
10. **Keep the current pipeline as the control.** Automatic membership additions and automatic identity decisions require separate owner choices. [Plan:78](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:78), [D149](/Users/lchingen/hivemind/docs/DECISIONS.md:2170), [D166](/Users/lchingen/hivemind/docs/DECISIONS.md:2323)

# Review of Jev usage and reranker positioning

Reviewed on **2026-10-25**. This review covers the requested parts of sections 3–6. It does not redesign extraction, change the pipeline, or authorize a paid experiment.

I read public vendor documentation, repository sources, stored evaluation answers, and relevant papers. I made no paid model calls. Calculations below use saved answers; they are not new model measurements.

## 1. Latest TypeSafe API

### Versions and changes

TypeSafe identifies **`jev-1.14.0`**, released October 14, as its newest model. **`jev-1.13.0` remains supported**. Both `jev-latest` and `jev-preview` currently resolve to 1.14.0. A version pin matters because changing an alias can change answers under an existing threshold. [Models](https://docs.typesafe.ai/models)

The release announcement describes incremental improvements, with the largest expected gain in multilingual support. It also introduces experimental image input, a `box` answer type, and longer context. Images are enabled for both versions; `box` is restricted to 1.14.0. These experimental features are explicitly less mature than ordinary text decisions. The announcement does **not** establish a quantified improvement on Chinese grouping or identity. [Jev 1.14 announcement](https://typesafe.ai/blog/jev-1-14)

### Request and response shapes

The endpoint remains **`POST https://api.typesafe.ai/v1/systemone`**, using bearer authentication. The required body fields are `model`, `state`, and `questions`. `questions` is an object keyed by caller-chosen identifiers. The response contains `model`, `answers` under those identifiers, and token `usage`. [API reference](https://docs.typesafe.ai/api/system-one)

`state` accepts a string, object, or array. The old repository’s requirement that it be a nonempty string is a narrower local contract. [State documentation](https://docs.typesafe.ai/concepts/state), [Old client:28–29](/Users/lchingen/tn-hivemind/src/tn_hivemind/models/jev.py:28)

| Type | Question shape | Answer shape and meaning |
|---|---|---|
| `choice` | `instructions`; `criteria` object mapping labels to descriptions | `type`, winning `choice`, per-label `probabilities`, `confidence`. Appropriate for unordered categories. [Choice](https://docs.typesafe.ai/primitives/choice) |
| `score` | `instructions`; ordered `criteria` array | `type`, numerical `score`, `legend`, per-level `probabilities`, `confidence`. The score is the expected level index, from zero to the highest index. [Score](https://docs.typesafe.ai/primitives/score) |
| `noul` | Yes/no instructions; optional criteria explaining true/false | `type` and `noul`, the probability of yes. It does **not** return a separate confidence field. [Noul](https://docs.typesafe.ai/primitives/noul) |
| `box` | Experimental image-location question | Bounding-box coordinates; requires the image opt-in header. Irrelevant to this text POC. [API schema](https://api.typesafe.ai/openapi.json) |

Instructions and descriptions can use structured values; strings are sufficient here. The question identifier itself is not model context, so a target named only `g1` would be insufficient. Claude’s example includes the target description in `instructions`, which avoids that problem. [Structured instructions](https://docs.typesafe.ai/primitives/advanced), [Choice](https://docs.typesafe.ai/primitives/choice)

### Limits and prices

| Item | Current documented value |
|---|---|
| Input price, both versions | **$0.042 per million input tokens**; output tokens free. [Models](https://docs.typesafe.ai/models) |
| Questions per request | No separate numerical cap; context limits apply. [Models](https://docs.typesafe.ai/models) |
| Default request context | **64k tokens:** state plus all questions. [Models](https://docs.typesafe.ai/models) |
| Default per-question context | **32k tokens:** state plus one question. [Models](https://docs.typesafe.ai/models) |
| Experimental long context | Both limits become **262k** with `TypeSafe-Danger-Zone-Long-Context: true`; documented as slower and less accurate. [Models](https://docs.typesafe.ai/models) |
| HTTP body | **32 MiB**, independently of token limits. [Request rules](https://docs.typesafe.ai/api/errors) |
| Encoding and nesting | UTF-8 JSON without BOM; maximum 64 nested levels; finite numbers. [Request rules](https://docs.typesafe.ai/api/errors) |
| Choice criteria | Maximum **255**. The OpenAPI schema allows a minimum of one; a meaningful comparison normally needs alternatives. [OpenAPI](https://api.typesafe.ai/openapi.json) |
| Score criteria | Maximum **10**. OpenAPI permits one; prose documentation says the scale should have at least two. [OpenAPI](https://api.typesafe.ai/openapi.json), [Score](https://docs.typesafe.ai/primitives/score) |
| Rate limits | Organization-specific requests/second and tokens/second; numerical allowances are in the console. [Models](https://docs.typesafe.ai/models) |
| Rate-limit response | `429`; overload can return `529`. SDKs retry with backoff. [Errors](https://docs.typesafe.ai/api/errors) |
| Chinese | Accepted under CJK support; English remains the strongest documented language. No Chinese grouping accuracy figure was found. [State](https://docs.typesafe.ai/concepts/state) |

The **120,000-byte**, **64-question**, and **two-minimum-criteria** checks in the old wrapper should therefore be described as **local restrictions**, not current vendor limits. Its request and response validation also explicitly pins 1.13.0, so changing only the request’s model string would not make that wrapper support 1.14.0. [Old client:24–43,61–62](/Users/lchingen/tn-hivemind/src/tn_hivemind/models/jev.py:24)

### Minimal correct request

This adapts the documented support-ticket example. It is illustrative; I did not send it.

```json
{
  "model": "jev-1.14.0",
  "state": "The customer says their subscription was charged twice.",
  "questions": {
    "issue": {
      "type": "choice",
      "instructions": "Which issue does the message report?",
      "criteria": {
        "duplicate_charge": "The same fee was charged more than once.",
        "other": "A different issue is reported."
      }
    }
  }
}
```

Send this JSON to the endpoint above with the bearer and JSON content-type headers. Read the result at `answers.issue`; do not expect generated explanation text. [API request examples](https://docs.typesafe.ai/api/system-one)

### Probability, confidence, and calibration

TypeSafe markets Jev as trained for calibrated decisions using RLCD. That is a vendor claim about training, not proof of calibration on this repository’s labels. [TypeSafe’s description](https://typesafe.ai/)

For a Choice with \(n\) options, the current documented formula is:

\[
\mathrm{confidence}
=\frac{p_{\max}-1/n}{1-1/n}.
\]

Thus, for three options, confidence **0.95** corresponds to a winning probability of approximately **0.9667**, not 0.95. A winning probability of 0.90 corresponds to confidence 0.85. A confident `cannot_tell` is still `cannot_tell`. [Confidence](https://docs.typesafe.ai/confidence)

The plan must name which field it thresholds. The old tagging policy thresholds **`confidence`**. Choosing that threshold on dev does not, by itself, demonstrate that probability bins match empirical success rates. [Tagging policy:595–618](/Users/lchingen/tn-hivemind/src/tn_hivemind/data/relations.py:595)

The old wrapper records two-decimal rounding as an **observed behavior** and allows resulting summation error. I found no basis for promoting that observation into a permanent precision guarantee. [Old validator:79–94](/Users/lchingen/tn-hivemind/src/tn_hivemind/models/jev.py:79), [Current schema](https://api.typesafe.ai/openapi.json)

### Batching, latency, retention, and SDKs

**Batching is supported and encouraged.** TypeSafe says each question is evaluated separately against the shared state. Its fan-out pattern explicitly places several questions in one request. This supports one candidate and quote in shared state, with one target-specific question per recalled card. It is not a listwise comparison among all targets. [Fan-out](https://docs.typesafe.ai/patterns/fan-out)

The vendor’s older Jev 1.12 cookbook compares 13 batched questions with 13 sequential requests over a 53,777-character document. It reports **0.27 seconds versus 2.71 seconds**, and **$0.000497 versus $0.006090**. These are workload-specific results against sequential calls, not a universal latency promise. Several answers exhibit small run-to-run variation, contradicting an assumption of guaranteed exact repeatability. [Parallel-question experiment](https://docs.typesafe.ai/cookbooks/parallel_questions)

The **70–500 ms** figure is a vendor launch claim, not a measured latency for this POC or its largest batches. [Launch announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

TypeSafe says it does not train on customer requests or responses. **Zero data retention is an enterprise offering, not the documented default.** The public privacy policy and DPA use necessity-based retention language rather than a fixed universal deletion period. [Legal overview](https://docs.typesafe.ai/legal), [Privacy policy](https://typesafe.ai/legal/privacy-policy), [DPA](https://typesafe.ai/legal/data-processing)

Official clients include Python **`typesafe-sdk`**, with synchronous and asynchronous clients, and JavaScript/TypeScript **`@typesafe-ai/sdk`**. The JavaScript documentation specifies Node.js 22+. [Python SDK](https://docs.typesafe.ai/sdk/python), [JavaScript SDK](https://docs.typesafe.ai/sdk/javascript)

**Access limits of this review:** the public documentation, OpenAPI, cookbooks, release announcement, and legal text were readable without login. I did not access the account console, authenticate to the API, verify the account balance, or measure current service latency. Current numerical account rate limits and current payment status remain unverified.

### Direct vendor examples relevant to this review

- **Reranking:** a Jev 1.12 cookbook retrieves 30 legal candidates with BM25 and judges query–candidate pairs using Noul. Across 40 queries, it reports rounded top-1 retrieval success rising from **5% to 18%**, top-5 from **15% to 35%**, and top-10 from **38% to 62%**. This supports the intended pattern, not a grouping accuracy forecast. [Reranking cookbook](https://docs.typesafe.ai/cookbooks/rerank_typesafe)
- **Entity matching:** another Jev 1.12 example processes **450 preblocked beer pairs**, using a three-level Score plus field-specific Nouls. It produces **40 same-entity assertions, 50 review cases, and 360 unlinked pairs**. Those are routing counts; the page does not report accuracy against gold labels. [Entity-alignment cookbook](https://docs.typesafe.ai/cookbooks/entity_alignment)

## 2. What the old repository actually did

### Two different cascades

The plan combines two distinct uses.

**Relationship tagging:** `tag_state` supplies the subject, counterparty, first quote, and additional quotes as context. One request asks three Choice questions:

1. The counterparty’s role relative to the subject.
2. What flows between them, or the market in which they compete.
3. The subject’s stated dependence on the counterparty.

The instructions require grounding in the quote. [relations.py:543–577](/Users/lchingen/tn-hivemind/src/tn_hivemind/data/relations.py:543)

The selected cascade keeps extraction’s labels unless Jev confidently disagrees on **role or channel**, which triggers an isolated Luna adjudication. Dependency disagreement does not trigger this policy, and direct Jev dependency replacement is disabled by `jev_dependency: False`. [relations.py:588–619](/Users/lchingen/tn-hivemind/src/tn_hivemind/data/relations.py:588)

**Evidence relations:** the historical implementation asks whether evidence `supports`, `contradicts`, is `contextual` to, or is `irrelevant` to a premise. Its cascade **accepts Jev’s answer directly at confidence ≥0.95**, otherwise asking Luna. Here Jev is a first-pass decider, not merely a disagreement check.

Historical source: `/Users/lchingen/tn-hivemind/src/tn_hivemind/edges_v4.py:65–117`, read at commit `79540ee74b3f5c210ebb9a11bee8fad180fbedf1`. The current decision record also describes this optional Jev-first evidence cascade. [Old DECISIONS.md:968](/Users/lchingen/tn-hivemind/docs/DECISIONS.md:968)

That historical file judges each premise–evidence pair in isolation because earlier shared context allowed reasons to borrow neighboring facts. This is an isolation requirement for the material presented to a judgment; it does not establish that TypeSafe requires one question per HTTP request. Historical source: the same `edges_v4.py:1–7`.

### Evidence-relation evaluation: correcting the denominators

The gold task concerns a thesis, premise, and attributed evidence—not group membership or duplicate identity. Its difficult cases include mismatched periods, segment versus total scope, forecasts versus actuals, and different entities. The gold is explicitly **cross-family model-authored, not human gold**. [SPEC.md:3–20,59–89](/Users/lchingen/tn-hivemind/evals/bench-v1/SPEC.md:3)

| Evaluation | Jev alone | Luna alone | Jev-first cascade, reconstructed |
|---|---:|---:|---:|
| Dev, 51 pairs | 41/51 = **80.4%** | 43/51 = **84.3%** | 44/51 = **86.3%** |
| Test, 69 pairs | 56/69 = **81.2%** | 60/69 = **87.0%** | 61/69 = **88.4%** |
| All 120 pairs | 97/120 = **80.8%** | 103/120 = **85.8%** | 105/120 = **87.5%** |

Sources: saved [Jev scorecard and rows:9–188](/Users/lchingen/tn-hivemind/evals/bench-v1/results/relations-jev-r1.json:9), [Luna scorecard and rows:9–188](/Users/lchingen/tn-hivemind/evals/bench-v1/results/relations-v4-r1.json:9). Cascade values are my calculation using the historical policy above.

I reconstructed the cascade by joining saved answers on item ID and selecting Jev’s prediction when its saved confidence was at least 0.95, otherwise Luna’s prediction. On test, this accepts **37 Jev answers** and sends **32/69 pairs to Luna**. Thus it avoids **53.6%** of Luna calls under that policy.

The test improvement over Luna is exactly one item, **R-110**: gold and Jev say `contradicts`; Luna says `contextual`. [Jev R-110:2098](/Users/lchingen/tn-hivemind/evals/bench-v1/results/relations-jev-r1.json:2098), [Luna R-110:1553](/Users/lchingen/tn-hivemind/evals/bench-v1/results/relations-v4-r1.json:1553)

The plan’s **81.2 / 85.8 / 88.4** comparison mixes the test population with the all-items population. The older prose contains that same mismatch; the stored results resolve it. [Plan:27](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:27), [Old cross-company design:647–650](/Users/lchingen/tn-hivemind/docs/CROSS_COMPANY_DESIGN.md:647)

There is also a relevant failure concentration: on test, Jev labels **9 of 20 contextual cases as supports**. That cautions against treating topical connection as substantive support, though it does not directly measure grouping. [Jev confusion matrix:159–183](/Users/lchingen/tn-hivemind/evals/bench-v1/results/relations-jev-r1.json:159)

### Relationship tagging: what 74% and 91% mean

The test gold contains **302 positive mentions and 71 hard negatives**, but tag accuracy uses **221 matched positive mentions**. The scorer matches sources, parties, and spans, then computes tag accuracy over all matches—including matches a mode subsequently excludes as `no_relationship`. [Scorer:176–238](/Users/lchingen/tn-hivemind/evals/bench-x1/score_links.py:176)

| Test mode | Positive recall | Role accuracy | Channel accuracy | Dependency accuracy | Negative false positives |
|---|---:|---:|---:|---:|---:|
| Extraction | 221/302 = 73.2% | 197/221 = **89.1%** | 113/221 = 51.1% | 173/221 = 78.3% | 0/71 |
| Jev mode | 209/302 = 69.2% | 164/221 = **74.2%** | 143/221 = 64.7% | 181/221 = 81.9% | 0/71 |
| Selected cascade | 221/302 = 73.2% | 201/221 = **91.0%** | 131/221 = 59.3% | 175/221 = 79.2% | 0/71 |

Sources: [selected cascade:6–15](/Users/lchingen/tn-hivemind/evals/bench-x1/results/links-test-final.json:6), [extraction:60–69](/Users/lchingen/tn-hivemind/evals/bench-x1/results/links-test-final.json:60), [Jev:87–96](/Users/lchingen/tn-hivemind/evals/bench-x1/results/links-test-final.json:87). Integer numerators are reconstructed from the stored fractions and scorer denominator.

The correct interpretation is:

- Against Jev alone, the selected cascade is substantially better on role.
- Against the existing extraction baseline, it gains **4 correct role labels out of 221**, approximately 1.8 percentage points.
- Jev mode excludes 12 previously matched positives, reducing recall.
- All three modes have 0/71 negative false positives, so that result does not demonstrate a unique Jev benefit. [Same result file:6–96](/Users/lchingen/tn-hivemind/evals/bench-x1/results/links-test-final.json:6)

The much larger dev role improvement came mainly from AWS customer agreements being called partnerships. The benchmark reports **275 adjudications among 1,901 mentions**; that is a different population from the 221 test matches. [BENCHMARK.md:193–199](/Users/lchingen/tn-hivemind/docs/BENCHMARK.md:193)

A further qualification: “Jev alone” is the name of an evaluation mode. Failed or missing validated Jev results fall back to extraction, and the test report records Jev checks for 1,736 of 1,744 system mentions. [relations.py:608–614](/Users/lchingen/tn-hivemind/src/tn_hivemind/data/relations.py:608), [Result metadata:4,115](/Users/lchingen/tn-hivemind/evals/bench-x1/results/links-test-final.json:115)

### Cost and operational history

The pinned configuration records **$0.37 across 11,948 calls**, about $0.000031 per call. That is historical workload cost, not a price for a future batch of 64 long pair questions. [v4p2-jev-links.json:2–23](/Users/lchingen/tn-hivemind/config/models/v4p2-jev-links.json:2)

The implementation log records HTTP 402 failures beginning October 10 and subsequent extraction fallback. It establishes what happened then, not the account’s current balance. [IMPLEMENTATION_LOG.md:91–96](/Users/lchingen/tn-hivemind/docs/IMPLEMENTATION_LOG.md:91)

The later missing-key lesson is also accurately relevant: configured Jev/cascade operation was changed to refuse a missing credential rather than silently behave differently from replay. That is separate from payment failure. [IMPLEMENTATION_LOG.md:1928–1939](/Users/lchingen/tn-hivemind/docs/IMPLEMENTATION_LOG.md:1928)

## 3. Corrections to the plan, in line order

### Section 3: facts and proposed request

**Line 24 — “TypeSafe `jev-1.13.0` … up to 64 questions … ≤120 KB.”**

**Correction:** name 1.13.0 as the old integration’s pin. Refer to the current limits in §1. Do not present local wrapper restrictions as vendor restrictions. [Plan:24](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:24), [Old wrapper:24–43](/Users/lchingen/tn-hivemind/src/tn_hivemind/models/jev.py:24)

**Line 24 — “Each answer carries `probabilities` … `confidence`, `choice`.”**

**Correction:** this describes Choice only. Score and Noul have different fields, as shown in §1. Two-decimal precision is an old observation, not an established API guarantee. [Plan:24](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:24), [Primitive overview](https://docs.typesafe.ai/introduction), [Old validator:72–94](/Users/lchingen/tn-hivemind/src/tn_hivemind/models/jev.py:72)

**Line 25 — “about $0.00003 a call.”**

**Correction:** retain only as a historical average with its workload attached. It does not estimate an arbitrary batch. The token price remains consistent with the vendor’s current published price. [Plan:25](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:25), [Historical configuration:23](/Users/lchingen/tn-hivemind/config/models/v4p2-jev-links.json:23), [Published price](https://typesafe.ai/)

**Line 26 — “Not as the decider.”**

**Correction:** true of the selected tagging cascade; false as a description of all old Jev usage. The evidence cascade accepted high-confidence Jev labels directly. Also specify that only role/channel disagreement triggered tagging adjudication. See the two implementations in §2. [Plan:26](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:26), [effective_tags:599–619](/Users/lchingen/tn-hivemind/src/tn_hivemind/data/relations.py:599), [Old decision:968](/Users/lchingen/tn-hivemind/docs/DECISIONS.md:968)

**Line 27 — “Jev alone 81.2%, Luna alone 85.8% … 88.4% on test.”**

**Correction:** use the same test denominator: **56/69, 60/69, 61/69**. Give the tagging denominator as **221 matched positives**, with recall separately out of 302. Neither test measures grouping or identity. [Plan:27](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:27), [Evidence scorecards](/Users/lchingen/tn-hivemind/evals/bench-v1/results/relations-v4-r1.json:127), [Tag scorer:233–237](/Users/lchingen/tn-hivemind/evals/bench-x1/score_links.py:233)

**Line 28 — “the account needs payment before any call.”**

**Correction:** say that the last cited operational record reports payment failures. Present current status as unverified. The same correction applies to section 6’s payment prerequisite. [Plan:28,83](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:28), [Historical incident:91–96](/Users/lchingen/tn-hivemind/docs/IMPLEMENTATION_LOG.md:91)

**Line 30 — membership “is the shape Jev did well on”; identity “is the shape it did badly on.”**

**Correction:** replace both conclusions with hypotheses. Evidence-relation and business-role tests do not establish a membership-versus-identity capability boundary. The vendor’s entity-matching example further undermines a categorical claim that identity is unsuitable. It does not prove identity accuracy either. [Plan:30](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:30), [Old task definitions](/Users/lchingen/tn-hivemind/evals/bench-v1/SPEC.md:59), [Entity-alignment example](https://docs.typesafe.ai/cookbooks/entity_alignment)

**Line 30 — “calibrated probabilities, which a cross-encoder’s sigmoid does not give.”**

**Correction:** distinguish a vendor calibration claim from measured calibration on this task. A sigmoid alone does not guarantee calibration; neither does Jev’s product description. Neural classifiers can be calibrated after training. [Plan:30](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:30), [Guo et al.](https://proceedings.mlr.press/v70/guo17a.html), [Neural-ranker calibration](https://arxiv.org/abs/2101.04356)

**Line 32 — “one call decides up to 64 pairs for about $0.0001.”**

**Correction:** batching is appropriate, but neither the pair count nor price is fixed by this design. All target descriptions, instructions, and criteria contribute tokens. At the published price, $0.0001 buys about **2,381 input tokens**; a 20,000-token batch costs **$0.00084**. These are arithmetic examples, not token measurements. [Plan:32](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:32), [Fan-out](https://docs.typesafe.ai/patterns/fan-out), [Price](https://typesafe.ai/)

**Lines 35–40 — the JSON example.**

**Verdict: structurally valid under the documented text API.** The model remains accepted; Choice criteria are correctly objects; instructions are in the correct place. Parsing the printed JSON gives two questions, a **243-byte decoded state**, and a **1,387-byte compact request**. These are byte counts, not tokenizer measurements. State length is not a practical problem in this example. [Plan:35–40](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:35), [API schema](https://api.typesafe.ai/openapi.json)

**Line 38 — `does_not_belong`: “a different matter or a company’s own financial line.”**

**Correction:** the blanket financial-line exclusion conflicts with a scope that includes cloud-provider capital spending and revenue ramp-up. It can instruct Jev to reject the very capex memberships the plan expects. D165 permits an ordinary financial question to join an existing matter when appropriate; it is not a universal exclusion. Resolve the intended boundary in the gold before treating an answer as wrong. [Plan:38,70](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:38), [D165:2316–2321](/Users/lchingen/hivemind/docs/DECISIONS.md:2316)

**Line 39 — `part_of` versus `same_matter`.**

**Correction:** the descriptions overlap: a component quantity is also a different quantity within the same matter. The relation also describes candidate-as-part-of-target but leaves reverse containment unclear. This is a label-definition problem, not invalid JSON. A Choice needs distinguishable alternatives. [Plan:39](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:39), [Choice guidance](https://docs.typesafe.ai/primitives/choice)

**Line 43 — a key mismatch “turns `same` into `part_of` or `different`.”**

**Correction:** a key conflict can prohibit identity; it does not prove containment or unrelatedness. Different annual periods, for example, do not establish that one quantity is part of the other. The current matching guard rejects the merge; it does not infer either of those semantic labels. [Plan:43](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:43), [Identity checks:19–32](/Users/lchingen/hivemind/src/hivemind/views/identity.py:19), [Matching guard:302–313](/Users/lchingen/hivemind/src/hivemind/views/matching.py:302)

**Line 43 — “`belongs` above a threshold … `cannot_tell` … go to the matching call.”**

**Correction:** this is a coherent conditional policy, but specify whether the threshold applies to `probabilities.belongs` or `confidence`. Keep explicit `cannot_tell` separate from a low-confidence distribution. “As today” overstates continuity because Jev’s proposed membership routing is new. [Plan:43](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:43), [Confidence definition](https://docs.typesafe.ai/confidence), [D149:2172–2174](/Users/lchingen/hivemind/docs/DECISIONS.md:2172)

### Section 4: experiment and decision layer

**Line 61 — top-10 Luna with the new labels is “the control that is also the current method.”**

**Correction:** call this a comparison arm. Changing the candidate list, label set, and request changes the method. The existing matching request includes additional context and decisions; the unchanged pipeline remains the control. [Plan:61](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:61), [Current matching request:219–244](/Users/lchingen/hivemind/src/hivemind/views/matching.py:219)

**Line 61 — “104 calls, 1–3k tokens each, under $0.02.”**

**Correction:** the arithmetic is reasonable **if** the token assumption holds: approximately $0.0044–$0.0131. The unmeasured part is whether all pair questions fit that assumption. Count the complete serialized request, not only the candidate card. [Plan:61](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:61), [Price](https://typesafe.ai/)

**Line 61 — “Jev is deterministic … one call, one distribution.”**

**Correction:** one distribution per call does not imply the distribution repeats exactly. The vendor’s repeat experiment contains small numerical variation. Keep repeatability as something to measure, not an exemption from the repository’s sampling rule. [Plan:61](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:61), [Vendor repeats](https://docs.typesafe.ai/cookbooks/parallel_questions), [AGENTS.md:167–169](/Users/lchingen/hivemind/AGENTS.md:167)

**Line 62 — high score → `same`; middle → `same-matter`; low → `different`.**

**Correction: remove this interpretation.** A high membership probability means strong evidence of membership, not identity. A high confidence in `different` means strong evidence of difference. A Score can represent a deliberately defined ordered property, but does not make arbitrary relation labels into ordered truth levels. [Plan:62](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:62), [Score semantics](https://docs.typesafe.ai/primitives/score)

The key guard is also not general permission to merge. Current automatic identity requires the actual complete-key contract, including object, key version, scope provenance, and a concrete measure; matching additionally checks eligible targets. [identity.py:7–16](/Users/lchingen/hivemind/src/hivemind/views/identity.py:7), [matching.py:314–327](/Users/lchingen/hivemind/src/hivemind/views/matching.py:314)

**Line 62 — “zero or several, never exactly one.”**

**Correction:** presumably this means **never forced to choose exactly one**. Exactly one valid group must remain possible. Independent pair questions support zero, one, or several positive memberships. [Plan:62](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:62), [Independent questions](https://docs.typesafe.ai/introduction)

### Section 5: expected outcomes

**Line 70 — shared words imply the cross-encoder “should recover” or “should reject” particular items.**

**Correction:** these are untested predictions. Word overlap is not a reliable explanation of a semantic classifier’s outcome. Likewise, a card-only hit does not by itself prove memorized product knowledge. The source-assisted comparison is useful, but its result must decide the claim. [Plan:70](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:70), [Ditto’s contrasting high- and low-overlap examples](https://arxiv.org/pdf/2004.00584)

The observation that a fused group card can invite broad membership is logically reasonable. However, “splitting … needs pairwise scores … and a clustering step” names one possible approach, not a proven necessity. No split design needs to be selected in this review. [Plan:70](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:70)

**Line 71 — “an estimate from the old repository’s measurements.”**

**Correction:** call it an **untested hypothesis**, without importing the old percentages as expected membership performance. There is no measured transfer relationship between those tasks. The old role score also does not establish an identity ceiling. [Plan:71](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:71), [Old evidence labels](/Users/lchingen/tn-hivemind/evals/bench-v1/SPEC.md:71), [Old tagging questions](/Users/lchingen/tn-hivemind/src/tn_hivemind/data/relations.py:568)

**Line 71 — calibrated probabilities imply “the cascade is the design”; otherwise “only a recall-side filter.”**

**Correction:** calibration alone cannot select the architecture. The relevant quantities also include task errors, coverage, and the cost of a wrong action. Poor calibration does not logically make filtering safe; the old Jev mode reduced positive recall. [Plan:71](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:71), [Old recall results:87–96](/Users/lchingen/tn-hivemind/evals/bench-x1/results/links-test-final.json:87), [Ranking calibration research](https://arxiv.org/abs/2101.04356)

**Line 72 — every related-but-different pair ranks near the top; without the gate it “would merge.”**

**Correction:** neither outcome follows automatically. Rank order depends on the model and candidates; merging depends on the consuming decision rule. The correct point is that relevance alone cannot establish identity. The predicted “2 of 3” source-assisted result is a hypothesis, not a measured accuracy estimate. [Plan:72](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:72), [Retrieve-and-rerank distinction](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

**Line 74 — determinism “alone removes” membership variation.**

**Correction:** fixed scorer output can remove one source of variation for fixed inputs. It cannot remove variation caused by changing extracted cards, quotes, candidate lists, or later decisions. The proposed arms themselves distinguish different inputs. [Plan:61,74](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:61)

### Section 6: proposed pipeline effect

**Line 78 — “Nothing in extraction’s contract.”**

**Correction:** the extraction schema might remain unchanged, but final membership authority expands when another component can add groups. This is a product behavior change under D149/D166, not merely an implementation detail. [Plan:78](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:78), [D149](/Users/lchingen/hivemind/docs/DECISIONS.md:2170), [D166](/Users/lchingen/hivemind/docs/DECISIONS.md:2323)

**Line 78 — “model citation ∪ alias hit ∪ reranker hit.”**

**Correction:** this union can add memberships but cannot remove an existing wrong model or alias membership. Consequently, it cannot by itself deliver the earlier promised rejection of all forbidden memberships. This follows directly from the proposed set operation. [Plan:70,78](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:78)

**Line 78 — identity uses the model “in the abstain band.”**

**Correction:** this implies another component decides identity outside that band, contradicting line 30’s “Jev is the check” positioning. The owner must choose which authority is intended before the POC is described as a route to implementation. [Plan:30,62,78](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:30)

## 4. Literature on the positioning

### Is retrieval followed by a closed-set pair classifier recognized?

**Yes.** Dense or lexical retrieval can produce a shortlist, after which a model reads both sides and estimates a task-specific relation. Sentence Transformers documents retrieval followed by cross-encoder relevance scoring. Entity matching commonly calls candidate reduction **blocking**, then applies pair classification; Ditto is a clear example. [Retrieve and rerank](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html), [Ditto](https://arxiv.org/pdf/2004.00584)

A classifier and a reranker are not mutually exclusive categories. Sorting candidate pairs by the probability of the desired class makes the classifier act as a reranker. Applying a threshold then adds an acceptance decision. Probability-based ranking has a substantial literature, including explicit analysis of calibration and uncertainty. [Penha and Hauff](https://arxiv.org/abs/2101.04356)

There is also a close grouping precedent: Saravanakumar et al. combine document–cluster similarity with a neural decision about joining an existing cluster or creating another. Their representation is not the exact Jev card-pair design, so this supports the general pattern rather than validating this implementation. [Event-driven news clustering](https://aclanthology.org/2021.eacl-main.198.pdf)

### What performance ranges have been reported?

These metrics are deliberately kept separate. **Accuracy, pairwise F1, and clustering F1 are not interchangeable.**

| Task | Published result | Relevance and limitation |
|---|---|---|
| Duplicate-question detection, QQP | BERT-base **71.2 F1**, BERT-large **72.1 F1** on the official GLUE test evaluation | Task-trained pair classifiers; Table 1 explicitly reports F1 for QQP. These are not Jev forecasts. [BERT, Table 1](https://aclanthology.org/N19-1423.pdf) |
| Entity matching | Ditto: **75.58 F1** on Amazon–Google, **94.37** on Beer, **98.99** on DBLP–ACM, **100.00** on Fodors–Zagats | Wide dataset variation despite the same general method. These are trained matching systems, not generic relevance scores. [Ditto, Table 5](https://arxiv.org/pdf/2004.00584) |
| News-event clustering | Compared systems span **89.76–94.76 B-cubed F1**; the authors’ full system reaches **94.76** | Their dense-only variant reaches **68.98**, demonstrating that representation and task definition matter. These are event clusters, not overlapping thesis memberships. [News clustering, Table 1](https://aclanthology.org/2021.eacl-main.198.pdf) |

The literature supports **testing the pattern**. It does not support an expected accuracy number for this repository without its own accepted labels and evaluation.

### Known failure modes

- **Part-of versus same.** Event-coreference research explicitly distinguishes full identity from subevent relations. That supports keeping containment separate instead of treating it as weaker identity. [Araki et al.](https://aclanthology.org/L14-1725/)
- **Temporal differences.** The news-clustering paper reports incorrect merges without temporal information. In entity linking, source dates can exclude otherwise plausible namesakes. [News clustering](https://aclanthology.org/2021.eacl-main.198.pdf), [Historical entity linking](https://link.springer.com/article/10.1007/s10462-024-11102-9)
- **Popularity bias.** Historical entity-linking experiments measure systems preferring more popular entities over less common correct ones. This is evidence of a general risk, not a measured Jev defect on company stories. [Graciotti et al., Table 10](https://link.springer.com/article/10.1007/s10462-024-11102-9)
- **Similar wording with different identity.** Ditto’s examples include nearly identical product descriptions whose edition or grade changes the correct answer, and differently worded descriptions that identify the same product. [Ditto](https://arxiv.org/pdf/2004.00584)
- **Uncalibrated confidence.** Neural rankers can rank usefully while their numerical scores remain unreliable as probabilities. Conversely, calibration does not repair an incorrectly defined label. [Ranker calibration](https://arxiv.org/abs/2101.04356), [Classifier calibration](https://proceedings.mlr.press/v70/guo17a.html)
- **Jev-specific boundaries.** TypeSafe’s 1.13 guidance warns about numerical/date reasoning, indirection, distracting context, and option-order effects. These support keeping explicit numerical conflicts in code and measuring semantic judgments on the actual task. They are not quantified 1.14 failure rates. [Jev 1.13 limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13)

### Choice, Score, or one question per call?

For the plan’s unordered relation labels, **Choice is the appropriate starting type**. A binary membership question could use Noul; retaining an explicit insufficient-information category makes Choice reasonable. Score is appropriate only when the owner-defined property is genuinely ordered. The vendor’s entity example shows Score is possible, not mandatory. [Choice](https://docs.typesafe.ai/primitives/choice), [Score](https://docs.typesafe.ai/primitives/score), [Entity example](https://docs.typesafe.ai/cookbooks/entity_alignment)

Neither the API nor the old repository establishes a general requirement for one question per call. The old tagger already batches three. The important distinction is **one clearly defined judgment per question**, with the facts that judgment needs—not one HTTP request per judgment. [Old tagger:568–577](/Users/lchingen/tn-hivemind/src/tn_hivemind/data/relations.py:568), [Fan-out](https://docs.typesafe.ai/patterns/fan-out)

## 5. Decisions only the owner can make

1. **What counts as belonging to the matter?**  
   In particular, decide the capex boundary and whether the existing broad group is itself acceptable. The prompt currently contains conflicting answers. My lean: settle the gold definition before interpreting model errors. [Plan:38,70,82](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:38)

2. **What may Jev change automatically?**  
   Ranking candidates, flagging disagreements, adding memberships, and declaring identity are different authorities. My lean: evaluate membership directly, while keeping identity advisory unless a separate identity result justifies changing its authority. The old measurements do not settle this choice. [Plan:30,62,78](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:62), [Old results](/Users/lchingen/tn-hivemind/docs/BENCHMARK.md:190)

3. **Which errors matter enough to block adoption?**  
   Wrongly joining a group, missing a valid group, and wrongly merging two quantities have different consequences. The owner sets those acceptance priorities; the numerical threshold is then selected on dev. My lean: do not reuse 0.95 merely because an old, different task used it. [Old policy:595–618](/Users/lchingen/tn-hivemind/src/tn_hivemind/data/relations.py:595), [Threshold guidance](https://docs.typesafe.ai/confidence)

4. **Whether to commission the paid POC after these corrections.**  
   The current pipeline should remain the unchanged control. Any model version used should be explicit, and account readiness should be verified rather than inferred from an old payment incident. This review neither spends the proposed budget nor changes a default. [Plan:61,83–84](/Users/lchingen/hivemind/docs/research/2026-10-25-retrieval-poc/rerank-grouping-plan.md:61), [Historical payment record](/Users/lchingen/tn-hivemind/docs/IMPLEMENTATION_LOG.md:91)

*Delivery note: no repository file was edited. I could not save an output file because this session permits filesystem reads only, and no output-file path was supplied. The complete Markdown report is provided above.*