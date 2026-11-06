**没有发现会使这次 A/B 比较失效，或已证实混入 8 月 29 日记录的严重错误。**这是一项只读审查；没有修改文件，也没有发送模型请求。

例如，同一篇文章的两组请求都使用同一份 68 个问题的历史列表；代码检查去掉新增财报后，两组请求的序列化内容完全一致。三篇文章的列表也彼此相同，并且我从实际快照重新计算后，均与保存的列表一致。相关构造和比较见 [run_existing_library_pilot.py](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/run_existing_library_pilot.py:58)。

- **截止日期和快照：**实际快照最后完成的日期是 8 月 28 日、序号 1204。我逐表检查了现有的序号字段，没有发现大于 1204 的记录；源库中对应的 8 月 29 日部分记录已从副本移除。快照、来源库和问题列表的指纹记录见 [snapshot.json](/Users/lchingen/hivemind-no-preseed-evidence-review/poc/data/pilot-d369-existing-library-v2/snapshot.json:1)。这个库本身可能有不完美的问题，也不是三篇文章发表当天的完整状态；这正是本诊断需要明确报告的限制。
- **文章、财报和引用：**预检代码核对三篇文章的身份、正文指纹、来源和时间顺序，并检查参考引用确实出现在文章中；财报发布时间早于三篇文章。两组输出都以文章正文检查引用，财报中独有的句子不会作为文章引用通过。见 [preflight_archived_variants.py](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/preflight_archived_variants.py:45)。
- **指纹和发送：**协议中列出的文件指纹目前全部吻合；我重新构造的六个请求也全部吻合协议中的请求指纹。真实发送前还会检查实际请求的序列化内容，然后调用生产传输函数。见 [run_existing_library_pilot.py](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/run_existing_library_pilot.py:85) 和 [model.py](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/model.py:128)。
- **三次采样：**每次运行计划六个请求，每个请求使用新的独立存档，并拒绝缓存命中；需要分别运行三次，代码本身不强制三次都完成或编号各不重复。六个是每次的**逻辑请求数**：生产传输遇到部分网络错误时可能重试，所以实际 HTTP 发送次数可能更多。见 [run_existing_library_pilot.py](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-real-input-evidence/run_existing_library_pilot.py:118)。

我核对了预检与输出检查的代码，但没有运行会创建临时文件的完整预检，也没有实际模型输出可供验证；后续 writer 不在本次审查范围内。