# Resume the small ordered-concurrency comparison

> Historical D178 plan. D179 withdraws the unrelated extraction prerequisite and restores the acceleration comparison. The effective scope and rollback are in [resume.md](resume.md); the original plan below is retained as the record of the stopped run.

Alex asked to push the prompt change and return to the acceleration POC. The prompt candidate was pushed as `8848660`. This experiment uses that same T6-v11 configuration in **both** the serial and concurrent arms; it does not compare old serial instructions with new concurrent instructions. The original D174 experiment remains stopped and untouched.

Use the same three complete July 24 items and the same ordered pre-sequence-21 baseline described in [D174's plan](../2026-10-25-ingestion-smoke/plan.md). That plan owns the runtime, source projection, ordering, failure and isolation contracts. The sole harness addition is an explicit `--config` path, defaulting to the old v23 path. The chosen path and its content join the frozen manifest. No provider, schema, grouping or writer change.

## Fixed measurement and stop rules

Run control-1, concurrent-1, concurrent-2, control-2, control-3, concurrent-3; inspect each before starting the next. Each uses a fresh archive and separate baseline copy through `replay.run`, including daily judging and completion. The old product remains sequential by default. Both arms share the two-request outbound limit; only the experimental arm adds two-worker speculative extraction and independent Jev matching.

This is a new isolated journal with the same **$1.50 conservative ceiling and 144 physical-request maximum** as D174, not an increased cap or a reuse of its halted journal. Do not retry transport failures or launch the next trial on failure. Preserve unknown usage. No heavy task runs beside paid calls.

Score information coverage, direct attachment and faithful source status under D176/D177. Inspect the full raw answers and final links against the source, not only the counts or an automatic label:

- SK: retain the material proposed first-factory deployment, 2027 timing and explicitly stated platform facts under a directly relevant question. Do not turn announced capacity into delivered capacity or orders.
- NAVER: retain the GAK Sejong expansion's 200 MW target and 2028 timing as a plan. In this baseline no existing question directly covers it. Do not substitute Rubin production or generic NVIDIA revenue for this deployment.
- Keep the two customer projects distinct. Group membership may include an applicable broader rollout group; a shared group alone is not a duplicate thesis or wrong identity. Do not force customer-specific group counts or names.
- On the follow-up, use the existing appropriate questions for repeated project statements; a retelling is not independent corroboration. Missing a nonessential sentence is not failure. Report any new material fact separately.
- Read every additional proposed/written question, evidence link, source quote, group membership and judgement for unsupported assertions, lost material information or duplicate counting. A different but valid business question is not wrong merely because it differs from gold wording.

Compare all three controls to each other before interpreting differences between modes. Report every sample, accepted/reused/stale extraction count, physical calls, cost and end-to-end wall time. Report paired control/concurrent ratios and their median, without claiming whole-day 10x from three related documents. Saved response replay proves implementation, not fresh model agreement.

Stop before further paid trials if the first control fails coverage, if any trial introduces material unsupported/wrong/duplicate information, or if the structural audit fails. Preserve that result and report it; do not tune another arm in this experiment. A successful first control is read before launching concurrent-1.

## Addition to the state × event table

| State | Event | Required behavior |
|---|---|---|
| Before preparation | Explicit config supplied | Read that file; freeze absolute path, bytes and resolved settings alongside source/runtime hashes |
| Prepared | Same explicit config | Both modes use those settings in every stage and accepted-request reconstruction |
| Prepared | Different path or changed content | Refuse before credentials, archive, trial directory or provider calls |
| Trial finished | Manual source assessment fails | Record failure and stop the study; no next trial |
| Trial finished | Assessment passes | Next named trial may be started explicitly |

The earlier success, refusal, partial failure, cancellation, changed input, restart and day-completion rows remain D174's; no additional writer or runtime mode is introduced.

## Value × reader and new path × checks

| Value | Writer → readers | Check |
|---|---|---|
| Explicit config path and bytes | CLI → preparation, run, audit | Absolute path; same manifest at every trial; default still resolves v23 |
| v11 T6 role | Versioned config → normal request builder | Same role in both modes; categories/schema unchanged; captured accepted requests contain the selected role |
| Assessment | Source review → permission to start next named trial | Explicit per-trial reasons; no row-count substitute |

Before paying: read-only review of this delta, free preflight on copied stored inputs, two full-path fake-provider controls using the selected config, a wrong-config mutant that refuses before credentials, the touched suites, then the full suite once. Preserve existing tests and D174 artifacts. Current preflight refusals must equal their stored-data control. No new prompt wording is tested by first paying; D177 already tested this candidate.

Prior decisions: D149/D166 keep association during extraction; D159/D172 keep accepted requests bound to the committed prefix; D173 is ordinary API concurrency, not the asynchronous Batch API; D174 is stopped; D176/D177 define source coverage without mandatory cards in every context. This experiment does not change them or promote v11.
