# Restart handoff — stopped at Alex's request

**2026-10-27: Alex explicitly stopped this session. Do not treat this file as permission to restart calls.** His last message: “this is fucking pathetic, stop and log what you did so far, I need to restart a session with automatic permission”. All three launched study processes had already written their terminal DONE records before this handoff. No model calls or tests were launched after that instruction.

## What Alex wants

Diagnose extraction variance by reading the entire prompt/schema/payload and surrounding code. Correct conflicting responsibilities and measure actual stability on a small POC. No voting, no combining independent model answers. Compare the existing Luna with DeepSeek V4.1 Flash, without silently switching production. He asked for actual measurements, not another proposal.

This session became unnecessarily cumbersome with repeated permission requests and several research-runner mistakes. Own these mistakes; do not present them as all being model defects.

## Exact state at stop

Repository: `/Users/lchingen/hivemind`. Many unrelated/concurrent changes already existed. Preserve them. No commit, push, deployment, production prompt change, or long-run restart was performed.

Research code and prompts: `docs/research/2026-10-27-extraction-contract-poc/`.
All artifacts: `poc/reports/2026-10-27-extraction-contract-poc/`.

- Planned: 3 previously used development articles × 4 configurations × 3 independent repeats = 36 outcomes. Configurations: Luna original, Luna two-step, DeepSeek original, DeepSeek two-step. Original uses one call; two-step uses source then routing. Total planned model steps: 54.
- Received **49 model responses**, plus **4 failed connection attempts** without a response. Total connection attempts: 53. Five planned routing steps remain unsent.
- Original run completed: **27 scored outcomes**, **9 parser failures**. It received 45 model responses.
- All nine parser failures were DeepSeek source responses. Each single response contains multiple function-call objects with disjoint paragraph keys. Combining the pieces of that ONE response passes the original whole-object schema and source checks. No independent responses are combined.
- Original artifacts remain unchanged. All nine source responses were normalized offline into `repairs/<sample-id>/`.
- First routing-completion launch failed on two connections and stopped; no response received. These failures remain in `repairs/004/failure.json` and `repairs/007/failure.json` and the original budget journal.
- Manual network recovery then received four routing responses, under `completion/`: **004 and 007 scored; 010 and 015 contain malformed function arguments and failed JSON parsing**. The runner mistakenly stopped admission on local JSON parsing failures too, leaving five scheduled steps unsent. Do not retry the two malformed model answers merely to improve the score.
- **Unsent routing sample IDs: `018`, `021`, `026`, `029`, `036`.** Their exact prepared request bodies and normalized observations already exist in `completion/<id>/`.
- No `finish.py` or remaining-step runner has been written. `complete.py` cannot simply be rerun: it correctly refuses an existing output directory, and its journal is halted.
- **No final semantic score or result report exists.** `analysis.json` and `review-records.json` are early, incomplete intermediate exports. `semantic-review.json` has NOT been created. Do not quote their zeroes as measured semantic results.

## Spending and process state

Authoritative checkpoint: `poc/reports/2026-10-27-extraction-contract-poc/stopped-summary.json`.

| Item | Value |
|---|---:|
| Received responses | 49 |
| Input tokens | 319,389 |
| Output tokens | 113,025 |
| Estimated model cost | $0.130202088 |
| Conservative charges + unknown reservations | $0.407739 |
| Combined ceiling | $1.50 |
| Remaining under that ceiling | $1.092261 |

Estimate uses Luna $0.10/M input, $0.01/M cached input, $0.50/M output; DeepSeek peak-price upper estimate $0.30/M uncached, $0.006/M cached, $1.20/M output. It is not an invoice.

**Avoid double counting journal snapshots.** Sum these three non-overlapping records:

1. `sandbox-dns-budget-summary.json`: 2 failed connections, $0.050903 reserved.
2. `repair-budget-summary.json`: the main journal's latest state, 47 attempts (45 complete + 2 failed connections), $0.325577 held. This supersedes `budget-summary.json`; do NOT add both.
3. `completion/budget-summary.json`: 4 complete responses, $0.031259 charged; halted with `JSONDecodeError`.

Main run PID file: `run.pid` (34940); terminal log: `run.log`, `DONE 27 scored outcomes`.
First routing completion: `repair-run.pid` (37191); terminal log: `repair-run.log`, `REPAIR DONE`.
Recovery completion: `completion-run.pid` (37570); terminal log: `completion-run.log`, `COMPLETION DONE`.
Earlier failed sandbox process is preserved under `sandbox-dns-*`.
Do not kill these numbers blindly in a future session; PIDs may be reused. Terminal logs establish that these runs ended.

## What the POC changes

`source.txt` (1,998 characters): read the entire cleaned article, process every numbered nonblank line/paragraph, return distinct claims with source sentence IDs, summaries, original speaker/date, tier and event time. It sees no mutable thesis/group context. Code copies exact contiguous quotations from original offsets.

