# Round 37: the display slice is built; its browser proof is blocked by a larger integration defect. Review both; then the next step.

**Built as version 3:** `src/hivemind/bundle.py` (`not_judged`, refusals, suppression before creation), `tests/test_not_judged_bundle.py`
(10: a real row, empty, no table, no row, four malformed rows, two rows, before creation directly, through the library before and
on creation and after closing); the closed UI schema gains an optional `notJudged` (18 lines inserted; my first edit reformatted the
whole file and was restored); `adapters/bundle.js`, `model/thesis.js` (`snapshotThesis`: null before `created_day`), the drawer's
"Not judged" section (escaped, only when non-empty, placed beside the assessment or its absence); `poc/ui/test/not-judged.test.js`
(4: list, empty, null, older bundle; Idea path; closed-contract refusals; snapshot before and on creation); UI tests 62 pass; full
suite passes. A page-readable fortnight store was made at $0 (`not-judged-display/page_store.py`: 95 of 95 judge requests answered
from the archive, judgements and ladder rows equal to the stored draw's, processing records and days present).

**The browser proof is blocked:** building the page from that store (`scripts/mock_build.py --ledger …`) fails in the page's own
contract: `/theses/2/rungs: expected Yes/No or five unique ordinal scores` (`poc/ui/src/model/contract.js`). The new system's event
questions have three answer choices (Yes / Ruled out / Still open, D409/D416); the page accepts two or five. Census of stored new-system
judge stores: 6 of 12 questions in the fortnight, 4 of 7, 5 of 9, 5 of 12, 1 of 2 in other draws. One refused question fails the whole
dataset, so the product page cannot show the new system's library at all. This is gate 5's third concrete defect, larger than D397's.

**Proposed:** (a) record the display slice as built and unit-proved, its browser proof pending; (b) the next step is a $0 design of
the page contract for the new system's answer shapes: three-choice events, and five-range figures with their registered favourable end
(D398) where the page needs a score; the open product question is how the page's "AI score" and chart show an event's Yes / Ruled out /
Still open when the ladder states no direction for the company. Attack the slice, the defect's reading, and whether (b) is the council's
to decide (a presentation choice) or Alex's. End with `CONSENSUS: yes` or `CONSENSUS: no, because …`.
