**The change has one material problem: its new period restriction can be read as excluding a year-on-year comparison that the signed standard explicitly permits.** It correctly separates the decision to open a question from the decision to keep a statement, but “a span that is not one calendar year” is ambiguous when a question asks how a price in 2027 compares with 2026.

The diff shows one changed sentence in [c17-system.txt](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c17-system.txt:102). The closing check is unchanged.

| Changed wording | Verdict | Standard |
|---|---|---|
| “for one calendar year, this year or next” | **Consistent**, if it means the year whose outcome is being judged, while allowing a comparison with an earlier year. | §3 says “自然年的今年或明年” and “一个问题只问一个量的一个期间.” It also explicitly gives “2027 年 DRAM 合约价相对 2026 年的变化” as an example. |
| “a figure over a rolling twelve months … is not this reason’s period” | **Consistent** as a restriction on opening a question for a rolling period itself. | §3 specifies “自然年的今年或明年”; §4 says “原文支持这个期间，不把几年的平均写成今年.” Neither says to convert a rolling figure into a calendar-year figure. |
| “a span that is not one calendar year is not this reason’s period” | **Contradicts, if read as rejecting a comparison because it references two years; otherwise ambiguous.** The text does not distinguish the target year from the comparison year. | The explicit §3 example is “2027 年 DRAM 合约价相对 2026 年的变化.” It judges a 2027 outcome using 2026 as the comparison. |
| “whether its statement is kept is judged as evidence” | **Consistent.** It does not say that failing the period test makes the statement disappear. | §3 says “哪一类都不属于的不开；它是不是证据、挂到哪，照第 5 节和归档规则.” |

The standard also says “同一个量、同一年只有一个问题” and calls the next period of the same quantity a “续期.” That does not make every later-period statement automatically unrelated to an existing question: §4 separately says another population or proxy of the same aggregate can be evidence for it. The standard places comparisons with the existing library in the later matching step.

**Other sentences in the request:** I found no direct contradiction if the new parenthesis is applied only to the period of a *new question*. It can coexist with “Another population or wording of the same aggregate is evidence for it,” “another estimate, source or wording of what an open thesis tracks,” and “Do not exclude evidence solely because it concerns a related period.” Those sentences govern whether a statement informs a question, not whether its own period qualifies for a new question.

There is still a practical tension: the parenthesis says a non-calendar-year figure is “not this reason’s period,” immediately next to the opening rule, without explicitly saying that such a figure may inform a calendar-year question. The existing instruction to assess related periods and preserve their differences supplies that protection, but a model could overextend the new restriction. Likewise, “If the two cannot move apart, link the evidence” remains a separate test of whether two questions deserve separate tracking; the new sentence does not itself establish that their answers can or cannot move apart.

**Examples and schema:** The changed sentence introduces no new named company, product, or numerical example. The two existing examples are generic across industries and fit the standard’s shared-quantity category. The first does contain the calendar year **2026**, so it does not literally contain no number; it is a period label, not a covered company’s reported figure. The second, “next year’s average contract price of a raw material,” fits the one-calendar-year rule. Neither example tests the standard’s allowed comparison against the prior year.

The [schema](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c17-schema.json:25) can express a comparison in the question and outcome, a target period, and the statement’s own evidence period and links. I found no schema conflict with either existing example. Its free-text fields do not themselves prevent a model from losing the comparison or assigning the wrong period.

**Risks in the requested cases:**

- **2027 price versus 2026:** Yes, the model could drop the question or reshape it into the 2027 price alone. The risky words are **“one calendar year”** combined with **“a span that is not one calendar year.”** A comparison mentions two years, even though the outcome being judged is the change for 2027. Removing the 2026 reference would change what the question asks. This is a reading risk, not an observed model result.
- **A calendar-year figure that should open:** Yes, if the source also mentions a rolling period or the prior-year baseline, the model might classify the whole statement as “a span that is not one calendar year” and reject the supported calendar-year question. The wording does not explicitly direct it to distinguish the target figure from its context.
- **A statement kept as evidence:** The new sentence explicitly says to judge whether it is kept as evidence, so it does **not** instruct the model to drop it. But the same period wording could still cause the model to leave relevant evidence unlinked or reshape its period. That would conflict with the existing instructions to assess related periods, preserve the difference, and retain the statement’s figures and conditions.

This is a text audit; no model calls or behavioral measurement were performed.

