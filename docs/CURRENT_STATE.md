# Current state

As of November 4, 2026; decisions through D359. The POC build began October 23. The foundation remains frozen; pull mode and closing at the due day are decided and built (D54, D356); later recorded decisions authorize specific changes. [Decisions](DECISIONS.md) govern the [design page](system-design.html) and [module PRDs](prd/README.md).

## Repository (2026-11-03)

`main` holds the merged extraction work and the product code. The served data is the sealed three-month ledger with the cleaned items database (README, "Switching the served data"). The repository was cleaned at D353: experiment outputs and one-off scripts left Git (they stay in its history), documents and every file a reader names stayed. The `main` checkout's uncommitted experiment outputs are kept only in the backup D353 names. Its sixteen uncommitted decisions of 2026-10-27 are now D337–D352.

## Extraction pipeline (merged from `fix/extraction-quality-2026-10-28` on 2026-11-03)

- **Replay default:** `poc/config/poc-v108.json`, the frozen production extraction prompt (D274): extraction v74i on the one-decider architecture (D264, the request shows the day-start open questions with their takes lines and the extraction files each statement), Jev matching with the collision judge, judging-v7 (D263). `tests/test_frozen_extraction_prompt.py` pins it; a change is a new version only Alex opens. This supersedes the `poc-v23` replay default named below; the service's ledger and Idea configuration are unchanged by the merge.
- **The ruler is frozen** (AGENTS §7.1, D261, D262): extraction standard v3 with golden-v5, seeds v2, the judgement gold; `tests/test_frozen_rulers.py`.
- **Measured** (`research/2026-11-01-e2e-loop/design-v78-fields.md` §12–§13): on 50 stored articles, three sends each, v74i against the previous default v74d: core matters 59 → 70, supporting 87 → 117, noise 89 → 81. Reasoning effort raises recall and noise together; a long-item core loss at low reasoning is documented.
- **One path in the code (D359):** the code builds only extraction v74i and judging-v7 and refuses a configuration that names another version; older versions survive as stored runs (the extraction-quality worktree) and in Git. `scripts/preflight.py` replays the frozen run's answers against the questions each request showed.
- **Steps 3 and 4 frozen (D354):** opening and matching questions, and judging them, as `poc-v108` runs them; `tests/test_frozen_questions_and_judgement.py` pins the collision judge, the judge, the matching prompt, the judge's schema and the Jev questions. Accepted on three draws over 2026-07-01..07-14 against `poc-v94` (`research/2026-11-01-e2e-loop/log.md` row 29, run folder `poc/data/e2e-r9-frozen-v108-2026-11-03/`): judgement agrees with the frozen gold on 15/17, 15/17, 16/17; must-open 28/28 each draw; core matters reaching judgement 74.3 → 77.7. Known defects in D354: a duplicate question about one encounter in five, a ruled-out question opened in one draw of three, the operating-margin question left without evidence, the total-revenue question holding about a quarter of all links, and `scripts/preflight.py` unable to judge the one-decider architecture.
- **Open proposals, each a new version only Alex opens:** medium reasoning for items of 15,000 characters or more (D273 amended); driver questions for indirect evidence (a new ruler version). No run unless he asks.
- The branch's full state page at the merge is preserved: [current-state-extraction-branch-2026-11-03.md](research/2026-11-01-e2e-loop/current-state-extraction-branch-2026-11-03.md).

## What runs

The English pipeline runs end to end; product acceptance remains open. The replay default is `poc/config/poc-v108.json` (steps 1–4 frozen, D274 and D354): extraction v74i on `gpt-6-luna` files each statement under the questions open at the start of its day, Jev matching (`jev-1.14.0`) with the collision judge opens and matches questions, and judging-v7 judges once a day before due-date closure. `scripts/replay.py` prepares extraction requests 16 at a time (D183; `--workers 1` is the serial path).

The service, the MCP server and the standalone page serve the sealed three-month ledger `served-2026-10-28-v34-nvda-3m-through-0828` (68 theses, 34 groups), built by the earlier `poc-v34` pipeline, not by `poc-v108`. HTTP `/library`, MCP `thesis_library` and the standalone page share the dated bundle writer. Source dates, recording dates, historical evidence, dependency resolutions and succession remain separate. The current English snapshot has no dependency or succession rows; temporary-ledger tests cover those paths. See the [library integration result](../poc/reports/2026-10-26-library-ui/results.md).

The Idea API defaults to `poc-v33-idea` (D335): two discovery calls followed by one adoption/weighting assessment. Only adopted theses with positive weights appear; nonempty plans total 100%. Each candidate may name only its own two endpoints, enforced in the request schema. Saved weights remain fixed during historical replay. The [Idea contract](poc/idea-card.md) owns response fields, confidence calculation and the limits of those scores.

The interface has Thesis Library and Explore Ideas workspaces. The Idea canvas retains its state across navigation, reveals the connected theses, and shows the confidence Trigger and Action preview. Action settings and its separately dated NVDA stock chart are frontend features; no wallet connection or order execution is implemented. The [UI specification](poc/thesis-ui.md) and [integration guide](../poc/ui/README.md) own current behaviour. D334's [cleanup result](research/2026-10-27-frontend-cleanup.md) records unchanged output across 20 chart states, with 56 frontend tests, 20 mutation checks and 165 Python tests passing at that checkpoint.

