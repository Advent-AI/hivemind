# PRD 目录

每个模块一份 PRD，用 Markdown 写。在设计页（docs/system-design.html）点开模块，右侧点“查看 PRD”就能看到；页面顶部的“查看系统 PRD”是总览。

| 文件 | 模块 | 状态 |
|---|---|---|
| 00-system.md | 系统总览 | 主线已画出 |
| 01-universe.md | 研究对象名单 | 第一版已冻结 |
| 02-classification.md | 分类（上游完成） | 第一版已冻结 |
| 03-config.md | Config | 第一版已冻结 |
| 04-dispatch.md | 分发 | 第一版已冻结 |
| 05-code-processing.md | 代码处理 | 未设计 |
| 06-model-extraction.md | 模型抽取 | 未设计 |
| 07-research-store.md | 研究库 | 部分确定 |
| 08-thesis.md | 研究结论 | 未设计 |
| 09-pull-mode.md | Pull 模式 | 未设计 |
| 10-review-pool.md | 人工复核池 | 只定了哪些会进来 |

## 规矩

- 依据的顺序：Alex 的话 > docs/DECISIONS.md > PRD 和设计页。PRD 和 DECISIONS 不一致时，以 DECISIONS 为准，并改 PRD。
- 改了设计页或做了新决定，同一次改动里同步改对应的 PRD。
- 改了任何 .md 之后，跑一次 `python3 docs/prd/build_bundle.py`。直接双击打开设计页时，页面读的是打包副本；`python3 docs/prd/build_bundle.py --check` 能查出副本是否过期。
