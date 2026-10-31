**还剩一处实质冲突：5.1 和 5.2 的概括写得比 D250 的具体不收规则更宽。** 例如，一条具名分析师对新事件作出的新判断，即使分析员会记，只要它只是解读已记下的事、没有新事实或推算，D250 仍说不收。

[5.1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:371)写：

> “一个新的具体判断，是增量，不能漏”；“分析员会记的都留”。

但 [5.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:396) 和 [D250 第 4 条](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2982)说，具名分析师只是解读已记下的事、没有新事实或推算时不收。5.1 已指向 5.3 的具体边界，但“不能漏”和“都留”仍是无条件的说法。

[5.2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:387)也仍有同一冲突：

> “下面的不留清单不能用来删掉分析员会记的陈述。”

我同意 D240 原句 **“a reject rule never removes what the standard keeps”** 可以保留：D250 的具体边界也是标准的一部分。但前面的中文把“标准要留的”直接等同于“分析员会记的”，没有给 D250 明确不收的情况留空间。

最小修正是让 5.1 的“不能漏”“都留”和 5.2 的中文都明确按 **5.1 与 5.3 各行边界一起判**；D240 的英文原句保留。这只是消除页面内部的冲突，不新增规则。

五项倾向逐条核对如下：

1. **现成安排：一致。** 倾向是“只描述一个现成安排、没有新动作的，算背景，不收”。[5.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:397)写“只描述一个现成安排……没有新动作的，是背景，不收”；重述行也写“其余仍按这一行判”。[D250](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2979)一致，并保留仍有效的指引、预测和计划。没有日期本身不是删除理由。

2. **别家公司：一致。** 倾向是“说不出它通过需求、供给、竞争、定价这类路径动了英伟达哪个问题的，不收”。[5.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:405)写“要说得出它通过需求、供给、竞争、定价这类路径动了在研公司的哪个问题”。[D250](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2980)也用“such as”，不再把路径写成封闭的七类。

3. **产品对比：一致。** 倾向是“对手拿来和本公司比”的按 5.1 判，“其余的都算产品细节，不收”。[5.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:394)写“对手拿它和本公司产品比的……按 5.1 判”；“公司自己、伙伴或第三方发布的对比……是产品细节，不收”。[D250](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2981)一致；AMD 2.4 倍和同句的采用、集成动作仍有原来的处理。

4. **分析师解读：具体规则一致。** 倾向是“只是解读一件已经记下的事、没有新事实或推算的，不收”。[5.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:396)写“没有新事实或推算的，不收，有新事实或推算的按 5.1 判”；[D250](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2982)一致。它与 5.1 概括之间的冲突见上文。

5. **计数单位：一致。** 倾向是“只有当那条记录本身不是该留的事，才算留了杂音”。[9.2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/05-extraction-standard.html:541)明确写“不是金标判为核心、辅助或可选的同一件事时，才算留下”，并写计数辅助先算、有出入时读者对原文判。[D250](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2983)一致。现有金标本身没有完整的记录与事项对应关系，所以初算仍需读者处理差异，不能把它当成纯自动判定。

上一轮指出的流程图、第 6 节、5.1 的 5.3 指引和 B9 已按各行边界修正。除上面 5.1、5.2 的概括外，在本次范围内没有发现其他仍执行旧规则的地方；第 8 节的旧金标数字是历史记录，第 10 节的旧判例原话也是历史记录。整个审查保持只读。