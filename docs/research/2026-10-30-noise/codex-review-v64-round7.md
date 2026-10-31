**v64 makes the exceptions easier to understand, but I would not accept it as written.** The largest remaining problem is that the final check only reviews items already selected, while the earlier role text can reject an item that the check is meant to protect. For example, a company’s decision to make a product free could be rejected as a price detail before the check ever sees it.

The findings below are from a read-only comparison with the [signed standard](docs/prd/05-extraction-standard.html), [decisions](docs/DECISIONS.md), [v63](src/hivemind/prompts/review-v63.txt), and [the role text](src/hivemind/prompts/role-v64.txt). They describe risks in the wording, not measured model behaviour.

### Findings, most serious first

1. **The check cannot recover protected evidence that the role text rejected earlier.**  
   v64 says, “**Read each evidence item back**.” But the role text first says “**take it only when it has a kind and nothing on the list applies**” and rejects product-price details without business scale. The standard keeps the company’s decision to cancel a subscription fee as supporting evidence; §6 also gives examples of core evidence without an amount. A retold forecast or plan can face the same problem: the role rejects repeated arrangements, while §5.3 protects forecasts and plans still in force.

   **Smallest fix within this block:** Ask the model to check the article against the resulting list as well as rereading the list, and add any statement the role’s earlier rejection removed but §5.1 and the boundaries keep. A list-only check cannot resolve this conflict by wording its exceptions more clearly. This is a procedural change to the check, not a claim that a particular run missed these items.

2. **“Usually fail” weakens the standard’s reject rows.**  
   v64 says, “**These usually fail the check**.” Section 5.3 and §6 say to check the boundary of each reject row, treat its optional cases as optional, and reject the rest. “Usually” leaves room to keep, for example, a bare product power figure merely because the model thinks it might affect an answer.

   **Smallest fix:** Say: “Apply these rows after checking each row’s boundary. What falls within a row and not its boundary is not kept.” Preserve the separate instruction that the named boundary is judged by §5.1.

3. **The product exception adds an unsupported scale condition.**  
   The product row protects “**the launch, shipment, delay or cancellation of a product that sells or will sell at scale**.” Section 6 protects progress and configuration of the product that carries the company’s value, and D240 says missing scale alone cannot drop evidence. The quoted wording can make an unquantified launch or cancellation look unprotected even when it concerns that key product.

   **Smallest fix:** Replace that phrase with “the launch, shipment, delay or cancellation of the product that carries the company’s value.” Continue to judge other product events by §5.1; do not turn the exception into an automatic keep.

4. **The “not” instruction is understandable but still easy to reverse.**  
   “**What a line names after ‘not’ is not dropped by that line; the check judges it**” contains two uses of “not,” and each bullet then places a protected item directly after a reject example. A model could still read “not a partner’s or customer’s adoption” as a reason to discard the adoption—the failure the user describes for v62. The wording does not actually say that; this is a reading risk.

   **Smallest fix:** Replace the semicolon and “not” in each row with a positive label: “**Boundary — do not reject under this row:** …; judge it by the check.” This keeps each exception local without making it an automatic keep.

5. **The conditional valuation boundary is less precise than the standard.**  
   v64 protects “**a valuation with its assumptions, derivation and date**.” Section 5.3 specifies a **conditional** valuation with those elements, and §6 classifies it as supporting. The wording omits “conditional” and tells the model only that the row cannot drop it; it does not convey the standard’s positive treatment.

   **Smallest fix:** Use “a **conditional valuation** with its assumptions, derivation and date,” and state that the standard keeps it as supporting evidence when applying the overall rule.

6. **“Keep the fuller one” has no exact source and can lose information.**  
   Section 5.3 says one fact repeated in an item is one evidence item; the role text describes keeping its terms and figures together. Neither says that the longer of two versions is necessarily sufficient. One sentence may be longer while the other contains a material condition.

   **Smallest fix:** Replace “keep the fuller one” with “keep one item for the fact, preserving its material terms.” This concerns the wording of this check, not downstream matching.

### Line-by-line source audit

