**NOT READY TO FREEZE.** The closing check can throw away a useful financial statement just because it has no current link. For example, a cash balance could inform a future acquisition even if the article does not say so. D383 says useful statements with no current home are kept for later.

I read the three files in order, including every schema description. This is a read-only request audit; I did not read `council/ah-claude.md` or inspect model answers.

1. **Clause-by-clause verdicts**

   The entries below group clauses that make the same decision. Sources are the [signed standard](docs/prd/05-extraction-standard.html) and [D380–D386](docs/DECISIONS-log.md).

   - **Keep:** “write it in this week’s notes because it makes some question’s answer more or less likely” — **consistent**, standard §5.1: “分析员会在本周笔记里写下来” because it changes a question’s likelihood. The four evidence kinds, whole-page walk and eight-items example are also consistent with §5.1.
   - **Incomplete evidence:** “A missing amount, date or scale never drops an item on its own” — **consistent**, §5.2: “缺金额、缺日期也是证据.”
   - **Reject background and common claims:** “an arrangement … in place” and “a typical claim that is common knowledge” — **consistent**, §5.3’s existing-arrangement and common-knowledge boundaries. The exceptions for newly reported steps and specific new information carry §5.1 and D250.
   - **Product details and comparisons:** “a … specification with no business scale” and the competitor/adoption exceptions — **consistent**, §5.3 product-details row and D250 boundary 3. The additional blanket treatment of *any* product-plan change as exempt from that row is **no source** in §§2–5; it should still face §5.1.
   - **Views, policy, market moves and unrelated companies:** the closing rows rejecting “unargued view,” “political or strategic stance,” “share-price move,” and another company’s unrelated matter are **consistent** with §5.3 and D250 boundaries 2 and 4. Their stated exceptions return relevant news to §5.1.
   - **Valuation:** “a target price or valuation … is not kept” — **consistent with D385**, which says “目标价和估值结论都不留”; it deliberately overrides §5.3’s conditional-valuation instruction. “Estimates it rests on” are judged separately, consistent with D385.
   - **Repeated facts:** “same fact … within this item” is one item — **consistent** with §5.3 and D250’s counting unit. Retold guidance and live plans remain eligible; old actuals are optional under §5.3, so keeping them is **wider but permitted**.
   - **Links:** “every thesis it informs” and empty links when none covers it — **consistent** with D383’s “先存着，有观点再挂.” “Prefer the narrowest” reflects the standard’s §2 filing instruction, though it competes with “every”; see below.
   - **Figures:** “lists its useful figures” as conditions — **consistent in direction** with D382: “财务类型不应该是 thesis，而更多的是条件.” But “a balance or cash flow the item ties to nothing cannot” change expectations — **keeps narrower**, D383 and §5.1. The specific cash-flow example Alex rejected does not establish that every untied balance or cash flow is immaterial.
   - **Opening:** “one of four reasons” and excluding a financial measure on its own — **consistent** with D382 and D384; §3 supplies product node, obligation, shared quantity and policy stage. The independent-bet and public-material tests carry §4.
   - **Missing from the request:** §4 requires a candidate to explain *which* revenue, profit, cash/credit risk or competitive position changes; “can change a position” does not make that test explicit. §3 also says one question asks one quantity for one period or one event; the schema does not say so. The closing rejection of a thesis with no settlement date conflicts with the system’s “otherwise use null”: rewriting an unsupported question is allowed by §4, but an undated question cannot simply pass.

2. **Clauses pulling against each other**

   “Keep [a material statement] … with empty links” conflicts with the closing check’s automatic rejection of an untied balance or cash flow. “Link … to every thesis” versus “prefer the narrowest” can mean either all relevant links or only one. “A valuation … is not kept” conflicts with “an estimate and a valuation … each kept only if it passes the test”: the latter can imply valuation may pass. “Unfiled” historically meant discarded; although the request now explains it is kept, the old word invites the opposite reading.

3. **Examples**

   Examples span retail, airlines, banking, drugs, utilities and manufacturing; they are not confined to one industry. Several highly specific product-plan, supplier-catalogue and cash-balance examples resemble particular failure cases, but the request alone cannot establish they came from a test article. The four opening classes have only one product-node and one obligation example; AGENTS §6 asks for two or three per class. “Big matter” and “useful figure” remain broad judgments despite nearby examples.

4. **Size and additions**

   Character counts, including whitespace: system **15,068**, closing **8,534**, schema **7,598**; total **31,200**, up **4,718** from K6b. D382–D385 source the additions’ direction, but not every added boundary or example, especially the blanket cash rule. The record does not establish a reason for the full growth. Cut repeated unlinked instructions and duplicated closing explanations after preserving the final check.

5. **Smallest fixes**

   Remove the blanket cash/balance rejection; judge each statement under §5.1 while retaining Alex’s specific rejected case. Make all relevant links explicit, with narrowest as a preference rather than a limit. Make valuation rejection unconditional in both places. Add the two missing opening tests and clarify the date rule. Replace “unfiled” with “kept without links,” and provide varied examples for the two underillustrated opening classes.

**NOT READY — blocking clause: “a balance or cash flow the item ties to nothing cannot … so do not return that statement.”**