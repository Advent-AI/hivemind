仍有 **两个 blocker**，暂不建议提交。

- [run_forward.py:58](/Users/lchingen/hivemind/clean-arch/step2/run_forward.py:58) 忽略了链接类型，也没有使用 Step 1 已记录的未解决链接。例如，一个不存在的“新问题”恰好与已有问题同名时，会被当作已解决并连到已有问题；反过来，已有问题 ID 与新问题的临时 ID 相同时，也可能连错问题。现有测试只覆盖了 ID 不冲突的情况。
- [library.py:127](/Users/lchingen/hivemind/clean-arch/step3/library.py:127) 虽然现在保存了核实结果，但给读者看的文字仍一律把模型文字标为“Quote”。[compare.py:40](/Users/lchingen/hivemind/clean-arch/step2/compare.py:40) 同样把未核实文字作为引文交给比较。找到的原文和未找到的文字仍没有在这些使用处区分。

其余所列修复已在代码中看到；本次遵守只读要求，没有重跑测试或核验运行结果。

**BLOCKER：先修正链接识别和引文使用处的标记。**