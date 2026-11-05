复查发现 **1 个严重问题**：README 对花费上限的说明仍不完整，日终判断和并行中途的调用都可能让花费继续增加。

上一轮逐项核对：

- **并发设置：已解决。** [pipeline-plan.md:42](/Users/lchingen/hivemind/docs/poc/pipeline-plan.md:42) 写明“the measurement launcher passes its `HIVEMIND_WORKERS` there”。
- **超时和重试：已解决。** 同一行写明模型调用“180 s … up to three times”，Jev 调用“60 s, also up to three times”。
- **v16 有一次没有判断：已解决。** [CURRENT_STATE.md:21](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:21) 写明“One acceptance draw judged nothing on v16; its cause is not established”。
- **Idea 质量和稳定性的验收边界：已解决。** [CURRENT_STATE.md:24](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:24) 写明“broad analyst-prose quality and fresh Idea stability remain unaccepted”。
- **当前分支：按本轮范围不作为问题。** [CURRENT_STATE.md:12](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:12) 描述主目录“is the main checkout, where slice branches are cut from `main`”。
- **Docker 网络描述：已解决。** [README.md:153](/Users/lchingen/hivemind/README.md:153) 写明“container connectivity needs a fresh check before a container model run”。
- **40 次判断、两层依赖：已解决。** [pipeline-plan.md:42](/Users/lchingen/hivemind/docs/poc/pipeline-plan.md:42) 将数字限定为“on the 2026-11-02 runs”。
- **中国份额结果的解释：已解决。** [CURRENT_STATE.md:21](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:21) 写明“two readers found the starting figures did not cause the acceptance's drop”，并记录相同请求在两组运行中的保留差异。
- **找不到财报时继续运行：已解决。** [pipeline-plan.md:12](/Users/lchingen/hivemind/docs/poc/pipeline-plan.md:12) 写明“otherwise the step records that none was found and the run goes on”；[README.md:81](/Users/lchingen/hivemind/README.md:81) 的状态表也补上了“when one is found”。
- **花费上限的范围：部分解决。** [README.md:174](/Users/lchingen/hivemind/README.md:174) 现已写明“it is checked after each item”以及财报读取费用不计入，但仍漏掉下述日终判断和并行调用的情况。
- **较长运行的记录：已解决。** [CURRENT_STATE.md:21](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:21) 改为“no version of the current pipeline has completed a longer window”，并写明 60 天运行完成到 7 月 15 日后停止，链接到记录其局限的日志。

本轮新发现：

- **Serious — [README.md:174](/Users/lchingen/hivemind/README.md:174)：** “`--cap` stops the run once its items' spend passes the cap”及“the last item can pass it”仍不足以说明实际花费。代码在处理每个条目后检查上限，但在这之后才运行日终判断，且判断后没有再次检查；若这是最后一天，运行可以在判断费用使总额超过上限后正常结束。并行模式下，提前发出的调用也可能在停止时仍产生费用。[replay.py:112](/Users/lchingen/hivemind/src/hivemind/replay.py:112)、[replay.py:120](/Users/lchingen/hivemind/src/hivemind/replay.py:120)、[parallel_day.py:170](/Users/lchingen/hivemind/src/hivemind/parallel_day.py:170)。**修复：**说明上限在条目完成后检查，日终判断不会立即触发检查，并行运行中已发出的调用仍可能增加费用；因此它不是整个运行的硬上限。

serious: 1, wording: 0