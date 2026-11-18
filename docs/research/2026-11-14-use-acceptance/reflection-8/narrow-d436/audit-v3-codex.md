**The passage is not sound as written.** It gives a model a reason to select a figure even when the outcome names several things without identifying a main one—the choice D631 and D635 leave unresolved. It also misses one of the four proposed targets and adds 672 characters without the completed token comparison or compensating cut required by §6.

For example, “the outcome tracks a figure” can mean either “the outcome identifies this figure as the main one” or simply “the outcome mentions this figure.” In the second reading, the passage’s instruction to “ask the figure” makes the choice itself.

## 1. Clause-by-clause audit

The inserted text is in [edited-system.txt](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/edited-system.txt). Its sources are in [edit.json](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/edit.json).

| Passage | Verdict | Reason and collisions |
|---|---|---|
| “When the outcome tracks a figure” | **Consistent if “tracks” means the outcome already identifies the main figure; ambiguous otherwise.** | D397 says to judge the part named as the main one. D631 says neither D397 nor D436 supplies a way to choose when the outcome names several. The passage does not say how the model knows that the figure is already the main one. |
| “the share of that same figure that one kind makes up” | **Consistent with D436’s total-and-component example, but potentially wider in application.** | D436 treats the AI-chip portion beside the chip total as one bet. A part being mathematically included in a total does not, by itself, establish that every such pair is one bet or that the total is the main part. |
| “whether the supply that figure measures stays short of demand” | **Narrower than, and imprecise against, D436.** | It captures a supply quantity beside shortage, but a shipment *growth rate* measures a change in supply, not supply itself. D436 expressly covers shipment growth beside shortage. |
| “whether capacity keeps pace with the demand that figure measures” | **Consistent with D436’s orientation.** | D436 names demand as the figure and capacity keeping pace as its other side. |
| “the two are one bet seen from two sides, not several things with none the main one” | **Contradicts D397/D631 when mainness has not already been established.** | It turns the listed shapes into an exception to the frozen system’s line 6: “naming several with none of them the main one.” The same conflict appears in the schema’s `no_ladder` description. D436 identifies sides of a bet; it does not establish a general shape-based method for choosing the main part. |
| “ask the figure, and list that second side in not_judged” | **Consistent when the figure is already the main tracked part; otherwise contradicts the unresolved boundary.** | It agrees with D397’s display and the closing check’s “the one the topic’s outcome names,” but can override both when the outcome names multiple things without selecting one. Listing only the second side would also be incomplete if the wording contains further omitted parts: line 5 and the schema require **every** other part. |
| The three example sentences | **Their orientations are consistent with the three D436 examples, subject to the same mainness problem.** | Each says “named with,” not “identified by the outcome as the main figure.” They can therefore teach selection from the shape alone. The retailer example also equates sales with supply available to meet demand, which is less exact than shipments beside shortage. |

D436’s stated scope is clean Step 1, although it expressly says the second side is shown as not judged under D397. That supports carrying the display into the ladder step; it does not itself settle every choice of main figure in that step. See [D397, D436, D631 and D635](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4326).

## 2. Four targets

These are predictions from reading the request, not model results. Actual answers could differ because the trigger is ambiguous.

| Target | Likely question and listing | D436? |
|---|---|---|
| **acc/clean-8** | Ask 2027 HBM **shipment growth**; list whether supply remains short of demand. | **Yes**, this is Alex’s shipment/shortage example. But “supply that figure measures” may fail to match a growth rate, so the edit does not reliably express it. |
| **acc/clean-9** | Ask 2026 **total semiconductor revenue**; list the AI-chip portion. | **Yes**, this is the total-and-portion example. |
| **u3/clean-10** | The request does **not clearly direct** a question. It might ask **new capacity added** and list early arrival/easing the shortage, but the new text covers *supply short of demand* or *capacity keeping pace with a demand figure*. This topic instead names capacity additions, arrival timing and shortage relief. | D436’s cited capacity example is **demand as the figure**, with capacity keeping pace as the side. It does not expressly decide this different orientation. Treating this target as automatically settled goes beyond the stated decision. |
| **pool-17** | Ask 2026 **total accelerator shipments**; list the GPU/non-GPU composition and any other omitted comparison. | The total-and-part structure follows D436. The trigger still leaves room for disagreement over whether the outcome already identifies the total as the main part. |

## 3. Eight decline controls

“Still declines” below means the edit supplies no clear reason to reverse the decline; it is not a promise of what a model will do. The input does not include the complete themes and article context for every control, so object and publication-date reasons cannot all be verified here.

