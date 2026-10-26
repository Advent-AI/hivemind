# D229 · Reveal the Trigger last and remove its selector chevron

Alex wants the Trigger shown after the theses. The arrow request was clarified in D230: the Trigger connector is a plain line without a directional arrowhead; the comparison dropdown's normal indicator is restored. The reveal ordering below remains D229.

There is one Trigger renderer and one completed-tree reveal controller. The pending submit path currently also shows the Trigger, so changing only the completed animation would still show it first. Hide it during pending/error states, then include it as the completed reveal's final card.

## State × event

| State/event | Required result |
|---|---|
| Pending query / progress | Idea progress only; no Trigger or its connector |
| Completed query | Idea → theses top-to-bottom → existing overview return → Trigger and its connector fade in |
| Completed empty/unassessed result | Idea → overview → Trigger with unavailable confidence |
| Failed query | Existing error Idea; no Trigger |
| Manual cancellation | Settle all final cards and lines immediately; cancel future camera updates |
| Reduced motion / retained replay / range / navigation | Existing immediate or retained completed view; no replay of the entrance |
| New query / teardown | Hide/remove the prior Trigger; preserve existing reset and event cleanup |

## Values and checks

| Value | Owner / reader / proof |
|---|---|
| Pending versus answered | Bootstrap → graph options; controlled-service browser check |
| Final Trigger node and connector | Canvas → reveal controller; hidden and inert until all thesis entrances finish, visible after overview |
| Comparison selection | Existing Trigger/select controller; all six operators selectable by mouse/keyboard |
| Cancelled run | Existing abort signal → all cards/paths, including the final Trigger; no later callback |

D228 still owns the left-side position and Trigger → Idea connection. D227 still owns the straight downward thesis scan. D229 supersedes only D228's initial Trigger visibility and D226's pending Trigger. No confidence, condition, data or backend change. Claude's work is out of scope.

Self-review: hide the connector as well as the Trigger so no arrow floats into the Idea before its source appears. Cancellation must settle the final card and path too. Return to the overview before revealing it, so the left-side Trigger is visible without another camera trip. Verify a prior-controller scratch build fails the new last-card assertion. Use stored fixtures only.

## D229 verification before the D230 arrow clarification

- The real-browser sequence is `idea → v3 → v9 → v1 → trigger`. Across 296 thesis-scan frames the Trigger and connector remain hidden; the Trigger is inert. It enters only after the camera reaches the overview. The existing downward scan and partial line frames pass. Frame samples (local artifact: `../../poc/reports/2026-10-27-trigger-last/reveal-frames.json`).
- A scratch build that reveals the Trigger after the Idea is rejected with `Trigger preceded a thesis`. The final controller passes Fit cancellation, replacement, teardown and an empty result with a final Trigger. Cancellation reveals every final card and connector immediately.
- The controlled-service UI check passes no Trigger during loading, a completed `> 70%` default, no visible dropdown chevron, comparison selection, number/slider/wheel interaction, replay/range/tab retention and new-query reset. The default full graph still has five cards; failed and pending views do not require a Trigger in their snapshots.
- The first final-frame check found the Trigger at opacity 0.998504 after normal CSS transitions resumed. This affected the newly last card, whose inline animation styles were being removed in the same frame. Committing the settled appearance before restoring normal transitions removes that redundant final fade; the same browser check then passes with every card fully visible.
- All 52 frontend tests, lint and formatting pass. The final portable build validates 90 theses in 25.8ms and has 168,514 JavaScript bytes, within the existing budgets. No dependency or backend code changed. Verification uses stored responses, and the existing question is replayed only after a read-only, network-disabled cache check.
- The actual app tab now runs this build with the user's previous question restored. Its selector chevron has computed display `none`, the settled Trigger has opacity 1, and its left-side position is unchanged. The archive remains at 27 calls. [Updated current-question preview](../../poc/reports/2026-10-27-trigger-last/preview.png).

## D230 connector clarification

The canvas classifies a path touching a Trigger as `edge--trigger` when it is created. A single CSS marker rule holds in the normal, highlighted and revealed states; the shared hover code cannot restore an arrowhead. Normal thesis edges keep their markers. The browser check verifies this on initial display, Idea hover and leave, and after range/new-query redraws; it also verifies the restored dropdown indicator. All 52 frontend tests, lint and formatting pass. The change adds no data or service behaviour and keeps D229's final Trigger entrance.

