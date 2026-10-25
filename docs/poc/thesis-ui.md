# Thesis UI: data and component boundaries

This refactor covers thesis components and the page structure. Its initial scope left Idea judgement and matching in demo code. The subsequent October 24 update connected the Idea card to the service (`poc/ui/src/idea/idea.js`, `docs/poc/idea-card.md`): POST a sentence to `/ideas`, adapt the response with `fromIdeaResponse`, use `reading.chosen[0]` as the main card and the rest as supporting cards. The local `legacy/idea.js` matcher was removed at Alex's request.

For example, an agent retrieves the complete v3 record and passes it through one adapter. The card, history chart, evidence list and detail panel all read the same validated thesis instead of inferring separate field shapes.

## Scope and authority

- D76/D112: the service owns data retrieval and agent judgement. The UI does not call models, hold credentials or rewrite judgements.
- D78/D81/D87/D97–D129: preserve agreed terminology, colours, charts, interactions, centring and typography.
- The new entry accepts `thesis-ui/1`; existing `view_bundle` data passes through one adapter. The schema is the sole allowed-field list.
- This refactor does not alter extraction, matching, scoring or Idea product design, or enable paid calls. Add the read-only `thesis_bundles` / `GET /thesis-bundles` entry using the existing bundle writer.

## Original inventory

`data.en.json` contained 42 theses, 375 judgements, 1,089 evidence links, 44 lifecycle switches and 32 dependencies. Chinese and English files shared a structure. The former single page combined rendering, domain derivation, interaction and demo matching. Bundles supplied positions while the UI inferred scores from labels. Switches/dependencies had sequence numbers only; publication day was treated as arrival day, leaving insufficient dates for faithful historical replay.

## Ownership

| Module | Input | Responsibility | Excludes |
|---|---|---|---|
| `model/thesis.schema.json` | Canonical agent data | Versioned closed shape | Rendering |
| `adapters/bundle.js` | Mock/API bundle | Explicit scores, dates and canonical theses | Network/model calls |
| `model/contract.js` | Canonical data | Schema, reference and time validation; field-path errors | Repairing invalid data |
| `model/thesis.js` | Validated data and date | Current judgement, state, evidence, relations and history selection | DOM |
| `components/thesis-card.js` | Thesis and date range | Card | Idea matching |
| `components/thesis-chart.js` | Thesis, date range, callbacks | Chart and selection coordinates | Fetching |
| `components/thesis-detail.js` | Dataset, thesis ID, date | Overview/Evidence/History, local state and destruction | Global variables |
| `components/canvas.js` | Selected cards and callbacks | Layout, edges, pan and zoom | Selecting Idea matches |
| `idea/idea.js` | User input and service response | Service-backed Idea flow | The removed local demo matcher |

## Value × reader

| Value | Writer | Reader/contract |
|---|---|---|
| id | Ledger/agent | Cards, selection and dependencies; unique within dataset |
| rung.position / score | Adapter/agent | Chart, badge and table; consecutive positions and explicit scores; two yes/no or five numeric states |
| judgement.id / day / seq / rung / cited | Ledger/adapter | Historical reads ordered by day, sequence and stable ID; references exist and cannot cite future evidence |
| evidence.day / arrival_day | Source/ledger | Display uses publication day; historical filtering and bars use arrival day |
| switches.day / dependencies.day | Ledger sequence date | Only records existing by the selected date affect state/relations |
| dataset.as_of / days | Host | Default date and replay bounds, never machine time |
| URI | Source | Only http/https become links; escape text and attributes |

## State × event

| State/event | Result |
|---|---|
| Valid data + mount/update | Validate then replace atomically; all components share one snapshot |
| Invalid data + update | Throw a field-path ContractError; preserve the existing view |
| Judged/unjudged, not created, closed | Explicit empty states; no invented score; read the selected date's switch |
| Unloaded relation target | Preserve reference; draw only loaded targets without inventing content |
| Thesis/data switch | Remove old events/animations and reset local detail state |
| Repeated expand/collapse | Reverse from current height; destruction cancels animation |
| History hover/click/quiet day | Preserve D122 selection rules; never read future judgements |
| Event after destruction | No listener or animation continues writing DOM |
| Two instances | Separate roots, ID prefixes, data and lifecycles; no global DOM queries |

## Existing checks and new entry

Mock and API bundles use the same adapter. Replay both languages' 42 mock theses, complete ledger bundles and stored `/ideas` samples without model calls. Cover missing/unknown fields, duplicate IDs, invalid dates/states/references, unordered input, source immutability, lifecycle/relation dates, time before first judgement, date gaps, replacement evidence and unsafe links.

Browser verification covers both ladder kinds, empty judgements, filtering, historical selection, reversing expansion and destruction. Run the Python suite once and `docs/check.py` last.

Keep the single-file mock build while organising source into ES modules. Use esbuild and Ajv for development; compile the schema to a standalone validator so the browser does not run a compiler. Budget: 200 KB JavaScript excluding data/fonts and 200 ms to validate the full sample. Report measurements separately from budgets. ESLint and Prettier are development-only.

## Recorded refactor results (historical, not a new D163 run)

- UI tests: 10 passed; both 42-thesis mock languages and 94 live bundles used the same contract.
- Three mutants were rejected: future judgement as current, publication day as arrival day, and early closure.
- Python: 31 tests passed, including real HTTP/MCP bundle reads.
- Browser: two instances had unique DOM IDs; invalid updates retained old data; destroying one did not affect the other. Empty history, both ladders, replay, filters, expansion and selection worked.
- Build: about 174 KB JavaScript; 42-thesis validation about 23 ms. Lint and format checks passed.
- The read layer added IDs and dates without changing classification, extraction, matching, rejudgement or expiry rules.
