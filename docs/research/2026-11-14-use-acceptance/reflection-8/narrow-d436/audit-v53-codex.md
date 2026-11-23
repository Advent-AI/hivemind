**NOT SOUND:** the passage generally follows D654, but it extends the shortage rule to whether a shortage *eases*, and the unchanged request still tells the model to decline cases D654 says to answer.

For example, a shortage can ease while supply remains short. Those are different questions. D654 settles the latter alongside a supply figure; it does not establish a general rule for every question about easing.

I compared [the two system texts](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/edited-system.txt:5), [the stated sources and cut review](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/edit.json), the [closing check](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-closing.txt), [schema](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-schema.json), [cases](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/audit-topics.json), and the cited [decisions](/Users/lchingen/hivemind/docs/DECISIONS-log.md:9093). These are predictions from reading the request, not model results.

### 1. Passage, clause by clause

| Passage | Verdict and reason |
|---|---|
| “When the outcome tracks a figure and also names one of these second sides of the same bet … ask the figure, and list that second side in not_judged.” | **Consistent with D654.** It also implements D397’s requirement to list the parts left out. The phrase “not several things with none the main one” is an express exception to the system’s decline sentence on line 6. But the schema’s `no_ladder` description still independently says to decline “several with none the main one,” without that exception. The closing check likewise asks for “the one the topic’s outcome names” without explaining D654’s choice when the outcome names both sides without priority. These are request-level collisions. |
| “The share of the figure that one kind makes up” | **Consistent with D654**, provided that the figure is the tracked total and the share is its side. |
| “Whether supply stays short of demand … beside a figure that measures that supply or its growth” | **Consistent with D654** for the volume and shortage relationship. The same-bet and linked-supply wording matters: mere co-mention is insufficient. |
| “Or whether a shortage eases” | **Keeps wider than D654.** Easing and remaining short are not equivalent: a shortage can narrow without disappearing. D436 supports the specific capacity-and-shortage case presented to Alex, but the cited record does not establish a general easing rule for every supply figure. |
| “Whether capacity keeps pace with the demand that figure measures” | **Consistent with D654 and D436.** Demand is the figure; capacity is the side. |
| “In each example the first is the question.” | **Consistent** for the orientations given. It does not itself waive the other decline conditions: the question must still have an allowed period and object. |
| “When the outcome tracks the share itself, with the total only as its base, the share is the question” | **Consistent with D654.** It is the explicit counter-case to asking the total. |

The demand example also agrees with the earlier system sentence “Never fold two things into one ladder”: the passage asks one figure and lists the other side, rather than putting both in the answer choices. The unresolved conflict is the unqualified *decline* wording in the system and schema, plus the closing check’s lack of the D654 exception.

### 2. Four targets

| Topic | Question a careful reading points to; listed alongside it | D436 |
|---|---|---|
| **acc/clean-8** | 2027 global HBM shipment growth; list whether HBM supply remains short of demand. | **Yes.** This is the named shipments-and-shortage shape. |
| **acc/clean-9** | 2026 global semiconductor revenue; list the AI-chip portion. | **Yes.** This is the named total-and-share shape. |
| **u3/clean-10** | 2027 combined new HBM capacity; list whether it arrives before late 2027 and eases the shortage, including the associated price condition. | **Yes for this specific case**, which was among those put to Alex. The passage’s general wording about shortage *easing* goes further than this case. |
| **pool-17** | 2026 China AI-accelerator shipments in total; list the GPU versus non-GPU composition and the GPU decline comparison. | **Yes**, as total and composition. |

For each, the schema and line 6 leave a competing literal instruction to decline when the outcome names both without saying which is main. Thus the table states the result **under the inserted D654 instruction**, not a guarantee that the complete request produces it.

### 3. Six decline controls

| Control | Result under the edited request | Is decline justified? |
|---|---|---|
| **week-10-06:c1/clean-4** | Decline: 2026 and 2027 are two annual figures with neither selected as main. | **Yes.** D654 does not choose between two years. |
| **week-10-06:c1/clean-12** | Decline: the outcome names multiple years and comparisons without selecting one annual figure. | **Yes.** The share-of-GDP comparisons do not make the 2026 and 2027 spending totals one figure. |
| **fortnight:c1/clean-8** | Decline because the listed themes do not cover global venture funding for robotics startups. | **Yes**, under the request’s object rule. The annual period itself is allowable; the missing theme is the reason. |
| **pool-19** | Decline because the listed themes do not cover a broad federal AI-development ban and safety legislation. | **Yes**, under the object rule. `chip-export-controls` is not a general AI legislation theme. Its pending regulatory date alone would not require a decline. |
| **u1/clean-9** | Decline: the tracked share covers a rolling 12 months and no follow-up publication day is given. | **Yes**, explicitly under D417, even though the share is the main question. |
| **u2/clean-10** | The outcome asks whether capacity comes online and whether record prices persist; it does not track an annual supply figure with the shortage as its side. The edit does not settle which is main. | **A no-main decline remains justified** on that reading. It is a less clean control than the others because the description asks “how much” capacity, while the outcome frames capacity as whether it comes online. The passage does not authorize using the description to override that outcome. |

