# D228 · Put the Trigger on the Idea's left

Alex clarified that the Trigger belongs to the left of the Idea. Reserve its own 320px column with the existing 180px gap. Vertically centre it on the Idea. Connect Trigger → Idea into the Idea's left edge; keep Idea → Thesis connections unchanged. The default camera still centres the complete occupied tree at readable size.

## State, values and checks

| Case | Required behaviour |
|---|---|
| Pending, answered or failed Idea | Trigger remains to its left and is centred on it |
| No matched theses | Trigger and Idea remain connected |
| Completed reveal | D229 supersedes the initial entrance: show the left-side Trigger last, after the thesis scan and overview return |
| Replay, range, navigation | Existing condition, confidence, status and camera-retention rules hold |
| New query / teardown | Existing reset and controller cleanup hold |

Layout owns the positions and edge direction. D229 now owns the Trigger's final entrance after the overview return; there is no separate camera trip to it. The reveal continues to start at the Idea. The confidence reader, condition owner and controls do not change.

D226's right-column slot and its Idea → Trigger edge are superseded. D222's full-tree centring and D225's navigation lifetime remain. No backend, storage, model call, confidence calculation or new control is added. Claude's work and the separate cleanup branch remain out of scope.

Verify the stored multi-root/related graph and empty graph: Trigger on the left, 180px gap, shared vertical centre, one Trigger → Idea edge and no card overlap. Update the browser fixtures to expect the new direction and three thesis targets in the scan. Verify control/retention and reveal/cancellation paths, then the frontend suite and documentation check.

## Verification

- The browser shows Trigger x=180, width=320; Idea x=680, width=440. The gap is 180px. Both centres are y=464.5. The connector is Trigger → Idea, followed by the unchanged three Idea → Thesis connections. [Preview](../../poc/reports/2026-10-27-trigger-left/preview.png), [full default view](../../poc/reports/2026-10-27-trigger-left/full-view.png).
- The final controlled-service browser fixture passes pending/completed settings, comparisons, wheel/slider synchronization, replay, range, tab retention, new-query reset, attached endpoints and teardown. It makes two fixture submissions and zero aborts; no model or backend call is made.
- The stored multi-root/related and empty layout tests pass. The scratch mutation that removes the Trigger's left-column allocation fails its required gap assertion. The full frontend suite has 52 passing tests; all 17 mutation checks pass. D227's browser scan and cancellation checks also pass with this placement.
- The subsequent user screenshot came from the actual app tab still holding the previous inline bundle and its in-memory graph. The served HTML already had the new build. Reloaded that tab through a versioned URL, then restored the exact previous China/geopolitics question. A read-only replay with network calls refused confirmed all three model calls were cached before restoration; the archive stayed at 27 rows afterward. The actual app now shows Trigger x=180 and Idea x=680 with equal vertical centres, including after Library → Explore. Saved model answers were not the layout cache and were preserved. [Previous question after refresh](../../poc/reports/2026-10-27-trigger-left/previous-question-refreshed.png).

Reasoning refresh: placement changes only the frontend graph geometry and introduction. Upstream modules, stored records, confidence and Trigger condition rules are unchanged. The frontend specification, D226 introduction, integration guide and current-state paragraph now point to the corrected left-side position. No new glossary concept or PRD semantics are needed.
