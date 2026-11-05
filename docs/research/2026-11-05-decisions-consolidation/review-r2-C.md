这一轮还有 **7 类严重问题**。例如，正文已写“旧材料和更新都保留”，研究组的读取规则却仍要求排除被更新的旧材料。

上一轮各类的状态：

1. **抽取看到的题目和研究组：部分解决。** [05-extraction.md:17](/Users/lchingen/hivemind/docs/prd/05-extraction.md:17) 已写“open at the start of the item's day”和“no separate list of research groups”；但 PRD 06 的决定摘要仍有旧说法，见下方问题 1。
2. **已删除的候选题字段：已解决。** [05-extraction.md:155](/Users/lchingen/hivemind/docs/prd/05-extraction.md:155) 列出的候选题字段已不含这两个字段。
3. **日常材料挂多道已开题：已解决。** [05-extraction.md:44](/Users/lchingen/hivemind/docs/prd/05-extraction.md:44) 写“One home: the narrowest block-5 thesis … plus the answer's candidates”。
4. **只挂直接谈到的题：已解决。** [05-extraction.md:37](/Users/lchingen/hivemind/docs/prd/05-extraction.md:37) 已包括通过“demand, supply, competition or pricing”影响答案的材料。
5. **宏观主题必须逐条连到公司题：已解决。** [01-universe.md:80](/Users/lchingen/hivemind/docs/prd/01-universe.md:80) 已写“every open, judged theme thesis is shown to every asset thesis’s judgement”。
6. **逐篇判断：已解决。** [06-views.md:156](/Users/lchingen/hivemind/docs/prd/06-views.md:156) 已写“once a day after the day's last item”。
7. **判断读取全部有效材料：已解决。** [06-views.md:15](/Users/lchingen/hivemind/docs/prd/06-views.md:15) 已写最近五次判断以来的新材料及最近十次判断引用的依据。
8. **更新和迟到材料被退休或丢弃：部分解决。** [06-views.md:166](/Users/lchingen/hivemind/docs/prd/06-views.md:166) 已写“both in force”和“an older statement arriving later is stored and linked”；但研究组读取及修订报道的旧说法仍在，见问题 2、3。
9. **重复报道只增加来源：部分解决。** [06-views.md:344](/Users/lchingen/hivemind/docs/prd/06-views.md:344) 已写“A repeat is stored as its own piece”；但同一篇中的重复数字出现了互相矛盾的指令，见问题 4。
10. **匹配流程和默认配置：已解决。** [06-views.md:3](/Users/lchingen/hivemind/docs/prd/06-views.md:3) 已写 Jev、身份冲突判断和 `poc-v116`。
11. **Config 漏设置：已解决。** [03-config.md:8](/Users/lchingen/hivemind/docs/prd/03-config.md:8) 已列出身份冲突判断和开始跟踪时读取。
12. **只有事实能决定判断：已解决。** [06-views.md:91](/Users/lchingen/hivemind/docs/prd/06-views.md:91) 已写“The rung is a forecast against a reference”。
13. **后来补充依赖被永久禁止：已解决。** [06-views.md:128](/Users/lchingen/hivemind/docs/prd/06-views.md:128) 已标明这一决定“decided … but not built”。另有新题依赖的实现状态问题，见问题 5。
14. **当前阶段旧计划未标状态：未解决。** [10-filing-phase.md:89](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md:89) 仍写“删掉兜底句”，见问题 7。

严重问题：

- **serious — 旧决定摘要仍要求抽取看到依赖。** [06-views.md:374](/Users/lchingen/hivemind/docs/prd/06-views.md:374) 写“show dependencies during extraction”。但 [05-extraction.md:28](/Users/lchingen/hivemind/docs/prd/05-extraction.md:28) 明确写“no dependency links”；D211 删除旧上下文，D264 后来重新提供当天开始时的题和收纳说明，见 [log.md:2687](/Users/lchingen/hivemind/docs/decisions/log.md:2687) 和 [DECISIONS.md:47](/Users/lchingen/hivemind/docs/DECISIONS.md:47)。**改为：**“D41/D42 原先要求展示依赖；现行请求按 D211、D251、D264 展示当天开始时已开的题及收纳说明，不展示依赖链接。”

