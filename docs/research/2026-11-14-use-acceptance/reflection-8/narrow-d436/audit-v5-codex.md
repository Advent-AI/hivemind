**The passage is not sound:** it can make the shape of a topic choose the question even when the outcome has not established which figure is tracked. For example, “total lending and the commercial share” is directed to the total, although the example does not say the outcome makes the total the main figure.

This is a read-only assessment of the supplied text, not a model test. The control list contains **six cases, not eight**; I assessed all six supplied.

### 1. Passage, clause by clause

The inserted text is in [edited-system.txt](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/edited-system.txt:5). The comparison is with [D397, D436, D631 and D635](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4326), [the frozen request](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/frozen-system.txt:5), [the closing check](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-closing.txt), and [the schema](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json:19).

| Clause | Verdict | Reason |
|---|---|---|
| “When the outcome tracks a figure” | **Consistent** | D397 says to judge the part the outcome names as tracked. If tracking is already established, this does not choose it. |
| “and also names, as a second side of that same bet” | **Consistent in principle, but insufficiently decisive** | D436 calls for a second side of the same bet to remain context. The clause does not explain how to identify the tracked side when both are named without priority. |
| “the share of the figure that one kind makes up” | **Keeps wider** | D436 names AI-chip share beside chip total as a second side; it does not say every total-and-share pairing makes the total the tracked figure. |
| “whether supply stays short of demand beside a figure that measures that supply or its growth” | **Consistent for D436’s shipment example; wider as a general selection rule** | D436 treats shortage beside shipments as context. The wording also covers other supply measures and their growth, without establishing that each is the tracked side. |
| “whether capacity keeps pace with the demand that figure measures” | **Consistent for the stated orientation** | D436 explicitly puts capacity keeping pace beside demand. It still depends on the outcome actually tracking demand. |
| “the two are one bet … not several things with none the main one: ask the figure” | **Contradicts the unresolved boundary when tracking is not established** | If “tracks a figure” is taken as already proven, this follows D397 and D436. If the model infers tracking from the listed shapes, it selects a main part where D631 and D635 leave the choice open. |
| “list that second side in not_judged” | **Consistent** | D436 keeps the second side as context and D397 displays omitted parts as not judged. |
| Three total-lending, sales, and demand examples | **Keeps wider** | They say the figures are “named with” the other side, then direct the model to select those figures. They do not establish that the outcome tracks them. They therefore teach selection by shape. |
| “When the outcome tracks the share itself, with the total only as its base, the share is the question” | **Consistent** | This follows D397 when the share is clearly the tracked quantity. Its example does not resolve outcomes naming multiple different splits. |

The collision is conditional but material: the new “ask the figure” direction and examples can override the frozen instruction to decline when several things are named with none main, as well as the schema’s matching `no_ladder` description. The closing check asks whether the question is “the one the topic’s outcome names”; it does not resolve which one that is when the outcome names several. None of the passage expressly cancels the other date, period, or object declines.

### 2. Four targets

| Target | Likely question and listed context | D436 |
|---|---|---|
| **acc/clean-8** | Ask 2027 HBM shipment growth; list supply remaining short of demand. | **Yes.** This is the shortage beside shipments in D436. |
| **acc/clean-9** | Ask 2026 total semiconductor revenue; list the AI-chip portion. | **Yes.** This matches D436’s chip total and AI-chip share orientation. |
| **u3/clean-10** | Likely ask total new 2027 HBM capacity; list whether it arrives early enough to ease shortage and prices. | **D436 treats the cited case as one bet, but the passage does not cleanly express its timing side.** “Supply stays short” is not the same question as whether capacity arrives before late 2027. It may be listed, but the text does not ensure it. |
| **pool-17** | Likely ask 2026 total accelerator shipments; list GPU versus non-GPU composition, including the GPU decline comparison. | **Compatible if composition is the second side of the same bet.** D436 gives a total/share example, but does not independently settle every composition topic merely from its shape. |

### 3. Decline controls

The supplied themes include **semiconductor cycle**, **AI capital spending**, **custom silicon**, and **chip export controls**. They do not contain a general robotics-venture-funding theme or a general AI-safety legislation theme.