The two entangled topics were not counted as controls.

### 4. D631’s six boundary cases

The passage does **not** choose a main part in any of these cases:

| Case | Why D654’s shapes do not choose |
|---|---|
| Optical-switch shipments | Several shipment checkpoints and periods; no total-and-share, supply-and-shortage, or demand-and-capacity pair. |
| Chip sales into China | Two authorities’ decisions and a revenue consequence; not one of the three shapes. |
| Acquisition | Agreement, closing, consideration and conditions; not one of the three shapes. |
| Investment commitments | Remaining balance, cash funded and changes in commitments; no specified total with a kind’s share of it. |
| Memory prices | Price changes, selling prices and margins; related figures, but not a D654 pair. |
| Chip export licence | Licence status and resumed revenue; neither is a D654 pair. |

The edit therefore does not introduce a description-priority rule for these six.

### 5. Examples

- **Against the 44 test topics:** the steel-mill shipments and shortage example has the same structure as **acc/clean-8**. The drug maker’s total sales and largest medicine’s portion has the same structure as **acc/clean-9**. The utility’s demand and capacity example has the same structure as **acc/clean-10**. The industries, products and numbers are different, and I found no example copied from a test article. Sharing the general structure is expected when teaching the very shapes D654 names; it should not be described as an absence of structural mirroring.
- **Across industries:** the rule is expressed in terms of totals, shares, supply, demand and capacity, and can apply to a bank, drug maker, retailer or chip maker where those quantities exist. The individual examples use industry-specific nouns but do not make those nouns a condition of the rule.
- **Orientation:** both total/share examples ask the total; both supply examples ask the supply figure; both capacity examples ask demand or demand volume. That agrees with D436’s orientation. The fertilizer example nonetheless teaches the wider **easing** proposition identified above.

### 6. Growth

The recorded figures are **9,545 → 10,836 characters** and **2,031 → 2,302 tokens**. A written reason is supplied: D654 adds a previously absent rule, the classes need examples, and cuts can themselves change behavior. The cited [council-loop warning](/Users/lchingen/hivemind/.claude/skills/council-loop/SKILL.md:158) supports allowing justified growth instead of making an untested cut merely to meet a length target.

The review is **not yet sufficient as the whole-request review** required by [AGENTS §6](/Users/lchingen/hivemind/AGENTS.md:194). It examines system lines, but does not address the unchanged schema’s conflicting decline description or the closing check’s ambiguous restatement. It also does not show a review of the fixed user text and payload for contradictions, unnecessary fields or possible merges. A system-line review alone cannot establish that there is nowhere else to cut, merge or reconcile. This is a deficiency in the justification, not a demand for an arbitrary length-neutral cut.

### 7. Share-centred counterexample

For **u3/clean-11**, the inserted counter-case directs the model to ask the custom-ASIC share of hyperscaler accelerator spending, rather than total spending. It should list the separate capacity split and cost comparisons left out.

There is still a separate question about which of the multiple splits the outcome makes main; D654 does not resolve all of that topic’s possible choices. The counterexample establishes that **switching to total spending is not authorized**.

### 8. Same-bet trigger and counter-case

The three listed relationships are tied to the tracked figure: the share is **of the figure**, the shortage is beside a figure measuring **that supply or its growth**, and capacity keeps pace with **the demand that figure measures**. “Second sides of the same bet” further restricts the trigger. Two unrelated things merely mentioned together do not satisfy it.

The main sentence and the share counter-case are consistent: when the tracked figure is the total, ask the total; when the outcome tracks the share and the total is only its base, ask the share. The problem is not that distinction. It is the additional general “shortage eases” clause, and the unchanged decline and closing instructions that do not carry the D654 exception.

**NOT SOUND: remove the general “shortage eases” extension, reconcile the decline and closing instructions with D654, and complete the whole-request cut review.**