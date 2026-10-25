# English conversion (D163)

The maintained product will speak English: model instructions and new generated prose, public schema values, UI labels, current specifications, and operator instructions. A source quote stays in the source's language. Existing identifiers and archived content are not translated in place.

Example: new evidence uses `tier: "fact"`; a saved record with `tier: "发生的事"` still reads as the same fact. A quoted Chinese sentence remains exact. Converting its summary to English does not authorize rewriting that quote, changing its ID, or changing a financial value.

## Scope and unchanged behavior

This is a language change. D162 is finished and failed; its two-step experiment is not promoted. Do not fix event identity, admission, grouping semantics, or judgement policy as part of translation. No paid model run is authorized by this implementation plan. Existing tests and stored-answer replay establish code compatibility, not English extraction quality.

Included: `src/hivemind` active prompts and request builders; maintained CLI defaults and output; service/bundle vocabulary; current UI; README; current design page data and its PRDs; current POC specifications and experience documents. Historic prompt versions, completed research plans/results, previous decision entries, archive snapshots, source corpora, recorded model outputs, raw quotations and representative legacy fixtures retain their language. A remaining Chinese string must be classified as a source/legacy input, not silently overlooked.

The inventory uses file paths and exact Python string literals (`census.json`). The known positive control is extraction's four evidence-tier literals; the known legacy-data control is the recorded D162 $30 billion quotation. Generated PRD blocks are changed only through their owning page data, then regenerated with the existing block renderer. The language checker must keep checking real content after the glossary switches to English.

## Canonical vocabulary

Use one English value per existing meaning. No new state or relation is introduced.

| Domain | English values | Legacy values accepted when reading existing data |
|---|---|---|
| Thesis kind | `asset`, `theme` | `对象观点`, `主题观点` |
| Evidence tier | `fact`, `party_statement`, `third_party_view`, `rumour` | `发生的事`, `当事人说的`, `第三方看法`, `传闻` |
| Candidate decision | `merge`, `succession`, `new`, `skip` | `归入已有的`, `接续`, `新观点`, `不开` |
| Evidence decision | `repeat`, `replace`, `new` | `重复`, `替代`, `新证据` |
| Evidence push | `toward_first`, `toward_last`, `none` | `推向第一格`, `推向最后一格`, `不推` |
| Dependency direction | `first_is_bullish`, `last_is_bullish`, `same`, `opposite` | `对方第一格是看多`, `对方最后一格是看多`, `同向`, `反向` |
| Standard rung labels | Strongly bullish, Bullish, Neutral, Bearish, Strongly bearish, Yes, No | Exact existing standard labels; free result labels remain source prose |

One vocabulary module owns exact legacy-to-English conversion for named fields. It does not replace substrings in prose. New schemas enumerate English values. Existing prompt versions retain their old response vocabulary; version-aware model boundaries convert those answers before current code reads them. Storage readers normalize known legacy enum fields without updating rows; new writers store canonical values. Raw call archives remain unmodified. Text search and numeric parsers continue accepting Chinese source/legacy text as well as English.

## State × event

| State | Event | Transition, reads and writes |
|---|---|---|
| Empty/new database | New English input result | Existing dispatch sequence and publication day; canonical enum values and English generated prose; quotes unchanged |
| Existing Chinese database | Read/list/render/search | Normalize known enum fields in memory; retain record IDs, dates, source strings, search content and historical values |
| Existing Chinese database | Append a new English result | Not the selected build path. Alex selected a fresh English library; keep historical ledgers unchanged and readable. |
| Old configured prompt | Fresh call or cached historical response | Its response schema uses its registered legacy vocabulary; normalize at the consumer boundary; archive exact original response |
| New configured prompt | Fresh call | English-only enum schema; English request instructions; original source language permitted in quotes and source names |
| Unfinished old handover | Resume | Normalize its saved enum fields before existing checks; preserve sequence and progress rules; no data rewrite |
| Any input | Unknown enum | Existing schema/contract refusal, not guessed translation; no new automatic retry |
| Any run | Missing credential/network failure/crash | Existing behavior unchanged; language conversion adds no external service or background job |
| Any state | Multiple writers/config changes | Existing transaction and version rules remain; no migration overwrites a database |

## Value × writer × reader

| Value | Writers/input sources | Readers and required compatibility |
|---|---|---|
| kind/tier/rung labels | New/old model answers, legacy handovers, storage helpers, real fixtures | Extraction checks, matching, identity, writing, store queries, service, UI adapter, report/preflight scripts |
| matching outcome/direction | Model answers, saved matching records, tests | Matching checks, batch identity, writing, round/resume, historical diagnostics |
| push | Judgement answer and saved judgement JSON | Judgement checks, service/bundles, UI/report code |
| Generated prose | Versioned extraction/matching/judgement/idea prompts and dynamic request builders | Model, archive, ledger, API, UI; instruction is English, quotes retain original text |
| Known financial quantities | Existing structured bounds or legacy/free text | Matching orientation and service band parsing; English money forms must not collapse magnitudes; Chinese remains readable |
| Page/PRD prose | Current page-data constants; hand-authored PRD sections | Generated block comparison, bundle builder, renderer, glossary checks |
| Historical text | Frozen artifacts and original inputs | Read-only evidence; not a translation target |
| `year` / `wait_year` | Extraction answers, stored theses, matching dependencies | Fiscal-bound correction and waiting-dependency resolution must preserve the distinction between fiscal, calendar and multi-year periods; never infer identity from the first four digits |
| Numeric bounds / score orientation | Extraction rungs, storage, service/bundle builders | Preserve bounds through the bundle; both English-only and legacy ladders must give the same score for the same outcome |

