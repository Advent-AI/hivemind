- **Serious — [docs/poc/pipeline-plan.md:38](/Users/lchingen/hivemind/docs/poc/pipeline-plan.md:38)：** 文档说费用“从归档的 token 数计算，绝不使用归档中保存的费用”。这与运行代码不符：[`Archive.totals()`](/Users/lchingen/hivemind/src/hivemind/model.py:97) 直接汇总保存的 `cost_usd`；[replay](/Users/lchingen/hivemind/src/hivemind/replay.py:112) 用这个汇总检查花费上限，并用它输出每日费用。**修复：**区分运行时上限和日志使用归档费用，与测量报告按 token 和公布费率重新计算费用。

serious: 1, wording: 0