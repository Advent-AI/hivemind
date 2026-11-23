# Step 2 score experiment — design for review

Alex asks whether sending embedding similarity to Jev helps, given existing high retrieval recall and merge quality. This is an isolated fixed-history diagnostic, not a product change, adoption, a fresh held-out acceptance, or a comparison of search recall. Prior recorded acceptance 141/143 is search recall, 1/57 clearly wrong merges is not recall of Jev's repeat decisions. The fresh frozen reference and old labels do not change. Start with 11 archived c8 fresh comparison requests, selected before sending, covering the clearly wrong merge, disputed overlaps, accepted repeats, and new-evidence controls: `22:ev-11`, `13:e11`, `38:ev-2`, `18:e2`, `43:e3`, `3:e1`, `9:e6`, `14:e3`, `5:e1`, `9:e1`, `19:ev-guidance-70`. Two arms times three draws = 66 calls, with the original candidate sets and state fixed. This is a selected diagnostic and cannot measure overall precision or recall. A larger comparison is considered only if the cheap probe reveals a useful signal (AGENTS §7.3); the raw articles are already used, so neither probe is fresh acceptance.

## What is sent and why

C control: exact archived model/state/questions. T: each candidate instruction adds a newline and factual metadata: `Retrieval metadata (not part of the stored piece; cosine, not a probability): query 1 [thesis search]: 0.xxxx; query 2 [own-text search]: 0.xxxx`. Each query corresponds in order to the existing caller's query_vectors; its label and query type are made explicit without disclosing thesis text otherwise not sent. Include a score for each query, including non-retrieving queries; retrieval origins are recorded in the manifest, not sent. Jev returns no textual reasoning, so do not infer why its choice changes. Query type labels expose information C did not have, so any observed effect is the joint effect of score metadata and labels. No shuffled-score arm: it would describe intentionally incorrect scores as real, and its interpretation as a formatting control is uncertain. The test compares the practical intervention of adding real scores against the current request; it does not establish how Jev uses the numbers. Freeze this representation; do not infer importance from cosine or set thresholds. Decimal precision 4, cosine computed with existing compare.py and cached exact text vectors. Retrieval always uses original queries, no candidate changes. User requests testing this candidate, not deployment or any new rule.

## State × event

| Event | State and action | Date/time |
|---|---|---|
| Preflight | Read archives read-only; use the separate offline census for all 185 request bytes and answers, then reconstruct the 11 selected cases and their historical candidate lists; compare identity and score reconstruction. Abort on missing keys, candidates, requests or inconsistent data. | No wall-clock data in requests |
| First send | Separate research archive for each arm/draw; interleave all 6 requests per case in fixed seeded order; fresh transport, no archived cache hit. | Same day for all arms; timestamps metadata only |
| Transport failure | Record actual error; exactly one transport attempt; a lost reply remains ambiguous and the experiment stops; no replacement or analysis as different. | No date decision |
| Crash or interruption | Journal dispatch with flush and fsync; on any interruption stop and inspect, with no automatic resume or re-send. A dispatch without completion is ambiguous. | Save identifiers, not wall-clock ordering |
| Completed response | Validate with current Jev validator; record raw response and costs; malformed/refusal stops case and is reported. | Original dates stay unchanged |
| Analysis | Compare each request on fixed original library; no advance to newly grouped state; reviewed changes and controls with source, not self-scorer claims. | Historical source dates preserved |
| Later run/config change/another writer/two scopes | Refuse existing output on rerun absent exact frozen manifest and explicit resume; do not access live data or concurrent Step 1 writes. Different scopes use different research directories and archives. | No runtime time used as identity |

## Values × readers

| Value | Origin | Reader | Consequence |
|---|---|---|---|
| query and record text | saved Step 1 trace | existing query construction, Jev | Preserve bytes and record identity |
| query-to-group cosine | cached embeddings and current cosine | T Jev question only | Keep query provenance; numeric score is not truth |
| Jev choice/probabilities | model per candidate | original outcome function | Compare same candidate ids and code; no probability gate |
| group outcome | original outcome | read-only analysis and blind readers | Compare mergers, target group, revisions and omissions, including changed outcomes and controls |
| article and source | archived Step 1 input | independent blind reader | Judge whether actual statements are same, revised, or different; no score/arm/model decision shown |
| cost/failure | archives | report | Never infer zero from missing response |

## New path × old checks

| Check | C | T |
|---|---|---|
| model, state, candidate order, choice criteria | exact archive equality | identical, only question text lines appended |
| request JSON identity | equal per archived request | first strip appended metadata, equals original |
| score alignment | not sent | raw values recomputed against exact query and candidate; reconstructed historical top-ten union and origin membership must equal saved candidate sequence |
| Jev choice set and probability validation | current validator | same validator |
| missing input / empty population | refuse | refuse |
| stored historical answers | replay baseline 185 exact requests/answers without live calls | original answer passes current validator |
| outcome function | original candidates and order | same; group state frozen |
| unrelated later-link Jev calls | excluded | excluded |

## Acceptance and analysis

