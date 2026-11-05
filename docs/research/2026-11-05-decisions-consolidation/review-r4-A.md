上一轮的两项严重遗漏都已补上；再复核时发现四处严重问题。

上一轮及更早九项的状态：

1. **Pull mode：已解决。** 当前写明 “The closing is built; the successor step is not”。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:37)
2. **比较和分析师解读：已解决。** 当前保留 “a competitor's comparison”、同句中的 “adoption”，以及 “no new fact or calculation”。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:280)
3. **主题变化后的重判范围：已解决。** 当前限定为 “every open asset question with evidence in force”。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:194)
4. **Coverage-start 提示词冻结：已解决。** 当前写明 “frozen with its check: no further prompt version without Alex's decision”。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:257)
5. **外部 agent 的操作说明：已解决。** 当前写明提供 “the workflow recipe and the object list”。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:292)
6. **无标签表格：已解决。** 当前写明 “tables without tags are read by the model with no separate parsing code”。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:139)
7. **D9 索引：已解决。** 当前指向 “§1 System”。[索引](/Users/lchingen/hivemind/docs/DECISIONS.md:345)
8. **另一家公司的事项：已解决。** 当前使用 “one cannot say how it moves a question”。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:280)
9. **D367 索引：已解决。** 开头有 `consolidation` 锚点并引用 D367；索引指向该锚点。[开头](/Users/lchingen/hivemind/docs/DECISIONS.md:13)，[索引](/Users/lchingen/hivemind/docs/DECISIONS.md:701)
10. **多家媒体转载同一陈述：已解决。** 当前列出 “same known original speaker, original day and figures”、未知发言人或日期不匹配，以及 “every piece still stored”。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:181)
11. **问题树的七类驱动、归属和读取方式：已解决。** 当前列出七类、每个驱动声明所支持的根问题，并写明根问题读取结论；除种子外标为未建成。[登记表](/Users/lchingen/hivemind/docs/DECISIONS.md:190)

本轮发现：

- **Serious — [docs/DECISIONS.md:58](/Users/lchingen/hivemind/docs/DECISIONS.md:58)：** “Settled”部分说每天重判证据改变的问题，漏掉依赖问题的结论改变也会触发重判。同一登记表的判断部分写的是 “what it reads changed”，包括依赖结论和主题变化。[D63](/Users/lchingen/hivemind/docs/decisions/log.md:1685)要求将结论改变的依赖方加入当日轮次。**修复：**这里改为判断所读取的内容发生变化的问题，并涵盖依赖和主题结论变化。

- **Serious — [docs/DECISIONS.md:190](/Users/lchingen/hivemind/docs/DECISIONS.md:190)：** 问题树仍漏掉已决定的宏观主题结构：不同公司的影响方向由声明的依赖及其传导说明提供，判断时读取该说明；宏观证据只归入宏观主题。[D208](/Users/lchingen/hivemind/docs/decisions/log.md:2641)写明 “direction per company is a declared dependency with a channel sentence the judge reads” 和 “macro evidence is filed only under the macro theme”。**修复：**补上这两项，继续标明相关设计尚未建成。

- **Serious — [docs/DECISIONS.md:254](/Users/lchingen/hivemind/docs/DECISIONS.md:254)：** D360 在索引中标为有效并指向第 10 节，但该节只记录了测量规则，漏掉 D360 决定的归属规则：一段话涉及两个具体问题时，归到它最直接衡量的问题；分别给出两个数值时，分别形成两个证据项。[D360](/Users/lchingen/hivemind/docs/decisions/log.md:3836)同时说明，代码把引用同一句话的两个项存为一条带两个链接的记录。**修复：**把决定的这两条写入第 10 节，并保留 v74l 测试失败、未进入产品的状态，避免把设计说成当前实现。

- **Serious — [docs/DECISIONS.md:289](/Users/lchingen/hivemind/docs/DECISIONS.md:289)：** “A search with no thesis on what the idea names returns `null`”省略了文字匹配和相似度条件，可能让读者以为只要没有对应已命名对象的问题就返回空。[D91](/Users/lchingen/hivemind/docs/decisions/log.md:1816)要求同时检查对象名称和库内文字；[D132](/Users/lchingen/hivemind/docs/decisions/log.md:1998)进一步规定，只有未命名对象、没有文字匹配且最高相似度低于 0.30 才返回 `null`。**修复：**写出三个条件，以及超过相似度门槛但没有命名对象的想法仍交给模型。

复核范围说明：我检查了分类记录中有效且非前端的决定是否在索引前被引用，并核对了上面报告问题的原始日志；但没有完成对第 1–15 节和七个开放项的**每一句**与全部后续决定的逐句核对。因此这四项是已核实的发现，不能据此声称其余内容已全部通过。

serious: 4, wording: 0