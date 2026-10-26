# Idea weight presentation and connectors — D198/D199

The final weight pill contains a scale icon and percentage only. Hovering the icon or focusing it from the keyboard shows “Weight factor”. The visible word “Weight” was removed following Alex's final clarification.

The graph, contribution rows and weight explanations use descending impact weight. The actual stored response previously displayed 55 / 20 / 25; it now displays 55 / 25 / 20. Equal weights retain response order. Sorting copies does not mutate the response or score input. The same response still produces 61.25% Idea confidence, rounded to 61% on the card.

Default connector strokes changed from 1px / #c9c7c0 to 1.5px / #aaa99f. Arrowheads use the same new colour. Routing, card attachment points and active highlighting are unchanged.

Validation:

- The actual three-thesis response passes graph-order, analysis-order, unchanged-response and confidence assertions. A no-sort mutant fails the order assertion. A raw-score mutant fails the confidence assertion.
- Actual browser cards show 55 / 25 / 20; Full, Last 30 days and replay retain that order. Keyboard focus reveals the same CSS tooltip used by hover. Final screenshot: [UI](final.png).
- 46 UI tests, lint and formatting pass. The repository's product suite (`pytest -q tests`) passes 165 tests. An initial unqualified pytest invocation also collected five archived scratch mutation modules with removed imports; the product test directory was then used. No archived report or test file was changed.
- No model or embedding calls. The active model archive remains at nine rows. All three protected source database hashes match their baseline.
- Standalone build command: `python scripts/mock_build.py`. Final output: 158,678 JavaScript bytes; 90 theses validated in 24.9ms. Both stay below the existing 200 KiB and 200ms budgets. Browser inspection confirms all three default edges are 1.5px with rgb(170, 169, 159), matching the arrowhead.

Reasoning refresh: universe → classification → Config → dispatch → extraction → library → final verdict → pull mode → human review → overview. No pipeline inputs, writes, dates, identity rules or examples change. Current-state and UI text were refreshed for the final icon-only pill, confidence scale, descending order and connector style; historical decisions retain their original wording. `docs/check.py` is the final mechanical check.

## Latest presentation correction — D200/D201

Removed the weight tooltip and its keyboard focus target. Icon and percentage now use explicit centred line boxes. All three actual cards have equal icon/number vertical centres and no tooltip node. The stored three-thesis layout and live DOM both measure a 180px horizontal gap, increased from 120px; weight order remains 55 / 25 / 20.

46 UI tests, lint and formatting pass. Route checks cover 94 fan-out sizes and the stored multi-column graph. Final build: 158,612 JavaScript bytes, 90 theses validated in 25.0ms. No model configuration, calculation or database changes.

Reasoning refresh: only shared card presentation and column spacing change. Upstream scope, classification, Config, dispatch, extraction, library, final verdict, pull mode, human review and system semantics retain their existing inputs, writes and dates. UI/Idea descriptions and current state now reflect removal of the tooltip; D198 remains historical.

[Updated spacing and alignment](alignment-spacing.png).

## Chart text and compact Idea height — D202

The Idea SVG previously squeezed a 406-unit viewBox into 326px of card content. It now draws at the actual content width passed by the canvas, matching the Thesis chart’s native scale: subtitle 11px and vertical-axis labels 10px. One shared CSS rule owns the subtitle style.

The completed Idea card fits its content and remains centred within the graph’s reserved block. On the actual response, its height is 368px and bottom space is 17px including the border, compared with 380px and about 60px before. Full, Last 30 days and Home/End replay preserve the new sizing. Initial and replay renderers receive the card width. Pending/error cards keep their existing layout.

46 UI tests, lint/format and the standalone build pass. The build is 158,891 JavaScript bytes and validates 90 theses in 26.9ms. No model, score, weights, dates or database changes. The PRD sequence was reconsidered: all pipeline module inputs, writes, examples and acceptance remain unchanged; only UI presentation, its Idea contract and current state were refreshed.

[Verified final typography and spacing](chart-type-spacing.png).

## Idea detail header and explanation hierarchy — D203/D204

The detail title is followed by an AI confidence pill and the current UI submission's creation date. The previous bare date was the library cutoff; it is no longer labelled as creation. The date is captured once at submit, in browser-local calendar days, and stays fixed during score replay. Legacy callers without it show Not recorded. This is UI session metadata, without a new backend record.

