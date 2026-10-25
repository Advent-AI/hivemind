# Build a fresh English thesis library

Decision: D163. Alex chose a fresh English library on October 25, 2026. Start with the original source documents and an empty ledger. Keep the existing Chinese library as historical evidence. This page owns the build sequence; the [English conversion plan](plan.md) owns language compatibility.

For example, an NVIDIA earnings call should produce an English question, its English outcome ladder and English evidence summaries directly. The exact quotation remains the sentence in the earnings call. A later Reuters article is compared with the theses already written by earlier items; it can add evidence, repeat an existing source, or propose another question.

## How the old library was made

1. The corpus harvesters collected filings, earnings calls, company releases, official material and news pages. `assemble.py` put original text, publication dates, source identity, categories, subject labels and copy links into `items.sqlite`. A provider summary alone was not an original article eligible for extraction.
2. The POC used the smaller `poc/data/items-window.sqlite`, not every item in the full corpus. Earlier NVIDIA company documents seeded the empty library from February 25 through July 23. The news replay began July 24. The initial source database included attachments subsequently marked as not material; `items-window-tags2-2026-10-24.sqlite` preserves the same source rows with corrected labels.
3. `testdb.feed` read original items and copy records in publication-day order, company material before official material before news within a day. `dispatch.route` applied its existing completeness, copy, category and research-universe rules.
4. Extraction read each original with the existing thesis context. It proposed complete questions and outcome ladders, plus evidence linked to existing or proposed theses. The role explicitly required Chinese generated text. Matching searched existing theses and evidence; writing stored the decisions, original quotations, source links, dependencies and successors in an append-only SQLite ledger.
5. Judgement wrote the state and its evidence-backed reasons. The final UI ledger has 234 item-labelled judgements before July 29; from July 29 it has 203 day-labelled and 28 item-labelled judgements. Daily judgement was introduced during this run, not a clean cutover covering every record from that date. Due theses were frozen and closed. This mixed cadence is historical, not the new build configuration.
6. The sealed August 15 ledger feeds the API by default. `mock_data.py` also exported it for the early UI; `mock_translate.py` translated display strings afterwards, retaining Chinese `condition_zh` fields to read score direction. That export did not turn the underlying library into English.

The UI ledger, later keyed trial ledgers and the latest adopted code are different things. The UI's sealed ledger was built with `poc-v2`; `poc-v16` incorporates later identity/reference fixes, and D159 changed replay to finish each item's writes before extracting the next. No default configuration currently implements D149 grouping.

## Selected inputs and stages

The first build uses the corrected, fixed POC source population in `poc/data/items-window-tags2-2026-10-24.sqlite`. It does not silently switch to the much larger `poc/corpus/items.sqlite`. `audit_library.py` records their actual sizes, selected input IDs, original-content hashes, route decisions and the difference from the UI library's source labels. Counts come from its output, not a hand-maintained target.

| Stage | Inputs | Result and exit condition |
|---|---|---|
| Prepare, free | Existing source databases and ledgers | Record source provenance and exact populations; inspect hash/date/body failures before any model calls. No source or old ledger is rewritten. |
| Complete English runtime, free | Adopted extraction/matching/judgement/Idea contracts | Activate new versioned English prompts only after canonical fields, complete request builders, periods, score orientation, source preservation and legacy reads pass their checks. Update preflight's request parsing and enum checks for English requests; its current Chinese-header parser cannot replay them. Keep provider/model/reasoning unchanged. |
| Small paired check, proposed | The first NVIDIA results package and a later update from the recorded source list | Compare fresh old-language and English calls, at least three samples per arm. Agree the semantic expectations and an explicit cost cap before launching. No cached answers as model controls. |
| Seed the English library | The 20 eligible earlier NVIDIA documents, in their existing chronological order | Write a new English ledger and call archive. Review omissions, duplicates, false merges, quantities, periods, citations and score direction. Stop on a failed registered acceptance. |
| Continue the same ledger | July 24–31 from the fixed POC source population | Exercise updates against existing English theses, repeated-source handling, replacements and daily judgements. Do not reset the ledger between days. |
| Extend and expose | August 1–15 after the smaller stages pass | Use a new search index and point the API/UI at the English ledger explicitly. Export directly; no display-translation job or dependency on `condition_zh`. |

The small comparison is proposed, not launched or registered by this document. Its exact source IDs, semantic reading and cap must be settled before it becomes an acceptance. A source inventory proves input identity and routing, not correct extraction. A translated prompt or passing schema is likewise not evidence of model quality.

Research reference lists remain hints: a topic outside a company's list can still be proposed. Preserving that D155 behavior is separate from supplying D149 research groups. The English baseline must not be presented as the finished grouping product. No failed two-step extraction arm is introduced through the language switch.

## Inputs, outputs and transitions

| State × event | Action and date |
|---|---|
| Preparation × original source read | Read SQLite with `mode=ro`; record existing input IDs, publication days and hashes. No model calls. |
| Preparation × missing database, empty selected stage, inconsistent body hash or invalid date | Refuse preparation; do not substitute another corpus or call the model to discover what failed. |
| Empty English ledger × first source | Use the source's publication day and dispatch sequence; propose English theses without importing old Chinese theses. |
| Populated English ledger × next source | Finish the preceding write first; read the resulting English thesis context, then extract and match. |
| End of day × changed theses | One dependency-ordered judgement round, then the existing due-date close step; record the completed day. |
| Running × crash/refusal | Retain raw answers and completed writes; use existing resume behavior with the same pinned source/configuration. No reset or fresh sampling disguised as resume. |
| Historical Chinese ledger × English build | Read only for comparison; never a target of the new run. |
| Staged acceptance × failure | Record the failed population and trace; do not continue into the larger stage or change the standard to pass. |

