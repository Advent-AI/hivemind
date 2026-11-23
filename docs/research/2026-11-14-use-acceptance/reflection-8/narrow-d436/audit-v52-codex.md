**NOT SOUND:** D654 authorizes the central choice, but the passage’s capacity-added example is a close rewording of a test topic, and the stated reason does not yet justify all of the prompt growth.

For example, the request should ask how much HBM shipment growth occurs and show the shortage as context. D654 settles that choice. But the new vaccine example also asks how much capacity is added and whether it arrives soon enough to ease a shortage—the same structure and timing as test topic `u3/clean-10`.

This is a read-only assessment of what a careful model is instructed to do, not a model-run result. I compared [the two system texts](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/edited-system.txt), [the cases and themes](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/audit-topics.json), [the 44 test topics](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/cases.json), and the named decisions in [the decision log](/Users/lchingen/hivemind/docs/DECISIONS-log.md).

### 1. The passage, clause by clause

| Passage | Verdict | Reason |
|---|---|---|
| “When the outcome tracks a figure and also names one of these second sides of the same bet” | **Consistent.** | This uses D654’s trigger and preserves D397’s requirement to follow the outcome. It does not require an additional written priority that D654 was meant to resolve. |
| “the two are one bet … not several things with none the main one” | **Consistent.** | D654 explicitly says these three shapes are not the no-main-part decline case. This qualifies system line 6 and the matching `no_ladder` description; it does not remove the other decline reasons. |
| “ask the figure, and list that second side in not_judged” | **Consistent.** | This is D654’s direction and D397’s display rule. The unchanged closing check asks whether the question tracks the outcome and whether the other wording is listed; read with D654, it agrees. |
| “the share of the figure that one kind makes up” | **Consistent.** | It describes the total-and-its-share shape. The first sentence keeps the share tied to the tracked figure. |
| “whether supply stays short of demand, or whether a shortage eases, beside a figure that measures that supply or its growth” | **Consistent, with an example problem below.** | A shortage easing is the other direction of the shortage condition. The figure must measure the related supply or its growth. The vaccine example expresses this as capacity added and timing; that close resemblance to the test case is a separate prompt-principle problem. |
| “whether capacity keeps pace with the demand that figure measures” | **Consistent.** | It asks the demand figure and leaves capacity as context, matching D436’s orientation and D654. |
| The six total, supply and demand examples | **Consistent in orientation; one mirrors a test topic too closely.** | The examples select the total, supply or demand respectively. The vaccine example has the same added-capacity/arrives-in-time-to-ease-shortage structure as `u3/clean-10`. |
| “When the outcome tracks the share itself, with the total only as its base, the share is the question” | **Consistent.** | This is D654’s explicit counter-case. It prevents the total/share sentence from automatically changing a share-centred question into a total question. |

The main sentence does not collide with the closing check or `no_ladder` when the request is read as a whole: D654 identifies the figure as the question for the specified shapes, while line 6 still declines other no-main topics. The due-date and ownership rules remain applicable.

### 2. The four targets

| Topic | Question a careful reading selects | Listed as not judged | D436/D654 |
|---|---|---|---|
| `acc/clean-8` | Global HBM shipment **growth in 2027**. | Whether HBM supply remains short of demand. | Yes. |
| `acc/clean-9` | Global semiconductor **revenue in 2026**. | The AI-chip portion. | Yes. |
| `u3/clean-10` | Combined new HBM **production capacity added in 2027** by the three producers. | Whether it arrives before late 2027 and eases the shortage; the associated shortage/price condition. | Yes, under the ruled shortage-side reading. |
| `pool-17` | China’s total AI accelerator **unit shipments in 2026**. | The GPU versus non-GPU composition. | Yes, if that composition is read as the named parts of the total. |

### 3. The six decline controls

