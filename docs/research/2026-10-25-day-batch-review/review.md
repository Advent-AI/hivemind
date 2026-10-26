# Review: per-day API concurrency and the 10× target

**The acceleration is worth testing, but the queued plan is not ready to implement as written.** Its day-start reads change extraction, its proposed within-day pass is incomplete, and 10× is not supported by the recorded workload. Start with a correctness-preserving concurrency POC; treat a new day-level extraction contract as a separate product choice.

For example, the first NVIDIA earnings call creates the annual revenue thesis. Its CFO commentary later the same day links a quoted revenue figure to that thesis. At the start of the day that thesis does not exist. Parallelizing the existing calls with the same checks can discard the commentary's evidence. Merely sorting the database writes afterwards does not restore it.

Scope: current replay, extraction requests, Jev matching, writer, daily judging, recovery and evaluation. Baseline `da06fbd`. No product code or prompt is changed by this review. No live extraction or matching call has been made. These are offline proofs and an implementation proposal, not a completed acceleration benchmark.

Follow-up D172 implements the recommended offline POC; see its [implementation and current result](implementation.md). The measurements and limits below describe the original D171 review.

## What the stored data establishes

Read-only inventories cover both v23 arms, 480 extraction handovers per arm, through August 15. Calls copied from v21 archives are excluded. Audit (local artifact: `../../../poc/reports/2026-10-25-day-batch-review/audit-v2.json`), snapshot reconstruction (local artifact: `../../../poc/reports/2026-10-25-day-batch-review/snapshots.json`), visibility test (local artifact: `../../../poc/reports/2026-10-25-day-batch-review/visibility.json`).

| Check | Jev arm | Generative control | Meaning |
|---|---:|---:|---|
| Complete extraction requests reproduced from historical SQLite snapshots | 480/480 | 480/480 | The read reconstruction has a real control; original source and context match exactly |
| Requests whose text changes under a day-start snapshot | 214/480 | 168/480 | Moving groups alone does not make extraction independent; existing theses and group members also change |
| Stored evidence links to a thesis first created earlier that day | 90 | 82 | These targets do not exist at day start |
| Evidence items lost when the same raw answers pass the real checks with day-start IDs | 73/797 | 62/744 | Counterfactual code failure, not an estimate of what a fresh model would answer |
| Final repeat/replace decisions targeting evidence first created earlier that day | 86/320 | 47/196 | The new day-level resolver must cover evidence, not only candidate duplicates |
| New group declarations | 26 | 30 | Jev membership in existing groups does not supply group creation |
| Candidate records / distinct local candidate IDs | 102 / 9 | 96 / 10 | `c1` is local to an input, not a day-wide identifier |
| Evidence records / distinct local evidence IDs | 797 / 16 | 744 / 13 | Flattening answers into a dictionary keyed by `e1` overwrites evidence |
| Dependency rows | 0 | 8 | The Jev arm cannot test dependency ordering alone |

The first lost-link control is NVIDIA's February 25 CFO commentary: its full-year revenue statement points to the thesis introduced by the preceding earnings call. All 960 baseline requests reproduce exactly before the day-start counterfactual is applied. Both input ledgers and archives retain their original file hashes.

### Speed: what the estimate actually includes

The July 27 v23 Jev run processed 53 extraction calls, 82 Jev calls and seven judgement calls in about 513 seconds. The earlier 11.8-minute example describes the generative control, not the new default. Reusing the Jev run's recorded call durations in three separate waves gives:

| Maximum concurrent requests per wave | July 27 projected seconds | July 27 ratio | Full measured 31-day workload ratio |
|---:|---:|---:|---:|
| 6 | 123.0 | 4.2× | 2.5× |
| 12 | 79.5 | 6.5× | 3.0× |
| 24 | 63.6 | 8.1× | 3.2× |
| 32 | 59.6 | 8.6× | 3.2× |

