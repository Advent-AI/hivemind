# System overview

> Status: foundation frozen; pull mode and closing at the due day decided and built (D54, D356). Universe, classification, Config, dispatch, extraction and human-review intake froze on October 18, 2026; the library and matching labels on October 20; the full review completed October 22. D149 adds extraction-time grouping; D165 integrates it into the default pipeline. Corrected to D63, D198, D202, D204, D169, D190, D251, D260, D264 on 2026-11-05 (D367). English edition: October 25, 2026 (D163).
> Design page: `docs/system-design.html` → New → Open system PRD. Recorded decisions take precedence over this document.

## Purpose

Maintain a thesis library: create theses, update their judgements and close them when due. Upstream continuously supplies classified information. Extraction reads each whole item as a senior hedge-fund analyst, alongside existing theses, and returns linked evidence and candidates with research-group associations, declaring new groups where needed. The library preserves those associations and compares identity: merge, succession, new thesis or skip; repeat, replace or new evidence. Each thesis has a question, ladder and due date. Evidence moves its state, which freezes when due.

D149 requires organisation during full-text reading, with associations included in extraction output. See [the library's grouping contract](06-views.md#research-groups-associate-during-extraction) and [extraction's responsibility](05-extraction.md#determine-associations-during-extraction). Rubin shipments and SK factory deployment are separate questions in one continuing business process. D165 integrates grouping into the default pipeline; the [improvement plan](../poc/grouping-improvement-plan.md) records implementation gaps, D155 identity changes and validation work.

## Why rebuild

The old system pulled dated batches. Category definitions existed in nine modules, configuration used five overriding layers, and time had several clocks. Explaining an item's path required reading multiple implementations. The rebuild gives each decision one owner.

## System boundary

- **Upstream, outside this system:** acquire material, classify it, identify related subjects and publication time, and deliver it. Acquisition details are deferred.
- **This system:** dispatch through the library and pull mode, which closes due questions.
- **Tests:** stream stored items in publication order through the product's path, with replay time supplied to pull mode.

```text
                         Coverage-start reading (once, before the first item)
                                         ↓ starting figures
Upstream → Dispatch → Extraction → Thesis library ↔ Matching labels
                         │               ↑
                  read-only; groups   Pull mode: at day end, freeze
                                      and close due questions
```

| From | To | Content |
|---|---|---|
| Research universe | Upstream | Subjects and tracked categories |
| Research universe | Extraction | All themes for candidate selection in block 3 |
| Config | Extraction, library, coverage-start reading | Model settings version; library search result count |
| Coverage-start reading | Library | Once at coverage start, each open question's starting figure from the company's latest earnings report, linked to every question that read it (D363, D364) |
| Library | Extraction | The theses of the item's subjects and every theme thesis open at the start of the item's day, each with its takes line, in block 5 (D251, D264); no list of stored groups |
| Library | Matching labels | Comparison records for human labels and future smaller-model training |
| Dispatch, extraction, library | Human review | Unresolved items, proposed themes and repeated failures |

## Two modes

| | Incoming stream | Pull mode |
|---|---|---|
| Trigger | An item arrives | Day-end or scheduled interval |
| Initiator | Upstream delivery | System scheduling |
| Work | Read evidence/candidates and associations, preserve associations while matching identity, rejudge changed inputs in one round after the day's last item, the day passed in (D63), under library rules | At the end of each day, close the questions that are due at their rung; re-judge nothing (D356) |
| Calendar | Never reads it | Sole time-driven module; receives “now” explicitly |

## Principles

1. Start from theses. Their needs determine what to read and retain; do not build a financial-number warehouse first.
2. A thesis is a judgement; evidence records who said what in which item. Only incoming information creates evidence. Theses cannot prove each other.
3. Retain sources for every thesis, evidence item and information-triggered change, including the location in the original.
4. The stream is driven by incoming information, not the calendar. No input means no stream work; pull mode owns time.
5. Dispatch sequence determines order. Read earlier sequences plus the item's own writes (extraction reads the theses open at the start of the item's day, D251), with results equivalent to serial processing. Append knowledge without rewriting history. Store a late older statement as one more piece with its actual date, never as revising a newer one (D202); accept newly learned matters with their actual dates.
6. The research universe alone chooses subjects and categories. Upstream supplies only that scope; process every supplied item.
7. At matching time, open one thesis per subject and focus, with separate current/next-year numeric periods; manual reopening is excluded. D155 governs the POC's bounded code-owned identity. Search finds comparisons, not final identity. Resolve an evidence item's thesis before searching within it.
8. Fix questions and ladders in advance, and freeze the state when due. Rungs are verifiable outcomes. Append records and retain closed theses; the writer retires no evidence (D202).
9. Do not guess unresolved identifiers or rules; use human review.
10. Do not copy whole source material into the library. Retrieve it from the team's source store by ID.

## Glossary

Use one term per concept in the maintained design. `docs/check.py` checks terminology in the relevant page data and PRDs. Historical quotations, old source records and identifiers keep their original text. English replaces the previous Chinese presentation under D163; it does not rename stored identities.