1. Report every request, candidate, transport failure, cost and baseline variability. Quantify disagreements C vs T and change in wrong merges, missed repeats, revisions and target group, by request, comparing the three draws in each arm. Score-sensitivity is not proof of accuracy. No search recall improvement can be attributed to this intervention because search is held fixed.
2. As Jev and saved references are incomplete, blind readers inspect all eleven incoming records against their full candidate sets and source articles, including unchanged cases. Candidate order is randomized; scores, arm labels, retrieval rank and model decisions are hidden. Two independent reviews and adjudication of disagreements; do not use a new score program as semantic judge. If workload exceeds available reviewer context, partition into bounded batches and report coverage.
3. The original fresh run returned 3 supersedes answers attached to repeat outcomes; it did not exercise a standalone revision outcome. One selected case has a supersedes decision, so describe it as an individual diagnostic, not revision performance. A separate case set of documented real revisions may be read and assessed; it cannot stand in for the full product path.
4. One draw can expose mechanism; 3 same-day control draws characterize instability, not guarantee statistical power. State the counts and losses; no unregistered win threshold. Effect would justify a later separately approved, forward full-path validation; no effect is not proof of equivalence. Predeclare a compact decision before send with council, not after output.

## Prior decisions and limits

D381 selects the candidate with highest Jev same-statement probability; this experiment retains it. D379 seals old product; no frozen files or production config touched. AGENTS §7.1 historical rulers unchanged; repeat reference is exploratory, not new frozen gold. AGENTS §7.2 read raw answer against source. Current Jev model `jev-1.14.0`. Offline census reconstructs and verifies all 185 comparison requests and answers. Standing preflight run against v108 archive judged 243 extraction answers and 170 matching records, two matching records skipped, 12 extraction records dropped and 2 stored schema refusals; that script does not test the clean Jev score path. The latter needs its own replay and refusal controls before send.

## Probe prediction and stop

Hypothesis: score information moves at least one relevant comparison and makes at least one source-backed decision better without a source-backed decision getting worse. Prediction: the clearly wrong X22 grouping becomes separate more often in T than C, while the selected accepted-repeat controls remain correctly grouped. We do not predict a perfect result. Predeclare individual decision comparisons, 3 samples per arm and show all 66 outcomes and errors. For each outcome and selected source-backed candidate, count correct and incorrect choices across three draws per arm. A repeatable improvement requires at least one agreed previously incorrect decision to become correct in at least 2 of 3 T draws and fewer than 2 of 3 C draws, with no agreed previously correct decision becoming wrong in at least 2 of 3 T draws while correct in at least 2 of 3 C draws. A repeatable regression stops the line. If neither occurs or independent readers disagree, report inconclusive. This is a screening rule for selected examples, not a quantitative estimate of product impact. Blind-read all eleven incoming records against all their candidate sets and source articles, including unchanged controls; report gaps. Register case ids and score mapping and historical top-ten replay before any send; send no paid calls until council review and preflight pass.

## Review amendments and exact contract

The read-only Codex reviewer cleared harness design but not sending. Claude reviewed the earlier 10-case/three-arm draft and found lack of revision coverage, unsupported X22 direction and number presentation ambiguity; an eleventh recorded revision-bearing case was added. Its conclusion that 40 borderline probabilities bound opportunity is a hypothesis; confident outputs can also be wrong. The X22 prediction is a falsifiable probe hypothesis, not evidence of likely improvement. The shuffled arm is removed due to false attribution; C versus T assesses the total intervention, not score causation.

Literal metadata is appended after a newline: `Retrieval metadata (not part of the stored piece; cosine, not a probability): query 1 [thesis search]: 0.1234; query 2 [own-text search]: 0.5678`. Four-decimal Python formatting. The label is `thesis search` for every thesis query, `own-text search` for the extra document query, never the thesis content. One score per query against each candidate group's original. Do not claim all queries retrieved that candidate. The manifest records all query identities, full top-ten lists, origin query indices per candidate, all vectors' computed scores and union order. Reconstruct the pre-article group order by replaying saved outcomes article by article, with no same-article visibility, and require union order and saved answer outcome to match all selected cases; fail on missing input. The manifest and source request/answer identities and case list are frozen with hashes before send.

Negative controls: mutate a query vector, candidate score, candidate id, and retrieval origin separately; each must trigger the independent check. A known multi-query case must have every query and origin checked, not only the union. A fake transport must pass 3 separate control draws with 3 calls, fail a malformed response and cover interruption; a missing input and empty population must fail. If an actual send ends ambiguously after dispatch, record it as unresolved and do not silently resend it; incomplete calls are not success. The experiment transport makes exactly one attempt, including after a dropped reply; no retries.

Readers independently classify each new-versus-old statement as same / revision / different / overlapping / unable to decide, using both source articles. Candidate order is shuffled in the reading packet. A multiple-target repeat is acceptable if any source-supported candidate is selected; a revision link must itself be supported; a missing supported revision and a wrong extra revision are errors separately from grouping. Overlap or absent source makes that pair unresolved; it cannot establish improvement or regression. Resolve disagreements by a third reader, and report unresolved without counting correct or wrong. Each of the six draws per case is scored against the same frozen blinded judgments; evaluate repeat target and revision links, not only outcome kind. If model failures or blind review coverage prevent a comparison, report incomplete, never success.
