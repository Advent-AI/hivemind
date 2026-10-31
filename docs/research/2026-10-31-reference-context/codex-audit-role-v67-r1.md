The draft still has serious conflicts with the signed standard. The main one is that it makes two filled-in fields the final keep test, while the standard requires the analyst to apply the keep rule **together with each relevant reject row and its boundary**.

For example, a model can write a plausible `new_in_it` and `moves` for a product benchmark, then read “the rest stays” as permission to keep it—even though §5.3 rejects that product detail. The same problem works in reverse: a retold forecast still in force may have no newly reported fact, but the standard says to keep it at its original weight.

This is a text audit, not a measurement of model behavior. The findings below describe what the draft says or reasonably permits the model to infer; they do not claim that a particular number of records would be lost or retained.

## Serious findings

1. **The final check replaces the signed test with a field-completion test.**  
   [Draft, lines 4–6 and 41](docs/research/2026-10-31-reference-context/role-v67-draft.txt:4): “keep the statement only when you can write both” and “drop any item whose `new_in_it` names nothing new or whose `moves` names no question; **the rest stays**.”

   The first question in [§5.1](docs/prd/05-extraction-standard.html:369)—what is new, and which answer does it move—is the right starting point. But it is not the whole procedure. Section 5.1 also asks whether the analyst would record the statement, and tells the reader to apply §5.3’s rows **and their individual boundaries**. A string can name something new and a question without making the statement one the analyst would record. Conversely, the standard explicitly keeps some retold material.

   “The rest stays” is a global keep rule. It can override the earlier reject list and recreate the failure described in the request.

   **Smallest fix:** make the final review apply §5.1 and each relevant §5.3 row with its own boundary; remove “the rest stays.” Use the two fields to explain that judgment, not as sufficient proof of it.

2. **The “new fact” requirement conflicts with forecasts, views and permitted retellings.**  
   [Line 5](docs/research/2026-10-31-reference-context/role-v67-draft.txt:5): “what is new here, **as a fact**”; “a figure already known” is “Not new”; then “Guidance, and a forecast or a plan still in force, are kept when retold.”

   A forecast, a rumour, a conditional valuation or a specific new judgment need not be a fact in the sense of an established outcome. More directly, a retold forecast may be known already, so it can fail the mandatory `new_in_it` test even though the next sentence says to keep it. The analyst persona also claims to know “the figures everyone quotes,” although the model is only given the current item and the brief question list.

   [§5.2](docs/prd/05-extraction-standard.html:386) keeps forecasts, rumours, counterevidence, distant and conditional scenarios; §5.3 and D243 preserve retold guidance and forecasts or plans still in force. They also make retold past actual figures **optional**, not categorically rejected, and say that an event is not treated as a retelling if the text and date do not show it is old.

   **Smallest fix:** define `new_in_it` as the information or applicable retelling in the item, without calling it an established fact. State the retelling boundaries as written in §5.3, including the optional past actual and the rule for material that cannot be identified as old.

3. **The opening and `moves` instructions narrow which questions may make evidence useful.**  
   [Lines 1 and 6](docs/research/2026-10-31-reference-context/role-v67-draft.txt:1) frame the purpose as changing an **open** question or raising a question worth a **new bet**. The later exception permits a question about “a customer, supplier, competitor or regulator” that is not open and is too small to open.

   That exception is helpful, but it does not cover every question in [§5.1](docs/prd/05-extraction-standard.html:369): the standard also names **macro** questions and does not limit unopenable questions to other parties. The initial framing can make the first day’s “None yet” especially restrictive. The path list is presented after “through which path,” and could also be read as closed, although §5.1 and D250 use paths such as demand and competition as examples.

   **Smallest fix:** say the answer may concern any question an analyst would note, including one about the company, another party or the wider world, whether or not it is open or worth opening. A path is required under D250 for another company’s action or operating figure to bear on the covered company; present the listed paths as examples. Leave `links` empty when no supplied or proposed question fits.

