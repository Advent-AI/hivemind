You are an independent, read-only reviewer. Do not edit files, run model calls or start runs. Read only the files named here.

Context: a step writes one judged question (its "answer choices") for each research topic. Each topic has two text fields: a
`description` (the topic's question) and an `outcome` (what is tracked). The step may instead decline ("no_ladder") in the seven
cases listed in line 6 of `clean-arch/step4-2026-11-10/ladder/candidate-system.txt`; line 5 of the same file tells it which part to
judge and what to list as not judged. The governing decisions are D397, D417 and D436 in `docs/DECISIONS-log.md` (search for the
headings "## D397 ", "## D417 ", "## D436 ").

Inputs:
- `docs/research/2026-11-14-use-acceptance/unlisted-parts/topics-66.txt`: the 66 stored topics, each with its description (D) and
  outcome (O). The prefixes july, fortnight and week-10-06 are three separate runs; the same matter can recur across runs.
- `docs/research/2026-11-14-use-acceptance/unlisted-parts/decline-audit-refusals.txt`: every time the step declined on these topics,
  with its reason and two first readers' verdicts on whether the refusal was justified (N: holds = justified).

Tasks:
1. For every topic, say whether the outcome names more than one thing. For each extra clause, give its kind: second figure, second
   event, period or checkpoint, comparison, consequence, settlement source (how the answer will be known). Mark topics that repeat a
   matter of another run.
2. For each topic whose outcome names more than one thing, say which part D397 and D417 make the main part, if they settle it, quoting
   the words that settle it; or say "needs a new choice" and state the choice in one sentence.
3. Say whether the decisions support any general distinction for finding the main part when the outcome names more than one thing.
   If they do, state it and quote its source. If they do not, say so plainly. Do not invent a rule the decisions do not hold.

Return your answer as your final message: a table for tasks 1 and 2 (one row per topic), then counts (topics whose outcome names more
than one thing; distinct matters among them; rows settled by the decisions; rows needing a new choice), then task 3.
