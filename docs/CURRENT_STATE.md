# Current state

As of October 26, 2026; frontend decisions through D218. Governing design: `docs/system-design.html` and `docs/prd/`. The POC build began October 23. The foundation is frozen except pull mode and the final verdict; changes to frozen modules need a recorded decision. One row per measured step is in the [build log](research/2026-10-25-english/build-log.md). Earlier states are in [the previous snapshot](research/2026-10-25-english/current-state.before-refresh.md) and, for this phase before the close-out, in commit `f4ff787`; they are not work orders.

## Status

The English pipeline runs end to end. Extraction v10 (`role-v10`, `categories-v10`, `gpt-6-luna`) reads each item whole and declares groups for ongoing matters (D163–D166); matching runs on TypeSafe's Jev `jev-1.14.0` by default (D169, `poc/config/poc-v23.json`), with the generative matcher kept as the configured alternative (`poc-v23-llm`); the writer owns the replacement and succession rules (D167, D168); judging runs once a day before pull mode (D63).

Measured on two arms with the same extraction over the seed (NVDA, February 25 to July 23), the week of July 24–31 and August 1–15, scored per state against golds read from the texts (log rows 41–49, `poc/reports/2026-10-25-benchmark-v23/`): Jev matching equals the generative call on evidence and candidates (merge 7/9 vs 7/7, new 82/82 vs 70/71, evidence repeat and new within a point or two), groups far better (required members 35/38 vs 18/28), and matches at 45% lower cost and 4.8 times the speed. Its two weak states were root-caused and corrected in D168, measured by re-sending the stored requests: wrong replacements 17 to 1, successions 0/3 to 3/3. Evidence retrieval is measured apart: recall@10 36/36 and 46/49. The whole run cost about $1 per arm at published rates.

The phase was closed out with a code review (D170, log row 50). The ledgers, archives and traces are kept on disk and in two backups, listed in the [data manifest](research/2026-10-25-english/data-manifest.md); `poc/data/` is not in Git. Commit `f4ff787` holds the measured state whole, including the research code removed at the close-out.

## Adopted implementation

- D155: reference lists no longer veto candidates; full-match period handling, exact scopes, event identity, same-answer coalescing, old-key trust and atomic write and resume.
- D159: each item finishes writing before the next extracts.
- D163–D166: the English runtime (`vocabulary.py`, canonical values with legacy conversion on read), the fresh English library, research groups declared during extraction with aliases and decided by names in code (`views/groups.py`).
- D167–D169: no hard-coded identity; the measure vocabulary gains `market_size` and `project_cost`; the Jev engine (`views/jev_matching.py`, client `jev.py`) with the PRD's replacement definition, the shared succession rule and an answer for "the same quantity, another period"; a repeat may name the piece shown for the same evidence under another thesis.
- Idea service: default `poc-v32-idea` uses the unchanged two `idea-v7` candidate-discovery requests, then `idea-summary-v7` returns only model-adopted theses with positive weights totaling 100. Final associations, bundles, graph and score use exactly that list; no zero-weight or automatic related cards remain. The live sample shows 55%, 25%, 20% from top to bottom and 61% Idea confidence. [Contract](poc/idea-card.md); [verification](../poc/reports/2026-10-26-positive-weight-selection/results.md).
- UI and service: shared thesis schema and adapter, cards, history chart, evidence, drawer and graph routing; historical reads, search, numeric claim evaluation and thesis bundles over HTTP and MCP ([service specification](poc/service.md)).

The [pipeline overview](poc/pipeline-plan.md) separates the implementation from the design requirements.

## Open defects and limits

