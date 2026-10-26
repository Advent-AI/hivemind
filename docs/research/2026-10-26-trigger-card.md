# D226 · Idea confidence Trigger

Add a reusable frontend Trigger card in the existing card style. Placement and direction now follow [D228](2026-10-27-trigger-left.md): it sits left of the Idea and connects into the Idea's left edge. Existing thesis ordering and associations stay intact. An Idea with no theses still has its Trigger. Standalone Thesis/library callers do not receive one.

For example, `If AI confidence > 70%` reads the same rounded percentage shown by the Idea. At 61% its status is `Not met`; changing the threshold to 60% shows `Met`. This is a frontend condition and status only. It sends no request and performs no external action.

## State × event

| State/event | Transition |
|---|---|
| New query | Reset to `> 70%`; D229 shows only the Idea while pending |
| Answer / selected replay date | Read the existing composite confidence; evaluate the selected condition using the displayed whole percentage |
| No assessment / failed query | Completed results without assessment show `No confidence`; D229 omits the Trigger on failed queries |
| Choose operator | Support only `>`, `>=`, `<`, `<=`, `=`, `!=`; immediately update status |
| Drag slider / keyboard / type percentage | One integer threshold from 0 through 100; keep number and slider in sync |
| Scroll over threshold or slider | Adjust one percentage point in the scroll direction, clamp at 0/100, consume the event so the canvas does not pan |
| Replay / range redraw | Preserve the condition; update only its current confidence/status |
| Library → Explore | Preserve the mounted Trigger and condition under D225 |
| Replacement / teardown | Destroy the old select and listeners; a new query resets the condition |
| Completed tree reveal | D229 shows Trigger last after the thesis scan and overview return |

## Value × reader

| Value | Writer / readers |
|---|---|
| Operator and threshold | Trigger emits a validated condition; bootstrap owns it for the current query; canvas redraws read it |
| Confidence | Existing composite/date functions → Idea chart and Trigger; no new score calculation |
| Met / not met / no confidence | One pure comparison function → Trigger status |
| Trigger geometry and connection | Graph layout → canvas routes, bounds, default camera and reveal |
| Select lifecycle | Trigger controller → canvas render/destroy; no detached document listeners |

## New path × existing checks

| Path | Required checks |
|---|---|
| Optional Trigger graph | Existing explicit thesis IDs and branches validate unchanged; a Trigger requires a leading Idea |
| Extra card / edge | No card overlap, existing 180px minimum column gap, attached endpoints, width-centred default camera |
| Condition changes | Closed operator set, finite confidence or null, integer percentage bounds, keyboard accessible controls |
| Re-render / hidden navigation | Existing confidence/date source, retained condition and camera, no new request |
| Animation | Existing cancellation, one-shot reveal, reduced motion and teardown hold for the extra target |

Prior decisions: D197 owns confidence conversion, D213 the Idea/Thesis widths, D218 the shared controls, D222 camera centring, D223 reveal and D225 tab lifetime. Their score/data/request rules are unchanged. The 200 KiB script and 200ms validation budgets remain.

Self-review: placing the Trigger on top of existing theses would overlap cards; reserve a real layout slot. Recreating its select without teardown would leak document listeners; destroy its controller before replacement. Comparing raw fractional confidence while displaying a rounded integer would make equality confusing; compare the displayed value. Canvas wheel handling must not receive threshold scrolls. Claude's backend work, data and separate cleanup branch remain out of scope.

Verify every operator at below/equal/above boundaries, missing confidence, bounds and rejected inputs. Check the real DOM with a stored-response service: default placement/style, keyboard selection, slider/number/scroll synchronization, no canvas movement, replay/range/navigation retention, new-query reset, animation and teardown. Use scratch mutation controls for decisive comparisons/layout, run the touched checks and full frontend suite, refresh documentation, then run `docs/check.py` last. No model call is needed.

## D226 verification before D228

- All 51 frontend tests pass. The Trigger cases cover 18 operator boundaries, percentage rounding, 0/100, missing confidence and rejected inputs. The stored eight-root/five-related graph and an empty graph reserve a non-overlapping Trigger slot, preserve thesis order and connect it to the Idea with the existing 180px column gap.
- All 17 scratch-copy mutations are rejected. The three new controls catch a strict comparison changed to inclusive, missing confidence changed to false, and removal of the Trigger's reserved layout height. Their failures are assertion failures on the intended cases.
- The isolated browser check passes defaults, pending-to-completed edits, all control synchronization paths, status/equality, wheel bounds and containment, confidence agreement with the chart, historical replay, range redraw, navigation retention, query reset, attached endpoints and controller teardown. It submits two stored-response queries, with zero aborted requests; editing causes no request. The separate navigation fixture also passes its three-query completion/failure/replacement scenarios with the extra card.
- Native keyboard actions decrease the number and increase the slider back to 70, then choose `≠` through Home/End/Enter. A native scroll changes the threshold from 70 to 71 while the camera remains exactly `translate(645.674px, 65.942px) scale(0.551449)`. The comparison menu stays above neighbouring cards.
- A fresh stored-response submission completes the full reveal and returns to `scale(1)`. Idea/Thesis cards remain 440px wide; the Trigger is 320px. Its selected threshold is 70, current confidence 63, and status Not met. [Idea and Trigger preview](../../poc/reports/2026-10-26-trigger-card/idea-and-trigger.png), [full default view](../../poc/reports/2026-10-26-trigger-card/default-view.png).
- Lint, formatting and diff whitespace checks pass. The final portable build validates all 90 theses in 26.1ms and contains 168,295 JavaScript bytes, below the unchanged 200 KiB budget. No dependency was added. All three protected source hashes match the D181 baseline. This slice uses only the static-server fixture and stored responses; it makes no model call and changes no backend file.

Reasoning refresh: research universe → classification → Config → dispatch → extraction → thesis library → final verdict → pull mode → human-review intake → system overview keep their data paths, examples and acceptance criteria. The system glossary now names the frontend Trigger card without defining a new trading or execution rule. The frontend specification, ownership table, integration guide, decision and current state reference this one condition/lifecycle contract. The generated design page bundle needs only its normal PRD refresh. The final mechanical check is `python3 docs/check.py`.
