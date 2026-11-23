这批代码暂不建议提交：Step 2 可能把未核实的引文当作原文，也可能因为 Step 1 已记录的未解决链接而中断。

例如，Step 1 已标记一段引文找不到原文；Step 2 仍把模型生成的那段文字交给比较，并存进证据库，没有保留“未核实”标记。

### BLOCKERS

- [run_forward.py:52](/Users/lchingen/hivemind/clean-arch/step2/run_forward.py:52) 使用 `source_passages`，丢弃了 Step 1 的 `verified_source_passages` 和查找错误。修复过的引文仍以模型文字进入比较；找不到的引文也会被保存为普通 `passages`。结果中的来源文字因此可能不是原文，且读者看不到警告。
- [run_forward.py:58](/Users/lchingen/hivemind/clean-arch/step2/run_forward.py:58) 把所有链接直接变成问题 ID，包括 Step 1 已记录为未解决的链接。随后 [run_forward.py:75](/Users/lchingen/hivemind/clean-arch/step2/run_forward.py:75) 用该 ID 查问题，触发 `KeyError`，整次运行中断。Step 1 对这种情况明确允许继续并留待检查。
- [library.py:54](/Users/lchingen/hivemind/clean-arch/step3/library.py:54) 对已有记录 ID 只检查存放位置，不检查记录内容。相同 ID 带着不同摘要或来源再次写入时，旧内容被保留，新链接却会被加到旧内容上，违反“一条记录的 ID 只代表同一件事”。现有 [test_library.py:77](/Users/lchingen/hivemind/clean-arch/step3/test_library.py:77) 只检查补链接，没有覆盖内容变化。
- [compare.py:134](/Users/lchingen/hivemind/clean-arch/step2/compare.py:134) 普通比较调用失败后立即拒收记录，没有按 [设计约定](/Users/lchingen/hivemind/clean-arch/STEP1-CONDITIONS-DESIGN.md:172) 重试一次。一个短暂失败就会丢掉本可在重试中成功的记录；[测试](/Users/lchingen/hivemind/clean-arch/step2/test_compare.py:138) 反而固定了立即拒收的行为。
- 提交范围里有 **66 个 `.jsonl`、66 个 `.stderr`、11 个 `.pid` 和两个 `.patch`** 临时文件，例如 [a-codex.jsonl](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/council/a-codex.jsonl)。应从提交中排除原始事件流、进程文件和临时补丁。

### SHOULD FIX

- [run_forward.py:103](/Users/lchingen/hivemind/clean-arch/step2/run_forward.py:103) 即使有比较被拒收或后续链接仍待处理，也写出结果并以退出码 0 结束。自动调用方会把不完整结果当成成功；至少应让退出状态明确反映未完成。
- [model.py:130](/Users/lchingen/hivemind/src/hivemind/model.py:130) 保留了最后一次 HTTP 错误，但后续网络错误不会清除它。若先收到 HTTP 500、最后一次超时，最终异常的文字描述超时，附带的状态码和响应体却来自较早的 500，容易误判最后一次失败。
- [run_forward.py:41](/Users/lchingen/hivemind/clean-arch/step2/run_forward.py:41) 每个输入片段打开 SQLite 连接但不关闭；多片段调用会泄漏连接。
- 默认生产路径经代码对照仍是最多三次尝试，失败后依次等待 **5、10、15 秒**；但新增测试只覆盖一次尝试，没有保护这个默认行为。

### NITS

- [runner.py:202](/Users/lchingen/hivemind/clean-arch/step1/runner.py:202) 等注释记载了决策历史；按 §3，可保留行为说明，把历史依据留在设计记录中。
- 将实现、测试、实验脚本和研究记录分组检查提交清单，会更容易审阅。脚本是否仍被外部手动使用无法仅凭引用搜索断定。

这是只读静态审查，未运行测试或付费调用。凭常见密钥格式搜索，没有发现明确的密钥；这不能证明所有文件都没有敏感内容。实验脚本只做了较轻的检查。

