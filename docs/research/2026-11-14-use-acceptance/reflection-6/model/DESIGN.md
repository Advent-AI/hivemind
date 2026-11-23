# Matched model comparison of the answer-choice step, gpt-6-luna against gpt-6.1-sol (D628), fixed before any send

**Hypothesis.** The frozen step's model, `gpt-6-luna` (the provider's "most efficient model for focused, high-volume tasks"), leaves
parts of a topic's outcome unlisted (L) and fuses decisions (Q) in about 1 of 6 sends on these topics (D626). A stronger model on the
same provider and the same request, `gpt-6.1-sol` ("near-Astra performance for complex work at a lower cost"), makes fewer of these
faults. The careful Claude writer's 0 of 26 is a lead, not a ranking.

**Same provider, same credential, same transport.** The model was found by a read-only listing (`model-list.txt`). Its published
rates are $2 and $10 per million input and output tokens (developers.openai.com/api/docs/models, read 2026-11-16), added to
`model.PRICES` with that source. No credential or provider cap changes.

## Arms and population

- **The arms:** `luna` (the frozen step as it is) and `sol` (identical except `model='gpt-6.1-sol'`). Both run at medium effort. Three fresh draws each, on
  the 26 topics outside the 44 used by the reference control (the fortnight's and the week of 10-06's, all 13 of each).
- **Interleaving:** luna d1, sol d1, luna d2, sol d2, luna d3, sol d3, each a separate run with its own archive.
- **Request equality:** every request is the frozen request byte for byte (system, user, schema, output cap, transport, retries),
  except `model`. This is checked at $0 on the bytes as sent.

## Reading

- **What is read:** all six arm-draws' written ladders and refusals (156 items), mixed blind and shuffled, plus six controls:
  - the reference control's four: two sound, a rung gap (R) and another question (Q);
  - two new ones:
    - an unlisted part (L): a stored ladder with one listed part its outcome names removed from not_judged;
    - an unjustified refusal (N): a "no main figure" refusal put on a topic with a stated main figure.
- **Who reads:** both families with `stage-a-reader-brief.md` (the full gate form).
- **Disputes:** counted both ways.
- **Validity:** a missed planted-wrong control voids the reading.
- **Review:** every agreed hard-line fault in the sol arm, and every one that differs between the arms on a topic, is reviewed
  against its source.

## What is counted

- Per arm, over 78 sends: items with an agreed fault on Q, L, R or N; refusals (the model's, and code's refused-twice); answers that
  could not be read (a truncation signal).
- Per topic: faulted sends in each arm.

## Outcomes, fixed now

- **Moves the candidate:** both of these, on agreed marks:
  - **a material paired improvement:** the sol arm has at most half the luna arm's faulted items, and at least 3 fewer;
  - **no new harm:** no topic faulted in 2 or more sol draws while faulted in no luna draw; sol refusals and unreadable answers no
    more than 2 above luna.

  The direction must not reverse when unresolved points count against.
- **Closes it:** the sol arm's failed sends at least the luna arm's minus 1.
- **Otherwise inconclusive.**

**Round 3 changes:**
- **Failed sends** are agreed hard-line faults plus sends refused twice by code. A lost answer cannot improve an arm. Each arm must
  hold all 78 sends.
- **Too little signal:** the result is inconclusive, never a close, when the luna arm fails fewer than 3 sends.
- **Sound controls:** both families failing a hard line on a sound control voids the reading as too harsh.
- **Request check:** the check compares the request bytes as built and sent. The model is the only difference.

## Spend

- Caps: luna $0.25, sol $4.50, reserved per attempt at the worst cost (sol about $0.20 an attempt), with sol at 4 workers.
- Expected: about $0.08 (luna), and about $2.2 (sol, today's luna token counts at sol's rates, no cache discount). About $9.7 is left of D439's $40.
- A separate council decision is needed before the send.

**Limits:**
- 26 topics, chosen as all of two stored weeks;
- one model;
- the same readers as before.

**Round 8 changes:**
- The first sol request, for the population's first topic, runs alone as a compatibility check. Its answer is kept as part of sol d1
  and is not inspected. If it writes no outcome, the run stops and is reported.
- The check output is regenerated for the launcher as reviewed.
