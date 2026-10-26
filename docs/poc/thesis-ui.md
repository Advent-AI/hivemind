# Thesis UI: data and component boundaries

The page opens the collected English library, then lets the reader browse stored research groups or explore an Idea. All chosen Idea theses remain peers; only the service's supplied `via` links connect related cards (D138). A group is not a parent thesis and does not receive a generated score.

For example, the Vera Rubin group contains six stored member theses at August 15, 2026, and one at February 25. Loading a snapshot for either date shows that date's membership, assessments and sources. The frontend never re-runs extraction or assigns membership.

## Presentation rules

Use sentence case for interface labels, navigation, section titles and controls. Never force interface text to all capitals. Preserve the spelling of tickers, acronyms, proper names and quoted source text. Separate adjacent metadata fields with `|`, using the shared separator; do not use middle dots or bullets as metadata separators.

The library has no connection/Refresh region, Research library eyebrow, As of date control or duplicate count/date row above the cards (D182). The supplied snapshot defines the displayed date; charts and detail history retain their date behaviour. Automatic API loading keeps the current snapshot when unavailable.

Use “Show more” for pagination actions in both the library and evidence list. Library statistics also use `|` between fields.

Assessment citations use plain blue `[1]` text without a background, border or extra padding; hover adds an underline. Current and historical assessments share this style and retain their source-opening behaviour (D190).

Default canvas connectors use a 1.5px stroke and darker grey (`#aaa99f`), shared with their arrowheads. Active highlighting and routing are unchanged (D199).

Idea and Thesis canvas cards share a 440px width (D213). Canvas columns have at least 180px of horizontal space between cards; larger fan-outs retain any additional required room (D201).

Card scores appear in a pill beside the chart's “AI score” title, aligned to the right on the same row and using the same 11px text size. This applies to library/canvas Thesis cards. The Idea chart instead shows “AI confidence” and a 0–100% pill, using the same title-row layout (D197). Both charts draw at their actual content width, so their 11px subtitles and 10px vertical-axis labels render at the same scale. Completed Idea cards fit their content with the normal bottom padding (D202). Card headers no longer contain a score. Replay updates the pill from the same selected-date assessment as the chart (D193).

On an Idea canvas, each adopted Thesis card's upper-right header shows a scale icon and `xx%` from the validated Idea plan (D196/D198). Cards are ordered from highest to lowest weight; the analysis uses the same order, with ties retaining response order. These weights total 100%; omitted candidates have no associated card and no automatic related cards are added. The scale icon and percentage share a vertically centred line box; there is no weight tooltip (D200). This weight belongs to the Idea association, so the same thesis in the library has no weight badge. The analysis drawer explains each allocation and relevance; replay keeps the plan's weights fixed.

The Idea input contains its send-arrow button. It is grey and disabled when trimmed input is empty, black when text is ready, and disabled while submitting. Click and Enter use the same form submission. The input is at most 500px wide and fits narrower screens (D183). Initial data loading updates the library without changing the user’s current view.

Click the completed Idea card to open its analysis; Enter and Space do the same when the card is focused. There is no separate View analysis button. Dragging the canvas does not open the card. The preview uses the service's analyst summary, and the drawer shows it in full (D186).

While an Idea is loading, leave the right side of the header empty. Show a connected vertical list of actual progress stages inside the card. Retain completed nodes and glimmer only the current node; append a node when the next stage arrives. Respect reduced motion. The [D187 contract](../research/2026-10-26-library-ui/idea-progress.md) owns the events and lifecycle.

## Authority and contract

D130 owns the modular component boundary, D138 the Idea graph, D163 English presentation and D181 the current-library integration. Existing typography, source attribution, score tables, historical crosshair, drawer animation and card layout remain shared.

The closed schema is [`thesis-ui/2`](../../poc/ui/src/model/thesis.schema.json). `fromBundles` adapts HTTP/MCP/standalone exports into it; `parseDataset` validates, copies and freezes the result. Canonical v1 payloads upgrade at this boundary. Unknown legacy dates remain unknown. An invalid update leaves the displayed snapshot intact.

The [D181 design and review resolution](../research/2026-10-26-library-ui/plan.md) owns this slice's state/event, value/reader and path/check tables. The [frontend integration guide](../../poc/ui/README.md) describes its public entry points. The [service specification](service.md) owns read semantics.

## Ownership

| Module | Responsibility |
|---|---|
| `src/hivemind/bundle.py` | Pin read transactions and project current or historical ledger data; preserve identity, sources and relationship dates |
| `model/thesis.schema.json`, `contract.js` | Versioned allowed shapes, dates, IDs and references; legacy conversion |
| `adapters/bundle.js` | One conversion from bundle values into UI labels and explicit scores |
| `model/thesis.js`, `library.js` | Pure historical state, membership, dependency and filter selectors |
| `components/library.js` | Group navigation, local text/subject/status filters, snapshot date and card grid |
| `components/thesis-card.js`, `thesis-chart.js` | Shared card and history plots |
| `components/thesis-detail.js`, `evidence.js`, `relations.js` | Drawer, citations, complete source list, identity and separately labelled relationship kinds |
| `components/canvas.js` | Explicit graph layout, pan/zoom, replay; no thesis or group selection logic |
| `idea/composite.js` | Idea plan validation, weighted historical calculation, confidence conversion, display ordering and coverage; no inferred direction |
| `components/detail-tabs.js` | Shared tab selection, keyboard navigation and scroll reset; content remains owned by each drawer |
| `idea/analysis.js` | Overview, expanded reading steps and original Response data in a read-only drawer; search records appear only in Response |
| `bootstrap.js`, `idea/idea.js` | API requests and cancellation, complete snapshot replacement, explicit Idea submit |

Full-library reads declare `coverage: library`. Selected-thesis reads declare `coverage: selection`; their group memberships refer only to loaded theses. They never claim a full group population. Sources retain the source date and the date they entered the ledger. Historical citation rendering uses the selected judgement date, even when the drawer opened at a later date.

## Verification and budget

The current corpus and older Chinese/translated fixtures pass through the same adapter. Real HTTP/MCP reads exercise the default English ledger, and explicit old-ledger tests retain the existing service regressions. Temporary real ledgers cover waiting dependencies, resolution and succession because the current English corpus contains none of those records.

Browser checks cover filtering, date changes, citations, the history plot, score definitions, drawer motion, narrow-snapshot replacement and empty/invalid datasets. Source databases remain read-only. Results and input hashes are in [the D181 report](../../poc/reports/2026-10-26-library-ui/results.md).

The production JavaScript budget remains 200 KiB, and full-corpus validation remains below a 200 ms budget. Production output is minified; sources remain formatted ES modules. Ajv and esbuild are existing build dependencies; no new UI framework is introduced.
