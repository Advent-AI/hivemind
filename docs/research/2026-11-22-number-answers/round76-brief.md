# Council round 76: review the slice-2 design (the reader's page) before any code (read-only)

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

## What to review

`docs/research/2026-11-22-number-answers/RELEASE-PAGE.md`, the design for slice 2 of the "Forecast unavailable" release. Slice 1 is
built and accepted (D759 at the end of `docs/DECISIONS-log.md`; `RELEASE-BUILD.md` revision 11; `RELEASE-CHECK-RESULT.md`;
`src/hivemind/release.py`, `scripts/release_build.py`, `tests/test_release.py`). D756 asks for a $0 check of the reader's screen on
a stored number question with a forecast and history: only the question, its sources and "Forecast unavailable" appear. D758
ordered the exporter first, the screen second. Council 74 deferred idea submission.

## Questions

1. **Leaks.** Can anything other than the package data reach the reader's screen, or any network request leave the page? Consider:
   the CSP, inline script and style hashes, `file://` origin rules, links, `<details>`, `noscript`, the escaping of the embedded JSON.
2. **The page = `render_page(data)` rule.** Is that the right structural check for the page? Is it sound with a read-once package? Is
   the format bump to `hivemind-release/2` the right handling?
3. **The screen check (§6).** Will CDP on headless Chrome show a CSP-blocked fetch as a request or a violation? Is the v8 screen
   assertion set right, and literal enough (council 75d's rule)? Is the budget set before the control?
4. **The tables (§2–§4) and tests (§5).** Is any cell blank or wrong? Is any test unable to fail without its code?
5. **Scope.** Is anything in this design scope drift beyond D756/D758, or a change to the POC?
6. **Verdict:** ready to build, or not ready with each serious finding.

**Out of scope:**
- the frozen judging, opening and extraction pieces;
- the closed v13s line;
- slice 1's accepted internals, unless slice 2 breaks them;
- the idea path;
- the recorded evidence-summary disagreement;
- wording.

Report only findings that change what is built or whether it is safe.