The redundant confidence / driver-count / date row is removed. All three adopted-thesis explanations show one full question with the shared scale/weight pill, then Relevance and Weight rationale with consistent body typography. Their returned text and descending 55 / 25 / 20 order remain intact. The duplicate short headings and current-format fixed-weight footer are gone.

Validation: 46 UI tests, lint/format, and actual response rendering pass. The header shows 61% and Oct 26, 2026; a replay check shows 50% with the same creation date. Missing confidence/date render explicitly unavailable. Final build: 159,337 JavaScript bytes; 90 theses validated in 26.2ms. No model prompt, source database, score or association change.

The reasoning refresh leaves all pipeline module boundaries and examples unchanged. The Idea/UI specifications, frontend integration guide and current state were refreshed together; historical verification snapshots retain their original measurements.

[Header](idea-header-final.png) · [Structured thesis explanations](explanations-final.png).

## Contextual confidence help — D205

Removed the numerical contribution table and the always-visible method paragraph. A question-mark button beside the analysis subtitle now displays that same paragraph on hover or keyboard focus. The adopted thesis explanations and weight pills remain in their existing order.

The actual browser reports zero tables in the Idea drawer, a hovered help control, and the exact requested text in its visible popup. The popup stays within the detail content width. The actual cached response still has three adopted theses and a 0.45 aggregate (61% displayed confidence). Updated the retired table assertions to check the calculation independently and the new weight/help presentation. 46 UI tests, lint/format and build pass. Final JavaScript: 159,172 bytes; 90-thesis validation: 25.6ms.

Reasoning refresh: no pipeline input, stored value, date, calculation or example changes. The Idea/UI contract and current state now describe the removed table and contextual help; historical tables remain in prior reports. No new model calls or source database changes.

[Normal view](confidence-help-closed.png) · [Visible help popup](confidence-help-open.png).

## Explanation labels and right-hand help — D206

All three thesis explanation dividers are removed. Relevance and Weight rationale now use black, semibold 14px text, matching the 14px body. The help popup opens eight pixels to the right of the question icon, top-aligned with it; its width is limited by the remaining heading row.

Verified all six labels against their body text in the actual browser: 14px / 14px, weight 600, colour rgb(15, 20, 13); all three divider widths are zero. The open popup is 340px wide and starts eight pixels to the icon's right. The 46-test UI suite, lint and formatting pass. Build: 159,172 JavaScript bytes; 90 theses validated in 25.3ms. No data, score or model changes.

The reasoning refresh preserves every pipeline module's inputs, examples and acceptance; only the Idea presentation contract and current state changed. [Final popup and labels](right-popup.png).

## Correct divider scope, spacing and help alignment — D207/D208

Corrected the over-broad divider removal: the first thesis has no leading divider; subsequent theses and main analysis sections have the shared 1px rule. Removed stacked spacing: metadata-to-Summary drops from 52px to 24px, confidence-heading-to-first-thesis from 56px to 20px.

The popup uses balanced wrapping at up to 440px on the current desktop layout. Browser measurement confirms the complete explanation occupies three lines, with no truncation, and the question SVG and heading have identical vertical centres. All three thesis divider widths are 0 / 1 / 1px; main section dividers are also 0 / 1 / 1px. Labels and right-hand popup placement remain intact.

46 UI tests, lint/format and standalone build pass. The final build is 159,172 JavaScript bytes; 90 theses validate in 24.6ms. The reasoning refresh leaves pipeline data, clocks, scores and examples unchanged; Idea presentation and current-state documentation reflect the corrected scope.

[Section spacing](section-spacing.png) · [Three-line popup](balanced-popup.png).

## Weight-first headings and compact reading steps — D209/D210

Weight tags now precede all three thesis titles, with an 8px gap. The reading trace is a list of closed-by-default topic disclosures, using the existing Thesis detail disclosure component. Each summary shows its numbered topic and subject/period; expansion reveals the unchanged explanation and direct/related thesis lists with consistent body typography.

The actual browser confirms three closed steps, complete text after expanding the first, and successful closing. All three weight badges precede their title at an 8px gap. The 46 UI tests, lint/format and standalone build pass. Final JavaScript: 159,354 bytes; 90-thesis validation: 25.5ms.

The reasoning refresh changes no pipeline data or source dates. Idea documentation and current state now describe expandable reading steps. No new model calls or database writes are introduced.

[Compact reading steps](reading-steps.png) · [Expanded step and weight-first heading](reading-step-open.png).

