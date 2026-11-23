NOT READY — the contract review is incomplete; I cannot give it a clean pass yet. I found no new serious defect in the parts I reached.

Both findings from [the previous contract review](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/council/hr-codex.md) are addressed in the text: the number parser now rejects an extreme exponent before converting it to a decimal, and fixture 8 consistently uses `clean-99` and `v99`. The parser’s handling still needs the specified entry-point test when the step is built.

I ran all eight answers through production’s `model.check_schema`: all eight passed. Checks 1–8 are not implemented yet, so their results below are a reading of the design, not a run of the step.

| Fixture | Designed checks 1–8 | Displayed `written` projection |
|---|---|---|
| 1. Company yes/no | Pass | Matches |
| 2. Company yes/no, omitted parts | Pass; due day is exactly 548 days after the article | Matches |
| 3. Company states | Pass | Matches |
| 4. Theme states | Pass as a code fixture | Matches; the fixture records known substantive faults for readers |
| 5. Company figure, lower favourable | Pass | Matches |
| 6. Theme figure with reference | Pass; the quoted reference occurs in the stored article | Matches |
| 7. No ladder | Pass | Displayed fields match |
| 8. Company figure, higher favourable | Pass | Matches, including `v99` |

The [schema validator](/Users/lchingen/hivemind/src/hivemind/model.py:179) enforces the declared types, required fields, patterns and enums; it does not enforce exactly five entries. The design assigns that and the other cross-field rules to new checks. Production’s [bounds check](/Users/lchingen/hivemind/src/hivemind/extraction.py:493) alone does not establish an open lower end or exact-decimal comparisons; the design explicitly adds both. The [write table](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:517) is consistent with the displayed projections I walked.

I did not find an answer that necessarily escapes every reader mark: [W](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md:71) allows a reader to name another misleading fault. That does not prove a reader will notice every fault. I did not identify a place in the reached contract text that necessarily requires two different builds.

**Not reached:** the individual source and reader-answer rows in `dryrun/`, `dryrun2/` packet A, `dryrun3/`–`dryrun6/`, `dryrun8/`, and `reference/`; in `dryrun7/`, I checked fixture 6’s article passage but did not independently walk all reader-answer rows. Those remain necessary before calling this angle ready.