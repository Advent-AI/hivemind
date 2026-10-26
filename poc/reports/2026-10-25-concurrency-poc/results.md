# Ordered concurrency POC: offline result

The first D172 slice works on the exercised offline paths. It has not run a paid performance or model-quality comparison. Default replay remains serial. Design: [implementation contract](../../../docs/research/2026-10-25-day-batch-review/implementation.md).

## Behavior implemented

- The isolated `poc/concurrency_study/runner.py` prepares a bounded number of extraction calls. It accepts results in dispatch order only after matching the complete current request, including its schema. A changed context causes another extraction; it never remaps stale IDs to make an answer pass.
- Source, configuration, universe and code/prompt identity are retained in per-day manifests. Restart refuses a changed contract and uses the existing accepted handover when one exists.
- Jev plans database reads on the coordinator, executes independent requests in a bounded worker pool and applies results in their original order. Identical requests share one future and one archived answer. Unsubmitted work does not start after a detected failure; already running work drains.
- The normal round still owns matching checks, the two matching phases, atomic writes, completion records and failure handling. The existing daily dependency scheduler and pull step still own day completion.
- New Jev matching records retain every logical request's call ID/hash. Daily cost uses the archive delta, including discarded speculative work.

## Problems found and corrected

1. **Concurrent duplicate requests could disagree under one archive ID.** Before the fix, two fake service calls with identical requests returned 0.2 and 0.8 but both received the same archive call ID. Before proof (local artifact: `duplicate-before.json`). The batch now shares one request result. The duplicate-dispatch mutant is caught.
2. **Queued matching work continued after failure.** The first code review found all Jev jobs were submitted before reading failures. The scheduler now maintains at most the worker count in flight and checks failed completions before submitting more. The ten-job/two-worker test confirms the other eight requests do not start. The unbounded-submission mutant is caught.
3. **Accepted-result cost omitted discarded speculative calls.** The daily log now reads the archive's actual cost change. Restoring accepted-only cost fails its test.

## Verification

- 143 tests passed in 13.46 seconds (local artifact: `tests-full.txt`): the full product suite, corpus-label tests, review controls and 15 new concurrency tests. Run from a temporary working directory.
- Five scratch mutants caught (local artifact: `mutants-final.json`): accept a stale request; dispatch duplicate requests; reverse result application; submit all jobs despite failure; omit speculative cost. Each failed at the intended assertion.
- 3,595 stored request identities checked (local artifact: `archive-identities.json`): 2,061 in the Jev archive and 1,534 in the generative archive, with zero changes to serialization/hash identity.
- Preflight (local artifact: `preflight.txt`): 250 stored Jev matching records judged, zero skipped and zero refusals; existing extraction refusals remain reported. This verifies the existing checks, not new model quality.
- Final focused review (local artifact: `../../../docs/research/2026-10-25-day-batch-review/runtime-review-2.txt`): no serious findings after bounded-submission correction. Earlier design/code findings and their reports are retained beside it.

The tests cover reversed completion, stale thesis and group context, schema identity, first-item failure, stale speculative failure, saved-handover recovery after rollback, source/configuration change on restart, no next-day work after failure, the English v23/Jev/group/write/judge path, request traceability, shared duplicate results, partial-call cache reuse and failure with more jobs than workers. External services are faked; storage, request builders, checks and writers are real.

## Production and measurement limits

This is an explicit-transport, single-writer POC. It does not establish safety for multiple uncoordinated writers. No live concurrent run has begun: the current per-item spend check cannot reserve in-flight cost, and unknown timeout usage needs accounting before that run. The next task is that live-run admission/accounting guard plus registration of fresh sequential/concurrent controls; earlier spent budgets are not reused.

There is no new 10× claim. The D171 timing projection and existing model-quality golds remain separate. Live elapsed time must include retries, stale work and judging, and new outputs need provenance/semantic mapping to the gold rather than ID equality.

## Reasoning refresh

Universe/classification are unchanged. Config still owns model settings, not worker/cap controls. Dispatch remains the sequence authority. Extraction retains its current context contract. The library keeps identity, group creation, evidence, atomic writes and history. Final verdict and pull design are unchanged; day completion stays after judging/pull. Human-review destinations stay unchanged. The system's default path remains serial; D172 makes only the experimental speculative-call schedule explicit. Documentation now marks D172's offline implementation complete and keeps live validation outstanding.
