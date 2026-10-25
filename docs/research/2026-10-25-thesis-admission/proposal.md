# Thesis admission: business question before representation

Status: proposal for Alex's review. No prompt, runtime, database, gold or production behavior changes are made here. The investor-facing criterion was clarified in the discussion after D174: absence of a separate NAVER card is not, by itself, a defect. Source coverage, appropriate question attachment and faithful interpretation are the criteria.

## Diagnosed mechanism

`role-v10.txt` starts by asking the model to test and form theses, but its next section instructs it to propose annual total/segment revenue theses and quantified external matters. That creates a numeric-card recipe before the model decides whether the underlying business question deserves a separate thesis. D154/D155 instead leave importance to the analyst model; the PRD's open granularity question is not permission to require a card for every number.

The returned `measure` then does two jobs: it identifies a quantity for matching and decides whether the date limit applies. `extraction.sift` permits future `event`/`policy_event` questions but rejects other measures after next year. A physical project's completion criterion can include a number. Expressing it as `capacity` rather than `event` changes admission. Rejected candidates lose their sole linked evidence; unused group declarations then disappear. This follows the current code, rather than a concurrency failure.

D174 measured this on real data: the stored NAVER answer proposed completion of a 200 MW expansion by 2028; the fresh sequential answer proposed capacity in 2028 and was rejected. The original SK request was byte-identical across the stored and fresh runs, yet the source interpretation and group output differed. The recorded horizon census contains eight refusals across 963 answers, including seven historical financial/spending forecasts and the fresh NAVER project. Those are not eight defects; blanket removal of the date limit is not justified.

## One admission decision, three responsibilities

1. **Analyst model: identify the business question and significance.** Read the full source and the existing thesis/group context. Decide whether a statement directly informs an existing question, justifies an independently testable new question, or is outside the current research task. A named project or number alone does not justify a new thesis. A plan remains a plan; do not invent orders, delivery dates or revenue recognition.
2. **Schema and code: represent how the question resolves.** Distinguish a quantity observed over a period from a milestone assessed at a deadline. Do not infer that distinction from words in the question or the presence of a numeric target.
3. **Existing library: compare, group and write.** Keep the current sequential matching/writing path. Group association stays in the original extraction call. Similarity, group membership and economic relevance do not establish duplicate identity.

This is one extraction call with a clearer contract. No new clustering call, company watch-list veto, project registry or hierarchy is proposed.

Adding a discriminator alone is not proof of a fix: the same model could still misclassify the source. The first experiment therefore keeps the existing schema and checks, changes only the contradictory thesis-selection instructions in a stored request, and compares fresh controls. It must show the intended question/attachment improves before a new representation is implemented. If it does not, trace the raw answer again rather than adding fields or prompt examples.

## Resolution contract: proposed closed alternatives

Replace the overloaded date decision with a tagged representation in a new prompt/schema version. The final field names and migration adapter would be fixed before implementation.

| Alternative | What it asks | Required meaning | Admission and representation |
|---|---|---|---|
| Period metric | What value will a defined quantity have over a stated period? | Quantity, scope, period, basis, unit; range ladder | Existing current/next-year policy remains. The numeric metric remains available to identity matching |
| Milestone | Will a specific, identifiable event or project reach a defined state by a deadline? | Event identity, source-grounded assessment deadline, verifiable completion condition; outcome ladder | Use the event deadline. The completion condition may contain a quantity, such as completion of the announced 200 MW expansion. It must describe that milestone, not relabel an ordinary annual forecast to bypass its horizon |

“NVIDIA 2028 revenue” stays a period metric. “Completion of NAVER's announced GAK Sejong expansion to 200 MW by its stated deadline” is a milestone. Neither gets a thesis automatically: first apply the business-question decision above. If they are merely supporting information for a directly relevant existing thesis, attach the evidence there.

The new request schema must express these alternatives without contradictory duplicate fields. One adapter converts an accepted alternative into the existing library identity/ladder representation. Old versions retain their old schema and interpretation. The writer and matcher do not reinterpret the same discriminator independently. Code validates shape, dates, source references, targets and key consistency; the meaning of materiality and the source-to-question relationship remains a semantic evaluation.

This clarifies the intended numeric/event distinction and changes the representation that enforces it. It requires a recorded decision and a versioned schema/prompt; it must not silently change existing stored records.

## NAVER through the proposed flow

- Preserve the statement as an announced expansion, with its 200 MW target and 2028 deadline attributed to the source. The number is not a confirmed NVIDIA order.
- Inspect the existing questions. If one directly tracks the relevant customer procurement/deployment development, attach the statement there without opening a duplicate project card. Do not attach it to total revenue merely because the project might eventually contribute revenue.
- If the project has an important, independently verifiable uncertainty not covered by the library, propose its milestone question and group association. If not, do not manufacture a thesis to save every number.
- Later reports find the same question or source statement through existing matching. A retelling adds a reference; it is not independent corroboration.

