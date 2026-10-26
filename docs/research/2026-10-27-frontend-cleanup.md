# Frontend cleanup

Scope: the current frontend only. Backend work, model prompts, data snapshots, public component APIs and user-facing behaviour are outside this cleanup.

## Census and mechanism

- The 276-line Action component owns both allocation editing and an independently interactive price chart. Move the existing chart markup, range selection and pointer/keyboard handling to one internal chart component. Keep all existing CSS classes, text and DOM order.
- Three price/date formatting functions construct a new Intl formatter on every call, including each pointer inspection. Keep the same locale/options in module-owned reusable formatters.
- The Action allocation and Trigger threshold each repeat percentage-wrapper, focus, input and browser-spinner rules. One shared style owns the identical declarations; component classes retain their different input widths. Their editing logic remains separate because Action commits on Enter while Trigger updates immediately.
- A full source/style class scan found no unused selectors after checking the static page shell. Public exports and legacy response support stay in place.

## State and event contract

| State/event | Preserved result |
| --- | --- |
| New Action | 5.0% and 1Y, current real snapshot and Monitoring dot |
| Allocation draft → Enter / Escape / outside pointer | Existing commit / cancel rules and one host write on commit |
| Price range click | Finish the allocation draft, notify host with selected range, then redraw |
| Price pointer / keyboard inspection | Same point, quote, change percentage and crosshair |
| Leave workspace / close | Cancel draft, close selectors, clear chart inspection |
| Range/replay replacement / destroy | Existing host settings retained; old listeners released |
| Missing price snapshot | Same unavailable display and editable controls |
| Trigger input / slider / scroll | Immediate threshold changes; existing current-value marker preserved |

## Values and readers

| Value | Owner and readers |
| --- | --- |
| Committed allocation / range | Host callback owns persistence; Action edits allocation; price chart requests range changes |
| Price geometry / inspected index | Price chart owns it; only its quote and SVG read it |
| Market snapshot | Existing closed parser; unchanged captured data |
| Percentage input appearance | Shared stylesheet; Action and Trigger retain their original classes and width settings |

## Checks and prior decisions

D237 requires transactional Action input and immediate unfocused wheel updates. D239 requires a pulsing black Monitoring dot with reduced-motion support. D240 requires 1Y by default. D225 retains navigation state. D230 keeps Trigger edges arrowless. These do not change.

Before editing, save a source/page snapshot and record built JS/CSS sizes. Compare complete Action DOM and computed percentage-control styles in a stored-response browser fixture before and after. Run existing Action, Trigger, navigation and reveal checks plus the full frontend suite, lint, formatting and mutation checks. Run the full Python suite once for the final repository check; no model calls or backend edits.

Self-review: keep range callbacks in the same order; clear chart hover on pause; abort chart listeners on teardown; preserve instance-local state; do not unify the two different percentage-editing behaviours. No behaviour choice or contract change is needed.

## Results

- All 20 before/after states match exactly: displayed text, SVG markup, chart keyboard inspection, Action/Trigger input styles and card positions.
- Action component: 276 → 127 lines. Its price-chart lifecycle is now independently owned in a 167-line internal component. No public exports were removed.
- Built JavaScript: 179,082 → 179,356 bytes; CSS: 41,309 → 40,748 bytes. Combined executable/style output falls by 287 bytes. The purpose is clearer ownership and removing duplicate styling, not a claimed large download reduction.
- 56 frontend tests, lint and formatting pass. All 20 existing scratch mutations are rejected. Full Python suite: 165 passed in 21.84 seconds.
- Action controls, Trigger controls and navigation-retention browser checks pass. A scratch version omitting the child chart's teardown fails specifically with “Destroyed price chart retained listeners”; the control passes.
- No dependency, model prompt, source data or backend module was changed by this cleanup.

## Reasoning refresh

The cleanup changes no research-universe, classification, Config, dispatch, extraction, thesis storage, final-verdict, pull-mode or review-pool behaviour. Their page/PRD examples and acceptance stay applicable. The frontend ownership table and integration notes now identify the internal price chart and shared percentage stylesheet. Existing UI decisions and defaults remain the governing behaviour.

The final reveal browser check passes its card order, line drawing, vertical camera scan and final centring. The actual app has been rebuilt and refreshed with its cached Idea, 5.0% allocation, 65% Trigger and 1Y chart retained.
