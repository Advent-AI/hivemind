**结论：目前继续用 Jev 做 clean Step 2，是现有证据支持得最充分的选择；但我对“它已经足够可靠”的信心较低，对“现在没有证据支持替换它”的信心较高。**

一个具体例子：两篇文章报道同一笔 Nvidia 收购，Jev 三次都把它们当作不同消息；DeepSeek 三次都认出是同一公告。但在另一组文章里，DeepSeek 三次都把“公司预测增长 70%”错误连成对“客户预测可能翻倍”的修订。它目前也没有提供产品需要的多个候选之间的排序。所以，**保留 Jev 是暂时的研究判断，不是 Jev 已经被证明最好或可以放心交付。**

## 实际比较结果

我核对了保存的逐次回答：六个选定案例、三种方式、各三次，共 **54 条完成记录**。下表中的“相同、不同、修订”是对指定候选的判断；三次是三次请求，不代表三个独立案例，也不能保证服务内部采样彼此独立。[原始事件](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/probe-2026-11-09/events.jsonl)、[请求内容](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/probe-2026-11-09/bodies.json)。

| 案例 | Jev 完整候选 | Jev 单对 | DeepSeek 单对 | 原文支持的判断 |
|---|---|---|---|---|
| B01：Broadcom 同一预测 | 相同 3/3 | 相同 3/3 | 相同 3/3 | 同一预测；新增细节不改变主陈述。 |
| B05：70% 与客户可能翻倍 | 修订 2/3，不同 1/3 | 不同 3/3 | 修订 3/3 | 原文支持不同；DeepSeek 有稳定回退，完整 Jev 也有错误。 |
| B10：Vera Rubin 投产、收入占比与交付 | 相同 1/3，不同 2/3 | 相同 2/3，不同 1/3 | 不同 3/3 | 交付和已有的投产、收入预测是不同陈述；其是否属于“明确错误”还是有重叠，历史读者有分歧。 |
| H01：同一收购公告 | 不同 3/3 | 不同 3/3 | 相同 3/3 | 原文支持同一公告；这是 Jev 稳定漏合并的例子。 |
| P01：官方否认延期 | 修订 3/3 | 修订 3/3 | 修订 3/3 | 目标关系有依据，但只覆盖这一个否认案例。 |
| R05：Shield TV 是否停产 | 修订 3/3 | 修订 3/3 | 不同 3/3 | **有争议**：我倾向不同，但不能把修订判定为无争议的错误。 |

这不是总体排名。Jev 完整候选是当前产品形式；另外两列只比较一个对子。B05 中，完整 Jev 和单对 Jev 给出不同结果，说明**这次结果对请求形式敏感**，但不能证明原因就是其他候选干扰。DeepSeek 同时换了提供商、模型和输出形式，因此也不能把差异单独归因于模型。

完整 Jev 的保存回答经现有代码重放后，B10 一次并入旧组、两次新建；H01 三次都新建。DeepSeek 没有判断其他候选，不能由它的单对回答推断整条记录最终会进入哪个组。[重放结果](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/RESULTS-DRAFT.md)、[分组代码](/Users/lchingen/hivemind/clean-arch/step2/compare.py:109)。

## 原文里最影响判断的地方

- **H01：**两篇保存的文章都说 Nvidia 周四宣布收购 Hugging Face；129 亿和约 130 亿美元可由四舍五入解释。文章支持“报道了同一公告”，但不证明交易已完成，也不证明公告本身真实。Jev 三次没认出重复，DeepSeek 三次认出。[两篇原文和记录](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/blind-missed.json)。

- **B05：**旧文章同时写了 70% 公司指引和客户预测可能翻倍，新文章写 70% 指引。它们可以同时成立，不支持把前者说成修改了后者。限制是：送给比较器的新记录没有包含原文中的供给约束，旧陈述日期未知，两篇报道对 70% 的个人说话人归属也不一致。**这些限制削弱对犯错原因的判断，不改变原文对“两个说法不同”的支持。**[原文](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/source-blind-packet.json)、[输入细节](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/INVESTIGATION.md:87)。

