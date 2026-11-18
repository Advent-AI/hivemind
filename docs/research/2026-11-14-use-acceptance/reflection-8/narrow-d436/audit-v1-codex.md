The passage is **not sound**: it turns “two sides of one bet” into a rule that always chooses the whole figure. That choice is not in D436, and it can settle cases that D631 and D635 leave open.

For example, the passage would choose total passenger numbers over whether planes stay full. But D436 also gives the opposite orientation: demand is the figure, while capacity keeping pace is the side left as context. This is a read-only assessment of the text and supplied cases; no model was called.

1. **Clause by clause**

| Inserted clause | Verdict | Reason and collision |
|---|---|---|
| “a figure together with a part of that same figure … [is] one bet seen from two sides” | **Keeps wider** | [D436](</Users/lchingen/hivemind/docs/DECISIONS-log.md:4847>) recognizes the AI-chip share beside the chip total as one bet. It does not say every whole-and-part pair is necessarily one bet. |
| “or with a condition on it” | **Keeps wider** | D436 identifies particular second sides; it does not make every condition on every figure a second side of the same bet. A condition can itself be a separately tracked outcome. |
| “not several things with none the main one” | **Contradicts / keeps wider** | This declares a main part whenever the broad whole-and-part or figure-and-condition pattern matches. [D397](</Users/lchingen/hivemind/docs/DECISIONS-log.md:4326>) says a topic with no main part gets no question; [D631](</Users/lchingen/hivemind/docs/DECISIONS-log.md:8527>) and [D635](</Users/lchingen/hivemind/docs/DECISIONS-log.md:8618>) leave the choice open when several parts are named. It collides with the decline case in [system line 6](</Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/frozen-system.txt:6>) and the same case in the [schema’s `no_ladder` description](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json:19>). |
| “ask the figure, and list the part or the condition in `not_judged`” | **No source for the selection rule; contradicts D436’s demand example** | Listing the unjudged side is consistent with D436 and D397. Automatically choosing the whole figure is not. It also collides with “Judge the one the topic’s outcome names as what is tracked” in [system line 5](</Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/frozen-system.txt:5>) and the [closing check](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-closing.txt:1>) when the outcome names several without selecting the whole. |
| The four examples | **Keep wider; one reverses D436’s orientation** | Each teaches the same automatic choice. The airline example selects passenger count over capacity utilization, whereas D436’s capacity-and-demand example makes demand the figure and capacity keeping pace the side. See item 5. |
| “Two separate figures, or one figure for two years, are still several things” | **No source as a general rule; ambiguous against D436** | The request already requires one figure for a named period. Two equally tracked annual figures can support a decline. But D436’s demand and capacity example can contain two separate figures as sides of one bet, and a previous year can be a comparison rather than another tracked question. See item 6. |

The passage does not explicitly cancel the other decline cases, such as a rolling period without a publication day. But its categorical “not several things with none the main one” conflicts with the existing no-main decline when its broad pattern applies.

2. **The four targets**

These are predictions from reading the request, not observed model answers.

| Target | Likely question and listed side | D436? |
|---|---|---|
| `acc/clean-8` | Ask 2027 HBM shipment growth; list whether supply remains short of demand. | **Yes.** This is D436’s shipment-and-shortage example. |
| `acc/clean-9` | Ask total 2026 semiconductor revenue; list the AI-chip portion. | **Yes.** This matches D436’s chip-total and AI-chip-share example. |
| `u3/clean-10` | Ask how much new HBM capacity is added in 2027; list whether it arrives early enough to ease the shortage and prices. | The passage pushes this answer, but **D436 does not establish this orientation**. Its capacity example puts demand as the figure and capacity keeping pace as the side. This topic names capacity and its timing, rather than a demand figure, so the cited example does not itself settle the choice. |
| `pool-17` | Ask total 2026 China accelerator shipments; list the GPU/non-GPU composition. | **Consistent by analogy** with total chips and their AI-chip portion, provided the total is indeed the tracked bet. D436 does not establish a universal whole-over-part priority. |

3. **The eight decline controls**

| Control | Edited-request assessment | Is a decline justified? |
|---|---|---|
| `week-10-06:c1/clean-4` | **Decline:** two annual capex figures, with neither selected. The final sentence reinforces that they are several things. | **Yes**, under D397’s no-main case. |
| `week-10-06:c1/clean-12` | **Decline:** 2026 and 2027 spending are both tracked. | **Yes**, for the same reason. The GDP percentages are additional comparisons. |
| `fortnight:c1/clean-8` | **Decline if the request has no matching theme.** Its 2026 funding figure is the main figure; the earlier figures are comparisons. | **Yes on the recorded theme finding**, not because it names several main figures. The supplied topic alone does not include the theme list; the [stored review](</Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-6/model/rule-audit.md:19>) reports that no theme covers it. |
| `pool-9` | **Likely decline:** memory-price series and rack memory cost are distinct figures, with no clear main one. | **Plausibly yes** under D397, though the broad “condition on it” wording could invite a model to force a relationship. |
| `pool-19` | **Not necessarily a decline.** The outcome names one event: enactment or failure of a bill. Its provisions describe that event. | **The control is wrong to require decline merely for multiple provisions.** D397 permits one event, and [D403](</Users/lchingen/hivemind/docs/DECISIONS-log.md:4414>) supplies the stated regulatory-date rule. A decline could still be warranted if no listed theme covers the matter; the supplied topic does not show the theme list. |
| `u1/clean-5` | **Likely decline:** multiple memory-price series, rack cost, and a 2026–2027 period are named. | **Yes on the supplied wording**, since no single tracked figure is selected. The new sentence reinforces the multi-year concern, though it does not resolve every interpretation of the period. |
| `u1/clean-9` | **Decline:** the survey covers a rolling twelve months and gives no publication day. | **Yes**, independently of the edit, under [D417](</Users/lchingen/hivemind/docs/DECISIONS-log.md:4606>) and system line 6. Choosing the domestic share does not remove that date problem. |
| `u2/clean-10` | **Likely decline, but not assured:** capacity coming online and persistent prices are both named. A broad reading of “condition on it” could instead select capacity and list prices. | The text does not establish that price persistence is merely a condition on capacity. A no-main decline is **plausible**, but the supplied decisions do not resolve this particular selection. It should not be treated as a certain control without that qualification. |

