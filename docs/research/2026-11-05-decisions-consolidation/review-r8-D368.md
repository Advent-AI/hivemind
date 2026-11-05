发现 3 个严重问题；均未修改文件。

1. **译文把读取方向写反了。** [10-filing-phase.md:62](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md:62) 写成主题题排在总收入题之后，并由主题题读取前一天的结论。实际是总收入题先判断，读取了部分主题题前一天的结论；随后主题题才判断。[独立审查记录](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/review-core-codex.md:11)和[判断代码](/Users/lchingen/hivemind/src/hivemind/views/judging.py:76)支持这一方向。**修复：**明确写总收入题读取了主题题前一天的结论。

2. **已决定的事项仍被写成等待 Alex 决定。** [10-filing-phase.md:62](/Users/lchingen/hivemind/docs/prd/10-filing-phase.md:62)末尾仍说箭头问题“for Alex to decide”；[05-extraction.md:201](/Users/lchingen/hivemind/docs/prd/05-extraction.md:201)也把下一抽取版本的两项改动指向“Open for Alex”。但 [D368 第 1、4 项](/Users/lchingen/hivemind/docs/DECISIONS-log.md:3965)已记录决定，登记表也说七项均已回答。**修复：**前者注明已由 D368 决定、修复尚待建；后者指向登记表中下一抽取版本的条目，而不是开放事项。

3. **更正记录中三处引文并非去掉 HTML 标签后的逐字原文。** [05-extraction-standard-corrections.md:12](/Users/lchingen/hivemind/docs/prd/05-extraction-standard-corrections.md:12)、[第 22 行](/Users/lchingen/hivemind/docs/prd/05-extraction-standard-corrections.md:22)和[第 31 行](/Users/lchingen/hivemind/docs/prd/05-extraction-standard-corrections.md:31)在 `D211`、`D201`、`PRD 06` 前加入了空格；[原页面](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:318)去掉标签后没有这些空格。记录同时声称每句均为逐字引用。**修复：**按去标签后的文本逐字引用，或将来源标记移出引号。不要修改冻结页面。

serious: 3