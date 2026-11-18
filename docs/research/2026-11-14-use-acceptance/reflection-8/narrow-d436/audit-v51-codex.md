The passage follows D654’s three permitted choices, but it is **not sound as written**: it gives only one example for each choice, while [AGENTS §6](/Users/lchingen/hivemind/AGENTS.md:227) requires two or three examples per class. It also does not clearly cover one of the four named targets.

For example, it clearly says to ask about shipment growth when the other side is whether supply **stays short of demand**. One target instead asks whether new capacity **arrives early enough to ease a shortage**. That is related, but the passage does not say it is the same case.

This is a read-only assessment of what the request says. It is not a model test.

1. **Clause by clause**

   - “**When the outcome tracks a figure**” is **consistent** with D397 and [D654](/Users/lchingen/hivemind/docs/DECISIONS-log.md:9093). It does not require the outcome to explicitly label the figure “main”; D654 settled that point.
   - “**one of these second sides of the same bet**” is **consistent** with D654 and D436. The relationship to the same bet is a condition in addition to the listed shapes.
   - “**the share of the figure that one kind makes up**” is **consistent** with D654’s total-and-share shape.
   - “**whether supply stays short of demand beside a figure that measures that supply or its growth**” is **consistent** with the shipment-and-shortage orientation. It is narrower than treating any shortage-related condition as covered; in particular, it does not clearly say that *when capacity arrives and whether it eases a shortage* qualifies.
   - “**whether capacity keeps pace with the demand that figure measures**” is **consistent** with D436’s orientation: ask demand, list capacity keeping pace.
   - “**not several things with none the main one: ask the figure, and list that second side**” is **consistent** with D654’s explicit exception. It qualifies the no-main-part decline in [system line 6](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/edited-system.txt:6) and the [no_ladder description](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json:19); it does not remove the other decline reasons. The [closing check](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-closing.txt:1) still asks for one outcome-named thing and every omitted part, so it is compatible.
   - “**When the outcome tracks the share itself, with the total only as its base, the share is the question**” is **consistent** with D654 and the preceding sentence. The two sentences apply to different tracked outcomes.

2. **Four targets**

   | Target | Question and listed context | Assessment |
   |---|---|---|
   | `acc/clean-8` | Ask 2027 HBM shipment growth; list whether supply remains short of demand. | Clearly matches D436 and the passage. |
   | `acc/clean-9` | Ask 2026 total semiconductor revenue; list the AI-chip portion. | Matches D436 and D654. |
   | `u3/clean-10` | The intended result is to ask 2027 capacity added and list early arrival and shortage relief, including the price context. | The passage does **not clearly direct** that result: the outcome asks about arrival timing and easing, rather than whether supply *stays short of demand*. D436’s record identifies shortage beside shipments, but the passage’s exact trigger leaves this target uncertain. |
   | `pool-17` | Ask total 2026 accelerator shipments; list GPU versus non-GPU composition. | The total/composition relationship fits the share shape, consistent with D654. |

3. **Decline controls**

   [audit-topics.json](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/audit-topics.json:28) contains **six** designated decline controls, not eight. It separately names two topics as *not used as controls*. Against the themes actually supplied:

   | Control | Result under the edited request |
   |---|---|
   | `week-10-06:c1/clean-4` | Decline: it tracks two annual capex figures with no main year. The inserted shapes do not choose one. |
   | `week-10-06:c1/clean-12` | Decline: it tracks capex in two years with no main year. The GDP percentages are not a kind’s share of the capex figure. |
   | `fortnight:c1/clean-8` | Decline is justified if robotics-startup venture funding is outside the listed themes. **AI capital spending** is listed, but funding raised by startups is not itself capital expenditure. The year and comparison figures alone do not justify declining it. |
   | `pool-19` | Decline: general legislation banning superintelligent AI is not covered by a listed theme. It is not chip-export control merely because both involve government. The pending-regulatory date rule does not cure the missing theme. |
   | `u1/clean-9` | Decline: the tracked share covers a rolling 12 months and no publication day is given. D417 remains applicable even though the share is a valid question shape. |
   | `u2/clean-10` | Still liable to decline for no identified main part: the outcome names capacity coming online and prices persisting, rather than one of the passage’s three clear shapes. This is a judgment about the text, not a measured model result; D654 specifically says to report this case rather than let it decide verification. |

   Of the two excluded topics, `pool-9` and `u1/clean-5`, neither has a clear total-and-kind-share, supply-short-of-demand, or demand-and-capacity-keeping-pace trigger in its **outcome**. I would not count either as a successful decline control: the file explicitly excludes them because of their relationship to D436.

4. **Six boundary cases**

   The insertion does not decide any of them on its stated shapes:

   - **Optical-switch shipments:** several shipment checkpoints; none is a listed second side.
   - **Chip sales into China:** decisions by two authorities; neither is a listed shape.
   - **Acquisition:** agreement, closing, consideration and conditions; none is a listed shape.
   - **Investment commitments:** remaining balance, cash funded and changed commitments; a balance relationship is not automatically a kind’s share of a tracked total.
   - **Memory prices:** contract prices, selling prices and margins; separate measures, not one of the three shapes.
   - **Chip export licence:** licence status and resumed revenue; neither is a listed shape.

   Thus the passage does not introduce the description-priority rule refused in [D631](/Users/lchingen/hivemind/docs/DECISIONS-log.md:8527) and [D635](/Users/lchingen/hivemind/docs/DECISIONS-log.md:8618).

5. **Examples**

   The four examples use generic banking, steel and utility language; they do not name a tested company, product or number. But three plainly **mirror the relationships** in the 44 test topics: total revenue and its AI-chip portion, shipments and shortage, and demand and capacity keeping pace. That structural resemblance is necessary to illustrate the ruled-on shapes; I cannot establish from the texts alone that the examples were copied from test articles.

   Their rules transfer to banks, drug makers, retailers and chip makers, although each concrete example uses a particular industry. Their orientations agree with D436: total lending, shipments, and demand are asked; the share-first example asks the share.

   The remaining defect is the count: there is **one example each** for total/share, shipments/shortage, demand/capacity, and share-first. AGENTS §6 calls for **two or three per class**.

6. **Growth**

   The diff confirms **9,545 to 10,529 characters**, an increase of **984**; `edit.json` reports **2,031 to 2,234 tokens**. Its reason explains why this missing ruling needs text and says reviewers found no safe cut. That is a reason for growth, but it does not itself demonstrate the required whole-request search for text to cut, merge or split. The passage also still falls short of the example requirement.

7. **Share-centred counterexample**

   For `u3/clean-11`, the request should ask the **ASIC-versus-GPU spending share**, not total spending: the outcome tracks the split and the total is its base. The outcome also names a split of incremental compute capacity; the request must list that separate capacity measure if it is left out. D654’s recorded verification limit is narrower: it checks that the total is not asked.

8. **Same-bet trigger**

   Yes. “**one of these second sides of the same bet**” requires both a listed relationship and the same-bet connection; the shape by itself does not establish that connection. The share-first sentence is consistent with the main sentence: it preserves the share when that is what the outcome tracks, with the total serving only as its base.

NOT SOUND: Add independently sourced examples to reach two or three per class, offset the added text where the whole request permits, and clarify the capacity-arrival target only within the scope of an authorized ruling.