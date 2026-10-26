# Frontend cleanup · D218

The scope is the existing frontend and its portable page. Keep the current product behaviour, API formats, confidence arithmetic and historical compatibility. Do not refactor ingestion, model calls or backend concurrency. Alex requested committing and pushing this work.

## Census and mechanism

- Two drawers independently implement tab clicks, arrow/Home/End navigation, selected state, panel visibility and scroll reset. They can share that interaction without sharing their content or lazy loading.
- Three internal exports have no callers: `scoreTable`, `formatCompositeScore`, `formatConfidenceEffect`. None is part of the package entry point.
- Old Idea slider, card footer, dependency-chip, example-button and analysis metadata selectors have no markup producer in source, the page template or verification pages. Inspect exact class names, including dynamic producers, before removing them.
- Canvas position rules are overridden later in the same stylesheet. Retain their final values at the original declaration.
- The analysis renderer has large nested templates; name the repeated thesis and reading-step renderers without changing their output.

Baseline: 47 frontend tests, lint and formatting pass; build is 159,137 JavaScript bytes and 34,689 CSS bytes. Save baseline rendered sections and compare them exactly after cleanup. Keep a local source/page snapshot before editing.

## State × event

| State/event | Required result |
|---|---|
| Closed drawer → open/reopen | Overview selected; original focus and animation behaviour |
| Any tab → click another | Cancel disclosures; select one tab/panel; reset content scroll |
| Any tab → arrows/Home/End | Same tab selection plus focus on the selected tab; wrap at ends |
| Thesis tab → Evidence/History first visit | Existing lazy rendering and chart/filter setup |
| Thesis citation → Evidence | Programmatic selection still opens the correct source |
| Drawer → close/destroy | Existing focus restoration; remove tab handlers on destroy |
| Two drawers/instances | No shared active tab or IDs |

## Value × reader and old checks

| Value | Owner/readers | Verification |
|---|---|---|
| Selected tab, tabindex, hidden panel | Shared tab controller; both drawers | Actual browser click/keyboard/reopen/lazy-tab checks |
| Analysis HTML, summary, reasons, response JSON | Existing analysis helpers | Exact stored-fixture output comparison; existing 47 tests |
| Card/plot geometry and visual style | Shared styles; library and canvas | Before/after screenshot and dimensions |
| Confidence/history/weights | Existing composite module; graph and drawer | Existing calculation/replay tests; cached actual response |
| Public exports/legacy formats | Package entry point and adapters | No removals from package exports; full suite and mutation checks |

## Prior decisions and review

D130 owns reusable components and instance isolation. D181 preserves dated library and source semantics. D197–D217 define current confidence, weight, spacing and detail layout. D214 requires keyboard tabs and reopening on Overview. D217 removes Search trace only from the UI. No decision or accepted format is being retired.

Read-only self-review of these rows: tab code must not absorb content rendering, dropdown handling, motion or focus trapping. Keep those drawer-specific callbacks. Dead-code removal must not remove legacy composite validation or exported package APIs. No serious design issue remains with that boundary.

## Verification results

- 47 frontend tests pass, with lint and formatting clean. All 13 existing scratch-copy mutation checks reject their defects.
- Five stored responses produce byte-identical Overview, Trace and Response markup: 15 sections checked, including older response formats.
- The actual cached NVIDIA Idea still shows 61%, weights 55% / 25% / 20%, four 440px cards and three 1.5px grey connectors. The first and last replay dates show 50% and 61%.
- Idea and Thesis tab clicks, arrow wrapping, Home/End, focus, reopen reset, citation-to-Evidence navigation and first-use History rendering work in the browser. Library search, clearing and Show more produce 24 → 0 → 24 → 48 cards.
- The six measured Idea detail sections have identical text and geometry. Before/after screenshots are pixel-identical.
- The full local Python suite passes: 165 tests. The portable build validates all 90 theses in 28.9ms. Its script is 158,927 bytes (previously 159,137); CSS is 33,206 bytes (previously 34,689). No dependency was added.
- All three protected database hashes are unchanged. The running Idea archive still contains nine calls; browser verification reused the cached response.

## Reasoning refresh

Reviewed the affected frontend contract against D130, D181 and D197–D217, then checked the module order in the PRD index. Universe, classification, Config, dispatch, extraction, stored thesis identity, final verdict, pull mode and human-review intake are unchanged by this cleanup. The system's confidence definition is unchanged. No page/PRD data needs regeneration for a new behaviour.

Two stale frontend descriptions were corrected: the README still described a removed confidence-help tooltip, and the component ownership table still described Search trace as a visible section. Both now describe the final Theses / Trace / Response arrangement. The current-state paragraph now describes the final interface instead of replaying each superseded layout revision.

## Push snapshot

The staged snapshot excludes unrelated extraction and concurrency changes. It independently passes 47 frontend tests, lint/format, 13 mutation checks and all 128 Python tests present in that snapshot. The larger working directory passes 165 Python tests. Raw experiment databases, archived model responses and process logs remain local.
