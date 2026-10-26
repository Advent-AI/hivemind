# POC pipeline: a minimal implementation of the design

Updated October 27, 2026. This is the working implementation overview. The original plan and detailed run history are preserved in the [historical snapshot](pipeline-plan-history-2026-10-25.zh.md). The original fifteen-task plan is `docs/superpowers/plans/2026-10-23-nvda-poc.md`; this shorter plan takes precedence where updated by recorded decisions. The [current state](../CURRENT_STATE.md) owns open defects and the next task.

## Current result

The English library (D163–D166) runs end to end on extraction v10 (`role-v10`, `categories-v10`). D169 makes Jev the default matching engine: `poc/config/poc-v23.json` (extraction v10, `matching.engine: "jev"`, `jev-1.14.0`) is the replay default; the generative matcher remains the configured alternative (`poc-v23-llm`). The separate Idea API uses `poc-v32-idea` under D196; its [contract](idea-card.md) owns discovery, adoption and weights. The measurement behind the matching default (build log rows 41–49, `poc/reports/2026-10-25-benchmark-v23/`): two arms on the same extraction over the seed, the week of July 24–31 and August 1–15, scored per state against golds read from the texts. Jev matching equals the generative call on evidence and candidates, groups far better (required members 35/38 against 18/28), and costs 45% less at 4.8 times the speed; its two weak states, replacement and succession, were root-caused and corrected in D168 (probes on the stored requests: wrong replacements 17 to 1, successions 0/3 to 3/3). Open, shared by both engines: the same figure in another document judged new; one matter held by several groups; decisions naming a candidate of the same answer. The ledgers, archives and traces of the phase are listed in the [data manifest](../research/2026-10-25-english/data-manifest.md).

Sequential replay remains the default. D180's isolated concurrency study completed a 53-item recorded-response comparison with identical logical records, plus a separate live matching-throughput measurement. It does not establish a fresh whole-pipeline speedup or promote concurrency. The NAVER v11 prompt is also experimental; neither study changes the replay configuration above.

Earlier in the phase, D162's [two-step extraction comparison](../../poc/reports/2026-10-25-source-first-01/results.md) failed end-to-end acceptance and no experimental role or grouping path was promoted from it.

## Group during extraction

D149 requires the model to organise questions while reading the original item: Rubin shipments and SK factory deployment keep separate theses while sharing a group for the ongoing matter. It is implemented in the default pipeline: extraction (prompt v7 and later) cites shown groups or declares new ones with aliases (D165, D166); `views/groups.py` decides group identity by names in code and plans memberships, which `views/writing.py` commits with the theses; from D169 the Jev engine also answers membership for every candidate (basis `jev`). Measured over the week and August: required members 35/38 with Jev, 18/28 with extraction-time grouping alone. Open: one matter can still end up in several groups (the capex matter holds two in the Jev arm), and moving membership wholly from extraction to matching is part of the queued day-batch shape.

The research harness that explored grouping before it entered the pipeline (`poc/hierarchy_study/`, D146–D162: isolated handoffs, member context, reason-first association, subject names, the Ohio sequence, source-first extraction; none adopted) was removed at the close-out (D170). Its code and tests are in commit `f4ff787`; its results stay in `poc/reports/` and the decisions.

## Product path and POC simplifications

The governing design is PRDs 00–06 and 08, with later decisions including D63, D149, D155 and D159. The old repository contributes requirements and two mechanisms: request-keyed model caching/archive and append-only historical records. Its debates, loop and readmodel are not ported. The corpus is the team's source store; the pipeline retrieves originals by ID rather than copying them into the thesis ledger.

| Module | POC path | Limit or deliberate simplification |
|---|---|---|
| Research universe | `poc/universe.json`: NVDA, peers and themes with categories/references | Manually maintained POC list |
| Classification | Corpus assembly supplies categories, subjects, copies and feed flags | Tables cover acquired channels, not full upstream design |
| Dispatch | Three questions, arrival sequence, processing records and review pool | Return-to-upstream is recorded, not notified |
| Extraction | Whole item, five prompt blocks, category content, JSON schema and source checks | Prompt quality remains experimental; corpus coverage varies by category |
| Thesis storage | Append-only SQLite tables with mutation-refusal triggers; full-text search | No human labels or trained smaller model; input supersession remains a recorded limitation |
| Matching | Jev by default (D169): per candidate one call asking the relation to each listed thesis and membership of each shown group; per evidence piece one call against its thesis's top-ranked pieces; code owns the key rules, succession direction and the checks shared with the generative matcher (ID, open-state, universe, succession and cycle) | Evidence recall@10 measured apart (36/36 and 46/49); the same figure in another document is still often judged new |
| Writing | Themes first; repeated sources, date-ordered replacement, dependency/succession writes and waiting-year binding | Single process; no distributed queues |
| Rejudgement | Dependency order, evidence in force plus replaced predecessor, dependency conclusions and prior conclusion for comparison | D63 explicitly changes cadence to once per day before pull, using `round.judge_day` |
| Pull | Once per calendar day, freeze/close due theses | Only the decided due-date behaviour |
| Final verdict | Not implemented; settings retained | Separate-step design unresolved |
| Replay | Items advance by day with future-input guard; cannot replay before a completed day; day-zero snapshot for agents | D159 serial extraction after each preceding write; failures stop the day |
| Agent layer | Reads day-zero snapshot and later judgements, keeps its own store | Initial consent mode is ask-first |
| Experience measurements | Changed judgements/exit conditions, last check, event records | Replay cannot measure live latency; settlement-value checks and hit records are later work |