These are optimistic **projections**, not provider measurements. They ignore added within-day comparisons, retries, rate limits, larger prompts and dependency constraints. The full-workload comparison is about 6,132 observed seconds against 1,922 projected seconds at 32 workers. Quiet days and slow individual judgements limit the benefit. The 315-second July 28 call remains in the projection. Cutting off that call cannot be counted as a saving without obtaining and paying for a successful replacement answer.

Judging already has six concurrent workers per dependency level (`judging.round_of_judgements`). Jev requests within an item remain serial (`jev_matching.decide`); archive locks cover SQLite accesses, not the network wait. Thus there is additional concurrency to expose, but the whole judging stage is not currently serial.

“Batch” here should mean bounded concurrent calls to the current normal APIs. OpenAI's separate Batch API describes a 24-hour completion window and unordered result files; it is not a seconds-level latency promise. It can be evaluated separately for cost-oriented offline work. [Official OpenAI Batch documentation](https://developers.openai.com/api/docs/guides/batch).

## Where the original plan breaks

| Finding | Code or data mechanism | Required design rule |
|---|---|---|
| Day-start extraction loses context | `round.run` reads `views_for_prompt` and `groups_for_prompt` after prior writes; `sift` admits only shown thesis IDs or local candidates | Either validate speculative reads before use, or explicitly change and evaluate the extraction contract. Do not silently change D159. |
| Moving membership does not replace group creation | Extraction emits names/scopes/aliases; Jev only returns membership probabilities for shown stored groups; `groups.plan` creates groups only for accepted founders | Retain extraction's source-backed group declarations in the first POC. A transfer of ownership needs a complete declaration and identity contract, not just removing the group block. |
| A final sort cannot fix stale matching | Earlier writes add targets, change in-force evidence, occupy successor slots and affect group membership | Rebuild/validate every affected comparison input before committing; a stored “new” decision is not valid merely because it was made earlier. |
| Local IDs collide | Each item restarts `c1`, `e1`, `n1` | Any day-wide intermediate reference is `(input_id, local_id)`; final ledger IDs remain assigned by the ordered writer. |
| “Compare everything in the day” hides a new workload | There are 263 earlier-item candidate pairs but 15,228 earlier-item evidence pairs in the Jev run, before filtering | Count queries, bytes, tokens and rate-limit demand. Limit comparisons by resolved thesis, while measuring recall. Do not assume the extra pass takes two seconds. |
| Pairwise equality is not necessarily transitive | Similarity/probability is not an equivalence relation; A≈B and B≈C do not prove A=C; a raw candidate can merge into a different canonical thesis | Resolve against the current canonical target, not unrestricted union-find or “highest probability wins” over all day pairs. |
| Late results can corrupt a newer plan | A response can arrive after a retry, configuration change or restart | Persist input/configuration/request identity; accept a result only for its exact request. Completion order never assigns sequence or ledger IDs. |
| A 60-second timeout alone is not a fix | A timed-out remote call may still have consumed tokens; retries and in-flight calls can exceed a nominal budget | Distinguish transient HTTP failure, schema refusal and unknown timeout outcome; reuse completed archived responses and account for attempts. Do not claim a cancelled call succeeded. |
| Existing gold is not plug-and-play for fresh outputs | Gold candidate IDs and membership view IDs belong to each original arm; the candidate scorer defaults unlisted candidates to “new”; some evidence sections are stored summary counts | Preserve the original labels, map by provenance/meaning, report unmatched outputs, and inspect them. Never award “new” automatically to an unmatched fresh candidate. |

## Recommended first POC: concurrent preparation, validated ordered commits

Use the existing extraction/grouping meaning first. Do not introduce a second clustering system or an all-day provisional graph while trying to establish the speed baseline.

