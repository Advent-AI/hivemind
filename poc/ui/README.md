# Thesis UI

A browsable research library with reusable thesis cards, charts, evidence lists and detail panels. The default page reads all 90 collected English theses and their stored research groups, with subject/status/search filters and dated membership. The Idea entry point in `src/idea/idea.js` posts the user's text to `/ideas`, adapts the response with `fromIdeaResponse`, and preserves the supplied connections through `graphOf` (D138). The superseded local matcher, `legacy/idea.js`, has been removed.

## Data boundary

[thesis.schema.json](src/model/thesis.schema.json), version `thesis-ui/2`, is the canonical UI contract. `parseDataset` validates, copies and freezes the data. Invalid input raises a `ContractError` with its field path; it never replaces the screen with a partial dataset.

Adapt existing bundles once with `fromBundles`. Cards do not rename fields or infer scores. `GET /library` or MCP `thesis_library` returns the full dated library. `createLibrary(root, {dataset})` renders it; its lifecycle supports `setDataset`, `getDay` and `destroy`. `coverage: selection` bundles include only loaded group members. Canonical v1 payloads remain readable through the compatibility boundary.

```js
import {createThesisExplorer, fromBundles} from './src/index.js';
import './src/styles/index.css';

// The caller selected these theses. This GET reads data without a model call.
const response = await fetch('/thesis-bundles?ids=v3,v1,v7&as_of=2026-08-15');
if (!response.ok) throw new Error(`Cannot load theses (${response.status})`);
const dataset = fromBundles(await response.json());

const explorer = createThesisExplorer(document.querySelector('#explorer'), {dataset});
explorer.showGraph({primaryId: 'v3', supportingIds: ['v1', 'v7']});
explorer.openThesis('v3');

// Validate before replacing the screen; invalid input leaves it unchanged.
explorer.setDataset(nextDataset);
// Remove DOM, events and animations when the host unmounts.
explorer.destroy();
```

The equivalent MCP call is `thesis_bundles({view_ids: ['v3','v1','v7'], as_of:'2026-08-15'})`.

Pass a `/ideas` response to `fromIdeaResponse`; `graphOf(response)` returns `rootIds` and `branches[{sourceId,targetId}]`. All chosen theses are roots. A related thesis's source comes from `related[].via`, never its array position. The UI does not call a model, hold credentials or choose theses for the agent.

Load a relationship's target before displaying it explicitly in `supportingIds`. Unloaded references can remain in the data, but the UI does not invent cards. Historical closure comes from `switches[].day`, not an inferred due-date rule.

Click the completed Idea card, or press Enter/Space while it is focused, to open analysis. `createIdeaDetail({root})` opens the existing service response with `open(card, theses)`, using the optional canonical thesis array to resolve names; `close()` and `destroy()` own its lifecycle. Opening the drawer makes no requests.

Pending cards render `idea/progress.js`: actual stages arrive through `readIdea(..., {onProgress})` over optional NDJSON. The client also accepts legacy JSON. Bootstrap keeps progress per request and adds the final card-preparation stage when bundle loading begins. No timer invents progress; only the active node animates, with a reduced-motion fallback.

## Components and fields

| Component | Main inputs |
|---|---|
| `createThesisCard` | `question`, `rungs[].score/label`, judgements visible as of the selected date |
| `ladderChart` / `bindHistoryChart` | Explicit scores, `judgements[].day/seq/rung`, `evidence[].arrival_day` |
| `createThesisDetail` | The same thesis's snapshot, sources, lifecycle switches and relationships |
| Evidence list | `one_line`, `quote`, `tier`, `source`, `original_who`, `replaced_by` |
| `createCanvas` | Caller-supplied roots, branches and optional leading card; the `primaryId/supportingIds` entry point remains available |

Evidence `day` is the display/source date; `arrival_day` is when it entered that thesis. Replay and evidence bars use the latter. A judgement's cited evidence must exist and must not arrive after that judgement. The contract rejects unknown fields, duplicate IDs, invalid dates and invalid states.

Display text is escaped, source links allow only HTTP/HTTPS, and cards do not use native hover-title tooltips. Each instance owns its state, events, DOM IDs and chart clip IDs, so two can mount together. The host supplies container height. Components inherit the [shared theme tokens](../../web/design-system/tokens.css) and use Geist.

## Development and verification

From the repository root:

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

Use the repository's configured Python environment for Python checks. Run the final documentation check only after the reasoning refresh required by AGENTS.md.

`poc/mock/index.template.html` is the page shell. The generated `poc/mock/index.html` embeds CSS, JavaScript and validated data for standalone opening. The default build reads `english-v23-jev-2026-10-25/views.sqlite` and `items-window-tags2-2026-10-24.sqlite` directly. `--ledger` and `--items` override them; `--data` selects an explicit legacy JSON export. Building does not modify source data or translation caches. esbuild, Ajv, ESLint and Prettier are build/development tools; the browser uses the generated standalone validator.

`npm --prefix poc/ui run verify:page` generates `poc/ui/dist/verify.html` for real-browser checks of multiple instances, invalid updates, teardown and empty history. Do not hand-edit `dist` or the generated validator.

The [design record](../../docs/poc/thesis-ui.md) contains data and state tables. Components themselves perform no requests or model calls. Only `src/idea/idea.js` and the page entry point `src/bootstrap.js` call the service, defaulting to `http://127.0.0.1:8788`; the host can set `<body data-api="…">`.

`node poc/ui/verify-library.mjs` creates `poc/ui/dist/library-check.html` to verify invalid/empty snapshots, a narrower date span, teardown and unique DOM IDs in a real browser.

## Composite preview

Build the reviewed D185 example into the standalone page explicitly:

```sh
python3 scripts/mock_build.py --composite-trials poc/config/idea-composite-trial-2026-10-26.json
```

The default build omits trial baskets. Only the exact configured Idea and date receive this trial chart. `prepareCompositeTrial` checks representative identity and connections; `compositeAt` reads a dated point; `scoreHistoryChart` renders fractional values with the shared chart style. The trial does not modify the canonical thesis schema or write an Idea score into the ledger.

`prepareIdeaComposite(card, dataset)` reads the API's validated composite plan and aligns supporting endpoints to the existing score orientation. `idea-composite/4` contains only adopted theses, each with a positive integer `weight_percent` and a `weight_reason`; nonempty plans total 100. It calculates dated weighted support; a date missing any adopted assessment stays unavailable. The analysis drawer exposes those adopted weights and their rationale under Theses. Older plan versions remain supported under their original contracts.

For an Idea graph, pass the validated `weightPercents` map in `showGraph(...)`; `bootstrap.js` derives it from the adopted response. The shared Thesis card receives `weightPercent` and shows it at the top right. A v4 response draws only adopted theses, with no zero-weight or automatically related cards. Ordinary library cards omit the badge. This metadata never changes the canonical thesis or its score.

Idea presentation uses `confidenceFromScore` and `confidenceHistory` to map the aggregate to 0–100%. `formatConfidence` rounds the compact card to a whole percentage; the detail header uses the same rounded percentage. The Idea chart passes `scale: "confidence"` to the shared chart renderer. Individual thesis charts keep their existing scale.

Both detail drawers use `components/detail-tabs.js` for tab selection, keyboard navigation and scroll reset. Each drawer owns its content, disclosures and lazy rendering. Idea details have Overview, Trace and Response tabs; Trace shows expanded reading steps, while raw search records remain in Response.
