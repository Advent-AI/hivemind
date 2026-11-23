# Round 45: serving while writing, run. Two findings; decide what to do with each.

`page-contract/SERVING-WHILE-WRITING-RESULT.md`, `serving-while-writing.txt`, `serving_while_writing.py`. Held: no partial day leaks into
the completed-day view (mid-day equals the previous day's view, twice); completion and closing dated right. Failed checks, both
findings on existing code paths:
1. **First day:** before any completed day, `/library` serves the in-progress day (as of 2026-09-22, its judgements) via
   `service.default_as_of`'s fallback to the latest judgement's day; `/days` gives none.
2. **The page's date on the live read:** `library.setDataset` keeps the embedded day clamped to the new history (verified behaviour,
   `verify-library.mjs`); a fresh page opens on the shell's day (or the new library's first day), not on the latest completed day.
   `thesis-ui.md`: "The supplied snapshot defines the displayed date".

Proposed (attack): (1) a store that records days (any processing step) and has no completed day serves no library by default
(`default_as_of` gives None there, so `bundle.library` refuses "no completed day; supply as_of"); a legacy ledger without day records
keeps the fallback; test both; (2) the startup's automatic live read (`bootstrap.loadLibrary`, the one place an embedded snapshot is
replaced by the served one) shows the served snapshot's `as_of`; later replacements keep the verified clamp; a new library option
`setDataset(input, { day })` or equivalent, tested and checked in the browser. Both $0. End with `CONSENSUS: yes` (build as proposed)
or `CONSENSUS: no, because …`.
