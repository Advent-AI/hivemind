# Day-batch acceleration: review and free proofs

Scope requested by Alex: review the per-day extraction/Jev/sequential-write plan against current code, stored results and golds; reason through correctness and test it step by step. Baseline commit: `da06fbd`. This slice builds diagnostic scripts and isolated simulations only. Product behavior, model prompts, the golds and the saved ledgers stay unchanged.

Example: morning news creates a question and an evidence item; afternoon news revises that statement. Concurrent requests can finish in either order. The final writer must still attach the afternoon statement to the morning question and correctly retain or replace its evidence. A day-start library snapshot alone cannot do this.

## Decisions to respect

- D159: later extraction reads earlier committed items. A day-start extraction snapshot changes the model's input, not merely its scheduling.
- D149/D165/D166: extraction declares new groups and references existing groups; code resolves names, then writes memberships. Jev currently adds membership in stored groups but cannot declare new ones. D169 explicitly leaves transferring ownership undecided.
- D63: one day-end judgement round, with dependencies judged before dependants.
- D167/D168: identity is not equal numeric values or a matching company; repeat/replace/new keep their defined meanings; succession preserves periods and direction.
- D170: measured baseline is the default Jev pipeline, not the earlier generative matcher. Historical archives include older copied calls; select the recorded configuration before measuring.

## Questions and measurements before implementation

| Proposed change | Existing input or reader | Free proof |
|---|---|---|
| Concurrent extraction from a day-start snapshot | Existing-thesis context, direct evidence links, group context and references | Count shown and referenced records first created earlier that day; show one original request for each class |
| Concurrent Jev matching | Candidate lists, evidence lists, group catalogue, same-day newly created targets | Count same-day targets in final matching attempts; distinguish candidate, evidence and group references |
| One sequential write phase | Per-item local c/e/n IDs, existing target IDs, replacements, successions, group founders, retries | Inspect writer and checks; simulate late-arriving worker results and an earlier write changing a later target |
| More concurrency | Current judging already has six workers per dependency level; calls and storage locks | Map actual calls to source days; compute bounded scheduling estimates at fixed worker counts, include tail calls and existing judgement dependencies |
| Score against saved results/golds | Golds contain per-arm candidate and view IDs; evidence scoring uses local IDs and target substrings | Inventory labelling coverage; require semantic/provenance mapping before fresh-output comparison; do not use ID equality as truth |

## State × event for the diagnostic slice

| State | Event | Behavior |
|---|---|---|
| Before read | Missing ledger, archive, expected field or baseline configuration | Fail, name the missing precondition; do not create a replacement database |
| Reading | Historical records contain same-day targets | Count by stored sequence and source publication day; retain examples |
| Reading | Calls cannot be linked to a source day | Report/fail measurement; do not silently drop slow or failed calls |
| Timing estimate | Fewer jobs than workers, empty day, long tail, sequential dependencies | Use actual job durations and prerequisite order; separate unmeasured provider effects |
| Scratch simulation | Responses shuffled, one missing/failed, retry, writer crash or later stale target | Assert deterministic order, no dependent commit, explicit stale-plan refusal or recomputation |
| Finished | Input hashes differ after analysis | Fail the read-only check |

## Value × reader

| Value | Source | Reader |
|---|---|---|
| input_id and sequence | processing_steps/handovers | Scope, order, trace and provisional reference identity |
| view/evidence/group IDs and creation sequence | Stored ledgers | Same-day visibility census; never newly assigned IDs as semantic gold |
| request/configuration/purpose/call ID/duration | model_calls and judgement rows | Timing model; original context inspection |
| candidate/evidence/gold labels | Existing frozen golds and final match records | Coverage audit only; correctness still requires original text |
| Estimate at worker count | Deterministic list scheduling over stored durations | Feasibility bound, explicitly not measured new latency |

## New path × old checks

The later runtime POC must preserve source validation, all candidate/evidence destinations, identity/succession rules, temporal target eligibility, group founder rules, complete atomic writes, failure/resume, day-end judging and historical reads. Existing D159 tests remain valid for the default path; an experimental day-batch path needs a separately agreed contract. Never make the old tests pass by weakening their assertions.

Output of this review: counted findings, one recommended architecture, complete runtime state/event and reader tables, explicit acceptance and staged test sequence. No paid call until the required product choices and measurement standard are settled. The $5 seed-build cap in D164 and completed experiment budgets are not reusable authorization for a new comparison.