| Term | Meaning | Avoid |
|---|---|---|
| Research group | Theses organised around a continuing business process; association is decided during extraction under the library contract | Treating a group as an overarching investment thesis |
| Admission reason | The one of four reasons a candidate thesis may open (D184): a main driver, an industry aggregate, a policy stage, a binding obligation; the answer states it as opens_as | Opening reason |
| Item | One upstream unit processed by classification, dispatch and extraction | Using file for every kind of item |
| File | Text-form source such as earnings, a report or news; qualify filesystem files as data/configuration files | Confusing source form with category |
| Table data | Fixed-field information; one release, such as a 13F or statistical release, is one item | Treating every cell as an item |
| Source material | Raw upstream material before classification | Calling excluded material an invalid item automatically |
| Form | Text or table | Using it for genre |
| Genre | Transcript, notes, memo, report, slides, article, letter or post | — |
| Filing | Formal submission to a regulator, exchange or court; SEC filing where applicable | SEC document as a category |
| Filing code | 10-K, 8-K, DEF 14A, etc. | Table code |
| Category | One of T1–T16 | Category type |
| Classification result | A category, duplicate merge, not source material, or invalid | Assuming every item has a category |
| Metadata | Supplied classification result, form, subjects, publication time and other attributes | — |
| Related subject | Company, cryptocurrency, commodity or theme identified for the item; it need not be in our universe | Equating company with stock |
| Subject identifier | Typed CIK, ticker, registered company name, cryptocurrency/commodity symbol or theme ID | One untyped subject code |
| Author | The party responsible for content; distinguish named individual and speaker | Treating delivery channel as author |
| Author type | Company, media, analyst, official or individual; author table then channel default | Category type |
| Publication time / publication day | Public-release timestamp / its New York date | Receipt time as publication day |
| Upstream ID / sequence number | Stable upstream version identity / dispatch-owned arrival order | Dispatch serial number |
| Original item | The item a duplicate merges into | — |
| Invalid | A classification result with a reason | Mixing it with excluded source material |
| Human review pool | Unresolved matters awaiting a person | Unqualified review pool |
| Dataset / data interface | Registered collection of table data / access channel | Confusing either with category |
| Prompt template / prompt / upload template | Shared five-block structure / assembled category instructions / upload table format | Unqualified template |
| Role | Senior hedge-fund analyst in prompt block 1 | Identity, which names a record or subject |
| Takes line | The code-written sentence under each open thesis in block 5 saying what its file holds (D254, D259, D264) | — |
| Thesis / candidate thesis | An immutable question, ladder and due date / extraction's proposed uncovered question, including personal-memo judgements | Calling every quoted opinion a thesis; naked candidate where ambiguous |
| Opinion | An author's, analyst's or media commentator's view | Confusing it with a stored thesis |
| Statement | What a source party says | — |
| Asset thesis / theme thesis | Tradable subject with business-impact rungs / theme with outcome-labelled rungs | Company view, object view, theme view |
| Focus | The quantity and year or event the thesis concerns, alongside its subject | Thesis driver |
| Ladder / rung | Exhaustive, non-overlapping outcomes: five, or two for yes/no | Fixed five-rung ladder; old verification-condition design |
| Due date | When the debate can resolve; a number's publication day | Expiry bucket |
| State | Our current rung judgement; not yet judged before a memo thesis first receives evidence | A second parallel state |
| Conclusion | State plus reasons; may change through key facts/numbers even within one rung | Equating changed conclusion with changed score only |
| Idea confidence | An Idea's weighted thesis assessment displayed on a 0–100% scale; the Idea service specification owns its calculation | Treating the index as a calibrated outcome probability |
| Trigger card | A frontend condition comparing an Idea's displayed confidence with a chosen percentage; the frontend specification owns its controls and status | Treating a met condition as an executed action |
| Action card | An editable frontend plan preview beside the Trigger, with a separately dated price chart; the frontend specification owns its fields | Treating a preview as an executable order or a connected wallet |
| Freeze | Preserve the current state and reasons at the due date, then close | A separate confirmed/falsified verdict in the current design |
| Unavailable answer / pending publication | Settled by D356: a question whose result is still unknown on its due day closes at its state; nothing waits for the result | Treating a question as waiting for its result |
| Evidence tier | Fact, party statement, third-party view or rumour; the judgement weighs each by tier and novelty in its forecast of the outcome (D260) | Mixing tiers with thesis kinds |
| Link | Evidence linked to a thesis, with its judgement-specific push | Treating push as intrinsic to evidence |
| Theme block | The open, judged theme theses shown to an asset thesis's judgement, one to all; the judgement states each theme's push on it | Theme context, macro block, theme dependency |
| Search / comparison list | Find plausible matches / top N shown to matching | Treating search ranking as identity |
| Open / closed | The lifecycle switch; only open theses update; closed theses remain searchable | Active thesis, inactive thesis |
| Repeat / replace / new evidence | Matching's three evidence decisions: the same claim, stored as its own piece with the pair recorded (D204) / a changed later version of the same statement or number, stored beside it as a revision (D202) / another event, period or speaker | Counting repeats as independent evidence |
| Revision | The pair a replace decision records: the later piece revises the earlier and both stay in force; the writer retires nothing (D202) | Deleted evidence; a replaced piece that no longer counts |
| Dependency | A thesis reads another's conclusion with a specified direction; no cycles | Premise in the current design |
| Succession / chain | Next period of the same focus / its ordered sequence; evidence revisions also form chains | Confusing succession with dependency |
| Matching / matching record | Decide destinations and retain inputs, answers, checks and writes | Inferring identity solely from similar wording |
| Jev / collision judge | The default matching engine, whose relations and scores are opinions code turns into decisions (D169, D201) / the generative call that answers the analyst's question for a candidate whose list holds a thesis of its own subject and measure, its verdict replacing Jev's (D190, D258) | One general-purpose model call deciding all matching |
| Merge | A candidate joins an open thesis or a part of it, inheriting its ladder and due date | Rewriting the target's identity |
| Source reference | Upstream ID, category, publication day, location and quote/cell | — |
| Original source | Who first said it and when; used for independence and revision ordering | Counting each retelling independently |
| Standalone summary | Evidence readable without its source; used by matching and rejudgement | — |
| Duplicate check | Proposed scheduled consolidation of duplicate open theses; not yet approved | Treating it as implemented |
| Rejudgement / round | Recompute from the evidence in view and dependencies / the day's one judging round, after its last item (D63) | Incremental score arithmetic; a round per item |
| Evidence in view | What a judgement reads: the arrivals since its fifth most recent judgement and the basis its last ten judgements cited; the rest stays in force, carried by the previous conclusion (D198) | All evidence in force as what a judgement reads |
| Matching labels / smaller model | Human-labelled destinations / future faster model trained from them | Assuming labels already provide acceptance |
| Code | Programmed rules, distinct from model judgement | — |
| Family / group | Five classification families / twelve theme-library groups | Calling theme groups categories |
| Frozen design | A decided module version; changes need a new decision | Confusing design freeze with a frozen thesis state |
| Starting figure / coverage-start reading | The figure a question's quantity stands at in the company's latest earnings report, recorded once when coverage starts / the step that reads it, after the seeds and before the first item (D363, D364) | Baseline figure; re-reading restated figures on the daily path |

