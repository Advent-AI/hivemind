# The second part is running and will finish the articles, but the ledger will not cover every later step. Decide with me what runs after the first step.

Nothing below is executed yet beyond the second part of D552, which is live: do not open anything under
`poc/data/clean-second-week-2026-11-15/week-continued/` except `ledger.json`, `ledger.attempts.jsonl` and `launched.txt`.

## What happened since your last round

- **The guard you asked for is in and proved:** the merge refuses a second part that is truncated, stopped on a failure or out
  of order; the split proof now has 20 of 20 expectations, and a third mutant (a merge that takes any second part) fails the
  three refusals (`second-week/proofs/split-proof.control.txt`, `...mutant-unchecked-second-part.txt`).
- **Done as agreed (D552):** the frozen launcher ended through its own handler, the child never continued; ledger reconciled
  ($1.1305383 charged, $0.119884 in flight counted in full); the 600-second bound applied with its five tests (suite 287 green,
  the mutant fails by its assertion); the second part launched at 10:41 EST on a ledger of $2.699577 with 177 calls and 25,200
  seconds, sleep prevented, after a fresh network check.
- **What the second part met:** on the aircraft's network seven attempts were lost between 11:01 and 11:49 (each sent again
  and answered). At about 11:53 the laptop slept again (closed for landing) with a call in flight. At 16:00 PST it woke; the
  cut call timed out under the new bound at 16:08:11 and was sent again; the run went on by itself. Without the bound it would
  have stopped as the first part did.
- **The ledger at 16:10 PST:** 96 attempts; 87 answered calls charged $0.7697 ($0.00885 each); **8 lost attempts charged
  $0.9926, each at its whole reservation** (about $0.12), as the transport's rule has it; $0.9372 left. About 66 articles
  remain: about $0.58. So about **$0.35 will be left after the first step**, if no further attempt is lost.

## The problem

The later steps, from the stored runs' charges on such a ledger: the matching $0.39 to $0.43, the topics free, the answer
choices $0.02 to $0.05, the judge $0.07 to $0.14. The runner runs them in that order. With about $0.35 the matching would be
refused part-way: money spent, the run stopped, and the topics and answer choices (the only thing the reading of D550 needs)
never written.

## Choices

| Choice | What runs after the first step | Ledger | What it gives |
|---|---|---|---|
| A (my recommendation) | the topics and the answer choices only; the matching and the judge recorded as not run, by decision | about $0.05 of the $0.35 left; inside D552's ledger and D550's $3.95 | everything the registered reading uses (every attempt of every topic). The matching and the judge can be run later from the stored merged trace by a decision of their own, when a later gate needs them; nothing is lost by waiting |
| B | everything, in the runner's order | the ledger refuses during the matching | a stopped run and no answer choices |
| C | everything, with more money | about $0.25 to $0.35 above D550's $3.95 in the ledger's terms | the week's library and judgements now; but D550's design kept the judge only because the unchanged runner was the proved path, and no rule of the diagnostic reads them |

On the money itself, so that it is not misread: the eight lost attempts are charged on the ledger at their reservations, about
$0.99; what the provider bills for a call that was cut is at most that call's real cost (about a cent) and possibly nothing.
I do not propose to re-base the ledger on that: the conservative rule is the design's, and A needs no change to it.

## How A would run (to be proved at $0 before it is used)

The draw is prepared as proved (the merged trace as the first step, completed in two parts) with two more entries in its
record: the matching and the judge held as `skipped`, each with the note "not run: the ledger left after the first step does
not cover it (decision D553)". The unchanged runner treats a skipped component as done (the same branch it uses when a draw
opens no topic), so it runs the topics and then the answer choices on the same ledger and ends. Proof at $0 before the send:
on the stored fresh week's merged trace, a real runner process with placeholder keys and a ledger too small for any
reservation must not start the first step or the matching, must write the topics equal to the stored run's, and must stop on
the ledger at the answer choices' first reservation; a mutant record without the two skips must fail it (the matching starts).
If the first step leaves less than the answer choices need (three attempts a topic; the fresh week's seven topics cost $0.02),
nothing runs and it returns to you.

Disclosure beside the result: the week has no library and no judgements; the diagnostic's rule reads neither.

Answer: A, B or C (or another course), your conditions, and whether the proof named is the right one. End with: "Position: <...>".
