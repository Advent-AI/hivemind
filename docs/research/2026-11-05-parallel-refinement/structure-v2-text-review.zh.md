结论：**新版 B 的改动基本符合标准；新版 A 有一处重要的标准遗漏，需要补回，再进行实验。** 现有交接代码还有已知的同引文合并问题；这不是新版提示词引入的，但会影响实验结果的解释。

例如，文章同一句给出总收入和数据中心收入时，模型可以分别写两条；现有代码仍会把它们合成一条，只留下第一条摘要。即使新版 B 更准确地识别了两件事，交接后也不一定都保住。

1. **新版 A 弱化了“是否值得单独追踪”的判断。** 旧版明确问新问题的答案能否“独立于其他问题变化，而且这种变化有意义”；新版改为问两个答案是否“可能以有意义的方式不同”。后者能帮助比较是否为同一个结果，但没有明确要求：**其他问题答案不变时，新问题单独变化是否会改变业务判断**。这是冻结标准第 4 节的独立意义测试。新版仍有“独立问题”等概括文字，但没有把这个被删掉的具体判断补回来。

   建议保留用户要求的**先比较已有题库**，同时补回这一测试；不需要改成不看题库。依据：[新版 A]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/structure-v2-new-thesis.txt:9)、[旧版 A]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/restructured-new-thesis-draft.txt:9)、[冻结标准 §4]( /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:313)。

2. **新增例子没有要求遇到相似情况就必须开题，但担保例子需要防止样本拟合。** 药物试验结果和获批的例子要求各自有独立意义；保险担保例子也写了金额问题要通过开题和核对测试。它们没有写成自动开题，且相关区分在[冻结标准]( /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:343)中有依据。

   但保险例子中的“是否承担担保”与“已承担计划的金额”，正好复刻了此次已看过文章漏题的比较结构，只换了行业；设计文档也明确说它对应这次漏题。不能声称它来自未见过的案例，也不能把这两篇上的改善当作泛化证据。[失败记录]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/trace-structure-review.zh.md:5)、[设计]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/structure-v2-design.zh.md:9)。

3. **新版 B 允许合理的间接证据，也保留了现行指引和缺失日期的边界。** 它明确说不同会计口径不是同一个数字，但有清楚联系时仍可帮助判断；季度实际值或预测也可以帮助判断全年。这符合 [D369 和 D371]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/DECISIONS-log.md:3990)。例如，非 GAAP 季度毛利率指引不能冒充 GAAP 全年毛利率，但也不能仅因口径不同就一律排除。

   两版都删除了开头一处较详细的来源、期间、条件和不确定性说明，但这些要求仍在具体写法和实际请求的检查中；仍有效的指引和预测也被保留。原始日期未知时，实际字段说明仍要求留空。此前确实出现过把报道日误填为原始发言日的回答，所以这是**已有的模型执行问题**，不能说新版已经解决。[新版 B]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/structure-v2-existing-evidence.txt:9)、[实际请求]( /Users/lchingen/hivemind-no-preseed-evidence-review/poc/data/parallel-restructure-small-2026-11-05-v1/manifest.json)、[已存 trace]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/trace-structure-review.zh.md:37)。

4. **同一句中的不同事项：格式能表达，现有交接不能保证保住。** B 的格式允许两条证据分别写摘要、来源和链接，也允许它们引用相同原文。实际旧回答中，两条分别记录总收入与数据中心收入，但 [现有代码]( /Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/extraction.py:682)按相同引文合并，保留第一条摘要、合并链接。第二个数字仍可能出现在引文里；其后续判断影响没有实测。

   新版 B 要先识别每个事项，但**没有新写一句强制同引文拆成两条**。因此，不能说某条新指令本身必然被代码拒绝；能明确说的是：即使模型按要求识别出两个事项，现有代码仍可能合并它们。这个限制属于旧代码，不是新引入的问题。[真实案例]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/trace-structure-review.zh.md:29)。

5. **会计口径设计的方向正确，但目前是待验证的输入改动。** 设计规定只复制题库中已知的 GAAP 或 non-GAAP；未知和 `n/a` 不加标签。这不会凭空给问题指定口径。A 暂时不加标签，B 的实验版本会加，因此两路看到的文字不同，应按设计如实报告。当前审查的保存请求是旧输入；我没有看到已生成的新请求，不能宣称标签已经正确送达模型。[设计]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/structure-v2-design.zh.md:17)。

另外，A 和 B 的格式及旧请求仍有两项已知限制：A 只返回新候选的证据，B 只找已有问题的证据，所以没有合适问题的信息仍可能被丢弃；A 的年度问题必须输出完整日期，而保存的输入有时只给预计月份。它们都不是本次新改文字造成的，也不能靠这次改写声称已解决。[已有审查]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/structure-v2-design-review.zh.md:20)。

本次只读对照了提示词、保存请求、标准、决策和相关代码；**没有修改文件，也没有调用产品模型**。建议先补回 A 的独立意义测试，再用原文、原始回答和交接结果逐条检查两篇实验。