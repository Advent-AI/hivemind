**这个设计还不能安全地跑七天。** 例如，一道问题没有到期日和判断档位，即使当天成功写入证据，现有代码仍会尝试判断它；而判断检查不可能接受一个不存在的档位，整天会停下来。

1. **空档位和空日期的四种组合没有定义完整。** 现有日终判断会处理有新证据的问题，并未检查档位是否为空；空档位会让任何判断结果都被拒绝。[判断入口](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/views/judging.py:300)；[结果检查](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/views/judging.py:211)。另外，到期日已知但档位为空时，现有日终关闭仍会把问题关闭，之后它就不能继续收集证据。设计需要分别写清日期有无、档位有无的行为，尤其是到期当天和次日。[日终关闭](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/pull.py:30)

2. **后续问题会直接报错。** 设计提到要安全处理空档位，但保留的写入路径对后续问题调用 `ladder_direction`；这个函数直接读取第一个和最后一个档位，空列表会报错。新问题和前一期问题的档位都可能为空，单测只覆盖普通新问题不够。[写入](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/views/writing.py:72)；[读取档位](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/views/matching.py:72)

3. **“保留每个意思”还没有落到实际写入规则。** 同一句话可能同时说总收入和数据中心收入；现有检查会留下第一条摘要，把两个问题的链接合并，第二条摘要消失。设计说绕过这一步，但没有定义两路重复同一事实、同一句包含两个事实、候选问题被合并或不被打开时，各自如何保存和连接。尤其现有写入器会丢掉只连到未打开候选的证据。[真实例子](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/trace-structure-review.zh.md:29)；[写入器](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/views/writing.py:206)

4. **绕过旧检查的范围过大。** 设计只要求核对原文和引用 ID，但旧检查还处理问题期间、对象和身份字段；这些字段会影响实际匹配以及是否把两个问题合并。准备步骤若只写“主体和来源”，并不能保证写入器所需字段齐全或含义正确。应逐字段列明来源、未知值和保留哪些既有检查，再对照实际写入结果。[旧检查](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/extraction.py:638)；[身份判断](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/views/identity.py:17)

5. **中断恢复尚未覆盖拆分后的步骤。** 现有流程保存的是一份完成的交接结果；它没有分别记录 A、B 和准备步骤的完成状态。若 A 返回后崩溃，设计没有说明恢复时复用什么、如何保证 B 看到同一文章和日初问题，以及如何避免重复写入。需要逐个测试回答后、匹配后和写入前后的中断。[现有恢复路径](/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/views/round.py:97)

6. **起始题库的历史真实性仍未证实。** 复制 8 月 28 日的 68 题，可以避免使用七天结束后的题库，但不能证明每道题的来源当时已经可获得，也不能证明题库完整。Alex 要求的是由测试开始前真实材料建立或还原的状态；现有记录明确说这份题库尚未充分核实。设计只过滤七天内的文章版本，没有解决起始库的问题。[起始状态纠正](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/point-in-time-start-correction-2026-11-05.zh.md:3)

另一个依据缺口是：[设计开头](/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-05-seven-day-request/optional-fields-poc-design.md:3)称 Alex 最新决定替代了强制日期和档位，但没有引用他的原话或对应决定记录；我在当前决定和状态文件中也没有找到这条决定的原文，因此无法核实授权边界。设计中的空日期、空档位行为应分别标明哪些是 Alex 已决定的，哪些是实验方案。

建议先用**已保存的真实回答**做一次不花钱的完整测试：覆盖四种日期和档位组合、后续问题、同句不同事实，以及中断恢复；检查最终保存的证据和次日实际看到的问题。通过后再决定七天运行。没有修改文件。