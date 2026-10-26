# Hivemind

Hivemind reads a stream of information as a hedge-fund analyst would: it identifies theses, links supporting and opposing evidence, and updates its judgement as information arrives. Equities, commodities and cryptocurrencies use the same process.

This repository rebuilds the earlier system in `../tn-hivemind`. The experimental implementation is in `src/hivemind`, `poc` and `scripts`. [Current state](docs/CURRENT_STATE.md) records measured results, open defects and the next task. The English pipeline runs end to end on extraction v10 with Jev matching (D169) and is measured per state against read golds; it has not passed product acceptance.

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
  Rejudge open theses whose inputs changed, dependencies first.
  ↔ Save matching records for human labelling and future model training
```

A thesis has a question, an outcome ladder and a due date, fixed when it is created. An asset thesis concerns a company, cryptocurrency or commodity; its five rungs run from strongly bullish to strongly bearish. A theme thesis concerns macroeconomics, policy or an industry; its rungs name outcomes without judging them as good or bad. A yes/no question has two rungs.

The thesis has one current state: a rung on its ladder. A dependency means one thesis reads another's conclusion when judged. Succession records which period follows which. Group association collects related business questions; it is distinct from a dependency or duplicate identity. Its extraction and storage requirements are specified, but it is not enabled in the default pipeline.

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

## Open the design

Clone the repository if needed:

```sh
git clone https://github.com/Advent-AI/hivemind.git
```

Open `docs/system-design.html` in a browser. Its PRDs load from `docs/system-design/prd-bundle.js` when opened from disk. Alternatively, serve the repository root:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000/docs/system-design.html>. Serving the repository root preserves PRD and icon paths.

- **New** shows this system; **Old** is the historical source-code comparison.
- Select a module or its number to open details. Status labels distinguish frozen modules from earlier drafts.
- Open a module's detailed flow, decision tree and examples, or follow its PRD link.
- The system PRD contains the overview and glossary.

## Run the pipeline

Replay the item window into a new ledger with the default configuration (`poc/config/poc-v25.json`: extraction v12 on `gpt-6-luna` with the admission fields of D184, matching on Jev); credentials are read from `~/.config/hivemind/credentials.json`, never from the repository:

```sh
python3 scripts/preflight.py --archive <an archive> --views <ledgers> --items poc/data/items-window-tags2-2026-10-24.sqlite   # $0, before any paid run
python3 scripts/replay.py --from 2026-07-24 --until 2026-07-31 --views poc/data/<run>/views.sqlite --archive poc/data/<run>/archive.sqlite --cap 3
python3 scripts/replay.py ... --workers 1       # the serial path: resumes a day a serial run left unfinished
```

The replay runs the parallel day by default (D183): up to 16 later items' extraction requests are prepared early (`--workers`), and each is accepted only if it is byte-identical, at its turn, to the request built from everything committed before it; `--jev-workers` sets the Jev matching questions sent at a time (8; 1 for another matching engine). The ledger equals the serial one for the same answers, 4.46x faster on a busy day of fresh calls, at about 24% more cost; a rerun on saved answers pays for the early requests its archive lacks. The live measurement and its checks are in `poc/reports/2026-10-26-e2e-parallel/results.md`.

Measure a ledger per state against the golds in `poc/eval/gold/` with `scripts/benchmark_states.py` (candidates, groups, evidence, threshold robustness, cost per stage at published rates), `scripts/score_evidence_gold.py` and `scripts/recall_oracle.py` (evidence retrieval measured apart); `scripts/trace_items.py` renders per-item trace pages. The ledgers, archives and traces of the 2026-10-25 phase are listed in the [data manifest](docs/research/2026-10-25-english/data-manifest.md); `poc/data/` is not in Git.

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
