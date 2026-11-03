# Single-call extraction stability: controlled development study

2026-10-27. Alex requests repeated stability tests and correction of conflicting extraction instructions, using an analyst's judgement. Voting, unioning several answers, and retrying until a preferred answer appears are excluded. This is a development experiment, not a new whole-product acceptance standard.

Example: CoreWeave's backlog can inform NVIDIA demand without being NVIDIA revenue. The prompt must distinguish the evidential business relationship from the claim's literal subject and amount. The same source claim should remain available on repeated single calls, including claims that weaken the investment case.

## Scope and prior decisions

Baseline runtime and prompts are the current `hivemind-admission-v12-2026-10-26` worktree. Preserve its files and all existing ledgers. New research files live here; frozen inputs, runtime copy, raw HTTP request bodies, answers, logs and costs live in `poc/reports/2026-10-27-extraction-stability/`. No default switch or resumption of the three-month run is implied.

Main D62 says: “Extraction variance is fixed in the prompt, not by sampling several times.” The admission worktree's D193 says: “Sampling several times per item is ruled out on cost.” Repeated calls here measure each independent answer; they are never combined into a production result. The current user request explicitly reopens prompt testing after admission-worktree D193/D194 closed earlier arms. D162's earlier two-call experiment failed end to end; this study keeps one call and the existing output schema. Candidate admission, grouping, matching, judging, UI, universe and trading behaviour are out of scope.

## Established diagnosis before changes

The prior audit script is `/private/tmp/hivemind-extraction-audit-2026-10-27.KoEsmk/audit.py`. It read all 1,553 extraction calls and all 98 scratch calls. Thirty fresh controls have matching canonical hashes, but JSON key sorting changed schema generation order: all original answers have evidence before candidates; all scratch answers have candidates before evidence. The nested evidence fields also changed from quote-before-links to links-before-quote. The test must reconstruct the writer's schema and prove value equality while preserving its property order. A sorted-schema control must be detected as changed even though its old hash is equal.

All 363 first-versus-last repeated-article requests differ: 349 changed shown theses, 294 changed research groups, 361 changed schema values. These pairs do not isolate sampling. The existing benchmark also counts a quote's first 120 normalized characters as identity; splitting or extending a quote can therefore look like a missing fact. Evaluation below tracks source claims independently of packaging.

The full CoreWeave request contains 7,458 system characters, 31,345 user characters and a 3,560-character serialized response-format object. Its 15,298-character page has 9,060 characters before the first reporting paragraph, a 3,141-character article window including interleaved recommendations, and 3,097 characters after it. The empty scratch answer is call 19: normal stop, 318 completion tokens including 292 reasoning tokens, against an 8,000-token cap. No truncation explains that answer.

Prompt tension: default-retain every statement; treat customer deployment as supplier evidence; link only directly concerned statements and omit indirect relationships; do not infer revenue. The missing distinction is that a source-grounded driver can bear on the outcome without stating or determining the outcome itself. A large answer is not intrinsically better, and no evidence count is a quality target.

## Fixed design

Use the three existing benchmark articles: CoreWeave `gnews:011203b517e045ffe773b1fb`, Motley Fool `gnews:dadd84590540a466aea01b3c`, Rest of World `gnews:01a49ffd41f6abe24538da65`. Reconstruct each original request from its archived message strings and current writer schema, asserting dictionary-value equality to the archived schema. Freeze the runtime before any live call. The new sender saves and hashes the exact bytes it passes as the HTTP request body; it must not use the existing sorted-key HTTP study helper.

A 2-by-2 comparison isolates instruction and page-noise effects: baseline versus analyst prompt, crossed with original page versus reporting-text-only page. Five independent single calls per cell and article: 60 calls total, interleaved by article and repetition with rotated cell order, at most two calls in flight. All cells use the original model, low reasoning, original output cap, identical schema property order, existing theses and groups. No temperature or seed is added.

The reporting-text-only input is an experimental upper bound on removing page furniture, not an untested production parser. A frozen list of original character spans retains the complete reporting text, title and byline, including arguments in both directions, and excludes menus, quote widgets, advertisements and related-story headlines. Every retained span must match the original exactly. Claim coverage is checked against both versions before calls.

The analyst prompt puts evidence selection before candidate construction, removes the conflicting default-retain and indirect-only statements, and defines relevant evidence by a source-grounded business driver. It preserves factual attribution, conditionality, original subject, units and period; it makes “not a new thesis” independent from “not useful evidence.” It does not name the three companies/articles/amounts as examples. Existing candidate-admission and group contracts stay intact. Record exact character counts and actual input/output token counts; any growth needs a reason before sending.

