# Hivemind

Hivemind reads a stream of information as a hedge-fund analyst would: it identifies theses, links supporting and opposing evidence, and updates its judgement as information arrives. Equities, commodities and cryptocurrencies use the same process.

This repository rebuilds the earlier system in `../tn-hivemind`. This branch, `fix/extraction-quality-2026-10-28`, holds the extraction work: the step's standard, its golden set and the extraction prompts. The service, the UI and the served data are documented on `main`. [Current state](docs/CURRENT_STATE.md) records this branch's measured results, open defects and next task. The pipeline runs end to end; it has not passed product acceptance.

**Which code is the latest (2026-10-30).** The newest pipeline code is this branch, `fix/extraction-quality-2026-10-28`, stacked on `feat/thesis-admission-v12` and `feat/parallel-day` (25 commits `main` does not have; all three pushed, none merged). Its replay default is `poc/config/poc-v67.json` (extraction role-v51, D246). `main` holds the newest service, UI and Idea code (3 commits this branch does not have) and still replays `poc-v23` (extraction v10). Merging the two is open work, listed in the [current state](docs/CURRENT_STATE.md); the next steps, principles and criteria are in the [handoff plan](docs/research/2026-10-29-ledger-standard/handoff-plan-2026-10-30.md).

## The extraction standard

[`docs/prd/05-extraction-standard.html`](docs/prd/05-extraction-standard.html) is the PRD for the extraction step and its one measuring standard, signed by Alex on 2026-10-29 (D243). It defines what the ledger records, the five kinds of question and when one is opened, which statements are kept as evidence and how much each weighs, the golden set built from it, and how a prompt change is written, measured and iterated. Open it directly in a browser. Its direction in Alex's words: lean cautious, most of a page is noise, and new information that adds to an answer is not missed.

The golden set is [`golden-v3-signed.json`](docs/research/2026-10-29-ledger-standard/golden-v3/golden-v3-signed.json) (118 articles, sha256 in D243). The drafts, the reader simulations, the drift reviews and the golden set's history are in [`docs/research/2026-10-29-ledger-standard/`](docs/research/2026-10-29-ledger-standard/README.md). The first version (D229) is superseded and kept as a source.

## How it works

```text
Research universe: what to research and which information categories to track
  ↓ determines what upstream supplies
Upstream (outside this system): obtain information and classify it
  ↓
Dispatch: validate each item, assign a sequence number and route it
  ↓
Extraction (read-only): read the whole item, without the library's theses;
  return evidence with sources, candidate questions and research groups
  ↓
Placement: file each statement under the narrowest open question;
  a statement no question takes is dropped, and evaluation reads the drops
  ↓
Thesis library: search and match each candidate;
  merge it, continue a previous period, open a new thesis, or skip it.
  Compare evidence within its thesis: repeat, replacement, or new evidence.
  Rejudge open theses whose inputs changed, dependencies first.
  ↔ Save matching records for human labelling and future model training
```

A thesis has a question, an outcome ladder and a due date, fixed when it is created. An asset thesis concerns a company, cryptocurrency or commodity; its five rungs run from strongly bullish to strongly bearish. A theme thesis concerns macroeconomics, policy or an industry; its rungs name outcomes without judging them as good or bad. A yes/no question has two rungs.

The thesis has one current state: a rung on its ladder. A dependency means one thesis reads another's conclusion when judged. Succession records which period follows which. A research group collects the questions that track one ongoing matter; extraction declares it (D165), and it is distinct from a dependency or duplicate identity.

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
| Extraction | Foundation frozen. On this branch the request is role-v51 (D246): no thesis or group shown (D211), a separate placement call under the one-home rule (D207, D209). The step's standard is the signed page above (D243); measured against it, and read beyond it, on 2026-10-30 (open defects in the current state) |
| Thesis library and matching records | Foundation frozen; matching on Jev (D169) with the collision judge (D190); listed open questions pending |
| Human review pool | Intake frozen; output not yet designed |
| Final verdict | Earlier draft; freezing the state on the due date is decided |
| Pull mode | Earlier draft; day-end/scheduled work and due-date freezing are decided |

