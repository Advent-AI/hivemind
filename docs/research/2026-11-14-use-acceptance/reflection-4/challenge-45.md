# Round 46: the two findings, designed. Attack before any code.

`page-contract/LIVE-READ-DESIGN.md`:
A (built): the first successful automatic read shows the served `as_of`, unless the person changed the date while it was in flight;
later replacements keep the verified clamp; a failed read keeps the embedded snapshot (as specified). Owner: `library.setDataset(input,
{ day })` plus a record of whether the person changed the date; `bootstrap.loadLibrary` passes the served day. Proof: tests with and
without the day, the clamp check unchanged, the paused-writer page check asserting the displayed day and question identities, a delayed
response with a date change, the production shell against a new-system store.
B (not built): every reader of `default_as_of` listed (library, thesis bundles, Idea, search, the service's views, view, evidence,
history, changes, day items, evaluation, MCP's start); census 0 of 143 stores in the first-day state; an operating rule instead: serve a
new-system store only after its first day completes, written in `docs/poc/service.md`; the reader table kept as the input of any later
change.

End with `CONSENSUS: yes` (build A, record B as proposed) or `CONSENSUS: no, because …`.
