# Data kept on disk, not in Git (sealed split experiment, D378)

The architecture benchmark and the screen keep these files on this machine only. Git ignores them (`.gitignore`: `docs/research/**/*.sqlite`
and the sealed-experiment block).

| Path (under this folder) | What it holds | Size | Rebuilt by |
|---|---|---|---|
| `runs/split-v3-d1..d3/` | split window draws: `views.sqlite` (ledger), `archive.sqlite` (every model call), `manifest.json`, `replay.log`, `run.out` | ~100 MB | not rebuildable without new calls; the archives answer an offline replay |
| `runs/control-v108-d1..d3/` | same-day production window draws | ~75 MB | as above |
| `runs/test-split-d1..d3/`, `runs/test-control-d1..d3/` | test-article draws: `handovers.json`, `archive.sqlite`, `manifest.json` | small | as above |
| `runs/gate-v108-d1-offline/`, `gate-v108-d1-offline-r2/`, `gate-v108-d1-offline-stored-writer/` | the comparability gate's replays of r10-control-v108/d1 | ~50 MB | `bench_run.py --offline --archive-from <r10 archive>` |
| `fixture/views.sqlite` | the 22-seed starting ledger, sha256 `eadb16a0…` | 0.3 MB | `bench_run.fixture()` from `poc/seeds/nvda-2026-07-01-v2.json` |
| `screen/archives/C1..C6, R1..R3, P1..P3.sqlite` | the screen's sends | 37 MB | not rebuildable without new calls |
| `results/traces-*.json`, `results/chunks/` | reading packets | 7 MB | `bench_traces.py` from the hits files and the runs |
| `results/*.log`, `screen/*.log`, `../2026-11-05-production-plan/r*/codex.log` | reviewer and reader transcripts; their answers are in the `.out` files beside them | up to 3 MB each | — |

The items database the runs read is not copied here. The eight byte-identical copies made for the runs were deleted on 2026-11-06, at Alex's
request to clean up (`deleted-copies-2026-11-06.txt`). The original stays at
`/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite` (sha256 `57bc2544…`).

The blind readers' answer keys, kept outside the repository during the reads, are now in `results/blind/keys/`. The first-100 reads' keys are in
`../2026-11-05-seven-day-request/blind-keys/`.