Changes to frozen modules require a recorded decision. [Decisions](docs/DECISIONS.md) contains the history; decision numbers are per branch until a merge (D227). Historical records and original source material retain their original language. Maintained documentation and new product text use English under D163; pages written for Alex's review are in plain Chinese.

## Open the design

Open `docs/system-design.html` in a browser. Its PRDs load from `docs/system-design/prd-bundle.js` when opened from disk. Alternatively, serve the repository root:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000/docs/system-design.html>. Serving the repository root preserves PRD and icon paths. **New** shows this system; **Old** is the historical source-code comparison. Select a module to read its flow, decision tree and examples, or follow its PRD link.

## Run the pipeline

Replay the item window into a new ledger with the default configuration (`poc/config/poc-v67.json`: extraction role-v51 on `gpt-6-luna` (D246), placement under the one-home rule, a statement no question takes dropped as `no home` (D207, D209); matching on Jev with the collision judge (D190); judging with the theme block (D195) and the evidence in view (D198)). Credentials are read from `~/.config/hivemind/credentials.json`, never from the repository. Before any paid run, replay the stored answers through the current checks at no cost:

```sh
python3 scripts/preflight.py --archive <an archive> --views <ledgers> --items <items database>   # $0, before any paid run
python3 scripts/replay.py --from 2026-07-24 --until 2026-07-31 --views poc/data/<run>/views.sqlite --archive poc/data/<run>/archive.sqlite --cap 3
python3 scripts/replay.py ... --workers 1       # the serial path: resumes a day a serial run left unfinished
```

The replay runs the parallel day by default (D183): up to 16 later items' extraction requests are prepared early (`--workers`), and each is accepted only if it is byte-identical, at its turn, to the request built from everything committed before it; `--jev-workers` sets the Jev matching questions sent at a time. The ledger equals the serial one for the same answers. Use a new dated destination and the agreed spending cap; a full-pipeline run starts only on Alex's explicit instruction.

Measure a ledger per state with `scripts/benchmark_states.py`, `scripts/score_evidence_gold.py` and `scripts/recall_oracle.py`; `scripts/trace_items.py` renders per-item trace pages. `poc/data/` is not in Git; the [data manifest](docs/research/2026-10-25-english/data-manifest.md) lists preserved runs.

## Test

```sh
PYTHONPATH=src:poc python3 -m pytest tests -q
python3 docs/check.py
```

The tests make no model calls: `tests/conftest.py` refuses every credential read. `docs/check.py` checks generated blocks, glossary controls, classification simulation and page rendering, and rebuilds the PRD bundle. A pass does not replace the reasoning review in [the PRD index](docs/prd/README.md) or establish product acceptance.

## Repository map

| Path | Purpose |
|---|---|
| `AGENTS.md` | Working rules: diagnosing, design, code, tests, verification, writing prompts, measuring and iterating; `CLAUDE.md` points to it |
| `docs/prd/05-extraction-standard.html` | The extraction step's standard and golden set (signed, D243) |
| `docs/research/2026-10-29-ledger-standard/` | Its drafts, simulations, drift reviews and golden set |
| `docs/research/2026-10-29-analyst-standard/` | The first version (D229, superseded) and the prompt loop's log |
| `src/hivemind/`, `scripts/`, `poc/` | Implementation, entry points and the POC corpus, configurations and universe |
| `poc/eval/gold/`, `poc/reports/` | Earlier golds and the measured reports behind the build log |
| `docs/system-design.html`, `docs/system-design/new-*.js` | Maintained design page and its source data |
| `docs/prd/` | One specification per module and an index |
| `docs/DECISIONS.md` | Recorded decisions |
| `docs/CURRENT_STATE.md` | Status, known defects and next task |
| `docs/check.py` | Mechanical design checks and PRD bundle refresh |
| `docs/archive/` | Frozen design snapshots |
| `reports/`, `research_notes/` | Research and reviews behind the design |
