# D183: inline Idea send control

Alex asked for an arrow send button inside the Idea input: grey and disabled when blank, black when text exists, Enter to send. Current census: one Idea form, one external Explore submit button, one submit handler. The existing native form already supports Enter and trims blank input; presentation and button state are missing.

| State / event | Button and submission |
|---|---|
| Empty or whitespace input | Grey, disabled; Enter sends nothing |
| Nonempty input | Black, enabled; click or Enter uses the same native form submit handler |
| Request pending | Disabled while the existing request is in flight; form announces busy |
| Answer, failure or cancellation | Recompute from current input; retain draft text |
| Switch away and back | Existing cancellation applies; recompute on entry |

The template owns one accessible Send idea button and input wrapper. Bootstrap owns enablement from trimmed input and its existing in-flight request. CSS owns shape, colour and focus. The existing request, response, archive, dataset and graph paths do not change. D130 component ownership, D182 sentence case and no native hover titles remain in effect. No new dependencies.

Verify blank/whitespace/typed states, arrow bounds, focus, native Enter and a completed response in the real browser. Reuse the already-cached user query and confirm model archive row counts do not increase. Run existing UI tests, lint/format and Python suite once; refresh the UI documentation and run docs/check.py last.

During the real-browser check, the initial library read completed after navigation to Idea and called `showLibrary()`, hiding the input mid-interaction. This occurs for the entire class “initial read completes after user navigation”, independent of input text. The read is not a navigation event: it replaces library data without changing the user's current view or cancelling their Idea request. Add that state/event row and verify navigation remains on Idea after the read. No old Idea response is merged into the library.

Alex subsequently requested half the width and bar separators in library statistics. The composer cap changes from 1000px to 500px while width remains responsive. The three existing statistics use two shared `SEP` elements. Browser checks measure both the width and separator count.
