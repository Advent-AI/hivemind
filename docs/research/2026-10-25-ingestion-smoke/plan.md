# Three-document ingestion comparison

Alex asked to continue after the isolated API smoke (D173). This next slice runs the product's replay entry point on independent scratch ledgers. It does not enable production concurrency, change a prompt, change a gold, or implement the asynchronous OpenAI Batch API.

## Source and fixed comparison

Use the complete stored July 24 documents, unchanged:

1. `nvidianews:sk-group-and-nvidia-expand-strategic-partnership-across-ai-factories-and-next-generation-memory`
2. `nvidianews:naver-nvidia-and-brookfield-to-expand-koreas-national-ai-factory-infrastructure-buildout`
3. `nvblog:ai-summit-korea-partners-and-nvidia`

The baseline is the historical Jev ledger strictly before sequence 21, the start of July 24. It contains no July 24 writes. The new source database contains only the three selected whole rows, preserving their metadata and order. This is a selected-subset stress test, not a replay of the entire day. The old Rubin test fixture contains excerpts and is not used as live source material. Source navigation/footer text is preserved too; no new cleaning rule is introduced.

The snapshot call explicitly excludes sequence-zero rows: those audit records have no order within the dispatch sequence. Census of both stored ledgers found 31 sequence-zero processing records each, all dated July 24 or later, plus 6/13 sequence-zero review-pool records without a recoverable originating input/date. The study's baseline omits these unordered audit rows rather than guessing their time. It is a projection of ordered product state, not a complete export of historical audit records. The baseline check also refuses any dated processing/evidence/judgement/day-completion record on or after July 24. Earlier positive-sequence product state is preserved. Prior snapshot diagnostics keep their default behavior; this new option is explicit for the study.

Run the unchanged `poc-v23` configuration through `replay.run`. Three fresh serial controls and three fresh concurrent trials, with their own empty archives and copies of one baseline, provide three paired samples and a serial-versus-serial variation check. Fixed order: control-1, concurrent-1, concurrent-2, control-2, control-3, concurrent-3. Read the first serial result before starting a concurrent trial. Each trial is launched explicitly; a failure does not automatically retry or start the next trial. Maximum 144 physical API calls and $1.50 total conservative cost, shared across all trials. This is a fresh budget, not a continuation of the API smoke's spending. No cap increases.

Both modes share a maximum of two in-flight provider calls, including daily judging. The serial control still uses the original item-by-item path and the original dependency-ordered day judging. The concurrent arm additionally uses D172's two extraction workers and two Jev workers. A semaphore in the study transport limits outbound calls; it does not change prompts, item order, matching, writer or judging rules. Network/unknown-usage failure closes admission. Known model refusals follow the existing product retry rules; every physical attempt counts. An authoritative failed item closes admission before the concurrent generator is drained.

After accounting durably records a response and before the study transport releases its semaphore slot, it validates the raw JSON/schema or Jev answer map with the existing validators. Malformed JSON, schema refusal or invalid Jev structure closes admission in that worker, covering day-judging workers as well as ingestion. Other slot waiters must recheck admission and cannot send. A valid-schema answer that fails a later product reference check still follows that product's existing correction rules; the study transport does not invent a semantic validator. Cancellation signals close admission before unwinding executors. Tests cover both an authoritative failed item and a schema failure within the actual daily-judging executor.

The budget reservation will use the request's actual validated output limit instead of reserving the model's maximum 128K output for every request. Keep the full 922K input bound and the same worst-case published Standard rates. For 16K output this reserves $0.520300, not $0.70; for 128K it reserves $0.612700. This does not raise the cap or infer tokens from text length. See the official source links in the D173 plan. Budget admission remains a refusal, never permission to overspend.

## Measure and calibration

The governing semantics come from D159/D172 and the existing Claude-authored `week-benchmark-v23-2026-10-25.json`. Its SK and NAVER candidates are distinct new events; their project groups are separate; Rubin association is optional for these deployments. Read the saved source statements: SK's first factory is planned for 2027 and uses Vera Rubin; NAVER's GAK Sejong expansion targets 200 MW by 2028 and also describes Rubin. The follow-up reports the same announced projects. Do not compare fresh candidate/group IDs literally with the gold's IDs, or classify every unlabelled new candidate as correct.

Report, for every trial:

