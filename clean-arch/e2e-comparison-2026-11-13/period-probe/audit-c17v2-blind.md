**Version 2 fixes the explicit year-on-year comparison problem, but I would not call the new sentence fully aligned with the standard.** It permits a 2027 price compared with 2026, yet its broad exclusions could still make the model overlook a valid calendar-year figure when that figure appears inside a rolling or multi-year statement.

For example, an article could give an average across several years **and** a separate figure for next calendar year. The words “an average or total over several years … is not this reason’s period” correctly reject the multi-year average as the question’s period, but do not tell the model to assess the separately stated annual figure on its own.

The diff changes only the shared-quantity sentence in [c17-system.txt](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c17-system.txt:102). The closing check and schema are identical to c8.

The changed sentence contains several distinct instructions:

| Changed wording | Verdict | Signed standard |
|---|---|---|
| “for **one calendar year, this year or next**” | **Consistent.** | “自然年的今年或明年” and “一个问题只问一个量的一个期间” in [§3](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:280). |
| “a figure over a **rolling twelve months … is not this reason’s period**” | **Consistent in its literal reading.** A rolling twelve-month period is not necessarily a calendar year. | The standard specifies “自然年的今年或明年” in [§3](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:280). It does not separately spell out rolling periods. |
| “an **average or total over several years** is not this reason’s period” | **Consistent for the multi-year measure itself**, but potentially narrower in application if read as excluding a separately stated calendar-year figure in the same statement. | “一个问题只问一个量的一个期间” and “不把几年的平均写成今年” in [§3–4](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:302). The latter explicitly names an average; the calendar-year rule also supports excluding a multi-year total as the period. |
| “while **a calendar year compared with the year before it is**” | **Consistent.** | The standard expressly gives “2027 年 DRAM 合约价相对 2026 年的变化” as an example in [§3](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:288). |
| “**whether a statement is kept is judged as evidence**” | **Consistent.** | “哪一类都不属于的不开；它是不是证据、挂到哪，照第 5 节和归档规则” in [§3](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:297). |

On the rest of the request, I see **no direct contradiction** with the four sentences named in the question. The new sentence governs whether a *new question* fits the shared-quantity period; the other sentences govern whether an existing question covers a statement and whether the statement should be kept and linked. The closing check reinforces that distinction by retaining material evidence even when no new question qualifies.

There is still an **ambiguity in application**. “Not this reason’s period” is attached to “a figure,” while “whether a statement is kept” comes immediately afterward. A model could apply the period exclusion to the whole statement rather than just the proposed question. That would conflict in practice with “Do not exclude evidence solely because it concerns a related period” and with the instruction to link evidence to every question it informs. This is a risk from the wording, not a demonstrated model failure.

The new examples are abstract period shapes, so they are **industry-neutral** and name no company, product, or numeric value. They agree with the schema: its question period and evidence period are strings, and its summary can preserve the comparison. The existing shared-quantity examples remain industry-specific illustrations—container capacity and a raw-material contract price—but do not name a covered company or product. The calendar-year comparison example agrees with the standard; the schema permits it, though it does not itself enforce the calendar-year rule.

For the three specific risks:

1. **Next year against this year:** The added “a calendar year compared with the year before it is” directly permits 2027 against 2026. It reduces the previous risk, but “for one calendar year” could still lead a model to rewrite the question as the 2027 price alone and lose the comparison. The request elsewhere says to preserve periods and comparisons, so this is an ambiguity rather than an explicit instruction to remove them.
2. **A calendar-year figure that should open:** Yes, potentially, when it appears alongside a rolling or multi-year figure. “A figure over a rolling twelve months” and “an average or total over several years” do not explicitly distinguish that measure from a separate eligible annual measure in the same passage.
3. **Evidence that is kept:** The sentence explicitly says to judge keeping separately, so it does not instruct the model to discard or reshape it. The risk is overextending “not this reason’s period” to the evidence itself, or dropping the comparison while summarizing it; the existing instructions to preserve the measure, period and comparison argue against that reading.

This is a read-only text audit. It identifies plausible readings of the request; it does not establish what the model actually does on a stored input.