4. **Several row boundaries became unconditional keep or drop instructions.**  
   [Line 7](docs/research/2026-10-31-reference-context/role-v67-draft.txt:7) says an official’s “order, law or ruling is a policy step and **is kept**.” Section 5.3 says a policy step **cannot be dropped by the political-stance row and is judged under §5.1**. The draft’s wording is wider: an irrelevant official step could be kept merely because it is a policy step.

   The same line rejects “a comparison the company, a partner or a third party publishes” without limiting it to the **product-detail comparisons** governed by D250. That wording can reach a business-scale comparison that the standard does not categorically reject. It also omits the boundary that a customer’s or partner’s adoption or integration **in the same sentence** is not removed by the product-detail row and is judged under §5.1.

   **Smallest fix:** attach each boundary to its own row: policy steps and competitor comparisons are judged under §5.1; the D250 comparison rejection concerns product details; adoption or integration in the same sentence is independently judged under §5.1. Do not turn any of those boundaries into a global keep.

5. **The rewritten question-identity paragraph erases D248 exceptions.**  
   [Line 16](docs/research/2026-10-31-reference-context/role-v67-draft.txt:16) declares “another deadline, another milestone of the same product generation … or one deal under a plan already asked by amount” the same question.

   D248 is more specific:

   - A **later** deadline is evidence while the earlier question remains open; after an unresolved expiry, a successor is opened.
   - Milestones separately worth betting on can be separate questions, such as a drug’s phase-3 results and approval.
   - An unsigned deal’s **yes/no signing question** remains separate from a plan’s amount question.

   The paragraph also says a small deal’s “statements stay evidence,” whereas D248 says whether to keep them is decided under §5. It can therefore serve as another global keep instruction.

   **Smallest fix:** restore those three boundaries and change the last phrase to “judge its statements under the evidence rule.” The general “same outcome settles both” and “answers can move apart and are separately worth a bet” tests belong alongside these cases.

6. **The candidate-opening test is incomplete, and parts of the unchanged text remain narrower than the signed standard.**  
   [Line 16](docs/research/2026-10-31-reference-context/role-v67-draft.txt:16) gives impact and a separate bet, but does not state §4’s independent-meaning test: can the answer change while the other questions’ answers stay the same, with a different business judgment? Nor does it state that a date and public material must resolve the outcome in fixed ranges. Parts appear later, but the opening decision is not expressed as all the required tests.

   The unchanged [line 17](docs/research/2026-10-31-reference-context/role-v67-draft.txt:17) also has two existing differences from [§3](docs/prd/05-extraction-standard.html:275): `industry_aggregate` is described only as a **combined quantity**, excluding shared prices such as a contract price or interest rate; and the obligation example mentions a sized unfinished **equity stake**, omitting the signed inclusion of a sized unfinished **acquisition**. The standard notes that the current schema still uses the old `industry_aggregate` name, so the name alone is not evidence of a schema error.

   The new “too small” sentence includes “competitive position” alongside the financial effects for a deal, product or project. D248’s specific size boundary names revenue, profit, cash or credit risk; competition remains a reason in the **general** opening test. The draft blurs those two tests.

   **Smallest fix:** state the independent-meaning and verifiability tests, preserve the specific D248 size boundary, and broaden the two inherited descriptions to the standard’s shared quantity and sized unfinished stake **or acquisition**, using the schema’s actual enum name.

## Remaining sentence-by-sentence findings

