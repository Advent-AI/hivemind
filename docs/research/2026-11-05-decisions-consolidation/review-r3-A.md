上一轮的九项都已解决；本轮发现两处严重遗漏。以下结论基于已核对的条目，**尚不能证明登记表全部摘要和后续修订都已逐句核实**。

上一轮逐项复核：

1. **Pull mode：已解决。** 现写明“The closing is built; the successor step is not”。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:34)
2. **比较和分析师解读：已解决。** 现保留竞争对手比较、同句中的采用情况，以及“no new fact or calculation”的边界。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:273)
3. **主题变化后的重判范围：已解决。** 现限定为“every open asset question with evidence in force”。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:187)
4. **Coverage-start 提示词冻结：已解决。** 现写明“frozen with its check: no further prompt version without Alex’s decision”。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:250)
5. **外部 agent 的操作说明：已解决。** 现写明提供“the workflow recipe and the object list”。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:285)
6. **无标签表格：已解决。** 现写明“tables without tags are read by the model with no separate parsing code”。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:136)
7. **D9 索引：已解决。** 现指向“§1 System”。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:338)
8. **另一家公司的事项：已解决。** 现写明“one cannot say how it moves a question”，不再要求文章明确写出传导路径。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:273)
9. **D367 索引：已解决。** 现指向有锚点的“this page, opening”，开头也引用 D367。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:13)，[索引](/Users/lchingen/hivemind/docs/DECISIONS.md:695)

本轮发现：

- **Serious — [docs/DECISIONS.md:181](/Users/lchingen/hivemind/docs/DECISIONS.md:181)：** 登记表说同一陈述被多个媒体转载时，判断只看到一次，但漏掉了决定能否这样合并的条件。D248 要求**原始发言人、原始日期和数字都相同**；发言人或日期未知时不能匹配，而且每条来源记录仍要保存。[决策日志 D248 第 7 点](/Users/lchingen/hivemind/docs/decisions/log.md:2970) 没有这些条件，登记表会让人以为所有看似相同的转载都应合并。**修复：**补上三个匹配条件、未知值不匹配，以及每条记录仍保存。

- **Serious — [docs/DECISIONS.md:185](/Users/lchingen/hivemind/docs/DECISIONS.md:185)：** 对尚未建成的“问题树”设计，登记表只写了根问题、驱动层和共同主题，漏掉了 D208 已决定的关键结构：驱动层有**七个固定类别**；每个具体驱动声明它支持的根问题；根问题读取驱动和主题的结论，而不是直接读取它们的证据。[决策日志 D208](/Users/lchingen/hivemind/docs/decisions/log.md:2638) 这些决定会影响以后如何建造该功能。**修复：**在该条补上这些结构，并继续标明除种子问题外尚未建成。

serious: 2, wording: 0