1. **Freeze a day manifest.** Record the source IDs in existing dispatch order, sequence numbers, source hashes, configuration/prompt versions and the completed prior-day boundary. Keep the source day distinct from the wall-clock run date. Only one writer operates on this experimental ledger.
2. **Prepare calls concurrently against an immutable snapshot.** Workers receive fully built requests, never a writable SQLite connection. Keep separate bounded pools for extraction and Jev. Deduplicate identical in-flight request hashes within the batch. The archive remains the owner of raw responses.
3. **Commit in sequence, validating what was read.** At an item's turn, regenerate the exact extraction request and schema against the current committed prefix. Reuse its prepared answer only when the request hash is identical. Otherwise obtain a new answer for the current request and account for it as rework. This includes changes to a query that previously returned no results, group members, group IDs and permitted schema references.
4. **Prepare independent Jev questions concurrently.** Resolve candidate destinations before candidate-linked evidence comparison, as today. Compare the full Jev request against current target text, evidence in force, lists and group definitions. If any changes, redo only that request. Do not let concurrent workers mutate the shared candidate dictionaries (`jev_group_refs`) or totals; collect immutable results and apply them in input order on the coordinator.
5. **Write through the existing atomic writer.** Recheck exact identity, open state, successor eligibility, replacement entitlement and target existence. A write conflict returns to matching; it never forces creation or silently drops a link. Save the matching record, new IDs and item completion with the same transaction. Earlier committed items remain a valid prefix after a crash.
6. **Judge after all item commits.** Use the existing dependency scheduler: independent theses concurrently, upstream levels first, including newly triggered dependants. Mark the day complete only after judgement and pull succeed. Do not move to tomorrow while today's required work is incomplete.

This preserves the current meaning and provides a clean control for concurrency. It may be slower than the optimistic table because 214 requests have changed day-start context. That is a result to measure, not a reason to use stale answers. Pipeline overlap can improve the staged estimate, but must be measured separately.

Worker counts, queue limits, timeouts and spending caps are explicit run arguments recorded in the run manifest, not new product Config settings (D3). Bound queued request bytes as well as active workers; stream staged results to the run archive rather than retaining an entire large corpus in memory. Measure OpenAI and Jev limits separately. The first performance comparison retains the same timeout/retry policy in both arms; a shorter timeout is a separate experiment, not a free speed gain. Source/schema failures and transport failures retain separate reasons. Partial results and unknown usage remain in the denominator.

The more aggressive alternative is a new day-level contract: extraction retains all relevant statements and source-backed candidate/group descriptions independently of existing IDs; matching resolves old and same-day targets; ordered resolution governs identity and history. That changes what extraction produces and how omission is defined. D149/D159/D169 require a recorded decision before implementing it. It needs its own fresh semantic experiment; the archived outputs cannot prove it works. Do not fold that redesign into the first concurrency test.

## Runtime state × event: proposed control

| State | Event | Transition / persisted result |
|---|---|---|
| Prior day complete, no manifest | Start day | Persist ordered inputs, source/config hashes and starting boundary before submitting work |
| Manifest ready | No eligible inputs | Perform existing day-end duties; complete only on success |
| Request prepared | Eligible slot | Submit exact request; record attempt identity; no ledger mutation |
| In flight | Success | Archive exact response; mark it available for its request only |
| In flight | Rate limit/transient failure | Bounded retry under the same request and remaining attempt budget; completed items are not resubmitted |
| In flight | Timeout/unknown outcome | Record unknown usage and outstanding attempt; do not create an answer or silently duplicate its result |
| Answer ready, earlier item pending | Any completion order | Hold result; ledger order does not change |
| Answer ready, item reaches commit turn | Read/schema hash still matches | Validate and use answer |
| Answer ready, item reaches commit turn | Read or configuration changed | Discard it as a candidate for this commit, retain archive; prepare current request or stop on incompatible run configuration |
| Checked plan | Earlier write changed a target or successor | Recompute affected matching; no blind write |
| Writing | Exception midway | Roll back that item's entire transaction, including completion markers; preserve earlier committed prefix |
| Committed | Redelivery/restart | Reuse completion and final IDs; no duplicate source link, evidence, membership or call for completed work |
| Any unfinished state | Corrected input or changed scope | Existing versions stay fixed. Start a separately identified input/run under the decided correction rules; do not patch the manifest in flight |
| Any unfinished state | Another writer | Not supported by this single-writer POC; stop on boundary conflict rather than merge unseen writes |
| Last item committed | Judgement begins | Dependency levels, each affected thesis once under the existing rule |
| Judging/pull | Failure/crash | Day remains incomplete; resume remaining duties without replaying completed items |
| Day complete | Late result from an old attempt | Archive by its original request; never apply it to the completed day |
| Any state | Stop requested / cap exhausted | Stop submission, drain/account for in-flight work; retain the resumable prefix and do not mark an unfinished day complete |