- **B10：**一篇说产品已投产、管理层预计其占第三财季数据中心收入约 20%；另一篇说八月已有商业交付。交付是新节点，不是那个收入预测的复述。旧记录把“已投产”归给 Nvidia，比文章本身的归属更强；历史审阅对“明确错误”与“有重叠”也有分歧。[原文](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/source-blind-packet.json)、[历史分歧](/Users/lchingen/hivemind/reports/step2-wrong-merge-council-2026-11-09/CONCLUSIONS.md)。

- **R05：**旧文章推测标准版 Shield TV 似乎停产，同时承认可能只是缺货。后文拿到 Nvidia 回信：缺货由需求造成，未来供应没有更新；公司没有确认或否认停产。另一种合理读法是，同一作者的后续报道改变了先前判断。旧记录还把媒体推断的原始说话方写成 Nvidia。我倾向将两条看作不同陈述，但保留另一读法，不用多数票把它变成标准答案。[两篇原文](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/blind-revisions.json)、[分歧](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/result-blind-claude.md)、[只看原文的复核](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/r05-adjudication.md)。

- **P01：**官方否认延期的目标关系有依据，但否认已经出现在旧文章里，日期也有冲突，所以它不能证明识别“后来修改预测”的一般能力。更关键的是，完整 Jev 三次都除了连接延期报告，还连接了“备用机柜方案被取消”这一条。文章先提到该方案，再笼统说 Nvidia 拒绝这些说法；实际比较输入只说否认延期。**第二条链接是否成立仍有争议**，不能用目标关系答对来证明整个写入结果正确。[原文](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/blind-positive-revisions.json)、[第二条链接](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/results-codex-followup.md)。

这些阅读是对保存的媒体文本的判断；盲读者也是 AI，**不是 Alex 签过的金标**。部分结果盲读虽然隐藏了哪个模型产生答案，但答案选项和原文放在同一包里，不能称为完全看不到输出的盲读。

## 为什么暂时保留 Jev，为什么还不能放心

**支持保留的证据：**

1. Jev 已经完成当前路径：搜索候选后逐一比较；有多个重复时，按其给出的同一陈述概率选择一组。这是 Alex 的 D381 决定。DeepSeek 的实验只返回单对标签，没有提供这一排序，也没有测完整历史向前运行的结果。[PRD](/Users/lchingen/hivemind/clean-arch/PRD.md:129)、[D381](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4101)。
2. 一次新样本中，搜索找到 **141/143** 个已保存、已标注的重复对；另外两对因一条记录未保存而无法搜索，放到整个路径是 **141/145**。但一个大组贡献 55 对，修订几乎没有覆盖，所以不能把 98.6% 当作所有真实重复和修订的召回率。[记录](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1605)。
3. 同一次中，第三读者判定明确错误合并 **1/57**，另有两个有重叠的案例；此前一次是 **3/104**，没有达到 Alex 的 2% 线。三个开发运行分别是 **1/100、1/100、1/106**，但重复使用文章，不能当成三个独立数据集。结果随样本和读者判断变化，不能从一次通过推断稳定通过。[新样本和三次开发运行](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1619)、[此前未通过](/Users/lchingen/hivemind/clean-arch/step2-validation-2026-11-07/LOG.md:285)。

**限制同样重要：**

