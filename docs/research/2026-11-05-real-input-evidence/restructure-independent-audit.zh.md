# 组合请求独立复核

## 组合请求审计

**结论：我没有发现必须阻止这五篇文章的有限诊断的严重错误。** 但这份审计有两处表述不准确，不能把它当成“请求已完整符合标准”的证明；而且新请求的免费检查和固定请求指纹仍须先完成。

例如，模型可能写出一条季度收入指引，但如果没有把它关联到已有问题或同一次提出的有效问题，交接时仍会丢掉。新请求尝试改善这个过程，不能保证这条信息最终留下。

我核对了压缩文件里的五对实际请求：文件哈希与审计记录一致，五对均使用相同的输出格式；五篇中没有 T5 输入。结合标准、更正和直接交接代码，我认为需要区分以下几点。

- **审计对旧财务事实的描述不准确。** [审计第 12 行](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/restructure-combined-audit.md:12)说请求末尾明确把“重提的过去实际数字”列为可选；实际末尾没有这条明确例外，而是把重述的长期情况和背景归为杂音。标准则把重提的过去实际数字列为可选。[标准 §5.3](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/prd/05-extraction-standard.html:395) 这不是 D371 要求追踪当前及未来财务信息的直接反例，也未证明会影响这五篇诊断；但审计不应声称请求已经准确表达了该边界。

- **审计夸大了摘要保留原意的保证。** [审计第 17 行](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/restructure-combined-audit.md:17)说摘要保留条件和不确定性。实际请求明确要求保留谁、什么、数量和期间，也要求计划仍写成计划，并处理混合事实与传闻；但没有完整列出标准要求的所有条件，例如“最多”的上限或推算假设。[标准 §5.4](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/prd/05-extraction-standard.html:408) 输出格式只要求摘要是字符串，原文核对也不能证明摘要没有改变意思。[抽取代码](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/extraction.py:71) 因此诊断必须逐条对照原文检查条件、期间、来源和不确定性，不能只看引文是否通过。

- **公司市值的冲突已被承认。** 请求末尾排除市值，标准把在研公司的市值列为可选。[审计第 24 行](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/restructure-combined-audit.md:24) 正确指出了这点。它是请求与标准的真实差异，但可选项既不是 D369 的必留边界，也不是这次有限诊断必须先解决的问题。

**未测试的分支不等于已发现阻塞错误：**T5 演示材料、本人备忘录、财务问题加入已有研究组，以及价格或利率类问题，都没有在这五篇中得到有效验证。诊断结果不能推广到这些情况。历史问题快照也不证明每篇文章发表当天的完整状态；其中一篇的日期存在已记录的不一致，因此不能据此声称历史日终效果。[诊断设计](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/full-prompt-redesign-plan.md:35)

直接交接的限制在设计中已说清：候选问题引用证据，并不等于证据引用了候选问题；无有效关联的证据会被丢弃。代码也只按已记录的依赖关系去掉较宽的问题，不能保证所有关联在语义上正确。[交接代码](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/extraction.py:468) 因而结果应分别报告“没抽出、抽出但没关联、候选被检查拒绝、成功交接”，并人工检查关联是否合理。

**发送前仍有实际前置工作：**按现有设计固定新请求及输入指纹，并完成新版本自己的免费检查，包括有效关联、错误引文、错误关联和无关联被丢弃的检查。[诊断设计](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/full-prompt-redesign-plan.md:47) 上一版通过检查不能替代这些步骤。五篇各一轮只能提供诊断线索，不能证明总体改善、归因于某一句话，或作为上线验收。

本次只读审查，未修改文件，也未调用模型。

## 两条补充边界复核

**The two additions are sound, and the combined audit describes them correctly. The five-input diagnostic is not ready to run yet:** its frozen manifest still records older hashes for the draft, audit and request bundle.

For example, if an article repeats an identifiable old quarterly result, the draft now permits keeping or omitting it. If it says a project may deploy *up to* 40,000 units, the summary must retain both the limit and the uncertainty.

- **Past actuals:** [The draft](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/role-restructure-draft.txt:5) matches [§5.3](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/prd/05-extraction-standard.html:400): recognisable restatements of past actuals are optional, while still-valid guidance, forecasts and plans are judged on their merits. The original role did not state this exception, and the full [closing review](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/prompts/review-v74i.txt:1) did not explicitly state it either. The audit now says that accurately. D369 preserves the optional boundary; D371 addresses present and future information and does not make every number mandatory.
- **Preserving meaning:** [The added summary instruction](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/role-restructure-draft.txt:15) reflects [§5.4](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/prd/05-extraction-standard.html:408), including assumptions, limits and whether something is planned or has happened. It also supports §5.5’s requirement to describe an unconfirmed or planned secondary detail accurately. The audit correctly treats this as an instruction whose results still need human inspection, not a guarantee.
- **Decision boundaries:** [D369–D371](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/DECISIONS-log.md:3990) do not conflict with these additions. The audit also records that the five requests use the existing research context without adding a separate financial report or new preset questions.

The **run blocker is procedural, not a flaw I found in these two additions**. The current role, audit and request bundle hashes differ from [the frozen manifest](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/restructure-pilot-frozen.json:45); the [runner](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/run_restructure_pilot.py:40) refuses that mismatch. I verified that all five saved candidate requests contain the current role and both additions. The manifest and free checks must be refreshed for these exact files before sending. The diagnostic would remain a small combined test, not proof that either sentence independently works or that the product is ready for acceptance.

Read-only review; no files changed and no diagnostic sent.