- Shared by both matching engines (log row 49): the same figure stated in another document is often judged new (2–3 of 30 sampled new decisions); one matter can end up in several groups (the capex matter holds two groups in the Jev arm, three in the control); a decision naming a candidate of the same answer breaks a chain or duplicates a thesis (7 decisions over all ledgers, all generative); an empty `original_who` on both sides reads as the same party in the writer's rule; two names for the same population are sometimes kept apart (2 merge misses of 9 with Jev).
- Aggregate theses multiply under the `ai-capex` theme: the Jev arm holds nine 2026 aggregate-spending theses, each a different population under the gold's rule. Whether such variants deserve separate theses is the analyst's judgement, not an identity defect; it is recorded for a product decision.
- Extraction: the adopted instructions are narrower than the PRD's important-question rule and omit the personal-memo exception (the English prompt audit records it); extraction can change the quantity before identity matching (a guarantee amount versus the financing provided). D162's recorded failures in an experiment arm were not re-checked on v10.
- The classification simulation keeps the limits in [the preserved defect list](research/2026-10-25-english/classification-existing-defects.txt); a passing simulation is not classification acceptance.
- Corpus: 97 official notices with 56 body and filename collisions need the recorded re-fetch before a rebuilt corpus is relied on.
- The older intermittent search-test failure is untraced; the Docker external-connectivity restriction needs a current check before a container model run.
- Not yet done: broader fresh Idea quality/stability validation on the English ledger; `matching-v4` for dependencies in the generative matcher. The read-only library and UI switch is complete under D181. Scores are not calibrated probabilities; replay applies current weights to earlier states.

Pull mode and the final verdict remain earlier drafts to redesign together. The decided rule freezes the current state and reasons at the due date and closes the thesis. Upstream supply and human-review handling remain deferred.

## Current-library frontend (D181)

The default page now builds directly from the collected English Jev ledger: 90 theses, 18 stored groups, 51 memberships and 50 ungrouped theses. A library grid provides group, subject, status and text filters; the existing Idea canvas remains a separate explicit action. Group membership is never drawn as a dependency. The current ledger has no dependency or succession rows.

HTTP `/library` and MCP `thesis_library` share the dated bundle writer. The versioned `thesis-ui/2` contract preserves identity, all source records, replacement arrival dates, dependency resolutions and succession, with legacy adapters. Historical evidence reads use the selected judgement date. Source IDs in reasons link to the stored evidence. API/MCP defaults and the standalone build now agree on the English ledger/items; model prompts and ingestion are unchanged.

D182 removes the connection/Refresh area, library eyebrow, date picker and duplicate result row. Interface labels use sentence case, metadata uses `|`, and pagination uses “Show more”. D185 adds an explicitly configured composite-history trial for the current NVIDIA Idea: two reviewed connected representatives, equal weights, historical scores, coverage and a contribution table. It computes 0 through July 28, +0.50 from July 29 and 0 from August 10. This is a current-basket retrospective preview, not automatic scoring for every Idea ([result](../poc/reports/2026-10-26-composite/results.md)). D184/D186 open analysis by clicking the Idea card or pressing Enter/Space: full returned summary, per-part explanations and choices, search/candidate trace and response details, opening the drawer makes no model call ([verification](../poc/reports/2026-10-26-idea-analysis/results.md)). D183 adds the 500px input with inline send arrow, blank/pending disabled states and Enter submission; the initial library read no longer changes navigation. Statistics use bar separators. [Send-control verification](../poc/reports/2026-10-26-idea-send/results.md). The updated page is verified in [the presentation report](../poc/reports/2026-10-26-ui-presentation/results.md).

Validation and exact measurements are in [the frontend report](../poc/reports/2026-10-26-library-ui/results.md). No collected database was rewritten, and no model or embedding request was used. The semantic index now covers all 90 theses. The local API is running on port 8788, and one user-submitted Idea completed through the browser with ten selected theses ([startup smoke](../poc/reports/2026-10-26-idea-service-smoke/results.md)); this is operational verification, not a broad Idea quality acceptance. Read-only browsing also works without the API.

D187 replaces the pending Reading chip with a connected live progress list. Actual read-service stage events drive the UI; only the current node glimmers. JSON callers remain compatible, and prompts, model calls and source data are unchanged. The [result](../poc/reports/2026-10-26-idea-progress/results.md) records 155 Python tests, 37 UI tests, 12 mutation checks, browser cancellation/completion checks and a $0 cached actual-API replay.

