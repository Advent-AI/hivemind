**Serious issues remain in v2.** It reopens the company-wide figure question to some sized demand news, and its product sentence can file technical details that the standard excludes. The three missed examples are useful checks, but the text alone does not prove v2 will place them correctly.

For example, a customer’s “$5 billion order” could pass v2’s new size test and be filed under total revenue, even when the relevant demand question is open. That is the path D207 was designed to close.

The audit below compares [v2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/placement-narrow-v2.txt:1) with [v1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/placement-narrow-v1.txt:1), the [version 5 standard](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:369), and the cited decisions. This is a reading of the instructions, not a measurement of model behavior.

### 1. Sentence-by-sentence trace

| V2 words | Source and finding |
|---|---|
| “a library of open questions about **the company and its world**” | Consistent with §5.1 and D208. It removes v1’s company name and complies with AGENTS §6. |
| “return the ids … or an empty list” | Consistent with D207’s placement call and one-home rule. An empty result is possible when no question fits. |
| “Read each question’s **‘takes’ line**” | D207 supplies that line. |
| “never file … under a question it **does not bear on** because no better question exists” | Consistent with D207 and §5.1. D209 later specifies that an unfiled statement is dropped with its reason. |
| “whose answer it **makes more or less likely**, the **narrowest** such question … **one only**” | The first test follows §5.1; narrowest and one home follow D207. **But** §5.1 uses that test to decide whether an analyst would keep evidence at all. It does not, by itself, override D207’s stricter limit on what goes into a company-wide figure question. The next sentences need to preserve that distinction. |
| “A question about a **product generation takes** the steps, dates, delays, cancellations and configuration changes … and named customers’ statements about receiving it” | D248 item 3 supports one question per generation and treating milestones as evidence. Section 6 recognizes the value-carrying generation and its configuration. The unconditional **“takes” all listed things** is a new, wider rule: neither source says every component detail or customer statement is evidence. |
| “A company-wide figure question … takes … a **named counterparty’s order, plan, cut or price with a size that bears on it directly**” | **New rule, contrary to D207’s root-question limit.** D207 allows the company’s own figures, guidance and management statements; D208 routes driver evidence to driver questions. Naming a party and giving a size do not make an order or price an estimate of total revenue or margin. |
| “a **general statement** that demand is strong or supply is tight” goes to a driver “when one is open, **else under none**” | Driver routing follows D208, but this is a new special rule for a broad class. Section 5.3 rejects familiar, generic demand or supply background; §5.1 can keep genuinely new, specific information. The clause does not distinguish those cases, and “else under none” can also exclude another suitable event or theme question. |
| “A question about a **share, a price or an input takes** figures, estimates and named parties’ actions … in any market the question covers” | D208 supplies those driver classes. The unconditional list is a **new admission rule**, wider than §5.1 and §5.3: naming a party or a price does not establish that an analyst would note the statement. “Any market the question covers” also does not resolve whether a geographic or period-specific fact actually bears on the stated question. |
| “News … with **none of these homes**” goes to the question naming the matter, or none | The fallback follows v1 and D207, but **“none of these homes”** inherits the overly broad homes above. It can give a figure or product question priority over a more suitable matter-specific question. |
| “A rumour is filed **exactly as a confirmed statement is**” | Preserved from v1. Consistent with §5.1’s instruction that rumours can be evidence; certainty still needs to remain visible in the record. |

### 2. The company-wide figure question can become a sink again

V1 says the figure question takes the company’s own figures, guidance, estimates of that figure, and management statements about it. V2 additionally permits a named counterparty’s sized **order, plan, cut or price**. Examples v1 would leave out of the company-wide question include:

- A named customer plans a $5 billion order, or cuts orders by 20%.
- A named customer announces a $10 billion spending plan.
- A supplier raises an input price by 8%.

Those may be useful evidence for a demand, spending, supply or pricing question. They do not on their own state the company’s total revenue or margin for the question’s period. “**Bears on it directly**” is too open to decide that boundary: a model can reason that an order contributes to revenue, or an input price affects margin, and admit the whole class.

D207 recorded that six root questions had **66% of all links** before the change; links to the two measured sinks fell from **63/60/44 to 6/1/5** across its draws. Those are historical measurements, not a prediction of v2’s count. The wording nevertheless restores a route for the same kind of demand news. [D207 and D208](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2630) make the intended boundary clear.

**Smallest fix:** remove “**and a named counterparty’s order, plan, cut or price with a size that bears on it directly**,” restoring D207’s figure-question sentence. Keep driver news under the narrowest question that names its matter, or under none.

### 3. Product generation and the three examples

D248 says one generation normally has **one question at the milestone that brings revenue**, with sampling and launch as evidence; milestones an analyst would bet on separately are exceptions. Section 6 says the configuration of the value-carrying generation can be important. Neither says every technical change to every component belongs there.

- **China market share fell to zero:** v2’s share sentence can admit it if the open share question actually covers China and the relevant period. The D253 seed is for a particular market and year, so the prompt must not treat a different market or period as automatically covered.
- **Cancellation of the four-die design in favor of two chiplets:** this is a configuration change, and v2 points toward the generation question. If both the generation and a narrower question naming the affected matter are open, the one-home instruction still requires choosing the narrowest question that the statement actually bears on; the product sentence should not automatically claim both.
- **Management expects nearly $20 billion of CPU sales:** this is a forecast of a product line, not explicitly an estimate of **total FY2027 revenue**. V2’s “management’s statements **about it**” does not clearly authorize it for total revenue. The added counterparty clause does not cover management’s own forecast. The desired home therefore remains unresolved by the text; treating component forecasts as root-figure evidence would change D207’s stated boundary and needs a decision rather than an implicit prompt change.

**Smallest product fix:** change “**takes the steps … and … statements**” to “**may take evidence about its milestones and configuration when it bears on that question, subject to §5.1 and §5.3**.” Remove the chip/rack/board/interconnect list: the rule then reads across industries and does not promote component specifications into evidence.

### 4. Noise v2 could file

The new “**takes**” lists can make matching a category sufficient, even though §5.1 and §5.3 require a judgment of the statement and the boundary on its particular row. Examples include a product’s power specification under a generation question, a company’s product comparison under that same question, a customer’s description of an existing deployment with no new action, or a named analyst’s interpretation that adds no fact or calculation. Section 5.3 has specific boundaries and exceptions for each; they should not be replaced by one blanket rejection rule.

V1’s “question that **names its matter**” could leave such statements unfiled when no matching question existed. V2’s generation and driver lists give them broader apparent homes. This is a **textual risk**, not a count of actual extra filings.

**Smallest cross-cutting fix:** make each new category sentence conditional on the existing question actually being affected and on the applicable §5.3 row and boundary; do not write category membership as an automatic “takes.” Preserve the fallback to a matter-specific question.

The audit is read-only. The sink exception and unconditional product/driver admission rules remain serious; after those are narrowed, the CPU-to-total-revenue case still needs an explicit decision if that is the intended placement.