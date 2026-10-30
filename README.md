# Hivemind

Hivemind reads a stream of information as a hedge-fund analyst would: it identifies theses, links supporting and opposing evidence, and updates its judgement as information arrives. Equities, commodities and cryptocurrencies use the same process.

This repository rebuilds the earlier system in `../tn-hivemind`. It contains a working proof of concept, a browsable thesis library and an Idea explorer. The English pipeline runs end to end, but has not passed product acceptance. [Current state](docs/CURRENT_STATE.md) records the measured results, open defects and one next task.

For example, an Idea about NVIDIA revenue can draw on several stored theses. The explorer shows the selected theses, their weights, evidence and historical assessments. Its confidence chart applies the selected weights to those assessments; it is not a calibrated probability of the Idea coming true.

## Start here

| Goal | Start with |
|---|---|
| Browse the included demo | [Thesis Library and Explore Ideas](poc/mock/index.html); serve it locally using the command below |
| Understand the system | [Design page](docs/system-design.html) and [PRD index](docs/prd/README.md) |
| Run the API or connect an agent | [Run the service for testing](#run-the-service-for-testing) and [service contract](docs/poc/service.md) |
| Work on the UI | [Frontend integration and development](poc/ui/README.md) |
| Check what is finished | [Current state](docs/CURRENT_STATE.md) and [recorded decisions](docs/DECISIONS.md) |

The current UI has two workspaces. **Thesis Library** browses the collected English snapshot and its research groups. **Explore Ideas** submits a question to the API and displays an analysis with weighted theses. Its Trigger compares the displayed confidence with a chosen threshold. Its Action card is an editable preview with a dated NVDA price snapshot; it has no wallet connection or order execution.

This documentation update describes the working POC. The latest Trigger/Action implementation and other uncommitted development work are being kept local; this documentation-only commit does not publish them. The committed demo may therefore show the earlier frontend.

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
Dispatch: validate each item, assign a sequence number and route it
  ↓
Extraction (read-only): read the whole item with the existing theses;
  return evidence with sources and complete candidate theses
  ↓
Thesis library: search and match each candidate;
  merge it, continue a previous period, open a new thesis, or skip it.
  Compare evidence within its thesis: repeat, replacement, or new evidence.
  At day-end, rejudge open theses whose inputs changed, dependencies first.
  ↔ Save matching records for human labelling and future model training
```

A thesis has a question, an outcome ladder and a due date, fixed when it is created. An asset thesis concerns a company, cryptocurrency or commodity; its five rungs run from strongly bullish to strongly bearish. A theme thesis concerns macroeconomics, policy or an industry; its rungs name outcomes without judging them as good or bad. A yes/no question has two rungs.

The thesis has one current state: a rung on its ladder. A dependency means one thesis reads another's conclusion when judged. Succession records which period follows which. Research groups collect related business questions and are enabled in the default pipeline. Their [contract](docs/prd/06-views.md#research-groups-associate-during-extraction) is separate from dependency and identity matching.

Other modules:

- **Config** selects model settings and the number of search results.
- **Pull mode** owns time-based work: revisit theses at day-end or on a schedule, then freeze and close each thesis when due.
- **Human review pool** holds unresolved identifiers, proposed themes outside the universe and repeated processing failures.

For example, NVIDIA's April 15, 2025 8-K says H20 exports to China require a licence and may cause a charge of up to $5.5 billion. With an empty library, extraction proposes a theme thesis about licences for the affected chips and an NVDA thesis about FY2026 China revenue versus FY2025. Each carries quotations from the filing. Matching can open both and record the revenue thesis's dependency on the licence thesis. AMD's subsequent MI308 filing can contribute to the same licence thesis. A Reuters retelling of the NVIDIA filing adds another source for existing evidence, not new corroboration.

## Design and implementation status

The foundational design was frozen on October 22, 2026, except for pull mode and the final verdict. Later decisions authorize specific changes and the POC build. A design freeze does not imply that the implementation has passed acceptance.

| Module | Design status |
|---|---|
| Research universe | First version frozen; specific themes remain a draft |
| Upstream classification, Config, dispatch | First versions frozen |
| Extraction | Foundation frozen; English prompts v10 in the default pipeline; groups declared during extraction (D165, D166) |
| Thesis library and matching records | Foundation frozen; matching on Jev by default (D169) with the D168 rules; listed open questions pending |
| Human review pool | Intake frozen; output not yet designed |
| Final verdict | Earlier draft; freezing the state on the due date is decided |
| Pull mode | Earlier draft; day-end/scheduled work and due-date freezing are decided |

Changes to frozen modules require a recorded decision. [Decisions](docs/DECISIONS.md) contains the history; [Current state](docs/CURRENT_STATE.md) identifies active work. Historical records and original source material retain their original language. Maintained documentation and new product text use English under D163.

## Local requirements and data

Use Python 3.12 or later for the backend and Node.js 22 or later with npm for frontend builds. The HTTP service uses the Python standard library. The optional MCP service needs `mcp==1.26.0`. Frontend development dependencies are locked in `poc/ui/package-lock.json`.

The default backend reads these local files:

| Purpose | Path |
|---|---|
| Collected thesis ledger | `poc/data/english-v23-jev-2026-10-25/views.sqlite` |
| Source items | `poc/data/items-window-tags2-2026-10-24.sqlite` |
| Replay configuration | `poc/config/poc-v23.json`: extraction v10 and Jev matching |
| Idea configuration | `poc/config/poc-v33-idea.json`: two discovery calls and a final adoption/weighting call |
| Derived service index and Idea archive | `poc/data/service-english/` by default; overridable per run |

`poc/data/` is excluded from Git. A fresh clone includes the standalone demo, not these databases. Use the [data manifest](docs/research/2026-10-25-english/data-manifest.md) to locate preserved runs, or supply your own files with the documented CLI options. Keep provider credentials in the owner-only local file `~/.config/hivemind/credentials.json`, outside the repository.

## Run the service for testing

Run test services on the host. Start with read-only browsing and lexical search, which need no model or embedding calls. In the same shell where `repo` names the checkout, create a fresh dated run directory for the log, PID and derived files:

```sh
service_run=$(mktemp -d "$repo/poc/data/service-2026-10-27-XXXXXX")
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

The recorded VPN setup on this Mac blocked outbound model calls from Docker. Host operation is the tested workflow; the documentation refresh does not establish that container connectivity has changed.

## Run the pipeline

Replay writes a new thesis ledger and model-call archive. Before a paid run, replay the relevant saved answers through the current checks at no model cost:

```sh
python3 "$repo/scripts/preflight.py" \
  --archive /absolute/path/to/preserved/archive.sqlite \
  --views /absolute/path/to/preserved/views.sqlite \
  --items "$repo/poc/data/items-window-tags2-2026-10-24.sqlite"
```

Inspect changed refusals before continuing. For an authorized replay, use a new dated destination and the agreed spending cap; `--help` lists the options:

```sh
python3 "$repo/scripts/replay.py" --help
```

The default replay configuration is `poc-v23`; experimental admission and concurrency configurations are not the default. The [pipeline guide](docs/poc/pipeline-plan.md) describes the implemented stages. `scripts/benchmark_states.py`, `scripts/score_evidence_gold.py` and `scripts/recall_oracle.py` measure separate parts of the result; `scripts/trace_items.py` renders per-item traces.

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

Install pytest in your Python environment to run the Python tests. `mock_build.py` reads the local databases and embeds the dated market snapshot into `poc/mock/index.html`; it makes no model calls. `npm --prefix poc/ui run build` builds component assets only. The [frontend guide](poc/ui/README.md) covers custom data paths and browser fixtures. Run the reasoning refresh below before the final documentation check.

## Repository map

| Path | Purpose |
|---|---|
| `src/hivemind/`, `scripts/`, `poc/` | Implementation, entry points and the POC corpus, configurations and universe |
| `poc/eval/gold/`, `poc/reports/` | Golds read from the texts, and the measured reports behind the build log |
| `docs/research/2026-10-25-english/` | The English library build log (one row per measured step) and the data manifest |
| `docs/system-design.html`, `docs/system-design/new-*.js` | Maintained design page and its source data |
| `docs/system-design/old-*.js` | Historical system comparison |
| `docs/prd/` | One specification per module and an index |
| `docs/DECISIONS.md` | Recorded decisions |
| `docs/CURRENT_STATE.md` | Status, known defects and next task |
| `docs/views-rebuild-log.md` | Historical thesis-library design discussion |
| `docs/check.py` | Mechanical design checks and PRD bundle refresh |
| `docs/archive/` | Frozen design snapshots; intermediate snapshots remain in Git history |
| `reports/`, `research_notes/` | Research and reviews behind the design |
| `AGENTS.md` | Working rules; `CLAUDE.md` points to it |

## After changing the design

Read every module in the order and with the questions in [the PRD index](docs/prd/README.md). Reconcile the page, specifications and decisions, then run:

```sh
python3 docs/check.py
```

The script checks generated blocks, glossary controls, classification simulation and page rendering, and rebuilds the PRD bundle. A pass does not replace the reasoning review or establish product acceptance.