| Control | Expected result and reason |
|---|---|
| `week-10-06:c1/clean-4` | **Decline.** Combined capex for 2026 and 2027 names two yearly figures; none of D654’s three shapes chooses between them. |
| `week-10-06:c1/clean-12` | **Decline.** The question asks for 2026 and 2027 global AI spending. The GDP percentages are comparisons, not a share of the spending figure itself. |
| `fortnight:c1/clean-8` | **Decline.** Physical-AI venture funding is not covered by the listed themes. The 2025 and H1 2026 figures are comparison values, so they do not create a separate no-main reason. |
| `pool-19` | **Decline.** The proposed AI-systems ban is not covered by a listed theme. Its being a pending regulatory decision supplies a date under D403, but does not supply an eligible theme. |
| `u1/clean-9` | **Decline.** It tracks a share over a rolling twelve-month period, with no publication day given. D417 expressly confirms that decline. The share exception does not override it. |
| `u2/clean-10` | **Decline remains justified, but is less certain in application.** Its outcome names whether meaningful capacity comes online before late 2027 and whether record prices persist; it does not identify an annual supply figure paired with shortage in the form the passage specifies. The passage does not authorize choosing between those event and price parts. A model could nevertheless overread the description’s “how much capacity” as the figure; this is a prediction risk, not proof of the request deciding it. |

None of the six controls needs to be discarded on the text and themes supplied.

### 4. D631’s six boundary cases

The inserted shapes do not select a part in any of these cases:

| Case | Why the passage does not decide it |
|---|---|
| Optical-switch shipments | Several shipment checkpoints and periods; no total/share, supply/shortage, or demand/capacity pair. |
| Chip sales into China | Two authorities’ permissions or restrictions; not one of the three figure shapes. |
| Acquisition | Agreement, closing, consideration and conditions; not one of the three shapes. |
| Investment commitments | Remaining balance, cash funded and changes to commitments; no listed figure-and-second-side relationship. |
| Memory prices | Contract-price changes, makers’ selling prices and gross margins; not a supply figure paired with shortage. |
| Chip export licence | Licence status and the company’s China revenue; neither is one of the three specified pairings. |

The edit does not introduce the rejected description-priority rule for these cases.

### 5. Examples

- **Source and resemblance:** None names the test company, its products or its numbers. The examples necessarily illustrate the same general shapes as the ruled cases. However, the vaccine-maker example—“new production capacity added … whether it comes soon enough to ease a shortage”—closely mirrors `u3/clean-10`’s new production capacity and whether it arrives early enough to ease the shortage. Changing industry alone does not remove that resemblance. The other examples share the broad ruled shapes, but I found no equally specific factual match among the 44 topics.
- **General application:** The rules read across industries. The examples use different industries rather than requiring a bank, drug maker, retailer or chip maker to have the same business measures.
- **Orientation:** The bank and drug-sales examples choose totals; steel shipments and vaccine capacity choose supply; utility power demand and port volume choose demand. The two counterexamples choose the share. The utility and port examples therefore follow D436’s demand-first orientation.

### 6. Growth

The reported growth is **9,545 to 11,119 characters**, and **2,031 to 2,364 prompt tokens**. The need to carry D654, plus the requirement for examples, explains why some added text is needed. The council-loop warning also correctly says that an arbitrary cut is a separate behavioral change.

That is **not yet a sufficient reason for keeping all growth**. AGENTS §6 also requires an audit of the whole request for text that can be cut, merged or split, and says examples should replace an abstract clause where applicable. `edit.json` says nothing was cut because cuts are levers; it does not show that the existing text was examined and that each possible cut or merge would remove needed behavior. A written reason is present, but the required supporting analysis is missing.

### 7. Share-centred counterexample

For `u3/clean-11`, the counter-case says to ask the **share or split of accelerator spending**, not total spending. Its outcome also mentions a split of incremental compute capacity, so this review does not conclude which of those two splits must be judged. The specific safeguard tested here—do not switch to the total—is stated correctly.

### 8. The same-bet trigger

The three shapes are tied to the tracked figure: a part **of that total**, a shortage **beside that supply or its growth**, or capacity keeping pace with **the demand that figure measures**. Two unrelated things merely mentioned together do not satisfy that wording.

The main and counter-case sentences are consistent: the first applies when the outcome tracks the total or other figure and names its second side; the second applies when the outcome tracks the share itself and the total is only its base. The model still has to read what the outcome tracks; the text does not turn any mention of a share into an automatic total question.

NOT SOUND: Replace the vaccine example with a non-test-derived example of the shortage shape, and document the whole-request cut/merge review that justifies the remaining growth.