# Agentic experience: entrusting an investment belief to an agent

October 22, 2026, second draft. English edition: October 25 (D163). This is an **unapproved experience proposal**, not the governing system design or a claim about current product capabilities. The [original draft](research/2026-10-25-english/agentic-experience.original.zh.md) retains its historical wording. The [full experience proposal](experience-prd.md) develops the same direction. Current implementation status is in [CURRENT_STATE](CURRENT_STATE.md).

## The central experience

The agent remembers the exit condition you chose before the news arrived. When new evidence moves the judgement across that condition, it brings you both the exact source and the action you previously chose.

The promise is disciplined follow-through, not profit or faster execution than the market. You choose the condition while calm. Later, the agent returns your own words rather than changing the plan for you.

A ten-second demonstration first shows the saved belief, corresponding thesis, approved condition and date; then the new quotation and changed judgement, identifying any inference; finally it asks whether to take the previously chosen action. Use recorded cases and label historical replay as replay.

## Alex and NVDA: an illustrative journey

Numeric theses are annual in the governing design. Interim earnings provide evidence; they do not settle the annual question. The draft uses August 26 as a checkpoint, not a due date. Its dated examples illustrate a proposed experience and are not newly verified financial facts.

**July 24: set the plan.** Alex says: “I hold NVDA because I think data-center demand will last through year-end. Yesterday's drop worried me.” The agent responds:

```text
The closest question we have tracked since February 25 is:
How will NVDA FY2027 annual data-center revenue compare with FY2026?
Current judgement: growth above 50%. Due: the annual results next February.

Your belief concerns demand lasting through year-end. This question concerns
annual revenue growth. Demand can hold up while falling prices reduce revenue.
Does this question represent your belief, or do you need another question?

We found no change in the evidence we track that changed this judgement yesterday.
That does not establish that the price drop was unrelated.
China revenue, gross margin and customers' own chips are other relevant questions.

Plan for your review:
Expected outcome: growth above 50%.
Position: keep the current holding; do not add.
Exit condition: sell half if the judgement falls to growth below 10%.
Checkpoints: August 26 Q2 results and November 17 Q3 results.
Due: the annual results next February.
Permission: ask me first.
A loss-based stop belongs with your broker; set that separately.
```

The draft's illustrative history shows a one-rung increase after May 20 guidance of $91 billion and no further movement after July 8 Foxconn AI-server revenue growth of 39.8%. Alex accepts the question, changes “sell half” to “sell all” and confirms. The product must make the difference between his words and the tracked question visible.

**July 25–August 25: quiet monitoring.** A persistent card beside the position shows the belief, tracked question, current judgement, last check and exit condition. It is available when Alex looks; it does not push routine reminders.

**August 26: checkpoint.** The agent reports the quarterly figure as evidence, whether the annual judgement changed, whether the exit condition was crossed and the next checkpoint.

**A day in September: condition crossed.** A company filing moves the China-revenue judgement to the lowest rung. Alex has separately chosen an exit condition for that thesis. The agent shows the quotation, its evidence tier and his approved “sell all” instruction, then requests confirmation. The action is grounded in the source and his prior plan.

**Next February: outcome.** The proposed experience reports the published annual number, year-on-year change and corresponding rung. It describes that question's outcome, not the success of the entire position. Record the share-price result separately. This proposed verification at the due date extends beyond the frozen design's implemented freeze/close rule and needs its own decision.

**The following year: inspect the record.** Show requests, approvals, refusals, whether triggered actions were justified and missed triggers. More approvals do not prove better judgement; the user decides any change to permissions or budget.

## Responsibilities and limits

The proposal expects Hivemind to supply maintained theses, ladders, due dates, evidence tiers, quotations and judgement history. It proposes two additions: publish changed judgements with their supporting evidence, and verify outcomes against actual numbers in code. Neither is authorised merely by this proposal. The early “two to four questions per company” example is not a current hard quota.

The surrounding stack maps a belief to a thesis and explains the mismatch, drafts the plan, manages permissions, executes authorised actions and retains the persistent card and activity record. Hivemind itself holds no user funds and executes no trades.

Two limits must remain visible. A trigger follows a **judgement**, which can be moved by company statements, third-party views or rumours; it is not necessarily an established fact. Also, evidence-based action can follow a price move. It addresses a broken investment reason, not loss protection.

## What the reviews changed

The self-review and three-role Codex review found a useful experience with delayed value. They corrected the quarterly settlement example, replaced “the price drop is unrelated” with “we found no relevant change,” removed automatic budget expansion after several approvals, and replaced Sunday notifications with the persistent card.

Absolute competitor claims were withdrawn. Other agents and configurable assistants may provide much of this workflow. The proposed distinction needs to be demonstrated when sources are corrected, the maintained judgement contradicts the user's preferred story or a past error remains visible. A company without maintained history must be presented that way.

A replay showing when today's rule would have triggered is an explanation, not a claim that the product would have saved the user then. The rule's author already knows the historical outcome.

## Proposed first version

Include belief-to-thesis mapping with an explicit mismatch, a draft plan, ask-first permission, quotations and tiers at a trigger, the persistent card, checkpoint/outcome messages and an inspectable activity record.

Defer market expectations, per-rung probabilities, recommendations, rankings, automatic execution, a proprietary stop-loss, automatic budget increases and routine weekly notifications. Do not say “unrelated to you,” “your whole judgement was right” or “you were lucky” from one thesis outcome.

## Proposed verification and decisions

1. Map 20 real beliefs and test both correctness and whether users can explain the mismatch.
2. Replay NVDA from July 24 through October 22, looking for missed or incorrect triggers and false “unchanged” messages.
3. Compare with an existing configurable agent on the same period, measuring omissions, delay and differing answers.
4. Show refusals, late arrivals and wrong outcomes alongside successes.

Alex still needs to approve the central experience and first-version scope. This translation grants no trading authority and starts none of these proposed experiments.
