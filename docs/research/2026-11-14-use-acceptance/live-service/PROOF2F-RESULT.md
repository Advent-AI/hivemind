# Proof 2f: the page's day reaches the Idea call (D602), 2026-11-16, $0

`poc/ui/verify-live-day.mjs` builds two check pages from the demo page `poc/mock/index.html`, whose embedded snapshot is dated
2026-08-28. `proof2f_run.py` serves them and loads each in headless Chrome, where the checks run on load (`proof2f-output.txt`).
`fetch` is stubbed in the existing verifiers' pattern. The library and bundles are real: they come from the ledger the stored card
was made from (`english-v23-jev-2026-10-25`, last completed day 2026-08-15, the card's own day), through the product's `bundle`
functions.

- **A, the live read succeeds** (`/library` answers that ledger's library, as of 2026-08-15):
  - the library counts the served 90 questions;
  - the Idea is sent as of 2026-08-15;
  - the question bundles are asked as of 2026-08-15, which exercises `readBundles`;
  - the three chosen questions are drawn;
  - no page error.
- **B, the live read fails** (`/library` answers 503):
  - the page keeps 2026-08-28 and sends the Idea as of that day;
  - the stub answers as the real API does for a day after the store's last completed day: 409 `{"error": "day not completed",
    "requested": ..., "last_completed_day": ...}`, JSON;
  - the Idea error is shown;
  - no bundles are asked;
  - the library is unchanged (68 questions; the same 24 cards on its first page);
  - a second sentence is sent again, as of the same day, and its error is shown;
  - no page error.
- **Scope of "nothing else breaks":** exactly the checks above, not every behaviour of the page.
- **Mutant M1** (the built page sends no `as_of`): both cases fail, so it is caught.
- **Also run:** `npm --prefix poc/ui run lint` and `format:check` pass, and the UI's own tests pass (70).
- **No product code changed.**

## My errors, each caught by a failing check and traced before the fix

- The checks first waited on animation frames, which headless Chrome did not deliver; they wait on timers now.
- I asserted the library's 94 views as cards, but the library pages its cards 24 at a time. It now checks the library's own count.
- I first served the sealed run's store, which does not hold the card's composite questions. The page's composite then threw, and the
  Idea showed as failed. Traced in Node: `prepareIdeaComposite` raises "Composite entries must identify unique connected theses"
  with those bundles, and works with the card's own ledger.
  - **Observation, not a defect claim:** a composite error other than `CompositeUnavailable` marks the whole Idea failed, as the code
    is written (`bootstrap.js`).
