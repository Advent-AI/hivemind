# D181 reasoning refresh — October 26, 2026

The current library is now directly readable in the frontend. Example: Vera Rubin has six stored members on August 15 and one on February 25; selecting a date changes membership, evidence and assessments together. The UI does not create a parent thesis or change extraction.

The D22 review asks, in module order: whether this change affects the module, whether page and PRD agree, whether its examples still hold, and whether acceptance or open questions change. The following is the reasoning review, separate from `docs/check.py`.

| Module | Impact and page/PRD comparison | Example and acceptance result |
|---|---|---|
| 01 Research universe | No ingestion scope change. Subject filtering is a read operation over collected theses, not a new universe. | Company and macro-theme examples remain valid; no new subject or category is introduced. |
| 02 Classification | Source publisher, original speaker, source date and evidence tier remain separate. No classification rule changes. | A news report quoting an analyst keeps both identities; original source dates may be months or ranges. Existing classification acceptance is unchanged. |
| 03 Config | No model, prompt or search-count change. UI/API/MCP default ledger and item paths now agree; derived search storage is separate. | Explicit legacy paths still work. Read-only library calls need no model or semantic index. |
| 04 Dispatch | The frontend never dispatches an item. Historical visibility uses recorded sequence dates, not browser time. | Redelivery and resume examples are unaffected; no dispatch acceptance changes. |
| 05 Extraction | Association output is consumed as stored. Found and corrected three stale status surfaces: the related-decision summary and the page/PRD relation statement. D165 already integrated that output. | Rubin and customer projects retain separate questions in their stored group. Prompt quality and extraction acceptance are not re-evaluated here. |
| 06 Thesis library | Added a complete read projection of identity, sources, groups, replacement dates, resolutions and succession. Corrected the stale integration sentence in acceptance, without weakening semantic acceptance. | A later replacement does not rewrite an earlier judgement's evidence display. Group peers remain distinct from dependencies and other-period links. Empty relation kinds remain empty. |
| 07 Final verdict | No new verdict or result is computed. Existing recorded status and assessment are displayed. | Due-date freezing remains the existing contract; no new acceptance or decision. |
| 08 Pull mode | Date selection reads a snapshot; it does not run scheduled work, close theses or call a model. | The annual-results/closure example remains unchanged. |
| 09 Human review pool | No review workflow or new intake is added. Invalid UI envelopes are refused at the component boundary. | Existing classification and repeated-failure intake remains unchanged. |
| 00 System overview | Corrected the two stale integration-status statements to D165; the index's extraction/library rows now agree. Thesis, evidence, group and dependency retain the glossary's meanings. | The system still reads whole inputs, records associations during extraction and exposes stored results. No additional clustering pass or generated investment thesis. |

The UI specification previously described the first selected thesis as the graph parent. It now points to D138's explicit links and D181's separate library view. The service specification, README and component guide now describe the current English data paths, full-library read and `thesis-ui/2`. `CURRENT_STATE.md` retains existing extraction limitations and the acceleration task, replacing only stale frontend status. D181 records the authorized scope and measurements.

Generated extraction relations were rebuilt from `new-facts.js`, not hand-edited. Historical experiments and their original acceptance results are unchanged. The final mechanical check verifies generated blocks, the page bundle, terminology and the existing classification simulation; it is not a new extraction acceptance.

## D182 presentation follow-up

Module-order review: (1) universe, (2) classification, (3) Config, (4) dispatch and (5) extraction have no data or processing change; their page/PRD examples and acceptance remain intact. (6) The library supplies the same dated snapshot; only the library date picker and redundant display rows are removed. Card details and historical charts still read the supplied day. (7) Final verdict, (8) pull mode and (9) review pool have no changed input, output, trigger or acceptance. (10) The system glossary still distinguishes idea, thesis, group and dependency. The UI specification is the owner of sentence-case labels, bar metadata separators and the “Show more” label; AGENTS points to it. CURRENT_STATE and the component guide now describe snapshot dates rather than a date-filter control. The frozen pipeline contracts and data schema are unchanged.

D181's browser observations remain historical results. D182's new result records the deliberately removed controls, current lifecycle checks and retained filtering. The presentation cleanup plan contains the full state/event and reader walk.

## D183 input-control follow-up

In D22 order, universe, classification, Config, dispatch and extraction keep their contracts and examples. The library read returns the same fields but no longer navigates the page when its initial request settles; this preserves user input and in-flight Idea work. Final verdict, pull mode, review pool and the system glossary remain unaffected. UI ownership stays in the existing template, bootstrap and CSS. The UI specification and CURRENT_STATE now record the inline send states, Enter behaviour, 500px width and bar-separated statistics. The existing Idea model/search contract and semantic acceptance are unchanged; the cached browser replay verifies input submission only.

## D184 returned-analysis follow-up

In module order: universe, classification, Config, dispatch and extraction have unchanged inputs, outputs, examples and acceptance. The thesis library supplies existing immutable question titles to name candidates; grouping, judgement and temporal semantics do not change. Final verdict, pull mode and review-pool handling remain unchanged. The system glossary still separates user Idea, stored thesis and evidence. The Idea service document now names the full returned-analysis drawer and distinguishes it from a private reasoning stream; the component guide names its data/lifecycle owner. All content comes from the existing response and no analysis field is invented. CURRENT_STATE and D184 record the UI outcome; existing semantic-quality limits remain.

## D185 composite preview follow-up

In D22 module order, universe, classification, Config, dispatch and extraction have unchanged processing inputs and outputs. The library's stored states and identities are read at their historical date; no state is rewritten. Final verdict, pull mode and review-pool rules remain unchanged. The system's thesis/group vocabulary is unchanged: the trial basket is UI calculation input, not a new thesis or research group. The Idea service keeps its two calls and response; only an explicit optional UI build input enables the reviewed basket. The UI/Idea documents and current state now distinguish retrospective current-basket history from a persistent historical Idea judgement. Examples and original acceptance remain valid; D185's calculation checks do not claim model-quality acceptance.
