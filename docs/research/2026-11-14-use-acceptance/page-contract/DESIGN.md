# The product page's contract for the new system's answer shapes: design version 3 for the council (D570; rounds 38 to 40), 2026-11-16, $0

**Defect.** The page's closed contract accepts two answer choices scored Yes/No or five scored +2 to −2
(`poc/ui/src/model/contract.js`); the new system writes three shapes. On the replayed fortnight store
(`poc/data/clean-carried-run-2026-11-16/page-store-2026-11-16/`): 6 events with Yes / Ruled out / Still open (D409, D416), 2 company
figures labelled Strongly bullish … Strongly bearish by code from their registered favourable end (D398; `lower` for both), and 4 theme
figures labelled by their ranges, favourable end `n/a` (a theme is not for or against the company). One three-choice question fails the
whole dataset.

**What a score is today** (every reader traced): the adapter gives each answer choice a score (`adapters/bundle.js` `legacyScores`:
the stored score if any; Yes/No by label; for a theme, ascending amounts make the highest range +2; otherwise +2 first); the card and
chart show the score and colour it (`model/thesis.js` `stateWords`, `stateTone`: +2, +1, Yes positive; −1, −2, No negative), the
chart puts each choice on a lane (`laneOf`), and an Idea's composite turns a score into a number on the question's own axis (+2 … −2,
Yes 2, No −2) and multiplies it by the Idea plan's direction for that driver (`idea/composite.js`), which the plan, not the page, sets.

**Scope of this slice (council round 38): the page shows the stored outcomes and ranges faithfully and invents no direction; what
a new-system shape may contribute to an Idea is decided separately.** Today the Idea API serves production's ledger only
(`docs/CURRENT_STATE.md`, "Idea API"), so no Idea reaches a new-system question yet; the server-side planner offers the first and the
last choice as the two ends (`src/hivemind/idea_composite.py`), which for a three-choice event are Yes and Still open, not opposites.

**The bundle carries the ladder row's shape** beside `not_judged`, with the same refusals: `answer_shape` and `favourable_end`. The
discriminator is the store, not the row: a store without a `clean_ladders` table is a production ledger (`answer_shape: None`); in a
store that has the table, a question with its row gives `event` or `figure` (from the row's checked answer) and its `favourable_end`
(`higher`, `lower`, `n/a`, or `None` for an event), and a question **without a row gives `unrecorded`** (a question opened before rows
were written or by another writer: its shape is not known). The two fields describe how to read the stored answer choices, as the
question's labels do, so they are not suppressed before creation (only `not_judged`'s content is). The closed schema gains the two
optional fields and admits the event scores below.

| Shape (new-system row) | Scores in the dataset | Card and drawer words | Tone | Chart lanes and title | Score definitions table | Idea composite |
|---|---|---|---|---|---|---|
| Event, two or three outcomes (`answer_shape: event`) | the outcome names (Yes, No; Yes, Ruled out, Still open); any other labels refused, never guessed by position | the outcome named once | neutral for every outcome | one lane an outcome, in the stored order; title "Current outcome", not "AI score" | outcome and its condition; no score column | **unavailable**: a composite with such a driver is not computed and says which driver has no stated direction; no weight is renormalised |
| Company figure (`higher` or `lower`) | unchanged: the code-written labels carry the direction (D398) | unchanged | unchanged | unchanged | unchanged | unchanged |
| Theme figure (`n/a`) | the range positions, low to high | the range label only, no +2 … −2 word | neutral | five lanes by position; title "Current range" | range and condition; no score column | **unavailable**, as for events, pending a reviewed rule |
| New-system store, no row (`unrecorded`) | the range or outcome positions as stored | the stored labels only, no score word | neutral | one lane a choice, by position; title "Current answer" | label and condition; no score column | **unavailable**, naming the driver ("its answer shape is not recorded") |
| Production ledger (no table) | unchanged | unchanged | unchanged | unchanged | unchanged | unchanged |

**Readers traced:** adapter (`legacyScores`), `stateWords`, `stateTone`, `laneOf`, the card's chart title and badge
(`thesis-chart.js`), the drawer's score definitions (`thesis-detail.js`), bootstrap's `scoreOf` label for an Idea's chosen thesis, the
Idea composite (`idea/composite.js`), and the server-side planner (`idea_composite.py`: it plans only on production's ledger today; on a
new-system ledger it is not designed, recorded as an open gate item).

**Product choices, stated with their consequences** (the council's under D439, recorded for Alex): new-system events and theme ranges
show no positive or negative colour and no investment score; they cannot enter an Idea composite until a rule says what an unresolved
event or an undirected range contributes. Not changed and listed for Alex: production's Yes/No questions colour Yes positive and No
negative, and production's theme figures score the highest range +2 by inference.

**Proof ($0).** UI unit tests for each shape (scores, words, tone, lanes, titles, score definitions, an unavailable composite naming its driver) and refusals (a three-choice ladder with
other labels); a mixed store (one question with a row, one without) and a production ledger side by side, each read by its own rule; the contract tests on the
older production dataset unchanged; the page built from the replayed fortnight store (`scripts/mock_build.py`), opened in a browser:
every question listed; an event's card, chart and drawer, a company figure's, a theme range's, on two dates; the D397 "Not judged"
section on `v7` (the display slice's pending proof). Falsifier: the page cannot show a stored outcome faithfully, or a downstream reader
needs a direction the ladder does not state.
