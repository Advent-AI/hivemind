这一轮发现 **3 处严重问题**：一处示例把尚未实现的功能写成现有行为，另两处是已登记、留待 Alex 处理的 PRD 10 状态。

- **serious — 示例称系统会为文章新开的题自动添加依赖。** [05-extraction.md:124](/Users/lchingen/hivemind/docs/prd/05-extraction.md:124) 写“The library opens #2, dependent on #1”，其生成源是 [new-facts.js:145](/Users/lchingen/hivemind/docs/system-design/new-facts.js:145)。D51 决定由匹配步骤选择依赖，但当前默认路径尚未实现：[jev_matching.py:7](/Users/lchingen/hivemind/src/hivemind/views/jev_matching.py:7) 明写“Dependencies are not asked”，[DECISIONS.md:32](/Users/lchingen/hivemind/docs/DECISIONS.md:32) 也将其列为已决定、未建成。**建议改为：**“The library opens #2. Selecting its dependency on #1 was decided in D51 but is not built on the default Jev path.” 同步调整示例后文对该依赖的描述。

- **serious — PRD 10 把旧方案写成待执行步骤。** [10-filing-phase.md:89](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md:89) 仍写“删掉兜底句”。该方案的测试未通过，[DECISIONS.md:45](/Users/lchingen/hivemind/docs/DECISIONS.md:45) 记录 D361 暂时保留兜底句，并将 PRD 10 的修改留给 Alex。**建议仅加状态行：**“本节方案已在第 8 节测试中未通过；D361 暂时保留兜底句。”

- **serious — PRD 10 写错冻结标准的版本。** [10-filing-phase.md:63](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md:63) 写“抽取标准第 3 版”。[AGENTS.md:7.1](/Users/lchingen/hivemind/AGENTS.md) 将冻结标准列为第 5 版，[DECISIONS.md:45](/Users/lchingen/hivemind/docs/DECISIONS.md:45) 也已记录这个差异。**留待 Alex 决定后更正：**“抽取标准第 5 版”。

此次只读，未修改文件。

serious: 3, wording: 0