# Extraction

> **2026-11-05: every open question per item.** Alex chose the recommended all-open lookup after reviewing its context cost. Each item reads every question open before its own dispatch sequence, including topics opened earlier on the same day. The split POC's A and B calls receive the same per-item snapshot and may run in parallel. This supersedes the subject-filtered selection and D251's once-per-day snapshot. The old production code still uses day-start subject-filtered context until implementation and verification. Historical runs and the frozen ruler remain unchanged. The message is in the decision log.

> **2026-11-05 decision:** A worthwhile new question with its article evidence is handed to the thesis library even when date, check material, period or ladder is unknown. Those fields are conditional, not code gates; later research agents may fill them from information available then. Never invent a date or interval to make a record pass. This supersedes mandatory-field admission clauses in the current implementation for the new design, without editing the frozen extraction ruler or rewriting historical scores. See [Thesis library](06-views.md).

> Status: foundation frozen, October 18, 2026; the production prompt is frozen at extraction v74i (`poc/config/poc-v108.json`, D274) and the code builds no other version (D359). D149 requires extraction-time grouping; D165 integrates it into the default pipeline (poc-v20), with a company's own financial lines carrying no group. English edition: October 25, 2026 (D163); corrected to D207, D209, D211, D251, D259, D264, D265, D273, D274 and D361 on 2026-11-05 (D367).
> Design page: `docs/system-design.html` → New → Extraction → Details. Recorded decisions take precedence over this PRD.
> The step's standard (what is kept, how much it weighs, which questions open, the golden set and how a prompt change is measured) is the signed page `05-extraction-standard.html` (D243), which replaces `docs/research/2026-10-29-analyst-standard/standard.md` (D229). Where this PRD differs from it on what is kept, its weight, which questions open or how a change is measured, the page governs; on the request's shape and the pipeline, the decisions in force govern (the page is frozen, D261; its statements later decisions changed are recorded in [05-extraction-standard-corrections.md](05-extraction-standard-corrections.md), D368).

## Purpose

