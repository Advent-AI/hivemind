# Extraction

> Status: foundation frozen, October 18, 2026; category prompt wording needs validation. D149 requires extraction-time grouping; D165 integrates it into the default pipeline (poc-v20), with a company's own financial lines carrying no group. English edition: October 25, 2026 (D163).
> Design page: `docs/system-design.html` → New → Extraction → Details. Recorded decisions take precedence over this PRD.
> The step's standard (what is kept, how much it weighs, which questions open, the golden set and how a prompt change is measured) is the signed page `05-extraction-standard.html` (D243), which replaces `docs/research/2026-10-29-analyst-standard/standard.md` (D229). Where this PRD differs from it, the page governs.

## Purpose

Read each whole item with its category prompt as a senior hedge-fund analyst. Return evidence linked to shown or candidate theses, and candidates for important uncovered questions. Each candidate also carries structured group associations and any necessary new group definitions. Every output retains its source. Hand everything to the library, which owns the [grouping contract](06-views.md#research-groups-associate-during-extraction). Personal memos follow the prompt rule below.

## Rationale

- Extraction reads; the library compares and stores. Those responsibilities remain separate.
- Read the complete file with embedded tables, or an entire table release, without separate text/table pipelines.
- Categories require different reading: news for events and attribution, research for views and ratings, official decisions for actions and effective dates. They share one prompt structure.
- A thesis is the analyst's judgement expressed as a question, ladder and due date. Evidence is an objective record of who said what in which item. Most items add evidence; fewer create new questions.
- Evidence matters in relation to a question. Block 5 supplies existing subject theses and their dependencies, allowing a company statement about assured export licences to link directly to the licence theme.
- Important uncovered matters, including another named company, a new material issue or a macro/policy event, become candidates with initiating evidence. The library later determines whether they are existing or new questions.
- Sources make both theses and evidence traceable to the original text.

## One item, step by step

The model performs step 2; code performs the others.

<!-- generated: steps -->
```
An item arrives with category and sequence number
  ↓ 1 Build the prompt (Code): Use the category's content in the shared template. The library supplies block 5: open subject theses, their dependencies and existing groups needed for association.
  ↓ 2 Read (Model): Read the whole item. Return evidence linked to block-5 theses or current candidates, and candidates for important uncovered questions with their initiating evidence. Personal memos follow their special rule. Decide each candidate's group association and return references under the library contract. Retain sources.
  ↓ 3 Check sources and group references (Code): Check that the quote or cell exists in the item and that cited numbers appear there. Evidence must link to block-5 theses or current candidates. Reject source mismatches with reasons. Validate association references under the library's complete handoff contract.
  ↓ 4 Hand off to the library (Code): Hand off evidence, candidates, associations and necessary group definitions with the sequence number. Matching decides identity; writing preserves membership.
```
<!-- /generated: steps -->

## Two outputs: evidence and candidates

One reading returns evidence, candidates, group associations and necessary new group definitions. Evidence may link to shown theses or current candidates. Candidates are reserved for important uncovered questions, subject to the personal-memo rule. From extraction version 12 (D184) a candidate opens only for one of four admission reasons, stated in the answer: an annual quantity that carries the company's value, guided or not; one industry aggregate per calendar year; a stage of a policy process; a binding obligation a universe company takes on (due within 18 months, D185). The candidate also names the public material that settles it, the shown thesis the statement would otherwise attach to (or none) and what is lost if it only attached there. Code checks the shape of these fields; the model keeps the judgement of importance (D154/D155). A later estimate, another population or another wording of a shown aggregate is evidence to it. The library first resolves a candidate's destination, then compares its evidence within that thesis.

<!-- generated: two -->
|  | Evidence | Candidate thesis |
|---|---|---|
| What it is | A statement or number from the item: who said what or what happened | A complete question to track: subject, question, ladder, due date and research-group association |
| How common | Present in almost every item | Few: important questions uncovered by block 5; also all judgements from the user's memo |
| Links | One or more block-5 theses, or current candidates | Carries initiating evidence; candidates from the user's memo may omit it |
| In the library | Compare against its thesis's existing evidence: repeat, replacement or new | Decide existing identity or a part of it, succession, new thesis or skip. Preserve associations with the final thesis; matching does not regroup. |
| Example | The 8-K statement that H20 exports to China require a licence | What will the China export-licence regime for chips covered by the April 2025 rule be on April 15, 2026? |

```
Read a statement or number | Which thesis does it concern? (Judgements in the user's memo bypass this tree: all become candidates and may lack evidence)
├─ A thesis in block 5 → Evidence: link to that thesis (Link only to the thesis directly discussed, not also to theses that depend on it)
├─ Not in block 5, but important → Candidate thesis with this statement as evidence (Return its group association during extraction. The library later decides existing identity or new thesis. A thesis covers only up to its due date; events after that date belong here too.)
└─ Neither → Do not extract (Background or boilerplate)
```
<!-- /generated: two -->

## Prompt template

All categories use these five blocks. Classification owns the category's definition and reading method.

<!-- generated: template -->
| Part | Writes | Source |
|---|---|---|
| Role | You are a senior hedge-fund analyst. Read this item to test and form theses: link supporting or opposing statements and numbers as evidence to existing theses. For important questions not covered, return complete candidates with a question, ladder, due date, research-group association and initiating evidence. Judgements in the user's own memo become candidates, may lack evidence and are not themselves evidence. Each thesis concerns one thing. Its ladder has five rungs, or two for yes/no, with concrete, verifiable, non-overlapping and exhaustive outcomes, never vague “partial” outcomes. Set the due date when the issue can be resolved; for a number, use its publication date. Name the year. This year and next year are relative to the item's publication day; company numbers use its fiscal year. | Shared by all categories; thesis rules come directly from the library |
| What this category is and how to read it | The category definition and reading method; for example, attribute opinions and estimates to their author rather than treating them as completed facts. | Owned by classification; not redefined here |
| Subjects | The item's related subjects plus every theme in the research universe. Select an existing theme for a theme candidate when applicable; otherwise describe the new issue clearly. | Item metadata; themes from the research universe |
| What to extract from this category | One row per category in the table below. | Extraction module |
| Existing theses and research groups | Open theses for the item's subjects and their dependencies, with dependency links. Supply only question, focus and due date, not states or evidence. Also supply available research groups under the library's grouping contract. | Thesis library |
<!-- /generated: template -->

## Category-specific prompts

T7 news illustrates how the five blocks fit together.

<!-- generated: prompt -->
```
T7 news prompt (The same template, with news-specific blocks 2 and 4)
├─ 1 Role → Senior hedge-fund analyst (Read to test and form theses. Link evidence to existing theses; for important uncovered questions, return complete candidates with question, ladder, due date and research-group association.)
├─ 2 How to read this category → Media reporting (From classification: opinion and analysis belong to T8; registered publication series use their category; remaining media material belongs here.)
├─ 3 Subjects → Subjects of this report (Filled by code, such as NVDA and AMD, plus all universe themes)
├─ 4 What to extract → What happened, when and who was involved; attribution and original sources (Official confirmation is fact; unnamed-source claims are rumours)
└─ 5 Existing theses and research groups → Open theses for the report's subjects and their dependencies (Filled by code with dependency links, questions, focus and due dates. For example, NVDA FY2027 China revenue versus FY2026 and its chip-export-licence dependency. Also include available research groups.)
```

- Each category has its own prompt using the same template. Blocks 2 and 4 vary by category; block 1 is shared; code fills blocks 3 and 5 for the item.
- One prompt per tracked category T1–T15. T16 is not tracked by default; write its prompt when needed.
- For theme candidates, select from block 3 or describe a new issue if absent. For companies, cryptocurrencies and commodities, provide the relevant symbol or name. Code resolves reference data and accepts registered names only, as classification does.
- The user's own memo (T8 authored by the user) yields candidate judgements, not evidence. These candidates may have no evidence. Once opened, their state is “not yet judged” until evidence first links to them.
- Code defines and validates output fields for evidence, candidates and associations, necessary new groups and sources. Do not restate the shape in prompts.
- Test each category's prompt on stored items before settling its wording. Config records each version; a change creates a new version.
<!-- /generated: prompt -->

## What each of the 16 categories yields: block 4

<!-- generated: categories -->
| Category | What to extract | Typical evidence tier |
|---|---|---|
| T1 Earnings releases | Actual figures, guidance and management explanations | Actual figures are facts; guidance and explanations are party statements |
| T2 Periodic reports | Actual and segment figures; risks and changes in risk factors and business descriptions | Figures are facts; described risks and changes are party statements |
| T3 Legal and capital-markets documents | Transaction terms: price, consideration, closing conditions and timetable; parties' statements and demands | Terms are facts; statements are party statements |
| T4 Company-call transcripts | Management answers to key questions, changes in wording and analysts' follow-up concerns | Answers are party statements; analysts' questions are third-party views |
| T5 Presentations | Management's medium/long-term targets, capital-allocation framework and new-business scale | Party statement |
| T6 Other company publications | Events such as executive changes, acquisitions, products and buybacks; published operating figures such as deliveries | Fact |
| T7 News | What happened, when and who was involved; attribution and original sources | Official confirmation is fact; unnamed-source claims are rumours |
| T8 Opinion and analysis | The author's opinions, arguments, forecasts, ratings and targets, and changes to them | Third-party view |
| T9 Interview records | The speaker's account of orders, prices, share and inventory, and how they know | Third-party view |
| T10 Official actions and records | The decision/action, effective date and affected parties; subsequent appeals and deadlines that may set the due date | Fact |
| T11 Macro policy and statistics | Published figures and policy decisions versus the previous release; changes in official wording | Figures and decisions are facts; wording is a party statement |
| T12 Market prices and trading | Changes in prices and trading | Fact |
| T13 Holdings and flows | Who buys, who sells and at what scale | Fact |
| T14 Calendar | Scheduled dates that can set due dates | Fact |
| T15 Third-party measurements | Measured operating data as quantitative evidence | Fact; identify the third-party measurement |
| T16 Reference data | Not tracked by default | — |

Read every whole file, including tables. A table release is one item and is read as a whole batch. Do not separately ingest XBRL facts already in the filing. Whether to fetch exact settlement numbers is deferred to pull-mode design.
<!-- /generated: categories -->

## Example: two items

<!-- generated: example -->
```
What two items yield (Illustration)
├─ NVIDIA 8-K, April 15, 2025 → Empty library; no theses in block 5 | Two candidate theses (T6 other company publication: H20 exports to China require a licence; expected charges up to approximately $5.5 billion)
│   ├─ Candidate: theme thesis → What will China export licensing for chips covered by the April 2025 rule, including H20 and MI308, look like on April 15, 2026? (Event thesis. Five rungs: full ban; licences required and none issued; licences issued with some conditions; all issued licences unconditional; no licence required. Due April 15, 2026. Quote: “…requires a license for export to China … of the Company’s H20 integrated circuits…”. NVIDIA discloses the licence requirement, classified as fact. The library opens thesis #1.)
│   └─ Candidate: NVDA asset thesis → How will NVDA FY2026 China revenue compare with FY2025? (Numeric thesis. Five rungs: up at least 50%; up 10% to under 50%; change under 10% either way; down 10% to under 80%; down at least 80%. Due on the FY2026 annual earnings date. Quote: “…up to approximately $5.5 billion of charges…”. This is a company expectation, classified as a party statement. The library opens #2, dependent on #1.)
└─ NVIDIA statement, July 14, 2025 → Block 5 contains #2 and its dependency #1 | One evidence item, no candidate
    └─ Evidence → Link to #1 (Party statement: NVIDIA says the US government assured it that H20 export licences to China will be granted (July 14, 2025))
```

Each evidence item records upstream ID, paragraph and exact quotation. Code checks that “$5.5 billion” appears in the quoted sentence. The first item sees an empty library, so important questions become candidates. The second sees the licence thesis and links NVIDIA's statement directly. The library compares candidates with searched theses and evidence within its thesis. Both candidates join the chip-licensing-and-China-business group; the evidence-only second item updates existing membership. Grouping does not replace #2's dependency on #1. The NVDA example uses the same process as equities, futures and cryptocurrencies.
<!-- /generated: example -->

## Source-reference fields

<!-- generated: sources -->
```
A source reference
├─ Which item → Upstream ID (Each version has its own ID; use it to retrieve the original from the team's library)
├─ Category and day → Category and publication day
├─ Where in the item → Section, paragraph or table cell (For table data, record dataset and record IDs)
└─ Which statement → The original sentence or table cell (Code verifies the quote exists in the item and the cited number appears there)
```

- Every thesis, evidence item and information-triggered change retains sources. Each state change identifies its supporting evidence, plus dependency theses when their changes triggered rejudgement.
- Extraction checks quote/cell presence, number presence and links to block-5 theses or current candidates. Reject output failing any check. The library refuses sources absent from processing records. Both record reasons.
- Trace in both directions: thesis to all source items, and item to every thesis and evidence item it created or changed.
- Do not store the whole source item; retrieve it from the team's library by upstream ID. Store only the quoted sentence or cell supporting the thesis or evidence.
- Repeated statements of the same fact within one item, such as a number in text and a table, become one evidence item with multiple references.
<!-- /generated: sources -->

## Acceptance

- Give the model every whole item with its category prompt; record the settings version.
- Every evidence link targets a shown thesis or current candidate. Reject missing or invalid targets with reasons.
- Repeated statements of the same fact within one item, including text/table repetitions, produce one evidence item with multiple references.
- Evidence contains a quotation, standalone summary, speaker, original source, tier and event time. A candidate contains subject, asset/theme kind, focus, question, ladder, due date, association, admission reason, settling material, the thesis it would otherwise attach to (or none), the loss if folded, and at least one evidence item; personal-memo candidates may lack evidence. A blank loss or settling material, an unshown thesis in the fold field, or a binding obligation due beyond 18 months is refused with its reason. Themes select from block 3 or clearly identify a new issue; assets use a symbol or registered name.
- Every thesis and evidence item has a source. Reject absent quotes/cells or numbers not printed in the cited location, recording the reason.
- Extraction does not mutate the library. Return evidence, candidates and associations together without a separate clustering call. Reference and semantic criteria are owned by the [grouping contract](06-views.md#research-groups-associate-during-extraction); similar names or equal counts do not prove correct grouping.
- Retry from the failed step and replace only that attempt's own result.

## Open questions

<!-- generated: open -->
- Validate each category prompt on stored items before settling it; record its version in Config.
<!-- /generated: open -->

## Related decisions

- D11: theses belong to subjects; extraction handles body mentions. D13: information-driven processing.
- D25–D28: one extraction module, shared analyst role, category prompts, whole-item reading, sources and restored report ingestion.
- D32/D33: whole table releases, no separate filing XBRL ingestion, read-only extraction with matching/writing in the library.
- D35/D37: first-version review and freeze; changes require a decision.
- D41/D42: candidates and block-5 context updated for the rebuilt library; separate evidence/candidate outputs with existing dependencies shown.
- D45: only recorded decisions apply; no unapproved preset settlement source or theme-scope restriction.
- D46: write the complete candidate while the full source is available.
- D47: explicit dependency links; link a statement only to the question it directly concerns.
- D51: omit unapproved restrictions on theme observations; evidence-link quality checks belong with matching labels; no consensus calculation.
- D58: include due dates in block 5; events after an existing due date can form candidates.
- D59/D60: subject identification and personal-memo candidates; no judgement before evidence first links; wording and diagram alignment without new rules.
- D149: associations are required extraction output; the default implementation has not yet integrated them.
- D155: current POC identity/reference changes are described in the improvement plan, not evidence of grouping acceptance.

<a id="抽取时同时确定研究归属"></a>

## Determine associations during extraction

<!-- generated: relations -->
- D149 requirement: while reading the full text, decide which continuing business process each candidate belongs to, called a research group. Rubin shipments and SK factory deployment retain separate questions while sharing the Rubin rollout group. Group during extraction, not in the frontend or a later whole-library clustering pass.
- Return evidence and candidates separately. Each candidate also carries structured associations; new groups have a name and scope. Mentioning a relationship only in prose is not a complete handoff. Extraction is read-only; the library's “Research groups: associate during extraction” section owns the full handoff and storage contract.
- Grouping remains a target requirement, not a default-pipeline handoff. D155 fixed reference-list vetoes, period/scope rewriting and same-batch duplicates; that does not prove grouping works. See docs/poc/grouping-improvement-plan.md for steps and measurements.
<!-- /generated: relations -->
