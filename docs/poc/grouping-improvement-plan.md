# Organising theses during extraction: improvement plan and verification

Updated October 25, 2026. Governing decisions: D149, D154 and D155, with later experimental results below. The original text and detailed historical refresh are retained in the [October 25 snapshot](grouping-improvement-plan-history-2026-10-25.zh.md).

The goal is for a second article to continue the research left by the first. Fewer questions alone do not establish success. Rubin shipments and SK factory deployment are separate questions in one business process; a launch is not a shipment. A reference list helps the analyst begin, but an unlisted Ohio project can still warrant a thesis and a new research group.

## Scope and completion

This plan covers extraction, thesis identity, writing, sequential reads of existing research, and their documentation and verification. Existing source checks, evidence matching, ladders, rejudgement and dispatch contracts remain. Idea, frontend, trading, classification, final verdict and pull-mode rules are outside this grouping slice. Do not rewrite historical databases or run the full half-year corpus under this plan.

Generating an overarching investment thesis is separate. A research group organises distinct questions; it has no score and does not automatically create dependencies.

Report omissions, false code refusals, duplicate questions, false merges, missing/wrong memberships, lost evidence and cost separately. Zero duplicate keys proves only that those keys are unique. Label stored-answer replay, code tests and fresh model results distinctly.

## Diagnosed classes

Sources: `poc/data/keyed-2026-10-25/archive-T2.sqlite` and eight `views-2026-10-25-v15-*.sqlite` ledgers. Reproducible checks are in the repository; the original read-only investigation used temporary directory `hivemind-grouping-review-20261025-71uzwtm8`.

| Class | Census and mechanism | Decisive proof and limit |
|---|---|---|
| Reference list used as a gate | T4c has 23 `candidate_outside_watch` records. `sift` drops unlisted questions before source checks; original answers remain in the archive | Remove only this gate and replay all other checks. This cannot recover questions the model never wrote |
| Multi-year calendar period changed to one fiscal year | One explicit case among 315 answers and 152 candidates: call 261's 2025–2027 period became February 2024–January 2025, retained in three experimental ledgers | Preserve 2025-01-01 through 2027-12-31. Convert only full-match single-year forms |
| Launch treated as shipment | Search, equality and conflict checks omitted `event_type`; no observed instance in the eight ledgers | Change only a real shipment candidate's event type to launch; it must cease to be an exact match and forced merging must be refused. This is a constructed regression case, not an observed semantic-error count |
| Broad alias rewrites scope | Two of 152 raw candidates match multiple scopes; one survives other checks. Call 584's AI hyperscalers became five hyperscalers | Exact names first; preserve actual free scope. Aliases suggest relevance, not automatic identity |
| Duplicate question within one answer | No observed instance in eight ledgers; duplicating a real first-article revenue candidate passes checks and writes twice | One thesis per complete code-owned key, retaining evidence from both candidates. Uncertain free scopes are not automatically equal |
| Same-day research invisible | Old `replay.pre_extract` reads a day-start snapshot for parallel extraction. Later identity matching cannot supply extraction-owned grouping | D159 fixes sequential reads: the second item sees the first item's committed work. Default grouping itself remains unimplemented |
| Grouping absent from default pipeline | No group handoff in the adopted schema, handovers, writer or database; D154 records this gap | Trace raw associations to stored members and evidence reads, then separately judge whether the model's associations are right |

Count one source answer retained in three ledgers as one source case and three stored outcomes. Calls 261 and 584 are known census controls.

## Sequence and stopping rules

**Current result:** D162's [two-step comparison](../../poc/reports/2026-10-25-source-first-01/results.md) failed end-to-end acceptance. All six sequences completed. Better content selection did not eliminate invalid ownership, wrong groups, a date-based merge override or an inaccurate numerical summary. No experimental role or grouping path was promoted. D163 English conversion is now the active task; [current state](../CURRENT_STATE.md) governs what happens next.

| Step | Delivery | Verification and stop |
|---|---|---|
| A: Baseline | Source-file hashes and read-only census of answers/ledgers | Record before changing; no model calls or old-data writes |
| B: Identity and reference list | Reference-only list, full-match year conversion, exact scopes, event type in identity, same-answer coalescing | Real cases flip; whole stored-answer replay; decisive scratch mutants; full suite once |
| C: Grouping handoff experiment | Extraction returns associations in the same reading; code stores them for the next item | Small isolated real-news comparison; retain agreed Rubin/customer positives and PC/other-customer negatives. Group names or counts are not correctness. Failure stops promotion |
| D: Sequential integration | Schema, prompt version, groups/memberships, atomic writes, resume and read-only queries | Same-day continuity; duplicate-free resend; no partial writes; evidence through actual links; failure cannot complete the day |
| E: Fixed-configuration acceptance | Three fresh samples per arm on identical inputs | Read every answer and refusal. Separate extraction from grouping error; one good sample cannot hide two failures. Retain failed results and criteria |

B can ship independently of C's model quality. Field completeness does not establish D while C fails. D159 independently fixed the pre-existing read-order defect: each item writes before the next extracts, and a failure stops replay. Its 214 passing tests do not establish default membership storage or grouping quality. See the [full-path diagnosis](../research/2026-10-25-pipeline-replay.md).

