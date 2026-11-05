上一轮四项中，两项已解决；付费探针的授权依据和 PRD 的版本引用仍未解决。

- **未解决 — 付费探针授权。** 两处现在文字一致：[AGENTS.md:326](/Users/lchingen/hivemind/AGENTS.md:326) 允许在方向已同意时进行“probes of a few cents … without asking”；[AGENTS.md:402](/Users/lchingen/hivemind/AGENTS.md:402) 也把这类探针排除在须明确许可的发送之外。但旧文件第 508 行说“A run starts only on his word”；[D355](/Users/lchingen/hivemind/docs/decisions/log.md:3713) 要求结果不符合假设时停下并告知 Alex，没有明确授权首次付费发送。**修正：**在 Alex 或一项决定明确授权这一例外之前，保留发送须经他明确许可的要求。

- **已解决 — 什么事情交给 Alex。** [AGENTS.md:37](/Users/lchingen/hivemind/AGENTS.md:37) 现在区分“a choice that changes what the system does”，需给问题、选项和建议；下一步工作则给“one recommendation and one test”。[AGENTS.md:339](/Users/lchingen/hivemind/AGENTS.md:339) 也明确保留产品选择的选项。

- **已解决 — 更正记录的内容。** [AGENTS.md:246](/Users/lchingen/hivemind/AGENTS.md:246) 已恢复“with its reason and its before and after”，并保留标日期、随评分打印、不合入金标的要求。

- **未解决 — 当前阶段 PRD 的标准版本。** [PRD:63](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md:63) 仍写“抽取标准第 3 版”；[AGENTS.md:234](/Users/lchingen/hivemind/AGENTS.md:234) 和 [D250](/Users/lchingen/hivemind/docs/decisions/log.md:2985) 均说明当前页面为第 5 版。这一项已在 [决策登记:41](/Users/lchingen/hivemind/docs/DECISIONS.md:41) 列为待 Alex 确认，且 PRD 正由其他人处理。**修正：**按其记录的变更边界更正版本引用，不改冻结标准页面。

本轮新增发现：

- **Serious — [AGENTS.md:123](/Users/lchingen/hivemind/AGENTS.md:123)：跨媒体重复陈述的启用条件被缩短。** 新文只说这个例外“switched on only after it is measured”，没有说明要测什么。[D248 第 7 条](/Users/lchingen/hivemind/docs/decisions/log.md:2966) 要求启用前既测 G3 金标上的合并风险，也测原始发言人和日期字段的准确性。只测其中一项也可能被理解为满足新规则。**修正：**明确列出这两项启用前测量，或直接指向 D248 的完整条件。

- **Serious — [AGENTS.md:447](/Users/lchingen/hivemind/AGENTS.md:447)：给 Alex 的页面语言被写成已确定的规则。** 这里要求“plain Chinese for Alex's pages”，同时要求维护中的文档用英语；但 [D163](/Users/lchingen/hivemind/docs/decisions/log.md:2302) 说当前文档用英语，而 [决策登记:48](/Users/lchingen/hivemind/docs/DECISIONS.md:48) 将给 Alex 审阅的页面使用中文列为“not a recorded decision”，待他确认。**修正：**将中文页面表述为待确认的做法，避免与已生效的英语规则并列为确定要求。

冻结尺子的路径在本次只读检查中均存在。章节号本身未发生重排；本次没有继续审查正在由其他人修改的 PRD 和系统设计文件，也没有修改文件。

serious: 4, wording: 0