# The new system's questions on the product's page: result (D570, D571), 2026-11-16, $0

**Built** (designs `page-contract/DESIGN.md` version 3 and `not-judged-display/DESIGN.md` version 3): `src/hivemind/bundle.py`
(`ladder_row`, `not_judged`, `answer_shape`); the closed UI schema (`answerShape`, `favourableEnd`, `notJudged`, the event outcomes as
scores; 18 + 9 lines inserted, the file's formatting kept); `adapters/bundle.js` (event outcomes by their exact names, refused
otherwise); `model/thesis.js` (`undirected`, `scoreTitle`, neutral tone, event lanes in stored order, the date filter of the parts not
judged); the contract (three outcomes for an event); the card and drawer (titles, "Answer definitions", "Not judged"); the Idea
composite (`CompositeUnavailable`: not computed, the Idea kept, its card names the driver); `docs/poc/thesis-ui.md`.

**Evidence:** `tests/test_not_judged_bundle.py` 11; `poc/ui/test/not-judged.test.js` 9; UI tests 67; full suite 299; frozen tests 21;
`mutants.txt`: control passes, nine mutants each fail. The page built from the replayed fortnight store (`scripts/mock_build.py`):
12 of 12 questions validated, 186,131 JS bytes (budget 200 KiB); read in headless Chrome through the page's own explorer:
- `v7` (an event): "Not judged" beside the assessment with its two parts and reasons; the state chip neutral "Yes"; the card titled
  "Current outcome"; the History tab's "Answer definitions" (Answer / Definition). On 2026-09-26, before it opened: no section.
- `v5` (a theme range, `n/a`): the chip neutral with the range label and no score word; "Current range"; "Answer definitions".
- `v2` (a company figure, no part left out): no "Not judged" section; the chip "−2 Strongly bearish", negative; "AI score"; "Score
  definitions" (Score / State / Definition). `v1`: one part shown.
- The production ledger's page (68 questions) builds and validates as before.
The browser extension was not connected; the check used Chrome headless with a probe script (`--dump-dom`), not a person's view.

**Not covered:** the Idea composite's unavailable state was tested in the UI unit tests, not on a live Idea call (the Idea API
serves production's ledger only); the server-side planner on a new-system ledger is not designed (an open gate item).

## Council round 41's four points, fixed (2026-11-16)

- **Positions, not inferred scores, for undirected shapes:** a theme range with no favourable end and a question whose shape is not
  recorded get the scores "1" … "n" by position (the schema admits them; the contract requires exactly that sequence for these
  shapes); an event keeps its outcome names. Every undirected shape is laid out in stored order (lane = position − 1) and its chart
  axis marks the position (`axisMark`), never a +2 … −2 score.
- **Both composite entry points refuse an undirected driver** (`prepareIdeaComposite` and `prepareCompositeTrial`), naming it; the
  Idea is kept and its card shows the note.
- **An unrecorded question of three choices with any labels passes** the contract by position.
- **The History tab's disclosure** is titled "Answer definitions" for undirected shapes, with a Mark / Answer / Definition table.

Evidence after the fixes: UI tests 70 (`not-judged.test.js` 12), bundle tests 11, full suite 299, `docs/check.py` passes; mutants
(`mutants.txt`): control passes and all twelve fail (the axis-mark mutant first passed, equivalent on positional theme scores; an
assertion on an event's axis marks was added and it now fails). The fortnight page rebuilt (12 of 12 validate, 186,647 JS bytes) and
read in headless Chrome: `v5` axis marks 1 … 5, neutral, top to bottom in stored order, "Answer definitions"; `v7` marks 1 … 3, neutral,
"Answer definitions"; `v2` +2 … −2 with positive and negative tones, "Score definitions".

## The drawer's remaining D397 checks (council round 42)

In headless Chrome on the fortnight page (`not-judged-display/drawer-check.txt`): `v7` opened with its assessments removed and a first
part carrying markup (`<b>…</b> & <img src=x onerror=…>`, reason with `<i>…</i>`): the drawer says "There is no assessment for this
thesis at the selected date." and shows "Not judged" beside it with all three parts; the markup appears as text and no `b`, `i` or `img`
element is created inside the section.
