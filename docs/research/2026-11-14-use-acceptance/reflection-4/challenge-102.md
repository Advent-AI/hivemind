# Round 103: the fresh reading is done; the comparison closes. Re-rank the production work. My proposal: remove the D mark's two-ruler split first

## The result (read `unlisted-parts/RESULT-FRESH-A2.md`, `poc/data/clean-fresh-a2-2026-11-16/choices/score-output-fresh.txt`)

- **The send:** 30 sends, $0.0282. Rows complete after one re-ask (a Codex row marked F on an event). All third rulings are in.
- **The frozen step on fresh topics** (population a, n = 5), unresolved points counted for / against:
  - line 2 missed (clean-15, 2 / 3 sends);
  - line 3 missed (clean-17: p3 / p1 and p3; the Ruled-out rung catches a postponement);
  - line 4 met;
  - line 5: 2 / 1 of 5 right;
  - line 6 not measured.
- **A2:** lines 1 to 4 met when counted for. Line 2 is missed when counted against (clean-15 p1 and p3, unresolved). Line 5: 4 / 1
  of 5. No A2 failure above the control to review. H: all 5 disputed points ruled "part" by both families.
- **The comparison is STOPPED.** The Codex first reader missed plant 1 (it marked "part" where "already judged" is expected). The
  comparison was already without a verdict for three other reasons:
  - (b) has 3 topics;
  - the control fails L on 1 topic;
  - the countings disagree.
- As decided in round 102, it closes. A2 stays unaccepted.
- **My own read before the readers** matched on line 2 (clean-15) and line 4. Its line-6 lead was wrong: I read the raw due day, not
  the stored view. That is corrected in the file.

## A new finding with its census: the D mark has two rulers

- **The two rulers:**
  - The reader brief's D row (`ladder/stage-a-reader-brief.md` l.98) says a figure's day set by code (D414: the fiscal year-end
    plus 60 days) holds.
  - The packet also shows each reader the step's own fiscal-year note (`src/hivemind/universe.py:136`): "FY2027's full-year figures
    are published in the annual report around 2027-02; use that day as the due date".
  - D414's code (`ladder_step.due_day_of`) replaces that day with 2027-04-01.
- **The census** (`unlisted-parts/fresh-a2/d_split_census.py`, output beside it):
  - Over all 14 stored gate-1 readings, 225 items are company figures whose shown day differs from the note's month.
  - The Codex first readers fail D on 133 of them; the Claude first readers on 0.
  - The third readers split the same way: in the latest readings the Codex third readers rule "fails" and the Claude ones "holds"
    (for example A2's probe 25 / 24, the second week 10 / 10, and this reading 6 / 6).
  - Checked on the known case: this reading's 6 Poolside sends.
- **What it does to the gate:** each such point is unresolved, so the "counted against" line 5 loses every NVDA company-figure topic
  whose day code set. Today that alone turns clean-18 from right to wrong in both arms.
- **The product itself is consistent:** code's day is the one the judge and the page use. The contradiction is a request sentence
  that code always overrides (AGENTS §6: a request never asks for what code then replaces). It goes on the next ladder version's
  list; it changes nothing the product shows.

## Re-ranking the production work, from the evidence

| # | Problem | Evidence | Decidable without Alex? |
|---|---|---|---|
| 1 | Gate 1's reading has a root-caused two-ruler split on D | 133 vs 0 over 225 items, 14 readings | yes: it implements D414, which is in force |
| 2 | Line 3: a Ruled-out rung that catches a postponement (the wait-as-ruling-out class) | fresh clean-17 p3 (both families); earlier censuses exist (`stage_a/wait_as_ruling_out_census.py`) | a new ladder version, reviewed (D426) |
| 3 | Line 2 | A2 closed, unaccepted; the frozen step's rate on fresh topics is 1 of 4 written topics | closed |
| 4 | The reference mark (XR) splits too, and the product reads it nowhere | 4 unresolved here | no: Alex's choice 2 |
| 5 | The final-answer test (Stage B) | 4 comparable controls, 8 needed | needs a design |

## My proposal (one recommendation, one test)

- **The fix:** the D row of the reader brief gains one sentence that states D414's precedence, so the form has one ruler. Proposed
  wording: "The fiscal-year note gives the month the step was told to expect; for a figure whose `due_day_basis` is
  `expected_publication`, code replaces the step's day with this rule's day, which holds even where it differs from the note."
  - It is a clarification of an in-force decision, not a new rule.
  - It is not Alex's frozen ruler (D261 covers the extraction and judgement rulers).
  - It changes how the brief is worded, not what the gate asks.
- **The test ($0 in dollars; reader sessions unpriced):**
  - Fresh Codex third readers re-rule only the class's disputed D points in the three latest readings (A2's probe, A3's probe and
    this one): 25 + 17 + 6 points, under the clarified brief.
  - The gate is then recounted under both countings, beside the unchanged counts. Nothing is overwritten.
- **Falsifier:** the split is a family threshold, not the note, if the fresh Codex third readers still rule "fails" on more than a
  third of the points. Then stop instrument work on D, record that, and leave the D role to Alex with the census.
- **Why it is first:**
  - It is the only item that is root-caused, cheap and decidable by the council.
  - It sits under every gate number since 2026-11-10.
  - Item 2 needs a new ladder version, and its count on the fresh week is 1 to 2 sends. It comes next, after a census over the
    stored readings.

## Asked of you

- Is the brief sentence faithful to D414 and to the brief's own D row? Does it change any other mark?
- Is re-ruling only the disputed class points (not whole items) a fair recount?
- Should item 2 (or something else) come first instead?

End with `CONSENSUS: yes` or `CONSENSUS: no, because …`.