## Title-height weight badges and optical icon alignment — D211

The three detail weight badges now measure 56×44px, matching each 44px title height, with 4px corners. Canvas badges remain unchanged. The confidence help glyph is 16px and raised 1px to align optically with the subtitle text rather than merely centring its line box.

Verified the three badge/title pairs and help transform in the live drawer. The 46 UI tests, lint/format and standalone build pass. Build: 159,354 JavaScript bytes; 90-thesis validation: 30.0ms. No source data or model changes. Reasoning refresh: pipeline modules retain all inputs, writes and examples; only detail presentation and its documentation changed.

[Updated detail view](tall-weight-tags.png).

## Theses title and equal card widths — D212/D213

The adopted-thesis section is now titled Theses, with its question mark and popup removed. The header confidence pill remains at 61%. Idea and Thesis cards now share one 440px width constant, preserving the 180px column gap. The Idea chart uses the matching 406-unit content width and retains content-fit height.

Actual browser measurements: all four cards are 440px wide, the gap is 180px, and the Idea chart viewBox is 0 0 406 158. The detail heading reads Theses with zero help controls. The 46 UI tests, lint/format and build pass; JavaScript is 158,520 bytes and the 90-thesis validation takes 30.2ms.

The reasoning refresh preserves all pipeline module inputs, dates, stored values and examples. UI/Idea descriptions and current state were refreshed; historical popup instructions remain in their original decisions. No model or source-data changes.

[Equal-width cards](equal-width-cards.png) · [Theses heading](theses-title.png).

## Overview, Trace and Response navigation — D214

The Idea drawer now uses the Thesis-style tab strip. Overview contains only the summary and adopted theses. Trace contains reading steps, search requests/results and excluded choices. Response shows the existing formatted JSON directly. Searches are grouped into expandable rows with query text, optional canonical query, result count and named candidate rows with stable IDs.

Opening a drawer defaults to Overview. Click and arrow/Home/End navigation switch the single visible panel, reset its scroll and retain the same response. Keyboard focus remains within the drawer. Switching tabs makes no API or model requests.

Validation: 47 UI tests pass, including panel-content separation and retained source data; lint/format and build pass. Actual browser checks cover all three panels, arrow and End navigation, reopening to Overview, focus returning to Close after the Response tab, and the initial search with all ten candidates. Source baseline hashes and nine archive rows remain unchanged. Build: 160,281 JavaScript bytes; 90 theses validated in 28.5ms.

The reasoning refresh changes only frontend navigation/readability; pipeline inputs, writes, scores, dates and examples remain unchanged. Idea/UI specifications and current state were refreshed together.

[Overview](tabs-overview.png) · [Trace](tabs-trace.png) · [Expanded search](trace-search-expanded.png) · [Response](tabs-response.png).

## Search titles without count or mode — D215

Removed the candidate-count and retrieval-mode subtitle from all four search rows. Expanded queries/results and the raw Response data remain unchanged. Browser verification finds four search disclosures and zero subtitle nodes. The 47 UI tests, lint/format and build pass; JavaScript is 160,159 bytes and validation of 90 theses takes 29.3ms. The Idea contract and current state were refreshed; no pipeline or source data change.

[Title-only search rows](search-titles-only.png).

## Reading steps open by default — D216

All reading steps now start expanded. Secondary search details are grouped under one collapsed Search trace disclosure below them; the original queries and results remain available. The actual browser confirms all three reading steps open and the outer search group closed.

The 47 UI tests, lint/format and build pass. Build: 160,216 JavaScript bytes; 90-thesis validation: 29.5ms. The reasoning refresh updates only the presentation defaults in the Idea contract/current state; no pipeline data or model changes.

[Default expanded reading steps](reading-default-open.png).

## Remove Search trace from the interface — D217

Removed the Search trace group, its per-search renderers and unused styles. Reading steps remain expanded by default. Original search fields are preserved in Response. The actual Trace tab contains zero search groups/rows and all three reading steps are open.

The removed search list had supplied the old fixture's only missing-bundle label. The same assertion now uses the existing typed-reading fixture so it still tests missing matched theses, rather than the retired search UI. All 47 UI tests, lint/format and build pass. Final JavaScript: 159,137 bytes; 90-thesis validation: 28.6ms.

Reasoning refresh: the Idea contract/current state now say Search trace is absent from Trace. No backend input, stored record, score or source date changes. [Final Trace without Search trace](trace-no-search.png).
