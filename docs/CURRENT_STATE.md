# Current state

As of October 25, 2026; decisions through D180. Governing design: `docs/system-design.html` and `docs/prd/`. The POC build began October 23. The foundation is frozen except pull mode and the final verdict; changes to frozen modules need a recorded decision. One row per measured step is in the [build log](research/2026-10-25-english/build-log.md). Earlier states are in [the previous snapshot](research/2026-10-25-english/current-state.before-refresh.md) and, for this phase before the close-out, in commit `f4ff787`; they are not work orders.

## Status

Sequential request-construction cleanup was committed and pushed separately as [`07aaff0`](https://github.com/Advent-AI/hivemind/commit/07aaff0db561803fe19f0ccb5ba80e7e4a8fa205) on `cleanup/sequential-requests`. It preserves all 3,595 archived request identities; 123 sequential product/corpus tests pass. It is not merged into `main`; experimental changes remain local.

The tested NAVER prompt candidate and its six-sample evidence are committed and pushed as [`8848660`](https://github.com/Advent-AI/hivemind/commit/884866055cc265455bb72d25cd22e71db10e6558) on `fix/thesis-admission-v11`, based on the sequential cleanup. That branch contains no concurrent runtime. It is not merged or enabled by default.

The English pipeline runs end to end. Extraction v10 (`role-v10`, `categories-v10`, `gpt-6-luna`) reads each item whole and declares groups for ongoing matters (D163–D166); matching runs on TypeSafe's Jev `jev-1.14.0` by default (D169, `poc/config/poc-v23.json`), with the generative matcher kept as the configured alternative (`poc-v23-llm`); the writer owns the replacement and succession rules (D167, D168); judging runs once a day before pull mode (D63).

Measured on two arms with the same extraction over the seed (NVDA, February 25 to July 23), the week of July 24–31 and August 1–15, scored per state against golds read from the texts (log rows 41–49, `poc/reports/2026-10-25-benchmark-v23/`): Jev matching equals the generative call on evidence and candidates (merge 7/9 vs 7/7, new 82/82 vs 70/71, evidence repeat and new within a point or two), groups far better (required members 35/38 vs 18/28), and matches at 45% lower cost and 4.8 times the speed. Its two weak states were root-caused and corrected in D168, measured by re-sending the stored requests: wrong replacements 17 to 1, successions 0/3 to 3/3. Evidence retrieval is measured apart: recall@10 36/36 and 46/49. The whole run cost about $1 per arm at published rates.

The phase was closed out with a code review (D170, log row 50). The ledgers, archives and traces are kept on disk and in two backups, listed in the [data manifest](research/2026-10-25-english/data-manifest.md); `poc/data/` is not in Git. Commit `f4ff787` holds the measured state whole, including the research code removed at the close-out.

## Adopted implementation

- D155: reference lists no longer veto candidates; full-match period handling, exact scopes, event identity, same-answer coalescing, old-key trust and atomic write and resume.
- D159: each item finishes writing before the next extracts.
- D163–D166: the English runtime (`vocabulary.py`, canonical values with legacy conversion on read), the fresh English library, research groups declared during extraction with aliases and decided by names in code (`views/groups.py`).
- D167–D169: no hard-coded identity; the measure vocabulary gains `market_size` and `project_cost`; the Jev engine (`views/jev_matching.py`, client `jev.py`) with the PRD's replacement definition, the shared succession rule and an answer for "the same quantity, another period"; a repeat may name the piece shown for the same evidence under another thesis.
- Idea service: the adopted two-call contract `poc-v9` / `idea-v7`, reasoning `none` (D135/D145); limits in the [Idea specification](poc/idea-card.md). The service still reads the sealed Chinese ledger with its search index.
- UI and service: shared thesis schema and adapter, cards, history chart, evidence, drawer and graph routing; historical reads, search, numeric claim evaluation and thesis bundles over HTTP and MCP ([service specification](poc/service.md)).

The [pipeline overview](poc/pipeline-plan.md) separates the implementation from the design requirements.

## Open defects and limits

- Shared by both matching engines (log row 49): the same figure stated in another document is often judged new (2–3 of 30 sampled new decisions); one matter can end up in several groups (the capex matter holds two groups in the Jev arm, three in the control); a decision naming a candidate of the same answer breaks a chain or duplicates a thesis (7 decisions over all ledgers, all generative); an empty `original_who` on both sides reads as the same party in the writer's rule; two names for the same population are sometimes kept apart (2 merge misses of 9 with Jev).
- Aggregate theses multiply under the `ai-capex` theme: the Jev arm holds nine 2026 aggregate-spending theses, each a different population under the gold's rule. Whether such variants deserve separate theses is the analyst's judgement, not an identity defect; it is recorded for a product decision.
- Extraction: the adopted instructions are narrower than the PRD's important-question rule and omit the personal-memo exception (the English prompt audit records it); extraction can change the quantity before identity matching (a guarantee amount versus the financing provided). D162's recorded failures in an experiment arm were not re-checked on v10.
- The classification simulation keeps the limits in [the preserved defect list](research/2026-10-25-english/classification-existing-defects.txt); a passing simulation is not classification acceptance.
- Corpus: 97 official notices with 56 body and filename collisions need the recorded re-fetch before a rebuilt corpus is relied on.
- The older intermittent search-test failure is untraced; the Docker external-connectivity restriction needs a current check before a container model run.
- Not yet done: the service and UI switch to the English ledger (a new search index), `matching-v4` for dependencies in the generative matcher.

Pull mode and the final verdict remain earlier drafts to redesign together. The decided rule freezes the current state and reasons at the due date and closes the thesis. Upstream supply and human-review handling remain deferred.

## Parallel POC: implementation-plan execution completed

D180 followed the existing [implementation plan](research/2026-10-25-day-batch-review/implementation.md), without changing extraction semantics. The [full result](../poc/reports/2026-10-25-full-day-parallel-r4/results.md) covers all 53 July 27 inputs. Sequential and eight-worker recorded-response execution produce identical views, rungs, evidence, sources, links, dependencies, succession, groups, memberships and judgments. All 106 accepted handovers match their exact current-prefix requests and archived answers; 10 stale preparations were recomputed. A nonempty-handover mutation fails the audit. The full 156-test suite passes.

A separate live comparison uses five identical Jev requests and one fixed snapshot, with three serial and three parallel samples. Median time is 3.959 versus 1.185 seconds (3.340x); actual concurrent provider peak is five. One borderline evidence decision varies in two parallel samples; the identical request's raw probabilities cross the existing threshold, and the other five decisions agree. The result records this variation and does not claim semantic stability or whole-pipeline 10x.

The source fixture was completed under current code because historical matching requests predate D168's criterion correction. Exact cached calls were reused; only missing calls were sent. This fixture-completion time is not reported as a latency control. All 138 protected database files are unchanged. Across the earlier run and this continuation there are 140 of the allowed 144 attempts; $0.088577 in conservative known charges and the original $0.517 unknown-use reservation, total held $0.605577 under the unchanged $1.50 cap. No prompt, matching rule, threshold, default runtime or working library was changed.

## Next task

Measure fresh end-to-end latency on the complete fixed workload before claiming a whole-pipeline speedup or promoting the mode. Keep the full-day structural proof and the live matching-throughput proof separate. Existing extraction findings remain recorded; they are not a new prerequisite work order for the concurrency task. No further paid call is launched by this status update.

## Previous experiments

D157–D162 (grouping and extraction experiments, including the two-step source-first comparison) failed semantic acceptance; their reports are in `poc/reports/2026-10-25-*` and their code in commit `f4ff787`. The first Jev benchmark (log rows 33–41, `poc/reports/2026-10-25-benchmark/`) measured the earlier engine on extraction v9 and found the replacement and succession issues that D168 corrected.
