**Version 2 fixes the broad scope, the growth example, and the instruction to name measure and scope. The missing-date issue is only partly fixed.** The request now says to use the annual results release, but if the article gives no release date, it still gives the model no supported calendar date to put in the answer.

For example, an article may forecast next year’s revenue without saying when the company will publish it. “The release of that fiscal year’s results” identifies the event, but does not establish its date. The model could return an unspecific event, invent a date, or decline to open the question.

This is a **read-only assessment of the text**, not a measurement of model behavior. I ran diffs on the system and closing texts and compared the schemas as parsed JSON. The schema adds `main_driver` to the allowed reasons and changes “four” to “five”; there are no other parsed schema changes.

The deliberate restriction to revenue and gross margin is documented in [PROBE-DESIGN.md](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/main-numbers/PROBE-DESIGN.md) and authorized for this test by [D490](/Users/lchingen/hivemind/docs/DECISIONS-log.md:5571). It is narrower than the signed standard’s full row A, but that narrowing is **not a finding**.

### Version 1 findings

| Earlier point | Version 2 assessment |
|---|---|
| Scope extended beyond revenue and margin | **Resolved for the test.** The new opening words say “the company’s own annual revenue or gross margin”; the fuel-cost example is gone. The two remaining examples still need clearer scope, discussed below. |
| No date when the item gives none | **Partly addressed, still unresolved.** The date rule now names the results release. It does not supply a date or explain what to do when that release date is unknown. |
| Growth example could invite a duplicate | **Improved.** “Same-store sales growth” is now “same-store sales,” and the text says level and growth are one question when the same reported figure settles both. The wider comparison between two new questions can still be clearer. |
| Measure and scope were not explicitly requested | **Addressed in the instruction.** “Name the measure, its scope and the fiscal year” is now explicit. The examples do not show the full scope, and the request does not explicitly say the fiscal year must be supported by the item. |

Sources for the prior points and revision: [version 1 audit](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/main-numbers/audit-c20-blind.md), [candidate system](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c20-system.txt:87), and [candidate schema](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c20-schema.json:30).

### Each changed sentence

The standard references below are [§3 and §4](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:272). D382 says financial figures are conditions unless the reason itself is a view; D384 excluded row A from the adopted clean request. D490 opens this departure **as a test**, while those decisions remain in force for the adopted path. [D382 and D384](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4107)

