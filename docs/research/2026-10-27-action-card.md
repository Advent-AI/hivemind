# Action preview and NVIDIA chart

Alex requested an Action card to the left of the Trigger: Buy [Spot] [Market Order] on [Hyperliquid], Invest [5.0%] of [0xas83....9832] wallet, with real NVIDIA prices underneath. This slice changes only the frontend and its portable build. Claude's backend, ingestion, matching, model calls, wallets and execution are outside its scope.

## Contract before code

D237 edit contract (supersedes immediate typed allocation updates):

| State | Event | Result |
| --- | --- | --- |
| Displayed committed value | Focus / type / arrow key | Local draft in the input; host settings unchanged |
| Draft | Enter with a finite number | Clamp to 0–100, round to one decimal, write host settings once, end editing |
| Draft | Empty Enter / Escape / blur / workspace pause | Discard draft, restore the committed percentage, end editing |
| Draft | Wheel | Adjust the draft by 0.1; no host write |
| Not editing | Wheel | Adjust committed percentage by 0.1, as before |
| Any | Chart range changes | Cancel any unfinished input through blur; retain committed percentage |

The allocation writer is the Enter/unfocused-wheel handler; the host callback and range redraw read only committed settings. Native input owns draft text, including temporarily empty input. All focus paths use blur for cancellation; replacement destroys the draft without sending it. The removed footer has one writer and one CSS rule. Source/currency/time move to the SVG's accessible description. D235's plan-only authority and captured stock data stay unchanged; D236's header stays without a badge. This presentation edit affects no frozen backend module.

Authority: a read-only price display and editable plan. No submit action, wallet connection, balance request, signer or execution endpoint. The supplied wallet string is an example label. Venue controls have the requested single options; they do not assert that Hyperliquid lists NVIDIA spot. The chart keeps its actual NVDA stock / USD source in its accessible description; D237 sets the visible Action pair and venue label.

| State | Event | Result and writes |
| --- | --- | --- |
| Empty / pending / failed Idea | Render | No Action or Trigger |
| Completed Idea | First reveal | Idea, theses from top down, overview, Trigger, then Action; plain links touching Trigger |
| Completed Idea | Edit investment or chart range | Local settings only; 0–100% in 0.1 steps; one of 1D/1W/1M/1Y |
| Completed Idea | Replay / date / canvas range | Preserve Action settings; chart remains dated market data, independent of retrospective thesis date |
| Completed Idea | Leave / return to tab | Preserve settings and camera; close menus, stop animations |
| Any render | New query / replacement / teardown | Reset new-query settings to 5.0% and 1Y (D240); remove old controls/listeners; cancel old animation |
| Price snapshot missing / malformed | Render | Show price unavailable; do not substitute invented points or break the Idea |
| Reveal in flight | Input / resize / reduced motion | Existing cancellation settles all cards, including Action |

| Value / source | Writer | Readers |
| --- | --- | --- |
| Market snapshot | Explicit dated build input from TrueNorth historical_bars | Closed frontend parser, Action chart; no thesis calculation |
| Investment / chart range | Action controls through host callback | Action display; retained per-query state on redraw |
| Action position | Graph layout | Card placement, connectors, reveal, bounds / camera |
| Plan fields | Single-option frontend selectors | Text display only |

| New path | Existing checks retained |
| --- | --- |
| Completed graph with Action | Valid thesis identities / topology; shared card style; no overlap; navigation retention; cancellation / teardown |
| Wider tree | Centre occupied width; cap zoom at 100%, fit width only when necessary; never shrink to fit tall thesis column; manual fit unchanged |
| Chart ranges | Use last observed time, not machine date; ordered finite positive USD closes; completed bars only; actual timestamp/source in the chart description |
| User controls | Shared select keyboard and outside-close lifecycle; investment scroll does not pan canvas; no service request |