## New path × old checks

| Changed path | Required proof |
|---|---|
| Canonical English enums | Complete mapping covers each old allowed value; new schemas reject unknown values; no prose replacement |
| Legacy reads | Stored answers and a real temporary legacy SQLite database preserve destinations, membership, quotes, dates and counts |
| New writes and resume | English outcome through extraction→matching→writing; saved old handover resumes through the same path |
| Request language | All active request builders use English; new schemas have no Chinese enum values; source text remains exact |
| Monetary text | English and legacy expressions describe equal bands and matching orientation; structured bounds remain authoritative |
| UI/API | Both old bundles and new canonical values render the same tier/kind and score; current component tests and build/lint |
| Documentation | Page owns generated blocks; English glossary has positive and negative controls; all current page nodes and links render |
| Experiment regression | D162 original records stay untouched; translation does not turn its failures into passes |
| Subannual wording | English and Chinese descriptions of the same half-year revenue question must have the same admission result; translating text must not bypass the existing filter |

## Review findings and selected library path

The first read-only review found four serious missing dimensions, recorded in `review.txt`. The search, score, year and subannual cases are implementation prerequisites, not findings to dismiss as translation details.

1. **Search across languages.** The current matching path uses literal-word retrieval, then truncates the candidates. The review reports four targets lost after translating stored queries, even after including existing context. Alex selected a fresh English library on October 25. Re-extract original sources into an empty, separately named ledger; do not translate old rows into it or append English extraction to the Chinese ledger. Cross-language ingestion is outside this build. Historical reads remain supported. The [library build plan](english-library.md) identifies the source population and launch prerequisites.
2. **Score orientation.** The review reports 12 of 18 five-rung themes reverse when `condition_zh` is removed. Verify on the stored bundles, retain structured bounds through the bundle, and test English-only legacy text where bounds are absent. Do not use language or rung position as a bullishness assumption.
3. **Period text.** Define a full-match parser for accepted English and legacy single-year forms. Use the same period interpretation when correcting fiscal bounds and resolving `wait_year`; preserve multi-year and unknown original ranges. The accepted set and rejection controls must be written before code.
4. **Half-year text.** Compare English/legacy pairs through the actual extraction check. Preserve the current admission boundary, including the distinction between a revenue period and an event scheduled in a half-year. Do not broaden the filter to all mentions of H1/H2.

## Prompt review: meaning, structure and terminology

Alex explicitly requested an extra prompt check: clear writing and structure, correspondence with PRD definitions, and no terminology drift. The glossary in `docs/prd/00-system.md` remains the vocabulary owner. `prompt-audit.md` maps those concepts to fixed schema fields and records discrepancies; it does not introduce a second glossary.

Review the entire request, not only the static prompt: role, category instructions, dynamically supplied context, response schema, examples and retry text. For every prompt family, record which PRD rule it implements, what data it can actually read, what the schema can express, and how code checks the answer. Inspect every category entry. Preserve source quotes, identifiers, amounts, dates, polarity and inclusive/exclusive bounds exactly.

Candidate translations remain review artifacts until the compatibility design is complete. Existing frozen prompt files and requests are never edited in place. Distinguish a faithful language change from a pre-existing policy conflict; do not hide a policy change inside translation. The Idea prompt's five-rung-only and always-bullish-first descriptions must be corrected to describe the existing two/five-rung, asset/theme contract. These corrections describe already supported data; they do not alter the ladder policy.

Before activation: a read-only review reads the English prompts alongside the PRDs, schema and readers, checks the terminology correspondence and walks real stored requests. Record static and assembled request characters and prompt tokens before/after. English character growth needs a written explanation; repeated enum lists owned by the schema are removed, not translated into a second list. No model-quality claim follows from these checks. Any fresh English quality comparison needs its own agreed acceptance and budget.

## Sequence and completion

1. Inventory and read-only design review. Resolve serious contract gaps before implementation.
2. Convert vocabulary, active request builders/prompts, numeric text readers and operator defaults, with compatibility tests and stored-answer replay.
3. Translate current design/docs through their owners; retain explicit archival exceptions and update links/glossary checks.
4. Run touched suites, meaningful scratch mutants, UI checks and the full Python suite once on the final code; perform the D22 reasoning refresh, then `docs/check.py` last.
5. Update CURRENT_STATE with measured remaining language coverage and open functional defects. English quality needs a separately registered fresh comparison; this change cannot claim extraction is sealed.

The implementation uses the standard library and existing build tools. Enum normalization is a bounded dictionary lookup per field, not another model call, embedding search or database migration. Dataset-size and call-count budgets remain unchanged; compare read-path output and timing on the stored data before claiming the compatibility layer is negligible.

Prior decisions: D3 keeps budgets outside product Config; no new paid settings. D25 retains one extraction module. D36 keeps one term per concept; English replaces the maintained glossary. D42 keeps evidence linked to a question. D149 retains extraction-owned grouping. D155 retains exact identity rules and reference lists as references. D162 remains a failed isolated experiment. D163 changes language, not any of those product rules.