| Supplied control | Assessment |
|---|---|
| **week-10-06:c1/clean-4 — hyperscaler capex in two years** | **Still decline.** Two separate annual figures are named without a main year. Neither the new same-bet shapes nor the AI-capex theme selects one. |
| **week-10-06:c1/clean-12 — global AI capex in two years** | **Still decline.** The two years remain separate figures; GDP comparisons do not make one year main. AI capex is a listed theme. |
| **fortnight:c1/clean-8 — robotics venture funding** | **Still decline on the supplied themes.** It asks global robotics startup funding, rather than a matter clearly covered by the listed themes. It is a single calendar-year figure, so “no main figure” or the rolling-period rule would not justify the decline. The theme judgment should be checked against the full article if it supplies a narrower covered matter. |
| **pool-19 — AI legislation** | **Still decline on the supplied themes.** A broad ban and safety legislation is not clearly chip-export controls or another listed theme. The current fiscal year-end can date a pending regulatory decision under D403, so lack of a date is not the reason. |
| **u1/clean-9 — domestic accelerator budget share** | **Still decline.** Its rolling twelve-month figure has no stated publication day; D417 expressly covers this kind of case. The share counterexample does not remove that decline. |
| **u2/clean-10 — HBM capacity and prices** | **No assured decline.** A model may read capacity and persistent shortage as the new supply shape and ask capacity, listing prices. But the outcome names capacity coming online and persistent prices; it does not clearly make one main. D436 does not establish a general capacity-versus-price priority. Declining for no established main part remains justified; retaining it as a control is reasonable, with that ambiguity stated. |

### 4. Six reserved boundary cases

The edited passage does **not explicitly select a part** in five cases: optical-switch checkpoints, the two China authorities’ decisions, the acquisition’s agreement/closing/consideration, memory prices versus makers’ figures, or the export licence versus resumed revenue. Those remain unresolved under D631 and D635.

**Investment commitments is a finding.** Its outcome names remaining balance, cash funded, and changes in commitments. A model could treat remaining balance as a figure and cash funded as a part of the same commitment, then apply “share of the figure that one kind makes up” or the examples’ total-versus-part orientation. The text does not explicitly say funded cash is a share of the remaining balance, so this is a **plausible overreach, not a certain instruction**. The frozen request did not supply that selection rule. More broadly, the examples invite a model to choose a total whenever it sees a related component.

### 5. Examples

The four examples change industries and do not copy the named companies or numbers. But **three mirror the test topics’ decision shapes**: total lending/commercial share mirrors **acc/clean-9**; sales/short shelves mirrors **acc/clean-8**; power demand/capacity keeping pace mirrors **acc/clean-10**. The share-centred bank example mirrors the share-versus-total issue in the supplied counterexample. Thus the examples are not literal copies, but they are close structural translations of the cases being assessed. [AGENTS §6](/Users/lchingen/hivemind/AGENTS.md:194) requires examples from varied domains and none taken from a test article.

The principles can be translated to a bank, drug maker, retailer, or chip maker, but the **retailer sales/empty shelves** example is less exact: sales are realized transactions, whereas shelves running short depend on inventory, replenishment and demand; sales need not measure supply or its growth. It can teach an overly broad relationship.

The stated orientations agree with D436: total beside its share; supply beside shortage; **demand beside capacity keeping pace**. The counterexample correctly selects a share when the outcome actually tracks that share.

### 6. Growth

The reason establishes a plausible missing relation: the frozen request predates D436 and the proposed passage adds **951 characters** and **199 reported tokens**. But [AGENTS §6](/Users/lchingen/hivemind/AGENTS.md:194) permits an addition when the audit shows an instruction is missing and says to remove at least as much elsewhere; growth needs a written reason. “Three rounds found nothing to cut without changing behaviour” is a reason for growth, but it does not cure the unsupported selection taught by the examples or show that the full extra passage is necessary. **It is insufficient to accept this version.**

### 7. Share-centred counterexample

For **u3/clean-11**, the passage does not clearly direct a switch to total spending: its counter-case says a tracked share remains the question. But the actual outcome names **two splits**—spending and incremental compute capacity. The passage does not establish which split is the one tracked, so it does **not assure** a spending-share question. A careful model should not replace it with total spending; choosing between the two splits remains unresolved.

### 8. Same-bet trigger and consistency

“**As a second side of that same bet**” is a useful condition, but it does not by itself stop shape from deciding the main figure. The examples omit an explicit statement that the outcome tracks the total, sales, or demand and nevertheless instruct the model to ask those figures. They can teach the model to infer both “same bet” and the main side from the pairing.

The counter-case and main sentence are **consistent when tracking is independently clear**: ask the total if the outcome tracks the total; ask the share if it tracks the share. They leave a conflict in ambiguous wording because the first sentence and examples can imply total priority while the counter-case requires deciding first whether the share is tracked.

**NOT SOUND: Require the outcome to establish the tracked figure independently, and revise the examples to say explicitly which figure the outcome tracks; do not infer priority from a total-and-part or supply-and-shortage shape.**