## Modules

See the [PRD index](README.md) for files and status. The universe defines scope; classification labels; Config selects settings; dispatch routes; extraction reads; the library matches, stores and rejudges; matching labels collect supervision; pull mode owns time and closes questions at their due day, with no separate final verdict (D356); human review receives unresolved matters.

## Compared with the old system

| Aspect | Old system | Rebuild |
|---|---|---|
| Input | Date-driven pulls | Incoming upstream items |
| Processing | Daily batches | Item sequence order |
| Categories | Separate definitions in nine modules | One set of 16 |
| Scope | Overriding configuration, arguments and presets | Research universe |
| Time | Several clocks | Publication day in the stream; supplied “now” in pull mode |
| Sources | Local copies | Retrieve from team storage by ID |
| Reports | Repeated downloads and stored individual numbers | Whole-item reading into theses and evidence |
| Theses | Accumulation, ambiguous rewritten identity and no exit | Fixed question/ladder/due date, identity matching and due-date freezing |

## Not yet designed

Human-review handling; upstream acquisition/classification and return notifications; category prompt wording; library open questions, particularly analyst-level thesis granularity; settlement figures for closed questions (prices, filings). A grouping requirement is not evidence that its implementation has passed acceptance.

## Related decisions

- D10/D17: classified stream and dispatch as the sole entry. D12–D14: no internal clock; separate stream and pull mode.
- D16/D18/D19: human review, universe-owned scope and first module freezes.
- D25–D28: one extraction module, shared analyst role, central library, sourced whole-item reading and report ingestion.
- D29/D30: historical final-verdict and disagreement design, revised by D38/D54 and retired by D356 (closing at the due day is pull mode's).
- D31/D32: sequence order, one queue per thesis, whole table releases and no separate filing XBRL ingestion.
- D33–D37: read-only extraction, SEC publication day, extraction review, glossary and first-version freezes.
- D38–D42: rebuilt thesis structure, library intake/history, matching labels, aligned module boundaries and binary ladders.
- D44/D45: initial model-owned matching; separate proposals from decisions; similar questions remain distinct. D155 later bounds code-owned identity in the POC.
- D46/D49: one state, verifiable ladders, normal ingestion of decisive information, publication-relative years and top-N search.
- D47/D48: consistent terms and complete comparison paths; library freeze.
- D51: changed-input rejudgement, explicit conclusion change, dependencies chosen in matching, seven intake steps, no consensus calculation.
- D52/D53: plain terms and full context review without added rules.
- D54–D57: due-date freezing without a separate result or wait, manual universe maintenance and one open/closed switch.
- D58–D60: clarify directions, waiting, due-date scope, manual operations, subject identification and personal memos; freeze the foundation except final verdict/pull mode.
- D149: extraction-owned research-group association. D155: current identity and reference-list changes.
- D163: English for maintained product text and documentation; historical evidence retains its original text.