`route.txt` (1,243 characters): one explicit primary destination for every immutable observation, from exactly the displayed usable thesis IDs plus `pending`/`unrelated`. It explains business-driver relevance without equating customer figures to NVIDIA revenue. No new candidate construction in this isolated path. Pending is retained but does not count as library delivery.

Original control prompt is the prior frozen admission-v12 prompt (7,458 characters), original schema/candidate/group behavior. All four cells use the same cleaned reporting text per article. Each provider's first-stage request is byte-identical across its three repeats. Two-step route inputs vary with the source response.

Both source and linked records are saved. Linked POC records also pass the original frozen `sift_with_groups`, without changing that code. Its quote-based merge can discard the second summary from one quoted sentence. Production candidates, groups, matching, judging, storage, UI and defaults are out of scope.

Luna: `gpt-6-luna`, low reasoning, strict JSON schema; original output cap 8,000, POC source 12,000, route 4,000.
DeepSeek: `deepseek-flash`, `thinking: {type: disabled}`, `temperature: 0`, forced strict function at `https://api.deepseek.com/beta/chat/completions`. Official docs map this alias to DeepSeek-V4.1-Flash-1017. This tests configurations, not isolated model weights.

## Findings so far — not final acceptance

`review-notes.md` records the manual reading of most original outcomes. All normalized DeepSeek source summaries were also read in this session, including the complete first variants and field-by-field differences for later variants. Their notes still need writing into the semantic annotation file.

1. **Luna two-step raw source-anchor counts are 5/5 CoreWeave, 6/6 Motley and 7/7 Rest of World on all three repeats.** Read summaries before claiming complete semantic accuracy. The first two routing repeats and final scores preserve those core claims; final 031 route reasons were not individually reviewed yet. Non-core fields/links still vary.
2. Luna original CoreWeave: first sample 001 links old-GPU claims to v37 (binding chip-value financing coverage); sample 016 leaves all links empty; sample 027 links contract/pricing to v6. Same request, materially different routing.
3. DeepSeek original CoreWeave, samples 003/014/025: eight evidence records each, all links empty. It reads useful source facts but delivers none.
4. DeepSeek two-step sample **004 still sends every observation to `pending`**, despite explicitly identifying strong neocloud demand. Its reason says no question covers that driver; v6 Data Center revenue is in the displayed list. Source reading alone does not fix routing interpretation.
5. DeepSeek two-step sample **007 retains six Motley core claims and links them to v6**. It also links EPS projections to total revenue, a non-core semantic concern.
6. DeepSeek routing samples **010 and 015 leak DSML markup inside function arguments**. Example prefix: `{"p004o01">\n<｜｜DSML｜｜: "v6", "reason": ...}`. These are genuine malformed outputs, unlike the recoverable disjoint source objects. Preserve as failures; do not invent a regex semantic repair.
7. DeepSeek source sample **021 invents 2025** for the article's October quarter in `event_time`, also applying that year to Blackwell. Source 010 does not assert the year, and 036 explicitly says it is not stated. This varies at temperature 0.
8. Old sift merges the Kress A100-utilization statement into the Intrator H100-renewal record when both cite the same sentence. It retains only the first summary. Observed in Luna 002/013; expected to inspect after DeepSeek routing too. Luna 028 instead combines both speakers already in one source observation. Identity/attribution is not stable.
9. **Anchor hit is not semantic retention.** Luna original Motley 030 has raw core count 6, but its summaries omit the competition/self-designed-chip mechanism. Correct its semantic count rather than crediting a broad quote.
10. Opposite measurement error: DeepSeek original Rest of World 009/e9 and 035/e10 retain training-vs-inference through the article's later “Nvidia chips are essential for training” sentence, rather than the frozen anchor. Explicit semantic record-ID overrides should credit this when appropriate, without changing the fact label.
11. Old controls frequently put article dates into original statement dates/event time, including precise invented month-end dates for “January”, “October”, or “last August”. Separately measure preserved business meaning versus complete source/time fields. Do not present content coverage as full record correctness.
12. Corrected a mistaken manual lead: the article's final “he said” can refer to Soliman because the immediately preceding sentence names him. Do NOT accuse samples 009/012 of misattributing that ending to Soliman; the complete source was re-read and `review-notes.md` corrected.

The labels are assistant-authored **development annotations**, not independent human gold. Three articles were already used in tuning/research. No broader reliability or production-promotion conclusion is supported.

## Files and how they relate

