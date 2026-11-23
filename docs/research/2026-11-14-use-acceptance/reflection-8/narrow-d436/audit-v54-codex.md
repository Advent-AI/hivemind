**NOT SOUND.** The passage carries Alex’s new rule in the right direction, but “whether that shortage eases” is wider than his ruling, and the two shorter reminders omit conditions needed to keep the share-centred case safe.

For example, a shortage can ease while supply remains below demand. Those are different outcomes, so asking about either one is broader than asking whether supply remains short.

## 1. Passage and reminders, clause by clause

| Sentence or clause | Verdict | Reason |
|---|---|---|
| “When the outcome tracks a figure and also names one of these second sides of the same bet … ask the figure, and list that second side in not_judged.” | **Consistent** | This follows [D654](</Users/lchingen/hivemind/docs/DECISIONS-log.md:9093>), [D436](</Users/lchingen/hivemind/docs/DECISIONS-log.md:4847>) and [D397](</Users/lchingen/hivemind/docs/DECISIONS-log.md:4326>). It makes the listed exception to the “several with none … main” decline case in [system line 6](</Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/audit-v54-inputs/edited-system.txt:6>). |
| “the share of the figure that one kind makes up” | **Consistent** | This is D654’s total-and-share shape, provided the outcome tracks the total. |
| “whether supply stays short of demand … beside a figure that measures that supply or its growth” | **Consistent, with a coverage uncertainty** | This matches the shipment-and-shortage shape. But “measures that supply or its growth” does not clearly include *new production capacity*, which is potential supply rather than necessarily supply delivered. That matters for `u3/clean-10`, a case included in D436’s underlying review. |
| “or whether that shortage eases” | **Wider** | D654 says whether supply **stays short**. Easing measures a change in the shortage; it can ease and still remain. “That” links it to the same shortage but does not make the two tests equivalent. The cited D436 case explains why the wording was considered, but D654’s stated general rule does not itself establish this wider form. |
| “whether capacity keeps pace with the demand that figure measures” | **Consistent** | D654 puts demand in the question and capacity in the background. |
| “In each example the first is the question” | **Consistent for the intended examples**, with one unclear example | It gives the orientations D654 requires. The port example’s “container volume” could mean actual throughput rather than demand; if so, the example does not clearly meet its own preceding clause. |
| “When the outcome tracks the share itself, with the total only as its base, the share is the question” | **Consistent** | This is D654’s explicit counter-case and follows D397. |
| Closing check: “the figure, when the outcome names it with one of its second sides” | **Wider** | It omits “tracks” and the share-itself exception. A share outcome also names a total as its base, and the total has that share as a second side. The reminder can therefore instruct the model to switch to the total, colliding with the passage’s final sentence. |
| `no_ladder`: “a figure named with one of its second sides, as the system text lists them, is one thing” | **Wider** | It likewise says “named,” not “tracked,” and does not carry the share exception. Its reference to the system text helps, but the sentence itself states a broader rule. It also does not override the other six decline reasons. |

The existing “Never fold two things into one ladder” sentence remains compatible if the new passage is read as the specific exception: the figure is judged and the other side is listed. System line 6 retains the general decline rule, which the passage explicitly qualifies. The two reminders need the same qualification.

## 2. Four targets

These are readings of the request, not model results.

| Target | Question and listed part | D436 result? |
|---|---|---|
| `acc/clean-8` | Ask **2027 global HBM shipment growth**; list whether HBM supply remains short of demand. | **Yes.** This is the explicit shipment-and-shortage shape. |
| `acc/clean-9` | Ask **2026 global semiconductor revenue**; list the AI-chip portion. | **Yes.** The amount of one kind is the part of the total. |
| `u3/clean-10` | Intended: ask **new HBM capacity added in 2027**; list whether it arrives early enough to ease the shortage, including the timing condition. | **D436 included this case**, but the edited wording does not securely reach it: added capacity is not necessarily a measure of actual supply or supply growth. The easing phrase also goes wider than D654 as explained above. |
| `pool-17` | Ask **2026 total China AI-accelerator shipments**; list the GPU/non-GPU composition. | **Yes**, as total and composition. |

The main passage’s phrase “outcome tracks a figure” does not require the outcome to explicitly label that figure “main”; D654 supplies the choice for these shapes.

## 3. Six decline controls

The two entangled topics are excluded as requested.

