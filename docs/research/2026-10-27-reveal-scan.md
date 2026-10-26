# D227 · Reveal down the thesis column without returning to the Idea

Alex wants to read the reveal from top to bottom, with no repeated pan back to the Idea. At the start of this slice, the controller visited the connection's source before every target, then followed the path from that source. The three-thesis-plus-Trigger graph made three unnecessary returns to the Idea. The same loop affected every connected result; stored examples had three and thirteen connections, producing two and twelve unnecessary returns respectively. Empty results had none.

Keep the current card/connection order and parent-before-child grouping, which already put the default thesis column in displayed top-to-bottom order. Start with the Idea, move once to the top of the thesis column, then move directly from the current camera position to each next target's vertical position. Hold horizontal focus on that column. Keep drawing each actual incoming line from source to target. The line animation no longer dictates the camera path. Return to the existing balanced overview once, after the final target. D228 places the Trigger left of the Idea; D229 reveals it last after the overview return, outside the thesis scan.

## State × event

| State/event | Required transition |
|---|---|
| Completed result | Existing Idea entrance |
| First connection | Draw line while moving from Idea to first target |
| Later connection | Draw line while continuing from current camera to next target; no source visit |
| Target reached | Existing card entrance and short pause |
| Last target | Existing single return to balanced 100% overview |
| Empty result | Idea entrance and overview; no column movement |
| Pointer, wheel, replay, range, resize, replacement, hide or teardown | Existing cancellation: expose all cards, no stale camera updates |
| Reduced motion | Existing immediate completed view |

## Values, readers and checks

| Value | Owner / reader / proof |
|---|---|
| Card order | Canvas layout → existing reveal sequence; check the stored default graph and Trigger have ascending target heights |
| Camera start | Current canvas pose → each line tween; browser frames must not return to the Idea between targets |
| Column focus | First target column's widest card centre → all target movements; browser frames hold the same x after the first target |
| Line progress | Existing path length → stroke dash offset; retain partial-line frames and hidden-until-arrival targets |
| Final pose | Existing tree bounds → one return; retain native scale and balanced margins |

D223's per-connection source visit is superseded. Its line direction, target entrance, parent/child order, one-shot behaviour, cancellation and final overview remain. D228 owns the corrected Trigger position. No data, weights, thresholds, backend or service call changes. Claude's backend work and separate cleanup branch are out of scope.

Self-review: merely deleting the source tween would still jump the camera to the source at the next line's first frame. Start every camera tween from its actual current pose and stop using the line head as camera input. A narrower Trigger must not cause sideways camera movement. Check the real frame sequence and reject the old source-following camera as a scratch mutation. Use stored responses only.

## Verification

- The final stored-response browser run reveals `idea → v3 → v9 → v1`. It judges 158 scan frames: horizontal translation remains -420px after reaching the thesis column; the target translations move down from 183.5 to -220.5 to -624.5px. No source phase occurs. Partial line drawing and hidden-until-arrival targets still pass. The final view is balanced at 100% zoom. Frame samples (local artifact: `../../poc/reports/2026-10-27-reveal-scan/frames.json`).
- Replacing only the reveal controller in a scratch bundle with the prior implementation fails with `Camera returned to a connection source`; the current control passes. The final build also passes Fit cancellation, replacement, teardown and the empty result.
- All 52 frontend tests and 17 existing mutation checks pass, including default top-to-bottom target order and the corrected left-side Trigger layout. Lint and formatting pass. The final portable page contains 168,260 JavaScript bytes and validates 90 theses in 25.0ms, within the existing budgets. All browser work uses stored fixtures with no model calls.

Reasoning refresh: research universe, classification, Config, dispatch, extraction, thesis storage, final verdict, pull mode, human review and system semantics remain unchanged. The frontend contract, integration guide and current state now describe the direct vertical scan and link to this camera decision. D223 retains ownership of cancellation and other timing. No governing PRD block needs a semantic change.
