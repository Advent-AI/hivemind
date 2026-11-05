复查发现 3 个严重问题；上一轮的三项新发现中，财报读取的说明仍有一处遗漏。

上一轮逐项核对：

- **并发设置：已解决。** [pipeline-plan.md:42](/Users/lchingen/hivemind/docs/poc/pipeline-plan.md:42) 写明“`--workers` … the measurement launcher passes its `HIVEMIND_WORKERS` there”。
- **超时和重试：已解决。** 同一行写明模型调用“180 s … up to three times”，Jev 调用“60 s, also up to three times”。
- **v16 有一次没有判断：已解决。** [CURRENT_STATE.md:20](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:20) 写明“One acceptance draw judged nothing on v16; its cause is not established”。
- **Idea 质量和稳定性的验收边界：已解决。** [CURRENT_STATE.md:23](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:23) 写明“broad analyst-prose quality and fresh Idea stability remain unaccepted”。
- **当前分支：按本轮审查范围，不再作为问题。** [CURRENT_STATE.md:12](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:12) 写的是主目录“is the main checkout, where slice branches are cut from `main`”。用户已明确状态页描述主 checkout，而非这次临时审查分支。
- **Docker 网络描述：已解决。** [README.md:153](/Users/lchingen/hivemind/README.md:153) 写明“container connectivity needs a fresh check before a container model run”。
- **40 次判断、两层依赖：已解决。** [pipeline-plan.md:42](/Users/lchingen/hivemind/docs/poc/pipeline-plan.md:42) 现在将其限定为“on the 2026-11-02 runs”。
- **中国份额结果的解释：已解决。** [CURRENT_STATE.md:20](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:20) 写明两位读者认为起始数字没有造成下降，并记录相同抽取请求在两组运行中的保留差异。
- **找不到财报时继续运行：部分解决。** [pipeline-plan.md:12](/Users/lchingen/hivemind/docs/poc/pipeline-plan.md:12) 写明“otherwise the step records that none was found and the run goes on”；[README.md:45](/Users/lchingen/hivemind/README.md:45) 和 [CURRENT_STATE.md:7](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:7) 也加了“when one is found”。但 README 的状态表仍有一处无条件描述，见下。

本轮发现：

- **Serious — [README.md:81](/Users/lchingen/hivemind/README.md:81)：** 状态表仍写“at coverage start each question reads the company's latest earnings report once”，没有限定找到报告的情况。[baseline.py:127](/Users/lchingen/hivemind/src/hivemind/baseline.py:127) 在没有符合条件的报告时返回空列表；[baseline.py:183](/Users/lchingen/hivemind/src/hivemind/baseline.py:183) 记录没有报告并继续。因此这一处仍会让读者误以为每次都有财报读取。**修复：**在表中也写明只有找到符合条件的报告才读取，否则记录并继续。
- **Serious — [README.md:166](/Users/lchingen/hivemind/README.md:166)：** 运行说明要求使用约定的花费上限，并在示例中给出 `--cap 3`，但没有说明它并不覆盖整个运行的花费。[scripts/replay.py:75](/Users/lchingen/hivemind/scripts/replay.py:75) 先运行可能产生模型费用的财报读取；之后 [replay.py:69](/Users/lchingen/hivemind/src/hivemind/replay.py:69) 才记下计算上限的起点，[replay.py:112](/Users/lchingen/hivemind/src/hivemind/replay.py:112) 在处理条目后检查差额。因此财报读取的费用不计入该上限，检查也不是发送前的硬上限。**修复：**说明 `--cap` 的实际范围和可能超出的情况，避免把它描述成全程硬上限。
- **Serious — [CURRENT_STATE.md:20](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:20)：** “no version of the current pipeline has run over a longer window” 抹掉了一次已停止的较长运行。[argument-record/log.md:39](/Users/lchingen/hivemind/docs/research/2026-11-04-argument-record/log.md:39) 记录 `poc-v108` 的 60 天运行在完成 7 月 15 日后被 Alex 叫停，也记录了复用存档时判断调用重新付费并发生分叉。它没有完成 60 天，但确实超过了 14 天。**修复：**写明没有版本完成较长窗口，并保留这次运行完成到 7 月 15 日即停止及其证据限制。

serious: 3, wording: 0

