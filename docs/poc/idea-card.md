# Idea card: read a user's idea against the thesis library

D112–D145; English edition and current-document refresh, October 25, 2026 (D163). A user supplies an **idea**; the library contains **theses**. The service reads the idea against those records and returns the information the frontend needs. User text does not become a stored thesis merely by opening an Idea card.

The adopted design is the full **two-call** flow, `poc/config/poc-v9.json` with `idea-v7` and reasoning effort `none` (D135/D145). Earlier one-call and agent-loop implementations and measured alternatives are retained in the [historical document](../research/2026-10-25-english/idea-card.original.md) and [tuning log](idea-tuning-log.md). Newer filenames do not imply adopted behavior. D163's English prompt candidate is not yet activated.

## Request path

```text
User idea → POST /ideas → coverage search
                         ├─ no recorded coverage → return null reading
                         └─ model call 1: typed parts and an explicit dollar claim
                            → code searches each part
                            → model call 2: map parts to supplied theses and explain
                            → code validates IDs and claim, reads related theses
                            → return Idea card, evaluation and optional thesis bundles
```

The browser never receives a model credential. The route runs in the service, keeps no user account or commitment, and returns a complete per-request result. Model calls are archived; the same exact request can replay from the archive. A changed library or request is not automatically an identical cached call.

## Model and code responsibilities

Call 1 returns two to four typed parts: subject in `object`, figure/event in `looks_for`, period and search query. The first part is the idea's main question. A claim is present only for an explicit US-dollar amount, with part index, comparator and full-dollar value.

Code searches each part using the model's query and a canonical query composed from subject, focus and period. It interleaves the two result lists without duplicates and supplies candidate briefs. Where semantic search is available, the parts' query embeddings are batched in one round trip.

Call 2 maps each part to supplied candidates as `direct`, `driver` or `context`, writes a per-part reason and a short summary. The adopted driver definition includes causes or consequences. The service does not use the unadopted `idea-v10` causal-clause requirement. It preserves only allowed candidate IDs; it reports dropped choices.

Code selects the first part's direct thesis only from records the model called direct, using that part's search order and the existing year compatibility rule. It does not choose a different financial measure based only on subject/year. The current rule accepts a following fiscal-year label for a calendar-year query; that heuristic is not proof of exact period equivalence.

At most three drivers per part go to the canvas; excess drivers become context. Direct and retained driver IDs form the chosen set. Related theses come from the actual dependency graph around the first part's mapped theses, with `via` preserving their source. No graph grouping or hierarchy is inferred from list order.

A share-price, market-cap or valuation part is treated as a market reading and is not evaluated against business-figure ladders. A claim must name an existing part, state an amount in the original idea and have a direct thesis. Code evaluates the claim against that thesis's numeric ladder; a driver is not a substitute for the named quantity.

## Response and consumers

| Field | Content | Consumer |
|---|---|---|
| `idea` | Original text and `as_of` day | Idea heading/context |
| `search` | Mode and initial candidate IDs | Trace/debug display |
| `reading` | Summary, typed/mapped parts, chosen IDs, claim, dropped choices, search trace and language-slip count; null for no coverage | Idea adapter and card |
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

`src/idea/idea.js` posts the input; `fromIdeaResponse` validates and converts the response to `thesis-ui/1`; `graphOf` supplies explicit roots and edges. Every chosen thesis connects directly to the Idea. A related thesis connects through its `via` source. The shared card header, drawer, chart and connector rules are owned by the [Thesis UI design](thesis-ui.md), not reimplemented here.

No redundant decomposition table is placed inside the Idea card. The legacy browser-only matcher has been removed. Components do not call a model or infer new group associations. See the [integration guide](../../poc/ui/README.md).

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

The adopted full contract retains per-part reasons because measured no-reason variants were less stable. The route's two serial model calls, retrieval coverage and semantic errors remain limitations. Older agent-loop counts, speedups and approximate floors are historical environment measurements, not promises for current hardware or providers.

No new tuning arm is authorised by this document. D163 must first preserve the adopted contract while translating terminology and verifying old/new data readers. English model quality requires a separately registered comparison; static translation and cached replay cannot establish it.
