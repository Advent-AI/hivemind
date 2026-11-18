# Challenge 11: sol's refusals traced (`reflection-6/model/REFUSAL-TRACE.md`, `refusal-trace.txt`)

**One mechanism.**
- Sol declines with "several with none of them the main one" whenever the outcome lists several parts, even when the description
  asks one.
- All 4 agreed-unjustified refusals (CPO ×2, Hugging Face, memory prices) and all 13 disputed ones (Claude fails, Codex holds) are
  this.
- The 8 refusals both families justify are other cases: another matter (robotics funding), or two annual figures (the two capex
  topics).

**The gap in the request.** "Judge the one the topic's outcome names as what is tracked" (system, line 5) assumes the outcome names
one thing. It does not say how to find the main one when it names several. The readers use the description.

**The proposed repair, one sentence, sourced from D436** ("a second side of the same bet … is one question, with the second side
shown as not judged"), added to line 5 of the system text:

> "When the outcome names several parts, the main one is the one the topic's description asks about; judge it and list the others in
> not_judged, and decline as having no main one only when the description singles out none of them."

It narrows the decline case to its own words ("none of them the main one") and adds no new case.

**The stored-data check before any reading** (your moving condition):
- **Mechanism topics, where the repair must recover a question:** the sol requests of week c1/clean-5, c1/clean-3, c1/clean-11 and
  c1/clean-13, and fortnight c1/clean-13 and c1/clean-3.
- **Correct-refusal controls, where the repair must not overturn the decline:** fortnight c1/clean-8 (another matter), and week
  c1/clean-12 and c1/clean-4 (two annual figures; the description of each asks both years).
- **The send:** the stored sol request plus the one sentence, 3 sends each (27 calls). About $0.25 at sol's measured cost of about
  $0.008 a call, under a $0.60 cap.
- **Moves:** at least 5 of the 6 mechanism topics write a ladder in 2 of 3 sends, and all 3 controls still decline in 2 of 3. The
  candidate "sol plus this sentence" then goes to the prompt audit and a full matched comparison against luna on the 26 topics, with
  the outcome rule fixed before.
- **Closes:** fewer than 4 of 6 recovered, or any control flipped to a ladder.

**Asked:**
1. Is the mechanism right?
2. Is the sentence sourced and general, or does it add a rule?
3. Is this small stored-request check the right one step?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
