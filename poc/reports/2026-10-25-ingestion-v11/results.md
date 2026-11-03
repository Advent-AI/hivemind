# Acceleration POC: restored scope and first paired run

> Historical result, not the current work order. D179 withdraws the instruction to repair extraction before continuing acceleration. The semantic findings and measurements remain recorded; [resume.md](../../../docs/research/2026-10-25-ingestion-v11/resume.md) defines the restored scope. The study stop flag was restored with its attempts, charges and limits unchanged; see `rollback.json`.

## Current result after D179

The mistaken extraction prerequisite and its stop flag were reversed without changing runtime code or prompts. The first concurrent trial then completed successfully.

| Trial | Wall time | Physical requests | Outcome |
|---|---:|---:|---|
| control-1 | 60.65 s | 12 | All three inputs, ordered writes and daily completion; both projects retained |
| concurrent-1 | 43.03 s | 10 | Same structural checks pass; both projects retained; two stale preparations recomputed |
| concurrent-2 | 13.74 s before failure | 2 | First extraction connection closed with TLS EOF; one request has unknown usage, the other completed while draining |

The first pair's observed ratio is 1.409x, but it is only one pair and the workloads differ (four judgments in the control versus two in concurrent-1). It does not establish a concurrency speedup or the 10x target. The NAVER follow-up reuses the existing project evidence in concurrent-1. No duplicate project was introduced.

The second concurrent trial wrote no new views, evidence, handovers or judgments. The existing transport correctly stopped and drained after the connection failure. There is no automatic retry and no claim this was an extraction or concurrency-logic regression. The journal now has 23 complete requests and one unknown request: $0.049062 conservative known charges plus $0.517 held for unknown usage. The hold is not a confirmed bill and has not been released. Known Standard list-price estimates sum to $0.015188. The remaining paired samples have not run.

The [saved-call latency breakdown](latency.md) finds that both later preparations were discarded and matching had only one request per phase; it finds no useful extraction overlap in this sample. About 78% of the observed wall-time reduction is explained by the smaller judgment workload.

See [continuation-summary.json](continuation-summary.json) for computed values. All source databases remain unchanged. The next work is completion of the acceleration measurement after handling the transport interruption within the original budget, not a new extraction rewrite.

## Historical first-control assessment under withdrawn D178 gate

The first sequential control retained both projects and completed in **60.65 seconds**, but failed the registered direct-evidence-link criterion. Three of six new evidence links were indirect. No concurrent trial was started, so this run provides **no acceleration result**. The prior NAVER-only prompt result remains valid within its narrower scope; it did not test this three-item sequence or its follow-up links.