## State × event

| State | Event | Result |
|---|---|---|
| Source read, no destination chosen | Directly covered by an existing question | Source-grounded evidence link; no duplicate candidate |
| Source read, no destination chosen | Important uncovered, verifiable business question | Candidate with resolution alternative, initiating evidence and existing group contract |
| Source read, no destination chosen | Background or outside scope | No candidate; do not force an unrelated attachment |
| Period metric candidate | Outside the permitted period | Existing policy rejection with reason; do not relabel it as an event |
| Milestone candidate | Numeric completion criterion | Validate the named milestone and deadline; do not apply the annual-metric horizon merely because its criterion contains a number |
| Candidate validation | Malformed or contradictory representation | Explicit invalid output/failure; it is not equivalent to the model finding nothing useful |
| Accepted candidate | Matching finds same question | Existing merge/evidence comparison; preserve valid associations |
| New or repeated source | Same claim already present | Existing repeat/replacement rules; retain provenance and avoid double counting |
| Historical replay | Old schema version | Old interpretation; no in-place reclassification or identifier rewriting |

Ordering remains publication/dispatch-sequence based, not wall time. This design does not alter the failure/retry protocol, storage transactions, day boundaries or concurrency scheduling.

## Value × reader

| Value | Writer / readers | Ownership |
|---|---|---|
| Source statement, attribution, event time | Extraction → source check → evidence writer → matching/judging | Existing fields; no conversion of plans into realized orders |
| Proposed business question | Extraction → candidate comparison → writer | Existing question/focus fields; novelty and significance checked semantically |
| Resolution alternative | Versioned extraction schema → one admission/identity adapter | New version only; old records unchanged |
| Period or milestone deadline | Adapter → year/date checks, identity, ladder, UI | One interpretation; migrate every reader through the adapter rather than another ad hoc check |
| Group references | Extraction → group validation → existing writer | Existing D165/D166 contract |
| Accepted/rejected/dropped outcome | Admission → processing records and evaluation | Distinguish no proposal from rejection; report why coverage was lost |

## New path × old checks

| Existing check | Required proof |
|---|---|
| Exact quotation and provenance | Same source check for both resolution alternatives |
| Candidate/evidence references | Only existing/shown or same-answer targets; no fabricated fallback revenue link |
| Current/next-year numeric limit | Out-of-range annual forecasts still refused |
| Event identity and duplicate matching | Milestone normalization preserves identity, scope, deadline and source; numerals do not create a second project |
| Fixed exhaustive ladder | Numeric ranges remain non-overlapping; milestone conditions are verifiable and fixed |
| Groups, repeats, replacements | Existing semantics and transaction boundaries remain |
| Versioned replay | Old requests and stored answers keep their old interpretation; no database migration in this slice |

## Verification sequence

1. Correct the diagnostic rubric with Alex before another scored arm: information coverage and valid attachment matter; a mandatory project card or fixed group count does not. Keep the original gold file and record any revised interpretation separately.
2. Audit the full v10 request, not only the role text. Remove the mandatory numeric-card recipe; retain source attribution, important uncovered questions, existing-question reuse and group instructions. Compare total characters/tokens before and after. Add no NAVER-specific instruction.
3. Use stored cases for free controls: the NAVER source in milestone and period-metric forms; ordinary beyond-horizon revenue forecasts; short-dated quantities; existing project coverage; repeated announcements; a source with no material uncovered question. Then run the minimal instruction-only counterfactual described above, with fresh controls. A new schema is conditional on this causal diagnosis, not the first step. If adopted, prove a numeric target alone cannot turn an annual forecast into a milestone, and include a mutant that restores the overloaded `measure` gate.
4. Read-only design/code review, then full stored-answer preflight on copies. A changed refusal population is diagnosed before paid calls.
5. Run only the affected extraction calls with fresh controls and at least three samples, under a separately registered small cap. Judge coverage, attribution, legitimate new questions, wrong links, duplicate questions and milestone/period consistency. Calibrate against serial-versus-serial variation. Matching/writing remain the product path.
6. Resume the isolated sequential/concurrent comparison only after the baseline meets the agreed semantic criterion. Publish verified changes affecting the sequential path separately, under Alex's commit/push instruction.

## Boundaries and prior decisions

D154/D155 leave importance to the analyst rather than a hard-coded company topic list. D165/D166 own grouping and forbid company financial lines founding groups indiscriminately. D159 owns sequential visibility. D38/D49 and 06-views own ladders, fixed questions and numeric periods. D163 requires consistent English terminology. D170 explicitly left thesis granularity as unresolved work; a cleanup commit cannot silently settle it. D174 stopped the timing comparison after an uncalibrated semantic control, and D175 separates sequential maintenance from experimental work.

The main unresolved decision is the precise admission contract above, including how a source-grounded milestone with a numeric completion criterion maps to existing event identity. This proposal does not broaden every forecast horizon or claim that model importance judgements can be guaranteed by a schema.
