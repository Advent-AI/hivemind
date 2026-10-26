# Idea card: read a user's idea against the thesis library

D112–D145; English edition and current-document refresh, October 25, 2026 (D163). A user supplies an **idea**; the library contains **theses**. The service reads the idea against those records and returns the information the frontend needs. User text does not become a stored thesis merely by opening an Idea card.

The default is `poc/config/poc-v32-idea.json`: two candidate-discovery calls (`idea-v7`) followed by one final adoption and weighting call (`idea-summary-v7`, D196). The model/provider and reasoning settings are unchanged. Older configurations, including v31, retain their original response contracts.

## Request path

```text
User idea → POST /ideas → coverage search
                         ├─ no recorded coverage → return null reading
                         └─ model call 1: typed parts and an explicit dollar claim
                            → code searches each part
                            → model call 2: map parts to supplied theses and explain
                            → code validates IDs and claim, reads related theses
                            → configured assessment: adopt and weight theses, write analyst TLDR
                            → return Idea card, evaluation and optional thesis bundles
```

The browser never receives a model credential. The route runs in the service, keeps no user account or commitment, and returns a complete per-request result. Model calls are archived; the same exact request can replay from the archive. A changed library or request is not automatically an identical cached call.

### Live progress

D187 adds optional streaming to the same endpoint. `Accept: application/x-ndjson` returns newline-delimited `progress` records with a `stage`, followed by one `result` record with the existing response in `data`. A handled failure returns an `error` record with `status` and `message`. Ordinary JSON callers keep the existing response. The [progress contract](../research/2026-10-26-library-ui/idea-progress.md) owns the stage boundaries and pending UI. These are public task steps, not model reasoning. Prompts and model-call count do not change.

## Model and code responsibilities

Call 1 returns two to four typed parts: subject in `object`, figure/event in `looks_for`, period and search query. The first part is the idea's main question. A claim is present only for an explicit US-dollar amount, with part index, comparator and full-dollar value.

Code searches each part using the model's query and a canonical query composed from subject, focus and period. It interleaves the two result lists without duplicates and supplies candidate briefs. Where semantic search is available, the parts' query embeddings are batched in one round trip.

Call 2 maps each part to supplied candidates as `direct`, `driver` or `context`, writes a per-part reason and a short summary. The adopted driver definition includes causes or consequences. The service does not use the unadopted `idea-v10` causal-clause requirement. It preserves only allowed candidate IDs; it reports dropped choices.

The final assessment receives candidate theses, their dated states and endpoint conditions. It returns a variable-length list of adopted IDs, each with a positive impact percentage, endpoint and explanation. Omitted candidates are not Idea associations; the JSON has no zero-weight or excluded branch. Code checks IDs, uniqueness and a 100% total, reverses lower-claim direction once and projects all associations onto the adopted set. A provisional claim/evaluation whose direct thesis is omitted is cleared. The model cannot invent IDs or the calculated composite score.

Code selects the first part's direct thesis only from records the model called direct, using that part's search order and the existing year compatibility rule. It does not choose a different financial measure based only on subject/year. The current rule accepts a following fiscal-year label for a calendar-year query; that heuristic is not proof of exact period equivalence.

In the current configuration, only the final positively weighted set goes to the canvas; code imposes no thesis-count quota and appends no dependency neighbours. Candidate discovery does not itself establish final associations. Historical configurations retain their prior cap and related-thesis behavior.

A share-price, market-cap or valuation part is treated as a market reading and is not evaluated against business-figure ladders. A claim must name an existing part, state an amount in the original idea and have a direct thesis. Code evaluates the claim against that thesis's numeric ladder; a driver is not a substitute for the named quantity.

## Response and consumers