The [README](../README.md) owns startup, build and shutdown instructions. Local databases are excluded from Git; a fresh clone can browse the embedded demo. An earlier successful service smoke is evidence of that run, not a claim that a service is currently running. The [data manifest](research/2026-10-25-english/data-manifest.md) locates the preserved ledgers, archives and backups.

## Measured work and publication boundaries

| Work | Evidence and limit |
|---|---|
| English pipeline and Jev matching, D163–D170 | [Build log](research/2026-10-25-english/build-log.md), rows 41–50. Paired runs measured matching cost and speed; stored-request probes corrected replacement and succession. These are not whole-product acceptance. |
| Sequential request cleanup, D175 | `07aaff0` on `cleanup/sequential-requests`: 3,595 archived request identities preserved and 123 tests passed. Recorded as pushed separately, not merged into main. |
| NAVER admission candidate, D177 | `8848660` on `fix/thesis-admission-v11`: six fresh samples on one fixed source. Remains an experimental prompt, not the default. |
| Concurrency POC, D180 | [Full-day result](../poc/reports/2026-10-25-full-day-parallel-r4/results.md): all 53 July 27 items, ten logical tables identical, 106 exact request/answer handovers and ten stale preparations recomputed. This uses recorded responses. |
| Live matching throughput, D180 | The same report measures five fixed Jev requests in three serial and three parallel samples: median 3.959 versus 1.185 seconds (3.340x). One near-threshold decision varies. This is not fresh whole-pipeline latency or semantic-stability acceptance. |
| Current Idea and frontend, D275–D334 | Contracts and focused results are linked above and in [Decisions](DECISIONS.md). UI verification does not establish broad Idea quality. |

The concurrency study remains within its recorded 144-attempt/$1.50 ceiling: 140 attempts, $0.088577 known conservative charges and $0.517 held for unknown usage. This status update launches no paid run and changes no budget or default.

## Open defects

Of the frozen steps (D354 holds each with its census):

1. **Competitor and customer news is filed under the company's revenue questions** instead of the share, capital-spending or custom-chip question it informs (D355; filing is otherwise about 85% right). Share facts are often not written at all, an extraction recall miss (D355). The total-revenue question holds about a quarter of all links (D354).
2. **One bet opened twice** about one encounter in five: the collision judge splits a seed question from an identical candidate on a fine detail.
3. **A question the standard rules out** (the lidar legislation) was proposed by the extraction and opened in one draw of three.
4. **Measured on one company and one 14-day window**, with the judgement scored at the window end only; `poc-v108` has not run over a longer window.
5. **Not built:** argument records (a versioned current argument per question for the judge to read).

The extraction phase's open-defect list before the end-to-end loop (role-v51, 2026-10-30) is preserved in the branch's state page at the merge, [current-state-extraction-branch-2026-11-03.md](research/2026-11-01-e2e-loop/current-state-extraction-branch-2026-11-03.md); the readers' doubts about the frozen standard listed there remain for Alex, nothing changed.

Earlier open defects, unchanged:

- Matching, from build-log row 49: another document's copy of the same figure can be treated as new evidence (2–3 of 30 sampled new decisions). One business matter can occupy several groups (two capex groups with Jev, three in the control). Same-answer candidate references caused seven generative-matcher chain/duplication decisions. Empty `original_who` values can count as the same party. Different names for the same population account for two of nine Jev merge misses.
- The Jev arm contains nine 2026 aggregate-spending theses under `ai-capex`, each with a different population under the gold's rule. Whether to combine those questions remains a product choice, not an established identity defect.
- Extraction's adopted instructions remain narrower than the PRD's important-question rule and omit the personal-memo exception. Extraction can change a quantity's meaning before matching, such as a guarantee amount versus financing provided. D162's experiment failures were not rechecked on v10.
- Classification retains the [recorded simulation defects](research/2026-10-25-english/classification-existing-defects.txt). A passing simulation does not establish classification acceptance.
- The corpus audit recorded 97 official notices with 56 body/filename collisions requiring re-fetch verification before relying on a rebuilt corpus. The older intermittent search-test failure remains untraced. The recorded Docker outbound-network restriction needs a fresh check before a container model run.
- Fresh Idea allocations vary; saved weights do not. The confidence chart applies the current plan to past thesis states and is not a record of historical allocations or a calibrated outcome probability. Broad analyst-prose quality and fresh Idea stability remain unaccepted. Generative matching dependencies still await `matching-v4`.

Pull mode and closing at the due day are decided and built (D54, D356). Upstream supply and human-review output remain deferred.

## One next task

Steps 1–5 are decided: extraction, question opening and matching, and judging are frozen (D274, D354); closing at the due day is pull mode's and is built (D356). The next event is the first real due day, 2026-12-31 ("Will Nvidia begin shipping its Rubin generation by December 31, 2026?"), which gives the first closing to read against a published result. Until then, the open items are Alex's to take up: the known defects of D354 and D355, argument records. No paid run is authorized by this update.

## Documentation maintenance

The [October 27 refresh record](research/2026-10-27-documentation/refresh.md) lists corrected descriptions and the reasoning pass across all modules. The [previous current-state page](research/2026-10-27-documentation/current-state.before-refresh.md) preserves the detailed chronology; it is a historical snapshot, not current operating instructions.
