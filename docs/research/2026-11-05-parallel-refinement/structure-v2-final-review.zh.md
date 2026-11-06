**没有发现这次修订新引入的严重问题。** 十份实际请求中的改动与设计一致；但它们还没有证明模型会正确处理这些情况。

例如，第二篇文章同时包含季度 **non-GAAP 毛利率指引**和已有的 **GAAP 全年毛利率问题**。新版 B 明确允许两者有合理联系时作为间接信息，同时说它们不是同一个数字。[新版 B]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/structure-v2-existing-evidence.txt:11)、[实际请求]( /Users/lchingen/hivemind-no-preseed-evidence-review/poc/data/parallel-structure-v2-2026-11-05-v3/manifest.json)

- **A 的遗漏已补回。** 实际 A1 请求问：“If other questions' answers stayed the same, could this outcome change independently and alter the business judgment?” 这对应签署标准要求的其他答案不变、只有新答案变化时业务判断是否不同。[新版 A]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/structure-v2-new-thesis.txt:9)、[标准 §4]( /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:316)

- **新增例子符合范围。** 零售商的销售与利润、药物试验与获批都以“各自有独立意义”为条件，没有要求遇到类似情形就自动开题。药物节点的区分也有标准依据；例子没有沿用已看文章里的担保结构。[新版 A]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/structure-v2-new-thesis.txt:11)、[标准 §3–4]( /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:277)

- **口径标签的实际范围与说明一致。** 第一篇的 B1/B2 只给 `v6` 加了 GAAP；第二篇只给 `v6`、`v10` 加了 GAAP，均与保存的问题字段一致。两篇没有实际的 non-GAAP 标签案例，因此不能据此声称已验证非 GAAP 或未知口径的表现。A 和 B0 没有新增标签。[问题快照]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/source-only-inputs.json)、[设计说明]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/structure-v2-design.zh.md:18)

- **实际请求和格式核对通过。** 两篇各有 A0/A1/B0/B1/B2；每篇 A1 相对 A0 只改系统文字，B1 相对 B0 只加上述标签，B2 相对 B1 只改系统文字。文章、问题 ID、证据及候选问题所需字段均存在；未发现新文字与用户部分或输出格式新增矛盾。新版 B 要求识别各事项，但没有同时要求相同引文必须拆开、又要求它们必须合并。

**仍需单独报告的原有限制：**

- 相同引文的两条不同事项仍可能在交接时被合并，只保留第一条摘要；这不是新版 B 新引入的义务，也不能说新版已修复。[交接代码]( /Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/extraction.py:682)
- A 只返回新问题的证据，B 只处理已有问题；没有合适问题的信息仍可能丢失。A 输入有时只给预计月份，却要求完整日期，也仍是已有局限。[设计说明]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/structure-v2-design.zh.md:12)
- A 提前比较已有问题符合这次两路分工，但若它误判为已有问题而不提出候选，下游就无法纠正；这是已有架构风险，不是本次补回独立判断造成的新问题。[已有审查]( /Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/structure-v2-design-review.zh.md:10)

本次为只读审查，没有修改文件、调用产品模型或改动金标。