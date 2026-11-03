**The audit found serious wording problems in v65; it is not yet a faithful check of standard version 5.** The clearest example is a partner adopting a product in the same sentence as a comparison: the standard says to keep the adoption, but the check sends everything the exclusion “does not cover” back through a general test.

The findings below are about what the words permit or instruct. They are not measurements of model behavior. I made no edits.

### Findings, most serious first

1. **The check weakens boundaries that require a keep.** [review-v65.txt, line 2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/review-v65.txt:2) says: “A line that says what it does not cover leaves that to the check.” That applies to adoption on line 5, conditional valuation on line 6, and the guidance, forecasts and plans on line 3.

   The standard makes a distinction: competitor comparisons, the news behind a move and policy steps go through §5.1; **same-sentence adoption or integration is kept**, a conditional valuation with assumptions, derivation and date **is kept**, and retold guidance and forecasts or plans still in force retain their weight. [Standard §5.3 and §6](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:394)

   **Smallest fix:** Remove the blanket instruction on line 2. State the outcome at each relevant boundary: “judge by the check” for the first group; “keep” or “keep their place” for the second. Do not turn all exceptions into a closing keep list.

2. **The earlier role text can exclude evidence before this check sees it.** The role says “take it only when it has a kind and nothing on the list applies” and rejects “everything that has no kind.” The check correctly says “Fitting one of the four kinds does not keep an item” and uses the analyst’s judgment, but §5.1 says the four kinds describe what kept statements **usually** look like. [role-v65.txt, lines 4–6](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/role-v65.txt:4), [standard §5.1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:369)

   There are also conflicts with the role’s earlier rejection of repeated arrangements and its narrower treatment of other companies’ matters. A final check of **items already produced** cannot reliably recover an item omitted by the earlier instruction. The two texts are contradictory even if the final check states the newer rule correctly.

   **Smallest fix within this scope:** Preserve the accurate §5.1 and row-specific boundaries in the check; do not claim that wording the check alone resolves the earlier exclusion. The role is explicitly out of scope for rewording, so this conflict remains.

3. **D250’s analyst-interpretation rule is too wide.** Line 6 rejects “an analyst’s reading of an event already recorded that adds no new fact or calculation.” D250 and §5.3 say **“具名分析师”**—a *named* analyst—interpreting **“一件已记下的事”**, with no new fact or calculation. [D250](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2975), [standard §5.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:396)

   The check removes the named-analyst limit. Its negative condition does correctly leave a reading with a new fact or calculation outside this rejection, but it does not say as plainly as the standard that such a reading goes through §5.1.

   **Smallest fix:** Say “a **named** analyst’s reading of an event already recorded that adds no new fact or calculation,” followed by “a reading that adds a new fact or calculation is judged by the check.” Keep the conditional-valuation boundary as a required keep.

4. **The arrangement row adds a condition that D250 does not have.** Line 3 begins “background **the analyst already knew**: an arrangement the item only describes as in place, with no new step.” D250 says **“只描述一个现成安排……没有新动作的，是背景，不收，文中没写日期也一样”**: an arrangement merely described as already in place, with no new step, is background even without a date. It does not require separately establishing that the analyst already knew the particular arrangement.

   This wording could keep an existing arrangement simply because it was previously unknown to the analyst.

   **Smallest fix:** Replace “background the analyst already knew” with “background,” leaving the rest of the arrangement test intact. The new-step exception is otherwise correctly scoped: a reported new step whose age is unclear is not rejected as a retelling.

5. **The product-comparison boundary needs explicit precedence and the required adoption outcome.** Line 5 rejects “a comparison the company, a partner or a third party publishes” and then says the row “does not cover a competitor’s comparison against the company’s product” or a partner’s or customer’s adoption or integration. D250 says **“只有对手拿来和本公司产品比的按 5.1 判”** and **“同一句里伙伴、客户采用或集成的动作照留”**: judge the competitor’s comparison by §5.1, and keep adoption or integration in the same sentence. [standard §5.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:394)

   A competitor can also be described as a third party or partner. The exception points in the right direction, but explicit precedence prevents the two phrases from pulling against each other. The adoption issue is the required-keep problem in finding 1.

   **Smallest fix:** Say “except a competitor’s comparison against the company’s product, which is judged by the check”; separately say “keep a partner’s or customer’s adoption or integration, including when it is in the same sentence.”

6. **One example violates the requested generality.** Line 5’s “the card draws 415 watts” repeats the standard’s specific card example, **“这张卡 415W.”** In this extraction context it is a chip-product example, contrary to the instruction to use varied industries and no chips or examples from a test article. I cannot establish from this audit alone whether that wording also appears in a test article. The drug comparison is general and fits the rejected comparison rule; “a reviewer’s test” is consistent but vague.

   **Smallest fix:** Replace the card example with a product specification from another industry that gives no business scale. Do not change the rule itself.

### Line-by-line disposition

- **Line 1:** The analyst’s weekly-notes test, caution about repeated common knowledge, and statement that missing amount, date or scale alone cannot drop an item agree with §5.1–5.2 and D240. “Guidance, and a forecast or a plan still in force, keep their place even when retold” is right on its own; line 2 weakens it. “A long-standing situation retold” should not be read as rejecting a **new specific fact** about an old situation—for example, the role’s CFO report that older plants still run at full capacity. The standard judges new information by §5.1.

- **Line 2:** Serious problem as described in finding 1.

- **Line 3:** D250’s “in place,” “no new step” and “even when no date is given” conditions are carried correctly, apart from the added “analyst already knew” condition. The history example is general. Guidance and in-force forecasts and plans need the explicit outcome described above.

- **Line 4:** The typical-common-knowledge rule and the point that a figure alone does not automatically make a statement worth keeping agree with D243 and §5.1. The steelmaker example is general. Its *dated* forecast is an example, not a requirement that every forecast have a date; line 1 correctly says a missing date alone never drops an item.

- **Line 5:** See findings 5 and 6. The competitor comparison belongs to §5.1 judgment; adoption or integration in the same sentence is a keep. The listed product launch, shipment, delay, cancellation and changes to a value-carrying product are consistent with §6’s core subject matter. The company’s decision to change what its product costs is supported by §5.1’s example of cancelling a subscription fee; “price charged for its product” would be clearer than “what its product costs.”

- **Line 6:** See finding 3. The “hold” and “pivotal moment” examples agree with the unargued-view and characterising-quote rows. A conditional valuation with assumptions, derivation and date must be kept, not merely exempted from this row.

- **Line 7:** Fine. A political or strategic stance with neither a figure nor a decision is rejected; a policy or regulatory step is not rejected by that row and is judged under §5.1. This agrees with §5.3 and the role’s policy examples.

- **Line 8:** Fine. The price move or position is rejected; the news behind a move is judged by §5.1. The example is general.

- **Line 9:** The D250 boundary is carried accurately: the check says **“when you cannot say through which path … it moves a question about the company”**; D250 says **“说不出它通过需求、供给、竞争、定价这类路径动了在研公司哪个问题的，不收.”** Both reject mere proximity through an article, event or ecosystem. A path does not automatically keep the matter; it still receives the §5.1 judgment. This is broader than the old v64 row, as D250 requires.

- **Line 10:** Keeping one item for the same fact agrees with the standard’s same-fact row. “Keep the fuller one” is a selection instruction, not a reason to discard a distinct research matter.

- **Line 11:** Fine as an instruction to return the evidence items that pass this check.

The remaining examples are varied and do not name NVIDIA, its products, AI or chip companies. The serious findings above remain open; I cannot say that nothing serious remains.