- 搜到了不等于认对了。H01 的候选已找到，Jev 仍三次漏合并；搜索成绩不覆盖这类比较错误。
- “正文保留下来”不等于读者一定正确理解。当前代码保留每条成员自己的文本，却把它展示在“同一陈述的后续报道”之下；B10 因此会有误导性标题。此前针对后来新增细节的阅读测试里，分组与不合并分别得到 **25/36 与 25/36**；这支持保留文本，但测试没有证明错误分组安全。新样本的 **22/26 对 22/26** 更主要是结构性保存检查，不是读者理解的证明。[阅读测试](/Users/lchingen/hivemind/clean-arch/step2-validation-2026-11-07/LOG.md:237)、[展示代码](/Users/lchingen/hivemind/clean-arch/step3/library.py)。
- 修订链接没有被 D381 的三条验收线充分测到。四个保存运行共写出 **84 条修订链接，来自 39 条新记录**；其中有的记录同时并入重复组。它们不是 84 个独立案例，也没有全部经过原文判断。B05 证明，即使记录并入了正确的 70% 组，仍可能额外写出错误修订链接。[逐运行计数](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/INVESTIGATION.md:47)。
- D202 和 D204 的教训是：不能因一次模型判断就丢掉旧证据或新文本。clean 路径保留文本是重要进步，但错误关系仍会影响读者如何理解两条记录；目前没有证明 B10 改变了最终投资判断。[D202 和 D204](/Users/lchingen/hivemind/docs/DECISIONS-log.md:2594)。

## 其他办法的证据

- **给 Jev 看搜索相似度：**原计划 11 个案例，完成了 6 个；这 6 个的 46 个候选关系在三次对照与三次处理里没有变化。关键错误合并和修订案例没跑到。因此没有看到收益，也不能说无效或等价。[中断实验](/Users/lchingen/hivemind/reports/step2-score-council-2026-11-08/RESULTS.md)。
- **设置 0.5 门槛：**对保存的 363 次合并决定离线回放，会挡住 1 次读者认为错误的合并，也挡住 4 次读者接受的合并和 1 次有重叠的合并。高分错误也存在；这不足以支持门槛。[复核](/Users/lchingen/hivemind/reports/step2-merge-fix-council-2026-11-09/CONCLUSIONS.md)。
- **只在没有新增重要内容时合并：**旧试验在同一批 102 次合并中只保留 22 次；虽然留下了抽查中的重要新增内容，也把不少无关紧要的变化拆开。这个办法没有证明能可靠分辨重要与不重要。[历史测试](/Users/lchingen/hivemind/clean-arch/step2-validation-2026-11-07/LOG.md:135)。
- **DeepSeek 替换或加一道复核：**H01 值得重视，B05 同样值得重视。它尚未回答多候选排序、不同意见如何处理、搜索漏掉候选怎么办，以及完整写入后的效果。B05 是结果出现后的严重回退，**不是预先明确写下的 B01/P01 自动停止条件**。[实验规则与纠正](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/COUNCIL-LOOP.md:71)。

要推翻“继续用 Jev”的建议，需要一个完整候选方案在相同的保存输入及之后独立的新文章上，既能按 D381 选择正确组，又能减少错误合并、漏合并和错误修订，同时保住真实重复与真实更新；还要看读者实际看到的内容。反过来，如果系统性检查发现 Jev 的错误链接或漏合并经常改变读者对证据的理解，即使替代方案还没准备好，也会推翻“当前可靠”的判断。

**我建议的唯一下一步免费研究：**逐条检查已完成的 D392 第一次开发运行中 **56 个 Jev 判为修订的候选回答**，把每个回答放回原始文章、当时的完整候选、实际写入的所有链接和读者看到的文字中。分别列出有原文支持、无原文支持、争议未决，以及输入缺失的信息；同时保留真实否认和真实更新作为反例。56 是候选回答数，不能直接称为 56 个独立错误或 56 条最终链接。这个检查能先回答：B05、P01 是否只是孤例，以及问题在比较、写入关系还是展示。它不需要改代码、发请求或改变任何标准。[待查范围](/Users/lchingen/hivemind-step2-identity-2026-11-09/clean-arch/step2-identity-2026-11-09/results-claude.md:84)。

本次只读；没有编辑文件、发送模型请求或打开运行中的数据库。