- **serious — 研究组仍排除被更新的旧材料。** [06-views.md:397](/Users/lchingen/hivemind/docs/prd/06-views.md:397) 和生成源 [new-facts.js:41](/Users/lchingen/hivemind/docs/system-design/new-facts.js:41) 写“excluding evidence already replaced at that point”。D202 明确规定“both pieces stay in force”，见 [log.md:2597](/Users/lchingen/hivemind/docs/decisions/log.md:2597)。**改为：**“按请求的序号读取成员题实际关联的材料；修订前后的材料都保留并生效，修订关系另行记录。”

- **serious — 修订后的报道仍被写成只改变来源。** [06-views.md:162](/Users/lchingen/hivemind/docs/prd/06-views.md:162)、[319](/Users/lchingen/hivemind/docs/prd/06-views.md:319)、[350](/Users/lchingen/hivemind/docs/prd/06-views.md:350) 及 [new-facts.js:305](/Users/lchingen/hivemind/docs/system-design/new-facts.js:305)、[458](/Users/lchingen/hivemind/docs/system-design/new-facts.js:458) 写“A revised input changes only its own source reference”或“A revised retelling changes only its own source reference”。这会让报道修订后新增或改变的内容丢失。D204 要求“stores every incoming piece once with all its destination links”，见 [log.md:2612](/Users/lchingen/hivemind/docs/decisions/log.md:2612)。**改为：**“修订后的报道按新输入读取并保存其内容和关联；它不改写原始报道的材料，匹配出的重复或修订关系另行记录。”

- **serious — 同一篇中重复的数字被要求既合并又分别保存。** [06-views.md:191](/Users/lchingen/hivemind/docs/prd/06-views.md:191) 和 [new-facts.js:338](/Users/lchingen/hivemind/docs/system-design/new-facts.js:338) 把“the same number in text and table”列入“Store it as its own piece”。但 [05-extraction.md:147](/Users/lchingen/hivemind/docs/prd/05-extraction.md:147) 与 [06-views.md:302](/Users/lchingen/hivemind/docs/prd/06-views.md:302) 均要求同一篇中的文字和表格重复成为一条材料、带多个引用；D204 的丢失场景是另一条输入的内容，见 [log.md:2612](/Users/lchingen/hivemind/docs/decisions/log.md:2612)。**改为：**“同一输入中文字和表格重复的同一事实使用一条材料及多个引用；另一条输入的重复材料各自保存并记录关系。”

- **serious — 设计页把新题选择依赖写成现有行为。** [new-design.js:109](/Users/lchingen/hivemind/docs/system-design/new-design.js:109) 写“New theses select dependencies”。但 [DECISIONS.md:31](/Users/lchingen/hivemind/docs/DECISIONS.md:31) 明确记载：D51 已决定由匹配选择，但默认 Jev 路径没有询问，文章开的题因此没有自己的依赖。**改为：**“新题由匹配选择依赖是已作出的决定；默认 Jev 路径尚未实现这一选择。”

- **serious — 抽取 PRD 把冻结标准页放在后续决定之上。** [05-extraction.md:5](/Users/lchingen/hivemind/docs/prd/05-extraction.md:5) 写“Where this PRD differs from it, the page governs”。但 [DECISIONS.md:47](/Users/lchingen/hivemind/docs/DECISIONS.md:47) 已列出冻结页中被后来决定改变的内容，包括抽取看到的题和判断是预测；冻结页不能因此改写。**改为：**“标准页作为冻结的衡量依据保留；后来决定改变的产品行为以现行决定为准，差异按冻结规则另作记录。”

- **serious — PRD 10 的旧计划仍未标明已被测试结果取代。** [10-filing-phase.md:89](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md:89) 仍写“删掉兜底句”；同页 [140–142](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md:140) 记录方案未通过测试、D361 暂时保留兜底。[DECISIONS.md:44](/Users/lchingen/hivemind/docs/DECISIONS.md:44) 将此列为等 Alex 处理的事项。**建议仅加一条状态行：**“本节方案已在第 8 节测试中未通过；D361 暂时保留兜底句。”PRD 10 按约定留给 Alex。

此次只读，未修改文件。

serious: 7