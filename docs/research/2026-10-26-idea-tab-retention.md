# D225 · Keep the current Idea across workspace tabs

Switching Library / Explore an idea preserves the submitted question, graph, assessment, selected replay date, range and camera until a new query is submitted. This lasts for the current page session; reload keeps its existing reset behaviour.

## Diagnosis and ownership

One navigation path causes the loss: `showLibrary` aborts the request, destroys the explorer and sets `app` to null. `showIdea` then creates an empty explorer. Keep the mounted explorer instead. Pause its replay/reveal and close its detail drawer when leaving; teardown remains owned by `pagehide`.

## State × event

| State/event | Required transition |
|---|---|
| First Explore visit | Create explorer, show empty canvas and focus composer |
| Completed/error Idea → Library → Explore | Hide/show the same explorer; retain graph/date/range/camera and do not replay its reveal |
| Pending Idea → Library | Continue the same request; retain its pending card |
| Progress arrives while hidden | Update request state, defer DOM work until visible |
| Result/error arrives while hidden | Validate and retain the response; queue its presentation without measuring hidden DOM |
| Return to a completed background request | Apply queued data/graph once; play the first reveal once for a newly seen result |
| Return to a still-pending request | Refresh its progress card at valid visible dimensions |
| Submit another query | Clear deferred presentation, then use the existing request/reset path |
| Pagehide | Abort requests and destroy explorers/controllers as before |

## Values × readers and checks

| Value | Owner/readers | Proof |
|---|---|---|
| Explorer and graph DOM | Bootstrap retains; navigation toggles visibility | Same scoped canvas IDs and card contents after repeated switches |
| Date, range, camera | Existing canvas | Exact same slider/range/transform after returning |
| Deferred progress/presentation | Bootstrap only | Hidden result does not create zero-width cards or detached routes |
| In-flight request | Existing request generation/abort controller | Tab switch sends no new request and does not abort; pagehide/new-query handling remains |
| One-shot reveal | Existing completed-result presentation | No replay on revisiting an already shown result |

D187 owns progress/cancellation, D219 the composer, D221/D222 the default camera and D223 the one-shot reveal. D225 changes navigation lifetime; it does not add storage, model calls, score logic or data formats.

Self-review: keeping DOM alone is insufficient because background result rendering would measure a hidden canvas at zero width. Defer that rendering until visible. Keep completed graphs untouched on return; only queued background updates may rerender.

Verify completed and failed requests, repeated switches, pending return, completion while away, replacement by a new query, preserved camera/date/range and no extra/aborted requests using a stored-response browser fixture. Run frontend and documentation checks. Claude's backend files, running jobs and the separate cleanup branch are out of scope.

## Verification

- The real-browser fixture passes all listed paths: pending progress while away, completion while away, failure while away, three repeated completed-view switches, retained error and replacement by a new query. It submits three controlled queries, with zero navigation-triggered submissions or aborts. Connector endpoints meet the visible cards after deferred presentation.
- Two scratch bundles are rejected at their intended assertions: restoring destruction fails with `Navigation removed the pending card`; restoring cancellation fails with `Navigation aborted the pending request`. Production source is not changed by these controls.
- A separate click through Library / Explore preserves the exact view: `Replacement idea`, `2026-08-15`, `Last 30 days`, `canvas-1-arrow`, and `translate(621.742px, 64.2626px) scale(0.902539)` before and after. [Screenshot after returning](../../poc/reports/2026-10-26-idea-tab-retention/retained-after-navigation.png).
- All 48 frontend tests pass; lint and formatting pass. The portable page validates 90 theses in 28.4ms and contains 163,786 JavaScript bytes, within the existing 200 KiB budget. No dependency was added. The three protected source database hashes match the D181 baseline.

The first fixture's mock script had a template-string newline escaping error. Its submission accidentally reached the real local API and made three model calls costing $0.001463; those records remain in the local service archive. The error was disclosed to Alex. The fixture now emits its newline explicitly, never delegates fetch, and sets its fallback API to the static-only server on port 8002. All passing navigation checks and both mutation controls use this isolated service.

Reasoning refresh: research universe → classification → Config → dispatch → extraction → thesis library → final verdict → pull mode → human-review intake → system overview retain their data contracts, examples and acceptance criteria. This change owns only browser navigation lifetime; it writes no thesis, evidence, assessment or group data. The frontend specification, integration guide, decisions and current state now point to this retention contract. No governing page/PRD block needs a semantic change. The final mechanical check is `python3 docs/check.py`.
