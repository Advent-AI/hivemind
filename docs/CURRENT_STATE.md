# Current state

As of October 27, 2026; decisions through D241. The POC build began October 23. The foundation remains frozen except pull mode and the final verdict; later recorded decisions authorize specific changes. [Decisions](DECISIONS.md) govern the [design page](system-design.html) and [module PRDs](prd/README.md).

This page describes the working tree. The documentation-only publication leaves product code and raw research artifacts uncommitted; the latest local frontend features are not part of that publication.

## What runs

The English pipeline runs end to end, but product acceptance remains open. Its default is `poc/config/poc-v23.json`: extraction v10 on `gpt-6-luna`, Jev matching (`jev-1.14.0`) and once-per-day judging before due-date closure. Sequential processing remains the default. Extraction supplies research groups; matching and the writer resolve identity and preserve the resulting records. The [pipeline guide](poc/pipeline-plan.md) owns the implementation overview.

The current library snapshot contains 90 theses, 18 groups, 51 memberships and 50 ungrouped theses. HTTP `/library`, MCP `thesis_library` and the standalone page share the dated bundle writer. Source dates, recording dates, historical evidence, dependency resolutions and succession remain separate. The current English snapshot has no dependency or succession rows; temporary-ledger tests cover those paths. See the [library integration result](../poc/reports/2026-10-26-library-ui/results.md).

The Idea API defaults to `poc-v33-idea` (D258): two discovery calls followed by one adoption/weighting assessment. Only adopted theses with positive weights appear; nonempty plans total 100%. Each candidate may name only its own two endpoints, enforced in the request schema. Saved weights remain fixed during historical replay. The [Idea contract](poc/idea-card.md) owns response fields, confidence calculation and the limits of those scores.

The interface has Thesis Library and Explore Ideas workspaces. The Idea canvas retains its state across navigation, reveals the connected theses, and shows the confidence Trigger and Action preview. Action settings and its separately dated NVDA stock chart are frontend features; no wallet connection or order execution is implemented. The [UI specification](poc/thesis-ui.md) and [integration guide](../poc/ui/README.md) own current behaviour. D241's [cleanup result](research/2026-10-27-frontend-cleanup.md) records unchanged output across 20 chart states, with 56 frontend tests, 20 mutation checks and 165 Python tests passing at that checkpoint.

The [README](../README.md) owns startup, build and shutdown instructions. Local databases are excluded from Git; a fresh clone can browse the embedded demo. An earlier successful service smoke is evidence of that run, not a claim that a service is currently running. The [data manifest](research/2026-10-25-english/data-manifest.md) locates the preserved ledgers, archives and backups.

## Measured work and publication boundaries

| Work | Evidence and limit |
|---|---|
| English pipeline and Jev matching, D163–D170 | [Build log](research/2026-10-25-english/build-log.md), rows 41–50. Paired runs measured matching cost and speed; stored-request probes corrected replacement and succession. These are not whole-product acceptance. |
| Sequential request cleanup, D175 | `07aaff0` on `cleanup/sequential-requests`: 3,595 archived request identities preserved and 123 tests passed. Recorded as pushed separately, not merged into main. |
| NAVER admission candidate, D177 | `8848660` on `fix/thesis-admission-v11`: six fresh samples on one fixed source. Remains an experimental prompt, not the default. |
| Concurrency POC, D180 | [Full-day result](../poc/reports/2026-10-25-full-day-parallel-r4/results.md): all 53 July 27 items, ten logical tables identical, 106 exact request/answer handovers and ten stale preparations recomputed. This uses recorded responses. |
| Live matching throughput, D180 | The same report measures five fixed Jev requests in three serial and three parallel samples: median 3.959 versus 1.185 seconds (3.340x). One near-threshold decision varies. This is not fresh whole-pipeline latency or semantic-stability acceptance. |
| Current Idea and frontend, D181–D241 | Contracts and focused results are linked above and in [Decisions](DECISIONS.md). UI verification does not establish broad Idea quality. |

The concurrency study remains within its recorded 144-attempt/$1.50 ceiling: 140 attempts, $0.088577 known conservative charges and $0.517 held for unknown usage. This status update launches no paid run and changes no budget or default.

## Open defects and limits

- Matching, from build-log row 49: another document's copy of the same figure can be treated as new evidence (2–3 of 30 sampled new decisions). One business matter can occupy several groups (two capex groups with Jev, three in the control). Same-answer candidate references caused seven generative-matcher chain/duplication decisions. Empty `original_who` values can count as the same party. Different names for the same population account for two of nine Jev merge misses.
- The Jev arm contains nine 2026 aggregate-spending theses under `ai-capex`, each with a different population under the gold's rule. Whether to combine those questions remains a product choice, not an established identity defect.
- Extraction's adopted instructions remain narrower than the PRD's important-question rule and omit the personal-memo exception. Extraction can change a quantity's meaning before matching, such as a guarantee amount versus financing provided. D162's experiment failures were not rechecked on v10.
- Classification retains the [recorded simulation defects](research/2026-10-25-english/classification-existing-defects.txt). A passing simulation does not establish classification acceptance.
- The corpus audit recorded 97 official notices with 56 body/filename collisions requiring re-fetch verification before relying on a rebuilt corpus. The older intermittent search-test failure remains untraced. The recorded Docker outbound-network restriction needs a fresh check before a container model run.
- Fresh Idea allocations vary; saved weights do not. The confidence chart applies the current plan to past thesis states and is not a record of historical allocations or a calibrated outcome probability. Broad analyst-prose quality and fresh Idea stability remain unaccepted. Generative matching dependencies still await `matching-v4`.

Pull mode and the final verdict remain earlier drafts to redesign together. Due-date state freezing and closure are decided. Upstream supply and human-review output remain deferred.

## One next task

Measure fresh end-to-end latency on the complete fixed workload before claiming a whole-pipeline speedup or promoting concurrency. Keep the recorded-response structural proof and live matching-throughput proof separate. Existing extraction findings remain recorded; they are not a new prerequisite work order for acceleration. No further paid call is authorized by this documentation update.

## Documentation maintenance

The [October 27 refresh record](research/2026-10-27-documentation/refresh.md) lists corrected descriptions and the reasoning pass across all modules. The [previous current-state page](research/2026-10-27-documentation/current-state.before-refresh.md) preserves the detailed chronology; it is a historical snapshot, not current operating instructions.
