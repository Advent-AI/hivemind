**Serious issues remain:** v69a adds filters that can reject evidence the signed standard keeps. For example, a named customer’s new order without a stated size can matter to revenue, but the new wording can reject it for lacking both a date and a size.

This is a read-only audit of the changes in [role-v69a-draft.txt](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-31-reference-context/role-v69a-draft.txt:5), using [standard version 5](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:369) and the decisions named in the earlier audit.

1. **The new definition of “new” requires details the standard does not.** It says “a **dated** event or step,” “a forecast or plan **with a period**,” and “a specific judgement **with a reason**.” It later requires `new_in_it` to name “the date, step or figure the item is the **first to report**.”

   Section 5.1 calls a new event, figure or **new specific judgement** an increment. It does not require the judgement to include a reason or a figure. Section 5.2 permits forecasts, rumours, counter-examples and conditional or distant statements; D240 says a missing amount or date alone is not a reason to drop a named party’s action. An item also need not prove it was the first to report a figure: §5.3 says a development is not a retelling when the text does not show it is old. The new wording conflicts with the draft’s own opening promise to keep qualifying items without an amount, date or scale.

   **Smallest fix:** restore v68a’s “new event or step,” “new figure,” “new forecast or plan,” and “new specific judgement.” Delete the requirement that `new_in_it` name a date, step or first-reported figure; let it state the new information or permitted retelling in a few words.

2. **The “not new, whoever says it” list turns specific boundaries into blanket rejection rules.** Its five parts have different problems:

   - “**the company describing what its product does or saves**” is wider than §5.3’s product detail **without business scale** and D250’s specified product comparisons. It can also sweep up a new adoption or integration step in the same sentence, which the product-detail boundary sends back to §5.1.
   - “**an executive’s or author’s remark about a trend**” is wider than the rule against common knowledge and general views. Section 5.1 expressly keeps a new specific judgement when the analyst would note it; a named person can make one without a figure.
   - “**a named company listed as an example of who uses the product**” is sourced only when the item describes an **existing arrangement with no new step**. A new customer adoption must be judged under §5.1, including when no size is given.
   - “**a comparison with history or with another industry**” has no blanket source in §5.3. The row on product comparisons is about who publishes a product comparison; it is not a ban on every historical or cross-industry comparison.
   - “**a reporter’s own market-size figure with no source**” has no blanket rejection in the cited rows. Whether it is new, useful and sufficiently connected is judged under §5.1; its source and certainty are recorded separately.

   **Smallest fix:** delete the added “Also not new, whoever says it” sentence. The existing §5.3 rows and their own boundaries already handle product details, common claims, background, existing arrangements and the specified comparisons.

3. **The company-wide quantity sentence is a new rule, not D207’s one-home rule.** The draft says such a question “is moved **only by a figure or guidance for that quantity, or by a named customer’s order, plan or cut with a size**.” [D207](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2630) is a *placement* rule: company-wide figure questions take “their own figures, guidance **and management statements**,” and it files a statement under the narrowest question. It does not say that other evidence cannot change the likely answer, and it does not impose the draft’s customer-size test. Section 5.1 asks whether the statement makes an answer more or less likely; D240 rejects a missing-size gate.

   **Smallest fix:** delete the “company-wide quantity question … only” sentence. The preceding instruction to name the question and explain **how** the statement changes its answer can remain; “supports demand” alone does not explain the path.

4. **The new definition of a question risks applying the opening test to evidence.** “A question is a bet with an answer that **a figure or an event will settle**” borrows the shape of a question worth formally opening. Section 5.1 also permits evidence that moves a customer’s, supplier’s or macro question that is **not open and too small to open**. Requiring the model to recast every such question as a settleable bet can exclude useful conditional or incomplete evidence before the analyst’s judgement.

   **Smallest fix:** replace the sentence with “Name the question whose answer the statement makes more or less likely, whether it is open, worth opening, or too small to open.” The existing instruction to leave `links` empty for the last case is consistent with §5.1.

The unchanged descriptions of a **retold forecast or plan still in force**, a **past actual figure as optional**, and an **existing arrangement with no new step** have sources in §5.3 and D250. The problem is that the added absolute filters can override those boundaries before they are applied.