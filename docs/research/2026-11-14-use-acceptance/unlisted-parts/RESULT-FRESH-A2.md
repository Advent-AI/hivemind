# The fresh A2 comparison (D587 to D589): a fresh gate-1 reading of the frozen step, and no comparative verdict

**In one line:** on topics no development touched, the frozen answer-choice step still misses Alex's gate (lines 2, 3 and 5). A2
does no worse anywhere and better on the one topic with a part left unlisted. But the comparison gives no verdict:

- population (b) is under its minimum;
- the control fails L on only 1 topic;
- the two countings disagree;
- a planted control was missed.

The two reader families' third readers disagree on 21 of the 29 points they ruled, and those splits decide most of the gap between
the two countings.

## What ran

- **First step:** the frozen Step 1 on the unread week of 10-13 (383 articles) from the 10-06 week's library. Complete, $3.4485, 5
  topics (`poc/data/clean-fresh-a2-2026-11-16/`).
- **Populations** (`population/population.json`):
  - (a) has all 5 topics.
  - (b), classed blind by a Codex classer and me separately, has 3: f1/clean-16, -17, -18.
  - f1/clean-15 is a development matter. f1/clean-14 is uncertain, because the classers split on it.
- **Answer choices:** control and A2, three sends each (30 sends, $0.0282). 12 ladders and 3 refusals in each arm. The $0 checks
  passed first (D589).
- **Reading:**
  - Two families of first readers, 2 packets (33 items, with 3 plants).
  - Third readers of both families on 22 sends (26 differing marks, 3 named faults) and on 5 H points.
  - One Codex row (item 24, a plant) was invalid (F marked on an event) and was asked again of a fresh session.
  - Score: `fresh_score.py`, output `choices/score-output-fresh.txt`.
- **My own read** of every send was written before the readers' rows (`choices/own-read-before-readers.md`).

## The fresh gate-1 reading of the frozen step (control), population (a), n = 5

| Line | Unresolved counted for the answer | Counted against |
|---|---|---|
| 1 | met | met |
| 2 | missed: clean-15 p1, p2 | missed: clean-15 p1, p2, p3 |
| 3 | missed: clean-17 p3 | missed: clean-17 p1, p3 |
| 4 | met (the 3 refusals of the AI-bill topic justified) | met |
| 5 | 2 of 5 right (1 by a ladder) | 1 of 5 right (0 by a ladder) |
| 6 | not measured (1 company figure, 4 ladder topics; 3 and 20 needed) | not measured |

- **Line 2:** on the hyperscaler custom-silicon topic the control leaves out the outcome's spending split (p1) or Maia's role as
  Microsoft's primary inference system (p2: both families' third readers). Its other three written topics list every part.
- **Line 3:** on Taiwan's export controls, p3's Ruled-out rung ("formally announces that it will not adopt tighter export controls
  … by January 31, 2027") also catches a postponement, which leaves the event still awaited (both third readers). This is the known
  wait-as-ruling-out class.
- **Line 5:** right needs every mark, so the reference mark (XR, not one of Alex's six lines) and the due-day mark (D) decide much of it.

## A2 beside the control (no verdict; reported as "not shown to be independent of the development matters")

| | Control | A2 |
|---|---|---|
| L topics, counted for / against | clean-15 / clean-15 | none / clean-15 (p1, p3 unresolved) |
| Line 3, for / against | missed / missed | met / met |
| N sends | 0 | 0 |
| H points (both third readers: all "part") | 0 | 0 |
| Line 5 right, for / against | 2 / 1 of 5 | 4 / 1 of 5 |
| A2 failures above the control to review | none | none |

- **Population (b)**, the 3 different-matter topics: neither arm fails L, and both arms give the same counts.
- **Why no verdict:**
  - (b) has 3 topics, under 5.
  - The control fails L on 1 topic, under 2.
  - The countings disagree.
  - `fresh_score.py` stops the comparison because a planted control was missed. The Codex first reader marked plant 1 (a
    termination the Ruled-out rung decides) as "part" instead of "already judged".
  - The plants guard only H, which is not one of Alex's lines. The Codex family's first H marks are therefore not trusted.
  - The two H third readers ruled all 5 disputed points "part".

## Where the families split (21 of 29 ruled points unresolved)

| Mark | Unresolved on arm sends | What splits them |
|---|---|---|
| D | 6 (clean-18, every send, both arms) | Code sets an undated annual filing at 60 days after year-end (2027-04-01, D414). The request's fiscal-year note says "published in the annual report around 2027-02; use that day as the due date". Codex reads the shown day as wrong; Claude follows code's rule. |
| XR | 4 (clean-14) | Whether IDC's "19% growth" forecast is the reference for a unit count. |
| L | 3 (clean-15) | Whether Maia's role as Microsoft's primary inference system is a part the gigawatt question leaves out. |
| R | 1 (clean-17 p1) | Whether a final control list that excludes Nvidia's products rules the event out. |

- **The D split comes from a contradiction inside the product,** checked in code:
  - The request's fiscal-year note (`src/hivemind/universe.py:136`) tells the step, for a company whose fiscal year does not end in
    December, that the full-year figures appear "around {year}-{month after year-end}; use that day as the due date".
  - The ladder step's D414 rule (`ladder_step.py`, `due_day_of`) sets every such figure with basis `expected_publication` to 60
    days after the year's end.
  - So every NVDA company figure answered this way is shown to the judge and the readers with a day the note contradicts.
  - How many disputed D marks this caused across the stored gate readings has not been counted.

## The rejection checked (AGENTS §7.3)

- **The control's line-2 and line-3 failures are the model's errors.** Both third-reader families agree on clean-15 p2 (L) and
  clean-17 p3 (R). I read both against the topic and agree.
- **The D failures under "against" are not shown to be model errors.** They are a request-and-code contradiction (see above).
- **My own pre-reading lead on line 6 was wrong.** I read the model's raw due day. The stored view, which code sets, is the same
  across sends on all 4 topics (correction in `own-read-before-readers.md`).

## What it teaches

- **Line 2 on fresh material:** the frozen step's line-2 failure rate on fresh material (1 of 4 written topics) is lower than on
  the development topics that motivated A to A3 (6 of 13). One week, one draw.
- **Where the gate's outcome comes from:** the readers' splits on two marks Alex has not ruled on (D on code-set days, XR) now
  decide more of it than A2's change does.
- **The comparison closes, as decided** (D589). A2 stays unaccepted.