## Values and readers

| Value / writer | All relevant readers | Rule |
|---|---|---|
| Input ID, source hash, source day, sequence / dispatch-manifest coordinator | Extractor, matcher, writer, audit, resume | Identity and chronology; source text stays exact |
| Request hash, schema, configuration / request builder | Worker, archive, retry, commit validator | One exact request; a changed read creates another request |
| Local candidate/evidence/group ID / extraction | Matcher, resolver, writer, scorer | Namespaced by input; never globally joined on `c1` alone |
| Candidate/group description / extraction | Jev, group planner, ordered writer | No membership implies identity; valid founders only; no unseen future group |
| Matching probabilities / Jev worker | Coordinator, existing code checks, matching archive | Immutable response; same criteria and threshold; current canonical target |
| Final IDs, replacements, dependencies, memberships / writer | Following item, historical reads, judging, API, audit | Commit atomically in sequence; retain sources and prior records |
| Judgement / dependency scheduler | Dependants, pull, API/history | Upstream conclusions first; only changed conclusions propagate |
| Gold correspondence / evaluation | Review and reported metrics only | Cannot determine production identity or silently change gold |
| Attempt time, outcome and usage / call wrapper | Scheduler, spend accounting, report | Include retries, incomplete calls and rework in elapsed/cost results |

## Test sequence and acceptance

| Step | Work | Gate |
|---|---|---|
| 0 — complete here | Census, historical snapshots, original-request reproduction, stale-ID replay, scheduling estimates, positive controls and mutants | No unidentified cases or historical-write changes; findings below remain explicit |
| 1 — before live calls | Isolated scheduler/coordinator using archived responses, shuffled completion order and injected failures | Same final semantic records and source links for identical validated responses; crash at every transition resumes once; late/duplicate responses never commit twice |
| 2 — first live POC | Same source snapshot and fixed code, ordinary APIs; fresh sequential control and concurrent arm, at least three samples each | Compare control against control first. Record every request, queue interval, attempt, response and write; no provider/model change |
| 3 — semantic reading | Reuse applicable gold plus explicit provenance mapping; review new/unmatched units from sources | No introduced false merge, lost quote/source, invalid reference, missing required membership or temporal leak; report all pre-existing errors and uncertainty, not only net counts |
| 4 — time/size reading | Fixed source workload on both arms; measure first submission through completed day | End-to-end elapsed ratio, tokens/cost, peak in-flight work, retries and rework; cached replay is not a live speed benchmark. Same worker limits and no competing heavy job |
| 5 — only after small pass | Seed, one busy day, then consecutive days containing replacements/successions, then the fixed week and August holdout | Keep the standard fixed; a failed registered acceptance stops the line. Publish every sample and do not drop quiet/slow days |

Use July 27 for the busy-day latency test, but use February 25/May 20 for same-day financial repeats and group founding; include July 28's slow-call behavior and August's succession examples. A July 27-only pass cannot establish the whole pipeline. The existing Jev ledger has zero dependency rows, so use the recorded generative dependency cases plus deterministic failure tests for that path; do not claim it was exercised by a zero-row check.

