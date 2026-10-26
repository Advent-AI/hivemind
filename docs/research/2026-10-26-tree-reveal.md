# D223 · Animated Idea tree reveal

On a completed Idea request, show the Idea first, trace each connection from source to target and reveal the reached thesis. Keep the response's displayed root order, including impact-weight ordering. A root's related children follow that root before moving to the next. The camera now scans directly down the thesis column under [D227](2026-10-27-reveal-scan.md), without revisiting sources. End at the existing 100% view centred on the whole tree, then reveal the left-side Trigger and its connector last under [D229](2026-10-27-trigger-last.md).

## Ownership and sequence

The canvas still owns layout, connections, pan and zoom. A cancellable reveal controller owns its temporary opacity, stroke offsets, timing and camera interpolation. Bootstrap requests a reveal once on the completed graph; the flag is not retained in replay or dataset state. No API, scoring or model changes.

Timings: 360ms Idea entrance; 650ms line drawing while the camera moves to the next target; 280ms target entrance; 140ms pause; 650ms return to the default view. D227 removes the per-connection source visit. These are design timings, not measured performance. There is no per-thesis count limit. Reduced-motion preference shows the finished graph immediately.

## State × event

| State / event | Transition and effect |
|---|---|
| Pending request → progress | Existing progress card; no tree reveal |
| Completed result → reveal | Build all final geometry; hide targets/lines synchronously, centre Idea and reveal it |
| Next target → trace | Animate path left-to-right along its real shape; camera moves directly from its current pose; arrow appears on arrival |
| Trace complete → target | Fade/slide target into view, then visit its children or next root |
| Last target → complete | Smoothly return to the whole-tree default at 100%; clear temporary styles |
| Empty adopted set | Reveal only the Idea, then settle |
| Reduced motion | Show all cards and connections at their final view without camera travel |
| Pointer interaction / wheel / replay / range / resize | Cancel reveal, expose the complete graph, leave camera at its current position for the user's action |
| Detail opened / new submission / dataset replacement / destroy | Cancel animation and queued work; no later callback may affect the new graph |
| Request failure | Existing error card; no invented connection animation |

## Values × readers and checks

| Value | Owner / readers | Check |
|---|---|---|
| One-shot reveal option | Bootstrap → explorer → canvas; omitted from stored graph | Replay does not restart it |
| Reveal sequence | Existing graph edges → controller | Real stored graph: each parent before its children; no omitted/duplicated edge |
| Temporary card/path styles | Controller only | Completion and cancellation expose every card/edge and remove temporary styles |
| Camera pose | Canvas getters/setters; reveal and manual controls | Following changes continuously; completion restores native zoom and balanced tree margins |
| Run cancellation signal | Controller → frame promises | Cancelling one run cannot move/reveal a replacement graph |

D187 owns request progress; D213 owns card width; D220 owns the launcher; D221/D222 own the final camera view. The reveal changes none of those contracts. Self-review: suppress the existing automatic card fade during the reveal, suppress unarrived arrowheads, keep unrevealed cards inert, and separate the reveal option from the graph retained by date replay.

Verify stored-edge order in the frontend suite and with a mutation returning the original breadth-first edge list. Use real-browser checkpoints for entrance, partial path, target arrival, camera following, final pose, cancellation, replacement, empty result and reduced motion. Reuse cached responses; no model call is needed.

## D223 verification before D227/D228

- 48 frontend tests pass. The new stored-data test checks all 13 connections, including each root's related children. All 14 scratch-copy mutation checks reject their defects, including a breadth-first reveal-order mutant.
- The real-browser fixture passes the complete sequence, partial line frames, camera following, final 100% scale, cancellation through Fit, graph replacement, canvas destruction and an empty result. A separate early-visible-target mutant fails with `Target appeared before its line arrived`; the unmodified control passes.
- A scratch build forcing the reduced-motion branch with its matching no-transition CSS shows all cards immediately at 100%, with no reveal controller running. This checks the branch, without changing the operating system's motion preference.
- The actual cached NVIDIA request displays only the Idea at first, with the first line drawing while its target remains hidden. On completion all four cards are 440px wide, the side margins are 430px each, and temporary stroke/marker styles are cleared. Historical replay does not restart the reveal.
- A native drag during the Idea entrance cancels the live sequence. The complete graph becomes visible and the camera remains at the drag position after the old sequence would have continued.
- The full Python suite passes: 165 tests. Lint and formatting pass. The portable page validates 90 theses in 25.8ms and contains 163,577 JavaScript bytes, within the existing 200 KiB budget. No dependency was added.
- All three protected source database hashes remain unchanged. The local archive's three newest calls belong to the separately submitted China question; verification of this animation reused the cached NVIDIA response.

The test harness initially mis-inserted a bundled script through string replacement and was corrected to insert it literally. The reduced-motion scratch fixture also needed the matching CSS branch. Neither issue changed product code. One short phase screenshot was missed; the frame-sampling browser check recorded and verified the complete sequence instead.

Screenshots and frame samples: [Idea first](../../poc/reports/2026-10-26-tree-reveal/idea-first.png), [line drawing](../../poc/reports/2026-10-26-tree-reveal/live-line.png), [final view](../../poc/reports/2026-10-26-tree-reveal/final.png), sequence samples (local artifact: `../../poc/reports/2026-10-26-tree-reveal/sequence.json`). `node poc/ui/verify-reveal.mjs` rebuilds the browser verification page from stored fixtures.

Reasoning refresh: universe, classification, Config, dispatch, extraction, stored thesis identity, final verdict, pull mode and human-review intake retain their contracts. The system's confidence definition is unchanged. The frontend specification, ownership table and current state now describe the one-shot reveal and its cancellation; no governing page data changes are needed.