| Draft text | Audit against the ruler | Smallest fix |
|---|---|---|
| “the senior analyst who has covered the company … for years” and “You know what is already known” | The analyst perspective comes from §5.1 and D243. Claiming actual knowledge beyond the supplied material has no demonstrated source in the request and risks treating a new statement as known. It also sits awkwardly with [line 13](docs/research/2026-10-31-reference-context/role-v67-draft.txt:13), “Use only this item’s information.” | Keep the perspective, but judge whether the item itself identifies a retelling; do not assert access to facts the request does not provide. |
| “most of a page is background, retelling and opinion” | Caution is sourced to D243. As a generalization it is fine, but it must not override the retelling and new-judgment boundaries above. | No separate fix once those boundaries are explicit. |
| “a new event, a new figure or a new specific judgement … even when it lacks an amount, a date or a scale” | Consistent with §5.1, §5.2 and D240, provided the statement is judged under the relevant §5.3 row. | Fine with that qualification. |
| “Read the item from its first paragraph to its last” and “eight … yields eight” | Directly supported by §5.1. | Fine. |
| “an arrangement … in place … with no new step, even when no date is given” | Correctly carries D250’s existing-arrangement boundary. | Fine; preserve it. |
| “a claim everyone following the company makes … without a figure and a specific account” | Correctly limits D243’s stricter rule to typical common-knowledge claims, rather than all claims. | Fine. |
| “a competitor’s comparison against the company’s product is judged like any other statement” | Correctly sends the exception to §5.1 rather than automatically keeping it. | Fine; retain it beside the product-detail row. |
| “a share-price move” is not kept | §5.3 makes a price reaction **after earnings optional** and says the news behind a move must be judged under §5.1. The draft omits both boundaries. | Include the optional earnings-reaction boundary and say the underlying news is judged under §5.1. |
| “an investor’s position” and “an unargued view”; a quote that only characterises | Supported by §5.3. | Fine, subject to the conditional-valuation boundary. |
| “another company’s valuation, share price or deal that touches none of the company’s markets” | Supported by D238 and §5.3. Other companies’ **actions and operating figures** must be judged by their path to a company question, rather than rejected by this row. Line 6 gestures at the path, but does not explicitly preserve that boundary. | Add the D250 row boundary locally. |
| “a named analyst’s reading of an event already recorded that adds no fact or calculation” | The rejection matches D250. The standard also says a reading that **does** add a new fact or calculation is judged under §5.1, not automatically kept. | Add that row-specific boundary. |
| “a conditional valuation with its assumptions, derivation and date is kept” | Supported by §5.3 and §6. It conflicts in practice with requiring `new_in_it` to name a “new … fact.” | Keep the valuation boundary and fix the field test. |
| “the same fact told again in other words” and one deal or measure with its terms as one item | Supported by §5.3 and the counting unit in D250. | Fine. |
| “boilerplate, bylines, forward-looking-statement text” | Supported by §5.3. The row also lists advertisements and unrelated page material; their omission means the draft does not expressly reject all examples in the standard. | Add “advertising and material unrelated to the item,” or equivalent row wording. |
| “A statement that moves no question is not evidence” | Consistent with §5.1 **only if** “question” includes the full range of questions the standard permits, not just open or separately openable ones. | Apply finding 3. |
| “A different population, source, estimate, wording or direction … is the same question” | Inherited [line 19](docs/research/2026-10-31-reference-context/role-v67-draft.txt:19) is broader than §4: the population or proxy boundary concerns the **same aggregate**, and identity rests on the same outcome settling both. | Scope the population example to the same aggregate and apply the same-outcome test. |

## Schema, examples and scope

- The stated two string fields can express the requested explanations, but the draft asks the model to “write two things … **for each statement**” even though those are **evidence fields**. Rejected statements have no specified output location. The smallest clarification is to ask the model to consider the two questions for every statement and populate the fields for each retained evidence item.
- `links` is an array, and the existing candidate schema has candidate IDs, so naming a supplied ID or a candidate ID is expressible. The draft should make clear that the written question in `moves` is not itself an ID and that an empty `links` array is valid when no supplied or proposed question fits. The existing schema is visible in [extraction.py](src/hivemind/extraction.py:120); the two added fields are part of the hypothetical contract supplied in the request, so their actual descriptions and validation cannot be audited from that contract alone.
- No example in the draft names a covered company. The examples are not company-specific. The rewritten evidence section, however, removes the varied bank, retailer, healthcare and other examples from v53 without replacing them with two or three examples per class as required by AGENTS §6. That is a prompt-procedure gap, not evidence that a particular output will fail.
- The rest is **not exactly verbatim**: besides the new opening paragraph and final check, the first sentence of v53’s customer-plan paragraph—“A number, a financial line, a target or a named customer project does not by itself open a thesis”—was removed. The separate-independent-bet wording partly covers its purpose, but the explicit rule has a source in §4 and its removal makes the opening test less clear.

The draft needs correction before it can be called aligned with the signed standard. The most important repair is to make the last review repeat **the analyst test plus the row-specific boundaries**, while treating `new_in_it` and `moves` as explanations of that judgment.