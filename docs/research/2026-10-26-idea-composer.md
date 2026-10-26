# D219 · Floating Idea input

Move the existing input onto the canvas, centred horizontally 24px above its bottom edge. Submission centres the whole Idea/thesis tree in the canvas at 100% zoom for readability and balanced horizontal whitespace (D221/D222) and folds the input into a circular TrueNorth-logo button at bottom right. The existing logo asset supplies the mark. All thesis cards and connections remain available by panning or Fit to view.

The launcher uses a black mark on a white, borderless 44px circle (D220). Hover and keyboard focus increase only its soft shadow; neither adds an outline.

## State × event

| State/event | Result |
|---|---|
| Library → Explore an idea | Show the canvas and expanded input; focus the input |
| Expanded → submit nonempty text | Capture text/date, clear input, collapse to logo; create centred pending card |
| Pending → progress | Update the card without moving the camera; logo stays available |
| Pending → success/error | Centre the completed/error Idea card; preserve existing result/error handling |
| Collapsed → logo click | Expand the same bottom-centred input and focus it |
| Expanded → outside pointer / Escape | Collapse; retain an unsent draft; Escape returns focus to the logo |
| Pending → reopen | Allow drafting; existing in-flight submission guard remains |
| Any canvas state → Library | Hide both input and logo; retain existing request cancellation |
| Resize / replay / pan / Fit | Input/logo stay anchored; replay preserves the camera; Fit still shows the graph |
| Page teardown | Remove composer event listeners with the existing teardown |

## Values and readers

| Value | Owner and readers |
|---|---|
| Expanded/collapsed | Composer controller → form visibility, logo visibility/ARIA, narrow-screen zoom-control spacing |
| Draft text | Existing input → submit handler; collapse never discards it |
| Submitted text/date/request generation | Existing bootstrap → request, progress, card and detail |
| Explicit `centerOn: 'tree'` | Idea submit → canvas camera only; default component callers retain graph fitting |

D183 owns the existing send/Enter and in-flight guard. D187 owns progress/cancellation. D213 owns equal card widths and D218 the shared detail controls. This changes their placement and initial camera focus only; service calls, confidence, weights, card relationships and history remain unchanged.

D221 supersedes the initial fit-scale choice: default generation shows the Idea at 100% zoom, even if related cards extend offscreen. Manual Fit to view still fits the whole graph.

Verify the real browser path: initial position, empty input, submit and logo fold, actual cached response, card centre, reopen/draft/outside click/Escape, library switch, replay and Fit. Check narrow-screen control overlap and source database hashes. Run existing frontend and Python suites and the documentation check. No paid model calls are needed.

Self-review: form and logo stay outside the pannable world; outside-click handling must ignore both controls and must not steal focus from a clicked card. A range/replay update must not re-centre a viewport the reader has moved. No other module changes are needed.

## Verification

- D219's 1920×873 browser check: input is 500×46, horizontally centred with 0px error and 24px above the canvas bottom. The launcher was 56×56 with 24px right/bottom gaps; D220 reduces it to 44×44. The completed Idea's horizontal centre error is 0px; vertical rounding error is below 0.001px.
- The cached NVIDIA response still has four cards, 55% / 25% / 20% weights and 61% confidence. Replay still shows 50% at the beginning and 61% at the end.
- Logo click focuses the input; a new draft survives outside click, Escape and switching to Library and back. Clicking inside the input does not fold it. Fit folds the input and retains its normal graph behaviour. The Idea detail still opens on Overview.
- The logo renders with `brightness(0)`. A real pointer hover retains the same `rgb(201, 199, 192)` border while the shadow changes. The button stays collapsed on hover.
- At the narrow breakpoint, moving the zoom controls to a 94px bottom inset leaves 24px above the 46px-high input at a 24px bottom inset. This is a CSS geometry check; the browser interaction checks used the desktop viewport.
- 47 frontend tests, lint/format and the full 165-test Python suite pass. The portable build validates 90 theses in 24.9ms and contains 159,880 JavaScript bytes, below the existing 200 KiB budget.
- All three protected source database hashes are unchanged. The Idea archive remains at nine calls; browser verification used cached responses only.

Screenshots: [input](../../poc/reports/2026-10-26-idea-composer/input.png), [submitted](../../poc/reports/2026-10-26-idea-composer/submitted.png), [reopened](../../poc/reports/2026-10-26-idea-composer/reopened.png), [monochrome launcher](../../poc/reports/2026-10-26-idea-composer/launcher.png).

Reasoning refresh: the module sequence in the PRD index is unchanged. This presentation change does not affect universe, classification, Config, dispatch, extraction, stored thesis identity, verdict, pull mode or review intake. The system's score definition is unchanged. The frontend specification and current state now describe the new input/launcher behaviour; no governing page data changes are needed.

## D220–D221 follow-up verification

- The launcher measures 44×44px, has a white background, 0px border and `outline-style: none`. Its click and Escape interactions still work; hover and keyboard focus use shadows.
- Generation now displays the 440px Idea card at 100% zoom, with zero horizontal and vertical centre error in the canvas. Manual Fit reduces it to 261.11px for this four-card graph; generating another Idea restores 440px. This verifies the default does not retain the prior fit zoom.
- All 47 frontend tests, lint and format checks pass. The standalone page validates all 90 theses and contains 159,883 JavaScript bytes. These changes touch only presentation and camera positioning.
- Latest screenshots: [readable default](../../poc/reports/2026-10-26-idea-composer/default-readable.png), [smaller borderless launcher](../../poc/reports/2026-10-26-idea-composer/launcher-small.png).

## D222 centering scope

The measured four-card tree spans 1,060px. Centering the Idea alone produced left/right gaps of 740px/120px. The three existing pending/success/error render calls now request tree centering. The shared card bounds supply both this 100% default and the existing manual Fit calculation. Date replay and progress updates do not reset the camera. Verify 430px/430px gaps on the same response, unchanged 440px card widths and normal manual Fit behaviour.

Verified in the actual browser: all four cards remain 440px wide, the tree remains 1,060px wide, both side gaps are 430px, and horizontal centre error is 0px. Replay preserves the view. Manual Fit still produces a 261.11px Idea card; another generation restores 440px cards with balanced side gaps. All 47 frontend tests, lint and format checks pass. [Balanced default view](../../poc/reports/2026-10-26-idea-composer/balanced-tree.png).

The D222 reasoning refresh affects only camera placement and its frontend descriptions. The PRD module sequence, stored data and score semantics remain unchanged.
