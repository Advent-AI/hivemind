# Round 142: proof 10 passed (D601, `live-service/PROOF10-RESULT.md`); proof 2f's design

## Proof 10

- **All 23 checks hold** (`proof10-output.txt`).
- **The first day:** `/days` and `/library` are 503 with the first-day body, and MCP refuses.
- **Six later pauses:** MCP's day and ids equal `/library`'s.
- **All seven pauses:** the lock is held, preflight refuses naming the snapshot route, and the store is in WAL.
- **Both snapshot states** are correct, out of WAL, integrity ok.
- **The poller:** 169 answers in 5.7 s, spanning the writer's whole run. The replay completes about 190 days in about 5.4 s; days
  without articles take almost nothing.
  - 9 were first-day 503s, and 160 were 200s over 16 distinct days.
  - The days never went backwards, and each answer equals its dated read.
  - 8 were in flight during a completion, and 10 transitions were seen directly. The harness's own "162 completions with answers on
    both sides" counts any earlier and any later answer, so it is loose and I do not use it as evidence.
- **After the writer:** the lock is free, the store is out of WAL, and the API answers as of 2027-04-02.
- **My error:** the first run stopped on my query of a nonexistent `view_switches.day` column. The January state is now asserted by
  which questions are closed.

## Proof 2f, proposed

The contract's line: the page verifier (`poc/ui/verify-*.mjs`). With the live read successful, the Idea call succeeds. With the live
read failed and a later embedded day, the Idea error shows and nothing else breaks.

**What the page does today** (read):

- `bootstrap.js` sends the Idea with `asOf: library.getDay()`.
- `library.getDay()` is the served `as_of` after a successful live read (`setDataset(next, {day: next.as_of})`). After a failed read,
  it stays the embedded snapshot's day.
- `idea.readIdea` throws `IdeaError(status, body.error)` on any non-200 answer.
- The API answers a later date with 409 `{'error': 'day not completed', 'requested', 'last_completed_day'}` before any header. This
  is tested at the real API in `tests/test_live_reads.py`.

**A new verifier, `poc/ui/verify-live-day.mjs`,** in the existing pattern: it stubs `fetch`, builds on `mock/index.html`, and runs in
headless Chrome by an auto-click copy as before. Two cases:

- **A, the live read succeeds:** `/library` answers a fixture library as of day L, earlier than the embedded day E. The stubbed
  `/ideas` records the request's `as_of`.
  - The Idea sent `as_of == L`.
  - The stored card is shown.
- **B, the live read fails** (`/library` answers 503): the page keeps E. The stubbed `/ideas` answers exactly what the real API
  answers for E: 409, the JSON body above, `Content-Type: application/json`.
  - The Idea sent `as_of == E`.
  - The Idea error is shown with the service's message.
  - The library's cards and day are unchanged.
  - The Idea input accepts a second sentence, which sends again.
  - No uncaught page error (`window.onerror` and `unhandledrejection` counted).

**Then:**

- `npm --prefix poc/ui run lint` and `format:check`;
- one mutant: the page sends no `as_of`, so case A's check fails.

**No product code change is planned.** If B shows the page breaking, that is a finding, brought back before any fix.

**Asked of you:** is the 409 body in the stub faithful to the real API? Is "nothing else breaks" specified enough? Is there a
day-related path of the page (the chart, `readBundles`) that should be in the check?

End with `CONSENSUS: yes` (build and run 2f) or `CONSENSUS: no, because …`.
