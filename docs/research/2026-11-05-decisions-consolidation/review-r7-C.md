发现 **4 处严重问题**：两处示例仍把未实现的依赖写成已有关系，一处设计页写错待决定事项数量，PRD 10 还有两处已登记、待 Alex 处理的旧文字。

- **serious — 两个示例仍称新问题已有依赖。** [05-extraction.md:129](/Users/lchingen/hivemind/docs/prd/05-extraction.md:129) 写“Grouping does not replace #2's dependency on #1”；[06-views.md:209](/Users/lchingen/hivemind/docs/prd/06-views.md:209) 写“depends on #1, with easing bullish”。对应生成源分别是 [new-facts.js:157](/Users/lchingen/hivemind/docs/system-design/new-facts.js:157) 和 [new-facts.js:359](/Users/lchingen/hivemind/docs/system-design/new-facts.js:359)。D51 决定在匹配时选择依赖，但当前 Jev 路径明确“不询问依赖”：[jev_matching.py:7](/Users/lchingen/hivemind/src/hivemind/views/jev_matching.py:7)；[DECISIONS.md:32](/Users/lchingen/hivemind/docs/DECISIONS.md:32) 也将其列为已决定、未建成。**修正：**两处都说明默认路径尚未创建这条依赖；主题通过主题内容影响 #2，如 [05-extraction.md:124](/Users/lchingen/hivemind/docs/prd/05-extraction.md:124) 已说明。

- **serious — 设计页写错待决定提案数量。** [new-design.js:109](/Users/lchingen/hivemind/docs/system-design/new-design.js:109) 写“two remaining pull-mode proposals are listed separately”，但 [06-views.md:360](/Users/lchingen/hivemind/docs/prd/06-views.md:360) 和其生成源 [new-facts.js:470](/Users/lchingen/hivemind/docs/system-design/new-facts.js:470) 只列出一项未决定的重复问题检查。**修正：**改为“one remaining duplicate-check proposal is listed separately”。

- **serious — PRD 10 仍把删除兜底句写成要做的事。** [10-filing-phase.md:89](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md:89) 写“删掉兜底句”；[D361](/Users/lchingen/hivemind/docs/decisions/log.md:3858) 写“The fallback sentence stays in production”。这是 [DECISIONS.md:45](/Users/lchingen/hivemind/docs/DECISIONS.md:45) 已登记、留待 Alex 处理的差异。**建议仅加状态行：**“第 5 节方案未通过第 8 节测试；D361 保留兜底句。”

- **serious — PRD 10 写错冻结标准版本。** [10-filing-phase.md:63](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md:63) 写“抽取标准第 3 版”，现行冻结标准是第 5 版；差异已记在 [DECISIONS.md:45](/Users/lchingen/hivemind/docs/DECISIONS.md:45)。**建议留待 Alex 处理：**状态行注明“冻结的抽取标准为第 5 版”。

本轮只读，未修改文件。

serious: 4, wording: 0