Prior decisions: D222 centred the whole occupied width at 100%; D227 scans downward; D229 shows Trigger after the theses; D230 removes directional arrows from Trigger connections; D225 retains the current query on navigation. The additional column requires width-only reduction when the full row exceeds the canvas. No change to vertical fitting or thesis order. Action follows Trigger at the end of the reveal.

Self-review: the market dates are later than the thesis ledger's August date, so the chart retains its own as-of date in its accessible description and never follows replay. The example wallet is not a real address and grants no authority. Snapshot failure is isolated from existing library rendering. Both connections touching Trigger remain plain. The new column participates in camera bounds and animation cancellation. No open contract choice remains.

## Data evidence

TrueNorth CLI `historical_bars`, NVDA, asset_class stock, instrument_type spot. Daily response: 371 bars; hourly response: 248 bars over 2026-09-26 to 2026-10-26. Last completed hourly close is $215.3794 at 2026-10-26T15:59:59.999Z. The tool dropped the incomplete future bar. Raw responses and normalized snapshot are retained under dated paths. This is a captured price history, not a streaming quote.

## Verification

The completed implementation passes 56 frontend tests, including the real 619-observation snapshot, range/date/geometry checks and malformed data. All 20 scratch mutations are rejected. Lint, formatting and the full 165-test Python suite pass. The production script is 178,609 bytes, below the 200 KiB budget; prices are embedded separately as data.

Browser checks pass the Action's fields, logo, layout, four distinct ranges, allocation scroll, replay/navigation retention, new-query reset, unavailable prices and teardown. The existing Trigger checks pass. The reveal visits Idea → three theses → Trigger → Action, with partial drawing frames, a vertical scan and a horizontally balanced final view. Cancellation settles the entire graph.

The user's previous China/geopolitics query was restored from the real API's existing cache. A read-only preflight refused any model/embedding request and succeeded; the archive remains at 27 rows. Its 65% Trigger setting is retained. No paid model calls, source ledger edits, backend changes, signer operations or order calls were made by this slice.

Document reasoning refresh: the new market display does not write research inputs, configuration, sequences, extracted theses, matching records, final verdicts, pull events or review-pool items. In module order (universe, classification, Config, dispatch, extraction, thesis library, final verdict, pull mode, review pool, system), the first nine keep their page/PRD behaviour, examples and acceptance criteria. The system glossary gains Action card. Frontend inconsistencies corrected: the default camera description now admits width-only reduction; reveal order now ends with Trigger then Action; the new component/data owner and separate market timestamp are recorded. Frozen module semantics remain unchanged.

Final browser correction: focusing the new SVG chart produced 70.5px of native scrolling inside the canvas's `overflow: hidden` container, moving the replay controls off the top even though camera state was unchanged. The canvas is positioned by its camera, so its clipping container now uses `overflow: clip`, which does not create a native scroll container. The browser check focuses the real chart and asserts zero scroll and a fixed replay-toolbar position. This removes the mechanism for every focusable child of the canvas without intercepting focus or adding scroll handlers.

D237/D238 verification: all 56 frontend tests and lint/format checks pass. The real-browser Action checks pass typed Enter commit, Escape cancellation, blur cancellation, empty input, draft wheel cancellation, immediate unfocused wheel, navigation/range retention, removed labels/footer and Monitoring icon. A scratch build that made Escape commit failed specifically with “Escape did not cancel the allocation draft”; the unchanged control passed. The source data and backend are unchanged. Bundle size: 179,200 bytes.

The outside-click path is checked separately from focus loss: canvas panning prevents the browser’s normal focus change on blank space, so a capture-phase pointer listener cancels the active allocation draft before that handler runs. It uses the component’s existing AbortController and is removed on teardown. The browser check dispatches a pointer event on nonfocusable canvas text and also verifies a real click restores the saved value.

D239 changes only the Monitoring indicator: a six-pixel black dot with a gentle scale/halo pulse replaces the robot. The reduced-motion style leaves a still dot. The old icon and SVG-specific status rule were removed; the Action controls and data paths are unchanged.
