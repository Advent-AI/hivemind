# Data manifest, 2026-10-25 close-out

The ledgers, model-call archives and traces of this phase stay on disk under `poc/data/` (git-ignored, 727 MB) and in one backup outside the repository. Nothing here was deleted at the close-out. Checksums are the first 16 hex digits of SHA-256, taken on 2026-10-25 after the last run.

Backup: `~/hivemind-backups/poc-data-2026-10-25.tar.gz` (158 MB, 273 files, the whole `poc/data/` tree), SHA-256 `a346bb8d460444f05a06973ef54717c97151fb0e521e0c1c4bcd0dd200ddf2c1`.
Second backup: `~/hivemind-backups/poc-reports-ignored-2026-10-25.tar.gz` (5385 files: the git-ignored trace pages and recall-oracle archives under `poc/reports/`), SHA-256 `bc5191711280bb9e42a398edf05bc9dcbae07611d2c5615639367fe800b42fa5`.

## Input

| file | what it is | SHA-256 |
|---|---|---|
| `poc/data/items-window-tags2-2026-10-24.sqlite` | the item window every English run replays (2026-02-25 to 2026-08-15) | 02791fd2b1b3d6ab |

## The measured ledgers (build log rows 43–49)

Each folder holds `views.sqlite` (the ledger), `archive.sqlite` (every model and Jev call, request and answer), the run logs, and for the two D167 arms a week snapshot (`views.week.sqlite`, `archive.week.sqlite`) taken before August.

| folder | configuration | window | role | views | archive |
|---|---|---|---|---|---|
| `english-v23-jev-2026-10-25` | `poc-v23` (extraction v10, Jev matching) | seed, week, Aug 1–15 | D167 arm; the default engine from D169 | f6ba83ffa79caafc | bc3e769937323819 |
| `english-v23-llm-2026-10-25` | `poc-v23-llm` (extraction v10, generative matching) | seed, week, Aug 1–15 | D167 control arm | a1ee44f68a179705 | d629f8df6b308a39 |
| `english-groups4-2026-10-25` | `poc-v21` | seed, week | control of the first Jev benchmark (row 41) | fe11a3bf86342f2c | 5b5042a5e5140125 |
| `english-jev2-2026-10-25` | `poc-v22` | seed, week | Jev arm of the first benchmark (row 41) | cfe09822456e9cd7 | 5bab7f8d33740f3f |
| `english-jev3-2026-10-25` | `poc-v22`, fixed engine | seed | engine replicate (row 37) | c460b6797a475645 | 406654ab0aeffed2 |
| `english-jev-2026-10-25` | `poc-v22`, first criteria | seed | first Jev seed (row 35) | c589e2304f3d3e9e | c7a462e4e4e129ad |
| `english-2026-10-25` | `poc-v17`–`v20` | seed, week, part of August | the English library build (rows 1–33) | — | 8bec7d710f0259ea |
| `english-groups-2026-10-25`, `-groups2-`, `-groups3-` | `poc-v19`–`v20` | seed or week | research-group iterations | baa802da5ea78c16 / 0ead32d89874db73 / 1160c9e522d85658 | 91ebcdebe66a176b / e0ab4d37ed9d7fa1 / a8d4535343896be9 |

## Earlier material, kept as found

`keyed-2026-10-25/` (the keyed-views rebuild, D155+), `sealed-2026-10-24-run3-*` (sealed ledgers with their own `SHA256SUMS`), `old-2026-10-23-run*`, `service/` (the service's idea archive, search index and timing runs), and the loose `views-2026-10-25-v1*.sqlite`, `archive.sqlite`, `views.sqlite` files at the top of `poc/data/`.

## Parallel-day studies (D172–D182)

The SQLite ledgers, archives and budget journals of the concurrency studies stay on disk, ignored by each report folder's `.gitignore`; the reports, summaries and per-trial results are in Git. Inputs and the recorded golden: `poc/reports/2026-10-25-full-day-canonical/` (current-code sequential fixture of July 27: `views.sqlite`, `archive.sqlite`) and `poc/reports/2026-10-25-full-day-parallel-r4/` (start-of-day `baseline.sqlite`, the day's `items.sqlite`, the golden `serial/views.sqlite`). The live study: `poc/reports/2026-10-26-e2e-parallel/live/` (`inputs/`, one folder per trial with `views.sqlite`, `archive.sqlite` and its `cross-replay/`, and `budget.sqlite`). The fifteen-day oracle study (D182): `poc/reports/2026-10-26-multi-day-oracle/` (`serial/`, `parallel-16/`, `parallel-16-mutant/`, each with `views.sqlite` and `archive.sqlite`), started from `poc/data/english-v23-jev-2026-10-25/views.week.sqlite`. Earlier studies: `2026-10-25-api-smoke`, `-ingestion-smoke`, `-ingestion-v11`, `-within-item-parallel`, `-full-day-parallel*`.

## The three-month NVDA window and the 2026-10-27/28 ledgers (build log rows 58–66)

Input: `poc/data/items-nvda-2026-07-01-10-27.sqlite` (249 MB) is the cleaned database the runs read (D256 on the main branch: the backfilled corpus after the binary rule and the second fetch pass); `.page.sqlite` holds the fetched pages, `.before-binary-rule.sqlite` and `.before-fetch2.sqlite` are the two earlier states, `-tn.sqlite` / `-tn.page.sqlite` the TrueNorth-only record (set aside). All on disk under `poc/data/`, not in Git.

Ledgers, each a folder with `views.sqlite`, `archive.sqlite`, `manifests/`, logs, scripts and a pid file: `english-v29-nvda-3m-2026-10-27` (poc-v29/v30, paused after 2026-08-24, 352 MB), `english-v32-nvda-3m-2026-10-27` (poc-v32, 119 items, paused), the week tests `english-v32-`, `-v33-`, `-v34-`, `-v34b-`, `-v34c-nvda-week-2026-10-27` (2026-07-01..07, D199–D204), and `english-v34-nvda-3m-2026-10-28` (the resume with poc-v34 and the D202–D204 writer). Scratch archives of the extraction arms: `poc/data/evidence-gate-2026-10-27/archive.sqlite` (every A/B send of rows 61–62); of the evidence-in-view A/B: `docs/research/2026-10-27-evidence-in-view/ab-archive.sqlite` (git-ignored). Step 3/4 measurements (rows 63–65): `poc/reports/2026-10-27-stage34-gold/` on the main checkout (arm1, arm2, fresh1, fresh2, jev-contradicts, the 47-replacement writer replay), 135 MB on disk. Costs: `poc/reports/2026-10-27-nvda-3m/cost-ledger.md`.

## Traces and reports

Per-item trace pages are generated from a ledger and its archive by `scripts/trace_items.py`; the ones built this phase stay on disk under `poc/reports/*/trace*/` and are git-ignored. The benchmark reports, probes and recall oracles of rows 41–49 are in `poc/reports/2026-10-25-*` (in Git, except the three recall-oracle call archives `poc/reports/2026-10-25-recall-oracle*/archive.sqlite`, 6–10 MB each, which stay on disk and in the backup); the golds they score against are in `poc/eval/gold/` with `SHA256SUMS`.
