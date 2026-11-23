# Build-level notes carried to the stage-0 freeze review

From the reviews of rounds 2 and 3. Each is checked on the built artifact, not in prose.

- §1.2: the input proof runs through both real entry points in order, with an excluded control and a kept control.
- §1.5 E: the judge's cutoff for each invocation, proved on a trailing day with no articles.
- §1.5 C: the 12,000-call bound, the shared-ledger reservations, and the stop gate kept on every attempt.
- §1.5 D: the astra check at the transport on every request, retries included (`ladder_step.py:378` appends the refusal note), with a
  refused-then-retried case in the test and the dry run.
- §1.5 F:
  - the card's "neutral form" against "as its request shows it": a blind reader must not be able to tell the systems apart from the form alone;
  - Deck 1's output must reproduce under the generalised `council_mark.py`.
- §1.6: D431 "as they stood at 07-14". Prove both systems' state at 07-14 can be read from the stored outputs, or snapshot it during the run.
- §1.4:
  - the guardrail shares pool the three draws;
  - a library under 35 questions is read whole;
  - the "median of running siblings" when a sibling has stopped.
- §1.7: the request-size check on stored data; the figure is reported, never a stop.
- §6: completed-article and completed-day counts come from SQLite online-backup snapshots, never the live file.
- D666's record describes one $250 ledger. The decision recording the six-ledger replacement is appended to the log, and D666's index row is marked
  as superseded on that point. The log is never edited (AGENTS §11).
- §1.4: the "tell the systems apart from the form alone" test covers the mapping view as well as the cards.
