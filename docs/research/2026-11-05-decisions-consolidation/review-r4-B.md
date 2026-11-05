上一轮的两处新增问题都已修改；当前阶段 PRD 的版本引用仍登记为待 Alex 决定。本轮另发现两处章节引用指错。

- **付费探针：按上一轮给定边界保留。** [AGENTS.md:326](/Users/lchingen/hivemind/AGENTS.md:326) 允许在方向已同意且没有停止指令时做“probes of a few cents on stored cases without asking”；[第 403 行](/Users/lchingen/hivemind/AGENTS.md:403) 要求更大范围的付费发送经 Alex 明确同意。[第 328 行](/Users/lchingen/hivemind/AGENTS.md:328) 保留“a result that contradicts the hypothesis stops the line and goes to him”。

- **交给 Alex 的事项：已解决。** [AGENTS.md:37](/Users/lchingen/hivemind/AGENTS.md:37) 区分“a choice that changes what the system does, as the question, its options and your recommendation”和“a next step of work, as one recommendation and one test”。

- **更正记录：已解决。** [AGENTS.md:247](/Users/lchingen/hivemind/AGENTS.md:247) 要求记录“its reason and its before and after, printed with every score and never merged in”。

- **当前阶段 PRD 的标准版本：仍待 Alex 决定。** [决策登记:44](/Users/lchingen/hivemind/docs/DECISIONS.md:44) 记录“§4 calls the frozen standard ‘version 3’ (the page is version 5)”及“PRD 10 changes only on Alex's word”。本轮没有审查该 PRD 的修改。

- **跨媒体重复陈述的启用条件：已解决。** [AGENTS.md:124](/Users/lchingen/hivemind/AGENTS.md:124) 保留“switched on only after its merge risk on the gold and the accuracy of the original speaker and day fields are measured”。

- **给 Alex 审阅的页面语言：已标明未确认。** [AGENTS.md:449](/Users/lchingen/hivemind/AGENTS.md:449) 写明“the practice since then, not yet confirmed by him”。

- **第 8 节的跨媒体表述：已解决。** [AGENTS.md:376](/Users/lchingen/hivemind/AGENTS.md:376) 在该表述后加入“how code applies it: §3, Identity”，指向上述启用条件。

- **颗粒度研究的章节引用：已解决。** [docs/granularity-research.md:24](/Users/lchingen/hivemind/docs/granularity-research.md:24) 现在写“AGENTS §7.3：模型调用是一次采样”；[AGENTS.md:321](/Users/lchingen/hivemind/AGENTS.md:321) 确有“A model call is a sampler”。

- **Serious — [docs/superpowers/plans/2026-10-23-nvda-poc.md:16](/Users/lchingen/hivemind/docs/superpowers/plans/2026-10-23-nvda-poc.md:16) 和 [第 66 行](/Users/lchingen/hivemind/docs/superpowers/plans/2026-10-23-nvda-poc.md:66)：章节引用指向了不存在的禁令。** 两处分别说“ No product code until Alex starts the build (AGENTS.md §11)”和启动构建会“lifts AGENTS.md §11”。但现行 [AGENTS.md §11](/Users/lchingen/hivemind/AGENTS.md:432) 讲的是设计文档与决策记录，没有这条禁令。旧版 §11 当时也写的是“the POC build started on 2026-10-23 under recorded decisions”。**修正：**把两处改成历史状态的准确出处，例如指向启动该 POC 的 D62，不再引用 §11。

- **Serious — [docs/superpowers/plans/2026-10-23-nvda-poc.md:21](/Users/lchingen/hivemind/docs/superpowers/plans/2026-10-23-nvda-poc.md:21)：模型调用记录要求的 AGENTS 章节引用不成立。** 该行把保存配置版本、校验和、请求、原始答案及用量归于“AGENTS.md §6”；现行 [§6](/Users/lchingen/hivemind/AGENTS.md:184) 是提示词写法，没有列出这项完整记录要求。该行同时引用了 `03-config.md`，所以可以保留其产品规范出处。**修正：**删除错误的 AGENTS §6 引用，保留并核实该行的配置规范引用。

serious: 2, wording: 0