| v64 text | Source and assessment |
|---|---|
| “Before you return … check it once” | The user’s requested procedure; the keep rule is §5.1. The limitation to existing items is finding 1. |
| “Read each evidence item … this week’s notes … more or less likely” | §5.1, including questions about the company, customers, suppliers, competitors, regulators and the economy. **The test itself is fine.** |
| “Ask first whether it is new … common knowledge … long-standing situation … unargued view” | §5.1 and D243. **Fine**, subject to the protected retellings that follow. |
| “Guidance, and a forecast or a plan still in force … even when retold” | §5.3 retellings boundary and D243 proposal 6. **Fine**, but finding 1 limits its reach. |
| “Fitting one of the four kinds does not keep an item” | §5.1 explicitly says this. **Fine**, but it conflicts with the role’s earlier kind-and-list procedure. |
| “A missing amount, date or scale never drops an item on its own” | §5.2, §6, D240 and AGENTS §6. **Fine.** |
| “A forecast, a rumour, a counter-example or a distant or conditional statement is judged like any other” | §5.2. **Fine:** their nature alone is not a reason to drop them. |
| “These usually fail …” and the “not” instruction | §5.3’s reject rows and boundaries are the source, but the procedure is weaker and harder to parse. See findings 2 and 4. |
| Background and “not a development … without making clear that it is old” | §5.1 common knowledge and §5.3’s retelling boundary. **Fine.** |
| Typical common-knowledge claim, figure plus specific account, and the unrelated figure example | §5.1, including its unrelated market-share example, and D243 proposal 5. **Fine.** A figure alone does not make a statement relevant. |
| “Not a dated forecast of a shortage, a price or demand” | §5.1’s shortage forecast and §6’s core shortage example support it. **Fine as an example**, provided “dated” is not read as a requirement for every forecast; the opening sentence protects missing dates. |
| Product, game, driver and benchmark detail | §5.3 product row. **Fine** as the reject class, subject to its boundaries. |
| Competitor comparison; partner or customer adoption or integration | §5.3 product boundary and §5.1 kind 2; D240. **Correctly attached** to the product row and still judged by the check. |
| Product launch, shipment, delay or cancellation at scale | The standard supports protecting key product progress (§6), but does **not** source the quoted scale condition. See finding 3. |
| Change to the plan or configuration of the product carrying value | §6 includes that product and its configuration; §5.2 protects plans. **Fine**, subject to finding 1. |
| Company decision to change its product’s cost | §5.1’s cancellation of a subscription fee and §6’s supporting example. **Fine**, subject to finding 1. |
| Unargued view and characterising quote | §5.3’s unargued-view and characterising-quote rows; D243 proposal 10. **Fine.** |
| Valuation with assumptions, derivation and date | §5.3 and §6 support a conditional valuation, but v64 omits “conditional” and its positive treatment. See finding 5. |
| Political or strategic stance without a figure or decision; policy or regulatory step | §5.3 political/strategic row and its boundary; §5.1 kind 4. **Correctly attached and fine.** |
| Share-price move or investor position; news behind the move | §5.3 share-price row and boundary. **Correctly attached and fine.** The standard makes the post-earnings reaction itself optional. |
| Other company’s unrelated valuation, share price or deal; its actions or operating figures | §5.3’s D238 paragraph and §6. **Correctly attached and fine:** actions and figures still require §5.1 judgment. |
| Second item for the same fact | §5.3 supports one item per repeated fact. “Keep the fuller one” has no exact source; see finding 6. |
| “Return only the items you keep” | Consistent with applying the keep decision, but it does not cure finding 1. |

### v63 exceptions and the role text

v64 retains the substance of v63’s closing list: forecasts, rumours, counter-examples, distant or conditional statements, missing amounts and dates, other parties’ actions and figures, competitor comparisons, adoption, product progress and pricing, policy steps, valuations, and news behind a price move. The material changes in scope are the product-scale wording and the less explicit conditional valuation described above. The exception for an action without an amount or date is now expressed through the general incompleteness rule and the other-company action boundary; it is no longer a global automatic keep, which agrees with §5.1.

The role text is byte-identical to role-v53. Its **kind plus reject-list** instruction conflicts with v64’s statement that a kind alone does not keep an item, because the role makes the earlier selection before the final check. Its product-detail and repeated-fact instructions can also exclude items that v64 later protects. The local product, policy, price-move and other-company boundaries themselves are otherwise attached to the right rows.

No prompt was edited and no model call was made.