| Field | Content | Consumer |
|---|---|---|
| `idea` | Original text and `as_of` day | Idea heading/context |
| `search` | Mode and initial candidate IDs | Trace/debug display |
| `reading` | Summary, typed/mapped parts, chosen IDs, claim, dropped choices, search trace and language-slip count; null for no coverage | Idea adapter and card |
| `reading.composite` | Version, method, requested date, named target/direction, adopted representatives with supporting endpoints, positive impact percentages and reasons; older versions retain their own fields | Composite chart, per-Idea card weights and calculation detail |
| `reading.parts[]` | Subject, focus, period, query, candidates, direct/driver/context IDs, selected direct ID, market-reading flag and reason | Coverage explanation; does not create ledger records |
| `evaluation` | Numeric verdict or null | Claim display |
| `related[]` | Related thesis ID, `via`, upstream/downstream relation, direction and current judgement | Graph edges |
| `views[]` | Complete dated bundles for chosen and related theses, unless disabled | `fromIdeaResponse` and shared thesis components |
| `days[]` | Completed ledger days visible at the requested date | Replay/date controls |
| `no_recorded_view` | Whether initial coverage search returned null | Distinguish no coverage from no relevant choices |
| `cost` | USD estimate, tokens, seconds, cache status and calls | Operator measurements |

Existing field names containing `view` mean **thesis**. They remain stable compatibility names, not a second concept.

## State × event

| State/event | Result |
|---|---|
| Empty idea | Refuse with an input error |
| No recorded coverage | Null reading/evaluation, no chosen bundles and no Idea model call |
| Coverage exists, no suitable mapping | A reading can explain the gap with an empty chosen set; distinct from null coverage |
| Missing Idea configuration | Refuse; do not silently switch models |
| Model supplies unlisted thesis | Drop and report it; do not read an invented ID |
| Market reading or no direct thesis for a claim | Do not evaluate against an unrelated business ladder; report the reason |
| Chinese prose in checked output fields | Existing D133 behavior: ask once more for English, count slips; the second answer is retained even if still non-English |
| Historical day requested | Searches, judgements, graph and bundles use that day |
| Concurrent requests | Request-owned database connections; shared ledger remains read-only |
| Bundles disabled | Return the card without heavy bundle content; the caller may fetch `/thesis-bundles` |

The existing English retry checks selected prose fields, not every possible source field. It is not a blanket proof that an entire response is English. Quotes and historical research text can remain in their original language.

## Frontend integration

`src/idea/idea.js` posts the input; the bundle adapter validates returned theses and `graphOf` draws each adopted thesis directly from the Idea. Historical responses can retain explicit related links. The shared card, chart and connector rules are owned by the [Thesis UI design](thesis-ui.md).

The Idea card previews `reading.summary`; clicking the card or pressing Enter/Space opens analysis (D184/D186). There is no separate View analysis button. Its drawer uses the shared Thesis-style tabs: Overview contains the full summary and adopted theses; Trace contains reading steps and excluded choices; Response displays the structured response directly (D214). Search trace is not rendered as a separate interface section; its original fields remain available in Response (D217). This is the service’s returned analysis, not a private internal reasoning stream. The detail header shows an `AI confidence: xx%` pill, then `| Idea created: date`, using the shared Thesis metadata style. Confidence follows the selected assessment date. Creation is the browser-local day captured for that UI submission, not the library `as_of`; legacy callers without a creation day show `Not recorded` (D203). In Trace, all reading steps are expanded by default. There is no Search trace section below the reading steps (D217). Expanding a step uses the shared Thesis disclosure control and reveals the complete stored explanation and matched theses (D210). Opening it makes no model call. Tabs switch locally with click or arrow/Home/End keys, reset content scroll, and make no requests. A newly opened Idea starts on Overview. A new submission or leaving the Idea view closes the prior detail.

No redundant decomposition table is placed inside the Idea card. The legacy browser-only matcher has been removed. Components do not call a model or infer new group associations. See the [integration guide](../../poc/ui/README.md).

## Idea confidence

Every covered Idea in the default configuration returns a composite plan. The frontend does not match question text against a registry. The final assessment selects adopted representatives for distinct economic drivers, accounting for overlapping revenue and spending measures by omitting redundant candidates from the plan. It chooses by relevance rather than a favourable current score. Older plan versions can include explicit exclusions; the default positive-selection format does not.

