# Hivemind

Hivemind reads a stream of information as a hedge-fund analyst would: it identifies theses, links supporting and opposing evidence, and updates its judgement as information arrives. Equities, commodities and cryptocurrencies use the same process.

This repository rebuilds the earlier system in `../tn-hivemind`. It contains a working proof of concept, a browsable thesis library and an Idea explorer. The pipeline runs end to end and has been measured on one company and one 14-day window; it has not passed product acceptance. [Current state](docs/CURRENT_STATE.md) records what runs, the open defects and the one next task; [Decisions](docs/DECISIONS.md) records what is decided now.

For example, an Idea about NVIDIA revenue can draw on several stored theses. The explorer shows the selected theses, their weights, evidence and historical assessments. Its confidence chart applies the selected weights to those assessments; it is not a calibrated probability of the Idea coming true.

## Start here

| Goal | Start with |
|---|---|
| Browse the included demo | [Thesis Library and Explore Ideas](poc/mock/index.html); serve it locally using the command below |
| Understand the system | [Design page](docs/system-design.html) and [PRD index](docs/prd/README.md) |
| Run the API or connect an agent | [Run the service for testing](#run-the-service-for-testing) and [service contract](docs/poc/service.md) |
| Run or measure the pipeline | [Run the pipeline](#run-the-pipeline) and the [pipeline guide](docs/poc/pipeline-plan.md) |
| Work on the UI | [Frontend integration and development](poc/ui/README.md) |
| Work on this repository | [Working rules](AGENTS.md), [current state](docs/CURRENT_STATE.md) and [decisions](docs/DECISIONS.md) |

The UI has two workspaces. **Thesis Library** browses the collected English snapshot and its research groups. **Explore Ideas** submits a question to the API and displays an analysis with weighted theses. Its Trigger compares the displayed confidence with a chosen threshold. Its Action card is an editable preview with a dated NVDA price snapshot; it has no wallet connection or order execution.

## Open the demo and design

Clone the repository, then serve its root. Replace the example path with your checkout's absolute path:

```sh
git clone https://github.com/Advent-AI/hivemind.git
repo=/absolute/path/to/hivemind
python3 -m http.server 8000 --bind 127.0.0.1 --directory "$repo"
```

Open <http://127.0.0.1:8000/poc/mock/index.html> for the app, or <http://127.0.0.1:8000/docs/system-design.html> for the design. Stop the page server with Ctrl-C. The included standalone page can browse its embedded snapshot without the API; submitting an Idea needs the service below.

The design page also opens directly from disk. **New** shows the rebuild and **Old** the historical comparison. Select a module to read its flow, examples and linked PRD. The bundled PRDs keep these links usable without a server.

## How it works

```text
Research universe: what to research and which information categories to track
  ↓ determines what upstream supplies
Upstream (outside this system): obtain information and classify it
  ↓
Start with an empty ledger or a supplied, article-created research library.
The default does not build a cold-start library or import the former preset questions.
  ↓
Each day, in order:
  Dispatch: validate each item, assign a sequence number and route it
  Extraction (read-only): read the whole item with the questions open at the start
    of the day; return evidence with sources, the questions each statement bears on,
    candidate questions and research groups; a statement no question takes is dropped
  Thesis library: match each candidate (open, merge, continue a period, or skip) and
    each evidence piece (repeat, replacement or new); save matching records for labelling
  Judging: once at the end of the day, re-judge the open questions whose evidence
    changed, dependencies first
  Pull mode: close every question whose due day has come, at the rung it stands on
```

A thesis has a question, an outcome ladder and a due date, fixed when it is created. An asset thesis concerns a company, cryptocurrency or commodity; its five rungs run from strongly bullish to strongly bearish. A theme thesis concerns macroeconomics, policy or an industry; its rungs name outcomes without judging them as good or bad. A yes/no question has two rungs.

The thesis has one current state: a rung on its ladder. A dependency means one thesis reads another's conclusion when judged. Succession records which period follows which. A research group collects the questions that track one ongoing matter; extraction declares it (D165), and it is distinct from a dependency or duplicate identity.

Other modules:

- **Config** selects model settings and the number of search results.
- **Pull mode** owns time-based work: at the end of each day it closes every question whose due day has come, at the rung it stands on; it re-judges nothing (D356).
- **Human review pool** holds unresolved identifiers, proposed themes outside the universe and repeated processing failures.

For example, NVIDIA's April 15, 2025 8-K says H20 exports to China require a licence and may cause a charge of up to $5.5 billion. With an empty library, extraction proposes a theme thesis about licences for the affected chips and an NVDA thesis about FY2026 China revenue versus FY2025. Each carries quotations from the filing. Matching can open both; the licence theme then reaches the revenue thesis through the theme block its judgement reads (D191, D195). AMD's subsequent MI308 filing can contribute to the same licence thesis. A Reuters retelling of the NVIDIA filing adds another source for existing evidence, not new corroboration.

## Design and implementation status

The foundational design was frozen on October 22, 2026; later decisions authorize specific changes and the POC build. A design freeze does not imply that the implementation has passed acceptance. Changes to a frozen module require a recorded decision.

| Module | Status |
|---|---|
| Research universe | First version frozen; specific themes remain a draft |
| Upstream classification, Config, dispatch | First versions frozen |
| Extraction | Frozen at extraction v74i (D274): one decider (D264) files each statement under the questions open at the start of its day; at coverage start each question reads the company's latest earnings report once, when one is found (D363–D365) |
| Thesis library, matching and judging | Frozen as the production configuration runs them (D354): Jev matching (D169) with the collision judge (D190); judging-v7 (D263) |
| Human review pool | Intake frozen; output not yet designed |
| Pull mode and closing at the due day | Decided and built: at the end of each day a due question freezes at its rung and closes; no separate final verdict (D54, D356) |

The replay default is `poc/config/poc-v118.json` (D370); it removes seeded starting questions and the separate coverage-start report import. It has not been accepted end to end. Every measurement uses one frozen ruler: the extraction standard [`docs/prd/05-extraction-standard.html`](docs/prd/05-extraction-standard.html) (its version 5: version 3 as signed in D243, with D248's and D250's boundaries) with its golden set golden-v5, the seed questions and the judgement gold ([AGENTS §7.1](AGENTS.md); D261, D262). Tests fail when a piece of either moves (`tests/test_frozen_rulers.py`, `tests/test_frozen_extraction_prompt.py`, `tests/test_frozen_questions_and_judgement.py`, `tests/test_baseline.py`). Maintained documentation, new product text and pages written for Alex's review are in English (D163, D368); historical records and quotations keep their original language.

## Local requirements and data

Use Python 3.12 or later for the backend and Node.js 22 or later with npm for frontend builds. The HTTP service uses the Python standard library. The optional MCP service needs `mcp==1.26.0`. Frontend development dependencies are locked in `poc/ui/package-lock.json`.

The default backend reads these local files:

| Purpose | Path |
|---|---|
| Collected thesis ledger | `poc/data/served-2026-10-28-v34-nvda-3m-through-0828/views.sqlite` |
| Source items | `poc/data/items-nvda-2026-07-01-10-27.sqlite` (cleaned pages, D351, with the whole pages as fetched in column `text_page`; also kept apart in `items-nvda-2026-07-01-10-27.page.sqlite`) |
| Replay configuration | `poc/config/poc-v118.json` (D370): v108 extraction, matching and judging settings without seeded starting questions or separate report import |
| Idea configuration | `poc/config/poc-v118-idea.json`: two discovery calls and a final adoption/weighting call |
| Derived service index and Idea archive | `poc/data/service-english/` by default; overridable per run |

`poc/data/` is excluded from Git. A fresh clone includes the standalone demo, not these databases. Use the [data manifest](docs/research/2026-10-25-english/data-manifest.md) to locate preserved runs, or supply your own files with the documented CLI options. Keep provider credentials in the owner-only local file `~/.config/hivemind/credentials.json`, outside the repository.

### Switching the served data

The page build, the two services and Compose each carry the same two defaults: the thesis ledger (`views.sqlite`) and the items database the ledger's input ids come from. Swap both together; a ledger whose items are missing shows evidence without titles or sources. Serve a copy of a ledger a run may still write (`snapshot.sh` in a run folder makes one with SQLite's backup API), never the file the run writes. The places that name the defaults, all changed in one edit:

| Place | What to change |
|---|---|
| `scripts/mock_build.py` | `--ledger` and `--items` defaults, then `python3 scripts/mock_build.py` rebuilds `poc/mock/index.html` |
| `scripts/hivemind_api.py` | `--views` and `--items` defaults |
| `scripts/hivemind_mcp.py` | `--views` and `--items` defaults |
| `docker-compose.yml` | the `/data/ledger` and `/data/items/items-window.sqlite` volumes of both services |
| This README and `poc/ui/README.md` | the default paths named in the table above and in the build description |
| `tests/test_ui_bundles.py` | `SERVED_VIEWS` and `SERVED_GROUPS`, the served library's thesis and group counts |

Then restart the API in a new dated service folder (below) so the search index is built for the new ledger. The current default, `served-2026-10-28-v34-nvda-3m-through-0828`, is the three-month NVDA run (`poc-v34`, extraction v18) stopped and sealed at 2026-08-28 on evidence bloat (D358); its folder README names the one empty thesis removed.

## Run the service for testing

Run test services on the host. Start with read-only browsing and lexical search, which need no model or embedding calls. In the same shell where `repo` names the checkout, create a fresh dated run directory for the log, PID and derived files:

```sh
service_run=$(mktemp -d "$repo/poc/data/service-$(date +%F)-XXXXXX")
nohup python3 "$repo/scripts/hivemind_api.py" --port 8788 \
  --lexical --config '' \
  --index "$service_run/search-index.sqlite" \
  --archive "$service_run/idea-archive.sqlite" \
  > "$service_run/api.log" 2>&1 &
printf '%s\n' "$!" > "$service_run/api.pid"
curl -fsS http://127.0.0.1:8788/days
```

`/days` returns the first and last completed ledger day. See the log if startup is not ready. To enable Idea submission and semantic search, stop this instance and start the same command without `--lexical --config ''`. That selects the default Idea configuration above and can call the embedding and language models. Exact archived requests can replay without another model call; changed requests can incur cost.

The app calls `http://127.0.0.1:8788`; its host may override this with `<body data-api="…">`. `/library` returns the dated snapshot. `--views` and `--items` select other source databases; `--index`, `--archive` and `--config` select derived storage and configuration. Stop only the API instance you started:

```sh
kill "$(cat "$service_run/api.pid")"
```

For an agent, `scripts/hivemind_mcp.py` defaults to stdio. Use `--transport streamable-http --host 127.0.0.1 --port 8789` to serve `/mcp`, and `--lexical` for model-free reads. The [service contract](docs/poc/service.md) lists the tools and historical-read rules.

Docker is an alternative when its outbound networking works. Compose mounts the source ledger/items read-only, `poc/data/service-english/` read-write, and credentials read-only. Prepare the MCP wheels on the host before building:

```sh
python3 -m pip download mcp==1.26.0 --dest build/wheels --only-binary=:all: --platform manylinux2014_aarch64 --platform manylinux_2_17_aarch64 --platform any --python-version 3.12 --implementation cp --abi cp312 --abi abi3 --abi none   # once, for the MCP image
docker compose up --build -d
docker compose ps && curl -s http://127.0.0.1:8788/days
docker compose down
```

The recorded VPN setup on this Mac blocked outbound model calls from Docker; host operation is the tested workflow, and container connectivity needs a fresh check before a container model run.

## Run the pipeline

Replay writes a new thesis ledger and model-call archive. Before a paid run, replay the relevant saved answers through the current checks at no model cost:

```sh
python3 "$repo/scripts/preflight.py" \
  --archive /absolute/path/to/preserved/archive.sqlite \
  --views /absolute/path/to/preserved/views.sqlite \
  --items "$repo/poc/data/items-nvda-2026-07-01-10-27.sqlite"
```

Inspect changed refusals before continuing. A replay is a paid run: it starts only when authorized, in a new dated folder, with the agreed spending cap. The default starts without seeded questions and can read an existing article-created library:

```sh
python3 "$repo/scripts/replay.py" --from 2026-07-01 --until 2026-07-14 --only NVDA --cap 3 \
  --views /absolute/path/to/new-run/views.sqlite --archive /absolute/path/to/new-run/archive.sqlite
```

`--cap` is checked after each item: parallel calls already sent and the day's judging round can exceed it, so it is not a hard whole-run limit. The default is `poc-v118`; the default input database is `poc/data/items-nvda-2026-07-01-10-27.sqlite`. A ledger containing the retired seeded questions is refused. Earnings releases still enter as actual source items; a report is not appended as background to other items. The new replay default is not accepted end to end. The historical seeded judgement scorer requires its frozen seeds and therefore is not a valid scorer for the new no-seed run. The [pipeline guide](docs/poc/pipeline-plan.md) describes the stages.


## Build and check

From the checkout root:

```sh
npm ci --prefix poc/ui
python3 scripts/mock_build.py
npm --prefix poc/ui run lint
npm --prefix poc/ui run format:check
npm --prefix poc/ui test
npm --prefix poc/ui run test:mutations
PYTHONPATH=src:poc python3 -m pytest tests -q
python3 docs/check.py
```

Install pytest in your Python environment to run the Python tests. `mock_build.py` reads the local databases and embeds the dated market snapshot into `poc/mock/index.html`; it makes no model calls. `npm --prefix poc/ui run build` builds component assets only. The [frontend guide](poc/ui/README.md) covers the frontend in detail.

The tests make no model calls: `tests/conftest.py` refuses every credential read. `docs/check.py` checks generated blocks, glossary controls, classification simulation and page rendering, and rebuilds the PRD bundle. A pass does not replace the reasoning review in [the PRD index](docs/prd/README.md).

## Repository map

| Path | Purpose |
|---|---|
| `AGENTS.md` | Working rules: authority, diagnosing, design, code, tests, verification, writing prompts, measuring and iterating; `CLAUDE.md` points to it |
| `docs/DECISIONS.md` | What is decided now, by module, and every decision number's status |
| `docs/DECISIONS-log.md` | The full record of every decision, in number order |
| `docs/CURRENT_STATE.md` | What runs, open defects and the one next task |
| `docs/system-design.html`, `docs/system-design/new-*.js` | Maintained design page and its source data |
| `docs/prd/` | One specification per module and an index; `05-extraction-standard.html` is the extraction step's standard (signed, D243) |
| `docs/poc/` | The pipeline guide and the service, Idea card and UI contracts |
| `docs/check.py` | Mechanical design checks and PRD bundle refresh |
| `docs/research/` | Measurements, golds and reviews behind the decisions, by date; `2026-10-29-ledger-standard/` holds the standard's drafts and golden set |
| `docs/archive/` | Frozen design snapshots |
| `src/hivemind/`, `scripts/`, `poc/` | Implementation, entry points and the POC corpus, configurations and universe |
| `poc/eval/gold/`, `poc/reports/` | Earlier golds and the measured reports behind the build log |
| `reports/`, `research_notes/` | Research and reviews behind the design |