The actual app tab is refreshed with its previous question restored from cached answers. Its Trigger line has computed marker `none`; all three thesis lines retain their arrow markers, and the dropdown indicator is visible. The archive remains at 27 calls. The build validates 90 theses in 26.9ms and contains 168,622 JavaScript bytes. [Plain connector in the current question](../../poc/reports/2026-10-27-trigger-last/plain-connector.png). The reasoning refresh changes only this frontend marker rule; no upstream, stored-data or PRD contract changes.

## D231 metric control

AI confidence is now a shared single-option select, with `If` remaining outside it. The metric, comparison and percentage controls are all 30px high. The metric's click/keyboard selection does not alter the condition, and both menus close and clean up together. The controlled-service browser checks its only available option, selection, aligned control heights, unclipped label and existing Trigger behaviour. Native ArrowDown/Enter selection also passes. All 52 frontend tests, lint and formatting pass; the build is 168,831 JavaScript bytes and validates 90 theses in 25.2ms.

The reasoning refresh leaves the pipeline, scoring, storage, condition shape and all upstream modules unchanged. Only the Trigger component, its style and frontend descriptions change; there is no speculative additional metric.

## D232 slider and readout before clarification

The round thumb is replaced by a 2px vertical bar inside the native 14px drag target. The filled track follows its centre. The footer is `Current value:`, supplied by the selected metric; the current single option reads the existing AI confidence. In the browser, native dragging changes the threshold from 70 to 30 while current confidence remains 63%. The existing controlled-service check also verifies that setting the threshold to 100 leaves the metric readout unchanged and that replay updates the metric from the Idea's selected-date confidence. The matching metric dropdown and all three 30px controls pass.

The final build contains 168,934 JavaScript bytes and validates 90 theses in 26.2ms. No data, backend field or calculation changed. The reasoning refresh affects only this frontend control and label; all upstream module contracts remain unchanged.

The user's open question is restored in the updated app. AI confidence is the selected metric, the threshold is 70%, and `Current value:` reads 55%. The archive remains at 27 calls; all 52 frontend tests, lint and formatting pass. [Current metric selector and bar handle](../../poc/reports/2026-10-27-trigger-last/metric-value.png).

## D233 current-value marker and D234 navigation

The round handle controls the threshold again. The current value has its own fixed vertical marker and a label immediately below it. In the browser, dragging the round handle from 70 to 30 leaves the marker at the same pixel position and the label at 63%. Threshold edits to 100 also leave the marker unchanged. Replay moves it with the Idea's displayed confidence. Labels stay inside the card at 0 and 100; an unavailable value hides the marker.

A scratch build that ties the marker to the threshold fails with `Threshold editing moved the current-value marker`; the current build passes. All 52 frontend tests, lint and formatting pass. The final build contains 169,229 JavaScript bytes and validates 90 theses in 25.4ms. The page shell now uses Alex's exact tab names `Thesis Library` and `Explore Ideas`, with unchanged navigation IDs and behaviour.

Reasoning refresh: the metric and threshold remain separate values, and no backend, scoring or upstream module changes. The frontend specification, integration guide and current-state paragraph now describe the corrected marker. These changes introduce no new glossary concept or generated PRD semantics.

The actual app preserves the user's 65% threshold. Its fixed marker and label show 55%; their horizontal centres match exactly, and the label sits below the marker. Switching the renamed tabs retains that state. [Corrected marker and round knob](../../poc/reports/2026-10-27-trigger-last/current-value-marker.png), [renamed navigation](../../poc/reports/2026-10-27-trigger-last/renamed-navigation.png). Restoring the question used cached answers; the archive remains at 27 calls.

Reasoning refresh: this changes only presentation order, the local comparison control and animation cleanup. Universe, classification, Config, dispatch, extraction, stored theses, final verdict, pull mode, human review and system semantics are unchanged. The frontend specification, earlier presentation contracts, integration guide and current state now point to the final Trigger entrance. No new glossary or generated PRD semantics are needed. Run `docs/check.py` last.
