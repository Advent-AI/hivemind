- **Serious — [docs/DECISIONS.md:264](/Users/lchingen/hivemind/docs/DECISIONS.md:264):** 登记表说修复后的表格引用保存为报告的“exact row”，但代码只保存从行标签到目标数值的原文片段，可能不包含后面的单元格。[baseline.py:50](/Users/lchingen/hivemind/src/hivemind/baseline.py:50) 明确写的是“from the quote’s label to its figure”，并在 [第 77 行](/Users/lchingen/hivemind/src/hivemind/baseline.py:77)返回该片段。例如，原文 `Revenue* 10 20 30` 的修复结果是 `Revenue* 10`。**修正：**将“exact row”改为“报告中从行标签到目标数值的原文片段”。

本轮核对了有效的非前端决定是否在正文出现，以及索引状态是否与分类记录一致；两项均未发现遗漏或不一致。我没有完成第 1–15 节所有条目和所有后续决定的逐句核对，因此这不是完整通过确认。

serious: 1, wording: 0