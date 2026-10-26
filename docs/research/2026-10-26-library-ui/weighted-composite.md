# D194: explicit Idea impact weights

Historical contract: D196 supersedes its zero-weight/exclusion representation. The current contract is [positive-weight selection](positive-weight-selection.md).

Alex requested model-returned impact percentages for the connected theses, visible in their card headers, summing to 100%, with deterministic weighted composite history. This replaces D188's equal-weight rule, not its fixed selection or endpoint direction rules.

## Scope and existing path

One final assessment call currently chooses representatives, endpoints and exclusions. Its schema/binder reject weights; the shared browser calculator averages representatives. The graph header does not receive any per-Idea weight. These are the three owners changed here. Preserve the first two mapping requests, extraction, library/group storage, provider/model and source databases. No 0–100 probability conversion, new Idea persistence system, historical re-selection or extra model call.

The existing three-thesis Data Center response contains two representatives (v3 and v1) and one overlapping exclusion (v9). Its existing value is +0.50. A stored-input fixture with 70% on neutral v3 and 30% on +1 v1 must calculate +0.30, not +0.50. These fixture weights test arithmetic and are not a claim that the model should choose them.

## Contract

- New immutable config `poc-v31-idea`, prompt `idea-summary-v6`, same Luna and reasoning settings. `reading.composite` becomes `idea-composite/3`, method `weighted`.
- Keep the keyed response: one required disposition per selected thesis ID. Each representative adds integer `weight_percent` (1–100) and `weight_reason`; excluded entries explicitly carry zero. Positive weights sum to exactly 100 whenever there is a representative; an empty plan has total zero and no score. Reject invalid totals, never silently normalize or repair them.
- Weight measures importance to the named Idea outcome and horizon, independent of today's favourable/unfavourable state. Preserve one representative per distinct economic driver and explain excluded overlap. Existing endpoint fields and code-owned lower-claim reversal remain unchanged.
- The model archive preserves the exact returned weights. A given response keeps the same weights during replay. The curve applies this current plan to past thesis states; it is not a record of past Idea plans.
- At day t: sum `weight_percent / 100 * direction * state_score(t)`. Binary endpoints remain +2/-2. If any positive-weight thesis has no assessment yet, return an unavailable value for that day; retain its missing weight and do not reallocate it. Empty plans are unavailable. Legacy equal-weight responses retain their previous calculation.
- Display the percentage in each connected Thesis card's upper-right header on the Idea canvas only. Exclusions and graph-only related theses show 0%; library cards have no per-Idea weight. The existing score pill remains beside AI score. The analysis drawer shows weights, signed contributions, weight reasons, exclusions and missing coverage.

## State × event

| State/event | Transition, writes and date |
|---|---|
| Before submission / pending | Existing progress; no invented weights |
| Final call succeeds | Validate complete keyed plan and total, bind IDs/questions/as_of; archive actual response |
| Invalid total, range, type, omission or unknown ID | Reject response; existing error state; no fallback or normalization |
| Transport/schema refusal or retry failure | Existing service error; do not display stale previous weights |
| Interruption during submission / new input | Existing request ownership and cancellation; only current request can render |
| All representatives assessed at replay date | Calculate exact weighted sum from states at or before that date |
| One or more assessments missing at replay date | Null score; retain weights and available contributions for explanation |
| No relevant representatives / unclear direction | Zero total, null score, 0% excluded connections |
| Replay / range change / reopening detail | Reuse returned weights; no new model call or re-selection |
| Later date / new config / changed selection | New exact request and response; no mutation of earlier archive rows |
| Concurrent requests / two Ideas sharing a thesis | Each response owns its weights; no weight written into the shared thesis |
| Crash before response render | Source library unchanged; existing archive replay reconstructs completed model calls |
| Legacy response/config | Existing v1/v2 behavior; no invented displayed percentages |

## Value × writer × reader

| Value | Writer / input | Readers |
|---|---|---|
| Weight and weight reason | Final Luna JSON; new schema and binder | API result, browser validator, calculator, card header, analysis drawer |
| Zero exclusion weight | Final Luna JSON checked by code | Graph labels, analysis, complete-total check |
| Endpoint and direction | Existing final call / code reversal | Weighted calculator and contribution explanation |
| Plan version, method, question, date | Binder from code/selected records | Browser validator and archive replay |
| Weighted value and contributions | Shared browser history calculator | Idea pill/chart and detail table |
| Per-Idea header percentages | Bootstrap passes validated response weights into graph | Thesis card renderer; never library data |
| New default config | API default and development launch | Service model calls; old configs stay immutable |

## New path × existing checks

| Check | Weighted path |
|---|---|
| Identity, complete partition, endpoint enum, polarity | Reuse existing binder before binding weight metadata |
| English prose and escaped UI text | Include weight reasons in checked prose; retain escaping |
| Model schema vs local checks | Integer/range checks and exact-sum check at binder; browser revalidates API boundary |
| Historical cutoff / binary scoring | Existing dated state lookup; apply fixed weight without renormalizing |
| Unchanged mapping / no fourth call | Compare exact first two requests and selected IDs in a real-storage test |
| Cached response / source isolation | Replay from exact archived request; all protected source hashes unchanged |
| Card header / graph routing / range | Optional per-Idea metadata; dimensions and routing unchanged |
| Legacy adapters and manual trial | Old paths and tests remain unchanged |

## Verification and model audit

Before live calls, run the repository preflight on the English archive and copied items database; additionally replay stored Idea answers through their original schema/binder. A changed model contract does not make old answers invalid under their original version. Test the weighted schema and calculator with a minimally edited stored three-thesis response, negative polarity, invalid totals, empty plan, missing states and later evidence. Mutants must fail for equal averaging, omitted total validation and missing-state renormalization.

Review the whole final request. Replace the equal-weight sentence, preserve polarity instructions and use a concise explanation of impact weighting; report prompt characters and request tokens before/after. Do not grow unrelated instructions. Use the real stored Data Center context, three fresh controls and weighted candidates, one pair before continuing. Negative polarity is checked on stored-input unit cases. Same model/provider, no retries in the experiment, maximum six calls and $0.035 additional conservative reservation within the existing $0.10 Idea experiment ceiling. The initial two-context proposal reserved $0.036985 using the conservative byte bound; it was reduced before any paid request, without increasing the cap. Record actual responses, totals, direction, reasons, cost and latency. No guarantee of identical discretionary weights across fresh samples; fixed accepted plans must calculate identically.

Self-review against the tables: selection changes, related 0% cards, missing historical states, legacy responses, invalid totals, negative ideas, replay and shared-library ownership are covered. No unresolved contract choice remains. Final verification includes browser headers, sum, contribution table, replay, UI and Python suites, source hashes, reasoning refresh and docs/check.py.

Transport recovery: the sixth attempted sample failed inside TLS `do_handshake`, before HTTP headers or body could be sent. Five completed answers are retained. Recover only that unissued request after a connection health check, requiring its archive to be empty. The six completed-model-call limit and $0.035 ceiling remain unchanged; this is not a repeat of a model answer or a semantic retry.

## D195 clarification

Alex explicitly wants the model to choose the participating theses and their weights. Fresh-sample allocation differences are not a reason to force a particular basket or allocation. Do not add the proposed horizon-based inclusion rule or another tuning arm. The v31 path removes the legacy three-driver display cap while preserving identity and percentage validation. The six completed D194 samples are retained as returned.