| Control | Reading under the edited request |
|---|---|
| `week-10-06:c1/clean-4` | **Decline:** two separate annual capex figures, with neither chosen as main. The exception does not pick a year. |
| `week-10-06:c1/clean-12` | **Decline:** separate annual spending figures, with no selected main year. The GDP percentages do not make the two annual amounts one of the listed shapes. |
| `fortnight:c1/clean-8` | **Decline:** global robotics venture funding is not clearly covered by any of the supplied themes. “AI capital spending” does not by itself establish that venture funding belongs to that theme. The prior-year and half-year figures are comparisons, so “several with none main” would not be the reason. |
| `pool-19` | **Decline:** the legislation concerns AI development and a new government department; none of the supplied themes clearly covers that matter. A pending regulatory decision can have a fiscal-year-end date under D403, but that does not cure the missing theme. |
| `u1/clean-9` | **Decline:** the tracked share covers a rolling twelve months, and no publication day is given. [D417](</Users/lchingen/hivemind/docs/DECISIONS-log.md:4606>) confirms this refusal. The share rule does not remove it. |
| `u2/clean-10` | **Decline remains justified:** the outcome names whether capacity comes online and whether record prices persist, without selecting one as main. Prices are not one of the listed second sides. The description’s “how much capacity” does not authorize choosing it over the outcome under D631/D635. |

The theme judgments for robotics funding and the AI bill depend on the provided theme names; they are not claims that those topics are unimportant. No supplied theme specifically names either matter.

## 4. D631’s six boundary cases

None clearly matches the passage’s three listed relationships, so the edit does **not** decide which part to ask in any of them:

- **Optical-switch shipments:** multiple shipment checkpoints, not total and share or one of the supply/demand shapes.
- **Chip sales into China:** two authorities’ decisions, not a listed figure-and-side shape.
- **Acquisition:** agreement, completion and terms; the edit does not choose among them.
- **Investment commitments:** remaining balance, cash paid and changes in commitments; none is described as a kind’s share of the tracked total.
- **Memory prices:** price change, selling prices and margins; not a listed shape.
- **Chip export licence:** licence status and revenue resumption; not a listed shape.

The separate existing rules may affect whether a topic can ultimately be asked. The point here is that this passage supplies no new choice among those parts.

## 5. Examples

- I compared the examples with the descriptions and outcomes of all **44** topics in [cases.json](</Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/cases.json>). None copies a test topic or uses its company, product or numbers. They deliberately **mirror the general relationships** in test topics—total and part, shipments and shortage, demand and capacity—but replace their industries and particulars.
- The **rules** can apply across banks, drug makers, retailers and chip makers. The examples use different industries and teach the same relationships. The port example needs clearer wording because actual container volume is not necessarily the demand that berths must meet.
- The examples put the total, supply figure or demand first, consistent with D436’s orientation. The bank and carmaker counterexamples correctly put the **share itself** first when that is what is tracked. The port’s ambiguity prevents a clean conclusion that its first figure is demand.

## 6. Growth

The stated reason is **sufficient as a reason for growth** under the cited instructions: D654 adds behavior absent from the frozen request, the classes have two examples each, and `cut_review` considers the request’s other parts. The [council-loop instruction](</Users/lchingen/hivemind/.claude/skills/council-loop/SKILL.md:158>) explicitly permits growth with a written reason when forced cuts could independently change behavior.

That does not establish that every retained sentence is indispensable. For example, the review itself says the “exactly one” shape is also enforced by code; it gives a reason to retain the sentence for the model, rather than demonstrating that it cannot be shortened. I would not make an untested cut merely to eliminate growth. The recorded system-text change is **9,545 to 10,839 characters**, and the stated token count is **2,031 to 2,302**.

## 7. Share-centred counterexample

For `u3/clean-11`, the **main passage** supports asking the custom-ASIC share rather than total spending. But the closing reminder says “the figure” whenever the outcome names a figure with a second side, without repeating the share exception. Thus the complete edited request does **not reliably protect** against switching to total spending.

There is a further limit: the outcome also names a split of incremental compute capacity. D654 settles that a tracked share must not become its total; it does not itself choose between the spending split and the capacity split if both are tracked without a main one. That choice remains unresolved.

## 8. Same-bet trigger

The main sentence ties the exception to a figure the outcome **tracks**, and each listed side is described as a relationship to that figure. Two unrelated things merely mentioned together should therefore not trigger it. The share counter-case is consistent with the main sentence: when the share is tracked, the total is its base rather than the tracked figure.

The problem is that the **closing and schema reminders weaken “tracks” to “names”** and omit the counter-case. They can therefore pull the answer away from the main sentence, especially when the share and its total are both named.

NOT SOUND: Remove “or whether that shortage eases,” clarify that the capacity target’s qualifying figure can be added capacity if supported by D654’s scope, make the port example explicitly demand, and qualify both reminders with “outcome tracks” and the share-itself exception.