## Measurement fixed before calls

Create assistant-labelled source-claim annotations before viewing the new outputs. Each annotation has a source span/anchor, importance, required business meaning and acceptable direct destinations. Distinguish core thesis-relevant claims, other relevant claims, and page furniture or unrelated material. Mark unresolved borderline claims as unjudged; do not silently count them as noise or remove them from the report. Historic judge citations are diagnostic context, not gold.

For every answer report: core claims preserved in valid evidence; source-claim coverage across all annotated relevant claims; retained subject/number/unit/period/attribution; exact destination sets; schema and quote refusals; unexpected candidates; and newly extracted claims outside the annotations. Quote splitting and merging never create extra credit. A claim counts at most once per answer. All nonidentical summaries and destinations receive semantic review, including the largest coverage swings.

Stability is the per-claim pattern over five answers, reported together with correctness. Always omitting a core fact fails correctness even though it is stable. The principal development comparison is the number of core facts correctly present in all five calls, the worst-call core coverage, and variation in meaning or relevant destination. Report every sample. Do not treat the 10 pairs from five draws as 10 independent trials. No claim of population reliability, complete recall, or universal prompt improvement follows from this sample.

The 60 calls are one predeclared diagnostic comparison. Do not tune the labels, add an arm, or add samples after seeing its results. If no cell gives stable, correct core coverage, report the remaining mechanism and its cases rather than declaring success. If a candidate clearly improves this workload, preserve it as a tested research prompt; wider validation and a default switch are separate decisions.

## State × event

| State | Event | Transition and record |
|---|---|---|
| Unprepared | Missing source/schema mismatch | Refuse before network; identify input |
| Prepared | Static controls and preflight pass | Freeze manifest, labels, spans, prompt and runtime; pin source publication dates |
| Prepared | File changed after freeze | Refuse using content hashes |
| Ready | Scheduled single call | Save ordered request bytes and attempt identity before dispatch; reserve cost in a new study journal |
| In flight | Valid answer | Save raw response and actual usage; run original schema/quote/link checks; never merge with another answer |
| In flight | Schema/semantic refusal | Retain the answer and its failure in that sample; no replacement draw |
| In flight | Transport failure/crash | Hold unknown charge; stop admission; retain in-flight outcomes and logs; no automatic retry |
| Running | User stop | Stop new calls; preserve completed/in-flight results |
| Finished | Analysis | Read-only analysis over every scheduled sample, including failures |
| Finished | Another run/date/configuration | New dated study; no overwrite or append-to-repair; existing production state is untouched |

## Values × writers × readers

| Value | Writer/source | Readers and contract |
|---|---|---|
| Ordered request body | Study sender from frozen request | HTTP sender and audit use the identical bytes; SHA256 includes property order |
| Legacy canonical identity | Existing model helper, diagnosis only | Shows original request value equality; never claims byte equality |
| Clean reporting spans | Manual source review before calls | Input builder and coverage proof; no invented or edited article wording |
| Claim labels | Assistant source reading | Scorer and semantic reviewer; not embedded in prompts |
| Raw answer/usage | Provider | Archive, original checks, scorer, cost accounting; no silent truncation or answer substitution |
| Candidate/evidence fields | One model answer | Existing schema/sift; downstream storage is not exercised or changed |
| Prompt candidate | This research slice | Experimental cell only; no production configuration reads it |

## New paths × old checks

| Path | Checks |
|---|---|
| Reconstructed baseline | Same messages/settings/schema values, original property order; detect sorted-key mutant |
| New prompt | Same schema and existing candidate admission; quote, link, date and group checks unchanged |
| Clean page | Every selected span is original text; all labelled claims still occur; same metadata/context |
| Claim scoring | Real stored positive examples and omission/wrong-number/wrong-link mutants; zero or unidentifiable population refuses |
| Live sender | Single-attempt HTTP, no automatic resampling; existing conservative journal with a $1.50 maximum for this small study and a 60-attempt ceiling; do not touch earlier budgets |
| Preflight | Run `scripts/preflight.py` against a copy of the relevant item database and matching ledger before paid calls; diagnose every refusal relevant to study samples |

Review this design and frozen annotations before implementation/live calls. Verification ends with the research checks, existing affected tests/full suite as applicable, the documentation reasoning refresh and `python3 docs/check.py`.