Structural acceptance is exact: source linkage, temporal visibility, valid IDs, one committed item result, rollback, restart and conservation of evidence. Semantic acceptance uses source meaning: equal IDs, wording, group counts or matching the old model's error are not success. Existing labels are Claude-authored and partially sampled, not independent human gold. Unlabelled new candidates are unjudged until reviewed, never automatically correct “new” decisions.

**10× acceptance:** retain it as a stretch target, not a promised outcome. Publish the ratio on the complete fixed workload against fresh sequential `poc-v23` controls, including retries, invalidation and judging. If correctness passes but speed is 3×, report 3×. Do not obtain 10× by comparing with the older LLM matcher, excluding slow days, clipping durations or changing the workload. The review does not authorize switching model/provider, crossing unfinished day boundaries or weakening judgement quality to make the ratio.

## Verification completed

- 960/960 extraction requests reconstructed exactly from real historical SQLite snapshots.
- Both raw-answer visibility replays completed; the introduced losses are counted above, not hidden.
- Existing scorer reproduced the Jev week's candidate result (47/47 new; 1/2 merge), August result (35/35 new; 6/7 merge; 0/3 succession) and group coverage (12/13 and 23/25). These are the saved runs before the D168 corrections; fresh controls must run current code. No gold was edited.
- Five diagnostic controls passed. Two scratch mutants were caught by their intended assertions: admitting future rows, and ignoring the worker limit. Mutant traces (local artifact: `../../../poc/reports/2026-10-25-day-batch-review/mutants.json`).
- The complete product, corpus-label and diagnostic suites passed together: 128 tests in 12.66 seconds, from a temporary working directory. Test output (local artifact: `../../../poc/reports/2026-10-25-day-batch-review/tests.txt`). Preflight judged all 250 Jev matching records with no refusals or skipped records, and 148 prompt-enum checks had no missing values. Preflight (local artifact: `../../../poc/reports/2026-10-25-day-batch-review/preflight.txt`). Neither establishes fresh model quality or batch-runtime correctness.
- Runtime scheduler, fresh model quality and live latency tests have not run. Their contracts/acceptance need agreement first; the old experiment budgets are not an authorization for new calls.
- A read-only review (local artifact: `reviewer-report.txt`) found no serious issue in the proposed contract. It independently reproduced the timing projection, all 960 message pairs and schemas, and the visibility losses. This validates the review's evidence and contract, not a future implementation.

## D22 reasoning refresh

No foundation behavior is adopted by this review. In module order:

| Module | Effect; page/PRD, example and acceptance check |
|---|---|
| Research universe | No scope/category change; worker controls remain outside the universe |
| Classification | Same fixed inputs, dates and duplicate metadata; no reclassification or corpus rebuilding |
| Config | Existing model/prompt configuration remains; proposed runtime worker/cap settings stay outside product Config |
| Dispatch | Its sequence remains the ordering authority; concurrent completion never reassigns sequence |
| Extraction | D159 context is preserved by the recommended proposal; the day-start alternative remains unapproved and cannot silently replace it |
| Thesis library | Identity, group declarations, evidence, atomic writes and historical reads retain their contracts; proposed coordinator tests must re-prove every reader |
| Final verdict | No change; remains deferred |
| Pull mode | Existing day-end close behavior remains after required judgements; no crossing an incomplete day |
| Human review | Existing refusal/failure destinations unchanged; no new automatic decisions |
| System overview | Source-driven sequence and read-only extraction remain; concurrent work requires validation before ordered writes |

The maintained inconsistency corrected in CURRENT_STATE is the claim that judging was per-item/serial and the implied general 12-minute-to-45-second result. The proposed contract is linked rather than copied into the governing PRDs. The mechanical documentation check runs after this reasoning refresh.

## Reproduce

Run `audit.py --out <new-report>`, `visibility_proof.py --out <new-report>` and `snapshot_proof.py --out <new-report>` from this directory using absolute report paths. All source databases are opened read-only. Snapshot tables exist only in memory. Run `python -m pytest <this-directory>/test_controls.py -q` for the five controls. Reports refuse to overwrite previous results.
