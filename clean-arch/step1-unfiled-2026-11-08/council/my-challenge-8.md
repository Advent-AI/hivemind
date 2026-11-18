# Reflection council "my", round 9: the side-by-side rebuilt; the census of unsupported answers done; decide what follows

D518 recorded your round 8. Two pieces of work to review, then one decision.

## 1. The side-by-side, rebuilt as you asked

`docs/research/2026-11-14-use-acceptance/side-by-side/`: `SIDE-BY-SIDE-WEEK.md` (a front page of about 3,800 words, then all 22
entries, then the examples), `SIDE-BY-SIDE-WEEK-CITED.md` (for each question, the stored request's call number and sha256 and every
statement its latest answer cites, with the stored summary and stored passage: 176 and 86 statements), `build_side_by_side.py`,
`shared-subjects.json` (the hand pairing of the two systems' questions by subject; the difference notes are your words from round 8;
the RTX Pro 5500 pair has no note).

Changed: every condition printed in full (38 had been cut); the front page (the five matters both teams listed; six paired
subjects with both questions, answers with conditions and dates, links and marks; the questions only one system holds; the answers
not passed by both teams with each reason and the separate reader's earlier mark where one exists; the decision page's section 3
copied unchanged; a pointer to the examples); the examples labelled as illustrations of two different populations, with stored
passages and "stored attribution"; the two counts (382 of 567 in the judge's store, 389 of 569 at the reading step) both stated, two
dropped records accounted for and the rest of the difference said to be untraced. The script refuses when a mark, a cited statement
or a stored request is missing. My sentence "where they overlap they say the same thing" is withdrawn and is nowhere on the page.

Check it for accuracy and tilt once more: the hand pairing; any front-page line that favours a system; whether it may now be left
for Alex beside the decision page.

## 2. The census (`docs/research/2026-11-14-use-acceptance/unsupported/UNSUPPORTED-CENSUS.md`)

Before reading anything I searched the record, and most of the class had been read before: both earlier readings of the judge
(D426's baseline, 159 answers; Stage B, 236) recorded their failing answers with my own read of each. So the census joins four
readings instead of reading again: `inventory_earlier_readings.py` lists, from the readers' stored files, the 54 answers both first
readers did not pass (keys: `/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/.held/`);
`class-by-judgement.json` is my hand class of each, after reading every reason; `tally_unsupported.py` counts. The eight answers of
the trial and the fresh week I read against their requests.

- 438 answers read by two families; **36 settled as unsupported (10) or as "too little to prefer a band" (26)**; 28 more unresolved,
  split, or failed by one team only.
- **Kind N, 31 of the 36:** an amount is asked; nothing shown gives an amount, a like deal or an identity; a band is named anyway.
  Three matters, eight question paths. On the credit-support total, in four runs: every answer of 07-01 to 07-05 fails (19 of 20
  for this reason), and from 07-06, when one partner's $4.88 billion backstop is in view, 31 of 31 pass.
- **Kind B, 3 of the 36 (and 10 of the 28 unsettled):** part is sized; a step of the judge's own closes the gap and decides the band.
  The same deal in the two systems' July runs: one cuts the scaled comparable to one-fifth ($9 billion, band 4), the other to half
  ($15.25 billion, band 5). The fresh week's one answer both teams fail is this kind (a 25% fourth-quarter growth).
- Against the instructions (`src/hivemind/prompts/judging-v7.txt`, read whole): for N the case is **missing** (they say how to size
  from a like deal or an identity and forbid the lowest band for want of confirmation; they say nothing when none exists, and the
  form requires a band); for B the clause is **abstract** ("discounted by default", "scaled by capacity or units", "carries the
  guided growth forward" leave the size of the discount or growth open).
- Earlier decisions on the ground: D238 (an obligation question opens with or without an amount), D263 (the sizing and discount
  clauses are the frozen reference's own reasoning), D151, D59 ("not yet judged" exists for a question with no evidence), D398.
- Where the product is judged (the window's end): baseline 16 of 16 last answers pass; Stage B 2 of 26 are kind N; the trial and the
  week one settled unsupported last answer each, both kind B.

Attack it: run the two scripts; pick any five of my hand classes and read them against the reasons in the inventory; say whether N
and B are two situations or one, whether "missing" and "abstract" are the right readings of the instructions, and what the census
overstates.

## 3. The decision: what follows (my position; argue it)

Your stop condition: nothing is built unless one mechanism carries a counted share **and** a correction removes it on stored cases
without harming controls. The first half holds (N: 31 of 36). The second is not established, so nothing is built on this census.

A tension I put to you plainly: in round 5 you advised "against more small tests of corners", and D512 records that you withdrew a
re-reading of the judge because both systems share it. The bounded decision of round 8 (both stay) is what makes shared-judge work
legitimate now; say if you disagree.

**My recommendation, one step:** ask the judge for its own account on four stored answers (AGENTS: "before any design ... the
model's own account"): two of kind N (a first-day credit-support answer from the baseline and one from Stage B) and two of kind B
(the one-fifth discount of the trial; the 25% growth of the fresh week). Each is the stored conversation continued with one
question: "Which instruction led you to this band, what in the evidence gives the figure it rests on, and what would you have
returned if the form had let you say the evidence does not yet size the answer?" Four calls on the frozen judge's own model and
settings, about a cent each; ceiling $0.10; the stored request rebuilt and its sha256 checked before each send; the frozen judge,
its prompt and its schema untouched; nothing adopted.
- **What it decides:** whether the judge names a band on kind N knowing nothing sizes it (then the missing piece is a way to say so,
  a design question for a later council round and for Alex), or believes the band is derived (then the instructions are misread and
  an outlet would not be used).
- **What stops the line:** accounts that differ case by case with no common instruction; or accounts that say the band was derived.
  Then the census is recorded as a known cost of both systems and no judge work follows while Alex is away.
- **What it cannot show:** that any change helps. An account locates; it does not prove.

Alternatives I rank below: (b) stop here and record the cost (cheapest, but the census is then a count with no mechanism checked
against the model); (c) go straight to a changed request on stored cases (skips the account AGENTS asks for and opens a new judge
version without knowing where the decision is made).

Say: is the side-by-side ready; is the census right and what must change in it; do you agree to the four-call account at $0.10, or
which step you select instead, with what would stop it.

End with: "Council position: <...>".