- The two project questions and their source evidence; separate identity and customer-specific group membership. Additional well-sourced questions are not a failure merely because counts differ. Manually map the small result to the source and existing gold; record the mapping and reasons. A wrong/missing required project is reported separately from optional grouping variation.
- Whether the follow-up cites existing project questions, repeats an earlier statement or creates a duplicate. A repeated statement adds a source; it is not independent confirmation. Do not require the model to extract every sentence of the blog.
- Every accepted extraction's complete request hash rebuilt from its actual committed prefix, including schema and group context. Find that exact call's archived body/answer, re-run the existing extraction checks, and require the resulting handover to equal the saved handover. Existence of a matching request alone is insufficient. Every accepted input, dispatch sequence and write sequence must agree.
- Source quotation validation, existence/order of destinations, preservation of baseline questions/ladders, new group/member records, and daily judgement followed by day completion. Each changed eligible thesis is judged at most once at that sequence; cited evidence belongs to it.
- End-to-end elapsed time, physical calls, accepted/reused/stale requests, and conservative and Standard list-price cost. Include discarded speculative calls. A failed or unexercised case does not count as a pass. This small dependent workload cannot establish whole-day 10x acceleration.

If the first control misses a required project, stop before further paid trials and examine its raw output, checks and final writes. If any structural check fails, stop. Read each trial before the next. The six-trial set is a diagnostic comparison, not registered production acceptance or a new gold standard. Production remains unapproved.

## State × event

| State | Event | Transition and write |
|---|---|---|
| Unprepared | Existing output folder / changed source | Refuse overwriting or mixing experiments |
| Prepared | New explicit trial | Copy the same baseline into a new trial directory; empty archive; record config/runtime/source/baseline hashes |
| Trial waiting | Caller resubmits started trial | Refuse; preserve its data, no automatic resume |
| Waiting for outbound slot | Slot opens | Guard checks budget and cancellation before reserving/dispatching |
| Request dispatched | Known response | Journal usage, archive, and continue normal schema/content checks |
| Request dispatched | Transport failure or unknown usage | Retain reservation, close admission, drain existing calls, fail trial |
| Accounted response | Invalid raw JSON/schema/Jev shape in any worker | Close admission before releasing the slot or draining any parent executor; raw response and known cost remain in the guard journal |
| Speculation ready | Earlier committed prefix changes | Existing D172 rule recomputes; both calls are counted |
| Authoritative item fails | Later preparation is pending | Close admission before generator cleanup; cancel pending and drain dispatched calls; no later authoritative write |
| Judging | Independent/dependent views | Existing topology; shared outbound limit; no next day/trial automatically |
| Trial finished | Structural and manual review pass | Record results; next named trial may be started explicitly |
| Trial finished | Structural failure / missing required control result | Preserve result and stop the comparison |
| Any end | Protected originals changed | Report changed paths; no claim of database isolation |
| Any active state | Cancellation signal | Close admission before raising cancellation; queued slot waiters never dispatch; drain committed requests |

## Value × reader and new path × checks

| Value | Writer and readers | Check |
|---|---|---|
| Three complete item rows | Prepared from read-only source → replay | Full row/text identity; fixed order; only selected IDs |
| Historical baseline | Existing snapshot function → every trial writer | No sequence >=21; identical baseline digest; never write the original |
| Exact request/context | Existing extraction builder → workers and acceptance audit | Rebuild against each committed prefix, schema included |
| Reservation | POC guard → every provider stage | Actual request output cap plus full model input bound; tests cover maximum and small caps; same total cap |
| Semaphore | Study transport → all provider threads | Real temp journals + fake provider prove <=2 dispatched calls; cancelled waiters never send |
| Failed item | Product result → study day wrapper → guard | Close admission before drain; fake held preparation proves no later dispatch |
| Failed judge worker | Raw response → shared study transport → guard | Actual judging executor with more jobs than slots; malformed first response prevents queued sends |
| Judgements/completion | Existing product code → structural audit | Current day/sequence; evidence ownership; no completion before successful judging |
| Gold correspondence | Manual source review → report | Stable meaning, not numeric IDs, names or equal counts |

The only reusable change is tighter reservation based on the request's existing output cap, in the POC budget owner. Other code stays in the study harness. The source corpus, golds, default transport and production runtime are out of scope. Read-only review checks these tables before implementation; offline controls precede any live trial.