The prompt candidate is pushed as [8848660](https://github.com/Advent-AI/hivemind/commit/884866055cc265455bb72d25cd22e71db10e6558). Both arms of this new experiment were configured to use it; the default product configuration remains unchanged.

## What worked and what failed

| Stored link | Source information | Destination | Assessment |
|---|---|---|---|
| e50 → v13 | Signed SK/NVIDIA letters of intent | SK first-factory deployment | Direct; retained as letters of intent |
| e51 → v13 | First SK factory planned online in 2027, using Rubin/HBM4 | SK first-factory deployment | Direct; plan and timing preserved |
| e52 → v14 | NAVER expansion from 55 MW to 200 MW by 2028 | NAVER deployment | Direct; the original loss is fixed in this sample |
| e53 → v7 (link 62) | NAVER's planned factory is expected to use Rubin/Blackwell | Rubin production shipments by the end of 2026 | Indirect; deployment plans do not directly establish that shipment timetable |
| e52 → v3 (link 63) | The follow-up retells NAVER's expansion | NVIDIA FY2027 Data Center revenue | Indirect; no source connection to that revenue period, orders or deliveries |
| e54 → v3 (link 64) | Planned $500-billion-plus SK partnership spanning infrastructure and memory | NVIDIA FY2027 Data Center revenue | Indirect; partnership scale is not the company's revenue or a specified FY2027 purchasing commitment |

This does not require every revenue evidence item to contain a revenue number. A source-grounded purchase or delivery development can directly inform a revenue question without stating dollars. Here the missing element is the connection to the business result and period being judged.

The project questions remain distinct. SK joins the existing Rubin rollout group; NAVER has its own project group. Those differences do not fail the grouping criterion. Plans remain party statements. The daily judgments explicitly retain uncertainty; a Yes directional rung is not being mistaken for a claim of completed deployment.

The NAVER retelling correctly reused e52 and appended its source, rather than creating another copy. However, it also added the wrong v3 link. The SK partnership amount is a different statement from the earlier letters of intent, so its separate evidence record is not by itself proof of duplicate counting. Approximately 100,000 GPUs was omitted from the final repeated summary; that minor detail is not the stopping reason.

## Trace to the mechanism

1. The extraction requests already showed both project questions when the follow-up arrived. The model nevertheless wrote links to v3 in its raw answer. NAVER's first release likewise wrote its platform statement to v7. Neither error originated in parallel execution: this was the normal serial path.
2. `extraction.sift` checks that the quote exists and the destination ID was shown. Both are true here, so it accepts the links. This is reference validation, not business relevance validation.
3. `jev_matching.decide` compares the incoming statement with old statements within each supplied destination. Its evidence questions classify repeat, replacement or different statement. They do not reconsider whether that destination is the right business question.
4. The writer preserves those accepted destinations. In the NAVER repeat, it reuses the existing evidence identity and appends the additional v3 link. The revenue and shipment judgments then receive the indirectly related statements. The shipment judgment itself calls the additional factory evidence indirect.

The primary defect is a model-written evidence association that passes reference checks. The downstream contract assumes that association is already correct; changing concurrency cannot repair it. The literal direct-link instruction is already in role-v11, so another untested warning added to the prompt would not be a demonstrated fix.

The [link census](link-census.json) reads the three selected sources across all completed D174/D177/D178 trial archives: 12 extraction answers, with v3/v7 links in four. That is a source-specific candidate census, not four automatically failed answers or a global quality rate. The independent [source assessment](../../../docs/research/2026-10-25-ingestion-v11/control-assessment-review.txt) reviewed all six new links and agrees that this control must stop. The raw answers, matching records, handovers and final records remain in `control-1`.

## Verification, costs and boundary

- All three accepted extraction requests reconstruct from their actual committed prefixes and match the archived answers/handovers. Existing baseline records are unchanged; daily judging and completion are ordered correctly. Structural audit: zero errors.
- Free full-path serial and concurrent replays passed using stored answers and a fake provider. The concurrent replay discarded two stale preparations. A substituted handover was caught; a changed config was refused before credentials or trial creation.
- The explicit study `--config` reaches preparation, both execution modes and the audit; the chosen absolute path and bytes are frozen. The default remains v23. Read-only design and code reviews found no serious issue in this delta.
- 28 touched tests, 151 product/corpus tests and five stored-data diagnostic tests passed. Preflight's refusals were unchanged from its saved control; all 250 matching records were checked, none skipped, and all 159 prompt enum checks passed.
- **12 physical requests**, no retries or unknown usage. Standard list-price estimate **$0.007102**; conservative guard accounting **$0.020530**, below the unchanged $1.50 cap.
- **138 protected databases unchanged.** The study journal is halted. No further trial or default activation occurred.

The registered stopping rule has fired. Do not change the gold, relax direct-link acceptance or design another paid arm silently. The next decision is how to resolve this evidence-association defect before requiring another correct end-to-end timing control; alternatively, separating scheduler verification from model-quality acceptance would be an explicit measurement-design change, not a speed result from this run.

## Correction after comparison with the accepted baseline

The previous v23 Jev ledger already contains three NAVER-source evidence items (e56/e57/e58) linked both to its deployment question and to v3, FY2027 Data Center revenue. The archived v23 extraction call 687 proposed those links. See `baseline-comparison.json`. The prior report diagnosed the current associations but failed to establish that this class was new relative to the accepted baseline before making it the next acceleration blocker.

The direct-link concern remains a semantic finding. It is not evidence of a concurrency regression, nor evidence that the NAVER milestone-retention fix stopped working. The experiment design must distinguish previously accepted semantic issues, fresh-sample variation and changes introduced by acceleration. The journal remains halted; no acceptance criterion is silently changed and no further paid trial is started by this correction.
