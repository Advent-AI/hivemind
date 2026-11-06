**可以做这一步的离线实现和测试，但目前还不能证明准备出来的记录可靠。** 不需要改 A 提示词或冻结金标；现有代码里有几处会改写或合并 A 的内容，必须在这一步明确拦住。

例如，存下的 A 问的是 NVIDIA 在 FY2027 年末有多少供应承诺。A 把 **1 月 31 日**说成要衡量的时点，把年报说成**预计 2 月左右**发布，并明确说不知道具体发布日期。系统却要求一个准确的到期日。不能把 1 月 31 日或 2 月某一天冒充年报发布日期；如果没有符合原标准、又能明确标为分析员检查日的日期，这条就应报告为无法表示。见 [存下的 A 回答](/Users/lchingen/hivemind-no-preseed-evidence-review/poc/data/simple-new-question-run-2026-11-05-v1/gnews_4d1b1ca014068fb532f116b3/result.json) 和 [候选写入标准](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/prompts/role-v74i.txt:19)。

还需要解决的具体问题和代码要求如下。

1. **先把“一条 A 内容对应哪条记录”定死。** A 的摘要字段实际叫 `what_it_shows`，不是 `one_line`。代码应按 A 中问题和证据的位置生成唯一 ID，把 A 的 `question`、每条 `quote` 和 `what_it_shows` 原样复制到生产记录的对应字段，并保存 `original_speaker` 原文作为可追溯信息。缺项、多项、引用不明或一条 A 证据无法对应一条记录，都要明确拒绝。不能让准备调用重写这些文字。现有 [A 格式](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/simple_new_question_poc.py:31) 和 [生产格式](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/extraction.py:71) 可以直接对照。

2. **来源日期和检查日必须真正留下来。** `due_day` 是会影响关闭时间的字段；`looks_at` 是会被保存、也会被后续判断读取的文本，因此可以放明确的“来源写明的日期”或“分析员选定的检查日”说明。代码应检查日期是真实日期、在文章之后、符合问题的期间与可核对材料，并检查说明与 `due_day` 一致。原标准对数字要求在公布时核对；对没有日期的待决监管事项才有明确的财年末检查日规则。**不能把“分析员选的”当作任意补一个日期的许可。** 已有财年工具只保存结束月份，并把月份最后一天当财年末，不能独立证明某公司实际的具体日期；生产检查还会重算数字问题的期间。准备前后都要比对，变化无法证明正确就拒绝。见 [标准](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/prd/05-extraction-standard.html:274)、[期间处理](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/extraction.py:649) 和 [财年工具](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/universe.py:74)。

3. **答案区间是新判断，不能只检查数量。** 数字问题应有五档，是非事件可以有两档；区间条件要可核对、覆盖所有结果、边界不重叠，并说明中间档的比较依据。金额用完整数值，百分比用 73 而不是 0.73；数值下界包含、上界不包含。现有检查允许所有边界为空，也不足以证明文字条件与数值边界一致或比较依据合理。需要逐条检查并保存分析员选区间的理由；没有足够依据时拒绝，不能假装这些区间来自文章。见 [写入规则](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/prompts/role-v74i.txt:24) 和 [现有检查](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/extraction.py:493)。

4. **其他补充字段也要逐个对照问题和原文。** 标的、问题类型、衡量对象、范围、期间、单位和会计口径不能悄悄改变原问题；开题理由必须能落入生产格式允许的类别，核对材料必须非空且能回答原问题。分组要指向有依据的持续事项，公司本身不算一个分组。证据的说话人、原始来源、日期和等级要能从文章支持；未知的原始日期保持空值，作者观点不能升级成公司事实。生产检查只检查其中一部分的格式，不能代替逐条语义审阅。见 [生产字段](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/extraction.py:96)。

5. **现有检查会改写或合并证据，必须在独立测试中暴露。** `sift` 会修补引文、按相同引文合并记录、保留第一条摘要，并可能规范化日期、范围和期间。保存 A 的原文后，应分别比对检查前后的每条记录；任何引文或摘要变化、合并、丢弃和引用变化都要成为明确的未完成结果，不能算通过。尤其不能用唯一 ID 声称相同引文的含义碰撞已经解决。见 [实际处理](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/extraction.py:609)。

6. **原始回答和理由需要单独保存。** 生产 JSON 格式禁止额外字段，也没有位置存准备调用的原始回答、区间选择理由或 A 的原始说话人文字。离线准备步骤因此需要与生产记录关联的独立记录：保存完整输入、原始 A 回答、准备调用的完整原始回答、每个问题和证据的位置对应、选择理由以及每次拒绝的原因。生产记录仍使用原有格式；不能把未完成记录伪装成有效结果。

我建议先做**一个不调用模型的存量输入测试**：用上述已存 A 回答和文章，构造一份模拟的准备回答，经过生产格式和检查，再逐字段比较检查前后的结果。测试应包含原样保留、缺项或多项、引文被修补、相同引文被合并、日期只有月份、无依据的区间，以及生产代码重算期间的情况，并让故意破坏原文的版本确实失败。这个测试能证明交接和拒绝机制；它**不能证明真实准备调用会作出正确的日期、区间或来源判断**。

七天集成仍然停止，直到相同引文的不同含义以及中断后恢复的问题得到解决。本次没有修改文件，也没有调用模型。