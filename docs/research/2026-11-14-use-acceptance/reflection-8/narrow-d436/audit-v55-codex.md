**SOUND:** the edited passage carries D654’s three choices and protects a topic that tracks a share itself. I found no sentence that clearly decides one of the six reserved cases.

For example, when a topic tracks total chip revenue alongside the AI-chip portion, the edited request asks total revenue and lists the portion as not judged. When the topic tracks the AI-chip share itself, it asks the share. This is a reading of the text, not a model-test result.

1. **Passage and pointers**

| Sentence or clause | Verdict | Reading against the decisions and request |
|---|---|---|
| “When the outcome tracks a figure and also names one of these second sides of the same bet … ask the figure, and list that second side” | **Consistent** | This states [D654](</Users/lchingen/hivemind/docs/DECISIONS-log.md:9093>) and carries [D436](</Users/lchingen/hivemind/docs/DECISIONS-log.md:4847>) into the display required by [D397](</Users/lchingen/hivemind/docs/DECISIONS-log.md:4326>). It specifically qualifies line 6’s decline for several things with none main. |
| “the share of the figure that one kind makes up” | **Consistent** | It is the total-and-share shape in D654. |
| “whether supply stays short of demand beside a figure that measures that supply or its growth” | **Consistent** | It covers the volume-or-growth and shortage shape. It does not explicitly add the broader question of whether a shortage merely *eases*. |
| “whether capacity keeps pace with the demand that figure measures” | **Consistent** | Demand is the figure and capacity is the side, as in D436 and D654. |
| “In each example the first is the question” | **Consistent** | All six examples put the total, supply figure or demand first. |
| “When the outcome tracks the share itself, with the total only as its base, the share is the question” | **Consistent** | This is D654’s explicit counter-case. It agrees with the main sentence: the total is not the tracked figure in this case. |
| Closing pointer: “the figure the outcome tracks …; the share, when the outcome tracks the share itself” | **Consistent** | It repeats both directions of the choice. “One of that figure’s second sides” points back to the closed list in the system text. |
| `no_ladder` pointer: “a figure the outcome tracks, named with one of its second sides as the system text lists them, is one thing” | **Consistent** | It points to the same list and requires the figure to be tracked. It qualifies only the no-main-part reason; it does not remove the other decline reasons. |

The existing sentence “Never fold two things into one ladder” is compatible: the request still judges one figure and lists the other side. The unmodified line 6 says to decline several things with none main; the new sentence explicitly says the three specified shapes are not that case. The remaining date, period and subject restrictions still apply. The [closing text](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-closing.txt>) matches the supplied frozen closing apart from its final newline; the supplied schema pointer changes the stated description.

2. **Targets**

| Topic | What a careful reading calls for | D436/D654 |
|---|---|---|
| `acc/clean-8` | Ask **2027 global HBM shipment growth**; list whether HBM supply remains short of demand. | Yes: shipment growth and shortage. |
| `acc/clean-9` | Ask **2026 global semiconductor revenue**; list the AI-chip portion. | Yes: total and its part. |
| `pool-17` | Ask **2026 total AI-accelerator shipments in China**; list the GPU/non-GPU composition and the omitted comparison in the topic. | Yes, if that composition is the named division of the total. |
| `u3/clean-10` — reported only | The intended question is **new HBM capacity added in 2027**, with its arrival timing and shortage-easing side listed. The edited text says supply or its growth and *staying short*; added capacity and *easing* do not plainly say the same thing. | Reported without a pass/fail verdict, as requested. |

The target readings come from the stored topics and are **not predictions of a measured answer**. [The 44 stored cases](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/cases.json>) contain the two `acc` topics and `u3/clean-10`.

3. **Decline controls**

| Topic | Reading under the edited request |
|---|---|
| `week-10-06:c1/clean-4` | **Decline:** it names separate 2026 and 2027 spending figures without choosing a main year. The new passage does not choose a year. |
| `week-10-06:c1/clean-12` | **Decline:** it likewise tracks spending in multiple years. The GDP comparisons are not a kind’s share of the spending figure. |
| `fortnight:c1/clean-8` | **Decline on the supplied themes:** global venture funding raised by robotics startups is not clearly covered by “AI capital spending” or another listed theme. The earlier funding figures are comparisons, not a reason to decline. |
| `pool-19` | **Decline on the supplied themes:** a broad AI-development ban and safety legislation is not clearly covered by the listed themes. A date for a pending regulatory decision would not supply a matching theme. |
| `u1/clean-9` | **Decline:** the tracked share covers a rolling 12 months and no publication day is supplied. [D417](</Users/lchingen/hivemind/docs/DECISIONS-log.md:4606>) confirms this reason. |
| `u2/clean-10` | **A decline remains justified, but application is less certain:** the outcome names whether capacity comes online and whether record prices persist; it does not clearly track an annual supply figure alongside the specified shortage condition. A model might nevertheless use the description’s “how much” capacity. D654 separately says this case is reported, not deciding. |

The two theme judgments are readings of the supplied theme names and topic descriptions. They are not claims about information an unseen article might add.

4. **Six boundary cases**

The edit does **not clearly decide** any of them:

- **Optical-switch shipments:** several shipment checkpoints; no listed figure-and-side relationship.
- **Chip sales into China:** decisions by two authorities; no listed relationship.
- **Acquisition:** agreement, closing and terms; the passage chooses none.
- **Investment commitments:** remaining balance, cash paid and changes; no kind’s share of the tracked total is stated.
- **Memory prices:** price change, selling prices and margins; no listed relationship.
- **Chip export licence:** licence status and revenue resumption; no listed relationship.

Other existing rules may affect whether a question can be written. The new passage supplies no new priority among these parts.

5. **Examples**

I compared the examples with the descriptions and outcomes of all **44** stored test topics. None copies a topic’s company, product or numbers. They **mirror the general relationships** present in those topics—total and part, shipments and shortage, and demand and capacity—which is necessary to illustrate the rules. They do not reproduce a test article’s particulars.

The relationships transfer across a bank, drug maker, retailer and chip maker. Each example puts the figure named by D436 first: total lending and total sales; shipped or produced supply; and **demand**, with capacity keeping pace as the side. The two counterexamples correctly ask the share itself.

6. **Growth**

The written reason is **sufficient to explain the growth**: D654 adds behavior absent from the frozen request, each of the three shapes has two examples, and the `cut_review` considers the system text, closing check, schema, payload and retry note. The cited [council-loop instruction](</Users/lchingen/hivemind/.claude/skills/council-loop/SKILL.md:158>) permits growth with a written reason because a forced cut can itself change behavior.

That does not prove every existing sentence is indispensable. It does make an untested cut solely to offset length unnecessary. The record gives **9,545 → 10,825 system characters** and **2,031 → 2,294 tokens**, with **1,528 characters added across all three edited places**.

7. **Share-centred counterexample**

For `u3/clean-11`, the new counter-case and closing pointer support asking the **custom-ASIC share of accelerator spending**, rather than switching to total spending. The outcome also names a split of incremental compute capacity. D654 protects the share from being replaced by its total; it does **not** settle a separate choice between the spending split and the capacity split if both are tracked without a main part.

8. **Same-bet trigger**

Yes. The main sentence requires the outcome to **track the figure**, and each listed side is tied to that figure: a share *of it*, a shortage beside a figure measuring *that supply*, or capacity keeping pace with *the demand that figure measures*. Merely mentioning two unrelated things together does not satisfy that wording.

The counter-case agrees with the main sentence: when the share is what the outcome tracks and the total is only its base, ask the share. The closing pointer now says this explicitly too.

SOUND