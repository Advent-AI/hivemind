# Finishing the week of 10-06 as a diagnostic: the matching, the judge and a reading of the last answers (D558, under D439), 2026-11-15

**Not started. It starts only on Alex's word.** It spends, and the order of the gates is his. It passes no gate.

## What it would show, and what it would not

The week's questions exist (11 of the 13 topics have written answer choices in the first attempt, which is the one the judge
uses), but nobody has seen how the system answers them: the matching and the judge were not run (D553). Finishing the week
shows whether the answers to the questions that exist are supported by what the judge was shown, on a second week outside the
tuned days, beside the fresh week (6 of 7 last answers supported by both reader families). It does not show anything about
the two spending topics that got no question, nor whether a fact that never reached an answer would have changed it, nor a
rate: one week, one run, a week continued after a stall.

## The run

- **Inputs, unchanged:** the merged trace of the 272 articles, the 13 topics and all three attempts of the answer choices, as
  stored in `poc/data/clean-second-week-2026-11-15/week-continued/c1/`. That draw and its record are not touched.
- **How:** `prepare_continued_draw.prepare_completion` copies those three into a new draw
  (`poc/data/clean-second-week-2026-11-15/week-completed/c1/`), each recorded as completed and copied; the unchanged runner
  (`run_fresh.py clean`) then runs what is left, the matching and the judge, on a ledger of its own.
- **Proved at $0** (`completion_entry_proof.py`, `proofs/completion-entry.control.txt`): on the stored fresh week a draw prepared
  this way, run by the unchanged runner with every call answered from the stored archives under a live reservation, gives the
  stored library, the stored decisions, the same judge request for every question on every day and the same 37 judgements;
  665 calls, none unreserved, none unknown; the copied inputs unchanged. Its mutant (the first two attempts of the answer
  choices exchanged) fails five expectations. One expectation was written blind and corrected: within a day's round the judge
  sends its questions side by side, so their order in the record is not the program's.
- **Price:** the matching, $0.34 for 235 articles in the fresh week and $0.38 for 243 in July, so about $0.39 to $0.43 for
  272; the judge, $0.07 for 7 questions in the fresh week and $0.12 for 15 in July, so about $0.08 to $0.12 for 11. About
  **$0.47 to $0.55**; **pipeline ledger ceiling $0.80** (the judge reserves about $0.013 a call and can hold eleven at once).
  Estimates, not a guarantee. Reader sessions are outside the ledger and their dollar cost is unknown. Paid calls under D439
  before it: about $22.10 of $40.
- **Conditions at the launch:** the runner's own preconditions, the suite and the frozen-ruler test green; the three
  providers reachable; sleep prevented and the lid kept open (the matching and the judge use the production transports, which
  wait 180 seconds a call and try three times).
- **Stops:** a component that stops, a ledger refusal, a judge run that is not complete. Then nothing is read and it returns
  to the council; no redo and no added money by itself.

## The reading, fixed beforehand

- **Population:** every question's last judgement by 2026-10-12, all of them (at most 11).
- **Form and item:** the fresh week's reading of last answers, unchanged (`../brief-B.md`): the request exactly as the judge
  was sent it and the answer; verdict supported, unsupported or insufficient; cited pieces checked against their own passage,
  speaker and date.
- **Controls, as then:** four planted wrong judgements (copies with the answer altered: two choices moved against the
  answer's own text, one yes or no flipped, one reason that adds a fact the request does not hold) and supported controls
  chosen afterwards by a separate reader; items shuffled with a fixed seed; the key outside the repository.
- **Readers:** two families apart; Claude's own marks on every item stored before any reader's answer is opened.
- **Disagreement:** listed item by item; no third reader; an answer counts as supported only when both families say so. A
  reader that misses more than one of the four planted items is said so beside its counts.
- **Reported:** the count of last answers supported by both families, the unsupported and insufficient ones each with its
  trace, the bad citations, the controls' results; beside the fresh week; labelled "continued, completed later, diagnostic".
