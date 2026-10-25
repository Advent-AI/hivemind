# Thesis UI

Reusable thesis cards, charts, evidence lists and detail panels. The Idea entry point in `src/idea/idea.js` posts the user's text to `/ideas`, adapts the response with `fromIdeaResponse`, and preserves the supplied connections through `graphOf` (D138). The superseded local matcher, `legacy/idea.js`, has been removed.

## Data boundary

[thesis.schema.json](src/model/thesis.schema.json), version `thesis-ui/1`, is the canonical UI contract. `parseDataset` validates, copies and freezes the data. Invalid input raises a `ContractError` with its field path; it never replaces the screen with a partial dataset.

Adapt existing bundles once with `fromBundles`. Cards do not rename fields or infer scores.

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
python3 -m pytest tests -q
python3 docs/check.py
```

Use the repository's configured Python environment for Python checks. Run the final documentation check only after the reasoning refresh required by AGENTS.md.

`poc/mock/index.template.html` is the page shell. The generated `poc/mock/index.html` embeds CSS, JavaScript and validated data for standalone opening. Building does not modify source data or translation caches. esbuild, Ajv, ESLint and Prettier are build/development tools; the browser uses the generated standalone validator.

`npm --prefix poc/ui run verify:page` generates `poc/ui/dist/verify.html` for real-browser checks of multiple instances, invalid updates, teardown and empty history. Do not hand-edit `dist` or the generated validator.

The [design record](../../docs/poc/thesis-ui.md) contains data and state tables. Components themselves perform no requests or model calls. Only `src/idea/idea.js` and the page entry point `src/bootstrap.js` call the service, defaulting to `http://127.0.0.1:8788`; the host can set `<body data-api="…">`.
