# Amendment to PRD 10 §5.2 and §6 (round 6 version; applies on Alex's word)

Found by the review rounds before any send of the links design (`log.md` rows 11–13). PRD 10 changes only on Alex's word, so nothing here is
applied. Each earlier version was refuted by a review and is kept in the log: round 3 refuted crediting a question with facts filed under a
question that feeds it (that judge never reads them) and bars on means (the control fails them against itself); round 4 refuted a per-question
guard by significance alone (a question fed by one article can lose all its facts at p = 5%, since three sends per arm allow only twenty splits);
round 5 refuted deciding per question by a reader's classes (a reading list that missed sparse noise; "sampling" and "caused by the rule"
overlapping; the single-home class excusing a move to a broader question); round 6 found the scorer reading one statement per gold item (a passage
holding revenue and margin guidance, written as two statements under two questions, counted as missing the margin question), a stricter guard
available at no cost (two facts falling from every control send to no variant send), and the limit adjustment written but not coded.

## 1. §6 decision rule

**Why the written rule cannot be used.** "超过对照三次的最高值" in every send fails a fresh control against the first one, so it judges nothing
(AGENTS §7.3); the held-out set has no room (22 facts the gold uses: 15 already reach their question, 5 were never written or were refused by a code
check); and per question, three sends cannot tell a real loss from sampling on a question fed by one or two articles.

**The one structural rule.** Code decides, by counts against the frozen gold, only what three sends per arm can tell from luck; every case the
counts list is read by a reader who did not write the change, to name its mechanism in the report, and decides nothing (AGENTS §7.1: "code checks
only structure and counts"; §7.2: "a score is a lead; the traces are the measurement"). Script: `decide.py`.

Totals. Each measure of `measure_filing.measure_send` is summed per arm; the observed difference (variant − control) is set against 4,000
reassignments of each article's six answers between the two arms (seed 20261105; the article and its request stay fixed). p is the share of
reassignments reaching the observed difference in the direction tested. All must hold:

| Set | Measure | Must show |
|---|---|---|
| development | facts the gold uses that reach a question it uses them for | up, p < 5% |
| development | statements under the company-wide revenue questions v1 or v22 | down, p < 5% |
| development and held-out | the standard's not-kept spans present | not up at p < 5% |
| held-out | facts the gold uses that reach a question it uses them for | not down at p < 5% |
| development and held-out | core matters present | not down at p < 5% |

Per question (both sets together), all by code:
- A gold item reaches a question when any statement expressing it is filed there: its best match, or any statement quoting the item's own passage
  (both are exact spans of the article; `measure_filing.expressing`). Read on the twelve cases round 6 pointed to: the passage rule accepts the
  five that are the same fact and rejects the seven that are not.
- A fact the gold uses for question q is *dropped* when the variant delivers it to q in at least two fewer of its three sends than the control, and
  *gained* in the reverse case; a *full* drop is every control send and no variant send. A drop is the *single home*, not counted, when in at least
  two of the variant's sends that miss q the fact is filed under another question the gold uses it for that is not broader than q (not q's ancestor
  in the seed tree: D207, one home, the narrowest); a move to a broader question counts. A gain mirrors it.
- A noise statement (its gold span not kept by the standard, or kept and used by no question) is *new* on q when the variant files it under q in at
  least two sends and the control in none (*full*: in every variant send), and *removed* in the reverse case.
- A question fails when, net of the reverse cases, it reaches any limit: **3 drops, 2 full drops, 5 new noise statements, 3 full new noise
  statements**. These are the smallest limits a variant identical to the control reaches by chance in about one draw in ten or fewer (reassignments
  of the stored arm with each earlier variant, 1,000 each: some question reaches 2 drops in 28–31% and 3 in 2.6%; 1 full drop in 18–32% and 2 in
  0.0–0.3%; 4 noise in 18–21% and 5 in 5.4–8.4%; 2 full noise in 10–11% and 3 in 1.1%; all four together in 8.1% and 10.0%).
- `decide.py` computes the reassignments first; while an identical variant would fail in more than 10% of them, it raises by one step the component
  that fails such variants most often; only then does it compare the observed counts.
- What three sends cannot tell from luck on one question (two facts lost without a full drop, two to four noise statements added) is listed with
  every drop, gain, single-home move and new noise statement, read to its raw answers, and reported with its mechanism; it does not decide the test.

Every send is reported beside the totals, regressions first; supporting matters present are reported with their mechanism. Calibration on the
existing development answers (`calibrate-decide-dnf.txt`, `calibrate-decide-def.txt`, with the passage rule): the draft-0 variant (definition, no
fallback) passes parking, noise, core and the per-question guard and fails the reach increase (+9, p = 11.8%); the definition-only variant fails
reach (+4, p = 34%) and parking (+4).

## 2. §5.2: one home

§5.2's second home ("另一方的题开着…一并挂上") departs from D207 (Alex: one home, the narrowest question). Replaced, within one home, by two
sentences of the links rule:
- "When it bears on two specific questions, take the one whose quantity it measures most directly (a hotel chain's room rate, under its room-revenue
  question rather than travellers' spending question; a parts maker's sales to carmakers, under the carmakers' parts-spending question rather than
  a rival parts maker's share question)."
- "A statement that gives a separate figure for each of two questions (a drug maker's sales of two drugs in one sentence) is written as two evidence
  items, one under each." (The code already stores two items quoting one sentence as one piece with both links: `extraction.sift`, "the same
  sentence read out twice is one piece with both links".)
