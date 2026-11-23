**NOT SOUND.** The passage correctly points toward judging shipments, the total, or demand in the examples Alex named. But it turns a resemblance in wording into an automatic decision about which figure is the main question. For example, it can treat any figure mentioned beside a supply shortage as the main figure, even when the outcome does not establish that relationship.

This is a read-only assessment of what the text instructs; it is not a model test. The inserted passage is in [edited-system.txt](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/edited-system.txt:5).

### 1. Clause by clause

| Passage | Finding |
|---|---|
| “When the outcome names a figure together with the share of it that one kind makes up” | **Keeps wider.** D436 identifies the AI-chip share beside the chip total as two sides of one bet. This sentence makes *every* total-and-share pairing one bet and selects the total, without first establishing that it is the same bet. D397 says to judge the main part named by the outcome; D631 and D635 do not establish a general way to choose between several parts. |
| “or with whether supply stays short of demand or capacity keeps pace with it” | **Keeps wider.** D436 names shortage beside shipments and capacity keeping pace beside demand. The passage attaches either condition to an unspecified “figure.” The grammar does not require that the figure be shipments or demand, or even that it be the quantity to which the condition relates. |
| “the two are one bet seen from two sides, not several things with none the main one” | **Keeps wider and conflicts with the refusal rule.** D436 describes an identified bet; this sentence declares the named shapes to be one bet. It overrides [system line 6](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/edited-system.txt:6) and the schema’s `no_ladder` description where the outcome genuinely has several parts and no main one. |
| “ask the figure” | **Keeps wider.** It selects the figure even when the outcome does not establish that it is the tracked part. That can conflict with “Judge the one the topic’s outcome names as what is tracked” and with the closing check’s “the one the topic’s outcome names.” It also does not distinguish demand from capacity when the latter is the figure. |
| “list the share or the shortage in not_judged” | **Consistent but incomplete.** Showing the other side as not judged agrees with D436 and D397. The sentence does not explicitly name capacity keeping pace as something to list, although the preceding general instruction and the closing check require every omitted part to be listed. D436 also says the second side stays as context; the insertion only says to list it. |
| Bank, retailer and utility examples | **The stated orientations match the three D436 examples**, but the examples repeat the broad automatic selection above. The utility example correctly asks demand and leaves capacity as the other side. |

The `no_ladder` description and closing check remain unchanged, so the request now has competing instructions in cases where a surface match does not establish a main part. Other refusal grounds, such as an unavailable publication date, remain in force; the added sentence does not expressly cancel them.

### 2. The four targets

These are the likely readings of the edited text, not guaranteed outputs.

| Target | Likely question and omitted part | D436 |
|---|---|---|
| **acc/clean-8** | Ask 2027 HBM shipment growth; list whether supply remains short of demand. | Yes: shipments and shortage are Alex’s example. |
| **acc/clean-9** | Ask 2026 total semiconductor revenue; list the AI-chip portion. | Yes: total and AI-chip share are Alex’s example. The outcome gives an amount rather than a percentage, but it is still a portion of the total. |
| **u3/clean-10** | A model may ask how much capacity is added in 2027 and list whether it arrives early enough to ease shortage. But the trigger says “supply stays short of demand,” while this outcome speaks of arrival timing and easing a shortage. A careful literal reading does not clearly trigger it. | **Not established by the stated examples.** D436’s capacity example asks demand and leaves whether capacity keeps pace as context; it does not decide that capacity additions are the main figure here. |
| **pool-17** | Ask total 2026 accelerator shipments in China; list the GPU/non-GPU composition. | Consistent with D436’s total-and-share example, assuming the composition is the second side of that same bet. |

### 3. The eight decline controls