The source check currently verifies quotations. Do not infer from that that generated numerical summaries are checked: D162 demonstrated a tenfold summary error despite an exact original quote.

## Identity and volume

The model determines which questions to propose; there is no per-company quota. Prompt rules define a question, verifiable ladder, due date and quarterly evidence. D155 supplies bounded code-owned duplicate identity and treats research lists as references, not admission gates. See the [grouping plan](grouping-improvement-plan.md) for exact scope, period, event-type and legacy-key rules.

## Model and configuration

Extraction and judging run on OpenAI `gpt-6-luna` (D62); matching runs on TypeSafe's Jev `jev-1.14.0` (D169). Keep provider/model explicit; never switch silently. `poc-v23` (extraction v10, Jev matching) is the default configuration; `poc-v16`/`role-v5` was the latest adopted extraction configuration before D163. Costs are computed from the archives' tokens at the published rates in `hivemind.model.PRICES`, never from an archive's stored cost. Experimental D160–D162 roles are not the default. Earlier DeepSeek comparisons and their original costs/results are historical evidence, not current availability or pricing claims. They are preserved in the snapshot.

D63 sets daily judgement: finish that day's item writes, gather changed theses, judge once in dependency order, then pull. Record the day judgement under `day:<date>` with the last sequence. Resume must not judge an already completed day twice. The historical run introduced daily judgement during the replay; its ledger retains both item- and day-labelled judgements from July 29, as measured in the [library build trace](../research/2026-10-25-english/english-library.md). Do not compare the old run as if it used one configuration.

## Verification and run discipline

Before paid work, run `scripts/preflight.py` over stored extraction answers and matching records, inspect every changed refusal class, and prove the decisive case on stored data. A cached replay establishes code behaviour, not model consistency.

Use a small, registered comparison before a larger run. Each treatment needs a fresh control and at least three samples. Keep source inputs, prompts, schemas, limits and semantic expectations fixed. Record raw answers, checks, final writes, cost and failure reasons. Do not change prompts during a run or automatically repeat a failed acceptance.

The original product acceptance includes:

- Valid judgement citations to evidence in force and dependency theses; first judgements and score changes declare a changed conclusion.
- Cached replay without model calls and with the same result.
- No reads of future items during replay.
- A labelled table for twenty user ideas, source-backed trigger records and false all-clear days.

Those are separate from extraction/grouping semantic acceptance. Missing gold or unexercised paths must be reported, not counted as passed.

## Service and frontend

The read-only service provides the complete dated library, search, historical thesis/evidence reads and numeric claim evaluation. The UI opens that library and offers a separate Idea flow with weighted theses and historical confidence. Its Trigger and Action controls are frontend previews. See [service](service.md), [Idea card](idea-card.md) and [Thesis UI](thesis-ui.md) for their owned contracts, and the [README](../../README.md#run-the-service-for-testing) for host startup and local-data requirements. Historical mock iterations are preserved in the snapshot; superseded layouts and local matching rules are not the current specification.

## Known limits

Prompt quality can produce missing, overly broad or trivial questions. Exact quotes do not prove accurate summaries. Code keys do not prove semantic identity or correct grouping. Corpus classification covers only observed channels. Some original-source locations and input supersession paths remain simplified. Event-dependency succession and large-library recall need path-specific validation. Model knowledge can extend beyond a replay window, so a chronological input guard is not proof against model look-ahead. Live latency cannot be measured from replay. Consult current state before launching further work.

## Historical records

The [snapshot](pipeline-plan-history-2026-10-25.zh.md) preserves the initial build sequence, three replay attempts, model comparisons, preflight diagnosis, daily-judgement change, sealed-run results, corpus-tag corrections and early UI iterations. Their original language, numbers and paths remain intact. Current instructions above and later decisions supersede historical proposals to rerun or tune.
