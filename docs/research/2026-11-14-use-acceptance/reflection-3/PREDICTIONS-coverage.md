# Predictions for the coverage trace, written before any reader's answer is opened (2026-11-15)

The council reviewer's step (`cold-codex-3.md`): at $0, take a library whose content is dated before a later stored news
window, and trace that window's topics against it: what was already covered, what still needed a new question.

Prior libraries found in storage, both dated by their own records:
- Library 1: the sealed three-month library, built only from news 2026-07-01 to 2026-08-28 under an older configuration
  (poc-v34), 69 questions (`sealed-library-questions.json`; every question's opening day is at most 2026-08-28). Its
  questions are not reviewed for quality: by eye it holds near-duplicates (a ban on Chinese open models five times) and
  single-deal questions an analyst would not hold.
- Library 2: the 7 topics the present clean system opened in the week of 2026-09-22, from empty.

**My own read, stored first.** Week of 09-22 (7 topics) against library 1: capital spending 2026 (v4), Vera Rubin shipments
(v21), the Hugging Face acquisition (v64) already had a question; credit support had by-deal yes-or-no questions (v1, v31 to
v33, v50) but no total; supply commitments had none; the two China topics are new chips beside the H200 questions. Week of
10-06 (13 topics) against both: capital spending (v4, v5, and the 09-22 topic), Rubin's ramp (v21, the 09-22 topic), Hugging
Face (v64, the 09-22 topic), supply commitments (the 09-22 topic), the lease guarantee (v31; the 09-22 total), Groq's rack
(v61) already had a question; Reflection AI and the B200 rental price are new; memory prices, the equity commitments total,
global AI spending, the loss-share exposure and the licence requirement had none or only a neighbour.
By eye, 12 or so of the 20 opening articles are general pieces ("which stock is the better buy") that mention the matter in
passing.

**Predictions (both families must agree for a topic to count).**
- Q1. Of the 13 topics of the week of 10-06, at least 6 are on a matter that already had a question in library 1 or 2
  (`same_question` or `same_matter`). Of the 7 topics of the week of 09-22, at least 3 against library 1.
- Q2. At least 10 of the 20 topics were opened from an article that is not news about that matter (`background`).
- Q3. Of the 7 topics of the week of 10-06 that carried an agreed fault or a refusal in the reading (clean-1, 3, 4, 7, 10, 12,
  13), at least 3 are on a matter already in a prior library.
- **Refutes** "a test from empty mostly re-invents standing matters": Q1 under 4 of 13, or Q2 under 6 of 20.
- **Cannot show:** that with the library present the system would have filed the article under the existing question
  (needs a run); that the prior questions are good ones; a rate for other companies or windows.

## Added before the July articles are read by anyone (2026-11-15, after the later weeks' tally)

The later weeks came out as: 18 of 20 topics on a standing matter, 16 of 20 opened from a passing mention, 2 new events
(both families). The same two marks (`article`, `matter_is`) are now taken on the 40 July topics with their articles (the first
14 days of a coverage from empty). I expect July to hold more real news than the later weeks, whose windows open months into
the story.
- J1. Standing by both families: at least 24 of 40. Background by both: at least 16 of 40.
- **Refutes** the general form ("a start from empty mostly re-creates standing matters from passing mentions"): standing
  under 12 of 40. Between 12 and 24 it holds for the later weeks only.
- Exploratory, no prediction: whether the matters whose questions came out the same in all three runs are more often news.