D188 makes the composite chart a default response feature rather than an exact-question trial. The model supplies one disposition per chosen thesis; code aligns explicit endpoint positions with the user's direction and averages historical scores. The real current question renders +0.50 with a full contribution/exclusion explanation. Validation: 160 Python tests, 40 UI tests, 13 UI mutations plus a backend sign-inversion mutant; all protected source hashes unchanged. [Result and measured limitations](../poc/reports/2026-10-26-default-composite/results.md).

D189–D193 simplify the chart caption, render references as plain blue `[1]` links and place card score pills beside the chart title on the same row at matching text size. D193 supersedes the temporary below-title placement. The original chart spacing and canvas card height are restored. The 90-card library and Idea graph use the shared renderer. [Latest layout verification](../poc/reports/2026-10-26-ui-presentation/score-beside-final.md); [citation verification](../poc/reports/2026-10-26-ui-presentation/score-citations.md). D197 subsequently replaces the Idea display with a 0–100% confidence index; individual Thesis scores retain their existing scale.

D196 supersedes the prior zero-weight format: the model returns only the adopted positive-weight list. 165 Python tests, 44 UI tests, a projection mutation and the live API/browser path pass. The service remains on port 8788 with a dated copied archive; original source databases and earlier archives are unchanged. [Positive-selection results](../poc/reports/2026-10-26-positive-weight-selection/results.md).

The current Idea UI shows 0–100% confidence, with a matching selected-date pill and submission date. The adopted theses appear in descending weight order, with scale-icon badges and separate relevance/rationale paragraphs. Idea and Thesis canvas cards share a 440px width and at least 180px horizontal gap. Detail tabs are Overview, Trace and Response; reading steps open by default, and search records appear only in raw Response. D197–D217 hold the individual presentation decisions. [Presentation verification](../poc/reports/2026-10-26-weight-order/results.md).

D218 cleans the frontend without changing those behaviours: one shared tab controller, named analysis renderers, three unused functions removed, 16 dead style rules removed and three duplicate positioning blocks consolidated. Five stored responses produce identical HTML in all 15 sections; browser layout is unchanged. Validation: 47 frontend tests, 13 mutation checks, 165 Python tests, lint/format and actual drawer/citation/replay checks. [Cleanup plan and results](research/2026-10-26-frontend-cleanup/plan.md).

## Next task: the day-batch shape (queued by Alex, 2026-10-25)

Alex asked to record it as his next task, finish the runs first, then come back to it (his words are in build-log row 45). Today a day is a serial chain (extract, match, write, judge, one item after another; on July 27 the control arm took 11.8 minutes for 31 items, all of it API wait: median 7 s extraction, 6 s generative matching, 12 s judging). The shape to build:

1. Route the day's items in sequence order (local).
2. One wave of extraction for all of them. This needs the extraction request to stop carrying the ledger's groups (today item k's request shows the groups items before k wrote, D149/D166), so group membership moves to matching, where Jev already answers it (35/38 required members over the week and August).
3. One concurrent round of Jev matching against the ledger as of the start of the day.
4. A new intra-day pass comparing the day's new evidence pieces and candidates among themselves, ordered by sequence number (needed: 19–31% of repeat or replace targets were pieces first stored the same day; it also covers decisions naming a candidate of the same answer).
5. Write in sequence order.
6. One wave of judging over the changed theses.

Expected effect: a day from about 12 minutes to about 45 seconds with the normal API and concurrency, bounded by the slowest call per wave (p90 13–22 s) and the provider's rate limits; the batch endpoint fits live daily operation (half price, hours per wave), not the replay. Before building: the state-by-event table for the intra-day pass, and Alex's decision on moving group membership from extraction to matching. Also: a 60-second timeout with retry to cut the roughly 320-second hung calls.

## Previous experiments

D157–D162 (grouping and extraction experiments, including the two-step source-first comparison) failed semantic acceptance; their reports are in `poc/reports/2026-10-25-*` and their code in commit `f4ff787`. The first Jev benchmark (log rows 33–41, `poc/reports/2026-10-25-benchmark/`) measured the earlier engine on extraction v9 and found the replacement and succession issues that D168 corrected.