| Control | Effect of the edit | Is a decline justified? |
|---|---|---|
| **week-10-06:c1/clean-4** | Does not match the new passage. Two years remain. | The edit leaves the existing no-main refusal available; the decisions cited do not select a year. |
| **week-10-06:c1/clean-12** | Does not clearly match: the GDP percentage is a reference alongside spending in two years, not a share of the spending total made up by one kind. | No-main refusal remains available. |
| **fortnight:c1/clean-8** | Does not match: 2025 and first-half 2026 are comparisons with the explicitly tracked full-year 2026 funding figure. | **No.** The outcome identifies one annual figure. The prior comparisons should be listed; this is a wrong decline control on the supplied text. |
| **pool-9** | Does not clearly match the share trigger: memory’s share of rack cost is in the description, but the outcome names price changes and per-rack cost. | A no-main decline remains available; the edit does not resolve which of those outcomes is main. |
| **pool-19** | Does not match: it asks whether one bill or equivalent measure is enacted, with provisions describing that measure. | **No, on the supplied wording.** The tracked event is enactment; the provisions do not by themselves make it several unrelated main events. A themed object must still be available. |
| **u1/clean-5** | The share appears in the description, not as the outcome’s “figure together with the share.” A loose reading might nevertheless apply the new sentence. | The outcome names multiple price series, years and rack cost; a no-main decline remains available. The description’s 25–30% is not a sound reason to select rack cost. |
| **u1/clean-9** | The outcome names a share and its implied remainder, but not a total figure paired with a share. | **Yes:** the rolling 12-month figure has no stated publication day, so D417 independently requires decline. |
| **u2/clean-10** | A model could stretch “supply stays short” to the shortage and select capacity, despite the outcome also tracking persistent prices. The wording does not expressly say supply is short of demand. | A no-main decline remains available. Applying the new sentence automatically here would be an unsupported selection. |

For the cases marked “available,” the supplied decisions do not themselves settle every disputed main-part judgment. That is different from proving a particular refusal is mandatory.

### 4. D631’s six boundary cases

None is an explicit match for the new passage, so **none is clearly decided by it on a literal reading**:

| Case | Why the insertion does not decide it |
|---|---|
| Optical-switch shipments | Shipment checkpoints across periods, with no share or supply/demand condition. |
| Chip sales into China | Two authorities’ decisions, not a figure and share or shortage. |
| Acquisition | Agreement, closing, consideration and conditions; no matching shape. |
| Investment commitments | Balance, cash funded and changed commitments; none is stated as a share of the total. |
| Memory prices | Price changes, average selling prices and margins; no matching shape. |
| Chip export licence | Licence status and revenue resumption; no matching shape. |

The concern remains that the passage decides **other** multi-part outcomes by surface shape. These six do not demonstrate that particular failure.

### 5. Examples

The insertion contains **three explicit examples**, not four. The general sentence also describes three shapes but is a rule, not a fourth worked example.

- **Bank lending and commercial share:** mirrors the total-and-component structure of **acc/clean-9**. It does not use its company, product or numbers.
- **Retail sales and shelves running short:** mirrors the shipments-and-shortage structure of **acc/clean-8**, though sales and shelf availability are not necessarily the same bet merely because they appear together.
- **Utility demand and capacity keeping pace:** closely mirrors **acc/clean-10**, which asks NAND demand and whether capacity additions keep pace. Its orientation agrees with D436: demand is judged and capacity is the side.

Thus, the examples are from other industries and do not copy the test articles’ names or figures, but they **mirror test-topic structures**, especially the utility example. The wording does not read identically across industries: lending, shelves and generating capacity are industry-specific illustrations. Their relationships can be translated across industries, but the reader still has to decide whether each pair represents one bet; the passage currently assumes it does.

The examples provide one illustration for each of three shapes, not two or three per class as AGENTS §6 requests for a classification. More examples alone would not fix the unsupported selection rule.

### 6. Growth

The edit adds **610 characters** and removes none, according to [edit.json](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-8/narrow-d436/edit.json:15). The reason identifies a potentially missing decision, but it does **not** establish that the required whole-request audit found no material to cut or merge. Nor does it report prompt tokens before and after. Saying no existing sentence covers precisely the same case is not, by itself, enough to satisfy §6’s requirement to remove at least as much elsewhere or give a supported reason for growth.

NOT SOUND: Replace the automatic shape-based selection with D436’s identified same-bet rule and its stated orientations, without deciding other multi-part outcomes; use non-test-derived examples and complete the required growth audit.