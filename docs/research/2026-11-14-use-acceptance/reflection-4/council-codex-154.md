The year split is a credible **design lead**, but the review has not yet shown that it meets D614’s criterion or moves a gate. I recommend developing its design at $0, then returning to the council before building or sending anything.

[D38](/Users/lchingen/hivemind/docs/DECISIONS-log.md:753) supports separate yearly views. The proposed mechanism still contains judgments: the model must identify the same quantity in two years and decide that both years are questions worth tracking. Code can distinguish two supplied years; it cannot establish those meanings merely from their labels. The two capex cases support the lead, while the 20 topics that mention two years but track one are essential controls.

The proposal does **not** meet D612’s stated gate-moving condition on the evidence presented. It may nevertheless be worth designing as a possible repair of the product defect D397 explicitly left open. That is a separate reason to pursue it, not evidence that gate 1 will pass. Nor should the review say the defect is closed before the split is built and measured.

Before any probe, the design needs to establish:

- **The unit and writer path:** whether two genuine new topics are created or one topic produces two views; how each receives an identity, evidence, dates and later updates; and how that respects D397’s one-question-per-topic rule.
- **The boundary:** one quantity in two years, a prior year used only as a comparison, two different quantities, multi-product questions, and the allowed-year and already-ended-year rules. Intel and Firmus are useful guards but do not exercise this boundary.
- **The test and its limit:** stored-request checks and a blind comparison of the original and split outputs, including wrong extra questions and lost context. The unchanged form may read each child, but that alone does not make two children comparable to one original gate item. State a product-level decision rule separately from the official gate.
- **The stop condition:** close the candidate if it cannot identify two worthwhile yearly bets without creating a question for a context year, losing a meaningful qualification, or breaking an existing guard.

The two capex matters are development cases, not independent acceptance evidence. A few-cent probe should be separately reviewed once the design and $0 checks make the result interpretable.

CONSENSUS: develop the period-splitting design at $0 as a product-defect lead; do not claim a gate movement or authorize a probe yet.