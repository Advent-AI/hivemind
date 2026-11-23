**我支持把 D186 的方向和代码排序纳入候选设计，但 v3 还不能送测：它可能稳定地回答错问题，也可能稳定地给出错误方向。** 下一步先完成第二位读者的盲读和仲裁，再修订问题、主题对象与测试规则；构建和付费调用仍须 Alex 授权。

一个具体例子：采购承诺从 $50bn 增至 $119bn，可能意味着供应更有保障，也可能意味着风险更大。强制模型选“越高越好”或“越低越好”，再由代码一致地排序，并不能证明这个判断对。([案例及首位读者](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/census/packet.md:233), [盲读记录](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/census/reader-codex.jsonl:7))

**(a) 风险与原因。** 区间和方向不稳定是明确的产品风险，因为首次写入后区间固定；但目前不能证明它是所有风险中“最大”的，也不能断言冻结提示句本身是原因。检查仅拒绝 1/36，并不衡量区间是否合理。([统计](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/census/production_ladders.txt:1), [D38](/Users/lchingen/hivemind/docs/DECISIONS-log.md:760))

我核对了存档请求：d1 call 13、d3 call 12、d4 call 12 的完整请求哈希相同，然而中间区间分别是 $5–10bn、$2–3bn、$1–5bn；前两次有利端在低处，第三次在高处。因此，**至少这三次的差异不能用文章参照不同解释**。其他调用的请求不同，文章、上下文和模型采样都可能影响结果，需逐项追踪。你说的 12 次包括 10 个完全相同的问题文字和两个不同措辞；脚本按前 60 个字符分成两组，不能仅凭分组代码证明 12 个语义相同。([输出](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/census/production_ladders.txt:10), [分组方式](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/census/production_ladders.py:46))

**(b) 一个视图和未回答部分。** 只展示新问题会减少“答案声称覆盖原问题”的误导，但还必须让读者在同一处看到原问题和未判断的部分；否则丢失的内容仍被藏起来。D38 对能独立变化的部分规定不同视图；它并未授权一律只选一个。([D38](/Users/lchingen/hivemind/docs/DECISIONS-log.md:761))

Ohio 的签约问题已有 D388 的明确依据；但 u1 clean-8 的 `outcome` 同时列收入或出货量，这两个量可不同方向变化。仅显示收入答案会让出货量从研究记录中消失。至于本版本是建立多个视图，还是明确报告暂时只处理一部分而留下未回答内容，是产品选择，不能由“避免重复开题”单独决定。([案例](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/census/packet.md:271), [D388](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4172))

**(c) 字段和检查。**

- 保留 `question`、截止日、区间、对象、参照及其来源；`settles` 若只重复 `question` 可删。保留未判断内容，但必须真正展示给读者。`ladder_type` 若能从明确的返回形状确定，就不必再让模型重复决定。
- `favourable_end` 需要允许“无法确定”，否则 6/6 被首位读者认为方向不明的公司数字题会被迫给出方向；该数字仍是**一位读者的结果**，尚待仲裁。([盲读统计方式](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/census/tally.py:24))
- **“文章中的任何数字都必须落在中间区间”没有得到 v74i 或 D186 的支持。** 文章里的历史数字未必是市场预期；`$119bn` 落在 `$100–119bn` 的**开区间之外**，机械套用还会触发边界问题。([生产区间](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/census/production_ladders.txt:14), [区间规则](/Users/lchingen/hivemind/src/hivemind/prompts/role-v74i.txt:31))
- 精确引用只能证明文字出现，不能证明它是恰当参照。日期必须晚于文章日也需先明确对已到期或当天事件的处理依据。18 个月规则有 D185 来源，但对已承担义务与未签事件的适用应按决定逐项核对。([D185](/Users/lchingen/hivemind/docs/DECISIONS-log.md:2472))
- `v<N>` 和 `e<N>` 确有必要匹配现有判断器，但必须保存 **每次运行内稳定、无碰撞的双向映射**；简单替换 `clean-4` 不足以处理现有视图或不同运行。([判断器](/Users/lchingen/hivemind/src/hivemind/views/judging.py:182))

**(d) 对照和通过线。** v74i 原文是可用的**对照候选**，但必须固定并披露其完整请求、输入和输出格式；原生产调用还有类别、对象、开放问题及 schema，单独摘句不等于完整生产路径。([请求构造](/Users/lchingen/hivemind/src/hivemind/extraction.py:377))

三条线都能计算，却尚不公平：

1. **26/31** 依赖尚未仲裁的“三条不可单独判断”，且没有解释为什么允许五条失败。
2. “任何类别不比对照差”需要预先定义类别和分母；只盲读每组一次，无法证明其余两次的质量。
3. **方向 3/3 一致不等于正确**；强制二选一还可能让三次都错。应分别报告一致性、读者是否认为方向有依据、以及无法确定。

Stage B 只读首次、末次和换档，会漏掉**档位未变但理由或推算改变**的错误；D260 要求看推算，因此应读每次判断，或明确承认抽样不能检出这类错误。([判断提示](/Users/lchingen/hivemind/src/hivemind/prompts/judging-v7.txt:10))

**(e) 需要 Alex 决定什么。** D186 本身已决定，D368 说下一抽取版本实现；**独立的 clean 区间调用是否承担这项决定**需要明确，不能把旧区间照搬当作已解决。多结果问题如何呈现和处理、以及不在研究名单中的主题如何承接，也需要具体方案和 Alex 的选择。生产请求允许写出名单外的主题名称，而后续匹配会跳过无法解析的对象；v3 限定只能选名单，改变了可表达的范围。([D368](/Users/lchingen/hivemind/docs/DECISIONS-log.md:3960), [生产请求](/Users/lchingen/hivemind/src/hivemind/extraction.py:385), [匹配](/Users/lchingen/hivemind/src/hivemind/views/matching.py:332))