| Value × writer | Readers and contract |
|---|---|
| Source text, ID, date, source URI and hash × existing corpus | Extraction, original-quote checks, evidence source lookup, audit. Retain byte content and dates. |
| English question, focus, outcome conditions and summary × versioned model requests | Matching, ledger, service, UI. Canonical vocabulary follows the PRD; source quotations are exempt from translation. |
| Numeric bounds and period × extraction plus existing checks | Identity matching, succession, claim evaluation, chart orientation. Language must not change values or financial period. |
| Run configuration and source population × build operator | Replay and verification. Use explicit separate source, views, archive and index paths; do not inherit the old CLI's `poc-v1` or API's sealed-library defaults. |
| Preparation manifest × `audit_library.py` | Review and later run registration. It contains source references, not a second corpus or generated theses. |

| New path × old checks | Required evidence |
|---|---|
| English extraction against empty library | Same admission, quote, ladder, fiscal-period and identity checks; inspect all refusals. |
| English updates against existing English library | Recall of the right thesis plus correct merge/repeat/replace/new decisions; chronology preserved. |
| English-only API/UI | Same scores and numeric evaluations without Chinese fallback fields; complete bundles and source citations. |
| Old ledger read | Same source IDs, evidence, dates and scores; no writes or bulk translation. |

Prior decisions: D44 leaves question selection to the model without a count quota; D62 pins the provider/model; D63 sets daily judgement; D149 requires extraction-time association; D155 removes reference-list vetoes and defines identity checks; D159 establishes sequential extraction after writes; D162 failed and is not promoted; D163 selects English and a new ledger. These decisions are not changed by selecting a build population.

## Status

The source preparation is complete. New prompts remain staged. No English thesis has yet been generated, no model call has been made for this build, and the API/UI still point to the old library. Runtime conversion is the next implementation task.

The [final source manifest](../../../poc/reports/2026-10-25-english-library-01/source-manifest-v3.json) records exact IDs and hashes. Earlier manifests are retained; v2 added comparison of every original/corrected source row, and v3 measures historical judgement cadence. Regenerate with `python3 docs/research/2026-10-25-english/audit_library.py --out <new-absolute-report-path>`.

| Measured population | Result |
|---|---|
| Old UI ledger | 94 theses, 827 evidence records, 465 judgements; all 94 questions contain Chinese |
| Original/corrected POC source rows | 2,205 each; zero changes to input IDs, original text, source URIs, publication days or content hashes |
| Corrected POC versus full corpus | 1,634 versus 7,198 feed-flagged records; do not silently substitute the full corpus |
| Earlier seed | 20 records, all routed to extraction; original labels had admitted 31 |
| July 24–31 | 324 records: 239 extraction, 12 copies, 73 not processed by existing routing |
| August 1–15 | 377 records: 221 extraction, 18 copies, 138 not processed by existing routing |
| Selected source consistency | 721 records checked, zero applicable full-body/hash/date failures; five databases unchanged after reading |

The audit's real-filing positive control passes; disabling either its body-hash check or date check on a scratch copy is caught by the corresponding assertion. [Control results](../../../poc/reports/2026-10-25-english-library-01/audit-controls.json). Hash agreement proves that bytes match the recorded source, not that the collector obtained the right article or that its claims are true.

The [read-only preparation review](library-review.txt) reproduced the 721 ordered inputs and route decisions and checked recorded hashes. Its one finding was the overly broad historical July 29 daily-judgement claim. Directly querying the sealed ledger confirmed 28 item-labelled judgements from July 29, alongside day-labelled judgements; both current descriptions were corrected as recorded below. The review's source-list result remains the same in v3; v3 adds the independently checked cadence measurement.

The existing preflight was also run once on `keyed-2026-10-25/archive-T2.sqlite`, the corrected POC sources and the T4c ledger: 315 stored extraction answers; 122/152 candidates and 694/806 evidence items retained; 155 matching records with two refused records; 68 prompt-enum checks with no missing values; 40 open keyed theses with no duplicate exact keys. It reports final-state replay, not the original historical state. These are old-language baseline results, not English acceptance. The zero schema-failure population is unexercised. The existing stored-answer omissions/refusals remain visible and are not declared fixed.

## Reasoning refresh for this slice

Read in D22 order: universe → classification → Config → dispatch → extraction → library → final verdict → pull mode → human review → system. No governing product behavior changes in this preparation slice. The universe and classification remain the selected POC versions; original sources and their dates stay intact. Config still owns versioned model settings. The audit exercises existing dispatch rather than inventing a selection rule. Extraction and the library retain their recorded language and grouping prerequisites. Final verdict, pull mode and human-review handling remain unchanged. The system's source/ledger separation still holds.

Fixed documentation inconsistencies: the migration plan and current state no longer call Alex's library choice pending; the pipeline overview now points to this source/build plan; input readiness is explicitly separated from runtime and model readiness. Both current descriptions of the historical July 29 cutover overstated it as fully daily; the ledger's actual item/day counts replace that claim here, and the pipeline overview links to this measurement. The build plan does not turn the UI's old ledger or a later trial ledger into the current implementation contract.
