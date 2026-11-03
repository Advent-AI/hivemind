**One serious issue remains:** the first filing sentence can still conflict with the company-wide figure limit.

For example, a customer’s order could make a company’s total revenue more likely to rise. If total revenue is the only open question affected, the first sentence says to file the order there. The later sentence says that question takes only the listed kinds of company figures, estimates and statements. An order does not meet that limit. [D207](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2630) set that limit to prevent demand news from accumulating under company-wide questions.

The first sentence should choose the narrowest question **that is allowed to take the statement and whose answer it affects**. If none qualifies, the result is empty. That preserves both the one-home rule and the figure limit.

I found no other serious issue in the revised [prompt](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/placement-narrow-v2.txt:2). This is a read-only judgment of the wording; it does not measure how the model will behave.