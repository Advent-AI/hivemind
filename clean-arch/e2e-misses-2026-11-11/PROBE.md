# Re-sending the saved requests behind the two untraced misses: protocol

2026-11-11. Written before any send; revised after the council's challenge (`council/b-codex.md`) and after a finding at no cost
(below). Part of the round in [LOG.md](LOG.md). Nothing in any step, prompt, rule or saved run changes.

## Found at no cost before the send (`refusal_census.py`)

Draw 3's judge first answered the China share question on 2026-07-08 with **rung 4**, the rung draws 1 and 2 chose that day. The
frozen check refused that answer because it named the export-controls theme (v8) as a dependency ("v8 is not a dependency of v17");
the day then re-asked with a note, and the re-sent answer was **rung 5**, which the question kept to the window end. Over the six
draws, 65 judgements were refused and re-asked (clean 10, 16, 18; production 10, 5, 6); 42 of the refusals are this one, on this
question. The re-sent answer changed the rung 8 times; 5 of the 8 are on the China share question (clean draw 2 on 07-05, clean
draw 3 on 07-08, production draw 1 on 07-08 and 07-12, production draw 4 on 07-02); clean draw 3's and production draw 4's changes
held to the window end and both are misses on the ruler.

## What the sends decide

- China share: whether, on draw 3's first request of 07-08, rung 4 is the judge's usual answer (then the refusal and its re-ask turned
  an agreeing answer into the miss) or a minority one (then the re-ask only drew the usual answer); and whether the note added on the
  re-ask itself moves the rung.
- FY2028 revenue: whether draw 2's window-end request and draw 3's differ in what the judge answers, or each allows both answers.

## The cases (`resend.py`; requests rebuilt by the offline replay of each draw)

| Case | Request | Saved answer to it |
|---|---|---|
| A. draw 3, China share, 07-08, first | the day's first request, whose answer the check refused | rung 4, refused (theme named as a dependency) |
| F. draw 3, China share, 07-08, accepted | the same request with the re-ask note | rung 5, kept |
| B. draw 1, China share, 07-08, accepted | the request of a draw that moved to rung 4 that day | rung 4, kept |
| C. draw 3, China share, 07-14, accepted | the window end of the miss | rung 5, kept |
| D. draw 2, FY2028 revenue, 07-14, accepted | the window end of the miss (one "41%" item, 19 items, previous rung 3) | rung 3, kept |
| E. draw 3, FY2028 revenue, 07-14, accepted | the window end of a draw that agrees (two "41%" items, 24 items, previous rung 3) | rung 2, kept |

Three sends a case, 18 in all, interleaved and sent at once through the production transport, no archive, one spending limit.
Cost: about $0.04 expected; $0.65 if every send were tried three times at its worst; cap $0.70. Reviewed before the send
(`council/sender-review-codex.md`: four serious findings, each closed in `resend.py`, then a second review).

`resend.py check` passed for all six, with no send: each request equals, sorted, the saved archive's request and, as production
serializes it, what `model.build_request` builds today; each draw's ledger is rebuilt and stopped before that day's judging round; on
it the saved kept answers pass the frozen check, case A's saved answer is refused again for the same reason, and an answer citing an
id the request does not show is refused.

## Reading rule, fixed now

Each answer is read for its rung, and for whether the frozen check accepts it. **An answer the check refuses counts for its rung
only when every reason it was refused for concerns which ids it names** (a dependency, a shown item or theme, a push); a refusal for
the rung or for `changed` leaves its rung uncounted. Refusals are reported beside, with their reasons. A case with fewer than three
counted rungs decides nothing. Three answers give a lead, not a rate.

- **A.** Rung 4 in at least two of three: rung 4 is the more common answer to that request in these samples, a lead that the refusal
  and its re-ask turned an agreeing answer into the miss. Rung 5 in at least two of three: the re-ask drew the more common answer, and
  the refusal is not shown to be the cause. Anything else: not decided.
- **F against A.** If F's rungs sit lower (toward 5) than A's by two or more answers, the note itself may move the rung; otherwise the
  note is not shown to matter.
- **B.** Read beside A: if both give mostly 4, draw 3's and draw 1's inputs of that day are not shown to differ in what they produce.
- **C.** Rung 5 in three of three: the window-end request holds the rung the question reached. A rung 4 in any: the window-end answer is
  itself open. Neither says why the saved run chose 5.
- **D, E.** D at rung 3 in three of three and E at rung 2 in three of three: the requests differ in what they produce, a lead to trace
  (not which difference matters). Both mixed: each request allows both answers. Any other pattern: not decided. In D, whether any
  answer again reads $553 billion as below the $550 billion floor.

## What it cannot say

Three answers a case give no rate. Nothing here covers other days or other questions. An outcome that supports the refusal as the
cause of the China miss still leaves the window-end rung as the product of every later day.
