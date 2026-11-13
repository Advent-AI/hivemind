**Hold the send:** the revised refusal wording conflicts with the rule for a pending regulatory decision.

Point 1 now plainly covers both cases I raised, but it also says to refuse **every** event with no stated date and no named period. [Line 22](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:22) and [D403](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4422) give a pending regulatory decision an exception: use the company’s current fiscal year-end.

I would change the event clause in both the request and schema to:

> “for an event, neither the topic nor the item gives a date and the topic names no period, unless it is a pending regulatory decision, for which use the company’s current fiscal year-end.”

I withdraw my number-check objection **as a reason to hold this six-request probe**: D402 says the answers are read by hand, and the step’s checks are not applied. The recorded difference remains relevant when the step is built.