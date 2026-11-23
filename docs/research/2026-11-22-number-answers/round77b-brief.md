# Council round 77b: review the built slice 2 (the reader's page) against its design, and its $0 result (read-only)

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

Round 77 (`codex-r77.md`) did not accept slice 2 on three browser-check gaps; Claude corrected the check and re-ran it once against the same pinned page and frozen expectation, and corrected the result page. Slice 2 was built to `docs/research/2026-11-22-number-answers/RELEASE-PAGE.md` revision 7, which council 76h found ready. The pieces:
- `src/hivemind/release.py`: `page_template`, `render_page`, `embed`, the format-2 `write_package` and `check_package`;
- `tests/test_release.py`: tests 26–29, and the format-2 updates to earlier tests;
- `release_screen_prepare.py` and `release_screen.mjs`;
- the run `poc/data/release-screen-2026-11-23b/`: `screen-expected.json`, `screen-results.json`, `old-1-v8.png`;
- the result: `RELEASE-PAGE-RESULT.md`;
- the mutants: `release_mutants.py`;
- the four-store check: `release_check.py`, run `poc/data/release-check-2026-11-23i/`.

## Questions

1. **Are the three round-77 findings closed?** Then: does the code do what revision 7 specifies? Name each departure with file:line, and whether it is unsafe.
2. **Can the shipped page leak anything not in its data, make a request, or show the reader something other than the frozen screen?**
   Look at the actual template and script, not only the design.
3. **Do the screen check and its negatives judge what they claim?**
   - Is the frozen expectation independent of the page under test?
   - Does each negative fail for its own reason?
   - Is the "measured" CDP behaviour recorded faithfully?
4. **Do the claims in `RELEASE-PAGE-RESULT.md` follow from the saved results?**
5. **Verdict:** slice 2 accepted, or not accepted with each serious finding. Optional tightenings are listed as optional (AGENTS §5;
   further checks against hypothetical CSS were judged optional in 76g/76h because the whole template is pinned).

**Out of scope:**
- the frozen pieces;
- the closed v13s line;
- slice 1's accepted internals, unless slice 2 breaks them;
- the idea path;
- the evidence-summary disagreement;
- style.
