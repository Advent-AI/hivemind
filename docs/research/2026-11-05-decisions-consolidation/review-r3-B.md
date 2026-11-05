上一轮的六项中，四项已解决；付费探针按本轮给定的解释保留，PRD 版本引用仍待 Alex 决定。本轮另发现两处严重问题。

- **付费探针：按本轮给定边界保留。** [AGENTS.md:326](/Users/lchingen/hivemind/AGENTS.md:326) 允许在方向已同意、没有停止指令时做“probes of a few cents on stored cases without asking”；[第 402–404 行](/Users/lchingen/hivemind/AGENTS.md:402) 要求更大范围的付费发送经 Alex 明确同意。[第 328–329 行](/Users/lchingen/hivemind/AGENTS.md:328) 同时保留 D355 的要求：“a result that contradicts the hypothesis stops the line and goes to him”。我不再把这一授权边界列为本轮发现。

- **交给 Alex 的事项：已解决。** [AGENTS.md:37](/Users/lchingen/hivemind/AGENTS.md:37) 写明改变系统行为的选择要给“the question, its options and your recommendation”；下一步工作给“one recommendation and one test”。

- **更正记录：已解决。** [AGENTS.md:246](/Users/lchingen/hivemind/AGENTS.md:246) 要求更正记录包含“its reason and its before and after”，并随每次评分打印、不合入金标。

- **当前阶段 PRD 的标准版本：仍待 Alex 决定。** [决策登记:41](/Users/lchingen/hivemind/docs/DECISIONS.md:41) 记录 PRD 写的是第 3 版、页面是第 5 版，并写明“PRD 10 changes only on Alex's word”。本轮按要求没有审查正在修改的 PRD。

- **跨媒体重复陈述的启用条件：上一轮指出的条件缺失已解决。** [AGENTS.md:123](/Users/lchingen/hivemind/AGENTS.md:123) 现在要求先测“merge risk on the gold and the accuracy of the original speaker and day fields”。但另一处无条件表述仍与此冲突，见下方新发现。

- **给 Alex 审阅的页面语言：已标明未确认。** [AGENTS.md:447](/Users/lchingen/hivemind/AGENTS.md:447) 现在将中文页面标为“the practice since then, not yet confirmed by him”，并指向待确认事项。

本轮新增严重发现：

- **Serious — [AGENTS.md:375](/Users/lchingen/hivemind/AGENTS.md:375)：跨媒体重复陈述仍被无条件写成一条。** 这里说“a statement carried by several outlets is one statement”，但同文件[第 123–125 行](/Users/lchingen/hivemind/AGENTS.md:123)说该例外只有在两项测量后才能启用。[D248 第 7 条](/Users/lchingen/hivemind/docs/decisions/log.md:2966)也要求先测合并风险和原始发言人、日期的准确性。读者按第 8 节执行时，可能直接合并，绕过启用条件。**修正：**第 8 节指向第 3 节的条件，明确这是选定但须先测量才能启用的例外。

- **Serious — [docs/granularity-research.md:24](/Users/lchingen/hivemind/docs/granularity-research.md:24)：章节引用指错位置。** 该行写“AGENTS §6：模型调用是一次采样”，但现行规则在 [AGENTS.md:321](/Users/lchingen/hivemind/AGENTS.md:321) 的 §7.3；§6 是提示词规则。读者按引用查不到所述规则。**修正：**将该引用改为 AGENTS §7.3。

serious: 2, wording: 0