## Step B contract

### Reference lists and periods

A reference list supplies example measures and scopes. Every candidate still passes the existing year, source, subject and ladder checks. Being unlisted is not a refusal reason. The unlisted marker is recomputable from the original answer and list; it creates no approval process.

At D155, single-year conversion accepts complete `YYYY`, `FYYYYY`, `FY YYYY`, `YYYY年` or `YYYY财年`, case-insensitively. Complete `YYYY自然年` or `CY YYYY` is a calendar year. Other forms retain their valid original date range; never extract the first year and reinterpret it as a fiscal year. Dates must exist and start must not follow end. These literal legacy inputs remain documented for compatibility; D163's English equivalents require the shared period contract before activation.

### Scope and identity

Use a reference scope spelling only when the normalised complete name matches. A partial alias indicates possible relevance. For normally unqualified measures, remove only a complete redundant expression: empty scope, GAAP/non-GAAP, the measure's own name, or their combination. Do not erase Reality Labs from operating loss or cash from capex. Each occurs once in the raw-answer census and reaches this path after the list veto is removed.

One pure key comparison serves post-search identity checks and writing: subject, measure, scope, start/end, accounting basis, unit and event type. Automatic equality requires every component to agree and a code-owned scope. Vague `other` measures/event types do not establish it; `n/a` is not a wildcard. Search may retrieve an unknown basis for model comparison without authorising a merge.

Coalesce same-answer new candidates only on that complete automatic key. Keep every candidate-to-thesis mapping and all evidence; different events or periods remain separate. Use the first candidate's question and ladder in input order, deduplicate dependencies after resolving final IDs, and refuse the whole plan for conflicting succession targets, conflicting directions on one dependency or a resulting cycle.

The shared plan runs before `matching.check` succeeds, so conflicts use its existing retry path. The writer repeats the same check inside its transaction. Do not leave a cached answer permanently failing only at writing. If an automatically identical thesis already exists but the plan still asks to create one, refuse and roll back; identity matching must decide again without bypassing evidence comparison. This check must not reject distinct free scopes that still require model judgement.

### Historical records and atomic writing

New keys carry code-generated contract version 2. Old keys and handovers without that version gain no automatic-merge authority from an old `scope_source=watch/none`. They remain semantic comparison candidates, including when an old period or scope is wrong. Do not backfill old values.

Database opening and the write boundary share missing-column handling for version, `scope_source` and rung bounds. It also covers an already-open connection restored from an old backup. Read functions do not alter schema. Unkeyed old ladders retain their original response shape.

The writer opens a savepoint inside an existing transaction, or obtains the SQLite write lock first. The round commits successful writes with the completion marker. On error, roll back to the savepoint and record the failure; previously persisted handover/matching records remain available for resume. No partial thesis write survives.

Replay stops on failure and does not mark that day complete. Resume retrieves the original sequence and handover from the processing record.

### State × event

| State | Event | Transition, writes and time |
|---|---|---|
| Before extraction | Listed or unlisted answer | Same source checks; use the item's publication day and supplied context, never wall-clock time |
| Before extraction | Fiscal/calendar/multi-year period | Convert / preserve calendar year / preserve valid original range; invalid dates refuse the candidate |
| Extracted | Initial or corrected matching answer | Same identity comparison and target checks; retries do not relax them |
| Matched | Same or different complete key in one batch | One thesis with all ID mappings, or distinct theses; use the current dispatch sequence |
| Writing | Existing identical key, exception or crash | Roll back the whole write; no completion marker; resend retains sequence |
| Written | Same input resent | Dispatch skips it; no duplicate write |
| Resuming | Changed configuration or corrected input | Do not reinterpret a persisted handover; corrected input receives a new ID |
| Different inputs | Later day, two subjects or two writers | Key includes subject/period; existing-key check is transactional; a competing failure uses normal resume |

### Value × writer × reader

| Value | Writers and inputs | Readers and contract |
|---|---|---|
| Scope, period | Raw model answer through `sift`; old handover; historical import | Matching, writer, `view_keys`, service. Correct new answers; do not silently migrate old values |
| Equal key | Shared pure function over candidate or stored key | Matching and writer. Broader search does not change equality |
| Candidate-to-thesis mapping | Writer creates/coalesces; matching supplies old targets | Evidence, dependencies, metrics. Count unique stored thesis IDs |
| Reference list | Universe configuration | Prompt, exact scope names and search hints; no candidate veto |
| Completion | Round and dispatch | Resume and daily metrics; commit with successful writing only |

### New path × existing checks

| Path | Required checks |
|---|---|
| Unlisted question | Schema, subject resolution, quarter/year, valid dates, ladder, source quote, surviving evidence and allowed matching targets |
| Free scope | Same checks; model comparison, no automatic equality |
| Same-batch coalescing | Every evidence check, cycle check after ID resolution; candidate itself never becomes evidence |
| Write rollback | Retain handover/matching for resume; no partial thesis, evidence or completion marker |

### Prior decisions