Each adopted thesis has a `weight_percent` from 1 to 100 and a `weight_reason`. A nonempty plan must total exactly 100%; omitted candidates do not appear in it. Code aligns the endpoint with the claim direction and sums weight/100 times the signed score. Binary endpoints remain +2/-2. If an adopted thesis has no assessment on a historical date, that date has no score; its weight is not reallocated. An empty adopted set has no score. Legacy plans retain their previous behavior.

The Idea chart title is “AI confidence”, displayed on a 0–100% scale. Code converts the weighted aggregate with `50 + 25 × aggregate`: −2 maps to 0%, neutral maps to 50%, and +2 maps to 100%. The chart draws at the Idea card’s content width; its subtitle and vertical-axis text match the Thesis chart, and the card fits its content with normal bottom padding (D202). The compact pill rounds to a whole percentage; the analysis header uses the same rounded confidence. The adopted-thesis section is titled “Theses”, without a help icon or popup (D212); the numerical contribution table remains omitted. The redundant confidence/count/date row is omitted. Each adopted-thesis explanation starts with its weight badge followed by the full question. The detail badge has 4px corners and stretches to the title height (D209/D211), then separate relevance and weight-rationale paragraphs. Their labels use black, semibold body-sized text; major sections and consecutive thesis blocks use the shared Thesis-detail divider and spacing; only the first thesis has no leading divider (D207). Every associated Thesis card shows a scale icon and `xx%` at the upper right, with the icon vertically centred against the number and no tooltip (D200). Idea thesis cards and explanations appear in descending impact-weight order; equal weights retain the response order. The chart applies the current plan to historical thesis states; it is not a record of earlier plan choices or an outcome probability. The detail drawer lists the same adopted set and its weight rationale. Candidate IDs remain in search trace only. Exact-request replay retains the chosen weights; fresh model choices may differ.

The [D196 contract](../research/2026-10-26-library-ui/positive-weight-selection.md) owns the current positive-selection format. D194 and D188 remain historical contracts; old configurations and explicit trials stay readable.

## Historical measurements and limits

These measurements belong to the original October 24–25 runs, not the English conversion. Full samples and experiment history remain in the linked source and tuning log.

| Criterion | Measured result | Interpretation |
|---|---|---|
| New-idea latency target ≤6 seconds | Full contract 10.9 seconds; lean alternative 8.6 seconds; earlier serial baseline 20.4 seconds | Target not met; the full contract remains adopted |
| Cost target ≤$0.005 per idea | Full $0.0098; lean $0.0070; earlier $0.012–0.013 | Target not met; no automatic budget/model change |
| First direct thesis consistency | Full 8/8 sampled ideas; lean 7/8 | Sample result, not a universal guarantee |
| Canvas Jaccard target ≥0.8 | Full 0.65 development / 0.68 held-out | Target not met; varying parts, retrieval and driver choices contribute |
| Lower driver cap simulation | Two drivers: 0.67/0.76 overlap, wanted-driver recall 0.65→0.56 | Tradeoff measured, not adopted |
| Second mapping call simulation | 0.73 overlap at another call's cost | Not adopted |
| Share-price claims | Zero after the code guard in the measured set | Keep the semantic regression check |
| Wrong direct ladder for claims | 0/13 after respecting the model's direct label | Earlier subject/year-only rule was removed |
| Language slips | Two in 49 ideas, both re-asked | Checked-field behavior, not proof of all-field language quality |
| Model-authored 20-idea gold | Correct direct 18/20; two traps; median wanted-driver recall 65%; canvas noise 22%; claim evaluation 20/20 | Gold is an analyst-model reading, not Alex's own labels |

The adopted full contract retains per-part reasons because measured no-reason variants were less stable. Those measurements cover the earlier two-call flow. The current default adds a final adoption/weighting assessment; its three stages, retrieval coverage and semantic errors remain limitations. Older agent-loop counts, speedups and approximate floors are historical environment measurements, not promises for current hardware or providers.

D186 preserves the original two mapping requests and adds the isolated TLDR after selection. Its focused development comparison and measured cost/latency are in [the TLDR report](../../poc/reports/2026-10-26-analyst-tldr/results.md); this does not establish broad Idea matching quality or meet the historical whole-flow latency target.
