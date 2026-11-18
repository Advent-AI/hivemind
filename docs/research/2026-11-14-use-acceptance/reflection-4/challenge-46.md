# Round 47: version 2 (written; re-read). Go or no-go.

`page-contract/LIVE-READ-DESIGN.md` version 2. A: the library has no date control of its own (its day is set only at creation and in
`setDataset`; searched), so the one automatic read at start shows the served `as_of` via `setDataset(input, { day })`; other replacements
keep the verified clamp; a failed read keeps the embedded snapshot as specified (recorded for Alex). B: enforced, not only written: the
API and the MCP server refuse to start on a store that records processing steps and no completed day (`service.first_day_unfinished`),
legacy ledgers start as before, a crash-left store is refused the same way; completed days only grow, so a start check is the whole
guard; tests through the real entry points (the API process both ways, the MCP process refusing). End with `CONSENSUS: yes` or `CONSENSUS: no, because …`.