D149 reserves matching for thesis/evidence identity and dependencies; it cannot repair lost extraction-time association. D154 says, “the key is a necessary, not a sufficient, condition of identity.” Aliases and vague values therefore cannot authorise equality. D155 changes D154's list veto and alias rewriting into references; date, event and same-batch defects are implementation corrections. Alex's review/fix request superseded D152's division of work; preserve Claude's concurrent changes.

## Steps C/D: design boundary

The order is dispatch → read committed research → whole-item extraction with associations → identity matching → atomic storage → next item.

Retrieve available research groups across the global library, including other companies. A reference measure name is not automatically a business-process group. Show existing groups' names, scope and recognisable member questions. New groups declare name and scope; create one only when an accepted, actually written thesis uses it. Group IDs are stable; equal names do not prove identity. Groups have no automatic hierarchy, and relatedness does not imply dependency.

C must validate whether name selection or explicit references work from raw answers; do not declare either representation reliable in advance. Before D, complete the exact fields and transition tables, then obtain a read-only design review.

D's state table must cover the first empty-library item, a second same-day item, cross-company reuse, evidence-only input, skip/merge/succession, invalid references, interrupted writes, resend, configuration changes, historical reads and concurrent writers. Its value table must cover declarations → references → final thesis IDs → memberships → evidence reads → later extraction. Matching and rejudgement do not manufacture evidence from membership.

## Cost and measurement

- B: zero model calls; replay all stored extraction answers and report candidates judged, refusal reasons and affected IDs.
- C: finish the harness/input list and run `scripts/preflight.py` first. At most three paired small-news samples; register inputs, calls and spending independently. Do not reuse or raise a previous cap. A defective measure is reported before paid resampling.
- D: real temporary SQLite records; fake only the external model service. Record each scratch mutant's decisive failure.
- E: retain every raw answer, check result and final thesis/member/source. Report each case, not only averages. A small experiment does not establish large-library recall or market-wide cost.

## Measured history

These are historical measurements, not new D163 acceptance results. Detailed logs and the original module-by-module refresh remain in the linked snapshot and report directories.

| Work | Result |
|---|---|
| A census | 315 answers, 152 candidates, 806 evidence items. Old checks retained 92 candidates/668 evidence items. Removing list-only refusal retained 121/691: all 29 restored at extraction, not a claim that every candidate resolves, writes or is semantically correct |
| Same-day snapshot census | 195 of 255 T4c parallel extractions had earlier same-day new theses. Exposure to missing context, not 195 observed grouping errors |
| B implementation | `poc-v16`/`role-v5`, reference-only lists and version-2 key trust. Replay remains 121 candidates/691 evidence items; calls 261/584 corrected, Reality Labs/cash qualifiers retained; old ledgers untouched |
| B checks | 28 targeted and 168 full tests passed in Python 3.10.10. System Python 3.9 first failed collection because MCP was absent; log retained. Full checks exposed three old-backup missing-column and two old-response empty-bounds compatibility defects, fixed at the write/read boundaries |
| B mutants | Ten caught. Removing coalescing made the valid batch fail the writer's identical-key refusal; its traceback confirms the intended failure |
| B prompt audit | Same first article and empty context: system/user 8,037 → 8,006 characters; local `o200k_base` estimate 3,417 → 3,388 tokens. Zero fresh model calls |
| D156 measurement repair | Four old third-article answers have zero candidates and 3/2/2/1 evidence items. The old 4/4 relationship score only measured retained earlier links; six holdouts were unstarted. New membership was unexercised, not passed; empty candidates alone do not establish an omission |
| D157 | 20 calls, estimated $0.373923. Only one of three retained the analyst's project-risk link, with other wrong groups/links still present. Failed business acceptance. Missing legal-ID schema constraints were repaired with stored answers, not resampling |
| D158 | 326 answers replayed: one NAVER event and three evidence items restored by fixing the event/year check; Ohio unchanged. First fresh control timed out after 180.342 seconds; others unstarted. Retained $0.105535 reservation for unknown usage; 211 tests passed, no semantic acceptance. Its proposed automatic continuation was superseded by D159 |
| D159 | Sequential extraction after committed writes; 214 tests passed and old parallel behavior fails the order check. Default grouping still absent |
| D160 | Six sequences, 36 calls. Two project questions retained/grouped 3/3, but complete risks and amount meanings only 2/3. Failed full acceptance; later articles had no new candidates, so the older identity split was unexercised |
| D161 | Six sequences, 36 calls, estimated $0.497585. Criticism 3/3 versus control 2/3, first-article cost 1/3 versus 0/3; each arm misgrouped one sequence under Rubin. Failed; 217 tests passed |
| D162 | Six sequences, 45 calls, estimated $0.6928525. First-article cost selected 3/3 versus control 1/3, stored only 2/3. Invalid ownership, wrong grouping, date-based merge override and inaccurate numerical summary remain. Failed; 227 tests passed |

The [grouping acceptance contract](../research/2026-10-25-grouping-acceptance.md) owns the units, six judgement layers, case cards and offline-check rules. Current work remains the single next task in CURRENT_STATE; none of these historical plans authorises another automatic paid run.
