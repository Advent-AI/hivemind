# "Forecast unavailable" release, slice 2: the reader's page, built and checked at $0 (2026-11-23)

**Result: accepted by council 77b** (`codex-r77b.md`), after round 77. Slice 2 is built to `RELEASE-PAGE.md` revision 7, which council 76h found ready after eight rounds (76 to 76h). The
package now holds the reader's page, a pure function of its data (format `hivemind-release/2`). The $0 screen check of D756 passes:
- the stored number question `old-1/v8`, which has a forecast and a history, shows only its question, its sources and "Forecast
  unavailable";
- the two known Yes/No leaks show "Answer: Yes" without their explanations;
- every negative page is caught for its own reason.

Nothing is committed, published or deployed. The POC is unchanged.

- **Code:** `src/hivemind/release.py`: `page_template`, `render_page`, the format-2 package and its check.
- **Tests:** `tests/test_release.py`, tests 26–29.
- **Screen check:** `release_screen_prepare.py` and `release_screen.mjs` (in this folder).
- **Run:** `poc/data/release-screen-2026-11-23b/`: `screen-expected.json`, sha256 `7934eb2a…`, frozen before the run;
  `screen-results.json`; `old-1-v8.png`. The first run, `release-screen-2026-11-23/`, passed on the template before the one change
  below and is kept for the record.

## 1. No regressions

- **Full suite:** 429 passed. The 40 release tests are part of it, and so are the frozen-ruler guards.
- **Mutants:** 37 of 38 caught by failing tests, judged from each failure's full message. The six slice-2 mutants are caught:
  - the embed not escaping `<`;
  - the quote written with `innerHTML`;
  - the source address made a link;
  - the package page not compared with its data;
  - the page hash unchecked;
  - the CSP hash taken over another script.
- **The one miss** is the canonical-day mutant, equivalent on Python 3.10, as in slice 1.
- **The four-store check under format 2** (`release_check.py`, `poc/data/release-check-2026-11-23i/`) passes every item it names.
  Each forged copy carries the page made from its forged data:
  - the forged evidence summary passes the page check and fails comparison with the store;
  - the forged manifest fails earlier, because `note` is outside the manifest's allowed fields.

## 2. The screen check (design §6), headless Chrome 158 through its DevTools protocol

| Check | Result |
|---|---|
| `old-1` page, light | renders in 0.05 s (budget 3 s); one request, the page itself; no log error, exception or console error; zero links, `href` or `src`; background `rgb(245, 242, 235)` |
| `v8` collapsed | the whole read page equals the frozen page. The card reads "How much Data Center segment revenue will NVIDIA report for FY2027?", "Open", "Forecast unavailable", "1284 pieces of evidence" |
| `v8` expanded, then closed and reopened | the whole read page equals the frozen page with all 1,284 evidence groups, in order, grouped, each source as plain text |
| 390 px, dark | no horizontal scroll (390); background `rgb(15, 20, 13)`; the page with `v8` expanded equals the frozen page; Morningstar's quote wraps over 5 lines within the screen (36–374 px) |
| `old-3/v36` at 2026-08-25 | "Will NVIDIA begin shipping Rubin Ultra by December 31, 2027?", "Open", "Answer: Yes", "1 piece of evidence", and its one entry; nothing else |
| `old-1/v10` at 2026-08-28 | the Firmus question, "Open", "Answer: Yes", "1 piece of evidence", and its one entry; nothing else |
| Hostile quote (`</script><img onerror>`, `&`, U+2028) | shown exactly as text; no `img` element; no error |
| Size | the final `old-1` page is 5,794,595 bytes against 5,788,634 of data (budget: data + 64 KB) |

- **Every read text passed the not-clipped and contrast rules** in the scheme its visit used: no clipping ancestor, and at least
  4.5:1. `old-1` was read in light and in dark; each dated page in one scheme.
- **Every normal visit** (old-1 light, old-1 at 390 px dark, both dated pages, the escaping fixture) recorded exactly one request,
  the page itself, and no log error, exception or console error.
- **Each whole-page visit first read its card as rendered,** closed, before any toggle. These are the four visits of `old-1` and the
  dated pages. The escaping fixture was opened directly and checked for exact visible text, no `img` and clean signals.

**The negatives,** each a copy of the `old-1` page with its script changed and its CSP hash recomputed so the changed script runs:

| Negative | Caught by |
|---|---|
| a fetch of `http://127.0.0.1:59999/library` restored | the page rendered, and Chrome logged a `security` error naming the address and `connect-src` |
| "Forecast: $361 billion" added inside the `v8` card | the card read exactly the frozen lines plus that one line, and nothing landed in `other` |
| the same line added beside the card | the line landed in `other` |
| the list made transparent | all 47 cards existed, none was visible, the fallback was gone and no error was logged, so the 3 s deadline was missed for that reason |
| quotes clipped to one line | 1,220 texts clipped at 390 px |
| quotes in a one-line `contain: paint` wrapper | 1,284 texts with a clipping ancestor |
| the marker drawn dark on its own dark background, with light selected | all 19 markers below 4.5:1, the page around them `rgb(245, 242, 235)` |
| the marker drawn in the page colour, in dark | all 19 markers below 4.5:1 |

Council 77 required each normal visit to keep its requests and errors, each negative to keep the observation that earned it credit,
and the light-mode negative to select light. The check was corrected and re-run once against the same pinned page and the same frozen
expectation: zero failures. The browser profile now lives outside the run folder. The profiles of earlier runs were moved to the
scratchpad, not deleted.

**Measured, recorded in the design:** Chrome reports a CSP-blocked fetch as two log errors, not as a network request. A scratchpad
probe page named port 8788 once. Chrome refused it under the CSP before connecting, so nothing reached that service.

## 3. One change during the build

- **What.** The first screenshot showed a dangling comma when a source has no original day ("original: NVIDIA,"). The page now adds
  ", <day>" only when there is a day.
- **How it was re-certified.** That changed the pinned template, so the expectation was frozen again in a new folder
  (`release-screen-2026-11-23b`), the screen check re-run (zero failures, all eight negatives caught), and the new template hash
  pinned (`f94bb3cb…`, test 29).

**A pre-release departure, recorded (council 77).** The comma change altered the template under the same format 2, where revision 7
says a changed template gets a new format version. The earlier page was never released, and the current checker refuses it. The
format-version rule applies from the first release on.

**A second change, after acceptance: the labels (council 78/78b, D761).** Each evidence entry now shows "Hivemind summary" before the
summary and "Source quote" before the quote. This settles the evidence-summary disagreement by consensus.
- The expectation was frozen again (`poc/data/release-screen-2026-11-23c`, sha256 `30e8640f…`), with both labels in every expanded
  group.
- The screen check re-ran with zero failures: one request and no error on each of the five visits, and all eight negatives caught.
- The new template hash is pinned (`33fd58c6…`).
- Suite 429; the four-store check passes (`release-check-2026-11-23j`); mutants 37 of 38 (the equivalent miss).
- The format stays 2: council 78 judged a pre-release change acceptable under it.

## 4. Not shown, and still open

- **The idea path in the release** (council 74): deferred, its acceptance pending.
- **The evidence-summary disagreement** (`RELEASE-BUILD.md` §8): settled by consensus in councils 78/78b (D761).
- **Commit, publish and deploy:** Alex's.
