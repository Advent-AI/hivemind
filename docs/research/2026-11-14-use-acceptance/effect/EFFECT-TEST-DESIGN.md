# Does one missing fact change one stored judgement? A six-call test, version 2 (D508, under D509), 2026-11-15

**Authority.** Alex is not active (D509: "我要睡觉了，下来你自行按照我的准则操作，需要深度的审视每一轮run 用council"); D439 is in force. The council (thread mx,
round 21) and Claude agreed on this test before he left; its design goes to the council before the send, and its result after.

**What it can decide.** Whether, for the one confirmed missing fact of D508 that bears against a stored answer, adding that fact to
the judge's own request changes the judgement. It is a bounded signal on one stored request: not the size of the gap's effect on the
product, not a rate, and nothing about which system carries forward. Before the send it can still change this: whether the open
defect of D506 and D508 has a measured effect on a judgement, which decides whether a design for it is worth the council's time or
the defect is recorded as real and without a shown effect in this week.

**Version 2, after council round 22 (`mx-codex-22.md`), before the send.** The council ran the dry check (the archive key and the e379
block reproduce; the rebuilt schema's property order matches the stored reply's) and asked for four changes, all made: (1) every
HTTP attempt is written to disk before anything is parsed, and a call that fails is recorded, not lost; (2) an answer counts only
when it passes the judge's schema and the judge's own `check_answer` against the request that was sent; (3) retries are counted:
one attempt at a time, at most two for a call, and the ceiling covers twelve attempts; (4) "confidence fell" needs the two
conditions to separate completely in both readers' ranking, since the stored answer already names risks and two against one is
within a condition's own variation.

## The case (fixed)

- **The question (v7 of the new system's stored fresh-week run):** "Will China's Ministry of Industry and Information Technology (MIIT)
  formally approve purchases of Nvidia's RTX Pro 5500 by Alibaba, ByteDance, or other Chinese firms by January 31, 2027?" Possible
  answers: 1 Yes, 2 Ruled out, 3 Still open. Its last stored judgement (2026-09-28, 22 statements shown): answer 1.
- **The fact it was never shown (e379, article 163 of 2026-09-27, read six articles before the question opened and linked to the
  export question v3):** "In September 2025, Beijing told firms to stop buying Nvidia's RTX Pro 6000D, and the stock fell 2.6% that
  day." Both fresh readers of the census said it makes "yes" less certain.

## The two conditions (`effect_test.py`, after the reviewed method of `docs/research/2026-11-04-filing-end-to-end/one_test.py`)

- **Control:** the stored last request of v7, rebuilt by `model.build_request` with the frozen judge's setting (`rejudging`:
  gpt-6-luna, medium effort, 16,000 output tokens) and schema (`judging-v7`); the script refuses unless the rebuild has the stored
  archive key. Checked dry: it has (key d10d5014...).
- **With the fact:** the same request with e379's block inserted at the head of the evidence list and the list's count raised from
  22 to 23; nothing else differs (the script takes the block and the count back out and refuses unless that gives the stored text).
  The block is written by the production formatter and is, character for character, the text the judge saw for e379 under v3
  (checked dry). It sits first because its article is earlier than every statement under v7.
- Three sends of each on the same day, at once, straight through the model module's transport (no archive, so no send is answered
  from a stored reply), one HTTP attempt at a time and at most two for a call, each attempt written down before it is parsed. Six
  calls; about $0.011 at the published rates from the stored call's tokens (5,628 in, 2,514 out); $0.108 if all twelve possible
  attempts were charged their whole output allowance; **ceiling $0.25**. Spend recorded under D439 before this: about $18.4 of $40.
- An answer is valid when it passes the schema and `judging.check_answer` (its answer within the question's possible answers, every
  cited statement among those the request showed).

## Reading (frozen before the send)

- **By code:** each answer's `rung`, its cited statements (`cites`), and whether e379 is among them.
- **Blind, by a reader of each family:** the valid answers (rung, reasons, implied outcome, cited ids) in shuffled order under
  labels, with the question and its possible answers; the key outside the repository. The reader **ranks them by how firmly each
  holds "yes"**, from the firmest (rank 1) to the least firm, giving two the same rank only when their reasons give no ground to
  tell them apart; an answer that is not "yes" ranks below every "yes". Per answer also `uses_precedent`: whether an earlier Chinese
  stop order on a related Nvidia chip is used as a reason that bears on the answer (not a bare mention), and the judgement's own
  words that decide its rank. The readers are not told that the answers come from two conditions. A ranking compares the six with
  one another, so the caveats the stored answer already carries do not by themselves count as a loss of confidence.
- **Claude reads all six answers in full**, beside the two requests.

## Outcomes (frozen before the send; "no effect" is not among them)

- **The answer moved:** at least two of the three answers with the fact are not answer 1, and at least two of the three controls
  are answer 1.
- **Confidence in "yes" fell** (only when the answer did not move): all six answers are valid; in **both** readers' rankings every
  answer with the fact ranks strictly below (less firm than) every control; and both readers mark `uses_precedent` yes for at least
  two of the three answers with the fact. (Three against three in complete separation is one ordering in twenty by chance.)
- **Inconclusive:** anything else: the rankings overlap, in either reader's; the controls vary among themselves as much as the
  conditions differ; the fact is cited without a separation; the readers disagree; or no difference can be seen. An inconclusive
  result does not show the gap is without effect.
- The order of precedence is as listed: moved, then fell, then inconclusive. A reply that is not valid is reported and not counted
  as an answer; fewer than three valid answers in a condition is inconclusive.

## What follows each outcome (decided by the council, recorded under D439)

- Moved or confidence fell: the defect has a measured effect on one judgement of this run; the council takes up whether and what
  to design (the kind here is "read before the question opened": nothing files an earlier statement under a later question).
- Inconclusive: recorded as such; the council decides whether the line stops or one more case is worth its cost.

**Stated limits:** one request, three sends a condition, one fact; the judge's schema carries no probability, so a loss of
confidence is read from its reasons by the definitions above; position effects (the fact is the first item of the list) are not
separated from the fact's content.

## Correction (2026-11-15, found by the reflection council "my", round 3, and checked in the stored run)

This page said that nothing in the new system files an earlier statement under a question opened later, and that a judge is shown
the statements linked "when their articles were read". Both are wrong as written. **The new system has a later-linking step**
(`clean-arch/step3/library.py`, `link_later`): when a question opens, the system checks the earlier groups of statements (a
statement with its repeats) **whose original statement arrived without a question** (a batch that fails twice stays pending and is
tried again; none stayed pending in this run). In this week: seven calls, 516 group-and-question checks, 2 linked (both to the Vera
Rubin question); of the 196 links, 194 were made when the statement's article was read and 2 by this step. **A group whose original
arrived under another question is excluded, even if the new question also needs it:** e379 (the group `163:e3` in the stored
library) arrived linked to the export question at article 163, so it was not among the 166 checked when the RTX Pro 5500 question
opened at article 169. The counts and findings of this page do not change; the description of the cause does: the
case is "linked elsewhere and so never reconsidered", not "nothing looks back". Production does not link an earlier record to a
question opened later (D456: none of 3,225 links in six draws points back; a later article that repeats the fact can still deliver
it; `clean-arch/e2e-comparison-2026-11-13/unlinked-trace/UNLINKED-TRACE-RESULT.md`, which found that in those draws, on the graded
questions of the July window, such unlinked facts cost no final answer).