| Changed text | Verdict | Source and assessment |
|---|---|---|
| “It opens for one of **five reasons**, a closed set” | **Consistent**, for this test. | §3: “开题理由是封闭的” and lists five categories. D490 permits testing the addition; it does not adopt it. |
| “`main_driver`: the company’s own annual revenue or gross margin, for its current or next fiscal year, whether or not the company guides it …” | **Keeps narrower**, deliberately. | Row A: “承载公司价值的那个年度量，不管公司指不指引” and “公司财年的今年或明年.” The standard also permits other main annual quantities; D490 limits this test. A possible ambiguity remains: “the revenue that carries the business” grammatically qualifies revenue more clearly than it qualifies gross margin, while row A requires the main value-carrying quantity. |
| “… the revenue that carries the business, in total or of its main segment, or the gross margin” | **Consistent**, subject to the separate-question test. | Row A names “撑起业务的分部收入、毛利率.” §4 says “一个新数字、一个更窄的范围，单凭这些不开.” A main segment is eligible, but its existence alone does not justify a second question beside total revenue. |
| “the bank’s net interest income this fiscal year”; “the retailer’s same-store sales next fiscal year” | **Consistent in substance**, but underspecified as complete questions. | Both measures appear in row A: “银行的净利息收入、零售商的同店销售.” Neither example states the reporting scope needed to distinguish, for example, total sales from a comparable-store measure. Whether each is treated as revenue within this narrower test can be made clearer. |
| “It is not every line of the statements.” | **Consistent.** | Row A: “不是每一行报表数.” |
| “Name the measure, its scope and the fiscal year” | **Consistent.** | §4: “算谁、不算谁、算什么写清楚” and “原文支持这个期间.” The sentence asks for the year but does not repeat that it must be supported. |
| “A level and its growth rate are one thesis when the same reported figure settles both.” | **Consistent.** | §4: “同一个结果能判掉两题，就是同一题.” The condition matters: a growth question also needs its comparison period and measure identified before one can establish what settles it. |
| “The material that publishes the figure, usually the annual report, settles it.” | **Consistent.** | Row A: “公布这个数的公开材料，通常是年报.” The actual material must publish the specified measure and scope. |
| When the item gives no date, use “a `main_driver` quantity, the release of that fiscal year’s results” | **No source for treating an unknown release event as an available calendar date.** The choice of release as the due date is **consistent**. | Row A says “到期日是这个数的发布日.” But §4 requires “有一个日期和一份公开材料” and requires the time basis in the source. Its explicit analyst-set dates are for an undated pending regulatory decision and an unsigned obligation. It does not grant an arbitrary date for an annual quantity. |
| Do not open “a quarter’s figures or guidance, or the level, growth, margin or guidance of a financial measure that is not a `main_driver` quantity, on its own” | **Consistent with the test’s exception, with an ambiguity affecting other reasons.** | §4 excludes “季度数字和季度指引” and every line of guidance; row A permits a qualifying annual main driver. “On its own” preserves other reasons in principle, but a reader could apply the financial-measure exclusion to a separately qualifying obligation or shared quantity. |
| Closing check: “five reasons” | **Consistent**, conditional on the fifth reason being applied correctly. | §3’s reasons are a closed set; the rest of the check still requires public material, a date and compliance with the exclusions. |
| Schema enum adds `main_driver`; description changes to “one of the five” | **Consistent.** | Row A uses `main_driver`; D490 opens the test. The schema can represent the new reason, but the enum does not enforce its measure, scope or date. |

### Other sentences in the request

- **Role paragraph:** No direct contradiction. It says new questions must be important, raised by the item and supported by evidence, and “Never open a thesis only to give a statement a home.” The new reason still sits under those conditions. A bare figure should not automatically become a question just because the new reason exists.

- **CONDITION:** No direct contradiction. “Inform an open thesis about its revenue or earnings path” describes where figures can link; the next sentence expressly recognizes “open or new” questions. A figure may support a newly proposed annual question. The wording could nevertheless pull toward linking only to an already open question if the model gives the first sentence too much weight.

- **“One quantity for one period, or one event”:** Compatible with annual revenue or gross margin. It does not itself tell the model whether two differently worded questions describe the same result.

- **Date rule:** The new fallback conflicts in practice with “Give the date the item supports” when the item does not give the results-release date. The instruction names *what date to use*, but does not make that date known. The schema’s `period` accepts a string or null and asks for the period **or** check date “with how it was set”; `settled_by` asks for material that settles the answer “on a date.” Neither supplies an actual date. [Schema](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c20-schema.json:38)

- **Another estimate, source or wording:** Compatible. A later forecast for the same question should be evidence for it. The new level-and-growth sentence improves this boundary, though it does not explicitly walk the total-versus-segment comparison.

- **“An annual quantity after next year”:** Compatible with current or next **fiscal** year. The model must use the company’s fiscal year rather than silently treating calendar years as fiscal years.

- **`closest_open_thesis` and `why_a_separate_bet`:** Compatible for comparison with an existing question: the model must explain how their answers can move apart. These fields do not ask for that comparison against another question proposed in the same answer. The closing check compares new questions for “the same underlying question,” but its explicit “cannot move apart” test mentions only an open question.

- **Closing check, figures and conditions:** The instruction not to drop a retold figure, guidance or forecast concerns keeping evidence; it does not make each figure a new question. The sentence that a missing date does not drop an **evidence item** is also compatible with requiring a date to open a **question**. The same-fact row combines a reported measure and its growth rates in one evidence item; the new level-and-growth sentence concerns questions. Finally, the extra usefulness check for the company’s figures applies to statements returned **without links**. A statement linked to a new question still faces the general evidence test, but no longer faces that particular unlinked-figure check.

