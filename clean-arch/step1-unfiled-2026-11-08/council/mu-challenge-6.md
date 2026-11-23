# Council mu, round 7: the $0 boundary check (D469) and a candidate

Read `clean-arch/e2e-comparison-2026-11-13/ladder-refusal/main-refusal-cases.json` (every thesis the ladder step refused at least once for "no
main figure", across all stored Stage A runs and the full run: 12) and the blind reader's verdicts `reader-verdicts.md`.

**Result.** The reader's two groups match the step's behaviour by group: the six "none main" cases are refused consistently (3 of 3, 12 of 15,
15 of 15 …: right); the six "one main" cases are laddered most of the time and refused in 12 of their 66 sends (acc/clean-8 2 of 15, acc/clean-9
1 of 15, c2/clean-10 1 of 3, c3/clean-3 1 of 3, u3/clean-10 5 of 15, u3/clean-11 2 of 15). So the rule's direction holds; about one send in
six over-applies it on a case with a main one. The reader's boundary: "whether the outcome identifies a particular figure or event as the thing
being tracked, with the rest explaining, comparing, qualifying, or showing another side of that same bet … a causal connection alone is not
enough: when several independently changeable figures or events are presented without a primary one, neither is main" (D436's examples are
the same kind: the shortage beside the shipments, the AI-chip share beside the chip total).

**Candidate L2 (one clause inside the first refusal case of line 6, nothing else):** "… or naming several that an analyst would track
separately, none of them the main one; a component of the tracked total, a comparison with it, or another side of the same bet beside the
tracked figure or event is not a second main one: judge the tracked one and list the other in not_judged."
Sources: the step's own line 5 and Alex's D436 ("算一个题，第三处不改"). Counterexample read at $0: the six "none main" cases are pairs that can
each change independently with no primary named (an investment amount and the stake; obligations and awards; memory prices and rack cost …);
the clause does not name them, but Firmus's "amount and stake" could be read as one deal's two sides, which is the hardest case.

**Probe (about $0.10):** the 12 cases, L1 as frozen against L2, five sends each (120 sends; the fourth Stage A cost $0.0008 a send). Lines,
fixed now: on the six "one main" cases L2 refuses in at most 1 of 30 sends and L1's own count is reported (base rate 12 of 66); on the six
"none main" cases L2 ladders none in two or more of its five sends (no case flips) and L1 likewise; every L2 ladder on a "one main" case judges
the reader's main figure and lists the other part (read by Claude). Falsifier: L2 refuses two or more of 30 on "one main" cases, or flips a
"none main" case. Effect on the final judgement: none on the graded seven; it targets Alex's Stage A line 4 (no unjustified refusal).

Agree, or what would you change? End with: "Council position: <...>".
