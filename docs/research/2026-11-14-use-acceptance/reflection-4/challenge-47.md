# Round 48: A is built and proved; B, version 3. Accept A; go or no-go on B.

**A** (built as approved): `library.setDataset(input, { day })`; `bootstrap.loadLibrary` passes the served `as_of`; two lifecycle checks added
to `verify-library.mjs` ("a supplied day is shown instead of the kept one"; "without a supplied day the kept day stays"); in headless
Chrome the library check passes 11 of 11 (`page-contract/library-check.txt`). On the way: the check embeds the committed demo page's
script, which an old build cannot validate with the new fields (the coordinated upgrade the design states): the demo page was rebuilt
by the README's default command; lint and format checks pass after formatting my edits (the committed files were already formatted;
one unused import removed). UI 70, `npm run build` 186,654 bytes.

**B** version 3 (`page-contract/LIVE-READ-DESIGN.md`, last section): the check on every read, at the one place each entry point opens
the ledger per request (the API's `Connections.__enter__`; a wrapper on each MCP tool), 503 "the store's first day has not completed",
no `as_of` bypass, empty and legacy stores read as today, crash-left stores refused while in that state; tests through one running API
process across the three states (empty, first day unfinished, first day completed) and the MCP tools on the same states.

End with `CONSENSUS: yes` (accept A; build B as written) or `CONSENSUS: no, because …`.
