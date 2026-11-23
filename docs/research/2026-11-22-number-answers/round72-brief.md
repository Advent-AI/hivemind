# Council round 72 (the release-prep design for "Forecast unavailable"), read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

## Context
- **Alex's decisions:** D726 ("同意": a first release shows number questions with sources and "Forecast unavailable", the band, the
  forecast text and the history withheld together; "built with the release work, which is not started") and D756 ("结束这条线，预测暂缺上线").
  Both are in `docs/DECISIONS-log.md`.
- **Alex's direction for tonight** is quoted in D750: converge, no scope drift, head toward production. D439 governs: reversible, $0,
  nothing committed, never start what only Alex can launch.
- **The design:** `docs/research/2026-11-22-number-answers/FORECAST-UNAVAILABLE-DESIGN.md`.
- **The code:**
  - `src/hivemind/service.py` (`view`, `views`, `history`, `changes`, `evaluate`, `record`, `summaries`);
  - `src/hivemind/bundle.py`;
  - `src/hivemind/idea.py`;
  - `scripts/hivemind_api.py`, `scripts/hivemind_mcp.py`;
  - `poc/ui` (`prepare-data.mjs`, `src/adapters/bundle.js`).

## Questions
1. **Scope.** Is preparing this design tonight, without building it, the right step under Alex's direction and D726's "built with the
   release work, which is not started"? Or should it be built now, reversibly and uncommitted? Is starting the release work Alex's to
   launch?
2. **Completeness.** Does §4's reader table name every place a number question's band, forecast text or history reaches a reader?
   Search the code (bundle fields, idea composition, search ranking, any other export). Is the identity rule (a numeric `lo` or `hi`
   on any rung) right on the stored stores, and does it hold for every number question the product opens?
3. **Faithfulness to D726.** Is showing the ladder (the possible bands with their conditions) consistent with "the band … withheld"?
   Is the evaluate change right?
4. **The switch.** An explicit setting, with the default an open question for Alex. Is this the smallest correct course?
5. **Verdict:** design ready for release work as is, ready with listed changes, or not ready.

Return a numbered report with citations, then the verdict.
