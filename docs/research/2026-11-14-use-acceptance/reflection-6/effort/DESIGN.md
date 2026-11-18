# Matched reasoning-effort comparison of the answer-choice step (D624), fixed before any send

**Hypothesis.** The frozen step (`gpt-6-luna`, medium reasoning effort) leaves parts of a topic's outcome unlisted (L) and asks
another question (Q) more often than a careful writer does (`../reference-control/RESULT.md`). The same model at high effort makes
fewer of these errors. This is a hypothesis, not an established cause.

## Arms and population

- **The arms:** `medium` (the frozen step as it is) and `high` (identical except `reasoning_effort='high'`). Three fresh draws each, on
  the 26 topics outside the 44 used by the reference control (the fortnight's and the week of 10-06's, all 13 of each).
- **Interleaving:** medium d1, high d1, medium d2, high d2, medium d3, high d3, each a separate run with its own archive.
- **Request equality:** every request is the frozen request byte for byte (system, user, schema, output cap, transport, retries),
  except `reasoning_effort`. This is checked at $0.

## Reading

- **What is read:** all six arm-draws' written ladders and refusals (156 items), mixed blind and shuffled, plus six controls:
  - the reference control's four: two sound, a rung gap (R) and another question (Q);
  - two new ones:
    - an unlisted part (L): a stored ladder with one listed part its outcome names removed from not_judged;
    - an unjustified refusal (N): a "no main figure" refusal put on a topic with a stated main figure.
- **Who reads:** both families with `stage-a-reader-brief.md` (the full gate form).
- **Disputes:** counted both ways.
- **Validity:** a missed planted-wrong control voids the reading.
- **Review:** every agreed hard-line fault in the high arm, and every one that differs between the arms on a topic, is reviewed
  against its source.

## What is counted

- Per arm, over 78 sends: items with an agreed fault on Q, L, R or N; refusals (the model's, and code's refused-twice); answers that
  could not be read (a truncation signal).
- Per topic: faulted sends in each arm.

## Outcomes, fixed now

- **Moves the candidate:** both of these, on agreed marks:
  - **a material paired improvement:** the high arm has at most half the medium arm's faulted items, and at least 3 fewer;
  - **no new harm:** no topic faulted in 2 or more high draws while faulted in no medium draw; high refusals and unreadable answers no
    more than 2 above medium.

  The direction must not reverse when unresolved points count against.
- **Closes it:** the high arm's failed sends at least the medium arm's minus 1.
- **Otherwise inconclusive.**

**Round 3 changes:**
- **Failed sends** are agreed hard-line faults plus sends refused twice by code. A lost answer cannot improve an arm. Each arm must
  hold all 78 sends.
- **Too little signal:** the result is inconclusive, never a close, when the medium arm fails fewer than 3 sends.
- **Sound controls:** both families failing a hard line on a sound control voids the reading as too harsh.
- **Request check:** the check compares the request bytes as built and sent. Effort is the only difference.

## Spend

- Caps: medium $0.25, high $0.75, reserved per attempt at the worst cost.
- Expected: about $0.08 (medium) and an unmeasured $0.15 to $0.30 (high).
- A separate council decision is needed before the send.

**Limits:**
- 26 topics, chosen as all of two stored weeks;
- one model;
- the same readers as before.