4. **The six boundary cases**

The first two cases below are the clearest places where the new text can decide, or push a decision, that the frozen request leaves open. The wording does not guarantee every model will make that interpretation.

| Case | Effect of the edit |
|---|---|
| Optical-switch shipments | **Finding:** the full-year total can be read as the figure and the interim cumulative shipments as parts of it. “Ask the figure” then favors the full-year number and lists checkpoints. The final sentence may also encourage treating Q4 2026 and 2027 as separate things. Neither settles how to handle the outcome’s span of checkpoints. |
| Investment commitments | **Finding / application risk:** funded cash can be read as a part of the original commitments, while the remaining balance and changes are other figures. The inserted rule pushes whichever amount the model treats as the whole over the part, although the outcome names all three and does not specify that priority. It does not reliably identify a single whole, so the particular winner remains ambiguous. |
| Memory prices | **Not clearly decided.** Contract-price changes, makers’ selling prices, and gross margins are distinct measures. The last sentence calls separate figures “several things,” but does not say which is main. If a model treats a reported price as a part or condition of the general price figure, the broad clause creates a risk of an unsupported choice; that relationship is not explicit. |
| Chip sales into China | **Not decided by the literal figure rule.** US approval and Chinese acceptance are events or authorities’ decisions, not a figure and its part. |
| Acquisition | **Not decided by the literal figure rule.** Signing and closing are events; consideration and conditions accompany them. The edit gives no event-selection rule. |
| Chip export licence | **Not decided by the literal figure rule.** Licence status and resumed revenue are different kinds of outcome; the edit does not say which is main. |

The boundary is consequently not protected: the optical case at least is exposed to an automatic choice, and commitments are exposed to the same broad reading. [D631](</Users/lchingen/hivemind/docs/DECISIONS-log.md:8534>) says D436 keeps the sides of an **identified** bet together; it does not give a general rule for identifying the main part.

5. **The examples**

- **Bank loans / commercial share:** Mirrors the total-versus-portion structure of `acc/clean-9` in the [44 test topics](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/cases.json>). It also resembles `pool-17`, though that target is outside those 44. It uses a banking measure, but the whole-and-share idea transfers to all four industries. Its orientation matches D436’s chip-total example when the total is the tracked bet.
- **Carmaker deliveries / electric share:** Also mirrors `acc/clean-9`’s total-and-portion structure, and closely mirrors `pool-17`’s shipments and composition. It transfers across industries as a total and product mix. Its orientation matches D436’s chip-total example in that setting.
- **Airline passengers / planes staying full:** Mirrors the supply-versus-demand relationship in `acc/clean-8` and the capacity-keeping-pace relationship in `acc/clean-10`, both among the 44. The concepts transfer, though “planes stay full” is airline-specific. **Its orientation conflicts with D436’s third example:** it chooses demand over a capacity-utilization side only if passenger count is treated as demand; the wording “planes stay full” instead measures demand relative to capacity. It is an imperfect analogy and does not teach the distinct D436 case where **capacity keeps pace with demand**. It cannot support a general rule that capacity or the first named figure always wins.
- **Retail sales / shelves running short:** Mirrors `acc/clean-8`’s shipments-and-shortage structure in the 44. The supply-shortage relationship transfers to the other industries, although shelves are retail-specific. Its orientation is consistent with D436’s shipment-and-shortage example.

These are changed-industry examples rather than copied company names or numbers. Nevertheless, they mirror the test topics’ structures closely, and the two total-and-share examples repeat essentially the same classification. They do not establish a closed, sourced boundary for when related measures are one bet. The example and generality requirements are in [AGENTS.md §6](</Users/lchingen/hivemind/AGENTS.md:194>).

6. **The last sentence**

“Two separate figures, or one figure for two years, are still several things” is **a new general rule as written**. The existing request supports one figure for one named period, and D397 supports declining when several things are tracked with no main one. Neither says every pair of separate figures is necessarily a separate bet: D436 explicitly keeps capacity keeping pace beside demand as context. Nor does a comparison with an earlier year by itself establish two competing tracked annual outcomes.

The smallest sound change is to remove the automatic whole-over-part selection and the broad classification, keep only the sourced instruction that an **identified** second side stays as context and is listed as not judged, and remove the final general sentence. The examples would also need to demonstrate only that sourced rule, without resolving an otherwise open choice.

NOT SOUND: Replace the passage with a narrowly sourced statement that an identified second side of the same bet remains context and is listed as not judged, without choosing the main part or declaring all separate figures or years to be separate things.