**我支持先单独验证“生成答案区间”这一步，再接判断；但 v2 还不能按原样交给 Alex 批准。** 最关键的问题是：它允许系统只回答原问题的一部分，却仍把答案挂在原问题下。

例如，u2 的内存问题同时问新增产能和价格是否持续高企。只回答产能，无法告诉读者价格会怎样；即使记录了“漏掉价格”，读者仍可能以为整道问题得到了回答。([案例原文](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/census/packet.md:895))

我接受你对我上次否决条件的批评：**“出现一个需要推导日期或没有参照数字的案例就失败”不成立。** 缺口应先分类、计数，再判断已有决定能否解决，以及是否需要请 Alex 决定。

你补充的事实大体成立，但有几个边界：

- 我复核了 34 条：开题类型确实是 7、6、13、8；日期字段为 5 条含 ISO 日期、29 条只有文字、0 条为空。5 条含日期不等于日期一定正确。资料包有 34 条问题、79 条开篇关联证据；它从保存的回答按描述找回字段，不代表当前产品库已保存这些字段。([资料包生成方式](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/census/build_packet.py:17))
- E3、E4 的记录准确：21/44 是旧实验的生成情况，18/25 是**错误条数**，不是 18 个受影响问题或 72% 的新系统失败率。([E3、E4](/Users/lchingen/hivemind/docs/prd/11-production-experiments-from-split.md:78))
- 21 条按 `shared_quantity` 或 `policy_stage` 开题，**不自动等于 21 条都应存为主题**；类型还要按具体问题判断。且只有已有当前判断、仍开放的主题才进入判断输入。([判断代码](/Users/lchingen/hivemind/src/hivemind/views/judging.py:76))
- 16 个匹配和 16/16 一致成立，但复用了原有问题和区间；Ohio 的日期不同，因此它不能不加处理地作为同一道定期问题的答案对照。([匹配](/Users/lchingen/hivemind/clean-arch/unseeded-2026-11-10/mapping-runs.json), [结果](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:2686))

**(a) 复合问题。** D38 已规定：数字与事件、或能独立变化的部分，要分成不同问题；D388 明确 Ohio 的重大未签承诺有独立的“是否签约”问题。它们**没有授权**通用地挑一个结果、把其他部分留在旁边后仍宣称回答了原问题。([D38](/Users/lchingen/hivemind/docs/DECISIONS-log.md:753), [D388](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4172))

Ohio 的签约是已有决定明确要求的一项；金额未披露也不能被当作已知。但 u2 clean-10 的产能与价格都写进 `outcome`，`settled_by` 也同时指向两类资料，所以“按这两个字段挑一个”没有决定选择哪一个。拆分后的身份和证据归属、或暂不生成并说明原因，需设计并在改变产品行为处请 Alex 决定。([案例](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/census/packet.md:895))

**(b) 主题。** D191、D195 已决定生产判断中主题对公司的作用及变化后的重判，D195 还明确替换了 D191 最初“不立即扩散”的后果说明。clean PRD §7 尚未规定如何接入，因此不能凭“开放”忽略已有决定；但把 clean 问题如何映射到主题对象，设计还没有答案。([D191](/Users/lchingen/hivemind/docs/DECISIONS-log.md:2503), [D195](/Users/lchingen/hivemind/docs/DECISIONS-log.md:2538), [clean PRD](/Users/lchingen/hivemind/clean-arch/PRD.md:191))

现有种子 v8 使用 `chip-export-controls`；**clean 主题目前没有确定的 object ID**。生产匹配器调用 `universe.resolve`，无法识别的对象会被跳过；`store` 本身能存任意文本，判断器也会把它展示出来，所以不能笼统说“任意 ID 必然让判断器崩溃”。须确定身份及所有读者，不能只设置 `object_kind`。([种子](/Users/lchingen/hivemind/poc/seeds/nvda-2026-07-01-v2.json:373), [匹配器](/Users/lchingen/hivemind/src/hivemind/views/matching.py:332))

**(c) 三个字段。** 保留 `settles`，让区间说明它实际回答什么；保留可见的未解决部分作为**检验结果**，但不能把 `left_out` 当成许可改题。`due_day_basis` 应保留，以区分原文日期、规则推导和预计日期；财政年度说明只给预计月份，未提供精确的实际发布日期。`reference` 不应强制只能摘自开篇文章：D260 的参照包括市场预期、指引、计划或期限，可能是非数字，也可能缺失。可以允许空值并报告，不能把无数字直接等同于无法判断。([财政说明](/Users/lchingen/hivemind/src/hivemind/universe.py:115), [D260](/Users/lchingen/hivemind/docs/DECISIONS-log.md:3049))

**(d) 检查。** 先对所有保存的生产答案做 E3 的零成本拒绝统计并逐条阅读，再决定移植。`empty_rung` 检查有限上下界的空区间；`band_problem` 只识别特定英文“within X%”表达，不能证明所有文字与数字一致。D186 的方向也不能仅靠这两个检查解决。D368 要求在下一抽取版本实现它；这个新独立调用是否属于该版本，应明确问 Alex，而不是默认推迟。([检查实现](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/split.py:408), [D368](/Users/lchingen/hivemind/docs/DECISIONS-log.md:3960))

**(e) 测试不能空过。** 16 个匹配是有用控制，**不是 16 个独立问题**，也不能覆盖另外 18 条或证明一般质量。比较前须逐个确认问题、期间、截止日和单位相同；不同的单列，不能硬比。([结果限制](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:2686))

- **A 阶段**必须覆盖 34/34，分别报告成功、拒绝、无区间；任何被写出的区间若经复核改变原问题、日期或有重叠／空档，则失败。预先写明最低可用数量与类别，不能让 34 个全拒绝也算通过。
- **B 阶段**必须审阅所有实际判断，并报告区间成功数、曾被判断的问题数、每次判断数、拒绝和中断；出现经仲裁的无依据判断即失败。若没有达到预先规定的可判断数量，结果是**未完成**，不是通过。控制中的日期不一致案例不能算作成功对照。

**(f) Stage 0 的停止条件。** 如果独立读者确认：**按 v2 的“选一个结果并保留原问题身份”会让至少一个被写出的答案改变原问题，而设计没有一个符合现行决定的处理方式**，就先停止该方案，不向 Alex 请求按它构建。u2 clean-10 是必须检验的反例；停止的是这个未经解决的契约，不是因为它没有数字参照或精确日期。

所以我建议：先完成 34 条盲读和 E3 的零成本检查，修订这一个契约；再把**单独生成区间、通过后接冻结判断**作为一个建设建议和分阶段测试提交 Alex。