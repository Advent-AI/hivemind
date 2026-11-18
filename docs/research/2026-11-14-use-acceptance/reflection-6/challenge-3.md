# Challenge 3: the matched effort comparison is prepared at $0 (`reflection-6/effort/`); send decision

Your round-2 changes are applied in `effort/DESIGN.md` (fixed before any send) and `effort/effort_probe.py`:

- **Arms:** fresh medium and high, three draws each, interleaved (medium d1, high d1, …), on the 26 topics outside the 44. Each
  arm-draw has its own archive, so nothing is answered from a stored answer.
- **The check** (`effort/check-output.txt`): 26 of 26 medium requests equal their stored first request (sha256). Each high request
  differs only in `reasoning_effort`: same keys in the same order, same schema, same cap (16,000 output tokens), same runner, limit,
  retries and transport.
- **Controls, six:**
  - the reference control's four: two sound, an R gap, a Q other-question;
  - two new planted-wrong ones from stored July ladders outside the population:
    - L: c2/clean-1 with its materiality part removed from not_judged, though the outcome names "whether the exposure is material";
    - N: c2/clean-4, the big four's 2026 capex, turned into a "no main figure" refusal.
  - A miss of any planted-wrong control by either family voids the reading.
- **Counted:**
  - per arm over 78 sends: agreed hard-line faulted items, refusals, and unreadable answers (the truncation signal);
  - per topic: faulted sends;
  - every agreed high-arm fault, and every fault that differs between the arms on a topic, is reviewed against its source.
- **Outcomes, fixed:**
  - **moves:** high faulted items at most half of medium and at least 3 fewer; no topic faulted in 2 or more high draws but in no
    medium draw; refusals and unreadable answers no more than 2 above medium; the direction is unreversed when unresolved points count
    against;
  - **closes:** high at least medium minus 1;
  - **otherwise inconclusive.**
- **Spend:**
  - caps $0.25 (medium) and $0.75 (high), $1.00 together, reserved per attempt at the worst cost;
  - a breach guard;
  - a stopped arm-draw is NOT MEASURED;
  - expected about $0.08 medium and an unmeasured $0.15–0.30 high;
  - about $9.7 left of D439's $40.
- **Tests** (`effort/test_effort_probe.py`, 4 of 4): the six arm-draws through the real runner with a fake transport, each at its own
  effort; equal arms close; four medium faults against none in high move; a missed planted control voids.

**Known risk:** high effort may hit the 16,000-token output cap more often. The cap is kept equal, as you required, and unreadable
answers are counted separately and bounded in the outcome rule.

**Asked:** send now, or name what must change first. After the send: the reading (both families, 162 items), the review, and a
result round.

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
