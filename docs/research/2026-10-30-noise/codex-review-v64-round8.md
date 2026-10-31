**Round 8 still has one serious contradiction:** the instruction to keep a conditional valuation is broad enough to conflict with the instruction to reject an unrelated company’s valuation. For example, a dated valuation of an unrelated business could satisfy both lines.

This is a reading of the prompt, not a measured model failure.

**Findings, ranked by seriousness**

1. **Serious — the conditional-valuation instruction can keep something the standard rejects.**  
   [The revised prompt](</Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/review-v64.txt:6>) says “**a conditional valuation with its assumptions, derivation and date is kept**.” Its next rejection also says “**another company's valuation, share price or deal that touches none of the company's markets**” is not kept.

   The [standard §5.3](</Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:383>) says “**有假设、有推导、有时点的条件估值要留**,” but also says “**和公司所有市场都无关的别家公司的估值、股价、交易**” are not kept. The revised positive sentence has no stated limit when those two cases overlap. The same overlap can apply to an irrelevant conditional valuation under §5.1’s relevance test.

2. **Reading risk — the background row can conflict with the protection for a plan still in force.**  
   The opening says “**a forecast or a plan still in force, keep their place even when retold**.” But the rejection list says “**an arrangement already in place, described again**” is not kept; that row’s stated exception covers only a development whose age is unclear. An ongoing backstop plan, for example, could be read as both an arrangement already in place and a plan still in force.

   The [standard §5.3](</Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:387>) says “**重提的季度指引和仍然有效的预测、计划按本来分量**.” The opening reflects that rule; the later, unconditional row makes its application less clear.

3. **Lower-severity wording risk — the header is understandable, but its reach is easy to misread.**  
   “**These are not kept. A line that says what it does not cover leaves that to the check**” is more direct than the former double negative. Read together with the bullets, it means that a named boundary is judged by the opening test, rather than automatically discarded or automatically kept. A reader could nevertheless take “These are not kept” to cover every phrase in the bullets, or assume that only exceptions introduced by “it does not cover” count. The conditional valuation is instead stated as a positive keep, while the in-force-plan protection appears before the list.

   The standard’s distinction is: “**写着‘不能用这一行删掉’或‘要留’的……按下面两步定分量；写着可选的归可选；其余不收**” (§6). The prompt also says all share-price moves are rejected, while the standard makes the **post-earnings reaction optional**. Dropping that optional item is allowed; the wording simply does not describe its optional status.

**The revised lines against their sources**

| Revision | Comparison |
|---|---|
| “**These are not kept**” | Correctly strengthens “usually fail” for items within a §5.3 reject row, subject to its boundaries and optional cases. The overlap above remains. |
| “**the launch, shipment, delay or cancellation of the product that carries the company's value or a change to its plan or configuration**” | Removes the unsupported sales-scale condition. §6 names “**关键产品进度**” and “**它承载价值的那一代产品及其配置、过渡方案**.” The listed events are left to the overall check, not made automatic keeps. |
| “**it does not cover …**” and “**leaves that to the check**” | The intended procedure matches §5.3 boundaries such as “**不能用这一行删掉，按 5.1 判**.” It is clearer than the double negative, with the reading risk in finding 3. |
| “**a conditional valuation with its assumptions, derivation and date is kept**” | Adds the missing “conditional” and matches the positive wording of §5.3 for the intended case. Its unqualified scope creates finding 1. |

I found no additional contradiction in the revised treatment of core evidence, guidance, policy steps, competitor comparisons, partner or customer adoption, other companies’ actions and operating figures, or the news behind a price move. Those boundaries are left to the overall test; a missing amount, date or scale is not a reason by itself to drop them.

Round 7’s list-only recall issue and “keep the fuller one” remain recorded as open and were not reassessed here. No files were changed and no model call was made.