# Stopped at the serial control: NAVER's project was lost before matching

The first live sequential control finished its three inputs in 75.38 seconds. Structural checks passed, but the required NAVER project was absent. No live concurrent trial was started. The test journal is closed to further dispatch, as required by the [registered plan](../../../docs/research/2026-10-25-ingestion-smoke/plan.md). All 122 protected database files are unchanged.

## What happened

| Step | Stored evidence |
|---|---|
| Read SK release | The fresh answer creates capacity and opening-date questions and associates both with the existing Rubin group. The old stored answer to the exact same request hash created one opening-date question and a project group. This demonstrates variation; it does not establish its frequency |
| Read NAVER release | The model returns one capacity question for the 200 MW GAK Sejong expansion in 2028, with valid source evidence and a new project-group declaration |
| Extraction check | `extraction.sift` rejects `capacity` beyond the following year. The publication year is 2026; the proposed year is 2028 |
| Evidence/group handoff | The sole evidence item links only to the rejected candidate, so it is also dropped. `sift_with_groups` retains no declared group without a surviving candidate |
| Matching/writing | The handover is empty. `round.run` finishes that item without matching or creating the project |
| Follow-up report | The NAVER capacity statement is linked to the existing NVIDIA Data Center revenue thesis. There is no NAVER project thesis in the library for it to find |

The historical answer represented the same source project as an **event**: completion of the expansion to 200 MW by the end of 2028. That passed. The fresh answer represented it as **capacity in 2028**. That failed. The prompt context differs for NAVER because the preceding SK answer changed, so this is not an identical-request sampling comparison for NAVER.

This is a question-classification/horizon interaction on the serial path. It is not a demonstrated concurrency, completion-order, retrieval or database-write failure. The guard enforces its existing rule correctly. Simply removing it would also admit deliberately excluded later financial forecasts.

## Census and limits

`horizon_census.py` replays the existing extraction check on the 480 stored Jev-arm answers, 480 stored generative-arm answers and three fresh serial answers:

| Population | Answers judged | Horizon refusals |
|---|---:|---:|
| Stored Jev arm | 480 | 5 |
| Stored generative arm | 480 | 2 |
| Fresh serial control | 3 | 1 |

The seven historical refusals cover later revenue-growth or aggregate-spending forecasts. The fresh refusal is the named NAVER project. These eight refusals are a rule census, **not eight bugs**. The existing Claude-authored gold requires the NAVER project; this control therefore fails the registered semantic check. No gold, prompt or eligibility rule was changed to make it pass.

## Validation completed

- 156 tests passed. Four new tests cover the historical projection, shared two-request limit, actual judging-pool failure, and failed-item boundary.
- Free full-path replay completed on temporary ledgers in both modes, using stored model outputs with a fake provider. Both audited cleanly; the speculative path recomputed two stale requests. This is plumbing evidence, not model-quality or speed evidence.
- Four code mutants failed their intended assertions; a scratch handover changed to empty also failed the strengthened audit. The audit binds each accepted handover to its reconstructed request and archived answer.
- Read-only reviews found the snapshot, judge-failure and initially weak audit issues before live work; their follow-up reviews found no remaining serious issue.
- Live control: 11 requests, zero network retries, no unknown-usage outcomes. Standard list-price estimate $0.007573; conservative usage accounting $0.021346. The day completed and all structural checks passed. Only the semantic comparison failed.

## Decision needed before more timing trials

The product needs one consistent rule for an explicitly dated project with a numeric completion target. The current outcome changes when the model chooses an event question versus a capacity question.

Recommended direction: distinguish a named project's completion deadline from an ordinary calendar/fiscal measurement period, and decide eligibility from that distinction before choosing the ladder. Keep the existing short horizon for ordinary financial forecasts. This would need a recorded eligibility decision and validation; it is not implemented here.

The alternative is to retain the strict numeric horizon and decide that the 2028 capacity version is intentionally excluded, then review the gold's expectation explicitly. Neither choice can be made by silently changing the prompt or the measuring stick during this experiment.

## Documentation refresh

The module order and four questions in the PRD index were reviewed. Universe, classification, Config, dispatch, library writes, final verdict, pull and review-pool contracts were not changed. The observed extraction eligibility inconsistency is recorded here for a product decision. Experimental baseline projection, transport accounting and audit changes stay outside the default runtime. No PRD/page rule or gold was rewritten.
