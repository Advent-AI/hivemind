# System overview

> Status: foundation frozen except final verdict and pull mode. Universe, classification, Config, dispatch, extraction and human-review intake froze on October 18, 2026; the library and matching labels on October 20; the full review completed October 22. D149 adds extraction-time grouping, not yet integrated into the default pipeline. English edition: October 25, 2026 (D163).
> Design page: `docs/system-design.html` → New → Open system PRD. Recorded decisions take precedence over this document.

## Purpose

Maintain a thesis library: create theses, update their judgements and close them when due. Upstream continuously supplies classified information. Extraction reads each whole item as a senior hedge-fund analyst, alongside existing theses, and returns linked evidence and candidates with research-group associations, declaring new groups where needed. The library preserves those associations and compares identity: merge, succession, new thesis or skip; repeat, replace or new evidence. Each thesis has a question, ladder and due date. Evidence moves its state, which freezes when due.

D149 requires organisation during full-text reading, with associations included in extraction output. See [the library's grouping contract](06-views.md#research-groups-associate-during-extraction) and [extraction's responsibility](05-extraction.md#determine-associations-during-extraction). Rubin shipments and SK factory deployment are separate questions in one continuing business process. Default integration is pending; the [improvement plan](../poc/grouping-improvement-plan.md) records implementation gaps, D155 identity changes and validation work.

## Why rebuild

The old system pulled dated batches. Category definitions existed in nine modules, configuration used five overriding layers, and time had several clocks. Explaining an item's path required reading multiple implementations. The rebuild gives each decision one owner.

## System boundary

- **Upstream, outside this system:** acquire material, classify it, identify related subjects and publication time, and deliver it. Acquisition details are deferred.
- **This system:** dispatch through the library, final verdict and pull mode.
- **Tests:** stream stored items in publication order through the product's path, with replay time supplied to pull mode.

```text
Upstream → Dispatch → Extraction → Thesis library ↔ Matching labels
                         │               ↑
                  read-only; groups   Pull mode: scheduled review,
                                      freeze and close due theses
Final verdict: earlier draft; decide its role with pull mode
```

| From | To | Content |
|---|---|---|
| Research universe | Upstream | Subjects and tracked categories |
| Research universe | Extraction | All themes for candidate selection in block 3 |
| Config | Extraction, library, final verdict | Model settings version; library search result count |
| Library | Extraction | Open subject theses and their dependencies: question, focus, due date and links; available groups under the library contract, in block 5 |
| Library | Matching labels | Comparison records for human labels and future smaller-model training |
| Dispatch, extraction, library | Human review | Unresolved items, proposed themes and repeated failures |

## Two modes

| | Incoming stream | Pull mode |
|---|---|---|
| Trigger | An item arrives | Day-end or scheduled interval |
| Initiator | Upstream delivery | System scheduling |
| Work | Read evidence/candidates and associations, preserve associations while matching identity, rejudge changed inputs under library rules | Overall review/update; freeze and close due theses; remaining design deferred |
| Calendar | Never reads it | Sole time-driven module; receives “now” explicitly |

## Principles

1. Start from theses. Their needs determine what to read and retain; do not build a financial-number warehouse first.
2. A thesis is a judgement; evidence records who said what in which item. Only incoming information creates evidence. Theses cannot prove each other.
3. Retain sources for every thesis, evidence item and information-triggered change, including the location in the original.
4. The stream is driven by incoming information, not the calendar. No input means no stream work; pull mode owns time.
5. Dispatch sequence determines order. Read earlier sequences plus the current round's own writes, with results equivalent to serial processing. Append knowledge without rewriting history. Log obsolete late statements; accept newly learned matters with their actual dates.
6. The research universe alone chooses subjects and categories. Upstream supplies only that scope; process every supplied item.
7. At matching time, open one thesis per subject and focus, with separate current/next-year numeric periods; manual reopening is excluded. D155 governs the POC's bounded code-owned identity. Search finds comparisons, not final identity. Resolve an evidence item's thesis before searching within it.
8. Fix questions and ladders in advance, and freeze the state when due. Rungs are verifiable outcomes. Append records and retain closed theses and replaced evidence.
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
| Thesis / candidate thesis | An immutable question, ladder and due date / extraction's proposed uncovered question, including personal-memo judgements | Calling every quoted opinion a thesis; naked candidate where ambiguous |
| Opinion | An author's, analyst's or media commentator's view | Confusing it with a stored thesis |
| Statement | What a source party says | — |
| Asset thesis / theme thesis | Tradable subject with business-impact rungs / theme with outcome-labelled rungs | Company view, object view, theme view |
| Focus | The quantity and year or event the thesis concerns, alongside its subject | Thesis driver |
| Ladder / rung | Exhaustive, non-overlapping outcomes: five, or two for yes/no | Fixed five-rung ladder; old verification-condition design |
| Due date | When the debate can resolve; a number's publication day | Expiry bucket |
| State | Our current rung judgement; not yet judged before a memo thesis first receives evidence | A second parallel state |
| Conclusion | State plus reasons; may change through key facts/numbers even within one rung | Equating changed conclusion with changed score only |
| Freeze | Preserve the current state and reasons at the due date, then close | A separate confirmed/falsified verdict in the current design |
| Unavailable answer / pending publication | Proposed pull-mode cases, not yet approved | Treating proposals as implemented states |
| Evidence tier | Fact, party statement, third-party view or rumour; only facts can establish the outcome | Mixing tiers with thesis kinds |
| Link | Evidence linked to a thesis, with its judgement-specific push | Treating push as intrinsic to evidence |
| Search / comparison list | Find plausible matches / top N shown to matching | Treating search ranking as identity |
| Open / closed | The lifecycle switch; only open theses update; closed theses remain searchable | Active thesis, inactive thesis |
| Repeat / replace / new evidence | Same existing statement / a later statement superseding it / another event, period or speaker | Counting repeated references as independent evidence |
| Replaced | Historical evidence no longer in force, kept for traceability | Deleted evidence |
| Dependency | A thesis reads another's conclusion with a specified direction; no cycles | Premise in the current design |
| Succession / chain | Next period of the same focus / its ordered sequence; evidence replacement also forms chains | Confusing succession with dependency |
| Matching / matching record | Decide destinations and retain inputs, answers, checks and writes | Inferring identity solely from similar wording |
| Merge | A candidate joins an open thesis or a part of it, inheriting its ladder and due date | Rewriting the target's identity |
| Source reference | Upstream ID, category, publication day, location and quote/cell | — |
| Original source | Who first said it and when; used for independence and replacement ordering | Counting each retelling independently |
| Standalone summary | Evidence readable without its source; used by matching and rejudgement | — |
| Duplicate check | Proposed scheduled consolidation of duplicate open theses; not yet approved | Treating it as implemented |
| Rejudgement / round | Recompute from evidence in force and dependencies / all changes from one item | Incremental score arithmetic |
| Matching labels / smaller model | Human-labelled destinations / future faster model trained from them | Assuming labels already provide acceptance |
| Code | Programmed rules, distinct from model judgement | — |
| Family / group | Five classification families / twelve theme-library groups | Calling theme groups categories |
| Frozen design | A decided module version; changes need a new decision | Confusing design freeze with a frozen thesis state |

## Modules

See the [PRD index](README.md) for files and status. The universe defines scope; classification labels; Config selects settings; dispatch routes; extraction reads; the library matches, stores and rejudges; matching labels collect supervision; pull mode owns time; human review receives unresolved matters. Final verdict remains an earlier draft.

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

Human-review handling; upstream acquisition/classification and return notifications; category prompt wording; library open questions, particularly analyst-level thesis granularity; final verdict and pull mode beyond the decided freezing behaviour. A grouping requirement is not evidence that its implementation has passed acceptance.

## Related decisions

- D10/D17: classified stream and dispatch as the sole entry. D12–D14: no internal clock; separate stream and pull mode.
- D16/D18/D19: human review, universe-owned scope and first module freezes.
- D25–D28: one extraction module, shared analyst role, central library, sourced whole-item reading and report ingestion.
- D29/D30: historical final-verdict and disagreement design, revised by D38/D54.
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
