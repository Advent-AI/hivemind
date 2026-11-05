上一轮的七项问题都已修复；本轮又发现两处需要修改。

1. **已解决：pull mode。** [登记表第 34–36 行](/Users/lchingen/hivemind/docs/DECISIONS.md:34)现在写明：“The closing is built; the successor step is not.”
2. **已解决：比较和分析师解读。** [第 273–276 行](/Users/lchingen/hivemind/docs/DECISIONS.md:273)现在保留了竞争对手比较、同句中的采用情况，以及“new fact or calculation”的例外。
3. **已解决：主题变化后的重判范围。** [第 189 行](/Users/lchingen/hivemind/docs/DECISIONS.md:189)现在限定为“every open asset question **with evidence in force**.”
4. **已解决：coverage-start 提示词冻结。** [第 250–251 行](/Users/lchingen/hivemind/docs/DECISIONS.md:250)现在写明“frozen with its check: no further prompt version without Alex's decision”。
5. **已解决：外部 agent 的操作说明。** [第 285–286 行](/Users/lchingen/hivemind/docs/DECISIONS.md:285)现在写明 MCP front 向外部 agent 提供“the workflow recipe and the object list”，并引用 D134、D135。
6. **已解决：无标签表格。** [第 136–137 行](/Users/lchingen/hivemind/docs/DECISIONS.md:136)现在写明“tables without tags are read by the model with no separate parsing code”，并引用 D23。
7. **已解决：D9 索引。** [第 338 行](/Users/lchingen/hivemind/docs/DECISIONS.md:338)现在指向“§1 System”。

本轮新发现：

- **Serious — [docs/DECISIONS.md:273](/Users/lchingen/hivemind/docs/DECISIONS.md:273)：** “another company's matter with **no stated path**”比 D250 更严格。它会把文章没有明确写出传导路径、但分析师能够说清该路径的事项排除。D250 的原话是：“Another company's matter that **one cannot say moves a question** about the company through a path such as demand, supply, competition or pricing is not kept” ([log:2981](/Users/lchingen/hivemind/docs/decisions/log.md:2981))。**修复：**改为无法说清其如何通过这些路径影响公司问题的事项不保留，避免要求路径必须由原文明确写出。

- **Serious — [docs/DECISIONS.md:695](/Users/lchingen/hivemind/docs/DECISIONS.md:695)：** D367 的索引指向“§15 Working rules”，但该章节没有记载或引用 D367。索引承诺最后一列指出承载该决策的章节 ([register:326](/Users/lchingen/hivemind/docs/DECISIONS.md:326))；D367 实际记录的是登记表、完整日志和前端决策文件的整理结果 ([log:3934](/Users/lchingen/hivemind/docs/decisions/log.md:3934))，这些内容出现在登记表开头，而非 §15。**修复：**将索引指向登记表开头，并给该位置一个可定位的标题或锚点。

索引中 D1–D366 的 **in-force 与非 in-force 状态**和 `final.jsonl` 一致；非前端的在力决策也都在正文中有编号引用，D289 包含在 D288–D290 范围中。七个 open item 的描述没有发现其他经源记录证实的问题。

这轮检查不构成对所有摘要句子和后续修订均已逐句核实的证明。

serious: 2, wording: 0