- **Closing check, reasons:** “Five reasons” preserves all four existing reasons. There is no explicit instruction to replace or suppress them.

### Examples

The two added examples use generic bank and retailer descriptions. They name no covered company, product, or numerical value, and row A supports both measures. They are cross-industry examples, though the eligibility principle should still apply in any industry.

They fit the schema as **partial illustrations**, not complete valid questions: neither specifies the full scope, a public source that will publish that exact measure, or an actual settlement date. “Same-store sales” also describes a subset or comparable-store measure, so calling it simply the company’s revenue could blur the scope. The model needs to name that distinction when it matters.

### Specific risks and smallest sourced clarifications

**a. Every statement line, including EPS, net income, cash flow or a small segment.** The words most likely to cause over-opening are “the company’s own annual revenue or gross margin” if read as sufficient by itself, and “or the gross margin,” which is less clearly tied to the value-carrying test than revenue is. The surrounding “not every line,” position-impact and separate-bet tests oppose indiscriminate opening. EPS, net income and cash flow are outside the new reason as written; a small segment fails unless it is the qualifying main segment and separately significant.

A small clarification is: **“the revenue or gross margin that carries the company’s value”**, retaining “in total or of its main segment” where applicable. This carries row A’s own importance boundary to both measures.

**b. A quarter or a year after next fiscal year.** “Annual,” “current or next fiscal year,” the quarter exclusion and the later-year exclusion already oppose both. No new prohibition is needed. The remaining gap is source support: add **“Use a fiscal year supported by the item”**, reflecting §4’s “原文支持这个期间.” A quarterly statement may inform an annual question; it should not be converted into an unsupported annual forecast.

**c. Two questions for level and growth, or total and main segment.** The new “same reported figure” sentence addresses level and growth. The words “in total or of its main segment,” together with a comparison that explicitly asks whether answers move apart only against an **open** question, leave a risk of two unnecessary new questions. Total and segment must not be automatically merged: §4 says to judge whether their answers can move apart and matter independently on the actual material.

The smallest general clarification is: **“Compare new questions with each other as well: if the same result settles both, keep one; separate them only when their answers can move apart and an analyst would bet on them separately.”** This follows §4’s same-result and independent-meaning tests.

**d. Another company’s figures.** “The company” is defined as `current_entity`, and the new reason says “the company’s own,” so another company’s figure does not qualify under this reason. Other-party evidence can still inform research on the company. No extra rule is needed for this test. The signed standard separately discusses proposing another company’s own question, so this conclusion should not be generalized beyond the current request’s company scope.

**e. The other four reasons stop opening.** The five reasons remain alternatives, but “a quarter’s figures or guidance, or … a financial measure that is not a `main_driver` quantity” could be overread as blocking a quantity that independently qualifies as an obligation or a shared quantity. A minimal clarification is: **“This row does not exclude a matter that independently meets another opening reason.”** That preserves the existing reasons; it does not make a financial line sufficient by itself.

### What is still needed to write the question

- **Measure and scope:** Now requested explicitly. The answer must say what is counted—for example, total revenue or a named main segment, and the exact gross-margin measure. The illustrations do not demonstrate that full scope.
- **Fiscal year:** Requested explicitly, but the item must support the chosen year. The request should say so rather than invite a guess.
- **Settling material:** Present: the public material that publishes the specified figure, usually the annual report. The answer must identify material capable of resolving the actual measure and scope.
- **Date:** **Still missing when the source does not provide the release date.** The revision identifies the release as the relevant event, but neither the request nor the schema supplies its calendar date. The signed standard requires a date and does not give this category an analyst-set fallback. The text alone therefore cannot resolve this case without either a supported date from an available input or a separately decided way to handle its absence.