# D182: frontend presentation cleanup

Alex asked to remove four illustrated elements: the connection status and Refresh area, the Research library eyebrow, the As of date control, and the repeated count/date row above the cards. He also required sentence-case interface labels and vertical bars between metadata fields throughout the frontend.

## Census and mechanism

The current component templates contain three all-capital navigation/eyebrow labels and six middle-dot metadata templates: three connection states, the results row, card subject/year, and dependency direction. The first four dot templates disappear with the requested removals; the other two use the existing shared bar separator. Current CSS contains no uppercase text transform. Stored source quotations, company names, tickers and ordinary acronyms are data, not interface capitalisation. Chart markers remain chart data, not metadata punctuation.

## State × event

| State / event | Result |
|---|---|
| Initial saved data | Render the library with no connection banner, date control, eyebrow or repeated result row |
| Automatic library read succeeds | Validate and replace the snapshot through the existing component boundary |
| Automatic read fails or page is closed | Keep the saved snapshot; abort the read on page close; no removed DOM reference is accessed |
| Search / group / status changes | Update cards and existing sidebar/stat counts; no result-row dependency |
| New dated snapshot | Preserve existing date clamp and historical detail behaviour; the caller supplies the snapshot |
| Library / Idea switch | Existing explicit Idea submission and component teardown remain |

## Value × reader

| Value / writer | Readers and effect |
|---|---|
| Embedded/API snapshot | Library, Idea and detail components; data shape unchanged |
| Interface labels | Sidebar renders Workspace and Research groups; no uppercase CSS |
| Subject/year and dependency direction | Card/relationship templates use shared `SEP` |
| Removed controls | Bootstrap, library, CSS and browser lifecycle fixture lose references together |

## New path × old checks

| Changed path | Verification |
|---|---|
| Automatic load without status/button | Open real page with API unavailable; cards render and Library/Idea navigation works |
| Card metadata | Real-page DOM uses NVDA | FY2027; no UI middle dots |
| Library filtering without result row | Existing invalid/empty/replacement lifecycle fixture uses sidebar count, not removed output |
| Sentence case | Inspect current component/template literals and rendered sidebar; keep source text and identifiers unchanged |

D130 owns shared components; D138 owns Idea links; D181 owns current-library reads. D182 changes presentation only. The rule lives in the Thesis UI document, with an AGENTS pointer. Verify the UI suite, existing mutations, lint, format and real browser. Refresh module reasoning for presentation impact and run docs/check.py last. No model calls or database changes are required.

Alex also requested “Show more” for the pagination action. Census found two corresponding labels: library theses and detail evidence. Both use “Show more”.