- `plan.md`: original fixed design, sample scheme, diagnosis, tables and limits.
- `source.txt`, `route.txt`: POC prompts, already copied into frozen artifact inputs.
- `study.py`: original runner, source-unit builder, schema, converters, checks. Do not edit it while pretending the original manifest still holds.
- `budget.py`: conservative SQLite guard. Reserves using request byte bound and output cap; unknown cost remains held. Imported by runners after loading frozen runtime.
- `protocol-repair.md`: closed acceptance set for combining disjoint tool argument objects from ONE response and completing unsent route steps; cost/time accounting requirements.
- `repair.py`: `assemble()` and offline normalization. `prepare` completed. `run` failed on connections before any route response.
- `complete.py`: network-recovery runner. Received 4 routing responses, but mistakenly halted all admission for JSON parsing failures as well as transport errors. No further change made after Alex stopped.
- `analyze.py`: stage metrics and semantic-review consumer; now prefers `completion` then `repairs` over original `samples`. It retains original failure flag. Its latest version has not been rerun to completion or tested. It expects a `semantic-review.json` with `decisions["sample/stage/claim"] = {meaning, provenance, optional record_ids}`; `meaning`/`provenance` must be `pass` to receive the respective credit. Missing annotations are not passes.
- `review-notes.md`: manual observations through sample 032 plus earlier samples; notes for final original 031/033/034/035 and normalized DeepSeek sources still need formal annotation.
- Artifacts `inputs/`: frozen cases, full metadata, original text, paragraph/sentence offsets, original and POC requests, unchanged 31 labels (18 core).
- Artifacts `manifest.json`: original byte hashes and schedule. `manifest.before-host.json` preserves pre-DNS-budget-reduction state.
- Artifacts `samples/`: all 36 original sample folders and raw responses.
- Artifacts `repairs/`: nine normalized single-response sources, prepared route requests, failed first completion attempts.
- Artifacts `completion/`: exact copied normalized sources/requests; four route responses and two scores; five unsent request bodies.
- `protocol-census.json`: full 36-outcome census; all nine disjoint source responses validate.
- `network-recovery.md`, `execution-note.md`: network deviations and accounting. Only first sandbox DNS cause was directly reproduced as `gaierror`; the later pair's underlying URLError cause was not recorded. Subsequent host GET and unauthenticated POST probes succeeded.
- `stopped-summary.json`: final count/cost checkpoint for this stopped session.

## Verification completed / missing

- First design read-only review: no serious findings (`design-review.txt`).
- Protocol review found possible omission of source-step cost/time. Protocol updated, second review closed it (`protocol-review*.txt`). Source usage is recovered from response; elapsed source time from original failure record is marked approximate. Sum of model-step times excludes long wait between source and routing completion; not uninterrupted end-to-end latency.
- `study.py checks` passed: 61 paragraphs, 115 sentence spans; real source/handoff positive; missing paragraph, wrong sentence, contradictory empty reason, missing route, bad target, wrong quote number and call-limit negative controls.
- Code mutants of source quotation and target validation were caught (`mutants.json`).
- `repair.py checks` passed real 004 response; wrong function, overlapping keys, missing piece and bad source sentence refused. Removing overlap rejection was caught (`repair-mutant.json`).
- Frozen old preflight ran three times before respective network launches, with copied item/views DBs. Historical result unchanged: 4,217 extraction items judged, 772 dropped; 4,088 raw evidence, 3,337 kept. Logs: `preflight.log`, `preflight-repair.log`, `preflight-completion.log`. Existing D338 refusals are not fixed by this POC.
- PRDs were re-read across all modules; no production contract edits were warranted. Formal refresh writeup, full suite and final `docs/check.py` have **not** been run for this slice. Alex stopped work; do not imply they passed.

## Next session, only if Alex resumes

1. Read this handoff and the five prepared unsent route requests. Keep all existing model responses, including the two malformed route outputs. Do not restart original source draws, expand the sample, alter gold, or silently switch models.
2. Settle the permission mode first through the user's environment. This agent did not and cannot change the session's permission policy. The repeated escalation dialogs were a major failure of this session's execution.
3. If completing the five calls, use a narrowly bounded remaining-step runner that continues to the next scheduled sample after local schema/JSON failure, while stopping on transport/unknown-usage failure. Preserve all old journals; any new cap must subtract the entire $0.407739 already charged/held from $1.50. Five logical route steps remain; no retries of received malformed answers.
4. Finish semantic annotations. All 36 original outcomes must remain represented, including technical failures. Disclose that protocol normalization and later network recovery happened after the initial run; do not call this an untouched preregistered experiment.
5. Present per-article per-repeat core content, correct destinations, source/time-field failures, dropped/merged meanings, costs and summed step time. Distinguish clean development text from real noisy pages. Include the unchanged model/source defaults and untested candidate/matching/judging boundaries.
6. Update final research results, D339 and CURRENT_STATE; complete appropriate offline/full-suite/document checks only if work is resumed. No commit/push/deployment authority exists.

## Prior experiment to retain as context

`docs/research/2026-10-27-extraction-stability/` and matching artifact directory contain the completed earlier D338 study: 60 Luna calls, old/new analyst prompt × raw/clean text, five repeats per article. It failed to improve stability overall. Key findings include canonical JSON hashes not proving wire-byte equality, schema field reordering in scratch replay, repeated production articles having changed thesis/group context, displayed-but-unusable group-member IDs, empty links, punctuation-space quote rejections, and quote-prefix identity being an invalid semantic metric. The current POC uses its frozen runtime and unchanged labels. Do not overwrite or rerun that completed study.