| Control | Effect of edit and whether decline is justified |
|---|---|
| **week-10-06:c1/clean-4** | Still liable to decline: two annual capex figures, 2026 and 2027, with no selected main year. The added shapes do not apply. |
| **week-10-06:c1/clean-12** | Still liable to decline: multiple years and measures. The added shapes do not choose one. |
| **fortnight:c1/clean-8** | **The control is questionable.** It asks one 2026 annual venture-funding total; prior-year and half-year figures are comparisons. Nothing in the supplied topic establishes a line-6 decline. The edit does not change this; a missing matching theme, if confirmed from the full request, could independently justify decline. |
| **pool-9** | Still liable to decline: several memory price series and a separate per-rack cost. A memory share of rack cost is mentioned, but the outcome does not clearly track a total rack-cost figure and its component as the added clause requires. |
| **pool-19** | **The control is questionable.** Enactment of the bill or equivalent measure can be one event; its provisions can describe that event. D403 permits the stated period/current fiscal-year end for a pending regulatory decision. No decline follows solely from the bill having several provisions. |
| **u1/clean-5** | Still liable to decline: multiple price series, two years and resulting rack cost. The share wording does not clearly make the tracked price series a total whose component is named. |
| **u1/clean-9** | **Decline remains justified under D417** if the item, as the supplied period says, gives no follow-up survey publication day. A share and its complement do not remove the rolling-period date rule. |
| **u2/clean-10** | Still liable to decline on no established main part: capacity coming online and persistent record prices are distinct things. It does not clearly fit demand as the figure with capacity keeping pace. |

## 4. D631’s six boundary cases

On the supplied wording, **none is clearly decided by the new passage**. That is a finding about these six inputs, not proof that the general wording cannot decide another unresolved case.

| Boundary case | Effect |
|---|---|
| Optical-switch shipments | Several checkpoints and a full-year volume; neither a part/share, shortage nor capacity-versus-demand pair. No new selection. |
| Chip sales into China | Two authorities’ decisions and resulting revenue; not one of the three shapes. No new selection. |
| Acquisition | Agreement, closing, consideration and conditions; not one of the three shapes. No new selection. |
| Investment commitments | Remaining balance, cash funded and changes in commitments. The edit does not expressly say that a stock balance and a cash flow are a total and its share. A model could stretch the example to choose a balance, but the wording does not clearly require it. |
| Memory prices | Contract prices, producers’ selling prices and margins are different measures, not a total and its share. No new selection. |
| Chip export licence | Licence status and resumed revenue are distinct events/measures. No new selection. |

The general risk remains: “tracks a figure” plus “ask the figure” can select a figure in an unresolved total-and-component outcome, even though none of these six unambiguously triggers it.

## 5. Examples

The passage contains **three written examples**, not four: bank lending, retailer sales and utility demand. It also names three abstract shapes.

- **Mirroring the 44 test topics:** Yes, structurally. The bank example mirrors **acc/clean-9**’s total plus component; the retailer example mirrors **acc/clean-8**’s shipment/supply plus shortage; and the utility example mirrors **acc/clean-10**’s demand plus capacity keeping pace. The examples do not copy those topics’ named companies, products or numbers. Nevertheless, §6 says no example is taken from a test article and requires examples that teach a general rule; substituting industries does not erase the close structural mirroring. [Test topics](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/cases.json)
- **Across industries:** The relationships can be understood in banking, drugs, retail and chips, but the wording itself names three specific industries rather than presenting portable examples in each. The retailer example’s sales-versus-empty-shelves relationship is also less precise: sales can be constrained by availability, while shortage depends on demand as well.
- **Orientation:** The examples consistently choose **total lending**, **sales**, and **demand**, respectively. The third agrees with D436: demand is the figure and capacity keeping pace is the side. This does not make capacity the main figure in the different u3/clean-10 target.

## 6. Growth

**No.** The recorded reason identifies a potentially missing instruction and says two audits found no obvious sentence to cut. That is a useful explanation, but it does not complete §6’s requirement to remove at least as much elsewhere when adding an instruction, or to report prompt tokens before and after. The token comparison is deferred to a paid send, so it has not yet been reported. The passage grows from **9,545 to 10,217 characters**, an increase of **672**. [AGENTS.md §6](/Users/lchingen/hivemind/AGENTS.md:194)

NOT SOUND: Require the outcome to identify the figure as the main tracked part before applying the D436 examples; express shipment growth accurately, avoid test-topic mirrors, and make the required compensating cut and token comparison.