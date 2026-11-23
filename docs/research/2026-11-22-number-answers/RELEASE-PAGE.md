# "Forecast unavailable" release, slice 2: the reader's page (design for council round 76)

**Status: revision 7, ready per council 76h; built and screen-checked** (`RELEASE-PAGE-RESULT.md`; build review in council 77).
During the build, the evidence detail line was changed to add ", <day>" only when the original day exists. The template was
re-certified by a new screen run and its hash re-pinned. Then, by council 78/78b (D761), each evidence entry was labelled "Hivemind
summary" and "Source quote". The template was re-certified again (`poc/data/release-screen-2026-11-23c`) under format 2, still before
any release.

**Revision 7 answers `codex-r76g.md`:**
- **Contrast starts at the text's own element.** Its background is its own non-transparent `background-color`, or else the nearest
  ancestor's. A marker with dark text on its own dark background inside a light card fails.
- **The whole template is pinned.** `page_template()` is the complete page text with the CSP filled and one data placeholder;
  `render_page` splits it at that placeholder and inserts the escaped data. The test pins the sha256 of `page_template()`, so a
  change to any part of the page, the fallback sentence included, fails the pin until re-certified.

Council 76g judged further checks against hypothetical CSS optional once these are in: a template change already fails the pin.

**Revision 6 answers `codex-r76f.md` with general rules instead of one patch per trick** (AGENTS §1: "certify what the reader can
read" drew a new finding in 76c, 76d and 76f):
1. **No clipping ancestor.** No element between a read text and `body` may clip it: computed `overflow-x` or `overflow-y` other than
   `visible`, `contain` holding `paint`, `strict` or `content`, or `clip-path` other than `none`.
2. **Contrast.** Every read text has a contrast ratio of at least 4.5:1 between its computed colour and its effective background (the
   nearest ancestor with a non-transparent background), in light and in dark. This is WCAG's AA level for body text.
3. **The template is pinned.** The sha256 of `PAGE_STYLE` and `PAGE_SCRIPT` are literals in the tests. The screen check certifies
   that exact template, and any template change fails the tests until it is re-certified by a new screen run and a new format
   version.

**Revision 5 answers `codex-r76d.md`:** no text may be clipped.
- The template's stylesheet uses none of `overflow`, `clip`, `text-overflow`, `line-clamp`, `max-height` or `nowrap`.
- In the browser, every block element holding read text shows all of it. This is checked at desktop width and at 390 px, with the
  stored Morningstar entry as the test.
- A clipping copy is added as a negative page.

**Revision 4 answers `codex-r76c.md`:**
- the screen check compares the whole page's visible text, header and every card, with a frozen list; any text outside a known place
  fails;
- visibility is one test, `checkVisibility` with opacity and visibility, for the evidence and for the timer;
- the template's stylesheet draws no text (no `content`);
- a sibling forecast line and a fully transparent list are added as negative pages.

**Revision 3 answers `codex-r76b.md`:**
- the screen check compares every visible text of each checked card with a frozen list, in order and grouped by evidence, so an
  extra line fails;
- each dated card is frozen from its own dated package;
- the timer stops when the list is visible;
- the dark background is the literal `rgb(15, 20, 13)`.

Revision 2 answered `codex-r76.md`:
- source addresses are plain text, never links;
- the escaping is written out as literal JSON escapes, with the charset and the CSP first in the file;
- the format-1 checks are updated, and a lone page-hash error has its own test;
- the screen check compares the expanded `v8` card with frozen expected entries;
- the fetch mutant keeps its script running and must name `connect-src` and its destination;
- the fallback, timer, phone-width and dark-scheme conditions are made observable;
- the text filter is dropped. Slice 1 is built and accepted (D759: `RELEASE-BUILD.md` revision 11,
`RELEASE-CHECK-RESULT.md`). Council 73 (D758) ordered the exporter first and the reader's screen second. This slice completes D756's
screen check: a $0 check of the reader's screen on a stored number question that has a forecast and history, where only the
question, its sources and "Forecast unavailable" appear.

## 0. Scope

- **Built:**
  - a page that is a pure function of the package data;
  - the package gains that page (format 2);
  - the package check proves the page equals that function of the data;
  - a headless-browser check of the `old-1/v8` screen.
- **The page reads only the package's data,** embedded in it.
  - No network request of any kind: no live POC service, no `/library` fetch, no translated or prepared JSON, no composite trials,
    no fonts or images from outside.
  - No idea submission control or route (council 74).
- **Not in scope:**
  - the POC's page, API and MCP, unchanged;
  - colleagues' page;
  - the idea path;
  - any model call;
  - commit, publish, deploy (Alex's).

**Why a separate page, not the POC's library UI.** The POC's components read the `thesis-ui/2` contract, which needs a ladder,
scores and judgements for every thesis; a number question in the package has none. Adapting those shared components would change
the POC, which stays unchanged (design §2, D757). A small page written for the package has nothing to adapt and nothing that can
reach the network.

## 1. What is built

**A visible fallback.** The page starts with the line "This release page needs JavaScript to show its questions." The script removes it
once the list is built. A browser that blocks the inline script keeps that line (`<noscript>` would stay hidden there; council
76).

**In `src/hivemind/release.py`:**
- **`FORMAT = 'hivemind-release/2'`.** The data's allow-list (`release-allow-list/1`) is unchanged.
- **`PACKAGE_FILES = {'manifest.json', 'release-data.json', 'index.html'}`.** The manifest's closed set gains `page_sha256`.
- **`render_page(data_bytes) -> bytes`:** one fixed template, the module constant `PAGE_TEMPLATE`, with the data inserted once.
  - **The data** goes into `<script type="application/json" id="release-data">`, written from the exact `release-data.json` bytes,
    with each of these characters replaced by its six-character JSON escape: `<` by `\u003c`, `>` by `\u003e`, `&` by `\u0026`,
    U+2028 by `\u2028`, U+2029 by `\u2029`. These replacements stay valid JSON and parse back to the same data. The block can then
    hold no `</script` and no `<!--`.
  - **The file starts** with `<!doctype html>`, then `<meta charset="utf-8">`, then the CSP `<meta>`, before any style, script or
    data.
  - **A Content-Security-Policy `<meta>`:**
    `default-src 'none'; script-src 'sha256-<inline script>'; style-src 'sha256-<inline style>'; img-src 'none'; font-src 'none';
    connect-src 'none'; base-uri 'none'; form-action 'none'`. The two hashes are computed from the template's own script and style,
    so the browser refuses any other script, style or connection.
  - **The script** builds the page only with `document.createElement`, `textContent` and `className`. It creates no `<a>` element,
    no `href` and no `src`. It never uses `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, `Function`, or any network API
    (`fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `navigator.sendBeacon`, `import()`, `Worker`).
  - **The style** uses system fonts and inline colour tokens copied from `web/design-system/tokens.css`. It generates no text: no
    `content` property anywhere, so every word a reader sees is a text node the screen check can read. It clips no text: none of
    `overflow`, `clip`, `text-overflow`, `line-clamp`, `max-height` or `white-space: nowrap`, and long words wrap
    (`overflow-wrap: anywhere`). It has a dark scheme under
    `prefers-color-scheme: dark`, and it works at phone width.
- **`write_package`** also writes `index.html = render_page(data bytes)` and records its sha256.
- **`check_package`** also:
  - reads `index.html` once through the same folder handle;
  - requires its bytes to equal `render_page(the data bytes it read)` exactly;
  - requires the manifest's `page_sha256` to match.

  A page that differs by one byte from the function of the data is refused. So a page cannot carry anything the data does not hold,
  and no code the template does not hold.

**What the page shows,** in package order. Each shown value sits in an element with a fixed class, so the screen check can read it:
`question-text`, `question-status`, `question-forecast`, `question-answer`, `evidence-count`, `evidence-summary`, `evidence-quote`,
`evidence-meta`, `source-title`, `source-publisher`, `source-day`, `source-address`.
- **A header:** "Hivemind release", the package's day, and the count of questions by class.
- **Each question:**
  - its question text and "Open" or "Closed";
  - for a number question, the marker "Forecast unavailable";
  - for an event or Yes/No question, "Answer: <label>", or "Not yet answered" when the answer is null;
  - "<n> pieces of evidence", and a `<details>` element. When opened, it builds the evidence list:
    - each piece shows its summary, the quote, and a line with tier, speaker, and original speaker and day;
    - each source shows title, publisher, day and its address as plain text. The page has no links, so neither a click nor a script
      can make a request (council 76).

  Evidence is built only when opened, so the first screen stays fast on a 6 MB package.

## 2. State × event (the page and the check)

| State / event | What happens |
|---|---|
| Package with no questions | "No questions as of <day>" |
| A question with no evidence | "No evidence in force", and no `<details>` |
| A source address of any scheme, `javascript:` included | shown as text; the page has no links |
| Text holding `</script>`, `<img onerror=…>`, `&` or U+2028 | the embed escapes it, the page shows it as text, and the JSON parses back identical |
| The page is opened from disk, a static host or any path | it reads only its embedded data; nothing else exists to read |
| The browser blocks the inline script | the fallback line stays visible; nothing else renders, and the page holds no forecast to leak |
| A page edited after the build (a fetch added, a field added) | `check_package` refuses: the bytes differ from `render_page(data)` |
| The template changes in a later version | old packages fail `check_package` under the new code by design; a new template is a new format version |
| A dark scheme and a phone width | checked in §6: at 390 px wide the page has no horizontal scroll; with the dark scheme emulated, the body's background is the dark token |

## 3. Value × reader

- Every value the page shows comes from the embedded data; the page reads no other value.
- The page's readers are a person's browser and the browser check.
- The data's readers are unchanged from slice 1: `check_package`, `check_origins`, the tests. The page adds one reader of the data,
  the page script, and no new writer.

## 4. New path × old checks

| Slice-1 check | Slice 2 |
|---|---|
| Closed set of the data, origin check, staged check before the no-replace publication, the no-replace report | unchanged |
| The manifest's closed set | gains `page_sha256`; `format` becomes `hivemind-release/2` |
| Exactly the package files, each read once, no links, no pipes | the same rule over three files |
| The literal-values rule of verification (council 75d) | applied to the page checks as well |
| `release_check.py` pins `hivemind-release/1`; its helpers that forge data refresh only the data hash | the pin becomes `/2`. The forging helpers also regenerate `index.html = render_page(forged data)` and its hash, so a forged forecast still reaches the store comparison and is refused there, with its exact reason |

## 5. Tests (`tests/test_release.py`) and mutants

1. **Determinism.** `render_page` of the fixture data twice gives the same bytes.
2. **Escaping.**
   - A fixture quote holding `</script><img src=x onerror=alert(1)>`, an `&` and a U+2028 is embedded with the literal escapes.
   - The page bytes hold no `</script` inside the data block and no `<!--`.
   - Parsing the block back gives the data unchanged.
   - In the browser check (§6), on the fixture page with that evidence expanded, the exact quote is visible as text, and the page has
     no `img` element.
3. **No network code, no drawn text.**
   - The template's script contains none of the listed APIs, and no `createElement('a')`, `href` or `src`.
   - Its CSP is exactly the policy above, with the hashes of its own script and style.
   - Its stylesheet has no `content` property, and none of `overflow` (as a property name, so `overflow-wrap` is allowed), `clip`,
     `clip-path`, `contain`, `text-overflow`, `line-clamp`, `max-height`, `nowrap`, `opacity` or `visibility`.
   - The sha256 of `page_template()` (the whole page with its one data placeholder) equals a literal written in the test after the
     screen run certifies it. A change to any part of the page fails this until it is re-certified.
4. **The package check:**
   - a page changed by one byte, with the manifest hash refreshed, is refused with its exact reason;
   - a page with `fetch("http://127.0.0.1:59999/library")` added, its CSP hash and manifest hash both updated, is refused, because it
     is not `render_page(data)`;
   - **a correct page with only `page_sha256` wrong is refused with its exact reason**, which catches a deleted hash check;
   - a missing page and a fourth file are each refused;
   - all three files are read once through the folder handle, and the page bytes compared are the bytes hashed.
5. **Literal identifiers:** `hivemind-release/2` and `release-allow-list/1`, in the tests and the acceptance script.

**Mutants:**
- `render_page` not escaping `<`;
- the script using `innerHTML` for the quote;
- a source address rendered as a link;
- `check_package` not comparing the page with `render_page`;
- `check_package` not checking `page_sha256`;
- the CSP hash computed over a different script.

## 6. The $0 screen check (`release_screen.mjs`, run once)

- **Setup.** Headless Chrome from `/Applications/Google Chrome.app`, driven through its DevTools protocol with Node's built-in
  WebSocket, on a fresh profile in the scratchpad. Each page is opened from `file://`.
- **Packages:** `old-1` at its default day, and the two dated leak packages (`old-3` at 2026-08-25, `old-1` at 2026-08-28), built by
  the slice-1 command under format 2.

**Recorded for each page:**
- the page's own network requests (`Network.requestWillBeSent` for the page target). Only the document itself may appear;
- console errors, exceptions and CSP violations (`Runtime.exceptionThrown`, `Log.entryAdded`). Zero are allowed.

**Observation.** The `Network`, `Log` and `Runtime` domains are enabled before navigation and stay enabled through every expansion.
Any of these fails the page:
- a request other than the document;
- a `Log.entryAdded` error;
- a `Runtime.exceptionThrown`;
- a `Runtime.consoleAPICalled` of type `error`.

**Expected values, frozen before the run.** `release_screen.mjs` reads `screen-expected.json`. It is written before the first screen
run, with its sha256 recorded in the result, from the accepted slice-1 packages:
- `poc/data/release-check-2026-11-23g/old-1/package` for `v8`;
- `old-3/package-2026-08-25` for `old-3/v36` (at that day it asks whether NVIDIA will begin shipping Rubin Ultra);
- `old-1/package-2026-08-28` for `old-1/v10`.

For each checked page it holds the page's complete visible text:
- **the header:** "Hivemind release", "As of <day>", and the counts line;
- **every card collapsed,** in package order: its id, then its question, status, the marker or the answer, and the evidence count
  (or "No evidence in force");
- **the checked card expanded:** for each evidence entry in order, its own group: summary, quote, meta line, and per source its
  title, publisher, day and address.

**How the page is read.**
- **What counts as visible.** The check walks every text node of `document.body` in document order. It keeps a text only when its
  element passes `checkVisibility({opacityProperty: true, visibilityProperty: true, contentVisibilityAuto: true})` and has a
  non-zero box. A text inside a transparent, hidden or collapsed ancestor is not visible.
- **Not clipped.**
  - For each kept text whose element is a block (not `display: inline`), the element's `scrollWidth` is at most `clientWidth + 1` and
    its `scrollHeight` at most `clientHeight + 1`.
  - No ancestor between it and `body` clips: none has `overflow-x` or `overflow-y` other than `visible`, `contain` holding `paint`,
    `strict` or `content`, or `clip-path` other than `none`.
  - Any clipped text fails the page, whatever its content.
- **Readable.** Each kept text's contrast ratio is at least 4.5:1, computed (WCAG relative luminance) between its element's computed
  `color` and the first non-transparent `background-color` found from that element itself upward, the page canvas if none. This is checked in light and in
  dark. Any text below the ratio fails the page.
- **Where each text goes:** to the header, to a card (by `data-id`), to an evidence group within a card, or else to `other`.
  `other` must be empty.
- **What must match.** The read page must equal the frozen page exactly: collapsed, then with the checked card expanded, then after
  closing and reopening it.
- **What that catches.** An extra visible line anywhere fails: inside the card, beside it, or in the header. For example,
  "Forecast: $361 billion", Morningstar's genuine figure shown as if it were the system's. So does a missing, duplicated, regrouped
  or reordered entry.

**The screen of `old-1/v8`:**
- **Collapsed:** the whole read page equals the frozen page. The `v8` card reads "How much Data Center segment revenue will NVIDIA
  report for FY2027?", "Open", "Forecast unavailable", "1284 pieces of evidence".
- **With `v8` expanded:** the whole read page equals the frozen page with `v8`'s 1,284 groups. The full Morningstar quote and its
  attribution are included, and "Bullish" appears only where a frozen source text holds it.
- **Closed and reopened once:** the same.
- **No link anywhere on the page:** zero `a` elements, zero `[href]`, zero `[src]`.
- **A screenshot** of the expanded card's top is saved with the result.

**The leak screens.** For `old-3/v36` at 2026-08-25 and `old-1/v10` at 2026-08-28:
- the page's day equals its package's;
- the whole read page, collapsed and with the card expanded, equals the frozen page from that dated package. The card holds its
  question, status, "Answer: Yes", "1 piece of evidence", then its single evidence entry and source;
- so the entry is visible, and nothing else is: neither judgement's explanation, nor "around $1 trillion", "rung 4" or "at rung".

**The decisive negatives** (checks of the check). Each is a copy of the `old-1` page with its script changed and its CSP hash
recomputed, so the changed script runs. Each must fail for its own reason:
- **inside the card:** one visible line "Forecast: $361 billion" added in the `v8` card fails the comparison;
- **beside the card:** the same line added just before the `v8` card, as its sibling, fails the comparison (it lands in `other`);
- **transparent:** the whole list set to `opacity: 0` misses the 3 s deadline, because no card is visible, although every card
  exists;
- **clipped:** quotes held to one line (`white-space: nowrap; overflow: hidden; text-overflow: ellipsis` added through the script's
  inline style on each quote) fail the not-clipped rule at 390 px, although their text is identical;
- **clipping wrapper:** each quote placed inside a one-line wrapper (`contain: paint; height: 1.5em`), the quote itself wrapping
  normally, fails the clipping-ancestor rule at 390 px;
- **unreadable marker:** in dark, the marker drawn in `--ink` on an `--ink` background (`color` set to `rgb(15, 20, 13)` through the
  script's inline style) fails the contrast rule, although its text, box and opacity pass;
- **marker on its own background:** in light, the marker given dark text on its own dark background (`color` and `background` both
  `rgb(15, 20, 13)`) inside the light card fails the contrast rule.

**The escaping screen.** The fixture page of test 2, with that evidence expanded, shows the exact quote as text and has no `img`
element.

**The fetch mutant.**
- **Setup:** a copy of the `old-1` page with `fetch("http://127.0.0.1:59999/library")` added to its script, and the CSP script hash
  recomputed for the altered script, so the script runs.
- **It must fail the check for the right reason:**
  - the normal list renders;
  - a `Log.entryAdded` security error names `http://127.0.0.1:59999/library` and `connect-src`.

  A page whose script is blocked wholesale does not earn the credit.
- **Measured on this Mac (Chrome 158, headless, scratchpad probe):** a CSP-blocked fetch produces no `Network.requestWillBeSent`. It
  produces a `security` error naming the address and the directive, and a `javascript` error.
- **The probe page named port 8788.** Chrome refused it under the CSP before connecting ("Refused to connect"), so no request reached
  that service. Port 59999 is not on the fetch specification's blocked-port list, and nothing listens there.

**Phone width and dark scheme.**
- **At 390 × 844** (`Emulation.setDeviceMetricsOverride`):
  - `document.scrollingElement.scrollWidth` is at most 390;
  - with `v8` expanded, the whole read page, with the not-clipped rule, equals the frozen expanded page;
  - Morningstar's quote (`e2295`), scrolled into view, wraps over more than one line (`getClientRects` on its text), and its box lies
    within the 390 px viewport.
- With `Emulation.setEmulatedMedia` `prefers-color-scheme: dark`, the body's computed background is exactly `rgb(15, 20, 13)` (the
  shared `--ink`, used as the dark page colour). In light, it is `rgb(245, 242, 235)` (`--paper`).

**Budget,** set before the first control:
- at most 3 s for the `old-1` page in headless Chrome, from `Page.navigate` until the full list is visible: the fallback line is
  gone, and every expected question's card is present and passes the same visibility test as the text;
- the page's size at most the data's bytes plus 64 KB.

## 7. Prior decisions

D726, D756, D757, D758, D759; council 74 (no idea input); council 75d (literal expected values); D690 (poc-v118 stays the product);
D163 (English product text).
