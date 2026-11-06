# POC pipeline: the implementation of the design

Updated November 5, 2026. This is the working implementation overview: what each stage does in code and where it is specified. The PRDs own what each module must do, [decisions](../DECISIONS.md) own what is decided, and the [current state](../CURRENT_STATE.md) owns open defects and the next task. The original plan and the run history up to October 25 are preserved in the [historical snapshot](pipeline-plan-history-2026-10-25.zh.md); the original fifteen-task plan is `docs/superpowers/plans/2026-10-23-nvda-poc.md`.

## What runs

The replay default is `poc/config/poc-v118.json` (D370, D374): the frozen v108 extraction, matching and judging settings without seeded questions, a separate coverage-start report reading or the unused sampling setting. Existing article-created questions remain context. An earnings release can still enter as a source item. This configuration is not yet accepted end to end.

| Stage | What it does | Code | Specified in |
|---|---|---|---|
| Dispatch | Each item in order: three questions, a sequence number, a processing record; items before coverage start are not dispatched | `dispatch.py` | PRD 04 |
| Extraction | One call per item reads the whole item with the questions open at the start of its day and their takes lines, and files each statement under the questions it bears on; a statement no question takes is dropped as no home (D209, D264); extraction v74i at low reasoning (D274) | `extraction.py`, `placement.py` (the takes lines and the links rule) | PRD 05 and the extraction standard |
| Matching and writing | Jev asks each candidate's relation to the listed theses and each evidence piece's relation to its thesis's pieces (D169); the collision judge decides when a candidate collides with an open question (D190); themes are written first | `views/jev_matching.py`, `views/matching.py`, `jev.py`, `views/writing.py`, `views/groups.py` | PRD 06 |
| Judging | Once at the end of each day, the open questions whose evidence changed, dependencies first (D63); judging-v7 reads the evidence in view (D198, D263) | `views/round.py`, `views/judging.py` | PRD 06 |
| Pull mode | At the end of each day, every question whose due day has come closes at the rung it stands on; one never judged closes with "no data to verify"; nothing is re-judged (D356) | `pull.py` | PRD 08 |
| Replay | Items advance by day with a future-input guard; a run cannot start before a completed day; the parallel day prepares extraction requests early and re-checks each at its turn (D181–D183) | `replay.py`, `parallel_day.py`, `scripts/replay.py` | D159, D183 |

## Product path and POC simplifications

The old repository contributes requirements and two mechanisms: request-keyed model caching and archive, and append-only historical records. Its debates, loop and read model are not ported. The corpus is the team's source store; the pipeline retrieves originals by id rather than copying them into the thesis ledger.

| Module | Limit or deliberate simplification |
|---|---|
| Research universe | `poc/universe.json` (NVDA, peers and themes) is a manually maintained POC list |
| Classification | Corpus assembly supplies categories, subjects, copies and feed flags; the tables cover acquired channels, not the full upstream design |
| Dispatch | Return-to-upstream is recorded, not notified |
| Extraction | One company and one window measured; quotations are checked against the source, generated summaries and numbers are not (an exact quote does not prove an accurate summary) |
| Thesis storage | Append-only SQLite tables with mutation-refusal triggers and full-text search; no human labels or trained smaller model yet |
| Matching | The same figure in another document is still often judged new (build log row 49) |
| Writing | Single process; no distributed queues |
| Pull mode | No separate final verdict and no day-end re-judging (D356) |
| Replay | Replay cannot measure live latency; model knowledge can extend beyond a replay window, so the input guard is not proof against model look-ahead |

## Model and configuration

Extraction and judging run on OpenAI `gpt-6-luna` (D62); matching runs on TypeSafe's Jev `jev-1.14.0` (D169). Keep provider and model explicit; never switch silently. Measurements report cost from the archives' tokens at the published rates in `hivemind.model.PRICES`, never from an archive's stored cost; the replay's spend cap and daily log read the archive's stored `cost_usd`. The Idea API runs `poc-v118-idea` (D290, D335, D374).

## Run settings and timing

`scripts/replay.py` prepares extraction requests 16 at a time (`--workers`; `--workers 1` is the serial path; the measurement launcher passes its `HIVEMIND_WORKERS` there), sends Jev matching 8 at a time (`--jev-workers`) and judgements 32 at a time (`judging.JUDGE_WORKERS`; a day's round judges one dependency level at a time, themes before assets; on the 2026-11-02 runs a round held up to 40 judgements in two levels). A model call times out after 180 s and is tried up to three times (`model.openai_transport`); a Jev call after 60 s, also up to three times (`jev.transport`). The slowest honest answers seen take about 40 s (a judgement) to 60 s (an extraction). A measurement runs its three draws at the same time, one launcher each (`docs/research/2026-11-01-e2e-loop/harness/run_arm.sh`); no rate-limit error (HTTP 429) has been seen, at peaks of about 170 concurrent requests over three draws.

Measured on 2026-11-02 (arm 4, before the one-decider architecture: three draws of 14 days, 243 items each): 75 minutes of wall clock for all three against 3.3 hours of model time a draw (extraction 243 calls, 15 s on average; placement 212 calls, 9.4 s; Jev matching 461 calls, 1.6 s; judgements 356 calls, 16 s). About 45 minutes a draw was the serial chain at each item's turn (placement about 9 s, matching and the write about 3 s), because the separate placement call read the questions open at that moment; a day's judging round took about 16 minutes at 6 workers and about 2 at 32. The one-decider architecture (D264) removed the placement call from the chain: the extraction reads the day-start list and files the statements itself. The 14-day, three-draw acceptance of 2026-11-05 cost about $0.8 a draw at published rates.

## Verification and run discipline

The working rules own the procedure (AGENTS §5 and §7): replay stored answers through the current checks with `scripts/preflight.py` before any paid run and read every changed refusal ; prove the decisive case on stored data; a cached replay establishes code behaviour, not model consistency; a comparison of totals uses three draws beside a fresh control; no prompt or package code changes while a run is live.

The original product acceptance also includes:

- Valid judgement citations to evidence in force and dependency theses; first judgements and score changes declare a changed conclusion.
- Cached replay without model calls and with the same result.
- No reads of future items during replay.
- A labelled table for twenty user ideas, source-backed trigger records and false all-clear days.

Missing gold or unexercised paths are reported, not counted as passed.

## Service and frontend

The read-only service provides the complete dated library, search, historical thesis and evidence reads and numeric claim evaluation. The UI opens that library and offers a separate Idea flow with weighted theses and historical confidence; its Trigger and Action controls are frontend previews. See [service](service.md), [Idea card](idea-card.md) and [Thesis UI](thesis-ui.md) for their contracts, and the [README](../../README.md#run-the-service-for-testing) for host startup and local-data requirements.

## Known limits

Prompt quality can produce missing, overly broad or trivial questions. Code keys do not prove semantic identity or correct grouping; one matter can still end up in several research groups. Corpus classification covers only observed channels. Some original-source locations and input supersession paths remain simplified. Event-dependency succession and large-library recall need path-specific validation. Consult the current state before launching further work.

## Historical records

The [snapshot](pipeline-plan-history-2026-10-25.zh.md) preserves the initial build sequence, the early replays, model comparisons, the preflight diagnosis, the daily-judgement change, sealed-run results, corpus-tag corrections and early UI iterations, in their original language. The configurations, prompt versions and mechanisms retired since (the separate placement call, extraction versions before v74i, judging versions before v7) are recorded in the [decision log](../DECISIONS-log.md); current instructions above supersede historical proposals to rerun or tune.
