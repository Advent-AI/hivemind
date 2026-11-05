上一轮的六项中，五项已解决；工作树分支信息仍未写明。

- **并发设置：已解决。** [pipeline-plan.md:42](/Users/lchingen/hivemind/docs/poc/pipeline-plan.md:42) 现写明：“`--workers` … the measurement launcher passes its `HIVEMIND_WORKERS` there”。
- **超时和重试：已解决。** 同一行现分别写明模型调用“180 s … up to three times”和 Jev 调用“60 s, also up to three times”。
- **v16 有一次没有判断：已解决。** [CURRENT_STATE.md:20](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:20) 现写明：“one acceptance draw judged nothing on v16”。
- **Idea 质量和稳定性的验收边界：已解决。** [CURRENT_STATE.md:23](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:23) 现写明：“broad analyst-prose quality and fresh Idea stability remain unaccepted”。
- **当前分支：部分解决。** [CURRENT_STATE.md:12](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:12) 现在说主目录“is the main checkout, where slice branches are cut from `main`”，不再直接说它当前位于 `main`；但仍未写出当前分支。`git worktree list` 显示该目录位于 `docs/consolidate-2026-11-05`，HEAD 为 `20ab1bd`。应写出这个状态，让读者知道正在审查的未提交修改属于哪个分支。
- **Docker 网络描述：已解决。** [README.md:152](/Users/lchingen/hivemind/README.md:152) 现写明：“The recorded VPN setup on this Mac blocked … container connectivity needs a fresh check”。

本轮新发现：

- **Serious — [pipeline-plan.md:42](/Users/lchingen/hivemind/docs/poc/pipeline-plan.md:42)：** 文档把一次运行中的规模写成了普遍上限：“a day's round is up to 40 judgements in two dependency levels, themes then assets”。[judging.py:285](/Users/lchingen/hivemind/src/hivemind/views/judging.py:285) 说明代码按依赖顺序逐层处理；[judging.py:310](/Users/lchingen/hivemind/src/hivemind/views/judging.py:310) 每次选取当前可处理的一层，代码没有把总判断数限制为 40，也没有把依赖层数限制为两层。**修复：** 把 40 条、两层标为 2026-11-02 所观察运行的规模；保留当前代码每次最多并发 32 个判断的说明。

- **Serious — [CURRENT_STATE.md:20](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:20)：** “neither cause is established” 抹掉了对中国份额结果已经查明的一部分解释。[acceptance-design.md:52](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/acceptance-design.md:52) 记录两位读者认为起始数字没有造成这次下降；同一段指出，相同请求中，抽取在候选运行的两次保留了黄仁勋关于份额归零的陈述，在对照运行的两次丢掉了它。这不证明所有波动的完整原因，但比“原因均未查明”更具体。**修复：** 保留 v16 原因未查明的表述，同时写出 v17 已观察到的抽取差异和两位读者对起始数字的判断。

- **Serious — [README.md:45](/Users/lchingen/hivemind/README.md:45)、[pipeline-plan.md:12](/Users/lchingen/hivemind/docs/poc/pipeline-plan.md:12)、[CURRENT_STATE.md:7](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:7)：** 三处都无条件地说覆盖开始时会读取最新财报，但代码允许找不到财报时继续运行。[baseline.py:127](/Users/lchingen/hivemind/src/hivemind/baseline.py:127) 在没有符合条件的报告时返回空列表；[baseline.py:183](/Users/lchingen/hivemind/src/hivemind/baseline.py:183) 随后记录“no earnings report …”，将该步骤标为 `ok` 并继续，没有读取任何报告。读者可能因此以为运行一定有起始财务数据。**修复：** 在流程说明中写明：找到符合条件的报告时才读取；找不到时记录这一结果并继续，起始数字为空。

本轮未发现三份文件中的 Markdown 文件链接失效。审查期间 `CURRENT_STATE.md` 仍有并行修改；以上行号以最后一次读取为准。

serious: 3, wording: 0