Read each whole item with its category prompt as a senior hedge-fund analyst. Return evidence linked to shown or candidate theses, and candidates for important uncovered questions. Each candidate also carries structured group associations and any necessary new group definitions. Every output retains its source. Hand everything to the library, which owns the [grouping contract](06-views.md#research-groups-associate-during-extraction). Personal memos follow the prompt rule below.

## Rationale

- Extraction reads; the library compares and stores. Those responsibilities remain separate.
- Read the complete file with embedded tables, or an entire table release, without separate text/table pipelines.
- Categories require different reading: news for events and attribution, research for views and ratings, official decisions for actions and effective dates. They share one prompt structure.
- A thesis is an analyst's research question; its ladder and due date are recorded when supported and can be absent initially. Evidence records who said what in which item, including relevant attributed opinions. Most items add evidence; fewer create new questions.
- Evidence matters in relation to a question. The item reads every open question committed immediately before it, including earlier same-day writes, each with its question, subject, available due date and takes line. It shows no states, evidence or separate list of research groups. The model files each statement under those questions itself, with no separate placement call.
- Important uncovered matters, including another named company, a new material issue or a macro/policy event, become candidates with initiating evidence. The library later determines whether they are existing or new questions.
- Sources make both theses and evidence traceable to the original text.

## One item, step by step

The model performs step 2; code performs the others.

<!-- generated: steps -->
```
An item arrives with category and sequence number
  ↓ 1 Build the prompt (Code): Use the category's content in the shared template. Read every open question immediately before this item, including earlier same-day writes. Both experimental split calls use this same per-item snapshot; no dependency links or list of stored groups.
  ↓ 2 Read (Model): Read the whole item. Return evidence, each piece filed under the narrowest block-5 thesis it bears on and the answer's candidates it supports (D207, D264), and candidates for important uncovered questions with their initiating evidence. Personal memos follow their special rule. Decide each candidate's group association and return references under the library contract. Retain sources.
  ↓ 3 Check sources and group references (Code): Check that the quote or cell exists in the item and that cited numbers appear there. Evidence must link to block-5 theses or current candidates. Reject source mismatches with reasons. Validate association references under the library's complete handoff contract.
  ↓ 4 Hand off to the library (Code): Hand off evidence, candidates, associations and necessary group definitions with the sequence number. Matching decides identity; writing preserves membership.
```
<!-- /generated: steps -->

## Two outputs: evidence and candidates

The existing single-call design returns evidence, candidates, group associations and necessary new group definitions. The two-call split is an experiment, not the accepted production default. Each statement is filed under one home: the narrowest open thesis it bears on, as that thesis's own figure, step or estimate or through the demand, supply, competition or pricing behind its answer, never also a broader thesis beside it, plus the answer's own candidates it supports (D207, D259, D264). When no specific thesis is connected, a statement that moves the demand, supply, competition or pricing behind the company's results goes to the company-wide revenue thesis of its period (D273, kept by D361); a statement nothing takes is dropped as "no home" (D209). Code keeps the narrower of a thesis and one it depends on when a statement is linked to both (D265). The coverage-start reading's records are the one exception: each links to every thesis that read it (D364, below). Candidates are reserved for important uncovered questions, subject to the personal-memo rule. From extraction version 12 (D184) a candidate opens only for one of four admission reasons, stated in the answer: an annual quantity that carries the company's value, guided or not; one industry aggregate per calendar year; a stage of a policy process; a binding obligation a universe company takes on (due within 18 months, D185). The candidate also names the public material that settles it. Code checks the shape of these fields; the model keeps the judgement of importance (D154/D155). A later estimate, another population or another wording of a shown aggregate is evidence to it. The library first resolves a candidate's destination, then compares its evidence within that thesis.

<!-- generated: two -->
|  | Evidence | Candidate thesis |
|---|---|---|
| What it is | A statement or number from the item: who said what or what happened | A complete question to track: subject, question, ladder, due date and research-group association |
| How common | Present in almost every item | Few: important questions uncovered by block 5; also all judgements from the user's memo |
| Links | One home: the narrowest block-5 thesis it bears on, plus the answer's candidates it supports (D207, D264) | Carries initiating evidence; candidates from the user's memo may omit it |
| In the library | Compare against its thesis's existing evidence: repeat, replacement or new | Decide existing identity or a part of it, succession, new thesis or skip. Preserve associations with the final thesis; matching does not regroup. |
| Example | The 8-K statement that H20 exports to China require a licence | What will the China export-licence regime for chips covered by the April 2025 rule be on April 15, 2026? |

```
Read a statement or number | Which thesis does it concern? (Judgements in the user's memo bypass this tree: all become candidates and may lack evidence)
├─ A thesis in block 5 → Evidence: file it under the narrowest one it bears on (As that thesis's own figure, step or estimate or through the demand, supply, competition or pricing behind its answer; that thesis only, never a broader one beside it, plus the answer's candidates it supports (D207, D259, D264). When no specific thesis is connected, a statement that moves the demand, supply, competition or pricing behind the company's results goes to the company-wide revenue thesis of its period (D273, D361).)
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
| Open theses before the item | Every open question committed before this item, including earlier same-day writes, each with its takes line. Both experimental split calls receive the same per-item snapshot. No states, evidence, dependency links or list of stored research groups. | Thesis library, read per item |
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
└─ 5 Open theses before the item → Every open question committed before this report, including earlier same-day topics (Both experimental split calls share this snapshot; each question has its takes line. No states, evidence, dependency links or list of stored research groups.)
```

- Each category has its own prompt using the same template. Blocks 2 and 4 vary by category; block 1 is shared; code fills blocks 3 and 5 for the item.
- One prompt per tracked category T1–T15. T16 is not tracked by default; write its prompt when needed.
- For theme candidates, select from block 3 or describe a new issue if absent. For companies, cryptocurrencies and commodities, provide the relevant symbol or name. Code resolves reference data and accepts registered names only, as classification does.
- The user's own memo (T8 authored by the user) yields candidate judgements, not evidence. These candidates may have no evidence. Once opened, their state is “not yet judged” until evidence first links to them.
- Code defines and validates output fields for evidence, candidates and associations, necessary new groups and sources. Do not restate the shape in prompts.
- The production prompt is frozen at extraction v74i (D274); a change is a new version Alex opens, measured against it, and Config records each version.
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
│   └─ Candidate: NVDA asset thesis → How will NVDA FY2026 China revenue compare with FY2025? (Numeric thesis. Five rungs: up at least 50%; up 10% to under 50%; change under 10% either way; down 10% to under 80%; down at least 80%. Due on the FY2026 annual earnings date. Quote: “…up to approximately $5.5 billion of charges…”. This is a company expectation, classified as a party statement. The library opens #2; its dependency on #1 would be chosen in matching (D51), which the default Jev path does not yet do, and the licence theme reaches #2 through the theme block (D191, D195).)
└─ NVIDIA statement, July 14, 2025 → Block 5 shows #1 and #2, open immediately before the item, with their takes lines | One evidence item, no candidate
    └─ Evidence → Link to #1 (Party statement: NVIDIA says the US government assured it that H20 export licences to China will be granted (July 14, 2025))
```

Each evidence item records upstream ID, paragraph and exact quotation. Code checks that “$5.5 billion” appears in the quoted sentence. The first item sees an empty library, so important questions become candidates. The second sees the licence thesis and links NVIDIA's statement directly. The library compares candidates with searched theses and evidence within its thesis. Both candidates join the chip-licensing-and-China-business group; the evidence-only second item updates existing membership. Grouping is not a dependency: it neither creates nor replaces one. The NVDA example uses the same process as equities, futures and cryptocurrencies.
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
- Evidence contains a quotation, standalone summary, speaker, original source, tier and event time. A candidate contains subject, asset/theme kind, focus, question, ladder, due date, association, admission reason, settling material and at least one evidence item; personal-memo candidates may lack evidence. A blank settling material or a binding obligation due beyond 18 months is refused with its reason. Themes select from block 3 or clearly identify a new issue; assets use a symbol or registered name.
- Every thesis and evidence item has a source. Reject absent quotes/cells or numbers not printed in the cited location, recording the reason.
- Extraction does not mutate the library. Return evidence, candidates and associations together without a separate clustering call. Reference and semantic criteria are owned by the [grouping contract](06-views.md#research-groups-associate-during-extraction); similar names or equal counts do not prove correct grouping.
- Retry from the failed step and replace only that attempt's own result.

## Coverage-start reading (D363, D364)

Built 2026-11-05 (`src/hivemind/baseline.py`; configuration `poc/config/poc-v116.json`; validation record `docs/research/2026-11-04-filing-end-to-end/baseline-design.md`
rounds 8-26; design with its four tables `production-design.md` there). The daily stream keeps out restatements of figures the company has already reported (extraction
standard §5.3), so a question whose decisive figure was last reported before coverage started would wait a quarter for evidence. This step closes that gap once.

**When.** At coverage start, after the seed questions are written and before the first day's items; once per ledger, and only on a ledger that has processed nothing yet.
A resumed run skips it; a run cannot start after an unfinished coverage-start day (that day's judging round judges the starting figures).

**What it reads.** The company's earnings-release items (category T1, the company's ticker among the item's subjects) of the latest publication day before coverage
start; of that day the filed items when the day also has newsroom or investor-site copies. Their page text with tables (the cleaned text drops tables); a missing page
text refuses the step before any model call.

**The reading.** Each open question reads each item once, one question at a time, for the figure its quantity stands at in the report's most recent period; when the report
does not state the quantity under the question's name, only the lines it is computed from or the line that is the same quantity under another name — never a broader
line that holds other things, or a line next to it. Example: an operating-margin question writes the quarter's operating income and revenue; a capital-spending question
writes "Purchases related to property and equipment and intangible assets"; a question on one product's revenue, which the report does not state, writes nothing. The
prompt is `prompts/baseline-v3.json` with the schema in code; the code builds no other version.

**What code keeps (identity only).** A figure whose quote is the report's own text (at least eight characters), carries a label, and prints the figure written as the
value. A table row quoted with a footnote mark left off or a cell left out is stored as the report's own text from the row's label to the figure. Refused figures are dropped
with their reasons in the step's processing record. Which question a figure belongs to, and which column it is from, stay the reading's.

**What it writes.** One evidence record per item and quote, linked to every question that read it (D364: first-quarter revenue read by total revenue, operating margin and
next year's revenue is one record with three links; the daily stream's one-home rule does not apply to these records): fact tier, the company as speaker and original
source, the report's day, the item as source, the model's one-line with the unit added when the value has no scale of its own. One processing record (step
`baseline`, dated the coverage-start day, with its own sequence number) names the questions linked, the figures kept and refused, and the empty readings; the first day's
judging round judges those questions with the day's other changes.

**Measured.** On the frozen v108 ledgers, May 20, 2026 report: operating margin and capex each judged inside the gold range 9 of 9 (before: never judged); no question
that was right turned wrong; every kept figure the question's own quantity (two readers). On the held-out August 26 report: no wrong figure among 44; the operating-margin
lines read 3 of 3, capex 2 of 3. About three cents per company. Accepted end to end on 2026-11-05: three draws of the 14-day window against `poc-v108` re-run in the same
hours, scored on the frozen judgement ruler: operating margin and capex each inside the gold range 3 of 3 (never judged in the control), 53 against 45 agreements of 57,
no question made wrong by the starting figures (`acceptance-design.md` there). The replay default since D366.

**Known gaps (written down, not built).** The capital-spending line is missed in about one read in six (a miss leaves the question as it was); a labelled guidance figure
the reading keeps is written with the fact tier; later reports reach the questions through the daily stream only; `scripts/preflight.py` does not replay the reading's check (the research replays do).

## Open questions

<!-- generated: open -->
- The asset-ladder and shared-quantity changes Alex decided (D186, D191 point 4) are built in the next extraction version (D368; DECISIONS §6).
<!-- /generated: open -->

## Related decisions

- D11: theses belong to subjects; extraction handles body mentions. D13: information-driven processing.
- D25–D28: one extraction module, shared analyst role, category prompts, whole-item reading, sources and restored report ingestion.
- D32/D33: whole table releases, no separate filing XBRL ingestion, read-only extraction with matching/writing in the library.
- D35/D37: first-version review and freeze; changes require a decision.
- D41/D42: candidates and block-5 context updated for the rebuilt library; separate evidence/candidate outputs with existing dependencies shown (block 5 replaced by D211, D251 and D264, below).
- D45: only recorded decisions apply; no unapproved preset settlement source or theme-scope restriction.
- D46: write the complete candidate while the full source is available.
- D47: explicit dependency links; link a statement only to the question it directly concerns (widened by D259: the narrowest open thesis it bears on, including through the demand, supply, competition or pricing behind its answer).
- D51: omit unapproved restrictions on theme observations; evidence-link quality checks belong with matching labels; no consensus calculation.
- D58: include due dates in block 5; events after an existing due date can form candidates.
- D59/D60: subject identification and personal-memo candidates; no judgement before evidence first links; wording and diagram alignment without new rules.
- D149: associations are required extraction output; D165 integrates them into the default implementation.
- D155: current POC identity/reference changes are described in the improvement plan, not evidence of grouping acceptance.
- D184/D185: four admission reasons and the settling material. D211: the fields naming the thesis a candidate would otherwise attach to and what would be lost left the output.
- D207/D209/D259/D264/D265/D273/D361: one home per statement, the narrowest open thesis it bears on, plus the answer's own candidates; the company-wide revenue thesis takes indirect evidence no specific thesis takes; a statement nothing takes is dropped as "no home"; code keeps the narrower of a thesis and one it depends on.
- D211/D251/D264: extraction files each statement itself, with takes lines and no separate placement call. D375 on main supersedes the day-start timing: read the latest committed questions before each item.
- D274/D359: the production prompt is frozen at v74i; a change is a new version only Alex's decision opens, and the code builds no other.
- D363/D364: the coverage-start reading of the company's latest report, once per ledger; a figure several questions read is one record linked to each.

<a id="抽取时同时确定研究归属"></a>

## Determine associations during extraction

<!-- generated: relations -->
- D149 requirement: while reading the full text, decide which continuing business process each candidate belongs to, called a research group. Rubin shipments and SK factory deployment retain separate questions while sharing the Rubin rollout group. Group during extraction, not in the frontend or a later whole-library clustering pass.
- Return evidence and candidates separately. Each candidate also carries structured associations; new groups have a name and scope. Mentioning a relationship only in prose is not a complete handoff. Extraction is read-only; the library's “Research groups: associate during extraction” section owns the full handoff and storage contract.
- D165 integrates grouping into the default extraction handoff. Integration alone does not establish semantic quality; see docs/poc/grouping-improvement-plan.md and the recorded benchmark results for steps, measurements and limits.
<!-- /generated: relations -->
